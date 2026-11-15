import time
import threading
from typing import Optional
from core.logger import logger
from core.database import db
from planner.idea_generator import IdeaGenerator
from planner.planner import content_planner
from automation.queue_manager import queue_manager

class ProductionScheduler:
    """
    Automated job scheduler for continuous preschool channel programming:
    - Periodically plans and queues new educational videos
    - Rotates across curriculum categories (Colors, Habits, Numbers, Animals)
    - Enforces duplicate prevention
    """

    def __init__(self, interval_seconds: int = 3600):
        self.interval = interval_seconds
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._category_index = 0

    def start(self):
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._schedule_loop, daemon=True, name="SchedulerThread")
        self._thread.start()
        logger.info("Production scheduler started (Interval: %ds)", self.interval)

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=2)
        logger.info("Production scheduler stopped.")

    def _schedule_loop(self):
        while self.running:
            try:
                self.trigger_scheduled_batch()
            except Exception as e:
                logger.error("Error in scheduler batch: %s", e)
            time.sleep(self.interval)

    def trigger_scheduled_batch(self) -> Optional[str]:
        """Plans and queues an original song video automatically."""
        categories = IdeaGenerator.list_curriculum_categories()
        chosen_cat = categories[self._category_index % len(categories)]
        self._category_index += 1

        idea = IdeaGenerator.generate_idea(category=chosen_cat)
        title = idea["title"]

        # Duplicate Prevention Check
        existing_projects = db.list_projects()
        for p in existing_projects:
            if p["title"].strip().lower() == title.strip().lower() and p["status"] in ("PLANNED", "ASSETS_READY", "PENDING_APPROVAL", "APPROVED", "PUBLISHED"):
                logger.info("Scheduler skipped '%s' - already exists in production or published.", title)
                return None

        # Plan Project
        proj = content_planner.plan_project(topic=title, category=chosen_cat)
        # Enqueue for Worker
        queue_manager.create_job(proj["project_id"])
        logger.info("Scheduler successfully queued new project '%s' (ID: %s)", title, proj["project_id"])
        return proj["project_id"]

scheduler = ProductionScheduler()

