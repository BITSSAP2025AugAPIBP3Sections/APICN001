"""Speech-to-text: local faster-whisper by default, cloud (Groq/OpenAI) via .env."""
import os
import queue
import tempfile
import threading
import time

from dotenv import load_dotenv

load_dotenv()

_model_cache = None


def record_to_wav(seconds: float | None = None) -> str | None:
    """Press-Enter-to-start, press-Enter-to-stop recording (or a fixed duration)."""
    try:
        import numpy as np
        import sounddevice as sd
        import soundfile as sf
    except ImportError:
        print("Voice modes need: pip install sounddevice soundfile numpy faster-whisper")
        return None

    sr = 16_000
    audio_q: queue.Queue = queue.Queue()

    def callback(indata, frames, time_info, status):
        audio_q.put(indata.copy())

    running = True

    def wait_for_stop():
        nonlocal running
        input("  REC> recording... press Enter to stop.\n")
        running = False

    print("  REC> press Enter to START speaking...")
    input()
    with sd.InputStream(samplerate=sr, channels=1, dtype="int16", callback=callback):
        stopper = threading.Thread(target=wait_for_stop, daemon=True)
        stopper.start()
        frames = []
        if seconds:
            time.sleep(seconds)
            running = False
        while running:
            try:
                frames.append(audio_q.get(timeout=0.1))
            except queue.Empty:
                continue

    if not frames:
        print("  REC> no audio captured.")
        return None
    audio = np.concatenate(frames, axis=0)
    path = tempfile.mktemp(suffix=".wav")
    sf.write(path, audio, sr)
    return path


def _transcribe_cloud(wav_path: str, provider: str) -> str:
    import requests

    if provider == "groq":
        url = "https://api.groq.com/openai/v1/audio/transcriptions"
        model = os.getenv("STT_MODEL_CLOUD", "whisper-large-v3-turbo")
        key = os.getenv("GROQ_API_KEY", "")
    else:  # openai
        url = "https://api.openai.com/v1/audio/transcriptions"
        model = "whisper-1"
        key = os.getenv("OPENAI_API_KEY", "")

    with open(wav_path, "rb") as f:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {key}"},
            files={"file": f},
            data={"model": model},
            timeout=120,
        )
    resp.raise_for_status()
    return resp.json()["text"]


def _transcribe_local(wav_path: str) -> str:
    from faster_whisper import WhisperModel

    global _model_cache
    if _model_cache is None:
        t0 = time.time()
        _model_cache = WhisperModel(
            os.getenv("STT_MODEL", "base"), device="auto", compute_type="auto"
        )
        print(f"  [stt] model loaded in {time.time() - t0:.1f}s")
    segments, _info = _model_cache.transcribe(wav_path)
    return " ".join(s.text for s in segments).strip()


def transcribe(wav_path: str | None) -> str | None:
    if wav_path is None:
        return None
    provider = os.getenv("STT_PROVIDER", "local").lower()
    t0 = time.time()
    if provider in ("groq", "openai"):
        text = _transcribe_cloud(wav_path, provider)
    else:
        text = _transcribe_local(wav_path)
    print(f"  [stt {time.time() - t0:.1f}s] {text}")
    return text
