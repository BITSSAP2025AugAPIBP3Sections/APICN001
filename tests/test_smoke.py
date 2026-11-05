"""Smoke tests for the APICN008 RAG VoiceBot. Run: python -m pytest tests/ -q"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rag.retriever import Retriever, tokenize  # noqa: E402


def test_tokenize_drops_stopwords() -> None:
    toks = tokenize("the capital gain under section 112A")
    assert "the" not in toks
    assert "section" not in toks
    assert "capital" in toks


def test_retriever_ranks_relevant_chunk(tmp_path: Path) -> None:
    records = [
        {"text": "Section 80C allows a deduction up to one lakh fifty thousand for provident fund and ELSS.", "doc": "a.pdf", "page": 1},
        {"text": "TCS under section 206C applies to liberalised remittance scheme remittances.", "doc": "b.pdf", "page": 7},
    ]
    (tmp_path / "chunks.json").write_text(json.dumps(records), encoding="utf-8")
    ret = Retriever(tmp_path)
    hits = ret.search("80C deduction provident fund", top_k=1)
    assert hits[0]["doc"] == "a.pdf"


def test_retriever_returns_scores(tmp_path: Path) -> None:
    records = [{"text": "Long term capital gains on listed equity are taxed at twelve point five percent.", "doc": "c.pdf", "page": 3}]
    (tmp_path / "chunks.json").write_text(json.dumps(records), encoding="utf-8")
    ret = Retriever(tmp_path)
    hits = ret.search("long term capital gains listed equity rate", top_k=1)
    assert hits[0]["score"] > 0
