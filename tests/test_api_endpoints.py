import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from dashboard.app import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_api_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "2.0.0"
    assert "ffmpeg" in data

def test_api_catalog(client):
    response = client.get("/api/catalog")
    assert response.status_code == 200
    data = response.json()
    assert "catalog" in data
    assert data["total"] == 20
    assert len(data["catalog"]) == 20
    assert data["catalog"][0]["title"] == "The Dancing Dinosaur Song"

def test_api_pilots(client):
    response = client.get("/api/pilots")
    assert response.status_code == 200
    data = response.json()
    assert "pilots" in data
    assert len(data["pilots"]) == 2
    p1 = next((p for p in data["pilots"] if p["id"] == "video_01"), None)
    assert p1 is not None
    assert p1["number"] == 1

def test_api_characters(client):
    response = client.get("/api/characters")
    assert response.status_code == 200
    data = response.json()
    assert "characters" in data
    assert data["total"] == 5
    names = [c["name"] for c in data["characters"]]
    assert "Barnaby Bear" in names
    assert any("Pip" in n for n in names)
    assert "Sunny" in names

def test_api_system_status(client):
    response = client.get("/api/system/status")
    assert response.status_code == 200
    data = response.json()
    assert "ffmpeg" in data
    assert "image_provider" in data

def test_api_queue(client):
    response = client.get("/api/queue")
    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data

def test_cors_headers_present(client):
    response = client.get("/api/health", headers={"Origin": "https://rohit-jigar.github.io"})
    assert response.status_code == 200
    # In FastAPI/Starlette, with allow_origins=["*"] and allow_credentials=True,
    # the matching origin is echoed back in Access-Control-Allow-Origin
    assert response.headers.get("access-control-allow-origin") in ("*", "https://rohit-jigar.github.io")

def test_api_produce_endpoint_json(client):
    with patch("automation.pilot_producer.pilot_producer.produce_catalog_video") as mock_produce:
        response = client.post("/api/catalog/produce/3", headers={"Accept": "application/json"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "queued"
        assert data["song_number"] == 3
