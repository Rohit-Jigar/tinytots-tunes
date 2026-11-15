import uuid
from typing import Dict, Any, List, Optional
from core.database import db
from core.logger import logger

class QueueManager:
    """
    Manages the lifecycle, state transitions, and retries of production jobs.
    """

    @classmethod
    def create_job(cls, project_id: str) -> Dict[str, Any]:
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        job = db.create_job(job_id=job_id, project_id=project_id, status="QUEUED", current_step="INITIALIZED")
        logger.info("Created production job '%s' for project '%s'", job_id, project_id)
        return job

    @classmethod
    def get_job(cls, job_id: str) -> Optional[Dict[str, Any]]:
        return db.get_job(job_id)

    @classmethod
    def list_jobs(cls, limit: int = 50) -> List[Dict[str, Any]]:
        return db.list_jobs(limit=limit)

    @classmethod
    def update_progress(cls, job_id: str, status: str, step: str, progress: int, error: Optional[str] = None):
        db.update_job_progress(job_id=job_id, status=status, step=step, progress=progress, error=error)

    @classmethod
    def retry_job(cls, job_id: str) -> bool:
        job = db.get_job(job_id)
        if not job:
            return False

        current_retries = job.get("retry_count", 0) + 1
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE queue_jobs
            SET status = 'QUEUED', current_step = 'RETRYING', progress = 0, error_message = NULL, retry_count = ?
            WHERE id = ?
            """, (current_retries, job_id))
            conn.commit()

        logger.info("Job '%s' queued for retry (Attempt #%d)", job_id, current_retries)
        return True

    @classmethod
    def approve_project(cls, project_id: str) -> bool:
        """User approves video for publication."""
        project = db.get_project(project_id)
        if not project:
            return False

        db.update_project_status(project_id, "APPROVED")
        # Update project data json as well
        data = project.get("data", {})
        data["status"] = "APPROVED"
        db.save_project(
            project_id=project_id,
            title=project["title"],
            theme=project.get("theme", ""),
            status="APPROVED",
            data=data
        )

        # Enqueue publishing job
        job_id = f"job_pub_{uuid.uuid4().hex[:6]}"
        db.create_job(job_id=job_id, project_id=project_id, status="QUEUED_PUBLISH", current_step="READY_FOR_UPLOAD")
        logger.info("Project '%s' approved! Publishing job '%s' created.", project_id, job_id)
        return True

    @classmethod
    def reject_project(cls, project_id: str, reason: str = "Needs Revision") -> bool:
        project = db.get_project(project_id)
        if not project:
            return False

        data = project.get("data", {})
        data["status"] = "REJECTED"
        data["rejection_reason"] = reason
        db.save_project(
            project_id=project_id,
            title=project["title"],
            theme=project.get("theme", ""),
            status="REJECTED",
            data=data
        )
        logger.info("Project '%s' rejected: %s", project_id, reason)
        return True

queue_manager = QueueManager()

