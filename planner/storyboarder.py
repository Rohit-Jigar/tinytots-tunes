import re
from typing import Dict, Any, List
from characters.models import Character
from characters.manager import character_manager
from core.safety import SafetyChecker

class Storyboarder:
    """
    Transforms nursery song lyrics into a scene-by-scene visual and audio storyboard.
    Enforces visual continuity, toddler-friendly pacing, and camera motion specifications.
    """

    @classmethod
    def create_storyboard(cls, lyrics_data: Dict[str, Any], character: Character) -> List[Dict[str, Any]]:
        scenes = []
        scene_index = 1
        current_time = 0.0

        sections = lyrics_data.get("sections", [])
        char_prompt_suffix = character.get_consistent_prompt_suffix()

        for sec in sections:
            sec_type = sec["type"]
            lines = sec["lines"]
            action_cues = sec.get("action_cues", [])

            # We can create 1 or 2 scenes per section depending on line count
            # Group lines into digestible 2-line chunks (approx 4.0-5.0 seconds per scene)
            chunk_size = 2 if len(lines) > 2 else len(lines)
            for i in range(0, len(lines), chunk_size):
                chunk = lines[i:i + chunk_size]
                chunk_text = " ".join(chunk)
                raw_duration = max(3.5, len(chunk_text.split()) * 0.45) # ~0.45s per word for toddler singing pace
                # Quantize duration to 4/4 musical bars (at 120 BPM, 1 bar = 2.0s) for rhythm alignment
                bar_sec = 2.0
                num_bars = max(2, int(round(raw_duration / bar_sec)))
                duration = round(num_bars * bar_sec, 2)

                # Select action cue
                action = action_cues[i % len(action_cues)] if action_cues else "smiling and moving to the beat"

                # Motion cue rotation for visual variety
                motions = ["zoom_in", "pan_right", "gentle_bounce", "zoom_out", "pan_left"]
                motion = motions[(scene_index - 1) % len(motions)]

                # Sound effect cue check
                sfx = None
                if "[Pop!]" in chunk_text:
                    sfx = "pop"
                elif "[Chime]" in chunk_text:
                    sfx = "chime"
                elif "[Giggle]" in chunk_text:
                    sfx = "giggle"
                elif "[Splash!]" in chunk_text:
                    sfx = "splash"
                elif "[Clap!]" in chunk_text:
                    sfx = "clap"

                # Clean lyrics text for subtitles / TTS (strip all bracketed cues like [Roar!], [Chime], etc.)
                clean_lines = [re.sub(r'\[.*?\]', '', l).strip() for l in chunk]

                # Craft visual prompt
                setting_description = f"a colorful whimsical preschool landscape with soft rolling green hills, fluffy heart-shaped clouds, and cheerful flowers in the style of {sec_type}"
                visual_prompt = (
                    f"Preschool 3D animated cartoon scene, {setting_description}. "
                    f"Focus on {char_prompt_suffix}. "
                    f"Character is {action}. "
                    f"Very bright lighting, happy joyful aesthetic, clean high definition rendering, 8k"
                )

                scene = {
                    "scene_number": scene_index,
                    "section_type": sec_type,
                    "start_time": round(current_time, 2),
                    "end_time": round(current_time + duration, 2),
                    "duration": round(duration, 2),
                    "lyrics_lines": clean_lines,
                    "display_text": " ".join(clean_lines),
                    "action": action,
                    "camera_motion": motion,
                    "sfx": sfx,
                    "visual_prompt": SafetyChecker.sanitize_prompt(visual_prompt),
                    "image_filename": f"scene_{scene_index:02d}.png",
                    "audio_filename": f"audio_{scene_index:02d}.mp3"
                }

                scenes.append(scene)
                current_time += duration
                scene_index += 1

        return scenes

