import os
from pathlib import Path
from typing import List, Dict, Any

class SubtitleEngine:
    """
    Generates standard SRT and Advanced SubStation Alpha (.ass) subtitle files
    optimized for preschool sing-alongs (large colorful fonts, dark outline for readability).
    """

    @classmethod
    def format_srt_time(cls, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @classmethod
    def format_ass_time(cls, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centis = int((seconds - int(seconds)) * 100)
        return f"{hours:01d}:{minutes:02d}:{secs:02d}.{centis:02d}"

    @classmethod
    def generate_srt(cls, storyboard: List[Dict[str, Any]], output_path: str) -> str:
        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        lines = []
        for idx, scene in enumerate(storyboard, start=1):
            start = cls.format_srt_time(scene["start_time"])
            end = cls.format_srt_time(scene["end_time"])
            text = scene.get("display_text", "")
            if text:
                lines.append(f"{idx}\n{start} --> {end}\n{text}\n")

        content = "\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path

    @classmethod
    def generate_ass(cls, storyboard: List[Dict[str, Any]], output_path: str) -> str:
        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        header = """[Script Info]
Title: TinyTots Tunes Sing-Along
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KaraokePrimary,Arial Rounded MT Bold,64,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,60,60,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        event_lines = []
        for scene in storyboard:
            start = cls.format_ass_time(scene["start_time"])
            end = cls.format_ass_time(scene["end_time"])
            text = scene.get("display_text", "").replace('"', '')
            if text:
                event_lines.append(f"Dialogue: 0,{start},{end},KaraokePrimary,,0,0,0,,{text}")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header + "\n".join(event_lines) + "\n")

        return output_path

subtitle_engine = SubtitleEngine()

