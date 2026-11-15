import time
import traceback
import threading
from typing import Optional
from pathlib import Path
from core.config import config
from core.logger import logger
from core.database import db
from planner.planner import content_planner
from assets.manager import asset_manager
from video.ffmpeg_engine import ffmpeg_engine
from video.templates import AnimationStyle
from thumbnail.generator import thumbnail_generator
from youtube.uploader import youtube_uploader

class ProductionWorker:
    """
    Background worker that continuously processes the production queue:
    1. Asset Generation
    2. Video & Thumbnail Compositing
    3. Quality Gate (halts at PENDING_APPROVAL)
    4. YouTube Upload (upon human approval)
    """

    def __init__(self):
        self.running = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        """Starts worker in background daemon thread."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="ProductionWorkerThread")
        self._thread.start()
        logger.info("Production queue worker started.")

    def stop(self):
        """Stops worker loop."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=3)
        logger.info("Production queue worker stopped.")

    def _run_loop(self):
        while self.running:
            try:
                self.process_next_job()
            except Exception as e:
                logger.error("Unexpected error in worker loop: %s", e, exc_info=True)
            time.sleep(config.QUEUE_POLL_INTERVAL)

    def process_next_job(self) -> bool:
        """Picks up and executes the next pending job in the queue."""
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT * FROM queue_jobs
            WHERE status IN ('QUEUED', 'QUEUED_PUBLISH')
            ORDER BY created_at ASC
            LIMIT 1
            """)
            row = cursor.fetchone()

        if not row:
            return False

        job = dict(row)
        job_id = job["id"]
        project_id = job["project_id"]
        job_type = job["status"]

        logger.info("Worker picked up job '%s' (Type: %s, Project: %s)", job_id, job_type, project_id)

        try:
            if job_type == "QUEUED":
                self._execute_production_pipeline(job_id, project_id)
            elif job_type == "QUEUED_PUBLISH":
                self._execute_publishing_pipeline(job_id, project_id)
            return True
        except Exception as e:
            err_msg = str(e)
            logger.error("Job '%s' failed: %s\n%s", job_id, err_msg, traceback.format_exc())
            db.update_job_progress(job_id, status="FAILED", step="ERROR", progress=0, error=err_msg)

            # Auto retry check
            retries = job.get("retry_count", 0)
            if config.AUTO_RETRY_FAILED and retries < config.MAX_RETRIES:
                logger.info("Auto-retrying job '%s' (Attempt %d/%d)...", job_id, retries + 1, config.MAX_RETRIES)
                db.update_job_progress(job_id, status="QUEUED", step="RETRY_SCHEDULED", progress=0, error=err_msg)
            return False

    def _execute_production_pipeline(self, job_id: str, project_id: str):
        # 1. Load Project
        project_record = db.get_project(project_id)
        if not project_record:
            raise ValueError(f"Project '{project_id}' not found in database!")

        project_data = project_record["data"]
        db.update_job_progress(job_id, status="PROCESSING", step="STARTING_ASSETS", progress=5)

        # 2. Asset Generation Callback
        def on_asset_progress(pct: int, desc: str):
            db.update_job_progress(job_id, status="PROCESSING", step=desc, progress=pct)

        project_data = asset_manager.generate_project_assets(project_data, progress_callback=on_asset_progress)

        # 3. Video Rendering
        db.update_job_progress(job_id, status="PROCESSING", step="RENDERING_1080P_VIDEO", progress=65)

        def on_render_progress(pct: int, desc: str):
            db.update_job_progress(job_id, status="PROCESSING", step=desc, progress=pct)

        style = AnimationStyle.NURSERY_CLASSIC
        final_video = ffmpeg_engine.assemble_full_video(
            project_data=project_data,
            style=style,
            progress_callback=on_render_progress
        )

        # 4. Thumbnail Generation
        db.update_job_progress(job_id, status="PROCESSING", step="GENERATING_THUMBNAIL", progress=90)
        thumb_path = project_data["paths"]["thumbnail_file"]
        hero_scene_image = project_data["storyboard"][0]["image_file"]

        thumbnail_generator.generate_thumbnail(
            title=project_data["title"],
            base_image_path=hero_scene_image,
            output_path=thumb_path,
            badge_text=project_data["metadata"].get("thumbnail_badge_text", "SING ALONG!"),
            character_name=project_data.get("character_name", "Barnaby Bear")
        )

        # 5. Production Gate: Pause for Approval!
        project_data["status"] = "PENDING_APPROVAL"
        db.save_project(
            project_id=project_id,
            title=project_data["title"],
            theme=project_data["theme"],
            status="PENDING_APPROVAL",
            data=project_data
        )

        db.update_job_progress(job_id, status="WAITING_APPROVAL", step="PENDING_MANUAL_APPROVAL", progress=100)
        logger.info("Project '%s' rendered successfully! Placed in APPROVAL QUEUE.", project_id)

    def _execute_publishing_pipeline(self, job_id: str, project_id: str):
        project_record = db.get_project(project_id)
        if not project_record:
            raise ValueError(f"Project '{project_id}' not found in database!")

        project_data = project_record["data"]

        # If already published, mark job completed cleanly
        if project_data.get("status") == "PUBLISHED" and project_data.get("youtube_url"):
            db.update_job_progress(job_id, status="COMPLETED", step=f"ALREADY_PUBLISHED: {project_data.get('youtube_url')}", progress=100)
            logger.info("Project '%s' is already published. Marked job '%s' as COMPLETED.", project_id, job_id)
            return

        db.update_job_progress(job_id, status="UPLOADING", step="AUTHENTICATING_YOUTUBE", progress=10)

        # Upload to YouTube
        db.update_job_progress(job_id, status="UPLOADING", step="UPLOADING_MEDIA", progress=50)
        result = youtube_uploader.upload_project(
            project_data=project_data,
            privacy_status=config.YOUTUBE_DEFAULT_PRIVACY,
            bypass_approval_check=False  # Validates that project is APPROVED
        )

        db.update_job_progress(job_id, status="COMPLETED", step=f"PUBLISHED: {result.get('url', '')}", progress=100)
        logger.info("Job '%s' completed successfully. Published to YouTube: %s", job_id, result.get("url"))

worker = ProductionWorker()

