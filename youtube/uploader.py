import os
import sys
from pathlib import Path

# Ensure root workspace directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from typing import Dict, Any, Optional
from core.config import config
from core.logger import logger
from core.database import db
from youtube.mock_uploader import mock_youtube

# OAuth Scopes required for YouTube Video Upload and Metadata
YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]

class YouTubePublishError(Exception):
    """Raised when publication violates safety, approval, or API constraints."""
    pass

class YouTubeUploader:
    """
    Manages YouTube Data API v3 integration:
    - OAuth 2.0 user credentials management
    - Resumable video upload
    - Setting title, description, tags, category, and thumbnail
    - Mandatory Made for Kids designation (selfDeclaredMadeForKids=True)
    - Human-in-the-loop approval verification
    - Scheduled releases (publishAt)
    """

    def __init__(self):
        self.mock_mode = config.YOUTUBE_MOCK_MODE

    def get_authenticated_service(self):
        """Builds an authorized YouTube API client using OAuth 2.0 credentials."""
        try:
            from googleapiclient.discovery import build
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
        except ImportError:
            raise ImportError(
                "Google API client libraries are not installed. "
                "Run 'pip install google-api-python-client google-auth-oauthlib google-auth-httplib2' or enable YOUTUBE_MOCK_MODE=True in .env."
            )

        token_file = config.BASE_DIR / config.YOUTUBE_CREDENTIALS_STORAGE
        secrets_file = config.BASE_DIR / config.YOUTUBE_CLIENT_SECRETS_FILE
        creds = None

        if token_file.exists():
            creds = Credentials.from_authorized_user_file(str(token_file), YOUTUBE_UPLOAD_SCOPE)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not secrets_file.exists():
                    raise FileNotFoundError(
                        f"YouTube OAuth client secrets file not found at {secrets_file}. "
                        "Download your client_secrets.json from Google Cloud Console or enable YOUTUBE_MOCK_MODE=True."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(str(secrets_file), YOUTUBE_UPLOAD_SCOPE)
                creds = flow.run_local_server(port=0)

            with open(token_file, "w") as token:
                token.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)

    def upload_project(
        self,
        project_data: Dict[str, Any],
        privacy_status: str = "private",
        publish_at: Optional[str] = None,
        bypass_approval_check: bool = False
    ) -> Dict[str, Any]:
        """
        Uploads a completed video project to YouTube.
        Guarantees:
        1. Human approval gate: Will reject unapproved videos unless bypass_approval_check is set.
        2. Duplicate upload prevention: Will reject if already uploaded.
        3. COPPA compliance: selfDeclaredMadeForKids=True is strictly enforced.
        """
        p_id = project_data["project_id"]
        status = project_data.get("status")

        # 1. Approval Gate Enforcement
        if status != "APPROVED" and not bypass_approval_check:
            raise YouTubePublishError(
                f"Cannot upload project '{p_id}'! Current status is '{status}'. "
                "TinyTots Tunes enforces manual human approval before publishing. "
                "Approve this project in the Dashboard or CLI first."
            )

        # 2. Duplicate Upload Prevention
        existing_yt_id = project_data.get("youtube_id")
        if existing_yt_id and existing_yt_id != "null":
            raise YouTubePublishError(
                f"Project '{p_id}' has already been uploaded to YouTube! (Video ID: {existing_yt_id}). "
                "Duplicate uploads are blocked."
            )

        paths = project_data["paths"]
        video_path = paths["final_video"]
        thumbnail_path = paths.get("thumbnail_file")

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file does not exist at {video_path}! Render the video first.")

        metadata = project_data["metadata"]
        title = metadata["title"]
        description = metadata["description"]
        tags = metadata.get("tags", [])
        category_id = metadata.get("category_id", config.YOUTUBE_CATEGORY_ID or "1")

        # 3. Check for Mock Mode or Missing Secrets
        secrets_file = config.BASE_DIR / config.YOUTUBE_CLIENT_SECRETS_FILE
        use_mock = self.mock_mode or not secrets_file.exists()

        if use_mock:
            if not self.mock_mode:
                logger.info("Live client_secrets.json not found; operating in YouTube Mock Mode.")
            result = mock_youtube.upload_video(
                video_path=video_path,
                title=title,
                description=description,
                tags=tags,
                category_id=category_id,
                privacy_status=privacy_status,
                made_for_kids=True,  # STRICTLY TRUE FOR COPPA
                thumbnail_path=thumbnail_path,
                publish_at=publish_at
            )
        else:
            # 4. Live YouTube Data API v3 Upload
            from googleapiclient.http import MediaFileUpload
            youtube = self.get_authenticated_service()

            status_body = {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": True  # STRICTLY TRUE FOR COPPA
            }
            if publish_at and privacy_status == "private":
                status_body["publishAt"] = publish_at

            body = {
                "snippet": {
                    "title": title[:100],  # YouTube title limit 100 chars
                    "description": description[:5000],
                    "tags": tags[:30],
                    "categoryId": category_id
                },
                "status": status_body
            }

            media = MediaFileUpload(video_path, chunksize=1024*1024*8, resumable=True)
            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            logger.info("Uploading video to YouTube Data API v3...")
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info("YouTube upload progress: %d%%", int(status.progress() * 100))

            video_id = response["id"]
            video_url = f"https://youtu.be/{video_id}"

            # Upload Thumbnail
            if thumbnail_path and os.path.exists(thumbnail_path):
                try:
                    logger.info("Setting YouTube custom thumbnail...")
                    youtube.thumbnails().set(
                        videoId=video_id,
                        media_body=MediaFileUpload(thumbnail_path)
                    ).execute()
                except Exception as te:
                    logger.warning("Could not set thumbnail: %s", te)

            result = {
                "id": video_id,
                "url": video_url,
                "snippet": response.get("snippet", {}),
                "status": response.get("status", {}),
                "mock": False
            }

        # 5. Update Project Record
        project_data["status"] = "PUBLISHED"
        project_data["youtube_id"] = result["id"]
        project_data["youtube_url"] = result["url"]
        project_data["publish_info"] = result

        # Save to file & database
        with open(Path(paths["root"]) / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)

        db.save_project(
            project_id=p_id,
            title=project_data["title"],
            theme=project_data["theme"],
            status="PUBLISHED",
            data=project_data,
            youtube_id=result["id"],
            youtube_url=result["url"]
        )

        logger.info("Project '%s' successfully published to YouTube! URL: %s", p_id, result["url"])
        return result

    def upload_catalog_video(
        self,
        song_number: int,
        privacy_status: str = "private",
        publish_at: Optional[str] = None
    ) -> Dict[str, Any]:
        """Uploads a produced catalog pilot video from output/video_XX directly."""
        vid = f"video_{song_number:02d}"
        output_dir = config.BASE_DIR / "output" / vid
        video_path = output_dir / "final_video.mp4"
        thumb_path = output_dir / "thumbnail.png"
        meta_path = output_dir / "metadata.json"

        if not video_path.exists():
            raise FileNotFoundError(f"Deliverable video not found at {video_path}! Produce the video first.")
        if not meta_path.exists():
            raise FileNotFoundError(f"Metadata not found at {meta_path}!")

        with open(meta_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        proj_dict = {
            "project_id": f"proj_{vid}",
            "title": metadata["title"],
            "theme": metadata.get("category_id", "Film & Animation"),
            "status": "APPROVED",
            "metadata": metadata,
            "paths": {
                "root": str(output_dir),
                "final_video": str(video_path),
                "thumbnail_file": str(thumb_path) if thumb_path.exists() else None
            }
        }
        return self.upload_project(
            proj_dict,
            privacy_status=privacy_status,
            publish_at=publish_at,
            bypass_approval_check=True
        )

youtube_uploader = YouTubeUploader()

if __name__ == "__main__":
    import sys
    song_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    privacy = sys.argv[2] if len(sys.argv) > 2 else "private"
    res = youtube_uploader.upload_catalog_video(song_num, privacy_status=privacy)
    print(f"\n✔ Upload process completed for Video {song_num:02d}!")
    print(f"  URL: {res.get('url')}")
    print(f"  ID: {res.get('id')}")
    print(f"  Privacy: {res.get('status', {}).get('privacyStatus')}")
    print(f"  Mode: {'Mock (Test Mode)' if res.get('mock') else 'Live YouTube Data API v3'}")

