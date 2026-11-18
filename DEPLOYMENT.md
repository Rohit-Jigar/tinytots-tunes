# 🚀 TinyTots Tunes: Production Deployment Guide

This guide details the complete production deployment architecture for the **TinyTots Tunes AI Preschool Video Factory**, featuring a **decoupled frontend hosted on GitHub Pages**, a **containerized backend on Render Cloud**, and an **automated GitHub Actions CI/CD pipeline**.

---

## 🏛️ System Architecture

```
                                +-------------------------------------------+
                                |               USER BROWSER                |
                                +-------------------------------------------+
                                                      |
                         +----------------------------+----------------------------+
                         |                                                         |
                         v                                                         v
         +-------------------------------+                         +-------------------------------+
         |    GITHUB PAGES FRONTEND      |                         |     RENDER BACKEND (DOCKER)   |
         |  https://<user>.github.io/... |                         |  https://tinytots-studio...   |
         +-------------------------------+                         +-------------------------------+
         | - Responsive Preschool SPA    |                         | - FastAPI 2.0 REST Engine     |
         | - Master 1080p Video Player   |  CORS JSON API Calls    | - Background Queue Worker     |
         | - 10-Point Broadcast QC View  | ----------------------> | - Procedural Music Engine     |
         | - 20-Song Curriculum Catalog  |                         | - FFmpeg Broadcast Render     |
         | - Character Universe Roster   |                         | - SQLite Job Database         |
         +-------------------------------+                         +-------------------------------+
                                                                                   ^
                                                                                   | Automated Deploy
                                 +--------------------------------+                |
                                 |   GITHUB ACTIONS CI/CD ENGINE   |----------------+
                                 | - Flake8 & Safety Audit        |
                                 | - Pytest Suite (32/32 tests)   |
                                 | - Docker Container Build Check |
                                 | - GitHub Pages Auto-Deploy     |
                                 +--------------------------------+
```

---

## 1. 🌐 Frontend Deployment (GitHub Pages)

The frontend is completely decoupled as a zero-dependency Single-Page Application located in the [`docs/`](./docs/index.html) directory.

### Automatic Deployment (via CI/CD)
The included GitHub Actions workflow (`.github/workflows/ci-cd.yml`) automatically builds and publishes the `docs/` folder to GitHub Pages whenever you push to `main`.

### Manual GitHub Pages Settings (One-Time Setup):
1. Navigate to your repository on GitHub: `https://github.com/Rohit-Jigar/tinytots-tunes`.
2. Click **Settings** (top navigation bar) -> **Pages** (left sidebar under "Code and automation").
3. Under **Build and deployment**:
   - **Source**: Select **GitHub Actions** (recommended for automated deployments) **OR** select **Deploy from a branch** -> branch `main` -> folder `/docs` -> click **Save**.
4. Your frontend will be live within 1–2 minutes at:
   `https://rohit-jigar.github.io/tinytots-tunes/`

---

## 2. ⚡ Backend Deployment (Render Cloud)

The backend is fully containerized with Debian-slim, FFmpeg, fonts, and Python 3.11, configured with health checks at `/api/health`.

### Option A: 1-Click Render Blueprint (Recommended)
1. Log into your Render account at [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** -> **Blueprint**.
3. Connect your GitHub repository (`Rohit-Jigar/tinytots-tunes`).
4. Render will automatically detect the [`render.yaml`](./render.yaml) configuration file:
   - **Service Name**: `tinytots-tunes-studio`
   - **Environment**: `docker`
   - **Plan**: `standard` (or `starter` / `free`)
   - **Health Check**: `/api/health`
5. Click **Apply**. Render will automatically build the Docker container and deploy the service.

### Option B: Manual Web Service Setup on Render
1. Click **New +** -> **Web Service**.
2. Select your repository `Rohit-Jigar/tinytots-tunes`.
3. Choose **Docker** as the Runtime environment.
4. Set the **Health Check Path** to `/api/health`.
5. Add the following Environment Variables under the **Environment** tab:
   - `PORT`: `8000`
   - `APP_ENV`: `production`
   - `IMAGE_PROVIDER`: `mock` (or `pollinations` / `replicate`)
   - `VOICE_PROVIDER`: `edge_tts`
   - `MUSIC_PROVIDER`: `procedural`
   - `YOUTUBE_MOCK_MODE`: `true`
   - `VIDEO_WIDTH`: `1920`
   - `VIDEO_HEIGHT`: `1080`
   - `VIDEO_FPS`: `30`
6. Click **Create Web Service**. Your service URL will be something like:
   `https://tinytots-tunes-studio.onrender.com`

---

## 3. 🔗 Connecting Frontend & Backend

Once your Render backend is deployed:
1. Open your live frontend portal on GitHub Pages:
   `https://rohit-jigar.github.io/tinytots-tunes/`
2. In the top right corner of the header, enter your Render URL into the **Backend API URL** input box:
   `https://tinytots-tunes-studio.onrender.com`
3. Click **Connect**.
4. The status indicator will turn green (`CONNECTED`), and the live 20-Song Curriculum, Pilot Videos, and Character Universe will stream directly from Render.

---

## 4. 🔄 CI/CD Pipeline Automation

The `.github/workflows/ci-cd.yml` pipeline runs on every push and pull request to `main`:

| Stage | Action | Criteria |
| :--- | :--- | :--- |
| **1. Lint & Safety** | Flake8 syntax audit + Character Copyright Verification | Zero syntax errors & zero trademark breaches |
| **2. Test Suite** | 32 automated unit and integration tests with FFmpeg | 100% test pass rate (32/32) |
| **3. Docker Validation** | Full Docker Buildx image creation and `/api/health` test | Clean build with working container health check |
| **4. Frontend Deploy** | Publishes `docs/` to GitHub Pages via official Actions | Automatic live deployment |
| **5. Render Webhook** | Triggers Render build hook (optional secret: `RENDER_DEPLOY_HOOK_URL`) | Automatic backend rollout |

### Adding the Render Deploy Hook Secret (Optional)
To trigger automated Render deployments via the pipeline:
1. In Render, go to your Web Service **Settings** -> scroll down to **Deploy Hook**.
2. Copy the Deploy Hook URL.
3. In GitHub, go to **Settings** -> **Secrets and variables** -> **Actions**.
4. Click **New repository secret**, name it `RENDER_DEPLOY_HOOK_URL`, paste the URL, and click **Add secret**.
