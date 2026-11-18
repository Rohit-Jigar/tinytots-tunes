# 👶 TinyTots Tunes - AI Kids YouTube Video Factory

An automated Python-based animation and video production application built specifically for preschool and toddler YouTube channels. TinyTots Tunes manages the entire preschool media creation pipeline: from educational song ideation, rhyming lyrics, and character consistency, to multi-provider asset generation, FFmpeg/Blender 1080p rendering, high-CTR 1280x720 thumbnails, and COPPA-compliant YouTube publishing with human-in-the-loop approval.

---

> 📖 **Quick Documentation Links**:
> - [Free API Keys & Modern 3D Video Setup Guide](FREE_API_KEYS_GUIDE.md) — 100% free keys for 3D visuals, singing vocals, and high-speed generation.
> - [Production Deployment Guide](DEPLOYMENT.md) — Step-by-step GitHub Pages frontend & Render backend cloud setup.
> - [Live Web Portal](https://rohit-jigar.github.io/tinytots-tunes/) — Official streaming portal on GitHub Pages.

---

## 🌟 Key Features

### 1. Content Planner
- **Curriculum-Driven Ideation**: Generates original song topics mapped to early childhood milestones (Colors, Numbers & Counting, Hygiene & Habits, Animal Sounds, Bedtime Lullabies, Sharing & Feelings).
- **Rhyming Lyrics & Scripts**: Composes repetitive, toddler-friendly nursery rhymes with explicit motor action directions (`[Clap hands!]`, `[Jump!]`) and sound effect cues (`[Pop!]`, `[Chime!]`, `[Giggle]`).
- **Scene-by-Scene Storyboards**: Breaks songs into 3.5s–5.0s digestible scenes with camera motion directions, character actions, and visual prompts.
- **YouTube SEO Optimization**: Auto-generates clickable titles, chapter timestamp descriptions, 15+ preschool tags, and thumbnail visual prompts.
- **Structured Project Workspaces**: Every song is isolated into `projects/{project_id}/` holding `project.json`, `storyboard.json`, assets, audio stems, master video, and thumbnails.

### 2. Character Management & Trademark Safety
- **Original Character Roster**:
  - **Barnaby Bear**: A curious honey bear in bright teal dungarees with a red wooden button (`#C68B59`, `#00A896`, `#FFF1D0`, `#E63946`).
  - **Pip & Penny**: Synchronized waddling penguin twins with sunny yellow bowties and coral ribbons (`#4A6FA5`, `#FFE066`, `#FF758F`).
  - **Zara Zebra**: A creative zebra foal with whimsical purple stripes and lavender artist overalls (`#7B2CBF`, `#FFFFFF`, `#FFB703`).
  - **Sunny the Starling**: A cheerful golden songbird in a sky-blue aviator cap (`#FFD166`, `#118AB2`, `#FF9F1C`).
- **Visual Continuity**: Consistent wardrobe, color hex palettes, and facial features enforced through locked prompt suffixes across all scenes.
- **Strict Copyright Shield**: Active rule filter disallows Disney, Marvel, Cocomelon, Peppa Pig, Pinkfong/Baby Shark, Bluey, Paw Patrol, and other protected children's franchises.

### 3. Pluggable Asset Generation
- **Image Generation**:
  - `pollinations`: High-quality, fast, free AI image generation (no API key needed).
  - `openai`: DALL-E 3 (`1792x1024` landscape).
  - `stability`: Stability AI SDXL text-to-image API.
  - `mock`: Built-in Pillow 1080p vector-style landscape illustrator (sunny gradients, rolling hills, cartoon sun, character emblem). Guaranteed 100% offline fallback!
- **Voice Synthesis**:
  - `edge_tts`: Microsoft Edge Neural TTS (`en-US-AnaNeural` child voice, `en-US-JennyNeural`, free).
  - `windows_sapi`: Native Windows desktop speech synthesis (Zira/David), zero dependencies, instant local audio.
  - `openai`: OpenAI `tts-1` (`alloy`, `nova`, `shimmer`).
  - `elevenlabs`: ElevenLabs premium expressive vocal API.
- **Music Generation**:
  - `procedural`: Multi-track nursery music synthesizer built in pure Python (`numpy` + `scipy.io.wavfile`). Generates upbeat bell melodies (marimba/glockenspiel), warm chord progressions (I-IV-V-I), walking basslines, and shaker rhythms. 100% royalty-free!
  - `suno`: Suno AI API integration hooks.
- **Sound Effects (SFX)**:
  - Procedural sound effect synthesizer (`pop`, `chime`, `giggle`, `splash`, `clap`, `boing`).

### 4. Video Production Engine
- **FFmpeg 1080p Compositor**:
  - **Dynamic Ken Burns Motion**: `zoom_in`, `zoom_out`, `pan_right`, `pan_left`, and `gentle_bounce` (toddler dance rhythm).
  - **Karaoke Subtitle Styling**: High-contrast yellow bubble typography with dark drop shadow and rounded banner boxes for toddlers.
  - **Intelligent Audio Mixing**: Voiceovers mixed at 0 dB, ducked background music at -14 dB, synced SFX.
  - **Broadcast Quality**: 1920x1080 Full HD, 30fps H.264 (`yuv420p`), AAC stereo, `faststart` enabled for instant streaming.
- **Remotion Code-Based Motion Graphics & Three.js (`remotion-video` Skill)**:
  - Code-based video composition using React, springs, and `@remotion/three`.
  - Generates standalone Remotion projects with kinetic typography and 3D animated star/cloud overlays.
  - Preview via `npm run dev` and automated headless rendering via `npx remotion render`.
- **Post-Production Automation (`audio-postproduction-automation` Skill)**:
  - **Whisper Integration**: Millisecond-accurate word-level karaoke timestamp extraction.
  - **Sero Dead-Air Removal**: Automatic jump cuts detecting silences >350ms to keep toddler attention spans engaged.
  - **Broadcast Audio Mastering**: 80Hz high-pass filter, +3.5dB vocal presence EQ at 3.2kHz, compression, and YouTube EBU R128 (-14 LUFS) normalization.
- **Stateful Video Direction (`omni-video-gemini` Skill)**:
  - Integration with Gemini Interactions API tools (`animate_image`, `edit_video`, `generate_video`, `edit_user_video`).
  - Server-side `interaction_id` chaining to preserve character wardrobe, lighting, and art style across scene cuts without re-prompting.
- **Blender Python Engine**:
  - Generates standalone executable Blender automation scripts (`blender_*.py`).
  - Constructs 3D stages, camera dolly moves, cartoon sun lighting, and animated keyframed character planes.
  - Headless rendering execution via `blender -b -P script.py` when configured.

### 5. High-CTR 1280x720 Thumbnail Builder
- Generates 16:9 thumbnails (1280x720) optimized for preschool click-through rates.
- Multi-layered bubble typography with dual stroke outlines and 3D drop shadows.
- Callout badges: `"SING ALONG!"`, `"LEARN 1-2-3!"`, `"NEW!"`.
- Smart placement respecting YouTube's bottom-right video duration badge safe zone.

### 6. YouTube Data API v3 & COPPA Compliance
- OAuth 2.0 user authorization workflow with token refresh.
- Video upload with custom thumbnail and chapter timestamps.
- **COPPA Compliance**: Enforces `selfDeclaredMadeForKids = True` on all uploads.
- **Human-in-the-Loop Gate**: Hard rule preventing automated publishing without explicit human authorization.
- **Mock Sandbox Mode**: Realistic offline staging uploader for instant local testing without Google credentials.

### 7. Interactive Web Dashboard
- Powered by FastAPI, Tailwind CSS, and Jinja2 templates.
- **Overview**: KPI stat counters, approval queue, active jobs, and provider diagnostics.
- **Content Studio**: Interactive song planner and curriculum catalog.
- **Project Inspector**: Embedded 1080p HTML5 video player, thumbnail inspector, lyrics, and storyboard audio stems.
- **Character Studio**: Character roster, official color swatches, visual consistency prompts, and new character creator.
- **Production Queue**: Real-time worker status, progress bars, and retry controls.
- **API & Settings**: External service connection status.

---

## 🛠️ Architecture & System Design

```
TinyTots Tunes/
├── core/
│   ├── config.py              # Configuration & environment variables
│   ├── logger.py              # Centralized colored & file logging
│   ├── database.py            # SQLite database for projects, jobs, & characters
│   └── safety.py              # Copyright filter (disallows Disney, Peppa, Cocomelon, etc.)
├── planner/
│   ├── idea_generator.py      # Children's song themes, educational focus, catchy concepts
│   ├── lyric_writer.py        # Rhyming lyrics, verse-chorus structure, sound cues
│   ├── storyboarder.py        # Scene-by-scene timing, character actions, visual prompts
│   ├── metadata_gen.py        # SEO titles, kid-friendly descriptions, tags, thumbnail prompts
│   └── planner.py             # Planning orchestrator and workspace manager
├── characters/
│   ├── models.py              # Character definition schema (traits, palette, wardrobe)
│   ├── presets/               # Built-in original characters (Barnaby, Pip & Penny, etc.)
│   └── manager.py             # Character library CRUD & copyright validation
├── assets/
│   ├── base.py                # Abstract provider interfaces
│   ├── image_generator.py     # Multi-provider image generator (Pollinations, OpenAI, Mock)
│   ├── voice_generator.py     # Edge-TTS (free neural child/female voices), SAPI, OpenAI
│   ├── music_generator.py     # Catchy procedural nursery synth generator & API hooks
│   ├── sfx_manager.py         # Procedural and library SFX (pops, boings, chimes, cheers)
│   └── manager.py             # Asset generation orchestrator
├── video/
│   ├── ffmpeg_engine.py       # 1080p compositor: Ken Burns, character rigs, audio ducking
│   ├── blender_engine.py      # Blender Python automation script generator and headless renderer
│   ├── templates.py           # Animation styles (Nursery Classic, Dance Party, Lullaby, Learning)
│   └── subtitle_engine.py     # Word/phrase karaoke subtitles & animated text overlays
├── thumbnail/
│   └── generator.py           # 1280x720 thumbnail builder with cutout placement & bubble typography
├── youtube/
│   ├── uploader.py            # YouTube Data API v3 OAuth uploader (MadeForKids enforcement)
│   └── mock_uploader.py       # Offline / staging simulator
├── automation/
│   ├── queue_manager.py       # State machine job queue & retry logic
│   ├── worker.py              # Asynchronous / threaded background execution daemon
│   └── scheduler.py           # Timed batch and cron production scheduler
├── dashboard/
│   ├── app.py                 # FastAPI web application
│   ├── static/                # CSS, JS, audio/video player assets
│   └── templates/             # Jinja2 / HTML5 interactive dashboard pages
├── data/                      # SQLite DB, SFX, and character data
├── projects/                  # Per-project output directory (videos, assets, thumbnails)
├── tests/                     # Comprehensive test suite (18 unit & integration tests)
├── .env.example               # Template environment configuration
├── requirements.txt           # Python package dependencies
├── main.py                    # Unified CLI and application runner
└── run_mvp.py                 # Direct MVP demonstration script
```

---

## 🚀 Quickstart & Setup Guide

### Prerequisites
1. **Python 3.10+** (tested on Python 3.11).
2. **FFmpeg** installed on your system PATH (`ffmpeg -version`).

### Step 1: Clone & Install Dependencies
```bash
git clone <repo-url>
cd "TinyTots Tunes"
pip install -r requirements.txt
```

### Step 2: Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default settings work immediately out-of-the-box with zero paid API keys!

### Step 3: Run the End-to-End MVP Demonstration
Execute the MVP demonstration script:
```bash
python run_mvp.py
```
This performs an end-to-end production run:
1. Verifies the Copyright Safety Engine.
2. Plans an original song ("The Rainbow Paintbox Song" with Barnaby Bear).
3. Generates scene assets, vocal tracks, procedural nursery music track, and sound effects.
4. Composites the 1080p Full HD MP4 video with FFmpeg.
5. Renders the 1280x720 YouTube thumbnail.
6. Tests the human approval gate.
7. Publishes to the YouTube Data API pipeline (Mock/Staging or Live).

### Step 4: Launch the Web Dashboard
Start the FastAPI interactive dashboard:
```bash
python main.py dashboard
```
Open your browser at: **`http://localhost:8000`**

---

## 🔑 External Services & API Credentials Guide

| Service | Setting in `.env` | Required? | Description |
| :--- | :--- | :--- | :--- |
| **YouTube Data API v3** | `YOUTUBE_CLIENT_SECRETS_FILE`<br>`YOUTUBE_MOCK_MODE=False` | **Optional** (Enabled when publishing live) | Download `client_secrets.json` from [Google Cloud Console](https://console.cloud.google.com). Leave `YOUTUBE_MOCK_MODE=True` for offline testing. |
| **FFmpeg** | `FFMPEG_PATH="ffmpeg"` | **Mandatory** | System video compositor. Pre-installed in standard PATH or provide path to `ffmpeg.exe`. |
| **Blender** | `BLENDER_PATH=""` | **Optional** | Path to `blender.exe` if 3D headless rendering is desired. Blender scripts are always generated. |
| **Image Providers** | `IMAGE_PROVIDER` | **Optional** | Set to `mock` (free, 100% offline), `pollinations` (free AI), `openai` (DALL-E 3, requires `OPENAI_API_KEY`), or `stability` (requires `STABILITY_API_KEY`). |
| **Voice Providers** | `VOICE_PROVIDER` | **Optional** | Set to `windows_sapi` (free, instant offline speech), `edge_tts` (free neural voices), `openai` (`tts-1`), or `elevenlabs` (requires `ELEVENLABS_API_KEY`). |
| **Music Providers** | `MUSIC_PROVIDER` | **Optional** | Set to `procedural` (free, built-in multi-track nursery synth, zero API keys needed) or `suno` (requires `SUNO_API_KEY`). |

---

## 💻 CLI Commands Reference

TinyTots Tunes includes a unified CLI (`main.py`):

```bash
# 1. Start the Web Dashboard
python main.py dashboard

# 2. Produce a single video end-to-end via CLI
python main.py produce --topic "The Rainbow Paintbox Song" --character barnaby_bear --style nursery_classic

# 3. Produce and immediately auto-approve for publishing
python main.py produce --topic "Brush Your Teeth with Barnaby" --auto-approve

# 4. Run the background queue worker daemon
python main.py worker

# 5. List all registered original characters & color palettes
python main.py characters
```

---

## 🧪 Testing Suite

TinyTots Tunes comes with a complete suite of unit and integration tests covering safety filters, planning, character validation, asset generators, thumbnails, and YouTube approval gates:

```bash
pytest tests -v
```

All 18 tests pass with sub-second execution!

---

## 🛡️ Content Safety & COPPA Compliance

TinyTots Tunes adheres strictly to child safety and intellectual property guidelines:
- **Never copies copyrighted franchises**: Characters, lyrics, and prompts are scanned by `core/safety.py` to prevent trademark infringement.
- **COPPA Compliance**: Every YouTube video upload sets `selfDeclaredMadeForKids: True` to protect children's privacy.
- **Manual Review Gate**: Unapproved videos are blocked from publishing until human sign-off is granted via the Dashboard or CLI.

