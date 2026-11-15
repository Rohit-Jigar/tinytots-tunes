from typing import Dict, Any, List
from characters.models import Character
from core.safety import SafetyChecker

class MetadataGenerator:
    """
    Generates YouTube-optimized, COPPA-compliant preschool metadata,
    SEO tags, timestamped descriptions, and thumbnail prompts.
    """

    @classmethod
    def generate_metadata(
        cls,
        song_idea: Dict[str, Any],
        lyrics_data: Dict[str, Any],
        storyboard: List[Dict[str, Any]],
        character: Character
    ) -> Dict[str, Any]:
        title_base = song_idea.get("title", "Happy Sing-Along")
        char_name = character.name
        category = song_idea.get("category", "Nursery Rhymes")

        # Check safety
        SafetyChecker.enforce_safety(title_base, context="Metadata title")
        SafetyChecker.enforce_safety(char_name, context="Metadata character")

        # 1. SEO Title (under 80 characters, highly clickable with preschool emojis)
        title_candidates = [
            f"{title_base} 🎨 Preschool Learning Song with {char_name}",
            f"{title_base} | Nursery Rhymes & Kids Songs by {char_name}",
            f"Sing Along: {title_base} ✨ Fun Baby Songs with {char_name}"
        ]
        title = title_candidates[0]

        # 2. Timestamps from storyboard
        timestamps_str = ""
        for sc in storyboard:
            mins = int(sc["start_time"] // 60)
            secs = int(sc["start_time"] % 60)
            timestamps_str += f"{mins:02d}:{secs:02d} - Scene {sc['scene_number']}: {sc['section_type']}\n"

        # 3. Full Lyrics for description
        lyrics_text = lyrics_data.get("full_lyrics_text", "")

        # 4. Rich SEO Description
        description = (
            f"🌟 Welcome to TinyTots Tunes! Sing and dance along with {char_name} in \"{title_base}\"!\n\n"
            f"This original educational preschool song helps toddlers and kids with {', '.join(song_idea.get('educational_goals', ['learning', 'fun']))}. "
            f"Packed with joyful animation, positive reinforcement, and colorful characters designed especially for ages {song_idea.get('target_age', '1-5 years')}.\n\n"
            f"⏱️ VIDEO CHAPTERS:\n"
            f"{timestamps_str}\n"
            f"🎵 LYRICS / SING ALONG WITH {char_name.upper()}:\n"
            f"-----------------------------------------\n"
            f"{lyrics_text}\n"
            f"-----------------------------------------\n\n"
            f"✨ ABOUT TINYTOTS TUNES:\n"
            f"TinyTots Tunes creates 100% original, safe, gentle, and educational musical adventures for toddlers, babies, and preschoolers.\n\n"
            f"#PreschoolSongs #KidsMusic #NurseryRhymes #ToddlerLearning #{char_name.replace(' ', '')} #TinyTotsTunes"
        )

        # 5. Targeted Tags
        tags = [
            "preschool songs",
            "kids songs",
            "nursery rhymes",
            "toddler music",
            "educational songs for kids",
            "sing along for toddlers",
            "kindergarten songs",
            "baby songs",
            "children animation",
            title_base.lower(),
            char_name.lower(),
            category.lower(),
            "tinytots tunes",
            "safe kids videos",
            "cartoon songs"
        ]

        # 6. Thumbnail Prompt
        thumbnail_prompt = (
            f"YouTube thumbnail for preschool cartoon video, starring {character.get_consistent_prompt_suffix()}. "
            f"Large expressive joyful face smiling directly at camera, waving playfully. "
            f"Bright sunny pastel gradient background with sparkles and confetti stars. "
            f"High contrast, vibrant 3D Pixar style, clean composition with clear open space for bold title typography, 8k"
        )

        return {
            "title": title,
            "description": description,
            "tags": tags,
            "category_id": "1",  # 1 = Film & Animation
            "made_for_kids": True,
            "thumbnail_prompt": SafetyChecker.sanitize_prompt(thumbnail_prompt),
            "thumbnail_badge_text": "SING ALONG!" if "song" in title_base.lower() else "LEARN & PLAY!"
        }

