import os
import json
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from core.config import config
from core.database import db
from core.logger import logger
from characters.manager import character_manager
from planner.idea_generator import IdeaGenerator
from planner.lyric_writer import LyricWriter
from planner.storyboarder import Storyboarder
from planner.metadata_gen import MetadataGenerator
from planner.catalog_20 import catalog_manager

class ContentPlanner:
    """
    Orchestrates the entire planning phase:
    1. Generates or ingests preschool song ideas
    2. Writes rhyming educational lyrics & sound cues
    3. Builds the scene-by-scene storyboard
    4. Generates YouTube SEO metadata & thumbnail prompts
    5. Creates structured project directories and database records
    """

    @classmethod
    def plan_project(
        cls,
        topic: Optional[str] = None,
        category: Optional[str] = None,
        character_id: Optional[str] = None,
        project_id: Optional[str] = None,
        catalog_number: Optional[int] = None
    ) -> Dict[str, Any]:
        # Check catalog lookup
        cat_song = None
        if catalog_number:
            cat_song = catalog_manager.get_song_by_number(catalog_number)
        elif topic:
            cat_song = catalog_manager.get_song_by_title(topic)

        # 1. Resolve Character
        char = None
        target_char_id = character_id or (cat_song.get("lead_character_id") if cat_song else None)
        if target_char_id:
            char = character_manager.get_character(target_char_id)
        if not char:
            char = character_manager.get_character("barnaby_bear")
            if not char:
                all_chars = character_manager.list_characters()
                char = all_chars[0]

        # 2. Resolve Idea
        if cat_song:
            idea = {
                "title": cat_song["title"],
                "category": cat_song["category"],
                "target_age": cat_song["target_age"],
                "educational_goals": cat_song["educational_goals"],
                "tempo": cat_song["tempo"],
                "bpm": cat_song.get("bpm", 120),
                "hook": cat_song["hook"],
                "preferred_character": char.id,
                "visual_theme": cat_song.get("visual_theme", "")
            }
        elif topic:
            idea = {
                "title": topic,
                "category": category or "Preschool Sing-Along",
                "target_age": "2-5 years",
                "educational_goals": ["Fun", "Music appreciation", "Vocabulary"],
                "tempo": "Upbeat 120 BPM",
                "bpm": 120,
                "hook": f"Let's sing and dance together with {char.name}!",
                "preferred_character": char.id
            }
        else:
            idea = IdeaGenerator.generate_idea(category=category, preferred_character=char.id)

        # 3. Write Lyrics
        lyrics = LyricWriter.write_lyrics(idea, char)

        # 4. Generate Storyboard
        storyboard = Storyboarder.create_storyboard(lyrics, char)

        # 5. Generate SEO & Thumbnail Metadata
        metadata = MetadataGenerator.generate_metadata(idea, lyrics, storyboard, char)

        # 6. Setup Structured Project Directory
        p_id = project_id or f"proj_{uuid.uuid4().hex[:8]}"
        project_dir = config.PROJECTS_DIR / p_id
        assets_dir = project_dir / "assets"
        audio_dir = project_dir / "audio"
        video_dir = project_dir / "video"
        thumb_dir = project_dir / "thumbnail"

        for d in [project_dir, assets_dir, audio_dir, video_dir, thumb_dir]:
            d.mkdir(parents=True, exist_ok=True)

        project_data = {
            "project_id": p_id,
            "title": idea["title"],
            "theme": idea["category"],
            "character_id": char.id,
            "character_name": char.name,
            "status": "PLANNED",
            "idea": idea,
            "lyrics": lyrics,
            "storyboard": storyboard,
            "metadata": metadata,
            "paths": {
                "root": str(project_dir),
                "assets": str(assets_dir),
                "audio": str(audio_dir),
                "video": str(video_dir),
                "thumbnail": str(thumb_dir),
                "final_video": str(video_dir / "final_1080p.mp4"),
                "thumbnail_file": str(thumb_dir / "thumbnail_1280x720.jpg")
            }
        }

        # Save project.json and storyboard.json in folder
        with open(project_dir / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)

        with open(project_dir / "storyboard.json", "w", encoding="utf-8") as f:
            json.dump(storyboard, f, indent=2, ensure_ascii=False)

        # Persist to SQLite Database
        db.save_project(
            project_id=p_id,
            title=idea["title"],
            theme=idea["category"],
            status="PLANNED",
            data=project_data
        )

        logger.info("Successfully planned project '%s' (ID: %s) in %s", idea["title"], p_id, project_dir)
        return project_data

    @classmethod
    def load_project(cls, project_id: str) -> Optional[Dict[str, Any]]:
        record = db.get_project(project_id)
        if record and "data" in record:
            return record["data"]
        project_json_file = config.PROJECTS_DIR / project_id / "project.json"
        if project_json_file.exists():
            with open(project_json_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

content_planner = ContentPlanner()

