"""Measure STT transcript latency with faster-whisper on a generated WAV.

No microphone needed: we synthesise a question to WAV via pyttsx3, then time
faster-whisper transcription (model load separated from steady-state). Run from
project root: python scripts/measure_stt.py
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

SENTENCE = "What is the standard deduction under the new tax regime for this financial year?"
wav = str(ROOT / "report" / "_stt_sample.wav")

# 1) synthesise a ~5s sample to a WAV file
try:
    import pyttsx3

    eng = pyttsx3.init()
    eng.setProperty("rate", 165)
    eng.save_to_file(SENTENCE, wav)
    eng.runAndWait()
    ok = Path(wav).exists() and Path(wav).stat().st_size > 1000
    print(f"synth wav: {'ok' if ok else 'FAILED'} ({Path(wav).stat().st_size if Path(wav).exists() else 0} bytes)")
except Exception as e:  # noqa: BLE001
    print(f"pyttsx3 synth failed: {e}")
    ok = False

if not ok:
    print("No WAV to transcribe; STT timing skipped.")
    sys.exit(0)

# 2) time faster-whisper: first (with load) vs steady-state
from faster_whisper import WhisperModel  # noqa: E402

t0 = time.time()
model = WhisperModel("base", device="auto", compute_type="auto")
load_s = time.time() - t0
print(f"model load: {load_s:.1f}s")

times = []
for i in range(3):
    t0 = time.time()
    segs, _ = model.transcribe(wav)
    text = " ".join(s.text for s in segs).strip()
    dt = time.time() - t0
    times.append(dt)
    print(f"transcribe run{i+1}: {dt:.1f}s -> {text!r}")

print(f"\nSTT steady-state mean (model already loaded): {sum(times)/3:.1f}s")
print(f"STT first-call incl. load: {load_s + times[0]:.1f}s")
