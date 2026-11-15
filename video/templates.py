from enum import Enum
from typing import Dict, Any

class AnimationStyle(str, Enum):
    NURSERY_CLASSIC = "nursery_classic"
    DANCE_PARTY = "dance_party"
    BEDTIME_LULLABY = "bedtime_lullaby"
    LEARNING_ADVENTURE = "learning_adventure"

class AnimationTemplate:
    """Defines timing, camera motion, transitions, color grading, and audio mixing per style."""

    @classmethod
    def get_template(cls, style: AnimationStyle) -> Dict[str, Any]:
        if style == AnimationStyle.DANCE_PARTY:
            return {
                "name": "Upbeat Dance Party",
                "zoom_speed": 0.0025,
                "max_zoom": 1.25,
                "character_bounce": True,
                "bounce_speed": 4.0,  # 4 bounces per second
                "bgm_duck_level": 0.25,
                "vocal_gain": 1.2,
                "transition_type": "fade",
                "transition_duration": 0.5,
                "vignette": False,
                "saturation": 1.25,   # Extra bright and colorful
                "contrast": 1.1
            }
        elif style == AnimationStyle.BEDTIME_LULLABY:
            return {
                "name": "Bedtime Lullaby",
                "zoom_speed": 0.0008,
                "max_zoom": 1.08,
                "character_bounce": False,
                "bounce_speed": 1.0,
                "bgm_duck_level": 0.18,
                "vocal_gain": 1.0,
                "transition_type": "fade",
                "transition_duration": 1.0,  # Gentle slow crossfade
                "vignette": True,
                "saturation": 0.95,
                "contrast": 1.0
            }
        elif style == AnimationStyle.LEARNING_ADVENTURE:
            return {
                "name": "Learning Adventure",
                "zoom_speed": 0.0015,
                "max_zoom": 1.15,
                "character_bounce": True,
                "bounce_speed": 2.5,
                "bgm_duck_level": 0.20,
                "vocal_gain": 1.3,
                "transition_type": "wipeleft",
                "transition_duration": 0.5,
                "vignette": False,
                "saturation": 1.15,
                "contrast": 1.05
            }
        else: # Default: NURSERY_CLASSIC
            return {
                "name": "Nursery Rhyme Classic",
                "zoom_speed": 0.0012,
                "max_zoom": 1.15,
                "character_bounce": True,
                "bounce_speed": 2.0,
                "bgm_duck_level": 0.22,
                "vocal_gain": 1.15,
                "transition_type": "fade",
                "transition_duration": 0.6,
                "vignette": False,
                "saturation": 1.1,
                "contrast": 1.05
            }

