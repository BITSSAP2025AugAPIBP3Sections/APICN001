# TITO Test Results — APICN008

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


## Easy

| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |
|----|----------|--------------|---------------------------|----------------|---------------|
| Q-E01 | What are the income tax slab rates for an individual under the new regime for FY 2024-25 (AY 2025-26)? | I cannot find this information in the provided corpus. | no | Slabs exist in bs2024_25.pdf but retrieval surfaced FAQ pages instead; bot refused. Retrieval miss, not hallucination. | Updated-FQAs-on-Interplay&Transitions.pdf p.11; bs2025_26.pdf p.32; Updated-FQAs-on-Interplay&Transitions.pdf p.33; Updated-FQAs-on-Interplay&Transitions.pdf p.43; Updated-FQAs-on-Interplay&Transitions.pdf p.82 |
| Q-E02 | What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investments? | According to the provided context, Section 80C of the Income-tax Act, 1961 allows an aggregate deduction of Rs 1.5 lakh for specified savings instruments for individuals or HUF. The eligible instruments are now placed in Schedule XV, but the nature of qualifying payments such as life insurance, provident fund, tuition fees, etc., remains unchanged. Three eligible investments under Section 80C are:… | yes | Rs 1.5 lakh cap + LIC/PF/tuition correct and grounded. | bs2024_25.pdf p.61; Updated-FQAs-on-Interplay&Transitions.pdf p.78; bs202223.pdf p.27 |
| Q-E03 | What is the basic exemption limit for a resident individual under 60 years of age under the old regime? | I cannot find this in the provided corpus. | partial | Old-regime Rs 2.5 lakh limit is not clearly in this budget-centric corpus; honest refusal. | Updated-FQAs-on-Interplay&Transitions.pdf p.38; Updated-FQAs-on-Interplay&Transitions.pdf p.87; bs2023_24.pdf p.37; bs2023_24.pdf p.39 |
| Q-E04 | What is the standard deduction available to a salaried employee under the new tax regime for FY 2024-25? | (.bs2024_25.pdf, p.32) The standard deduction for salaried employees is proposed to be increased from ₹50,000/- to ₹75,000/-. | yes | Rs 75,000 standard deduction, correctly cited (bs2024_25.pdf p.32). | bs2024_25.pdf p.32; bs2024_25.pdf p.54; bs2023_24.pdf p.38; bs2023_24.pdf p.39 |
| Q-E05 | What is the tax rate applicable to income from capital gains on listed equity shares held for more than 12 months (long-term capital gains) as per the latest budget? | According to the latest budget as provided in the document (bs2024_25.pdf, p.56), the tax rate applicable to income from capital gains on listed equity shares held for more than 12 months (long-term capital gains) is 12.5%. | yes | 12.5% LTCG matches Budget 2024-25, cited. | FAQs-on-BIS-Exemption.pdf p.2; bs2024_25.pdf p.56; bs2024_25.pdf p.30; bs202223.pdf p.28 |

## Medium

| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |
|----|----------|--------------|---------------------------|----------------|---------------|
| Q-M01 | A salaried individual earns ₹18,00,000 gross annual salary in FY 2024-25, contributes ₹1,50,000 to EPF, pays ₹50,000 NPS Tier-1, and has ₹25,000 health insurance premium. Compute tax under the new regime (assume no other deductions, standard deduction applies). | To compute the tax under the new regime for a salaried individual earning ₹18,00,000 gross annual salary in FY 2024-25, we need to apply the tax slabs and rates provided in the document. The individual also contributes ₹1,50,000 to EPF and ₹50,000 to NPS Tier-1, and has a ₹25,000 health insurance premium. The standard deduction for salaried individuals is ₹75,000 under the new regime. Given: - Tot… | no | Correctly found 75k std deduction but applied a flat 25% to the whole income instead of slab-wise; final figure wrong. | bs2024_25.pdf p.54; bs2023_24.pdf p.39; bs2024_25.pdf p.32; bs202223.pdf p.26; bs2025_26.pdf p.50 |
| Q-M02 | I bought a residential property for ₹80,00,000 in 2018 and sold it in FY 2024-25 for ₹1,20,00,000. Compute the capital gains tax due (you may state your assumptions on indexation clearly). | I cannot find this in the provided corpus. | partial | Property indexation detail not in corpus; refusal is defensible but no computation attempted. | bs202223.pdf p.36; bs2025_26.pdf p.51; bs2025_26.pdf p.50; bs2023_24.pdf p.39; bs2023_24.pdf p.44 |
| Q-M03 | An individual transfers ₹12,00,000 in a financial year under the Liberalised Remittance Scheme (LRS) for foreign education. What is the TCS rate that applies after the FY 2023-24 changes to Section 206C, and what exemption applies? | For the FY 2023-24 changes to Section 206C, the TCS rate for foreign remittances for the purpose of education under LRS is proposed to be 20% for remittances in excess of ₹7 lakh. There is no specific exemption mentioned for this scenario in the provided corpus. Therefore, the TCS rate applicable would be 20%, and no exemption applies. | partial | 20% TCS rate correct; missed the education-via-loan 0.5% nuance and the Rs 7 lakh threshold framing. | bs2025_26.pdf p.51; bs2025_26.pdf p.53; bs2023_24.pdf p.44; bs2025_26.pdf p.28 |
| Q-M04 | What are the provisions for taxation of Virtual Digital Assets (cryptocurrency) under Section 115BBH, including the rate, the loss set-off rule, and the TDS under Section 194S? | I cannot find this in the provided corpus. | no | 115BBH/194S crypto provisions are in bs202223.pdf; retrieval under-grounded and bot refused. | bs202223.pdf p.27; Updated-FQAs-on-Interplay&Transitions.pdf p.18; bs202223.pdf p.29; Updated-FQAs-on-Interplay&Transitions.pdf p.76; Updated-FQAs-on-Interplay&Transitions.pdf p.59 |
| Q-M05 | A taxpayer has both salary income and house property income (one self-occupied house with home-loan interest of ₹2,00,000). Under which regime (old vs new) would their tax be lower, and why? Assume gross total income of ₹15,00,000, all of it except the interest deduction being salary. | To determine under which regime (old vs new) the taxpayer's tax would be lower, we need to calculate the tax liability under both the old and new tax regimes for the given gross total income of ₹15,00,000, considering the salary income and house property income. ### New Regime: The new tax regime has the following slabs and rates: - Upto ₹3,00,000: 0% - ₹3,00,001 to ₹7,00,000: 5% - ₹7,00,001 to ₹1… | no | Slab arithmetic garbled (wrong band widths); regime recommendation direction plausible but numbers wrong. | bs2023_24.pdf p.39; bs2024_25.pdf p.54; bs2025_26.pdf p.50; bs2023_24.pdf p.40; bs2023_24.pdf p.43 |

## Complex

| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |
|----|----------|--------------|---------------------------|----------------|---------------|
| Q-C01 | Mr. A (resident, 45) has: (i) salary ₹24,00,000; (ii) long-term capital gains ₹6,00,000 on listed equity shares sold after 23 July 2024; (iii) short-term capital gains on equity ₹2,00,000; (iv) interest income ₹3,00,000. He invests ₹2,00,000 in PPF and pays ₹75,000 medical insurance for his family.… | To compute Mr. A's tax liability under both the old and new Income Tax Acts, we need to follow the tax slabs and surcharges as per the provided documents. However, the specific surcharge and cess rates for the new Act are not provided in the given excerpts. Therefore, I will calculate the tax liability under the old Act (1961) and the new Act (2025) based on the provided information. ### Old Act (… | no | Answer truncated/looped with invented slab bands; no valid surcharge/cess computation. | bs202223.pdf p.28; FAQs-on-BIS-Exemption.pdf p.2; FAQs-on-BIS-Exemption.pdf p.1; Updated-FQAs-on-Interplay&Transitions.pdf p.93; Updated-FQAs-on-Interplay&Transitions.pdf p.76 |
| Q-C02 | A non-resident FII earned ₹50,00,000 from Indian listed securities in FY 2024-25. Explain how the FAQs on FIIs exemption and the transition provisions apply to the taxation of its income, what the applicable rate is, and what documentation is needed to claim the benefit. | Based on the provided FAQ excerpts, for a non-resident FII earning ₹50,00,000 from Indian listed securities in FY 2024-25, the applicable tax rate would be 20% under section 210(1) of the Income-tax Act, 2025. The income from securities is taxable at this rate. There is no specific mention of exemptions or concessional taxation for listed securities in the provided FAQ excerpts. Therefore, no addi… | partial | Mentions 20% rate but cites a non-existent 'section 210(1)'; FII exemption/transition logic thin. | FAQs-on-BIS-Exemption.pdf p.1; bs2024_25.pdf p.56 |
| Q-C03 | Compare the treatment of "days of stay" for determining residential status for an individual with Indian income of ₹40,00,000 who visited India for 130 days across two visits in a year, referencing the transition/deeming provisions. Then compute the tax consequence if the person is deemed resident b… | To compare the treatment of "days of stay" for determining residential status for an individual with Indian income of ₹40,00,000 who visited India for 130 days across two visits in a year, we need to refer to the provisions of the Income-tax Act, 1961 and the Income-tax Act, 2025. From the provided context, we understand that residential status is determined based on the days of stay in India. For… | no | Residential-status day-count logic incorrect (misapplied 182-day test); RNOR computation not delivered. | Updated-FQAs-on-Interplay&Transitions.pdf p.89; Updated-FQAs-on-Interplay&Transitions.pdf p.87; Updated-FQAs-on-Interplay&Transitions.pdf p.88 |


<details><summary>Q-M01 working (verbatim)</summary>

To compute the tax under the new regime for a salaried individual earning ₹18,00,000 gross annual salary in FY 2024-25, we need to apply the tax slabs and rates provided in the document. The individual also contributes ₹1,50,000 to EPF and ₹50,000 to NPS Tier-1, and has a ₹25,000 health insurance premium. The standard deduction for salaried individuals is ₹75,000 under the new regime.

Given:
- Total income (before deductions) = ₹18,00,000
- Standard deduction = ₹75,000
- EPF contribution = ₹1,50,000
- NPS Tier-1 contribution = ₹50,000
- Health insurance premium = ₹25,000

Total deductions = Standard deduction + EPF contribution + NPS Tier-1 contribution + Health insurance premium
Total deductions = ₹75,000 + ₹1,50,000 + ₹50,000 + ₹25,000 = ₹2,50,000

Adjusted income = Total income - Total deductions
Adjusted income = ₹18,00,000 - ₹2,50,000 = ₹15,50,000

Now, applying the tax slabs:
- Rate of tax: 5% for income up to ₹3,00,000
- Rate of tax: 10% for income from ₹3,00,001 to ₹7,00,000
- Rate of tax: 15% for income from ₹7,00,001 to ₹10,00,000
- Rate of tax: 20% for income from ₹10,00,001 to ₹12,00,000
- Rate of tax: 25% for income from ₹12,00,001 to ₹15,00,000
- Rate of tax: 30% for income above ₹15,00,000

Since the adjusted income is ₹15,50,000, it falls under the 25% tax slab.

Tax calculation:
Tax = Adjusted income × Rate of tax
Tax = ₹15,50,000 × 25/100
Tax = ₹3,87,500

Therefore, the tax under the new regime for the salaried individual in FY 2024-25 is ₹3,87,500.

</details>

<details><summary>Q-C01 working (verbatim, truncated by model token limit)</summary>

To compute Mr. A's tax liability under both the old and new Income Tax Acts, we need to follow the tax slabs and surcharges as per the provided documents. However, the specific surcharge and cess rates for the new Act are not provided in the given excerpts. Therefore, I will calculate the tax liability under the old Act (1961) and the new Act (2025) based on the provided information.

### Old Act (1961) Tax Calculation:

#### Step 1: Calculate Gross Total Income
- Salary: ₹24,00,000
- Long-term capital gains: ₹6,00,000
- Short-term capital gains: ₹2,00,000
- Interest income: ₹3,00,000
- PPF investment: ₹2,00,000 (not taxable)
- Medical insurance: ₹75,000 (not taxable)

Total Gross Income = ₹24,00,000 + ₹6,00,000 + ₹2,00,000 + ₹3,00,000 = ₹35,00,000

#### Step 2: Calculate Taxable Income
- Medical insurance: ₹75,000 (not taxable)
- PPF investment: ₹2,00,000 (not taxable)

Total Taxable Income = ₹35,00,000 - ₹75,000 - ₹2,00,000 = ₹26,25,000

#### Step 3: Calculate Tax Liability
- Income up to ₹1,50,000: 0%
- Income from ₹1,50,001 to ₹5,00,000: 7%
- Income from ₹5,00,001 to ₹10,00,000: 20%
- Income from ₹10,00,001 to ₹15,00,000: 40%
- Income from ₹15,00,001 to ₹20,00,000: 45%
- Income from ₹20,00,001 to ₹30,00,000: 45%
- Income from ₹30,00,001 to ₹40,00,000: 45%
- Income from ₹40,00,001 to ₹50,00,000: 45%
- Income from ₹50,00,001 to ₹60,00,000: 45%
- Income from ₹60,00,001 to ₹70,00,000: 45%
- Income from ₹70,00,001 to ₹80,00,000: 45%
- Income from ₹80,00,001 to ₹90,00,000: 45%
- Income from ₹90,00,001 to ₹100,00,000: 45%
- Income from ₹100,00,001 to ₹12,00,000: 45%
- Income from ₹12,00,001 to ₹15,00,000: 45%
- Income from ₹15,00,001 to ₹20,00,

</details>



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
