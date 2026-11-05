import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URLS: dict[str, str] = {
    "slm": os.getenv("SLM_BASE_URL", "http://localhost:11434/v1"),
    "groq": "https://api.groq.com/openai/v1",
    "openai": "https://api.openai.com/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "anthropic": "https://api.anthropic.com/v1",
}

DEFAULT_MODELS: dict[str, str] = {
    "slm": "phi3.5",
    "groq": "llama-3.3-70b-versatile",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-20241022",
    "openrouter": "meta-llama/llama-3.1-8b-instruct",
}

SYSTEM_PROMPT = (
    "You are an expert Indian Income Tax assistant. "
    "Answer ONLY from the provided context excerpts from official Income Tax documents. "
    "If the context does not contain enough information to answer, say: "
    "'I cannot find this in the provided corpus.' "
    "Always cite the source document name and page number for every key claim, "
    "e.g. '(bs2024_25.pdf, p.12)'. "
    "Be precise with numbers, rates, and section references. "
    "Do not add information not present in the context."
)


def _get_provider_config() -> tuple[str, str, str]:
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    if provider not in BASE_URLS:
        raise SystemExit(f"LLM_PROVIDER={provider!r} not recognised. Valid: {sorted(BASE_URLS)}")
    model = os.getenv("LLM_MODEL") or DEFAULT_MODELS[provider]
    key_env = {
        "slm": "SLM_API_KEY",
        "groq": "GROQ_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }[provider]
    return provider, model, os.getenv(key_env, "")


def _call_openai_compatible(base: str, api_key: str, model: str, messages: list[dict], max_tokens: int) -> str:
    resp = requests.post(
        f"{base}/chat/completions",
        headers={"Authorization": f"Bearer {api_key or 'ollama'}"},
        json={
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.1,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _call_anthropic(api_key: str, model: str, messages: list[dict], max_tokens: int) -> str:
    system_text = "\n".join(m["content"] for m in messages if m["role"] == "system")
    chat_msgs = [m for m in messages if m["role"] != "system"]
    resp = requests.post(
        f"{BASE_URLS['anthropic']}/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": model,
            "system": system_text,
            "messages": chat_msgs,
            "max_tokens": max_tokens,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


def chat(
    question: str,
    context: str,
    history: list[dict] | None = None,
    max_tokens: int = 800,
) -> str:
    provider, model, api_key = _get_provider_config()
    messages: list[dict] = list(history or [])
    messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.append({
        "role": "user",
        "content": f"Context from corpus:\n{context}\n\nQuestion: {question}",
    })
    if provider == "anthropic":
        return _call_anthropic(api_key, model, messages, max_tokens)
    return _call_openai_compatible(BASE_URLS[provider], api_key, model, messages, max_tokens)
