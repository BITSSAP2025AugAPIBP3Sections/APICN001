import json
import math
import re
from pathlib import Path

import numpy as np

TOKEN_RE = re.compile(r"[a-zA-Z0-9]{2,}")
STOP = set(
    "the a an and or of to in for on is are be with by from as at that this it "
    "under section subsection shall i we you he she they which who its were was "
    "have has had been do does did will would could should may might must not no".split()
)


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOP]


class Retriever:
    """Hybrid TF-IDF retriever with optional BM25-style scoring."""

    def __init__(self, index_dir: str | Path = "index"):
        data = json.loads((Path(index_dir) / "chunks.json").read_text(encoding="utf-8"))
        self.records = data
        n = len(data)

        postings: dict[str, dict[int, int]] = {}
        for i, rec in enumerate(data):
            for term in tokenize(rec["text"]):
                postings.setdefault(term, {})[i] = postings.get(term, {}).get(i, 0) + 1

        doc_len = np.array([len(tokenize(r["text"])) for r in data], dtype=float)
        avg_len = float(doc_len.mean()) if n > 0 else 1.0

        k1, b = 1.5, 0.75
        self.bm25: dict[str, dict[int, float]] = {}
        for term, docs in postings.items():
            idf = math.log((n - len(docs) + 0.5) / (len(docs) + 0.5) + 1)
            self.bm25[term] = {}
            for i, tf in docs.items():
                norm_tf = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len[i] / avg_len))
                self.bm25[term][i] = idf * norm_tf

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        scores: dict[int, float] = {}
        for term in set(tokenize(query)):
            for i, w in self.bm25.get(term, {}).items():
                scores[i] = scores.get(i, 0.0) + w
        best = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
        return [{**self.records[i], "score": round(s, 4)} for i, s in best]


if __name__ == "__main__":
    import sys

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    query = " ".join(sys.argv[1:]) or "How is long term capital gain on listed shares taxed?"
    for hit in Retriever().search(query, top_k=3):
        print(f"[{hit['doc']} p.{hit['page']} score={hit['score']}]\n{hit['text'][:200]}\n---")
