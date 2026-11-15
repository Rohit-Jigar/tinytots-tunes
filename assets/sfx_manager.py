import os
import wave
import numpy as np
from pathlib import Path
from typing import Optional
from core.config import config
from core.logger import logger

class SFXManager:
    """
    Manages and synthesizes cartoon sound effects for toddler animations.
    All sound effects are generated procedurally with high acoustic clarity.
    """

    def __init__(self):
        self.sfx_dir = config.DATA_DIR / "sfx"
        self.sfx_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_default_sfx()

    def _ensure_default_sfx(self):
        effects = ["pop", "chime", "giggle", "splash", "clap", "boing"]
        for eff in effects:
            target = self.sfx_dir / f"{eff}.wav"
            if not target.exists():
                self._generate_sfx(eff, str(target))

    def _generate_sfx(self, effect_name: str, output_path: str):
        sample_rate = 44100
        duration = 0.6
        total_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, total_samples, False)
        signal = np.zeros(total_samples, dtype=np.float32)

        if effect_name == "pop":
            # Pitch swept sine wave (400 Hz to 1200 Hz down to 200 Hz) with rapid decay
            freq = 400 + 800 * np.exp(-t * 30)
            env = np.exp(-t * 25)
            signal = np.sin(2 * np.pi * freq * t) * env
        elif effect_name == "chime":
            # Multi-harmonic crystalline chime (E6, G#6, B6, E7)
            frequencies = [1318.51, 1661.22, 1975.53, 2637.02]
            for i, f in enumerate(frequencies):
                st = np.maximum(0, t - i * 0.05)
                signal += np.sin(2 * np.pi * f * st) * np.exp(-st * 6) * 0.35
        elif effect_name == "boing":
            # Cartoon bouncy spring: modulating pitch with high vibrato
            freq = 200 + 350 * np.exp(-t * 4) + 60 * np.sin(2 * np.pi * 18 * t)
            env = np.exp(-t * 5)
            signal = np.sin(2 * np.pi * freq * t) * env
        elif effect_name == "splash":
            # Noise burst with liquid resonance
            noise = np.random.uniform(-1, 1, total_samples)
            filt = np.sin(2 * np.pi * 650 * t)
            signal = (noise * 0.6 + filt * 0.4) * np.exp(-t * 9)
        elif effect_name == "clap":
            # Sharp double transient
            env1 = np.exp(-t * 40)
            t2 = np.maximum(0, t - 0.03)
            env2 = np.exp(-t2 * 35)
            noise = np.random.uniform(-1, 1, total_samples)
            signal = noise * (env1 * 0.6 + env2 * 0.4)
        else:
            # Gentle playful twinkle
            freq = 880 + 440 * np.sin(2 * np.pi * 6 * t)
            signal = np.sin(2 * np.pi * freq * t) * np.exp(-t * 7)

        # Normalize and save 16-bit WAV
        max_val = np.max(np.abs(signal))
        if max_val > 0.001:
            signal = (signal / max_val) * 0.9

        int_data = (signal * 32767).astype(np.int16)
        with wave.open(output_path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(int_data.tobytes())

        logger.info("Synthesized default SFX '%s' to %s", effect_name, output_path)

    def get_sfx_path(self, effect_name: str) -> Optional[str]:
        if not effect_name:
            return None
        clean_name = effect_name.lower().replace("[", "").replace("]", "").replace("!", "").strip()
        path = self.sfx_dir / f"{clean_name}.wav"
        if path.exists():
            return str(path)
        # Fallback to pop
        fallback = self.sfx_dir / "pop.wav"
        return str(fallback) if fallback.exists() else None

sfx_manager = SFXManager()
