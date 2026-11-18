import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from core.config import config
from core.logger import logger
from core.database import db
from core.safety import SafetyChecker, CopyrightSafetyError
from characters.models import Character
from characters.manager import character_manager
from planner.idea_generator import IdeaGenerator, PRESCHOOL_CURRICULUM
from planner.planner import content_planner
from planner.catalog_20 import catalog_manager
from automation.queue_manager import queue_manager
from automation.worker import worker
from fastapi.middleware.cors import CORSMiddleware
from youtube.uploader import youtube_uploader

app = FastAPI(
    title="TinyTots Tunes Video Factory API",
    version="2.0.0",
    description="Production-grade AI Preschool Animation & Music Studio Backend"
)

# Enable Cross-Origin Resource Sharing (CORS) for GitHub Pages & distributed clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files and Projects Media Directory
templates_dir = Path(__file__).parent / "templates"
static_dir = Path(__file__).parent / "static"
output_dir = config.BASE_DIR / "output"
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
app.mount("/media", StaticFiles(directory=str(config.PROJECTS_DIR)), name="media")
app.mount("/output", StaticFiles(directory=str(output_dir)), name="output")

templates = Jinja2Templates(directory=str(templates_dir))

# Start background worker when app starts
@app.on_event("startup")
def startup_event():
    logger.info("Initializing TinyTots Tunes Web Dashboard & Worker...")
    worker.start()

@app.on_event("shutdown")
def shutdown_event():
    worker.stop()

# Helper: System Status Check
def get_system_status() -> Dict[str, Any]:
    import subprocess
    # FFmpeg check
    ffmpeg_ok = False
    try:
        r = subprocess.run([config.FFMPEG_PATH, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ffmpeg_ok = (r.returncode == 0)
    except Exception:
        pass

    # Blender check
    blender_ok = bool(config.BLENDER_PATH and os.path.exists(config.BLENDER_PATH))

    return {
        "ffmpeg": {"installed": ffmpeg_ok, "path": config.FFMPEG_PATH},
        "blender": {"installed": blender_ok, "path": config.BLENDER_PATH or "Not configured (Using FFmpeg Compositor)"},
        "image_provider": config.IMAGE_PROVIDER,
        "voice_provider": config.VOICE_PROVIDER,
        "music_provider": config.MUSIC_PROVIDER,
        "youtube": {"mock_mode": config.YOUTUBE_MOCK_MODE, "secrets_present": (config.BASE_DIR / config.YOUTUBE_CLIENT_SECRETS_FILE).exists()}
    }

# ----------------------------------------------------
# HTML Page Routes
# ----------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def dashboard_overview(request: Request):
    projects = db.list_projects()
    jobs = db.list_jobs(limit=15)
    chars = character_manager.list_characters()

    # Compute Statistics
    stats = {
        "total_projects": len(projects),
        "in_production": sum(1 for p in projects if p["status"] in ("PLANNED", "ASSETS_READY")),
        "pending_approval": sum(1 for p in projects if p["status"] == "PENDING_APPROVAL"),
        "published": sum(1 for p in projects if p["status"] == "PUBLISHED"),
        "failed_jobs": sum(1 for j in jobs if j["status"] == "FAILED")
    }

    approval_queue = [p for p in projects if p["status"] == "PENDING_APPROVAL"]

    return templates.TemplateResponse(request=request, name="index.html", context={
        "stats": stats,
        "approval_queue": approval_queue,
        "recent_projects": projects[:8],
        "recent_jobs": jobs,
        "characters": chars,
        "system_status": get_system_status()
    })

@app.get("/ideas", response_class=HTMLResponse)
async def ideas_studio(request: Request):
    categories = IdeaGenerator.list_curriculum_categories()
    chars = character_manager.list_characters()
    curriculum = PRESCHOOL_CURRICULUM
    return templates.TemplateResponse(request=request, name="ideas.html", context={
        "categories": categories,
        "characters": chars,
        "curriculum": curriculum
    })

@app.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str):
    record = db.get_project(project_id)
    if not record:
        raise HTTPException(status_code=404, detail="Project not found")

    p_data = record["data"]
    # Check if files exist on disk
    final_video_exists = os.path.exists(p_data["paths"].get("final_video", ""))
    thumb_exists = os.path.exists(p_data["paths"].get("thumbnail_file", ""))

    return templates.TemplateResponse(request=request, name="project_detail.html", context={
        "project": p_data,
        "final_video_exists": final_video_exists,
        "thumb_exists": thumb_exists
    })

@app.get("/characters", response_class=HTMLResponse)
async def character_library(request: Request):
    chars = character_manager.list_characters()
    return templates.TemplateResponse(request=request, name="characters.html", context={
        "characters": chars
    })

@app.get("/queue", response_class=HTMLResponse)
async def queue_view(request: Request):
    jobs = db.list_jobs(limit=50)
    return templates.TemplateResponse(request=request, name="queue.html", context={
        "jobs": jobs
    })

@app.get("/catalog", response_class=HTMLResponse)
async def catalog_view(request: Request):
    catalog = catalog_manager.get_catalog()
    catalog_display = []
    for s in catalog:
        song_id = s["id"]
        v_path = config.BASE_DIR / "output" / song_id / "final_video.mp4"
        r_path = config.BASE_DIR / "output" / song_id / "production_report.json"
        produced = v_path.exists()
        qc_score = 0.0
        if r_path.exists():
            try:
                import json
                with open(r_path, "r", encoding="utf-8") as rf:
                    qc_score = json.load(rf).get("overall_score", 0.0)
            except Exception:
                pass
        char = character_manager.get_character(s.get("lead_character_id"))
        catalog_display.append({
            **s,
            "produced": produced,
            "qc_score": qc_score,
            "lead_character_name": char.name if char else s.get("lead_character_id")
        })
    return templates.TemplateResponse(request=request, name="catalog.html", context={
        "catalog": catalog_display
    })

@app.get("/pilots", response_class=HTMLResponse)
async def pilots_view(request: Request, active: Optional[str] = "video_01"):
    import json
    pilot_ids = ["video_01", "video_02"]
    pilot_list = []
    active_data = None

    for pid in pilot_ids:
        song_num = int(pid.replace("video_", ""))
        song_info = catalog_manager.get_song_by_number(song_num)
        v_path = config.BASE_DIR / "output" / pid / "final_video.mp4"
        r_path = config.BASE_DIR / "output" / pid / "production_report.json"
        l_path = config.BASE_DIR / "output" / pid / "lyrics.txt"
        ready = v_path.exists() and r_path.exists()

        report_data = {}
        lyrics_text = ""
        if ready:
            try:
                with open(r_path, "r", encoding="utf-8") as rf:
                    report_data = json.load(rf)
                with open(l_path, "r", encoding="utf-8") as lf:
                    lyrics_text = lf.read()
            except Exception:
                pass

        char = character_manager.get_character(song_info.get("lead_character_id")) if song_info else None
        p_item = {
            "id": pid,
            "number": song_num,
            "title": song_info["title"] if song_info else pid.upper(),
            "badge": "🦖 Pilot 01" if pid == "video_01" else "🔤 Pilot 02",
            "character": char.name if char else "Barnaby Bear",
            "ready": ready,
            "report": report_data,
            "lyrics": lyrics_text
        }
        pilot_list.append(p_item)
        if pid == active or (active_data is None and ready):
            active_data = p_item

    if not active_data:
        active_data = pilot_list[0]

    return templates.TemplateResponse(request=request, name="pilots.html", context={
        "pilots": pilot_list,
        "active_pilot": active_data
    })

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "app": "TinyTots Tunes Studio",
        "version": "2.0.0",
        "environment": os.getenv("APP_ENV", "production"),
        "ffmpeg": get_system_status()["ffmpeg"]["installed"]
    }

@app.get("/api/catalog")
async def api_catalog():
    """Returns official 20-song curriculum catalog as JSON."""
    catalog = catalog_manager.get_catalog()
    catalog_display = []
    for s in catalog:
        song_id = s["id"]
        v_path = config.BASE_DIR / "output" / song_id / "final_video.mp4"
        r_path = config.BASE_DIR / "output" / song_id / "production_report.json"
        produced = v_path.exists()
        qc_score = 0.0
        if r_path.exists():
            try:
                import json
                with open(r_path, "r", encoding="utf-8") as rf:
                    qc_score = json.load(rf).get("overall_score", 0.0)
            except Exception:
                pass
        char = character_manager.get_character(s.get("lead_character_id"))
        catalog_display.append({
            **s,
            "produced": produced,
            "qc_score": qc_score,
            "lead_character_name": char.name if char else s.get("lead_character_id"),
            "video_url": f"/output/{song_id}/final_video.mp4" if produced else None,
            "thumbnail_url": f"/output/{song_id}/thumbnail.png" if (config.BASE_DIR / "output" / song_id / "thumbnail.png").exists() else None
        })
    return {"catalog": catalog_display, "total": len(catalog_display)}

@app.get("/api/pilots")
async def api_pilots():
    """Returns pilot deliverables, inspection scorecards, and media URLs as JSON."""
    import json
    pilot_ids = ["video_01", "video_02"]
    pilot_list = []

    for pid in pilot_ids:
        song_num = int(pid.replace("video_", ""))
        song_info = catalog_manager.get_song_by_number(song_num)
        v_path = config.BASE_DIR / "output" / pid / "final_video.mp4"
        r_path = config.BASE_DIR / "output" / pid / "production_report.json"
        l_path = config.BASE_DIR / "output" / pid / "lyrics.txt"
        t_path = config.BASE_DIR / "output" / pid / "thumbnail.png"
        ready = v_path.exists() and r_path.exists()

        report_data = {}
        lyrics_text = ""
        if ready:
            try:
                with open(r_path, "r", encoding="utf-8") as rf:
                    report_data = json.load(rf)
                with open(l_path, "r", encoding="utf-8") as lf:
                    lyrics_text = lf.read()
            except Exception:
                pass

        char = character_manager.get_character(song_info.get("lead_character_id")) if song_info else None
        pilot_list.append({
            "id": pid,
            "number": song_num,
            "title": song_info["title"] if song_info else pid.upper(),
            "badge": "🦖 Pilot 01" if pid == "video_01" else "🔤 Pilot 02",
            "character": char.name if char else "Barnaby Bear",
            "ready": ready,
            "video_url": f"/output/{pid}/final_video.mp4" if ready else None,
            "thumbnail_url": f"/output/{pid}/thumbnail.png" if t_path.exists() else None,
            "subtitles_url": f"/output/{pid}/subtitles.srt" if ready else None,
            "report": report_data,
            "lyrics": lyrics_text
        })
    return {"pilots": pilot_list}

@app.get("/api/characters")
async def api_characters():
    """Returns registered characters roster as JSON."""
    chars = character_manager.list_characters()
    return {
        "characters": [c.model_dump() if hasattr(c, "model_dump") else c.dict() for c in chars],
        "total": len(chars)
    }

@app.get("/api/system/status")
async def api_system_status():
    """Returns system status and engines availability as JSON."""
    return get_system_status()

@app.get("/api/queue")
async def api_queue():
    """Returns active and recent background production jobs as JSON."""
    jobs = db.list_jobs(limit=50)
    return {"jobs": jobs}

@app.get("/settings", response_class=HTMLResponse)
async def settings_view(request: Request):
    return templates.TemplateResponse(request=request, name="settings.html", context={
        "config": config,
        "system_status": get_system_status()
    })

# ----------------------------------------------------
# Action & API Endpoints
# ----------------------------------------------------

@app.post("/api/catalog/produce/{song_number}")
async def produce_catalog_endpoint(song_number: int, background_tasks: BackgroundTasks, request: Request):
    from automation.pilot_producer import pilot_producer
    background_tasks.add_task(pilot_producer.produce_catalog_video, song_number)
    accept = request.headers.get("accept", "")
    if "application/json" in accept or "json" in accept:
        return JSONResponse({"status": "queued", "song_number": song_number, "message": f"Production queued for song #{song_number:02d}"})
    return RedirectResponse(url="/pilots" if song_number in (1, 2) else "/catalog", status_code=303)

@app.post("/api/projects/plan")
async def plan_new_project(
    topic: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    character_id: Optional[str] = Form(None),
    auto_produce: bool = Form(False)
):
    try:
        project = content_planner.plan_project(
            topic=topic if topic and topic.strip() else None,
            category=category,
            character_id=character_id
        )
        if auto_produce:
            queue_manager.create_job(project["project_id"])
        return RedirectResponse(url=f"/projects/{project['project_id']}", status_code=303)
    except CopyrightSafetyError as ce:
        return JSONResponse(status_code=400, content={"error": str(ce)})
    except Exception as e:
        logger.error("Error creating project: %s", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/projects/{project_id}/produce")
async def start_production(project_id: str):
    job = queue_manager.create_job(project_id)
    return RedirectResponse(url=f"/queue", status_code=303)

@app.post("/api/projects/{project_id}/approve")
async def approve_project(project_id: str):
    success = queue_manager.approve_project(project_id)
    if not success:
        raise HTTPException(status_code=400, detail="Could not approve project")
    return RedirectResponse(url=f"/projects/{project_id}", status_code=303)

@app.post("/api/projects/{project_id}/reject")
async def reject_project(project_id: str, reason: str = Form("Needs adjustments")):
    queue_manager.reject_project(project_id, reason)
    return RedirectResponse(url=f"/projects/{project_id}", status_code=303)

@app.post("/api/jobs/{job_id}/retry")
async def retry_job(job_id: str):
    success = queue_manager.retry_job(job_id)
    return RedirectResponse(url="/queue", status_code=303)

@app.post("/api/characters/create")
async def create_new_character(
    char_id: str = Form(...),
    name: str = Form(...),
    species: str = Form(...),
    clothing: str = Form(...),
    features: str = Form(...),
    personality: str = Form(...),
    palette: str = Form(...),
    visual_prompt: str = Form(...)
):
    try:
        color_list = [c.strip() for c in palette.split(",") if c.strip()]
        new_char = Character(
            id=char_id.strip().lower().replace(" ", "_"),
            name=name.strip(),
            species=species.strip(),
            color_palette=color_list,
            clothing=clothing.strip(),
            distinctive_features=features.strip(),
            personality=personality.strip(),
            visual_prompt=visual_prompt.strip()
        )
        character_manager.save_character(new_char)
        return RedirectResponse(url="/characters", status_code=303)
    except CopyrightSafetyError as ce:
        return JSONResponse(status_code=400, content={"error": str(ce)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

