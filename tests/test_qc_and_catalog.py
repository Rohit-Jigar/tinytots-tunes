import pytest
from planner.catalog_20 import catalog_manager, SONG_CATALOG_20
from core.quality_control import quality_inspector
from core.safety import SafetyChecker

def test_curriculum_catalog_20_complete():
    catalog = catalog_manager.get_catalog()
    assert len(catalog) == 20
    # Verify song numbers 1 through 20
    numbers = [s["number"] for s in catalog]
    assert numbers == list(range(1, 21))

    # Verify each song has required preschool structure
    for song in catalog:
        assert song["title"]
        assert song["category"]
        assert song["lead_character_id"]
        assert len(song["educational_goals"]) >= 2
        assert song["bpm"] >= 75
        assert len(song["sections"]) >= 4

        # Safety check all titles and hooks
        safe_title, _ = SafetyChecker.check_text(song["title"])
        assert safe_title, f"Song title '{song['title']}' must be 100% original"
        safe_hook, _ = SafetyChecker.check_text(song["hook"])
        assert safe_hook, f"Song hook '{song['hook']}' must be 100% original"

def test_catalog_query_by_id_and_title():
    s1 = catalog_manager.get_song_by_number(1)
    assert s1["title"] == "The Dancing Dinosaur Song"
    assert s1["lead_character_id"] == "barnaby_bear"

    s2 = catalog_manager.get_song_by_number(2)
    assert s2["title"] == "ABC Phonics Adventure"
    assert s2["lead_character_id"] == "pip_bird"

    lookup = catalog_manager.get_song_by_title("Dancing Dinosaur")
    assert lookup is not None
    assert lookup["number"] == 1

def test_quality_control_checks_fail_on_missing_file():
    report = quality_inspector.inspect_package(
        video_path="non_existent_video.mp4",
        thumbnail_path=None
    )
    assert report["status"] == "NEEDS_ATTENTION"
    assert not report["all_passed"]
    assert report["inspections"]["1_container_integrity"]["pass"] is False
