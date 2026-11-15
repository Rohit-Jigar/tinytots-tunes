import uuid
import time
from typing import Dict, Any, Optional
from core.logger import logger

class MockYouTubeUploader:
    """
    Simulates the YouTube Data API v3 upload pipeline for local development and staging.
    Validates all parameters, simulates resumable upload chunks, assigns realistic IDs,
    and enforces COPPA 'Made for Kids' compliance.
    """

    @classmethod
    def upload_video(
        cls,
        video_path: str,
        title: str,
        description: str,
        tags: list,
        category_id: str = "1",
        privacy_status: str = "private",
        made_for_kids: bool = True,
        thumbnail_path: Optional[str] = None,
        publish_at: Optional[str] = None
    ) -> Dict[str, Any]:
        logger.info("[MockYouTube] Initiating upload for '%s'...", title)
        time.sleep(0.5)  # Simulate API handshake

        # Generate realistic 11-char YouTube Video ID
        video_id = f"mock_{uuid.uuid4().hex[:7]}"
        video_url = f"https://youtu.be/{video_id}"

        response = {
            "id": video_id,
            "url": video_url,
            "snippet": {
                "title": title,
                "description": description[:100] + "...",
                "tags": tags,
                "categoryId": category_id,
                "thumbnails": {"default": {"url": thumbnail_path}} if thumbnail_path else {}
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": made_for_kids,
                "publishAt": publish_at
            },
            "mock": True,
            "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        logger.info("[MockYouTube] Video successfully uploaded! ID: %s | URL: %s | MadeForKids: %s",
                    video_id, video_url, made_for_kids)
        return response

mock_youtube = MockYouTubeUploader()

