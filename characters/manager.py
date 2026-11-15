import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont
from core.config import config
from core.database import db
from core.safety import SafetyChecker
from core.logger import logger
from characters.models import Character
from characters.presets import DEFAULT_PRESET_CHARACTERS

class CharacterManager:
    """
    Manages the permanent 5-character TinyTots Tunes universe:
    - Barnaby Bear, Pip the Bird, Penny Bunny, Zara Zebra, Sunny
    - Enforces visual and wardrobe continuity across all scenes
    - Generates & caches permanent character reference turnaround sheets
    - Safeguards against trademark/copyright infringement
    """

    def __init__(self):
        self.char_dir = config.DATA_DIR / "characters"
        self.char_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_presets_loaded()
        self._ensure_reference_images()

    def _ensure_presets_loaded(self):
        """Loads and updates official 5 original characters into database."""
        for preset in DEFAULT_PRESET_CHARACTERS:
            # Upsert into database
            self.save_character(preset)
        logger.info("Synchronized 5 official TinyTots Tunes characters in database.")

    def _ensure_reference_images(self):
        """Generates permanent reference turnaround images for every character."""
        for char in DEFAULT_PRESET_CHARACTERS:
            ref_path = self.char_dir / f"{char.id}_ref.png"
            if not ref_path.exists():
                self._generate_character_portrait(char, str(ref_path))
                char.reference_image_path = str(ref_path)
                self.save_character(char)

    def _generate_character_portrait(self, char: Character, output_path: str):
        """Generates an official character reference card with color swatches and character artwork."""
        width, height = 1080, 1080
        img = Image.new("RGB", (width, height), color="#F0F4F8")
        draw = ImageDraw.Draw(img)

        # Background card frame
        draw.rounded_rectangle([30, 30, width - 30, height - 30], radius=40, fill="#FFFFFF", outline="#CBD5E1", width=4)

        # Character Header Banner
        draw.rounded_rectangle([60, 60, width - 60, 170], radius=24, fill="#0F172A")
        # Header text
        draw.text((90, 85), char.name.upper(), fill="#FFD166", font=None)
        draw.text((90, 125), f"Official Preschool Canon • {char.species}", fill="#94A3B8", font=None)

        # Color Swatches Section
        swatch_y = 200
        draw.text((70, swatch_y), "CANON COLOR PALETTE:", fill="#334155")
        for idx, col_str in enumerate(char.color_palette):
            hex_code = col_str.split(" ")[0].strip()
            sx = 70 + (idx * 230)
            sy = swatch_y + 25
            if sx + 200 < width - 60:
                draw.rounded_rectangle([sx, sy, sx + 200, sy + 50], radius=12, fill=hex_code, outline="#64748B", width=2)
                draw.text((sx + 10, sy + 15), col_str.split(" ")[0], fill="#000000" if "White" in col_str or "Cream" in col_str or "Yellow" in col_str else "#FFFFFF")

        # Center Character Illustration Area
        char_box = [140, 310, width - 140, 830]
        draw.rounded_rectangle(char_box, radius=30, fill="#E2E8F0", outline="#94A3B8", width=3)

        # Draw cute symbolic mascot for each character
        cx, cy = width // 2, 570
        if char.id == "barnaby_bear":
            # Brown teddy bear with teal dungarees
            draw.ellipse([cx - 150, cy - 130, cx + 150, cy + 180], fill="#8B5A2B", outline="#5C3A1E", width=8) # Body
            draw.chord([cx - 150, cy - 20, cx + 150, cy + 180], start=0, end=180, fill="#00A896", outline="#007F70", width=6) # Teal overalls
            draw.ellipse([cx - 25, cy + 30, cx + 25, cy + 80], fill="#E63946") # Red Button
            draw.ellipse([cx - 120, cy - 230, cx + 120, cy - 30], fill="#8B5A2B", outline="#5C3A1E", width=8) # Head
            draw.ellipse([cx - 140, cy - 260, cx - 70, cy - 190], fill="#8B5A2B", outline="#5C3A1E", width=6) # Ears
            draw.ellipse([cx + 70, cy - 260, cx + 140, cy - 190], fill="#8B5A2B", outline="#5C3A1E", width=6)
            draw.ellipse([cx - 50, cy - 130, cx + 50, cy - 60], fill="#FFF1D0") # Muzzle
            draw.ellipse([cx - 20, cy - 125, cx + 20, cy - 95], fill="#1E293B") # Button nose
            draw.arc([cx - 30, cy - 105, cx + 30, cy - 75], start=10, end=170, fill="#1E293B", width=6) # Smile
            draw.ellipse([cx - 55, cy - 180, cx - 25, cy - 140], fill="#1E293B") # Eyes
            draw.ellipse([cx + 25, cy - 180, cx + 55, cy - 140], fill="#1E293B")
            draw.ellipse([cx - 45, cy - 175, cx - 35, cy - 155], fill="#FFFFFF")
            draw.ellipse([cx + 35, cy - 175, cx + 45, cy - 155], fill="#FFFFFF")

        elif char.id == "pip_bird":
            # Yellow songbird in sky-blue aviator cap
            draw.ellipse([cx - 130, cy - 100, cx + 130, cy + 150], fill="#FFD166", outline="#F59E0B", width=8) # Body
            draw.chord([cx - 120, cy - 140, cx + 120, cy - 20], start=180, end=360, fill="#118AB2", outline="#0C6E8E", width=6) # Aviator cap
            draw.polygon([(cx, cy - 20), (cx - 35, cy + 25), (cx + 35, cy + 25)], fill="#FF9F1C") # Beak
            draw.ellipse([cx - 60, cy - 70, cx - 25, cy - 30], fill="#1E293B") # Eyes
            draw.ellipse([cx + 25, cy - 70, cx + 60, cy - 30], fill="#1E293B")
            draw.ellipse([cx - 50, cy - 65, cx - 38, cy - 45], fill="#FFFFFF")
            draw.ellipse([cx + 35, cy - 65, cx + 47, cy - 45], fill="#FFFFFF")
            draw.arc([cx - 140, cy, cx - 70, cy + 80], start=90, end=270, fill="#F59E0B", width=8) # Wing

        elif char.id == "penny_bunny":
            # Cute pink bunny in lavender pinafore
            # Long bunny ears
            draw.ellipse([cx - 100, cy - 290, cx - 40, cy - 100], fill="#FFB3C6", outline="#F43F5E", width=6)
            draw.ellipse([cx + 40, cy - 290, cx + 100, cy - 100], fill="#FFB3C6", outline="#F43F5E", width=6)
            draw.ellipse([cx - 85, cy - 270, cx - 55, cy - 120], fill="#FFF1F2") # Inner ear
            draw.ellipse([cx + 55, cy - 270, cx + 85, cy - 120], fill="#FFF1F2")
            draw.ellipse([cx - 120, cy - 90, cx + 120, cy + 170], fill="#FFB3C6", outline="#F43F5E", width=8) # Body
            draw.chord([cx - 110, cy + 10, cx + 110, cy + 170], start=0, end=180, fill="#C77DFF", outline="#A855F7", width=6) # Lavender dress
            draw.ellipse([cx - 100, cy - 150, cx + 100, cy], fill="#FFB3C6", outline="#F43F5E", width=8) # Head
            draw.ellipse([cx - 20, cy - 70, cx + 20, cy - 45], fill="#FB7185") # Pink Nose
            draw.arc([cx - 25, cy - 55, cx + 25, cy - 30], start=10, end=170, fill="#1E293B", width=5)
            draw.ellipse([cx - 50, cy - 105, cx - 20, cy - 65], fill="#1E293B") # Eyes
            draw.ellipse([cx + 20, cy - 105, cx + 50, cy - 65], fill="#1E293B")
            draw.ellipse([cx - 40, cy - 100, cx - 30, cy - 80], fill="#FFFFFF")
            draw.ellipse([cx + 30, cy - 100, cx + 40, cy - 80], fill="#FFFFFF")

        elif char.id == "zara_zebra":
            # Playful zebra with purple stripes & mint overalls
            draw.ellipse([cx - 120, cy - 80, cx + 120, cy + 170], fill="#FFFFFF", outline="#7B2CBF", width=8) # Body
            draw.chord([cx - 115, cy + 20, cx + 115, cy + 170], start=0, end=180, fill="#06D6A0", outline="#059669", width=6) # Overalls
            draw.ellipse([cx - 100, cy - 180, cx + 100, cy - 20], fill="#FFFFFF", outline="#7B2CBF", width=8) # Head
            # Purple stripes
            for sy in range(cy - 140, cy - 40, 25):
                draw.line([(cx - 95, sy), (cx - 50, sy)], fill="#7B2CBF", width=8)
                draw.line([(cx + 50, sy), (cx + 95, sy)], fill="#7B2CBF", width=8)
            draw.ellipse([cx - 50, cy - 120, cx - 20, cy - 75], fill="#1E293B")
            draw.ellipse([cx + 20, cy - 120, cx + 50, cy - 75], fill="#1E293B")
            draw.arc([cx - 30, cy - 65, cx + 30, cy - 40], start=10, end=170, fill="#7B2CBF", width=5)

        else: # sunny_sunshine
            # Radiant smiling sun
            # Rays
            import math
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                x1 = cx + int(150 * math.cos(rad))
                y1 = cy + int(150 * math.sin(rad))
                x2 = cx + int(210 * math.cos(rad))
                y2 = cy + int(210 * math.sin(rad))
                draw.line([(x1, y1), (x2, y2)], fill="#FF8800", width=14)
            draw.ellipse([cx - 140, cy - 140, cx + 140, cy + 140], fill="#FFD000", outline="#FF8800", width=10) # Disk
            draw.ellipse([cx - 110, cy - 10, cx - 50, cy + 40], fill="#FF595E") # Rosy cheeks
            draw.ellipse([cx + 50, cy - 10, cx + 110, cy + 40], fill="#FF595E")
            draw.ellipse([cx - 60, cy - 60, cx - 20, cy - 10], fill="#1E293B") # Eyes
            draw.ellipse([cx + 20, cy - 60, cx + 60, cy - 10], fill="#1E293B")
            draw.ellipse([cx - 50, cy - 55, cx - 35, cy - 35], fill="#FFFFFF")
            draw.ellipse([cx + 35, cy - 55, cx + 50, cy - 35], fill="#FFFFFF")
            draw.arc([cx - 60, cy - 20, cx + 60, cy + 70], start=10, end=170, fill="#C2410C", width=8) # Smile

        # Footer Specifications
        footer_y = 860
        draw.text((70, footer_y), f"SIGNATURE WARDROBE: {char.clothing}", fill="#334155")
        draw.text((70, footer_y + 35), f"PROPORTIONS: {char.proportions}", fill="#64748B")
        draw.text((70, footer_y + 70), f"VOICE PROFILE: {char.voice_profile.get('style', 'Melodious preschool sing-along')}", fill="#64748B")
        draw.text((70, footer_y + 105), f"ANIMATION HABITS: {char.animation_habits}", fill="#64748B")

        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        img.save(output_path, "PNG")
        logger.info("Generated permanent character canon reference: %s", output_path)

    def save_character(self, character: Character) -> Character:
        """Validates copyright safety and persists character to database."""
        SafetyChecker.enforce_safety(character.name, context="character name")
        SafetyChecker.enforce_safety(character.clothing, context="character clothing")
        SafetyChecker.enforce_safety(character.visual_prompt, context="character prompt")

        db.save_character(
            char_id=character.id,
            name=character.name,
            species=character.species,
            color_palette=character.color_palette,
            clothing=character.clothing,
            features=character.distinctive_features,
            personality=character.personality,
            visual_prompt=character.visual_prompt,
            ref_image=character.reference_image_path
        )
        return character

    def get_character(self, char_id_or_name: str) -> Optional[Character]:
        """Retrieves character by ID or Name."""
        row = db.get_character(char_id_or_name)
        if not row:
            return None
        return Character(
            id=row["id"],
            name=row["name"],
            species=row["species"],
            color_palette=row["color_palette"],
            clothing=row["clothing"],
            distinctive_features=row["distinctive_features"],
            personality=row["personality"],
            visual_prompt=row["visual_prompt"],
            reference_image_path=row.get("reference_image_path")
        )

    def list_characters(self) -> List[Character]:
        """Lists all registered characters."""
        rows = db.list_characters()
        return [
            Character(
                id=r["id"],
                name=r["name"],
                species=r["species"],
                color_palette=r["color_palette"],
                clothing=r["clothing"],
                distinctive_features=r["distinctive_features"],
                personality=r["personality"],
                visual_prompt=r["visual_prompt"],
                reference_image_path=r.get("reference_image_path")
            )
            for r in rows
        ]

    def build_scene_prompt(self, character_id: str, scene_action: str, setting: str) -> str:
        """Builds a locked, high-fidelity prompt ensuring strict visual continuity."""
        char = self.get_character(character_id)
        if not char:
            char = self.get_character("barnaby_bear")

        base_char = char.get_consistent_prompt_suffix()
        prompt = (
            f"Preschool 3D animated cartoon scene, {setting}. "
            f"Featuring {base_char}. "
            f"Character Action: {scene_action}. "
            f"Habits: {char.animation_habits}. "
            f"Soft volumetric lighting, cheerful bright pastel atmosphere, high definition render, masterpiece"
        )
        return SafetyChecker.sanitize_prompt(prompt)

character_manager = CharacterManager()
