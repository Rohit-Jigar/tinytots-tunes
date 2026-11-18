import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    # Application Info
    APP_NAME: str = os.getenv("APP_NAME", "TinyTots Tunes Video Factory")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # Directories
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / os.getenv("DATA_DIR", "data")
    PROJECTS_DIR: Path = BASE_DIR / os.getenv("PROJECTS_DIR", "projects")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

    # Asset Generation Providers
    # Options: 'pollinations', 'openai', 'stability', 'mock'
    IMAGE_PROVIDER: str = os.getenv("IMAGE_PROVIDER", "pollinations").lower()
    # Options: 'edge_tts', 'elevenlabs', 'openai', 'mock'
    VOICE_PROVIDER: str = os.getenv("VOICE_PROVIDER", "edge_tts").lower()
    DEFAULT_VOICE_NAME: str = os.getenv("DEFAULT_VOICE_NAME", "en-US-AnaNeural")
    # Options: 'procedural', 'suno', 'udio', 'mock'
    MUSIC_PROVIDER: str = os.getenv("MUSIC_PROVIDER", "procedural").lower()

    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    STABILITY_API_KEY: Optional[str] = os.getenv("STABILITY_API_KEY")
    ELEVENLABS_API_KEY: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_VOICE_ID: Optional[str] = os.getenv("ELEVENLABS_VOICE_ID")
    SUNO_API_KEY: Optional[str] = os.getenv("SUNO_API_KEY")
    HUGGINGFACE_API_TOKEN: Optional[str] = os.getenv("HUGGINGFACE_API_TOKEN")
    REPLICATE_API_TOKEN: Optional[str] = os.getenv("REPLICATE_API_TOKEN")
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    # Video Engines
    FFMPEG_PATH: str = os.getenv("FFMPEG_PATH", "ffmpeg")
    BLENDER_PATH: Optional[str] = os.getenv("BLENDER_PATH")
    VIDEO_WIDTH: int = int(os.getenv("VIDEO_WIDTH", "1920"))
    VIDEO_HEIGHT: int = int(os.getenv("VIDEO_HEIGHT", "1080"))
    VIDEO_FPS: int = int(os.getenv("VIDEO_FPS", "30"))

    # YouTube API
    YOUTUBE_MOCK_MODE: bool = os.getenv("YOUTUBE_MOCK_MODE", "True").lower() in ("true", "1", "yes")
    YOUTUBE_CLIENT_SECRETS_FILE: str = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
    YOUTUBE_CREDENTIALS_STORAGE: str = os.getenv("YOUTUBE_CREDENTIALS_STORAGE", "youtube_token.json")
    YOUTUBE_DEFAULT_PRIVACY: str = os.getenv("YOUTUBE_DEFAULT_PRIVACY", "private")
    YOUTUBE_CATEGORY_ID: str = os.getenv("YOUTUBE_CATEGORY_ID", "1") # 1 = Film & Animation
    YOUTUBE_MADE_FOR_KIDS: bool = os.getenv("YOUTUBE_MADE_FOR_KIDS", "True").lower() in ("true", "1", "yes")

    # Queue & Automation
    MAX_CONCURRENT_JOBS: int = int(os.getenv("MAX_CONCURRENT_JOBS", "2"))
    QUEUE_POLL_INTERVAL: int = int(os.getenv("QUEUE_POLL_INTERVAL", "5"))
    AUTO_RETRY_FAILED: bool = os.getenv("AUTO_RETRY_FAILED", "True").lower() in ("true", "1", "yes")
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    AUTO_PUBLISH_APPROVED: bool = os.getenv("AUTO_PUBLISH_APPROVED", "False").lower() in ("true", "1", "yes")

config = Config()

