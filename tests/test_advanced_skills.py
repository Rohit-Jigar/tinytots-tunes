import os
import pytest
from video.audio_postproduction import audio_postproduction
from video.remotion_engine import remotion_engine
from assets.omni_video_generator import omni_video_director

def test_remotion_composition_generation(tmp_path):
    project_data = {
        "title": "The Counting Penguins Song",
        "character_name": "Pip and Penny",
        "storyboard": [{"scene_number": 1, "end_time": 30.0}]
    }
    out_dir = str(tmp_path / "remotion_test")
    res = remotion_engine.generate_composition_files(project_data, out_dir)

    assert os.path.exists(os.path.join(out_dir, "package.json"))
    assert os.path.exists(os.path.join(out_dir, "Composition.tsx"))

    with open(os.path.join(out_dir, "Composition.tsx"), "r", encoding="utf-8") as f:
        content = f.read()
    assert "The Counting Penguins Song" in content
    assert "Pip and Penny" in content

def test_omni_video_stateful_chaining():
    # Scene 1: Animate Still
    res1 = omni_video_director.animate_image(
        image_path="scene_01.png",
        motion_prompt="Barnaby Bear waving playfully",
        camera_direction="slow_center_dolly_in"
    )
    int_id_1 = res1["interaction_id"]
    assert int_id_1.startswith("int_")
    assert res1["status"] == "COMPLETED"

    # Scene 2: Stateful Edit chained from Scene 1
    res2 = omni_video_director.edit_video(
        previous_interaction_id=int_id_1,
        edit_instruction="Barnaby hops up and down happily",
        camera_direction="pan_right"
    )
    assert res2["chained_from"] == int_id_1
    assert res2["interaction_id"].startswith("int_")
    assert res2["status"] == "COMPLETED"

def test_audio_postproduction_mastering(tmp_path):
    # Create simple WAV file
    import wave, numpy as np
    wav_in = str(tmp_path / "raw_voice.wav")
    sr = 44100
    t = np.linspace(0, 1.0, sr, False)
    data = (np.sin(2 * np.pi * 440 * t) * 16000).astype(np.int16)
    with wave.open(wav_in, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(data.tobytes())

    wav_out = str(tmp_path / "mastered_voice.m4a")
    res = audio_postproduction.master_vocal_track(wav_in, wav_out)
    assert os.path.exists(res)
    assert os.path.getsize(res) > 500
