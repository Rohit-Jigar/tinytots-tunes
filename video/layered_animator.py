import os
import re
import math
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from core.config import config
from core.logger import logger
from characters.models import Character
from characters.manager import character_manager

class LayeredKineticAnimator:
    """
    Multi-Layer 2.5D Animated Puppet & Parallax Compositor:
    Produces broadcast-quality animated preschool scenes without flat slideshow artifacts:
    - Layer 1: Parallax panoramic background with ambient drift
    - Layer 2: Midground scenery & props
    - Layer 3: Kinetic character puppet with beat-synced squash & stretch, eye blinks, and head-tilt
    - Layer 4: Foreground floating particle atmosphere (musical notes, sparkle stars, bubbles)
    - Layer 5: Dynamic multi-layer camera trajectory
    """

    @classmethod
    def generate_scene_frames(
        cls,
        character: Character,
        setting_type: str,
        action: str,
        output_dir: str,
        duration_seconds: float,
        bpm: int = 120,
        fps: int = 30
    ) -> List[str]:
        """
        Renders individual animated frames with procedural character kinetics,
        squash-and-stretch to the BPM beat, blinking, and atmospheric particles.
        """
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        total_frames = int(duration_seconds * fps)
        width, height = config.VIDEO_WIDTH, config.VIDEO_HEIGHT

        # 1. Generate or load base scenic background (wider than 1920 for parallax panning)
        bg_width = int(width * 1.25)
        bg = cls._render_scenic_background(setting_type, bg_width, height)

        # 2. Extract character sprite / mascot
        char_sprite_open = cls._render_character_sprite(character, blink=False)
        char_sprite_blink = cls._render_character_sprite(character, blink=True)

        frame_paths = []
        beat_period = 60.0 / bpm

        logger.info("Synthesizing %d animated 2.5D frames (%.1fs @ %dfps, BPM: %d)...",
                    total_frames, duration_seconds, fps, bpm)

        for f in range(total_frames):
            t = f / fps
            frame_img = Image.new("RGBA", (width, height), (0, 0, 0, 255))

            # A. Layer 1: Parallax Background Pan
            # Slow pan across the wider background canvas
            pan_offset_x = int((f / total_frames) * (bg_width - width))
            cropped_bg = bg.crop((pan_offset_x, 0, pan_offset_x + width, height))
            frame_img.paste(cropped_bg, (0, 0))

            # B. Layer 2: Character Puppet with Beat-Synced Squash & Stretch
            # Beat bounce: 2 bounces per bar
            beat_phase = (t % beat_period) / beat_period
            bounce_y = -math.sin(beat_phase * math.pi) * 28.0
            squash_factor = 1.0 + math.sin(beat_phase * math.pi * 2) * 0.06
            stretch_factor = 1.0 - math.sin(beat_phase * math.pi * 2) * 0.04

            # Blinking logic (blinks for 4 frames every 3 seconds)
            is_blinking = (f % (fps * 3)) < 4
            active_sprite = char_sprite_blink if is_blinking else char_sprite_open

            # Scale character with squash and stretch
            sprite_w, sprite_h = active_sprite.size
            new_w = int(sprite_w * stretch_factor)
            new_h = int(sprite_h * squash_factor)
            scaled_char = active_sprite.resize((new_w, new_h), Image.Resampling.BILINEAR)

            # Character Position on screen
            char_base_x = (width - new_w) // 2
            char_base_y = int(height * 0.45) + int(bounce_y)

            # Gentle rotational sway to the rhythm
            sway_angle = math.sin(t * math.pi * (bpm / 60.0) * 0.5) * 3.5
            rotated_char = scaled_char.rotate(sway_angle, resample=Image.Resampling.BILINEAR, expand=True)

            # Center adjusted position after rotation
            rot_w, rot_h = rotated_char.size
            final_x = char_base_x - (rot_w - new_w) // 2
            final_y = char_base_y - (rot_h - new_h) // 2

            # Soft ground contact shadow
            shadow_w = int(new_w * 0.85)
            shadow_h = int(40 * (1.0 - abs(bounce_y) / 40.0))
            shadow_img = Image.new("RGBA", (shadow_w, shadow_h), (0, 0, 0, int(90 * (1.0 - abs(bounce_y) / 60.0))))
            shadow_x = char_base_x + (new_w - shadow_w) // 2
            shadow_y = int(height * 0.84)
            frame_img.paste(shadow_img, (shadow_x, shadow_y), shadow_img)

            # Paste character
            frame_img.paste(rotated_char, (final_x, final_y), rotated_char)

            # C. Layer 3: Atmospheric Floating Particles (Musical Notes & Sparkles)
            cls._draw_ambient_particles(frame_img, f, total_frames, width, height)

            # Save frame JPEG/PNG
            frame_filename = out_path / f"frame_{f:04d}.jpg"
            frame_rgb = frame_img.convert("RGB")
            frame_rgb.save(frame_filename, "JPEG", quality=90)
            frame_paths.append(str(frame_filename))

        return frame_paths

    @classmethod
    def _render_scenic_background(cls, setting: str, width: int, height: int) -> Image.Image:
        """Draws rich 1080p preschool environment (Sky, rolling green hills, smiling sun, pastel clouds)."""
        bg = Image.new("RGB", (width, height), color="#87CEEB")
        draw = ImageDraw.Draw(bg)

        # 1. Vibrant Sky Gradient
        for y in range(int(height * 0.75)):
            r = int(90 + (190 - 90) * (y / (height * 0.75)))
            g = int(180 + (230 - 180) * (y / (height * 0.75)))
            b = int(250 + (255 - 250) * (y / (height * 0.75)))
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 2. Glowing Sun in corner
        sun_center = (260, 180)
        sun_r = 90
        for angle in range(0, 360, 24):
            rad = math.radians(angle)
            x_end = sun_center[0] + int(145 * math.cos(rad))
            y_end = sun_center[1] + int(145 * math.sin(rad))
            draw.line([sun_center, (x_end, y_end)], fill="#FFD166", width=8)
        draw.ellipse([(sun_center[0] - sun_r, sun_center[1] - sun_r),
                      (sun_center[0] + sun_r, sun_center[1] + sun_r)], fill="#FFB703", outline="#FB8500", width=6)
        # Sun smile & blushing cheeks
        draw.ellipse([(sun_center[0] - 65, sun_center[1] + 10), (sun_center[0] - 25, sun_center[1] + 45)], fill="#FF758F")
        draw.ellipse([(sun_center[0] + 25, sun_center[1] + 10), (sun_center[0] + 65, sun_center[1] + 45)], fill="#FF758F")
        draw.arc([(sun_center[0] - 40, sun_center[1] - 15), (sun_center[0] + 40, sun_center[1] + 50)], start=10, end=170, fill="#D97706", width=6)
        draw.ellipse([(sun_center[0] - 35, sun_center[1] - 25), (sun_center[0] - 15, sun_center[1] - 5)], fill="#1E293B")
        draw.ellipse([(sun_center[0] + 15, sun_center[1] - 25), (sun_center[0] + 35, sun_center[1] - 5)], fill="#1E293B")

        # 3. Fluffy Cartoon Clouds
        for cx, cy in [(750, 160), (1400, 130), (2000, 190)]:
            draw.ellipse([(cx - 90, cy - 50), (cx + 90, cy + 50)], fill="#FFFFFF")
            draw.ellipse([(cx - 140, cy - 20), (cx, cy + 50)], fill="#FFFFFF")
            draw.ellipse([(cx, cy - 30), (cx + 140, cy + 50)], fill="#FFFFFF")

        # 4. Multi-Layer Rolling Hills
        # Distant Hills
        draw.chord([(-100, int(height * 0.45)), (width + 200, int(height * 1.35))], start=180, end=360, fill="#70E000")
        # Mid Hills
        draw.chord([(200, int(height * 0.54)), (width + 400, int(height * 1.45))], start=180, end=360, fill="#38B000")
        # Foreground Rich Hill
        draw.chord([(-300, int(height * 0.62)), (width + 100, int(height * 1.5))], start=180, end=360, fill="#007200")

        # 5. Little Flowers on the Hill
        flower_colors = ["#FF0054", "#FFBD00", "#FF5400", "#7209B7", "#FFFFFF"]
        for fx in range(80, width - 60, 110):
            fy = int(height * 0.82 + (fx % 80) * 1.4)
            fcol = flower_colors[fx % len(flower_colors)]
            draw.ellipse([(fx - 14, fy - 14), (fx + 14, fy + 14)], fill=fcol)
            draw.ellipse([(fx - 6, fy - 6), (fx + 6, fy + 6)], fill="#FFD166")

        return bg

    @classmethod
    def _render_character_sprite(cls, char: Character, blink: bool = False) -> Image.Image:
        """Renders transparent character sprite for kinetic puppet animation."""
        size = 620
        sprite = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sprite)
        cx, cy = size // 2, int(size * 0.58)

        if char.id == "barnaby_bear":
            # Brown teddy bear with teal dungarees
            # Body
            draw.ellipse([cx - 140, cy - 120, cx + 140, cy + 180], fill="#8B5A2B", outline="#5C3A1E", width=7)
            # Teal dungarees
            draw.chord([cx - 140, cy - 20, cx + 140, cy + 180], start=0, end=180, fill="#00A896", outline="#007F70", width=6)
            # Red button
            draw.ellipse([cx - 22, cy + 30, cx + 22, cy + 74], fill="#E63946")
            # Head
            draw.ellipse([cx - 110, cy - 220, cx + 110, cy - 20], fill="#8B5A2B", outline="#5C3A1E", width=7)
            # Ears
            draw.ellipse([cx - 130, cy - 250, cx - 65, cy - 180], fill="#8B5A2B", outline="#5C3A1E", width=6)
            draw.ellipse([cx + 65, cy - 250, cx + 130, cy - 180], fill="#8B5A2B", outline="#5C3A1E", width=6)
            draw.ellipse([cx - 115, cy - 240, cx - 80, cy - 195], fill="#FFF1D0")
            draw.ellipse([cx + 80, cy - 240, cx + 115, cy - 195], fill="#FFF1D0")
            # Snout & Smile
            draw.ellipse([cx - 45, cy - 120, cx + 45, cy - 55], fill="#FFF1D0")
            draw.ellipse([cx - 18, cy - 118, cx + 18, cy - 90], fill="#1E293B")
            draw.arc([cx - 26, cy - 98, cx + 26, cy - 70], start=10, end=170, fill="#1E293B", width=6)

            # Eyes (Open or Blinking)
            if blink:
                draw.arc([cx - 50, cy - 165, cx - 20, cy - 145], start=180, end=360, fill="#1E293B", width=5)
                draw.arc([cx + 20, cy - 165, cx + 50, cy - 145], start=180, end=360, fill="#1E293B", width=5)
            else:
                draw.ellipse([cx - 50, cy - 170, cx - 20, cy - 135], fill="#1E293B")
                draw.ellipse([cx + 20, cy - 170, cx + 50, cy - 135], fill="#1E293B")
                draw.ellipse([cx - 42, cy - 165, cx - 32, cy - 150], fill="#FFFFFF")
                draw.ellipse([cx + 28, cy - 165, cx + 38, cy - 150], fill="#FFFFFF")

            # Waving Arm
            draw.ellipse([cx + 115, cy - 120, cx + 175, cy - 55], fill="#8B5A2B", outline="#5C3A1E", width=6)

        elif char.id == "pip_bird":
            # Yellow songbird in sky-blue aviator cap
            draw.ellipse([cx - 120, cy - 100, cx + 120, cy + 150], fill="#FFD166", outline="#F59E0B", width=7)
            # Aviator cap
            draw.chord([cx - 110, cy - 135, cx + 110, cy - 20], start=180, end=360, fill="#118AB2", outline="#0C6E8E", width=6)
            draw.polygon([(cx, cy - 15), (cx - 30, cy + 25), (cx + 30, cy + 25)], fill="#FF9F1C")
            if blink:
                draw.arc([cx - 55, cy - 65, cx - 25, cy - 45], start=180, end=360, fill="#1E293B", width=5)
                draw.arc([cx + 25, cy - 65, cx + 55, cy - 45], start=180, end=360, fill="#1E293B", width=5)
            else:
                draw.ellipse([cx - 55, cy - 70, cx - 25, cy - 35], fill="#1E293B")
                draw.ellipse([cx + 25, cy - 70, cx + 55, cy - 35], fill="#1E293B")
                draw.ellipse([cx - 48, cy - 66, cx - 38, cy - 50], fill="#FFFFFF")
                draw.ellipse([cx + 32, cy - 66, cx + 42, cy - 50], fill="#FFFFFF")
            # Flapping wings
            draw.ellipse([cx - 160, cy - 20, cx - 90, cy + 70], fill="#F59E0B")
            draw.ellipse([cx + 90, cy - 40, cx + 165, cy + 50], fill="#F59E0B")

        elif char.id == "penny_bunny":
            # Cute pink bunny in lavender pinafore
            # Ears
            draw.ellipse([cx - 95, cy - 275, cx - 35, cy - 90], fill="#FFB3C6", outline="#F43F5E", width=6)
            draw.ellipse([cx + 35, cy - 275, cx + 95, cy - 90], fill="#FFB3C6", outline="#F43F5E", width=6)
            draw.ellipse([cx - 80, cy - 255, cx - 50, cy - 110], fill="#FFF1F2")
            draw.ellipse([cx + 50, cy - 255, cx + 80, cy - 110], fill="#FFF1F2")
            # Body & Dress
            draw.ellipse([cx - 110, cy - 80, cx + 110, cy + 170], fill="#FFB3C6", outline="#F43F5E", width=7)
            draw.chord([cx - 105, cy + 15, cx + 105, cy + 170], start=0, end=180, fill="#C77DFF", outline="#A855F7", width=6)
            # Head
            draw.ellipse([cx - 95, cy - 145, cx + 95, cy], fill="#FFB3C6", outline="#F43F5E", width=7)
            draw.ellipse([cx - 18, cy - 65, cx + 18, cy - 42], fill="#FB7185")
            draw.arc([cx - 22, cy - 52, cx + 22, cy - 28], start=10, end=170, fill="#1E293B", width=5)
            if blink:
                draw.arc([cx - 45, cy - 100, cx - 20, cy - 80], start=180, end=360, fill="#1E293B", width=5)
                draw.arc([cx + 20, cy - 100, cx + 45, cy - 80], start=180, end=360, fill="#1E293B", width=5)
            else:
                draw.ellipse([cx - 48, cy - 105, cx - 18, cy - 68], fill="#1E293B")
                draw.ellipse([cx + 18, cy - 105, cx + 48, cy - 68], fill="#1E293B")
                draw.ellipse([cx - 40, cy - 100, cx - 30, cy - 82], fill="#FFFFFF")
                draw.ellipse([cx + 26, cy - 100, cx + 36, cy - 82], fill="#FFFFFF")

        elif char.id == "zara_zebra":
            # Playful zebra with purple stripes & mint overalls
            draw.ellipse([cx - 115, cy - 75, cx + 115, cy + 170], fill="#FFFFFF", outline="#7B2CBF", width=7)
            draw.chord([cx - 110, cy + 20, cx + 110, cy + 170], start=0, end=180, fill="#06D6A0", outline="#059669", width=6)
            draw.ellipse([cx - 95, cy - 170, cx + 95, cy - 15], fill="#FFFFFF", outline="#7B2CBF", width=7)
            for sy in range(cy - 135, cy - 35, 24):
                draw.line([(cx - 90, sy), (cx - 48, sy)], fill="#7B2CBF", width=7)
                draw.line([(cx + 48, sy), (cx + 90, sy)], fill="#7B2CBF", width=7)
            if blink:
                draw.arc([cx - 45, cy - 110, cx - 20, cy - 90], start=180, end=360, fill="#1E293B", width=5)
                draw.arc([cx + 20, cy - 110, cx + 45, cy - 90], start=180, end=360, fill="#1E293B", width=5)
            else:
                draw.ellipse([cx - 48, cy - 115, cx - 20, cy - 75], fill="#1E293B")
                draw.ellipse([cx + 20, cy - 115, cx + 48, cy - 75], fill="#1E293B")
                draw.ellipse([cx - 40, cy - 110, cx - 30, cy - 92], fill="#FFFFFF")
                draw.ellipse([cx + 28, cy - 110, cx + 38, cy - 92], fill="#FFFFFF")
            draw.arc([cx - 28, cy - 60, cx + 28, cy - 35], start=10, end=170, fill="#7B2CBF", width=5)

        else: # sunny_sunshine
            # Beaming little sunshine
            for angle in range(0, 360, 24):
                rad = math.radians(angle)
                x1 = cx + int(120 * math.cos(rad))
                y1 = cy + int(120 * math.sin(rad))
                x2 = cx + int(170 * math.cos(rad))
                y2 = cy + int(170 * math.sin(rad))
                draw.line([(x1, y1), (x2, y2)], fill="#FF8800", width=12)
            draw.ellipse([cx - 115, cy - 115, cx + 115, cy + 115], fill="#FFD000", outline="#FF8800", width=8)
            draw.ellipse([cx - 90, cy - 5, cx - 40, cy + 35], fill="#FF595E")
            draw.ellipse([(cx + 40, cy - 5), (cx + 90, cy + 35)], fill="#FF595E")
            if blink:
                draw.arc([cx - 50, cy - 50, cx - 20, cy - 30], start=180, end=360, fill="#1E293B", width=5)
                draw.arc([cx + 20, cy - 50, cx + 50, cy - 30], start=180, end=360, fill="#1E293B", width=5)
            else:
                draw.ellipse([cx - 52, cy - 55, cx - 20, cy - 15], fill="#1E293B")
                draw.ellipse([cx + 20, cy - 55, cx + 52, cy - 15], fill="#1E293B")
                draw.ellipse([cx - 44, cy - 50, cx - 32, cy - 32], fill="#FFFFFF")
                draw.ellipse([cx + 28, cy - 50, cx + 40, cy - 32], fill="#FFFFFF")
            draw.arc([cx - 50, cy - 15, cx + 50, cy + 60], start=10, end=170, fill="#C2410C", width=7)

        return sprite

    @classmethod
    def _draw_ambient_particles(cls, img: Image.Image, frame: int, total_frames: int, width: int, height: int):
        """Draws floating preschool particles (sparkle stars & musical notes) moving upwards."""
        draw = ImageDraw.Draw(img)
        particles = [
            (240, "#FFD166", "✨"),
            (520, "#FF758F", "🎵"),
            (960, "#06D6A0", "⭐"),
            (1380, "#FFB703", "🎶"),
            (1680, "#4CC9F0", "✨")
        ]
        for base_x, color, sym in particles:
            # Floating upward trajectory with horizontal oscillation
            y_pos = (height - int((frame * 4.5 + base_x) % height))
            x_pos = base_x + int(math.sin(frame * 0.08 + base_x) * 22)
            draw.text((x_pos, y_pos), sym, fill=color, font=None)

    @classmethod
    def render_animated_scene_clip(
        cls,
        character: Character,
        setting_type: str,
        action: str,
        audio_path: str,
        duration: float,
        output_clip_path: str,
        display_text: str = "",
        bpm: int = 120
    ) -> str:
        """
        Renders complete multi-layer animated clip directly to 1080p MP4 using FFmpeg image2 pipeline.
        """
        temp_frames_dir = Path(output_clip_path).parent / f"frames_{Path(output_clip_path).stem}"
        temp_frames_dir.mkdir(parents=True, exist_ok=True)

        # 1. Synthesize animated frames
        cls.generate_scene_frames(
            character=character,
            setting_type=setting_type,
            action=action,
            output_dir=str(temp_frames_dir),
            duration_seconds=duration,
            bpm=bpm,
            fps=config.VIDEO_FPS
        )

        # 2. Build Subtitle Filter
        vf_filters = []
        if display_text:
            safe_text = re.sub(r'\[.*?\]', '', display_text).strip()
            safe_text = safe_text.replace("'", "’").replace(":", "\\:").replace("%", "\\%").replace("[", "").replace("]", "")
            if safe_text:
                # Large, glowing preschool karaoke typography with rounded box
                drawtext_filter = (
                    f"drawtext=text='{safe_text}':"
                    f"font=Arial:fontsize=54:fontcolor=0xFFE600:bordercolor=0x000000:borderw=7:"
                    f"box=1:boxcolor=0x000000@0.6:boxborderw=24:"
                    f"x=(w-text_w)/2:y=h-th-85"
                )
                vf_filters.append(drawtext_filter)

        vf = ",".join(vf_filters) if vf_filters else "null"

        # 3. Render MP4 with FFmpeg from frames sequence + vocal audio
        frame_pattern = str(temp_frames_dir / "frame_%04d.jpg").replace("\\", "/")
        args = [
            config.FFMPEG_PATH, "-y",
            "-framerate", str(config.VIDEO_FPS),
            "-i", frame_pattern,
            "-i", audio_path,
            "-vf", vf,
            "-t", str(duration),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            output_clip_path
        ]
        subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

        # Clean up temporary frames
        import shutil
        shutil.rmtree(temp_frames_dir, ignore_errors=True)

        logger.info("Successfully produced animated 2.5D scene clip: %s (%.2f MB)",
                    output_clip_path, os.path.getsize(output_clip_path) / (1024 * 1024))
        return output_clip_path

layered_animator = LayeredKineticAnimator()
