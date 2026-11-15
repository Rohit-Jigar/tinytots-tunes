import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.config import config
from core.logger import logger

DB_PATH = config.DATA_DIR / "tinytots.db"

class Database:
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Projects Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                theme TEXT,
                status TEXT NOT NULL,
                youtube_id TEXT,
                youtube_url TEXT,
                data_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Characters Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                species TEXT NOT NULL,
                color_palette_json TEXT,
                clothing TEXT,
                distinctive_features TEXT,
                personality TEXT,
                visual_prompt TEXT,
                reference_image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Production Queue Jobs Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS queue_jobs (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                status TEXT NOT NULL,
                current_step TEXT,
                progress INTEGER DEFAULT 0,
                error_message TEXT,
                retry_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
            """)
            conn.commit()
            logger.info("Database initialized successfully at %s", self.db_path)

    # --- Project Methods ---
    def save_project(self, project_id: str, title: str, theme: str, status: str, data: Dict[str, Any], youtube_id: Optional[str] = None, youtube_url: Optional[str] = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            data_str = json.dumps(data, ensure_ascii=False)
            now = datetime.utcnow().isoformat()
            cursor.execute("""
            INSERT INTO projects (id, title, theme, status, youtube_id, youtube_url, data_json, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                theme=excluded.theme,
                status=excluded.status,
                youtube_id=COALESCE(excluded.youtube_id, projects.youtube_id),
                youtube_url=COALESCE(excluded.youtube_url, projects.youtube_url),
                data_json=excluded.data_json,
                updated_at=excluded.updated_at
            """, (project_id, title, theme, status, youtube_id, youtube_url, data_str, now))
            conn.commit()

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            if not row:
                return None
            res = dict(row)
            res["data"] = json.loads(res["data_json"]) if res["data_json"] else {}
            return res

    def list_projects(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT * FROM projects WHERE status = ? ORDER BY created_at DESC", (status,))
            else:
                cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item["data"] = json.loads(item["data_json"]) if item["data_json"] else {}
                result.append(item)
            return result

    def update_project_status(self, project_id: str, status: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute("UPDATE projects SET status = ?, updated_at = ? WHERE id = ?", (status, now, project_id))
            conn.commit()

    # --- Character Methods ---
    def save_character(self, char_id: str, name: str, species: str, color_palette: List[str], clothing: str, features: str, personality: str, visual_prompt: str, ref_image: Optional[str] = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            palette_str = json.dumps(color_palette)
            cursor.execute("""
            INSERT INTO characters (id, name, species, color_palette_json, clothing, distinctive_features, personality, visual_prompt, reference_image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name=excluded.name,
                species=excluded.species,
                color_palette_json=excluded.color_palette_json,
                clothing=excluded.clothing,
                distinctive_features=excluded.distinctive_features,
                personality=excluded.personality,
                visual_prompt=excluded.visual_prompt,
                reference_image_path=excluded.reference_image_path
            """, (char_id, name, species, palette_str, clothing, features, personality, visual_prompt, ref_image))
            conn.commit()

    def get_character(self, char_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters WHERE id = ? OR name = ?", (char_id, char_id))
            row = cursor.fetchone()
            if not row:
                return None
            res = dict(row)
            res["color_palette"] = json.loads(res["color_palette_json"]) if res["color_palette_json"] else []
            return res

    def list_characters(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters ORDER BY name ASC")
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item["color_palette"] = json.loads(item["color_palette_json"]) if item["color_palette_json"] else []
                result.append(item)
            return result

    # --- Queue Job Methods ---
    def create_job(self, job_id: str, project_id: str, status: str = "QUEUED", current_step: str = "INITIALIZED") -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute("""
            INSERT INTO queue_jobs (id, project_id, status, current_step, progress, error_message, retry_count, created_at, updated_at)
            VALUES (?, ?, ?, ?, 0, NULL, 0, ?, ?)
            """, (job_id, project_id, status, current_step, now, now))
            conn.commit()
            return {"id": job_id, "project_id": project_id, "status": status, "current_step": current_step}

    def update_job_progress(self, job_id: str, status: str, step: str, progress: int, error: Optional[str] = None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute("""
            UPDATE queue_jobs
            SET status = ?, current_step = ?, progress = ?, error_message = ?, updated_at = ?
            WHERE id = ?
            """, (status, step, progress, error, now, job_id))
            conn.commit()

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM queue_jobs WHERE id = ?", (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM queue_jobs ORDER BY created_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in cursor.fetchall()]

db = Database()

