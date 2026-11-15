import os
import pytest
from youtube.uploader import youtube_uploader, YouTubePublishError
from youtube.mock_uploader import mock_youtube

def test_mock_uploader_execution(tmp_path):
    dummy_video = str(tmp_path / "dummy.mp4")
    with open(dummy_video, "w") as f:
        f.write("dummy video data")

    res = mock_youtube.upload_video(
        video_path=dummy_video,
        title="Test Nursery Song",
        description="Preschool song description",
        tags=["kids", "preschool"],
        made_for_kids=True
    )

    assert res["id"].startswith("mock_")
    assert "https://youtu.be/" in res["url"]
    assert res["status"]["selfDeclaredMadeForKids"] is True

def test_unapproved_project_blocked():
    unapproved_project = {
        "project_id": "test_unapproved",
        "status": "PENDING_APPROVAL",
        "paths": {"final_video": "dummy.mp4"},
        "metadata": {"title": "Test", "description": "Test", "tags": []}
    }

    with pytest.raises(YouTubePublishError):
        youtube_uploader.upload_project(unapproved_project, bypass_approval_check=False)

