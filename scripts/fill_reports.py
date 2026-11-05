"""Generate the filled report files from report/_answers.json + measured verdicts.

Run from the project root: python scripts/fill_reports.py
Writes report/test_results.md (overwrites the template with real bot output).
Self-assessment verdicts are hand-set below from an honest review of each answer.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

answers = json.loads((ROOT / "report" / "_answers.json").read_text(encoding="utf-8"))

# Honest self-assessment: verdict + short evaluator note per question.
VERDICTS = {
    "Q-E01": ("no", "Slabs exist in bs2024_25.pdf but retrieval surfaced FAQ pages instead; bot refused. Retrieval miss, not hallucination."),
    "Q-E02": ("yes", "Rs 1.5 lakh cap + LIC/PF/tuition correct and grounded."),
    "Q-E03": ("partial", "Old-regime Rs 2.5 lakh limit is not clearly in this budget-centric corpus; honest refusal."),
    "Q-E04": ("yes", "Rs 75,000 standard deduction, correctly cited (bs2024_25.pdf p.32)."),
    "Q-E05": ("yes", "12.5% LTCG matches Budget 2024-25, cited."),
    "Q-M01": ("no", "Correctly found 75k std deduction but applied a flat 25% to the whole income instead of slab-wise; final figure wrong."),
    "Q-M02": ("partial", "Property indexation detail not in corpus; refusal is defensible but no computation attempted."),
    "Q-M03": ("partial", "20% TCS rate correct; missed the education-via-loan 0.5% nuance and the Rs 7 lakh threshold framing."),
    "Q-M04": ("no", "115BBH/194S crypto provisions are in bs202223.pdf; retrieval under-grounded and bot refused."),
    "Q-M05": ("no", "Slab arithmetic garbled (wrong band widths); regime recommendation direction plausible but numbers wrong."),
    "Q-C01": ("no", "Answer truncated/looped with invented slab bands; no valid surcharge/cess computation."),
    "Q-C02": ("partial", "Mentions 20% rate but cites a non-existent 'section 210(1)'; FII exemption/transition logic thin."),
    "Q-C03": ("no", "Residential-status day-count logic incorrect (misapplied 182-day test); RNOR computation not delivered."),
}

ORDER = {
    "Easy": ["Q-E01", "Q-E02", "Q-E03", "Q-E04", "Q-E05"],
    "Medium": ["Q-M01", "Q-M02", "Q-M03", "Q-M04", "Q-M05"],
    "Complex": ["Q-C01", "Q-C02", "Q-C03"],
}


def cell(text: str, limit: int = 400) -> str:
    """Flatten an answer to a single Markdown table cell, truncated."""
    one = " ".join(text.split())
    if len(one) > limit:
        one = one[:limit].rstrip() + "…"
    return one.replace("|", "\\|")


def table(section: str) -> str:
    rows = [
        "| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |",
        "|----|----------|--------------|---------------------------|----------------|---------------|",
    ]
    for qid in ORDER[section]:
        a = answers[qid]
        verdict, note = VERDICTS[qid]
        rows.append(
            f"| {qid} | {cell(a['question'], 300)} | {cell(a['answer'])} | {verdict} | {note} | {a['sources']} |"
        )
    return "\n".join(rows)


HEADER = """# TITO Test Results — APICN008

- Date tested: 2026-11-05
- LLM_PROVIDER: slm
- LLM_MODEL: qwen2.5:3b (Ollama, local)
- Retrieved top-k: 5
- Vector store: BM25 (in-memory, built by src/rag/ingest.py)

> Answers below are the bot's **verbatim** output (truncated to ~400 chars with …).
> "Correct?" is our honest self-assessment after reviewing each answer against the
> corpus and standard Indian tax facts. This run uses a small 3B local SLM on a
> CPU-only laptop; switching `LLM_PROVIDER=groq` (llama-3.3-70b) in `.env`
> materially improves the medium/complex computations without any code change.
"""

FOOTER_WORKING = """
<details><summary>Q-M01 working (verbatim)</summary>

{m01}

</details>

<details><summary>Q-C01 working (verbatim, truncated by model token limit)</summary>

{c01}

</details>
"""

VIVO_NOTES = """
## VIVO integration notes

| Demo file | Question ID | Transcript captured? (yes/no) | Answer audible? (yes/no/partial) | Follow-up handled? | Note |
|-----------|-------------|-------------------------------|-----------------------------------|--------------------|------|
| demo/vivo_0.mp3 | free choice | TODO record | TODO | TODO | free-choice demo with a follow-up (multi-turn) |
| demo/vivo_1.mp3 | Q-E01 | TODO | TODO | n/a | |
| demo/vivo_2.mp3 | Q-E02 | TODO | TODO | n/a | |
| demo/vivo_3.mp3 | Q-E05 | TODO | TODO | n/a | |
| demo/vivo_4.mp3 | Q-M01 | TODO | TODO | n/a | |
| demo/vivo_5.mp3 | Q-M04 | TODO | TODO | n/a | |
| demo/vivo_6.mp3 | Q-C01 | TODO | TODO | n/a | |
| demo/vivo_7.mp3 | Q-C03 | TODO | TODO | n/a | |

> Demo recordings require speaking to the running bot on your hardware; record them
> with `python src/app.py --mode vivo`. See demo/README.md.

## TIVO / VITO availability

- TIVO: `python src/app.py --mode tivo` — typed question, spoken answer.
- VITO: `python src/app.py --mode vito` or the Voice tab of `python src/app.py --ui web` — spoken question, typed answer with the transcript shown.
"""


def main() -> None:
    doc = [
        HEADER,
        "## Easy\n\n" + table("Easy"),
        "## Medium\n\n" + table("Medium"),
        "## Complex\n\n" + table("Complex"),
        FOOTER_WORKING.format(
            m01=answers["Q-M01"]["answer"], c01=answers["Q-C01"]["answer"]
        ),
        VIVO_NOTES,
    ]
    (ROOT / "report" / "test_results.md").write_text("\n\n".join(doc), encoding="utf-8")
    print("Wrote report/test_results.md")

    # Summary for the user
    tally = {"yes": 0, "partial": 0, "no": 0}
    for v, _ in VERDICTS.values():
        tally[v] += 1
    print(f"Self-assessment tally: {tally}")


if __name__ == "__main__":
    main()
