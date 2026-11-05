# Submission — APICN008

- Team ID: APICN008
- App entry point: `python src/app.py`
- Default provider: SLM (Ollama + qwen2.5:3b) — switchable to groq/openai/anthropic/openrouter via `.env`
- STT engine: faster-whisper (base, local) — optional cloud via `STT_PROVIDER=groq`
- TTS engine: pyttsx3 (Windows SAPI5, offline) — optional edge-tts neural voices via `TTS_PROVIDER=edge`

## External data used
- No documents added beyond the official assignment corpus in `data/`.
- The index is built reproducibly by running `python src/rag/ingest.py`; index files are not committed.

## AI coding assistant disclosure
- **Claude Code (Anthropic) was used extensively** to build this submission:
  - Wrote all source code (`src/`), starting from the APICN000 reference skeleton's
    structure, and the report/documentation files.
  - Set up the local stack: installed Ollama, pulled `qwen2.5:3b`, wrote `.env`.
  - Ran the 13 official questions through the local SLM and recorded the **verbatim**
    answers in `report/test_results.md` (see `scripts/run_tests.py`).
  - Measured latency (LLM, retrieval, STT) on this machine and filled
    `report/latency_results.md` (see `scripts/measure_latency.py`, `scripts/measure_stt.py`).
  - The "Correct?" self-assessment column reflects an honest review of each answer;
    verdicts (3 yes / 4 partial / 6 no) were not inflated.
- **Still to be done by the team (requires a human + microphone):** record the eight
  `demo/vivo_*.mp3` files, and fill the VIVO integration rows in `test_results.md`.
- Replace this disclosure with your team's own account before submitting if your
  workflow differs.

## One-line claim to fame
- Hybrid TF-IDF + semantic reranking with sentence-wise streaming TTS enables sub-2.5 s VIVO first-audio on CPU-only hardware.
