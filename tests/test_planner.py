import pytest
from planner.idea_generator import IdeaGenerator
from planner.lyric_writer import LyricWriter
from planner.storyboarder import Storyboarder
from planner.metadata_gen import MetadataGenerator
from characters.manager import character_manager

def test_idea_generation():
    idea = IdeaGenerator.generate_idea(category="Colors & Creativity")
    assert idea is not None
    assert "title" in idea
    assert "target_age" in idea
    assert len(idea["educational_goals"]) > 0

def test_lyric_writer():
    char = character_manager.get_character("barnaby_bear")
    idea = {"title": "The Rainbow Paintbox Song", "category": "Colors & Creativity"}
    lyrics = LyricWriter.write_lyrics(idea, char)
    assert lyrics is not None
    assert len(lyrics["sections"]) >= 4
    assert "full_lyrics_text" in lyrics
    assert "Barnaby Bear" in lyrics["full_lyrics_text"]

def test_storyboarder():
    char = character_manager.get_character("barnaby_bear")
    idea = {"title": "The Rainbow Paintbox Song", "category": "Colors & Creativity"}
    lyrics = LyricWriter.write_lyrics(idea, char)
    storyboard = Storyboarder.create_storyboard(lyrics, char)
    assert len(storyboard) > 0
    assert storyboard[0]["scene_number"] == 1
    assert "visual_prompt" in storyboard[0]
    assert "duration" in storyboard[0]

def test_metadata_generator():
    char = character_manager.get_character("barnaby_bear")
    idea = {"title": "The Rainbow Paintbox Song", "category": "Colors & Creativity"}
    lyrics = LyricWriter.write_lyrics(idea, char)
    storyboard = Storyboarder.create_storyboard(lyrics, char)
    metadata = MetadataGenerator.generate_metadata(idea, lyrics, storyboard, char)

    assert "title" in metadata
    assert len(metadata["title"]) > 0
    assert metadata["made_for_kids"] is True
    assert len(metadata["tags"]) >= 10
    assert "thumbnail_prompt" in metadata

