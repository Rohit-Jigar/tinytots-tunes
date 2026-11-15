import os
import sys
import argparse
import uvicorn
from core.config import config
from core.logger import logger
from core.database import db
from characters.manager import character_manager
from planner.planner import content_planner
from assets.manager import asset_manager
from video.ffmpeg_engine import ffmpeg_engine
from video.templates import AnimationStyle
from thumbnail.generator import thumbnail_generator
from automation.queue_manager import queue_manager
from automation.worker import worker
from automation.scheduler import scheduler
from youtube.uploader import youtube_uploader

def cmd_dashboard(args):
    """Runs the FastAPI interactive web dashboard."""
    logger.info("Starting TinyTots Tunes Dashboard on http://%s:%d", config.HOST, config.PORT)
    uvicorn.run("dashboard.app:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)

def cmd_produce(args):
    """Produces an original children's video end-to-end."""
    topic = args.topic
    category = args.category
    character_id = args.character
    style = AnimationStyle(args.style)

    logger.info("==================================================")
    logger.info("TinyTots Tunes Video Factory - End-to-End Pipeline")
    logger.info("==================================================")

    # 1. Content Planning
    logger.info("[1/5] Planning song concept, lyrics, and storyboard...")
    project = content_planner.plan_project(topic=topic, category=category, character_id=character_id)
    p_id = project["project_id"]
    logger.info("Project Created: %s ('%s')", p_id, project["title"])

    # 2. Asset Generation
    logger.info("[2/5] Synthesizing scene images, voiceovers, BGM, and SFX...")
    project = asset_manager.generate_project_assets(project)

    # 3. 1080p Video Rendering
    logger.info("[3/5] Compositing 1080p MP4 video with FFmpeg...")
    video_path = ffmpeg_engine.assemble_full_video(project, style=style)
    logger.info("1080p Video Ready: %s", video_path)

    # 4. Thumbnail Generation
    logger.info("[4/5] Rendering 1280x720 YouTube Thumbnail...")
    thumb_path = project["paths"]["thumbnail_file"]
    hero_image = project["storyboard"][0]["image_file"]
    thumbnail_generator.generate_thumbnail(
        title=project["title"],
        base_image_path=hero_image,
        output_path=thumb_path,
        badge_text=project["metadata"].get("thumbnail_badge_text", "SING ALONG!"),
        character_name=project.get("character_name", "Barnaby Bear")
    )
    logger.info("Thumbnail Ready: %s", thumb_path)

    # 5. Production Gate & Approval Check
    if args.auto_approve:
        logger.info("[5/5] Auto-approve flag set. Authorizing publication...")
        queue_manager.approve_project(p_id)
        result = youtube_uploader.upload_project(project, bypass_approval_check=True)
        logger.info("Video successfully published to YouTube! Link: %s", result.get("url"))
    else:
        logger.info("[5/5] Project placed in APPROVAL QUEUE (status: PENDING_APPROVAL).")
        logger.info("Visit the dashboard at http://localhost:%d/projects/%s to review and approve.", config.PORT, p_id)

    logger.info("Production complete for project %s!", p_id)

def cmd_worker(args):
    """Runs the asynchronous queue worker."""
    logger.info("Starting background queue worker daemon (Press Ctrl+C to stop)...")
    worker.start()
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping worker daemon...")
        worker.stop()

def cmd_characters(args):
    """Lists registered original characters."""
    chars = character_manager.list_characters()
    print("\n--- TINYTOTS TUNES CHARACTER ROSTER ---")
    for c in chars:
        print(f"\nID: {c.id}")
        print(f"Name: {c.name} ({c.species})")
        print(f"Colors: {', '.join(c.color_palette)}")
        print(f"Clothing: {c.clothing}")
        print(f"Features: {c.distinctive_features}")
    print("\nTotal Characters:", len(chars))

def main():
    parser = argparse.ArgumentParser(description="TinyTots Tunes - AI Kids Video Factory CLI")
    subparsers = parser.add_subparsers(dest="command")

    # dashboard
    p_dash = subparsers.add_parser("dashboard", help="Start the web dashboard")

    # produce
    p_prod = subparsers.add_parser("produce", help="Produce a video from start to finish")
    p_prod.add_argument("--topic", type=str, default=None, help="Song title/topic")
    p_prod.add_argument("--category", type=str, default=None, help="Curriculum category")
    p_prod.add_argument("--character", type=str, default="barnaby_bear", help="Lead character ID")
    p_prod.add_argument("--style", type=str, default="nursery_classic", choices=["nursery_classic", "dance_party", "bedtime_lullaby", "learning_adventure"])
    p_prod.add_argument("--auto-approve", action="store_true", help="Bypass manual approval gate and publish immediately")

    # worker
    p_work = subparsers.add_parser("worker", help="Run background queue worker daemon")

    # characters
    p_char = subparsers.add_parser("characters", help="List registered original characters")

    args = parser.parse_args()

    if args.command == "dashboard" or args.command is None:
        cmd_dashboard(args)
    elif args.command == "produce":
        cmd_produce(args)
    elif args.command == "worker":
        cmd_worker(args)
    elif args.command == "characters":
        cmd_characters(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

