import os
import json
from pathlib import Path
from typing import Dict, Any, Callable, Optional
from core.config import config
from core.logger import logger
from core.database import db
from assets.image_generator import image_generator
from assets.voice_generator import voice_generator
from assets.music_generator import music_generator
from assets.sfx_manager import sfx_manager

class AssetManager:
    """
    Orchestrates end-to-end asset generation for a project:
    - Generates 1080p scene illustrations (backgrounds + character focus)
    - Generates synchronized vocal speech clips per scene
    - Synthesizes full-length background nursery music
    - Maps required sound effect cues
    """

    @classmethod
    def generate_project_assets(
        cls,
        project_data: Dict[str, Any],
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> Dict[str, Any]:
        p_id = project_data["project_id"]
        storyboard = project_data["storyboard"]
        paths = project_data["paths"]
        assets_dir = Path(paths["assets"])
        audio_dir = Path(paths["audio"])

        total_scenes = len(storyboard)
        logger.info("Beginning asset generation for project %s (%d scenes)...", p_id, total_scenes)

        # 1. Generate Scene Images and Vocals
        import shutil
        section_image_map = {}
        for idx, scene in enumerate(storyboard):
            sc_num = scene["scene_number"]
            sec_type = scene.get("section_type", f"sec_{sc_num}")
            step_pct = int(10 + (idx / total_scenes) * 60)
            if progress_callback:
                progress_callback(step_pct, f"Generating Scene {sc_num}/{total_scenes} Visuals & Vocals")

            # A. Scene Image (Section-level visual consistency)
            img_path = assets_dir / f"scene_{sc_num:02d}.png"
            if not img_path.exists():
                if sec_type in section_image_map and os.path.exists(section_image_map[sec_type]):
                    shutil.copyfile(section_image_map[sec_type], str(img_path))
                    logger.info("Reusing section 3D master plate '%s' for Scene %d (Visual Continuity)", sec_type, sc_num)
                else:
                    prompt = scene["visual_prompt"]
                    image_generator.generate(prompt, str(img_path), width=config.VIDEO_WIDTH, height=config.VIDEO_HEIGHT)
                    section_image_map[sec_type] = str(img_path)
            else:
                section_image_map[sec_type] = str(img_path)
            scene["image_file"] = str(img_path)

            # B. Scene Vocals
            vox_path = audio_dir / f"audio_{sc_num:02d}.mp3"
            if not vox_path.exists():
                speech_text = scene["display_text"]
                voice_generator.synthesize(speech_text, str(vox_path))
            scene["audio_file"] = str(vox_path)

            # C. SFX Mapping
            if scene.get("sfx"):
                sfx_file = sfx_manager.get_sfx_path(scene["sfx"])
                scene["sfx_file"] = sfx_file

        # 2. Synthesize Full Background Music Track
        total_duration = storyboard[-1]["end_time"] if storyboard else 30.0
        # Add 2.0s padding for smooth outro
        bgm_duration = total_duration + 2.0
        bgm_path = audio_dir / "bgm.wav"

        if progress_callback:
            progress_callback(75, "Synthesizing Catchy Background Nursery Music Track")

        tempo = project_data.get("idea", {}).get("tempo", "116 BPM")
        music_generator.generate(
            prompt=f"Cheerful preschool nursery melody for {project_data['title']}",
            duration_seconds=bgm_duration,
            output_path=str(bgm_path),
            tempo=tempo
        )
        project_data["paths"]["bgm_file"] = str(bgm_path)

        # Update Project Record
        project_data["status"] = "ASSETS_READY"
        with open(Path(paths["root"]) / "project.json", "w", encoding="utf-8") as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)

        with open(Path(paths["root"]) / "storyboard.json", "w", encoding="utf-8") as f:
            json.dump(storyboard, f, indent=2, ensure_ascii=False)

        db.save_project(
            project_id=p_id,
            title=project_data["title"],
            theme=project_data["theme"],
            status="ASSETS_READY",
            data=project_data
        )

        if progress_callback:
            progress_callback(80, "Asset Generation Complete")

        logger.info("All assets generated successfully for project %s", p_id)
        return project_data

asset_manager = AssetManager()

