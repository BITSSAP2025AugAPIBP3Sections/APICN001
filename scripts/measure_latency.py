"""Measure latency: 3 runs each of Q-E02, Q-M01, Q-C01. Run from project root."""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")
from rag.llm import chat  # noqa: E402
from rag.retriever import Retriever  # noqa: E402

Q = {
    "Q-E02": "What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investments?",
    "Q-M01": "A salaried individual earns ₹18,00,000 gross annual salary in FY 2024-25, contributes ₹1,50,000 to EPF, pays ₹50,000 NPS Tier-1, and has ₹25,000 health insurance premium. Compute tax under the new regime (assume no other deductions, standard deduction applies).",
    "Q-C01": "Mr. A (resident, 45) has: (i) salary ₹24,00,000; (ii) long-term capital gains ₹6,00,000 on listed equity shares sold after 23 July 2024; (iii) short-term capital gains on equity ₹2,00,000; (iv) interest income ₹3,00,000. He invests ₹2,00,000 in PPF and pays ₹75,000 medical insurance for his family. Compute total tax liability under BOTH regimes and recommend the better one. Show every slab step, surcharge and cess calculation.",
}

ret = Retriever("index")
results = {}
for qid, qtext in Q.items():
    full_times, retr_times = [], []
    for i in range(3):
        t0 = time.time()
        hits = ret.search(qtext, top_k=5)
        t_retr = time.time() - t0
        context = "\n\n".join(f"{h['text']}\n[source: {h['doc']} p.{h['page']}]" for h in hits)
        chat(qtext, context, [])
        full = time.time() - t0
        full_times.append(full)
        retr_times.append(t_retr)
        print(f"{qid} run{i+1}: full={full:.1f}s retrieval={t_retr*1000:.0f}ms")
    results[qid] = {
        "full_mean": round(sum(full_times) / 3, 1),
        "retr_ms": round(sum(retr_times) / 3 * 1000),
    }

print("\n=== MEANS ===")
for qid, r in results.items():
    print(f"{qid}: full_answer_mean={r['full_mean']}s  retrieval_mean={r['retr_ms']}ms")
