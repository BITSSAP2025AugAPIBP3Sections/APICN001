"""APICN001: RAG VoiceBot for Indian Income Tax — TITO / TIVO / VITO / VIVO.

Usage:
  python src/app.py --mode tito            typed question -> typed answer
  python src/app.py --mode tivo            typed question -> spoken answer
  python src/app.py --mode vito            spoken question -> typed answer
  python src/app.py --mode vivo            spoken question -> spoken answer
  python src/app.py --question "..."       one-shot (handy for latency measurement)
  python src/app.py --ui web               launch the Gradio web UI (all modes)

Voice modes need: pip install faster-whisper sounddevice soundfile pyttsx3
"""
import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Make stdout UTF-8 so PDF-sourced characters never crash the Windows console.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

from dotenv import load_dotenv  # noqa: E402

from rag.llm import chat  # noqa: E402
from rag.retriever import Retriever  # noqa: E402

load_dotenv()

TOP_K = int(os.getenv("TOP_K", 5))


def answer(ret: Retriever, question: str, history: list[dict]) -> tuple[str, list[dict], float]:
    t0 = time.time()
    hits = ret.search(question, top_k=TOP_K)
    context = "\n\n".join(
        f"{h['text']}\n[source: {h['doc']} p.{h['page']}]" for h in hits
    )
    text = chat(question, context, history)
    elapsed = time.time() - t0
    return text, hits, elapsed


def format_sources(hits: list[dict]) -> str:
    seen = []
    for h in hits:
        key = f"{h['doc']} p.{h['page']}"
        if key not in seen:
            seen.append(key)
    return "Sources: " + "; ".join(seen)


def run_cli(mode: str) -> None:
    ret = Retriever(os.getenv("INDEX_DIR", "index"))
    history: list[dict] = []
    voice_in = mode in ("vito", "vivo")
    voice_out = mode in ("tivo", "vivo")

    print(f"\n=== APICN001 VoiceBot [{mode.upper()}] ===")
    print("Type 'quit' to exit.\n" if not voice_in else "")

    while True:
        if voice_in:
            from speech import stt

            wav = stt.record_to_wav()
            question = stt.transcribe(wav)
            if not question:
                continue
            print(f"\nYou (transcribed)> {question}")
        else:
            question = input("\nYou> ").strip()
            if not question:
                break
            if question.lower() in {"quit", "exit"}:
                break

        text, hits, elapsed = answer(ret, question, history)
        print(f"\nBot> {text}")
        print(format_sources(hits))
        print(f"[answered in {elapsed:.1f}s]")

        history += [
            {"role": "user", "content": question},
            {"role": "assistant", "content": text[:1800]},
        ]

        if voice_out:
            from speech import tts

            tts.speak(text)


def run_oneshot(mode: str, question: str) -> None:
    ret = Retriever(os.getenv("INDEX_DIR", "index"))
    text, hits, elapsed = answer(ret, question, [])
    print(text)
    print(format_sources(hits))
    print(f"[answered in {elapsed:.1f}s]")
    if mode in ("tivo", "vivo"):
        from speech import tts

        tts.speak(text)


def run_web() -> None:
    import gradio as gr

    ret = Retriever(os.getenv("INDEX_DIR", "index"))
    state: dict[str, list[dict]] = {"history": []}

    def respond_text(question: str) -> tuple[str, str]:
        if not question.strip():
            return "", ""
        text, hits, elapsed = answer(ret, question, state["history"])
        state["history"] += [
            {"role": "user", "content": question},
            {"role": "assistant", "content": text[:1800]},
        ]
        return f"{text}\n\n{format_sources(hits)}\n[answered in {elapsed:.1f}s]", ""

    def respond_voice(audio_path: str) -> tuple[str, str]:
        from speech import stt

        question = stt.transcribe(audio_path)
        if not question:
            return "(no speech detected)", ""
        text, hits, elapsed = answer(ret, question, state["history"])
        state["history"] += [
            {"role": "user", "content": question},
            {"role": "assistant", "content": text[:1800]},
        ]
        return question, f"{text}\n\n{format_sources(hits)}\n[answered in {elapsed:.1f}s]"

    def clear() -> None:
        state["history"] = []

    with gr.Blocks(title="APICN001 Income Tax VoiceBot") as demo:
        gr.Markdown("# APICN001 — Income Tax RAG VoiceBot\nAll four modes: TITO / TIVO / VITO / VIVO")
        with gr.Tab("Text (TITO / TIVO)"):
            q = gr.Textbox(label="Your question")
            a = gr.Textbox(label="Answer", lines=10)
            with gr.Row():
                gr.Button("Ask").click(respond_text, inputs=q, outputs=[a, q])
                gr.Button("Clear history").click(clear)
            gr.Markdown("*For TIVO, use the CLI (`--mode tivo`) which also speaks the answer.*")
        with gr.Tab("Voice (VITO / VIVO)"):
            mic = gr.Audio(sources=["microphone"], type="filepath", label="Speak your question")
            transcript = gr.Textbox(label="Transcribed question")
            va = gr.Textbox(label="Answer", lines=10)
            mic.change(respond_voice, inputs=mic, outputs=[transcript, va])

    demo.launch(server_port=int(os.getenv("PORT", 7860)))


def main() -> None:
    parser = argparse.ArgumentParser(description="APICN001 Income Tax RAG VoiceBot")
    parser.add_argument("--mode", choices=["tito", "tivo", "vito", "vivo"], default="tito")
    parser.add_argument("--question", help="one-shot question then exit")
    parser.add_argument("--ui", choices=["cli", "web"], default="cli")
    args = parser.parse_args()

    if args.ui == "web":
        run_web()
    elif args.question:
        run_oneshot(args.mode, args.question)
    else:
        run_cli(args.mode)


if __name__ == "__main__":
    main()
