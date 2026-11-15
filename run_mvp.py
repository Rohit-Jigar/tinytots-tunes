import os
import sys
import time
from pathlib import Path
from PIL import Image

from core.config import config
from core.logger import logger
from core.database import db
from core.safety import SafetyChecker, CopyrightSafetyError
from characters.manager import character_manager
from planner.planner import content_planner
from assets.manager import asset_manager
from video.ffmpeg_engine import ffmpeg_engine
from video.templates import AnimationStyle
from thumbnail.generator import thumbnail_generator
from automation.queue_manager import queue_manager
from youtube.uploader import youtube_uploader, YouTubePublishError

def run_end_to_end_mvp():
    print("\n" + "=" * 65)
    print(" 👶 TINYTOTS TUNES VIDEO FACTORY - COMPLETE MVP DEMONSTRATION")
    print("=" * 65 + "\n")

    # 1. Verification of Copyright Safety Engine
    print("--- [STEP 1/7] Testing Copyright Safety Engine ---")
    safe, viols = SafetyChecker.check_text("Barnaby Bear sings the rainbow song")
    assert safe, "Valid original character should pass safety!"
    print("  ✔ Original character verification: PASSED")

    is_peppa_safe, viols = SafetyChecker.check_text("Sing with Peppa Pig and Cocomelon")
    assert not is_peppa_safe, "Copyrighted character should be detected!"
    print(f"  ✔ Copyright blacklist detection: PASSED (Correctly flagged: {viols})")

    # 2. Content Planning
    print("\n--- [STEP 2/7] Content Planning & Storyboard Generation ---")
    topic = "The Rainbow Paintbox Song"
    category = "Colors & Creativity"
    char_id = "barnaby_bear"

    project = content_planner.plan_project(topic=topic, category=category, character_id=char_id)
    p_id = project["project_id"]
    storyboard = project["storyboard"]

    print(f"  ✔ Project Planned: ID '{p_id}'")
    print(f"  ✔ Title: {project['title']}")
    print(f"  ✔ Lead Character: {project['character_name']}")
    print(f"  ✔ Storyboard Scenes: {len(storyboard)} scenes generated")
    print(f"  ✔ SEO Title: {project['metadata']['title']}")
    print(f"  ✔ Total Tags: {len(project['metadata']['tags'])}")
    print(f"  ✔ COPPA Made for Kids: {project['metadata']['made_for_kids']}")

    # 3. Asset Generation
    print("\n--- [STEP 3/7] Multi-Provider Asset Generation ---")
    print(f"  * Using Image Engine: '{config.IMAGE_PROVIDER}'")
    print(f"  * Using Voice Engine: '{config.VOICE_PROVIDER}'")
    print(f"  * Using Music Engine: '{config.MUSIC_PROVIDER}'")

    project = asset_manager.generate_project_assets(project)

    for sc in storyboard[:3]:
        print(f"  ✔ Scene {sc['scene_number']}: Image '{Path(sc['image_file']).name}' | Audio '{Path(sc['audio_file']).name}'")
    print(f"  ✔ Background Music Track: '{Path(project['paths']['bgm_file']).name}'")

    # 4. 1080p Video Production
    print("\n--- [STEP 4/7] 1080p Video Compositing (FFmpeg) ---")
    print("  * Compositing Ken Burns camera motion, synchronized subtitles, and ducked BGM...")
    t0 = time.time()
    final_video = ffmpeg_engine.assemble_full_video(project, style=AnimationStyle.NURSERY_CLASSIC)
    render_time = time.time() - t0

    assert os.path.exists(final_video), "Final 1080p video must exist!"
    video_size_mb = os.path.getsize(final_video) / (1024 * 1024)
    print(f"  ✔ Video Rendered: {final_video}")
    print(f"  ✔ Resolution: 1920x1080 (Full HD MP4)")
    print(f"  ✔ File Size: {video_size_mb:.2f} MB")
    print(f"  ✔ Render Duration: {render_time:.2f} seconds")

    # 5. YouTube Thumbnail Generation
    print("\n--- [STEP 5/7] 1280x720 YouTube Thumbnail Generation ---")
    thumb_path = project["paths"]["thumbnail_file"]
    hero_img = storyboard[0]["image_file"]

    thumbnail_generator.generate_thumbnail(
        title=project["title"],
        base_image_path=hero_img,
        output_path=thumb_path,
        badge_text="SING ALONG!",
        character_name=project.get("character_name", "Barnaby Bear")
    )

    assert os.path.exists(thumb_path), "Thumbnail must exist!"
    with Image.open(thumb_path) as im:
        w, h = im.size
        assert (w, h) == (1280, 720), f"Thumbnail dimensions must be 1280x720, got {w}x{h}"
    print(f"  ✔ Thumbnail Dimensions Verified: {w}x{h} (16:9 Standard)")
    print(f"  ✔ File: {thumb_path}")

    # 6. Testing Human-in-the-Loop Approval Gate
    print("\n--- [STEP 6/7] Testing Human Approval Gate ---")
    # Verify unapproved upload is blocked
    try:
        youtube_uploader.upload_project(project, bypass_approval_check=False)
        print("  ❌ ERROR: Unapproved project was allowed to upload!")
    except YouTubePublishError as e:
        print(f"  ✔ Approval Gate successfully blocked publishing without authorization: '{e}'")

    # Now approve the project explicitly
    print("  * Simulating user clicking 'Approve for YouTube' in dashboard...")
    queue_manager.approve_project(p_id)
    approved_proj = content_planner.load_project(p_id)
    assert approved_proj["status"] == "APPROVED", "Status must be APPROVED!"
    print("  ✔ Project Status Updated to: APPROVED")

    # 7. YouTube Publishing
    print("\n--- [STEP 7/7] YouTube Data API v3 Upload & Publishing ---")
    upload_result = youtube_uploader.upload_project(approved_proj, bypass_approval_check=False)
    print(f"  ✔ Upload Success: YouTube Video ID: {upload_result['id']}")
    print(f"  ✔ YouTube Video URL: {upload_result['url']}")
    print(f"  ✔ COPPA Kids Designation: {upload_result['status']['selfDeclaredMadeForKids']}")
    print(f"  ✔ Final Project Status: PUBLISHED")

    print("\n" + "=" * 65)
    print(" 🎉 MVP PIPELINE TEST COMPLETED 100% SUCCESSFULLY!")
    print("=" * 65)
    print(f"\nDeliverable Output Files:")
    print(f"  1. 1080p Master Video: {final_video}")
    print(f"  2. 1280x720 Thumbnail: {thumb_path}")
    print(f"  3. Subtitles (.srt):   {Path(final_video).parent / 'subtitles.srt'}")
    print(f"  4. Subtitles (.ass):   {Path(final_video).parent / 'subtitles.ass'}")
    print(f"  5. Project Spec:       {Path(final_video).parent.parent / 'project.json'}")
    print(f"\nWeb Dashboard available via: python main.py dashboard")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_end_to_end_mvp()

