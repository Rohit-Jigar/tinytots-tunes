import os
import json
import shutil
import time
from pathlib import Path
from typing import Dict, Any, Optional

from core.config import config
from core.logger import logger
from core.database import db
from characters.manager import character_manager
from planner.planner import content_planner
from planner.catalog_20 import catalog_manager
from assets.manager import asset_manager
from video.ffmpeg_engine import ffmpeg_engine
from video.templates import AnimationStyle
from video.subtitle_engine import subtitle_engine
from thumbnail.generator import thumbnail_generator
from core.quality_control import quality_inspector

class PilotProducer:
    """
    Dedicated Producer for TinyTots Tunes Pilot Videos:
    Produces complete, verified broadcast-ready preschool animation packages:
    1. Plans project from official 20-song catalog
    2. Synthesizes studio audio (quantized polyphony) & character sprites
    3. Renders 2.5D multi-layer kinetic animated frames with beat bounce & parallax
    4. Generates high-CTR 1280x720 thumbnail & karaoke subtitles
    5. Executes 10-point automated broadcast Quality Control inspection
    6. Bundles deliverables into output/video_XX/
    """

    def __init__(self, output_root: Optional[str] = None):
        self.output_root = Path(output_root or "output")
        self.output_root.mkdir(parents=True, exist_ok=True)

    def produce_catalog_video(self, song_number: int) -> Dict[str, Any]:
        """
        Produces and packages a complete video for a specific catalog number (1-20).
        """
        song = catalog_manager.get_song_by_number(song_number)
        if not song:
            raise ValueError(f"Song number {song_number} not found in catalog!")

        video_id = f"video_{song_number:02d}"
        dest_dir = self.output_root / video_id
        dest_dir.mkdir(parents=True, exist_ok=True)

        logger.info("==================================================")
        logger.info("PRODUCING PILOT %s: '%s'", video_id.upper(), song["title"])
        logger.info("==================================================")

        t_start = time.time()

        # Step 1: Content Planning
        project_data = content_planner.plan_project(
            catalog_number=song_number,
            project_id=f"proj_{video_id}"
        )

        p_id = project_data["project_id"]
        char_id = project_data["character_id"]
        char = character_manager.get_character(char_id)

        # Step 2: Asset Generation (Character Mascots, SAPI Voice, Studio Polyphonic Music)
        logger.info("[%s] Generating Multi-Track Audio & Character Visual Assets...", video_id)
        project_data = asset_manager.generate_project_assets(project_data)

        # Step 3: Render 1080p Video via Layered 2.5D Kinetic Puppet Compositor
        logger.info("[%s] Rendering 1080p Master Video with Kinetic Puppet Engine...", video_id)
        final_video_path = ffmpeg_engine.assemble_full_video(
            project_data=project_data,
            style=AnimationStyle.NURSERY_CLASSIC
        )

        # Step 4: Generate 1280x720 High-CTR YouTube Thumbnail
        logger.info("[%s] Generating 1280x720 YouTube Thumbnail...", video_id)
        thumb_dest = str(dest_dir / "thumbnail.png")
        hero_scene = project_data["storyboard"][0]["image_file"]
        thumbnail_generator.generate_thumbnail(
            title=project_data["title"],
            base_image_path=hero_scene,
            output_path=thumb_dest,
            badge_text=project_data["metadata"].get("thumbnail_badge_text", "SING ALONG!"),
            character_name=project_data.get("character_name", char.name if char else "Barnaby Bear")
        )

        # Step 5: Export Subtitles (.srt)
        logger.info("[%s] Exporting Synchronized Subtitles (.srt)...", video_id)
        srt_dest = str(dest_dir / "subtitles.srt")
        subtitle_engine.generate_srt(project_data["storyboard"], srt_dest)

        # Step 6: Export Lyrics (.txt)
        lyrics_dest = dest_dir / "lyrics.txt"
        full_lyrics = project_data.get("lyrics", {}).get("full_lyrics_text", "")
        with open(lyrics_dest, "w", encoding="utf-8") as f:
            f.write(f"=== {project_data['title']} ===\n")
            f.write(f"Lead Character: {project_data.get('character_name', '')}\n")
            f.write(f"Tempo: {song.get('tempo', '120 BPM')}\n")
            f.write(f"Category: {song.get('category', '')}\n\n")
            f.write(full_lyrics + "\n")

        # Step 7: Export Storyboard (.json)
        sb_dest = dest_dir / "storyboard.json"
        with open(sb_dest, "w", encoding="utf-8") as f:
            json.dump(project_data["storyboard"], f, indent=2, ensure_ascii=False)

        # Step 8: Export Metadata (.json)
        meta_dest = dest_dir / "metadata.json"
        with open(meta_dest, "w", encoding="utf-8") as f:
            json.dump(project_data["metadata"], f, indent=2, ensure_ascii=False)

        # Step 9: Copy Final 1080p Master Video
        final_dest = dest_dir / "final_video.mp4"
        shutil.copyfile(final_video_path, str(final_dest))

        # Step 10: Run 10-Point Broadcast Quality Control Inspection
        logger.info("[%s] Running 10-Point Quality Control Inspection Suite...", video_id)
        qc_report = quality_inspector.inspect_package(
            video_path=str(final_dest),
            thumbnail_path=str(thumb_dest),
            subtitles_path=str(srt_dest),
            lyrics_text=full_lyrics,
            project_data=project_data
        )

        # Save production_report.json
        report_dest = dest_dir / "production_report.json"
        with open(report_dest, "w", encoding="utf-8") as f:
            json.dump(qc_report, f, indent=2, ensure_ascii=False)

        elapsed = time.time() - t_start
        logger.info("==================================================")
        logger.info("✔ %s COMPLETED in %.1f seconds | QC Score: %.1f/100 | Status: %s",
                    video_id.upper(), elapsed, qc_report["overall_score"], qc_report["status"])
        logger.info("Deliverables saved in: %s", dest_dir.resolve())
        logger.info("==================================================")

        return {
            "video_id": video_id,
            "title": project_data["title"],
            "character": project_data.get("character_name"),
            "dest_dir": str(dest_dir.resolve()),
            "qc_score": qc_report["overall_score"],
            "qc_status": qc_report["status"],
            "duration_sec": qc_report["inspections"]["3_duration_compliance"].get("duration_sec", 0.0),
            "deliverables": {
                "final_video": str(final_dest.resolve()),
                "thumbnail": str(Path(thumb_dest).resolve()),
                "lyrics": str(lyrics_dest.resolve()),
                "storyboard": str(sb_dest.resolve()),
                "metadata": str(meta_dest.resolve()),
                "subtitles": str(Path(srt_dest).resolve()),
                "production_report": str(report_dest.resolve())
            }
        }

pilot_producer = PilotProducer()

if __name__ == "__main__":
    import sys
    song_nums = [1, 2]
    if len(sys.argv) > 1:
        song_nums = [int(x) for x in sys.argv[1:]]
    for num in song_nums:
        pilot_producer.produce_catalog_video(num)
