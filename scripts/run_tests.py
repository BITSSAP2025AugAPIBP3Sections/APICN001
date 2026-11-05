"""Run the 13 official questions through the bot and write filled report tables.

Usage: python scripts/run_tests.py
Reads INDEX_DIR + .env from the APICN008 project (run from the project root).
Writes:
  report/_answers.json        raw results (answer, sources, timings)
  report/test_results.FILLED.md
  report/latency_results.FILLED.md
"""
import json
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

QUESTIONS = {
    "Q-E01": "What are the income tax slab rates for an individual under the new regime for FY 2024-25 (AY 2025-26)?",
    "Q-E02": "What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investments?",
    "Q-E03": "What is the basic exemption limit for a resident individual under 60 years of age under the old regime?",
    "Q-E04": "What is the standard deduction available to a salaried employee under the new tax regime for FY 2024-25?",
    "Q-E05": "What is the tax rate applicable to income from capital gains on listed equity shares held for more than 12 months (long-term capital gains) as per the latest budget?",
    "Q-M01": "A salaried individual earns ₹18,00,000 gross annual salary in FY 2024-25, contributes ₹1,50,000 to EPF, pays ₹50,000 NPS Tier-1, and has ₹25,000 health insurance premium. Compute tax under the new regime (assume no other deductions, standard deduction applies).",
    "Q-M02": "I bought a residential property for ₹80,00,000 in 2018 and sold it in FY 2024-25 for ₹1,20,00,000. Compute the capital gains tax due (you may state your assumptions on indexation clearly).",
    "Q-M03": "An individual transfers ₹12,00,000 in a financial year under the Liberalised Remittance Scheme (LRS) for foreign education. What is the TCS rate that applies after the FY 2023-24 changes to Section 206C, and what exemption applies?",
    "Q-M04": "What are the provisions for taxation of Virtual Digital Assets (cryptocurrency) under Section 115BBH, including the rate, the loss set-off rule, and the TDS under Section 194S?",
    "Q-M05": "A taxpayer has both salary income and house property income (one self-occupied house with home-loan interest of ₹2,00,000). Under which regime (old vs new) would their tax be lower, and why? Assume gross total income of ₹15,00,000, all of it except the interest deduction being salary.",
    "Q-C01": "Mr. A (resident, 45) has: (i) salary ₹24,00,000; (ii) long-term capital gains ₹6,00,000 on listed equity shares sold after 23 July 2024; (iii) short-term capital gains on equity ₹2,00,000; (iv) interest income ₹3,00,000. He invests ₹2,00,000 in PPF and pays ₹75,000 medical insurance for his family. Compute total tax liability under BOTH regimes and recommend the better one. Show every slab step, surcharge and cess calculation.",
    "Q-C02": "A non-resident FII earned ₹50,00,000 from Indian listed securities in FY 2024-25. Explain how the FAQs on FIIs exemption and the transition provisions apply to the taxation of its income, what the applicable rate is, and what documentation is needed to claim the benefit.",
    "Q-C03": "Compare the treatment of \"days of stay\" for determining residential status for an individual with Indian income of ₹40,00,000 who visited India for 130 days across two visits in a year, referencing the transition/deeming provisions. Then compute the tax consequence if the person is deemed resident but not ordinarily resident (RNOR) with the same income.",
}

TOP_K = 5


def sources_of(hits: list[dict]) -> str:
    seen = []
    for h in hits:
        key = f"{h['doc']} p.{h['page']}"
        if key not in seen:
            seen.append(key)
    return "; ".join(seen)


def run() -> dict:
    ret = Retriever("index")
    results = {}
    for qid, qtext in QUESTIONS.items():
        print(f"\n=== {qid} ===")
        t0 = time.time()
        hits = ret.search(qtext, top_k=TOP_K)
        context = "\n\n".join(f"{h['text']}\n[source: {h['doc']} p.{h['page']}]" for h in hits)
        answer = chat(qtext, context, [])
        elapsed = round(time.time() - t0, 1)
        results[qid] = {
            "question": qtext,
            "answer": answer.strip(),
            "sources": sources_of(hits),
            "elapsed_s": elapsed,
        }
        print(f"[{elapsed}s] {answer[:180]}...")
    (ROOT / "report" / "_answers.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return results


if __name__ == "__main__":
    run()
    print("\nDone. Raw results -> report/_answers.json")
