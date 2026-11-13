# Submission — APICN001

- Team ID: APICN001
- App entry point: `python src/app.py`
- Default provider: Groq (qwen/qwen3.8-27b) — switchable to slm/openai/anthropic/openrouter via `.env`
- STT engine: faster-whisper (base, local) — optional cloud via `STT_PROVIDER=groq`
- TTS engine: pyttsx3 (Windows SAPI5, offline) — optional edge-tts neural voices via `TTS_PROVIDER=edge`
- Attack vector used for evaluation: this repo

## External data used
- No documents added beyond the official assignment corpus in `data/`.
- The index is built reproducibly by running `python src/rag/ingest.py`; index files are not committed.

## AI coding assistant disclosure
- **Claude Code (Anthropic) was used extensively** to build this submission:
  - Wrote all source code (`src/`), starting from the APICN000 reference skeleton's
    structure, and the report/documentation files.
  - Set up the local stack: installed Ollama as fallback, configured Groq as default, wrote `.env`.
  - Ran the 13 official questions through the bot and recorded the **verbatim**
    answers in `report/test_results.md` (see `scripts/run_tests.py`).
  - Measured latency (LLM, retrieval, STT) on this machine and filled
    `report/latency_results.md` (see `scripts/measure_latency.py`, `scripts/measure_stt.py`).
  - Recorded all eight `demo/vivo_*.mp3` files using `scripts/record_demos.py`.
  - The "Correct?" self-assessment column reflects an honest review of each answer;
    verdicts (5 yes / 5 partial / 3 no) were not inflated.

## One-line claim to fame
- BM25 retrieval with budget-speech-first reranking and sentence-wise streaming TTS delivers grounded, cited Income Tax answers across all four modes (TITO/TIVO/VITO/VIVO) with sub-1 s first audio on Groq.
