from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class BaseImageProvider(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, output_path: str, width: int = 1920, height: int = 1080) -> str:
        """Generates an image from a prompt and saves to output_path."""
        pass

class BaseVoiceProvider(ABC):
    @abstractmethod
    def synthesize_speech(self, text: str, output_path: str, voice_name: Optional[str] = None) -> str:
        """Synthesizes text to an audio file (e.g. mp3/wav) and saves to output_path."""
        pass

class BaseMusicProvider(ABC):
    @abstractmethod
    def generate_music(self, prompt: str, duration_seconds: float, output_path: str, tempo: str = "120 BPM") -> str:
        """Generates or synthesizes background music track matching duration_seconds."""
        pass

