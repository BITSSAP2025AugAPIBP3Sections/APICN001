"""Text-to-speech: local pyttsx3 by default; edge-tts (cloud) or piper via .env.

Sentence-wise chunking lets playback start before the full answer is spoken,
which is the main lever for hitting the conversational latency target.
"""
import os
import re
import subprocess
import tempfile

from dotenv import load_dotenv

load_dotenv()

_SENTENCE_RE = re.compile(r"[^.!?]+[.!?]+", re.S)


def _split_sentences(text: str) -> list[str]:
    parts = [p.strip() for p in _SENTENCE_RE.findall(text) if p.strip()]
    if not parts:
        return [text.strip()] if text.strip() else []
    # fold any trailing text with no terminal punctuation into the last part
    matched = "".join(_SENTENCE_RE.findall(text))
    tail = text[len(matched):].strip()
    if tail:
        parts.append(tail)
    return parts


def _speak_pyttsx3(text: str) -> None:
    import pyttsx3

    engine = pyttsx3.init()
    voice = os.getenv("TTS_VOICE")
    if voice:
        engine.setProperty("voice", voice)
    engine.setProperty("rate", int(os.getenv("TTS_RATE", 175)))
    engine.say(text)
    engine.runAndWait()


def _speak_edge(text: str) -> None:
    import asyncio

    import edge_tts

    voice = os.getenv("TTS_VOICE") or "en-IN-NeerjaNeural"

    async def run() -> None:
        path = tempfile.mktemp(suffix=".mp3")
        await edge_tts.Communicate(text, voice).save(path)
        _play_file(path)

    asyncio.run(run())


def _speak_piper(text: str) -> None:
    model = os.getenv("TTS_VOICE", "")
    out = tempfile.mktemp(suffix=".wav")
    proc = subprocess.run(
        ["piper", "--model", model, "--output_file", out],
        input=text.encode(),
        check=False,
    )
    if proc.returncode == 0:
        _play_file(out)


def _play_file(path: str) -> None:
    import sys

    if sys.platform == "win32":
        os.startfile(path)  # noqa: S606 — opens default player on Windows
    elif sys.platform == "darwin":
        subprocess.run(["afplay", path], check=False)
    else:
        subprocess.run(["ffplay", "-nodisp", "-autoexit", path], check=False)


def speak(text: str, sentence_chunked: bool = True) -> None:
    provider = os.getenv("TTS_PROVIDER", "pyttsx3").lower()
    fn = {"pyttsx3": _speak_pyttsx3, "edge": _speak_edge, "piper": _speak_piper}.get(
        provider, _speak_pyttsx3
    )
    if not sentence_chunked or len(text) < 160:
        fn(text)
        return
    # speak two sentences at a time so audio starts early
    sentences = _split_sentences(text)
    for i in range(0, len(sentences), 2):
        fn(" ".join(sentences[i : i + 2]))
