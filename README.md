# APICN001 — RAG VoiceBot (Income Tax India)

## Team
| Member | Role | Email |
|--------|------|-------|
| Rajoli Vignesh | Lead Developer | 2023sl20037@wilp.bits-pilani.ac.in |
| Priya Sahay | RAG & ML | 2023sl70012@wilp.bits-pilani.ac.in  |
 Kousik Das | RAG & ML | 2023sl70006@wilp.bits-pilani.ac.in  |
  Pallavi S | RAG & ML | 2023sl70041@wilp.bits-pilani.ac.in  |

## Overview

A **RAG-based Income Tax (India) chatbot** that works in four interaction modes:

| Mode | Input | Output |
|------|-------|--------|
| TITO | Typed question | Typed answer |
| TIVO | Typed question | Spoken answer |
| VITO | Spoken question | Typed answer |
| VIVO | Spoken question | Spoken answer |

Answers are grounded in official Income Tax documents (Income Tax Act 1961, Budget 2022–2026, and FAQs on crypto/BIS/FIIs/transition provisions). Sources are cited for every answer.

## How to run

### Prerequisites
- Python 3.10+
- (Optional, for local SLM) [Ollama](https://ollama.ai/) installed and running
- Microphone for VITO/VIVO modes

### Setup steps

1. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env: set LLM_PROVIDER and the matching API key
   ```

4. **Place data files**
   Copy the PDFs from the assignment `data/` folder into this repo's `data/` directory.

5. **Build the index**
   ```bash
   python src/rag/ingest.py
   ```
   This chunks and indexes all PDFs in `data/` into `index/`.

6. **Start the app**
   ```bash
   # TITO (default)
   python src/app.py --mode tito

   # TIVO (text in, voice out)
   python src/app.py --mode tivo

   # VITO (voice in, text out)
   python src/app.py --mode vito

   # VIVO (voice in, voice out)
   python src/app.py --mode vivo

   # Web UI (all modes via browser)
   python src/app.py --ui web
   ```

## Modes

- **TITO**: Type a question at the prompt. The bot retrieves relevant chunks and prints the answer with source citations.
- **TIVO**: Type a question; the bot answers in text then speaks the answer aloud via TTS.
- **VITO**: Press Enter to start recording, press Enter again to stop. The bot transcribes your question and prints the answer.
- **VIVO**: Same as VITO but the answer is also spoken aloud. This is the headline mode; demos are recorded from this mode.

## LLM Provider switching

Edit `.env` and set `LLM_PROVIDER` to one of: `slm` | `groq` | `openai` | `anthropic` | `openrouter`

```
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...
LLM_MODEL=llama-3.3-70b-versatile
```

## Hardware used

- Laptop: Windows 11, Intel Core i7 (11th Gen), 16 GB RAM, no dedicated GPU (CPU-only)
- Default mode as tested: Ollama with `qwen2.5:3b` (local, CPU-only)
- STT: faster-whisper `base` model on CPU (1.6 s steady-state per ~5-second clip, measured)
- TTS: pyttsx3 (Windows SAPI5, offline)

## Latency summary (local SLM, qwen2.5:3b on CPU — measured, mean of 3)
- TITO full answer: easy 5.9 s, medium 32.0 s, complex 81.2 s
- Retrieval (BM25): ~1–2 ms
- STT transcript ready: 1.6 s
- TTS first audible output: ~0.6 s
- VIVO end-to-end (spoken → answer starts): easy 8.1 s

> On a CPU-only laptop the 3B SLM is the bottleneck on medium/complex questions.
> Set `LLM_PROVIDER=groq` in `.env` (no code change) to bring full answers to the
> 1–3 s range. See `report/latency_results.md` for the full table and optimisations.
