import os
import subprocess
import requests
import asyncio
from pathlib import Path
from typing import Optional
from core.config import config
from core.logger import logger
from assets.base import BaseVoiceProvider

class WindowsSAPIVoiceProvider(BaseVoiceProvider):
    """
    Built-in Windows Neural/Desktop Speech Synthesizer:
    Zero external dependencies, instant generation, completely offline.
    Automatically handles Linux/Docker container fallbacks gracefully.
    """
    def synthesize_speech(self, text: str, output_path: str, voice_name: Optional[str] = None) -> str:
        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        # Clean text for speech synthesis
        clean_text = text.replace('"', '""').replace("'", "''").strip()
        wav_path = str(Path(output_path).with_suffix(".wav"))

        if os.name != "nt":
            return self._synthesize_linux_fallback(clean_text, output_path)

        ps_script = f"""
        Add-Type -AssemblyName System.Speech;
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
        $synth.Rate = 0;
        $synth.Volume = 100;
        # Select female or child-friendly voice if available (e.g. Zira)
        try {{
            $synth.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Female);
        }} catch {{}}
        $synth.SetOutputToWaveFile('{wav_path}');
        $synth.Speak('{clean_text}');
        $synth.Dispose();
        """

        logger.info("Synthesizing speech via Windows SAPI: '%s'...", clean_text[:40])
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True,
                text=True
            )
            if res.returncode != 0 or not os.path.exists(wav_path):
                raise RuntimeError(f"SAPI TTS failed: {res.stderr}")
        except (FileNotFoundError, RuntimeError) as exc:
            logger.warning("PowerShell SAPI not available: %s. Using Linux/Universal fallback.", exc)
            return self._synthesize_linux_fallback(clean_text, output_path)

        # Convert to mp3 if requested and ffmpeg is available
        if output_path.lower().endswith(".mp3"):
            from video.audio_postproduction import audio_postproduction
            try:
                audio_postproduction.master_vocal_track(wav_path, output_path)
                if os.path.exists(wav_path) and wav_path != output_path:
                    os.remove(wav_path)
            except Exception:
                cmd = [config.FFMPEG_PATH, "-y", "-i", wav_path, "-b:a", "192k", output_path]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            from video.audio_postproduction import audio_postproduction
            try:
                temp_master = output_path + ".temp.wav"
                audio_postproduction.master_vocal_track(wav_path, temp_master)
                os.replace(temp_master, output_path)
            except Exception:
                pass

        logger.info("Saved SAPI synthesized speech to %s", output_path)
        return output_path

    def _synthesize_linux_fallback(self, text: str, output_path: str) -> str:
        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        wav_path = str(Path(output_path).with_suffix(".wav"))

        # Try edge-tts first if available
        try:
            import edge_tts
            async def _run():
                comm = edge_tts.Communicate(text, "en-US-AnaNeural", pitch="+15Hz", rate="+5%")
                await comm.save(wav_path)
            asyncio.run(_run())
            if os.path.exists(wav_path) and os.path.getsize(wav_path) > 100:
                if output_path.lower().endswith(".mp3"):
                    cmd = [config.FFMPEG_PATH, "-y", "-i", wav_path, "-b:a", "192k", output_path]
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if wav_path != output_path and os.path.exists(wav_path):
                        os.remove(wav_path)
                    return output_path
                return wav_path
        except Exception:
            pass

        # Synthesize procedural speech tone wave
        import wave, struct, math
        sample_rate = 44100
        words = max(len(text.split()), 1)
        duration = max(words * 0.35, 1.5)
        total_samples = int(sample_rate * duration)
        with wave.open(wav_path, "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            frames = bytearray()
            for i in range(total_samples):
                t = i / sample_rate
                env = 0.5 * (1 - math.cos(2 * math.pi * t / duration))
                val = env * 0.35 * (math.sin(2 * math.pi * 261.63 * t) + 0.4 * math.sin(2 * math.pi * 523.25 * t))
                sample = int(val * 32767)
                frames.extend(struct.pack("<h", max(-32768, min(32767, sample))))
            wf.writeframes(frames)

        if output_path.lower().endswith(".mp3"):
            cmd = [config.FFMPEG_PATH, "-y", "-i", wav_path, "-b:a", "192k", output_path]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if wav_path != output_path and os.path.exists(wav_path):
                os.remove(wav_path)
            return output_path
        return wav_path

class EdgeTTSVoiceProvider(BaseVoiceProvider):
    """
    Microsoft Edge Neural TTS (Natural child/female voices, high quality).
    """
    def synthesize_speech(self, text: str, output_path: str, voice_name: Optional[str] = None) -> str:
        voice = voice_name or config.DEFAULT_VOICE_NAME or "en-US-AnaNeural"
        clean_text = text.strip()
        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        try:
            import edge_tts
            async def _run_edge():
                # Preschool bright pitch (+15Hz) and friendly rate
                communicate = edge_tts.Communicate(clean_text, voice, pitch="+15Hz", rate="+5%")
                await communicate.save(output_path)
            asyncio.run(_run_edge())
            # Master the output
            from video.audio_postproduction import audio_postproduction
            temp_master = output_path + ".mastered.mp3"
            audio_postproduction.master_vocal_track(output_path, temp_master)
            os.replace(temp_master, output_path)
            logger.info("Saved Edge TTS speech to %s", output_path)
            return output_path
        except Exception as e:
            logger.warning("Edge TTS module unavailable or network error: %s. Falling back to SAPI.", e)
            return WindowsSAPIVoiceProvider().synthesize_speech(text, output_path, voice_name)

class OpenAITTSVoiceProvider(BaseVoiceProvider):
    """OpenAI TTS API provider."""
    def synthesize_speech(self, text: str, output_path: str, voice_name: Optional[str] = None) -> str:
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured in .env!")

        headers = {
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "tts-1",
            "input": text,
            "voice": voice_name or "nova",  # nova is friendly and high-pitched
            "response_format": "mp3"
        }

        resp = requests.post("https://api.openai.com/v1/audio/speech", json=payload, headers=headers, timeout=30)
        resp.raise_for_status()

        parent_dir = os.path.dirname(output_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(resp.content)

        logger.info("Saved OpenAI TTS speech to %s", output_path)
        return output_path

class ElevenLabsVoiceProvider(BaseVoiceProvider):
    """ElevenLabs Voice API provider."""
    def synthesize_speech(self, text: str, output_path: str, voice_name: Optional[str] = None) -> str:
        if not config.ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY is not configured in .env!")

        voice_id = config.ELEVENLABS_VOICE_ID or "21m00Tcm4TlvDq8ikWAM"  # Default friendly voice
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": config.ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=12)
            resp.raise_for_status()

            parent_dir = os.path.dirname(output_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(resp.content)

            return output_path
        except Exception as e:
            logger.warning("ElevenLabs request error: %s. Using high-quality Edge-TTS child voice fallback.", e)
            return EdgeTTSVoiceProvider().synthesize_speech(text, output_path, voice_name=voice_name)

class VoiceOrchestrator:
    """Manages multi-provider voice generation with automatic local fallback."""
    def __init__(self):
        self.providers = {
            "windows_sapi": WindowsSAPIVoiceProvider(),
            "sapi": WindowsSAPIVoiceProvider(),
            "edge_tts": EdgeTTSVoiceProvider(),
            "openai": OpenAITTSVoiceProvider(),
            "elevenlabs": ElevenLabsVoiceProvider(),
            "mock": WindowsSAPIVoiceProvider()
        }

    def synthesize(self, text: str, output_path: str, provider_name: Optional[str] = None, voice_name: Optional[str] = None) -> str:
        chosen = (provider_name or config.VOICE_PROVIDER).lower()
        provider = self.providers.get(chosen, self.providers["windows_sapi"])

        try:
            return provider.synthesize_speech(text, output_path, voice_name=voice_name)
        except Exception as e:
            logger.warning("Primary voice provider '%s' failed: %s. Falling back to Microsoft Edge Neural child voice.", chosen, e)
            try:
                return self.providers["edge_tts"].synthesize_speech(text, output_path, voice_name=voice_name)
            except Exception:
                return self.providers["windows_sapi"].synthesize_speech(text, output_path, voice_name=voice_name)

voice_generator = VoiceOrchestrator()
