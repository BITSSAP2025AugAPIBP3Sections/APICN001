"""Guided VIVO demo recorder for APICN001.

For each mapped question it:
  1. shows you the question to read aloud,
  2. records your spoken question (press Enter to start, Enter to stop),
  3. transcribes it (shown so you can confirm STT worked),
  4. runs RAG to get the grounded answer,
  5. synthesises the answer to speech,
  6. stitches [your question audio] + [bot answer audio] into demo/vivo_N.mp3.

Usage from project root:
  python scripts/record_demos.py            # record all 8 in order
  python scripts/record_demos.py 4          # record only vivo_4 (Q-M01)
  python scripts/record_demos.py 0 1 2      # record a subset

Needs: sounddevice, soundfile, pyttsx3, faster-whisper, ollama running.
Audio is stitched with ffmpeg if available, else saved as two-part WAV fallback.
"""
import sys
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

import numpy as np  # noqa: E402
import sounddevice as sd  # noqa: E402
import soundfile as sf  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from rag.llm import chat  # noqa: E402
from rag.retriever import Retriever  # noqa: E402
from speech import stt  # noqa: E402

SR = 16_000

# demo index -> (question id, question text)
DEMOS = {
    0: ("free choice", "Ask any Income Tax question of your choice, then ask a natural follow-up (e.g. 'and under the old regime?') to show multi-turn memory."),
    1: ("Q-E01", "What are the income tax slab rates for an individual under the new regime for FY 2024-25 (AY 2025-26)?"),
    2: ("Q-E02", "What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investments?"),
    3: ("Q-E05", "What is the tax rate applicable to income from capital gains on listed equity shares held for more than 12 months as per the latest budget?"),
    4: ("Q-M01", "A salaried individual earns 18 lakh gross annual salary in FY 2024-25, contributes 1.5 lakh to EPF, pays 50 thousand NPS, and 25 thousand health insurance. Compute tax under the new regime."),
    5: ("Q-M04", "What are the provisions for taxation of Virtual Digital Assets under Section 115BBH, including the rate, the loss set-off rule, and the TDS under Section 194S?"),
    6: ("Q-C01", "Mr A, resident aged 45, has salary 24 lakh, long term capital gains 6 lakh on listed shares sold after 23 July 2024, short term gains 2 lakh, interest income 3 lakh. He invests 2 lakh in PPF and pays 75 thousand medical insurance. Compute total tax under both regimes and recommend the better one."),
    7: ("Q-C03", "Compare the treatment of days of stay for determining residential status for an individual with Indian income of 40 lakh who visited India for 130 days across two visits. Then compute the tax if the person is RNOR with the same income."),
}


def record_fixed(seconds: float) -> np.ndarray:
    """Record for a fixed number of seconds — no stdin needed (works under non-interactive shells)."""
    print(f"    >> recording for {int(seconds)}s — start speaking NOW...")
    audio = sd.rec(int(seconds * SR), samplerate=SR, channels=1, dtype="int16")
    for remaining in range(int(seconds), 0, -1):
        print(f"       {remaining}s left...", end="\r", flush=True)
        time.sleep(1)
    sd.wait()
    print("    >> done recording.            ")
    return audio


def answer_of(ret: Retriever, question: str, history: list[dict]) -> str:
    hits = ret.search(question, top_k=5)
    context = "\n\n".join(f"{h['text']}\n[source: {h['doc']} p.{h['page']}]" for h in hits)
    return chat(question, context, history)


def tts_to_wav(text: str, path: str) -> bool:
    import pyttsx3

    eng = pyttsx3.init()
    eng.setProperty("rate", 170)
    eng.save_to_file(text, path)
    eng.runAndWait()
    return Path(path).exists() and Path(path).stat().st_size > 1000


def _ffmpeg_exe() -> str | None:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # noqa: BLE001
        return None


def stitch(q_wav: str, a_wav: str, out_path: str) -> str:
    """Concatenate question + answer audio. Prefer ffmpeg -> mp3; else wav fallback."""
    ffmpeg = _ffmpeg_exe()
    if ffmpeg:
        lst = tempfile.mktemp(suffix=".txt")
        Path(lst).write_text(f"file '{q_wav}'\nfile '{a_wav}'\n", encoding="utf-8")
        subprocess.run(
            [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-ar", "22050", out_path],
            check=False, capture_output=True,
        )
        if Path(out_path).exists():
            return out_path
    # fallback: concatenate raw samples into a .wav next to the intended name
    wav_out = out_path.rsplit(".", 1)[0] + ".wav"
    q, _ = sf.read(q_wav)
    a, _ = sf.read(a_wav)
    if q.ndim > 1:
        q = q.mean(axis=1)
    if a.ndim > 1:
        a = a.mean(axis=1)
    gap = np.zeros(int(SR * 0.5))
    sf.write(wav_out, np.concatenate([q, gap, a]), SR)
    return wav_out


def record_one(ret: Retriever, idx: int, seconds: float) -> None:
    qid, qtext = DEMOS[idx]
    print(f"\n\n{'#'*72}", flush=True)
    print(f"#  DEMO vivo_{idx}   ({qid})", flush=True)
    print(f"{'#'*72}", flush=True)
    print(f"\n   READ THIS ALOUD:\n", flush=True)
    print(f"   >>> {qtext}\n", flush=True)
    # visible, flushed countdown so you have time to read before recording
    for remaining in range(8, 0, -1):
        print(f"   recording starts in {remaining}s ...", end="\r", flush=True)
        time.sleep(1)
    print("                                           ", flush=True)
    mic = record_fixed(seconds)
    if len(mic) < SR // 2:
        print("    !! too short, skipping")
        return
    q_wav = tempfile.mktemp(suffix=".wav")
    sf.write(q_wav, mic, SR)

    transcript = stt.transcribe(q_wav) or ""
    print(f"    transcript: {transcript!r}")
    if not transcript.strip():
        print("    !! no speech detected; re-run this index")
        return

    print("    thinking...")
    ans = answer_of(ret, transcript, [])
    print(f"    answer: {ans[:160]}...")

    a_wav = tempfile.mktemp(suffix=".wav")
    if not tts_to_wav(ans, a_wav):
        print("    !! TTS failed")
        return

    out = str(ROOT / "demo" / f"vivo_{idx}.mp3")
    final = stitch(q_wav, a_wav, out)
    print(f"    SAVED -> {final}")


# per-demo recording window (seconds) — longer for complex questions
DURATIONS = {0: 18, 1: 10, 2: 10, 3: 10, 4: 18, 5: 14, 6: 22, 7: 20}


def main() -> None:
    args = [int(x) for x in sys.argv[1:] if x.isdigit()]
    todo = args or list(DEMOS.keys())
    ret = Retriever("index")
    print("Demo recorder: fixed-duration recording (no key presses needed).")
    print("Read each question aloud during its recording window.\n")
    for idx in todo:
        record_one(ret, idx, DURATIONS.get(idx, 12))
    print("\nAll requested demos recorded. Check the demo/ folder.")


if __name__ == "__main__":
    main()
