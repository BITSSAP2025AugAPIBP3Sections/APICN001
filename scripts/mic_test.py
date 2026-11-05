"""Quick mic level test: records 5s from the default input and reports volume.
Run: python scripts/mic_test.py   (speak during the 5s window)
"""
import sys
import time

import numpy as np
import sounddevice as sd

SR = 16_000
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

print("Default input device:")
print("  ", sd.query_devices(kind="input")["name"])
print("\nRecording 5 seconds — SPEAK NOW (say 'testing one two three')...")
audio = sd.rec(int(5 * SR), samplerate=SR, channels=1, dtype="int16")
for r in range(5, 0, -1):
    print(f"  {r}...", end="\r", flush=True)
    time.sleep(1)
sd.wait()

a = audio.astype(np.float32) / 32768.0
peak = float(np.abs(a).max())
rms = float(np.sqrt((a ** 2).mean()))
print(f"\n\npeak level : {peak:.3f}   (want > 0.05)")
print(f"rms  level : {rms:.4f}   (want > 0.005)")
if peak < 0.02:
    print("\nRESULT: mic captured (near) SILENCE — wrong device, muted, or no voice reached it.")
    print("Input devices with channels:")
    for i, d in enumerate(sd.query_devices()):
        if d["max_input_channels"] > 0:
            print(f"  [{i}] {d['name']}")
else:
    print("\nRESULT: mic is WORKING — your voice was captured. Recording demos will work.")
