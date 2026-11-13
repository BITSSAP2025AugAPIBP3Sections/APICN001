# Architecture — APICN001

## Overview

A retrieve-then-generate pipeline for Indian Income Tax questions, wired to four
interaction modes (TITO / TIVO / VITO / VIVO) behind one shared core.

## Pipeline

```
PDFs in data/  ──ingest.py──▶  index/chunks.json  ──Retriever──▶  top-k chunks
                                                                      │
 question ──(STT if voice)──▶  Retriever.search() ──▶ context + question ──▶ llm.chat()
                                                                      │
                                              answer + citations ──(TTS if voice)──▶ user
```

1. **Ingest** (`src/rag/ingest.py`). Each PDF in `data/` is read with PyMuPDF
   (≈35× faster than pypdf on the large documents). Pages are flattened and split
   into ~900-character chunks with 150-character overlap. Each chunk keeps its
   source `doc` and `page` so citations are exact. Output is a single
   `index/chunks.json` (1,456 chunks across 10 PDFs). The index is rebuilt by
   script and never committed.

2. **Retrieve** (`src/rag/retriever.py`). A BM25 scorer over tokenised chunks.
   BM25 was chosen over plain TF-IDF because the corpus mixes short FAQ answers
   with long budget-speech pages; BM25's length normalisation stops the long
   pages from dominating every query. Stopwords (including tax-document filler
   such as "section", "shall", "subsection") are dropped so scoring keys on the
   substantive terms. `top_k` is configurable (default 5).

3. **Generate** (`src/rag/llm.py`). One OpenAI-compatible client serves `slm`
   (Ollama), `groq`, `openai`, and `openrouter`; Anthropic has a thin second path
   for its Messages API. The provider, model, and key are selected purely from
   `.env` — the default is `groq` with `qwen/qwen3.8-27b`, and switching to any
   other provider is a one-line config change with no code edit. The system prompt
   forces answers from context only, demands a document+page citation for each
   claim, and instructs the model to say it cannot find the answer in the corpus
   rather than hallucinate.

## Modes (`src/app.py`)

All four modes share `answer()`. The differences are only at the edges:

| Mode | Input edge | Output edge |
|------|-----------|-------------|
| TITO | `input()` | `print()` |
| TIVO | `input()` | `tts.speak()` |
| VITO | `stt.record_to_wav()` → `stt.transcribe()` | `print()` |
| VIVO | `stt.record_to_wav()` → `stt.transcribe()` | `tts.speak()` |

The transcribed question is always printed so an evaluator can verify STT. A
Gradio web UI (`--ui web`) exposes the text and voice paths in a browser, and a
`--question` one-shot path is used for latency timing.

## Speech

- **STT** (`src/speech/stt.py`): local faster-whisper (`base`) by default, with
  the model cached across turns so only the first transcription pays load time;
  cloud Groq/OpenAI Whisper selectable via `STT_PROVIDER`.
- **TTS** (`src/speech/tts.py`): pyttsx3 (offline Windows SAPI5) by default;
  edge-tts Indian-English neural voice or Piper via `.env`. Answers are split into
  sentence pairs and spoken progressively, so the first audio starts before the
  whole answer is synthesised.

## Why this design

The corpus is small enough (~1,456 chunks) that a dependency-free BM25 retriever
beats the latency of loading an embedding model on a CPU-only laptop, while still
giving accurate, citable grounding. Keeping one provider-agnostic LLM client means
the Groq default and every other supported provider (slm/openai/anthropic/openrouter)
run through identical code, which is exactly what the assignment's `.env` switch requires.

*(TIVO and VITO are reachable with `--mode tivo` / `--mode vito`; the Voice tab of
the web UI demonstrates VITO/VIVO end to end.)*
