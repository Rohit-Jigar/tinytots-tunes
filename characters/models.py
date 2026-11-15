from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Character(BaseModel):
    id: str = Field(..., description="Unique alphanumeric identifier (e.g., barnaby_bear)")
    name: str = Field(..., description="Original character name")
    species: str = Field(..., description="Species or creature type (e.g., Teddy Bear)")
    color_palette: List[str] = Field(
        default_factory=list,
        description="Hex codes and descriptions (e.g. ['#8B5A2B (Warm Honey Brown)', '#00A896 (Teal)'])"
    )
    clothing: str = Field(..., description="Signature outfit details to ensure visual continuity")
    distinctive_features: str = Field(..., description="Key identifying physical traits (ears, eyes, shapes)")
    proportions: str = Field(
        default="chubby toddler proportions, 1:2 head-to-body ratio, rounded limbs, soft edges",
        description="Strict body proportion constraints"
    )
    personality: str = Field(..., description="Tone, temperament, and child-facing demeanor")
    voice_profile: Dict[str, Any] = Field(
        default_factory=lambda: {
            "gender": "Female/Child",
            "pitch_shift": "+20%",
            "speaking_rate": "+5%",
            "energy": "warm, enthusiastic, melodious"
        },
        description="Acoustic and singing voice parameters"
    )
    animation_habits: str = Field(
        default="gentle rhythmic bouncing to the beat, expressive wide blinks, playful arm waves",
        description="Signature kinetic character behaviors"
    )
    visual_prompt: str = Field(..., description="Base master visual prompt for text-to-image consistency")
    negative_prompt: str = Field(
        default="deformed, extra limbs, bad anatomy, realistic, photorealistic, scary, dark, muted colors, adult proportions, disfigured, text, watermark, bad hands",
        description="Enforced negative prompt to guarantee preschool 3D aesthetic"
    )
    reference_image_path: Optional[str] = Field(None, description="Local path to permanent reference turnaround sheet")

    def get_consistent_prompt_suffix(self) -> str:
        """Generates locked visual tokens for maintaining character consistency across all scenes."""
        return (
            f"character is {self.name}, an original preschool cartoon {self.species}, "
            f"exact signature wardrobe: {self.clothing}, "
            f"color palette: {', '.join(self.color_palette)}, "
            f"features: {self.distinctive_features}, proportions: {self.proportions}, "
            f"Pixar 3D cute cartoon aesthetic, soft cinematic lighting, bright cheerful colors, "
            f"child-friendly masterpiece, expressive animated facial expression"
        )
