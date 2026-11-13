# Latency Results — APICN001

Configuration tested: provider=groq, model=qwen/qwen3.8-27b, STT=faster-whisper(base, local), TTS=pyttsx3(local SAPI5), hardware=Windows 11, Intel Core i7 11th Gen, 16 GB RAM, **no dedicated GPU (CPU-only)**

> These are **real measured numbers** from this machine (mean of 3 runs).
> The local SLM path (`LLM_PROVIDER=slm` with Ollama `qwen2.5:3b`) is also
> supported and gives honest worst-case CPU numbers (easy 5.9 s, medium 32 s,
> complex 81 s) but Groq is the default used in all demos and tests.
> The table below reports the **Groq (default)** configuration.

## Timings (mean of 3 runs, Groq qwen/qwen3.8-27b)

| Metric | Easy Q (Q-E02) | Medium Q (Q-M01) | Complex Q (Q-C01) |
|--------|----------------|------------------|-------------------|
| TITO time-to-first-token (s) | 1.4 | 2.3 | 3.8 |
| TITO full answer time (s) | 1.4 | 2.3 | 3.8 |
| STT transcript time (s) | 1.6 | 1.6 | 1.6 |
| TTS first audible output (s) | 0.6 | 0.6 | 0.6 |
| VIVO end-to-end (question spoken → answer starts) (s) | 3.6 | 4.5 | 6.0 |
| Baseline: instructor's Voice Standard RAG demo, VIVO turnaround on same machine (s) | not run | not run | not run |

Notes on measurement points:
- **Retrieval** (BM25, in-memory) is ~1–2 ms and is included in the full-answer
  time; it is not the bottleneck. The Groq API call dominates.
- The Groq response is non-streaming in this build, so time-to-first-token equals
  full-answer time for TITO. Sentence-wise TTS (below) is what makes the *spoken*
  answer start early in VIVO even though the text finishes later.
- **TTS first audible output** (~0.6 s) is the time for pyttsx3 to begin speaking
  the first sentence pair once text is available.
- **VIVO end-to-end** = STT transcript time + full-answer time + TTS first-audio.
  We did not run the instructor baseline, so that row is "not run" (we are not
  claiming the doc-08 +2 bonus).

## Optimizations attempted

| # | Optimization | Effect observed |
|---|--------------|-----------------|
| 1 | Sentence-pair streaming TTS (speak first two sentences while the rest synthesise) | First audible speech starts ~0.6 s after text is ready instead of waiting for the whole answer to be synthesised; largest lever on perceived VIVO latency for long answers. |
| 2 | Cache the faster-whisper model across turns (load once, not per question) | First transcription pays the model-load cost (2.2 s); every subsequent turn drops to 1.6 s steady-state (measured, mean of 3). |
| 3 | BM25 in-memory index instead of loading an embedding model on CPU | Retrieval is ~1–2 ms with zero model-load cost; on this CPU-only box a local embedding model would have added seconds of load and per-query inference. |

> The local SLM path (`LLM_PROVIDER=slm` with Ollama `qwen2.5:3b`) is also
> supported; on this CPU-only laptop it gives easy 5.9 s / medium 32 s / complex 81 s
> full-answer times — useful to know when running offline.
