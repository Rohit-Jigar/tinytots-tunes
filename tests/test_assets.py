import os
import pytest
from assets.music_generator import ProceduralMusicProvider
from assets.image_generator import MockImageProvider
from assets.voice_generator import WindowsSAPIVoiceProvider

def test_procedural_music_generator(tmp_path):
    music_file = str(tmp_path / "test_music.wav")
    provider = ProceduralMusicProvider()
    out = provider.generate_music("happy toddler song", 3.0, music_file)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 10000

def test_mock_image_generator(tmp_path):
    img_file = str(tmp_path / "test_img.png")
    provider = MockImageProvider()
    out = provider.generate_image("preschool bear", img_file, width=640, height=360)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 5000

def test_windows_sapi_voice(tmp_path):
    vox_file = str(tmp_path / "test_vox.wav")
    provider = WindowsSAPIVoiceProvider()
    out = provider.synthesize_speech("Hello preschool friends!", vox_file)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 1000

