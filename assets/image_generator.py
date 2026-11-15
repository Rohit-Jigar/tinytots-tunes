import os
import urllib.parse
import requests
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from core.config import config
from core.logger import logger
from core.safety import SafetyChecker
from assets.base import BaseImageProvider

class PollinationsImageProvider(BaseImageProvider):
    """
    Generates high-quality AI illustrations using Pollinations.ai (Free, no API key needed).
    Uses Flux/Stable Diffusion models for children's cartoon style.
    """
    def generate_image(self, prompt: str, output_path: str, width: int = 1920, height: int = 1080) -> str:
        safe_prompt = SafetyChecker.sanitize_prompt(prompt)
        encoded_prompt = urllib.parse.quote(safe_prompt)
        seed = random.randint(1000, 999999)
        # 16:9 ratio free tier
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"
        logger.info("Calling Pollinations AI for image: %s...", safe_prompt[:60])

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)

        logger.info("Saved generated image to %s", output_path)
        return output_path

class OpenAIImageProvider(BaseImageProvider):
    """Generates images using OpenAI DALL-E 3 API."""
    def generate_image(self, prompt: str, output_path: str, width: int = 1920, height: int = 1080) -> str:
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured in .env!")

        safe_prompt = SafetyChecker.sanitize_prompt(prompt)
        headers = {
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "dall-e-3",
            "prompt": f"Preschool cartoon illustration for toddler animation: {safe_prompt}",
            "n": 1,
            "size": "1792x1024",  # Landscape
            "quality": "standard"
        }

        resp = requests.post("https://api.openai.com/v1/images/generations", json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        img_url = data["data"][0]["url"]

        img_data = requests.get(img_url, timeout=30).content
        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(img_data)

        # Resize to target 1920x1080 if needed
        with Image.open(output_path) as im:
            im = im.resize((width, height), Image.Resampling.LANCZOS)
            im.save(output_path)

        return output_path

class StabilityImageProvider(BaseImageProvider):
    """Generates images using Stability AI SDXL API."""
    def generate_image(self, prompt: str, output_path: str, width: int = 1920, height: int = 1080) -> str:
        if not config.STABILITY_API_KEY:
            raise ValueError("STABILITY_API_KEY is not configured in .env!")

        safe_prompt = SafetyChecker.sanitize_prompt(prompt)
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        headers = {
            "Authorization": f"Bearer {config.STABILITY_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        body = {
            "text_prompts": [
                {"text": f"Preschool 3D cute cartoon animation scene, {safe_prompt}", "weight": 1.0},
                {"text": "scary, dark, realistic, photographic, deformed, blurry", "weight": -1.0}
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }

        resp = requests.post(url, headers=headers, json=body, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        import base64
        image_bytes = base64.b64decode(data["artifacts"][0]["base64"])

        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_bytes)

        with Image.open(output_path) as im:
            im = im.resize((width, height), Image.Resampling.LANCZOS)
            im.save(output_path)

        return output_path

class MockImageProvider(BaseImageProvider):
    """
    Procedural Vector-Style Graphic Generator:
    Generates rich, vibrant, high-definition 1080p preschool landscapes with:
    - Sunny blue sky gradient
    - Radiant smiling cartoon sun with rays
    - Fluffy clouds
    - Multi-layered rolling green hills with flowers
    - Animated rainbow or pastel stars
    - Clean character showcase emblem with vibrant colors
    Guarantees 100% offline generation with zero network dependency.
    """
    def generate_image(self, prompt: str, output_path: str, width: int = 1920, height: int = 1080) -> str:
        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        img = Image.new("RGB", (width, height), color="#87CEEB")
        draw = ImageDraw.Draw(img)

        # 1. Sky Gradient (from #64B5F6 to #BBDEFB)
        for y in range(int(height * 0.7)):
            r = int(100 + (187 - 100) * (y / (height * 0.7)))
            g = int(181 + (222 - 181) * (y / (height * 0.7)))
            b = int(246 + (251 - 246) * (y / (height * 0.7)))
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # 2. Glowing Cartoon Sun (Top-Left)
        sun_center = (240, 200)
        sun_radius = 90
        # Draw sun rays
        for angle in range(0, 360, 30):
            import math
            rad = math.radians(angle)
            x_end = sun_center[0] + int(140 * math.cos(rad))
            y_end = sun_center[1] + int(140 * math.sin(rad))
            draw.line([sun_center, (x_end, y_end)], fill="#FFD166", width=8)
        # Sun disk
        draw.ellipse([
            (sun_center[0] - sun_radius, sun_center[1] - sun_radius),
            (sun_center[0] + sun_radius, sun_center[1] + sun_radius)
        ], fill="#FFB703", outline="#FB8500", width=6)
        # Sun smiling face
        draw.arc([(sun_center[0] - 40, sun_center[1] - 20), (sun_center[0] + 40, sun_center[1] + 45)], start=10, end=170, fill="#E65100", width=5)
        draw.ellipse([(sun_center[0] - 30, sun_center[1] - 25), (sun_center[0] - 15, sun_center[1] - 10)], fill="#E65100")
        draw.ellipse([(sun_center[0] + 15, sun_center[1] - 25), (sun_center[0] + 30, sun_center[1] - 10)], fill="#E65100")

        # 3. Fluffy Cartoon Clouds
        def draw_cloud(cx, cy, scale=1.0):
            r = int(50 * scale)
            draw.ellipse([(cx - r * 1.5, cy - r), (cx + r * 1.5, cy + r)], fill="#FFFFFF")
            draw.ellipse([(cx - r * 2.2, cy - r * 0.4), (cx, cy + r * 0.8)], fill="#FFFFFF")
            draw.ellipse([(cx, cy - r * 0.5), (cx + r * 2.2, cy + r * 0.8)], fill="#FFFFFF")

        draw_cloud(700, 180, scale=1.4)
        draw_cloud(1350, 140, scale=1.2)
        draw_cloud(1700, 230, scale=0.9)

        # 4. Colorful Rainbow Arc
        rainbow_colors = ["#FF595E", "#FFCA3A", "#8AC926", "#1982C4", "#6A4C93"]
        center_x = width // 2
        center_y = int(height * 0.85)
        for i, col in enumerate(rainbow_colors):
            rad = 520 - (i * 22)
            draw.arc([(center_x - rad, center_y - rad), (center_x + rad, center_y + rad)], start=190, end=350, fill=col, width=20)

        # 5. Layered Rolling Green Hills
        # Background Hill
        draw.chord([(-300, int(height * 0.45)), (width + 400, int(height * 1.3))], start=180, end=360, fill="#70E000")
        # Midground Hill
        draw.chord([(200, int(height * 0.52)), (width + 600, int(height * 1.4))], start=180, end=360, fill="#38B000")
        # Foreground Hill
        draw.chord([(-200, int(height * 0.58)), (width - 100, int(height * 1.4))], start=180, end=360, fill="#007200")

        # 6. Little Flowers on the Hill
        flower_colors = ["#FF0054", "#9E0059", "#FF5400", "#FFBD00", "#FFFFFF"]
        for fx in range(100, width - 100, 120):
            fy = int(height * 0.78 + (fx % 90) * 1.8)
            fcol = flower_colors[fx % len(flower_colors)]
            draw.ellipse([(fx - 15, fy - 15), (fx + 15, fy + 15)], fill=fcol)
            draw.ellipse([(fx - 6, fy - 6), (fx + 6, fy + 6)], fill="#FFD166")

        # 7. Center Character Silhouette / Emblem
        char_x, char_y = width // 2, int(height * 0.68)
        # Soft shadow
        draw.ellipse([(char_x - 140, char_y + 110), (char_x + 140, char_y + 160)], fill="#004b00")
        # Body (Honey Bear / Character shape)
        draw.ellipse([(char_x - 110, char_y - 80), (char_x + 110, char_y + 120)], fill="#C68B59", outline="#8B5A2B", width=8)
        # Dungarees (Teal)
        draw.chord([(char_x - 110, char_y), (char_x + 110, char_y + 140)], start=0, end=180, fill="#00A896", outline="#007F70", width=6)
        # Head
        draw.ellipse([(char_x - 90, char_y - 200), (char_x + 90, char_y - 40)], fill="#C68B59", outline="#8B5A2B", width=8)
        # Ears
        draw.ellipse([(char_x - 105, char_y - 225), (char_x - 55, char_y - 175)], fill="#C68B59", outline="#8B5A2B", width=6)
        draw.ellipse([(char_x + 55, char_y - 225), (char_x + 105, char_y - 175)], fill="#C68B59", outline="#8B5A2B", width=6)
        draw.ellipse([(char_x - 95, char_y - 215), (char_x - 65, char_y - 185)], fill="#FFE0B2")
        draw.ellipse([(char_x + 65, char_y - 215), (char_x + 95, char_y - 185)], fill="#FFE0B2")
        # Eyes
        draw.ellipse([(char_x - 40, char_y - 140), (char_x - 15, char_y - 105)], fill="#3E2723")
        draw.ellipse([(char_x + 15, char_y - 140), (char_x + 40, char_y - 105)], fill="#3E2723")
        draw.ellipse([(char_x - 30, char_y - 135), (char_x - 20, char_y - 120)], fill="#FFFFFF")
        draw.ellipse([(char_x + 25, char_y - 135), (char_x + 35, char_y - 120)], fill="#FFFFFF")
        # Snout & Smile
        draw.ellipse([(char_x - 45, char_y - 105), (char_x + 45, char_y - 55)], fill="#FFE0B2")
        draw.ellipse([(char_x - 18, char_y - 102), (char_x + 18, char_y - 78)], fill="#3E2723")
        draw.arc([(char_x - 25, char_y - 85), (char_x + 25, char_y - 60)], start=10, end=170, fill="#3E2723", width=5)
        # Waving hand
        draw.ellipse([(char_x + 95, char_y - 120), (char_x + 155, char_y - 70)], fill="#C68B59", outline="#8B5A2B", width=6)

        # 8. Subtle Watermark Badge
        draw.rectangle([(width - 340, height - 70), (width - 40, height - 30)], fill=(0, 0, 0, 160))
        # Draw label
        draw.text((width - 325, height - 62), "TinyTots Tunes Original", fill="#FFFFFF")

        img.save(output_path, quality=95)
        logger.info("Generated rich mock illustration at %s", output_path)
        return output_path

class ImageOrchestrator:
    """Manages multi-provider image generation with seamless fallback and provider circuit-breaker."""
    def __init__(self):
        self.providers = {
            "pollinations": PollinationsImageProvider(),
            "openai": OpenAIImageProvider(),
            "stability": StabilityImageProvider(),
            "mock": MockImageProvider()
        }
        self._offline_providers = set()

    def generate(self, prompt: str, output_path: str, provider_name: str = None, width: int = 1920, height: int = 1080) -> str:
        chosen = (provider_name or config.IMAGE_PROVIDER).lower()
        if chosen in self._offline_providers:
            return self.providers["mock"].generate_image(prompt, output_path, width=width, height=height)

        provider = self.providers.get(chosen, self.providers["mock"])

        try:
            return provider.generate_image(prompt, output_path, width=width, height=height)
        except Exception as e:
            logger.warning("Primary image provider '%s' failed: %s. Switching to Mock Image Generator circuit.", chosen, e)
            self._offline_providers.add(chosen)
            return self.providers["mock"].generate_image(prompt, output_path, width=width, height=height)

image_generator = ImageOrchestrator()
