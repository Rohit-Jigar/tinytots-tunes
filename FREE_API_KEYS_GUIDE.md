# 🎁 Free API Keys & Resources Guide for Modern 3D Video Production

This comprehensive guide shows you **where and how to obtain 100% free API keys, free monthly tiers, and developer credits** to produce modern, trending, 3D preschool videos (like Cocomelon and Super Simple Songs) with TinyTots Tunes **at zero cost**.

---

## ⚡ Quick Reference: Free Tiers & Providers

| Capability | Free Service / Provider | Free Allowance | How to Get It | TinyTots `.env` Setting |
| :--- | :--- | :--- | :--- | :--- |
| **3D Cartoon Images** | **Pollinations AI** | **100% Free & Unlimited** (No key required) | Built-in! Uses Flux / SDXL | `IMAGE_PROVIDER="pollinations"` |
| **3D Cartoon Images** | **Hugging Face** | **100% Free** (Free Inference API) | [huggingface.co](https://huggingface.co/settings/tokens) | `HUGGINGFACE_API_TOKEN="..."` |
| **3D Keyframes & Video** | **Fal.ai** | **$10–$25 Free Credits** on signup | [fal.ai](https://fal.ai/dashboard/keys) | `FAL_KEY="..."` |
| **3D Video & Motion** | **Replicate** | **Free Trial Runs** on GitHub login | [replicate.com](https://replicate.com/account/api-tokens) | `REPLICATE_API_TOKEN="..."` |
| **Preschool Singing & Music** | **Suno AI** | **50 Free Credits Every Day** (~5 songs/day) | [suno.com](https://suno.com) | `SUNO_API_KEY="..."` |
| **Natural Child Voices** | **Microsoft Edge-TTS** | **100% Free & Unlimited** (No key required) | Built-in! (`en-US-AnaNeural`) | `VOICE_PROVIDER="edge_tts"` |
| **Human Voice Acting** | **ElevenLabs** | **10,000 characters/month Free** forever | [elevenlabs.io](https://elevenlabs.io) | `ELEVENLABS_API_KEY="..."` |
| **Fast AI Storyboarder** | **Groq Cloud** | **100% Free** (Llama 3 70B, 30 req/min) | [console.groq.com](https://console.groq.com/keys) | `GROQ_API_KEY="..."` |
| **Smart AI Lyrics** | **Google Gemini API** | **15 requests/min Free** (1,500/day) | [aistudio.google.com](https://aistudio.google.com/) | `GEMINI_API_KEY="..."` |
| **YouTube Publishing** | **Google Cloud Console** | **10,000 free quota units/day** | [console.cloud.google.com](https://console.cloud.google.com) | `client_secrets.json` |

---

## 1. 🎨 3D Cartoon Visuals & AI Video (Free Options)

### Option A: Pollinations AI (100% Free, Zero Setup)
* **Cost**: $0.00 / Free forever. No account, credit card, or API key needed.
* **Models**: Flux.1, Stable Diffusion XL.
* **How to use in TinyTots Tunes**:
  ```env
  IMAGE_PROVIDER="pollinations"
  ```
  *(Already configured by default in your `.env`!)*

### Option B: Hugging Face Inference API (100% Free API Key)
* **Cost**: Free unlimited personal inference token.
* **Models**: `black-forest-labs/FLUX.1-schnell` (super fast, high-definition 3D cartoon style).
* **How to get your free key**:
  1. Go to [huggingface.co/join](https://huggingface.co/join) and create a free account.
  2. Navigate to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
  3. Click **Create new token**, name it `tinytots`, select Role: **Read**, and click **Create token**.
  4. Copy the token (starts with `hf_...`).
* **Add to `.env`**:
  ```env
  HUGGINGFACE_API_TOKEN="hf_your_token_here"
  ```

### Option C: Replicate (Free Trial Credits with GitHub)
* **Cost**: Free trial compute upon logging in with your GitHub account.
* **Models**: Flux 1.1 Pro, Minimax Video-01, Kling AI, Luma Ray 2.
* **How to get your key**:
  1. Go to [replicate.com](https://replicate.com) and click **Sign in with GitHub** (uses your `Rohit-Jigar` account).
  2. Go to [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens).
  3. Copy your API token (starts with `r8_...`).
* **Add to `.env`**:
  ```env
  REPLICATE_API_TOKEN="r8_your_token_here"
  IMAGE_PROVIDER="replicate"
  ```

### Option D: Fal.ai ($10–$25 Free Developer Credits)
* **Cost**: Free credits on first sign in.
* **Models**: Flux.1 Dev, Minimax 3D video, Fast SDXL.
* **How to get your key**:
  1. Visit [fal.ai](https://fal.ai) and sign up with GitHub or Google.
  2. Navigate to [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys).
  3. Click **Create Key** and copy it.
* **Add to `.env`**:
  ```env
  FAL_KEY="your_fal_key_here"
  ```

---

## 2. 🎵 Nursery Rhymes & AI Singing Vocals (Free Options)

### Option A: Suno AI (50 Free Credits Every Day)
* **Why it's essential**: Suno takes lyrics and generates **full songs with melodic singing voices** (cheerful female singer, preschool chorus, acoustic guitar, upbeat drums) rather than flat robotic speech.
* **Free allowance**: 50 credits refreshed **daily** (~5 full songs every day for free).
* **How to access**:
  1. Go to [suno.com](https://suno.com) and click **Sign Up** (Discord, Google, or Microsoft).
  2. You can create songs directly on the web app for free using our lyrics from `output/video_01/lyrics.txt` or `output/video_02/lyrics.txt`.
  3. For API access, you can obtain a free API trial key via [GoAPI / Chirp API](https://goapi.ai) or use the open-source Suno API wrapper.
* **Add to `.env`**:
  ```env
  SUNO_API_KEY="your_suno_key"
  MUSIC_PROVIDER="suno"
  ```

### Option B: Udio AI (Free Daily Generations)
* **Free allowance**: 10 free generations per day.
* **How to get it**:
  1. Visit [udio.com](https://udio.com) and create a free account.
  2. Use custom lyrics from the 20-Song Curriculum (`planner/catalog_20.py`).
  3. Set tags: `nursery rhyme, preschool, cheerful female vocals, acoustic pop, 120 bpm`.

---

## 3. 🎙️ Natural Human Speech & Character Voices (Free Options)

### Option A: Microsoft Edge-TTS (100% Free, No Key Required!)
* **Why it's great**: Microsoft Edge Neural TTS gives you **crystal-clear, friendly children's voices** (`en-US-AnaNeural`) completely free with **zero API limits and zero cost**.
* **How to use**:
  ```env
  VOICE_PROVIDER="edge_tts"
  DEFAULT_VOICE_NAME="en-US-AnaNeural"
  ```
  *(Already integrated into TinyTots Tunes!)*

### Option B: ElevenLabs (10,000 Characters/Month Free Forever)
* **Why it's great**: The world's #1 hyper-realistic voice generator. Sounds like a real human preschool teacher or cartoon character.
* **Free allowance**: 10,000 characters free every month.
* **How to get your free key**:
  1. Go to [elevenlabs.io](https://elevenlabs.io) and click **Sign Up Free**.
  2. Click on your profile icon (bottom-left) -> **API Keys**.
  3. Click **Create API Key**, name it `tinytots`, and copy it (`sk_...`).
  4. Select a pre-made friendly voice (e.g. `Freya`, `Giggle`, `Rachel`) and copy its Voice ID.
* **Add to `.env`**:
  ```env
  ELEVENLABS_API_KEY="sk_your_key_here"
  ELEVENLABS_VOICE_ID="21m00Tcm4TlvDq8ikWAM"
  VOICE_PROVIDER="elevenlabs"
  ```

### Option C: Google Cloud Text-to-Speech (4 Million Characters Free / Month)
* **Free allowance**: 4,000,000 characters free every month on WaveNet/Neural2 voices.
* **How to get it**:
  1. Visit [console.cloud.google.com](https://console.cloud.google.com).
  2. Enable the **Cloud Text-to-Speech API**.
  3. Generate an API Key under **APIs & Services > Credentials**.

---

## 4. 🧠 Storyboard & Lyric Generation (Free LLM Keys)

### Option A: Groq Cloud (100% Free, Ultra-Fast Llama 3 70B)
* **Why it's great**: Generates 12-scene preschool storyboards and rhyming lyrics in under 1 second. Free tier gives 30 requests/minute and 14,400 requests/day!
* **How to get your free key**:
  1. Visit [console.groq.com/keys](https://console.groq.com/keys).
  2. Sign in with GitHub or Google.
  3. Click **Create API Key**, name it `tinytots`, and copy it (`gsk_...`).
* **Add to `.env`**:
  ```env
  GROQ_API_KEY="gsk_your_groq_key"
  ```

### Option B: Google Gemini API (1,500 Free Requests / Day)
* **Why it's great**: High quality, huge context window, understands preschool visual styles.
* **How to get your free key**:
  1. Go to [aistudio.google.com](https://aistudio.google.com/).
  2. Click **Get API key** -> **Create API key in new project**.
  3. Copy the key (`AIzaSy...`).
* **Add to `.env`**:
  ```env
  GEMINI_API_KEY="AIzaSy_your_gemini_key"
  ```

---

## 5. 📺 YouTube Data API v3 (100% Free Official Key)

* **Free quota**: 10,000 quota units per day free forever (enough to upload ~6 Full HD videos per day automatically).
* **How to get your credentials**:
  1. Go to [console.cloud.google.com](https://console.cloud.google.com) and create a project called `TinyTots Tunes`.
  2. In the top search bar, search for **YouTube Data API v3** and click **Enable**.
  3. Go to **APIs & Services > OAuth consent screen**:
     - User Type: **External**.
     - App Name: `TinyTots Tunes Studio`.
     - Add your Gmail as a **Test User**.
  4. Go to **APIs & Services > Credentials**:
     - Click **+ Create Credentials** -> **OAuth client ID**.
     - Application type: **Desktop app**.
     - Name: `TinyTots Uploader`.
  5. Click **Download JSON** and save it in your project root as `client_secrets.json`.

---

## 6. 🚀 Recommended Free Starter Setup

To get modern 3D Cocomelon-grade visuals and singing vocals without spending a penny, use this configuration:

```env
# In your .env or Render Dashboard:

# 1. 3D Cartoon Visuals (Free & Instant)
IMAGE_PROVIDER="pollinations"

# 2. Preschool Singing Vocals (Free Neural Child Voice)
VOICE_PROVIDER="edge_tts"
DEFAULT_VOICE_NAME="en-US-AnaNeural"

# 3. Audio & Music
MUSIC_PROVIDER="procedural"

# 4. Optional Free Upgrade Keys (Add whenever you create them)
ELEVENLABS_API_KEY=""       # Free 10,000 chars from elevenlabs.io
REPLICATE_API_TOKEN=""      # Free trial from replicate.com
GROQ_API_KEY=""             # 100% free from console.groq.com
```

Whenever you paste any of these keys into [.env](file:///d:/TinyTots%20Tunes/.env) (or in your Render Dashboard Environment Variables), TinyTots Tunes will automatically detect them and elevate your output quality to modern 3D standards!
