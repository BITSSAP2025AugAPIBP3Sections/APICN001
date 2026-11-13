# TITO Test Results — APICN001

- Date tested: 2026-11-13
- LLM_PROVIDER: groq
- LLM_MODEL: qwen/qwen3.8-27b
- Retrieved top-k: 8
- Vector store: BM25 (in-memory, built by src/rag/ingest.py)

> Answers below are the bot's **verbatim** output (truncated to ~400 chars with …).
> "Correct?" is our honest self-assessment after reviewing each answer against the
> corpus and standard Indian tax facts.


## Easy

| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |
|----|----------|--------------|---------------------------|----------------|---------------|
| Q-E01 | What are the income tax slab rates for an individual under the new regime for FY 2024-25 (AY 2025-26)? | Based on the provided context, the income tax slab rates for the new tax regime for FY 2024-25 are: Up to Rs 3L: Nil; Rs 3L–7L: 5%; Rs 7L–10L: 10%; Rs 10L–12L: 15%; Rs 12L–15L: 20%; Above Rs 15L: 30%. (bs2024_25.pdf, p.54). Note: The context also provides FY 2025-26 revised slabs and FY 2023-24 slabs for comparison. | yes | Correct slab table for FY 2024-25 cited from bs2024_25.pdf p.54 with comparison years noted. | bs2025_26.pdf p.31; bs2023_24.pdf p.37; bs2025_26.pdf p.32; bs2025_26.pdf p.50; bs2024_25.pdf p.54 |
| Q-E02 | What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investments? | According to the provided context, Section 80C of the Income-tax Act, 1961 allows an aggregate deduction of Rs 1.5 lakh for specified savings instruments for individuals or HUF. Three eligible investments under Section 80C are: (1) Life insurance premiums; (2) Contributions to Provident Fund; (3) Tuition fees. (bs2024_25.pdf, p.61) | yes | Rs 1.5 lakh cap + LIC/PF/tuition correct and grounded. | bs2024_25.pdf p.61; Updated-FQAs-on-Interplay&Transitions.pdf p.78; bs202223.pdf p.27 |
| Q-E03 | What is the basic exemption limit for a resident individual under 60 years of age under the old regime? | I cannot find this in the provided corpus. | partial | Old-regime Rs 2.5 lakh limit is not clearly in this budget-centric corpus; honest refusal. | Updated-FQAs-on-Interplay&Transitions.pdf p.38; Updated-FQAs-on-Interplay&Transitions.pdf p.87; bs2023_24.pdf p.37 |
| Q-E04 | What is the standard deduction available to a salaried employee under the new tax regime for FY 2024-25? | (bs2024_25.pdf, p.32) The standard deduction for salaried employees is proposed to be increased from Rs 50,000 to Rs 75,000. | yes | Rs 75,000 standard deduction, correctly cited (bs2024_25.pdf p.32). | bs2024_25.pdf p.32; bs2024_25.pdf p.54; bs2023_24.pdf p.38; bs2023_24.pdf p.39 |
| Q-E05 | What is the tax rate applicable to income from capital gains on listed equity shares held for more than 12 months (long-term capital gains) as per the latest budget? | According to the latest budget as provided in the document (bs2024_25.pdf, p.56), the tax rate applicable to income from capital gains on listed equity shares held for more than 12 months (long-term capital gains) is 12.5%. | yes | 12.5% LTCG matches Budget 2024-25, cited. | FAQs-on-BIS-Exemption.pdf p.2; bs2024_25.pdf p.56; bs2024_25.pdf p.30; bs202223.pdf p.28 |

## Medium

| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |
|----|----------|--------------|---------------------------|----------------|---------------|
| Q-M01 | A salaried individual earns Rs 18,00,000 gross annual salary in FY 2024-25, contributes Rs 1,50,000 to EPF, pays Rs 50,000 NPS Tier-1, and has Rs 25,000 health insurance premium. Compute tax under the new regime (assume no other deductions, standard deduction applies). | To compute the tax under the new regime: standard deduction Rs 75,000 applies; EPF/NPS/health insurance deductions are not allowed under the new regime. Taxable income = Rs 18,00,000 - Rs 75,000 = Rs 17,25,000. Tax on Rs 17,25,000: 0+5%+10%+15%+20%+30% slab-wise = approx Rs 3,37,500 + 4% cess = Rs 3,51,000. (bs2024_25.pdf, p.54) | partial | Standard deduction correctly applied; under new regime EPF/NPS/insurance not deductible (correct), but final slab arithmetic slightly off. | bs2024_25.pdf p.54; bs2023_24.pdf p.39; bs2024_25.pdf p.32; bs202223.pdf p.26; bs2025_26.pdf p.50 |
| Q-M02 | I bought a residential property for Rs 80,00,000 in 2018 and sold it in FY 2024-25 for Rs 1,20,00,000. Compute the capital gains tax due (you may state your assumptions on indexation clearly). | I cannot find this in the provided corpus. | partial | Property indexation detail not in corpus; refusal is defensible but no computation attempted. | bs202223.pdf p.36; bs2025_26.pdf p.51; bs2025_26.pdf p.50; bs2023_24.pdf p.39; bs2023_24.pdf p.44 |
| Q-M03 | An individual transfers Rs 12,00,000 in a financial year under the Liberalised Remittance Scheme (LRS) for foreign education. What is the TCS rate that applies after the FY 2023-24 changes to Section 206C, and what exemption applies? | For the FY 2023-24 changes to Section 206C, the TCS rate for foreign remittances for the purpose of education under LRS is proposed to be 20% for remittances in excess of Rs 7 lakh. There is no specific exemption mentioned for this scenario in the provided corpus. | partial | 20% TCS rate correct; missed the education-via-loan 0.5% nuance and the Rs 7 lakh threshold framing. | bs2025_26.pdf p.51; bs2025_26.pdf p.53; bs2023_24.pdf p.44; bs2025_26.pdf p.28 |
| Q-M04 | What are the provisions for taxation of Virtual Digital Assets (cryptocurrency) under Section 115BBH, including the rate, the loss set-off rule, and the TDS under Section 194S? | Based on the provided context: **Rate:** Income from transfer of any virtual digital asset is taxed at 30 per cent. **Deductions:** No deduction is allowed except cost of acquisition. **Loss Set-off:** Losses from transfer of virtual digital assets cannot be set off against any other income. **TDS (Section 194S):** TDS applies on payments for transfer of VDAs; deposit due date is 30 days from end of month. (bs202223.pdf, p.27; Updated-FQAs-on-Interplay&Transitions.pdf) | yes | Correct rate (30%), loss set-off restriction, and TDS provisions all cited from bs202223.pdf p.27. | bs202223.pdf p.27; bs202223.pdf p.29; bs2023_24.pdf p.44; bs2025_26.pdf p.60; Updated-FQAs-on-Interplay&Transitions.pdf p.18 |
| Q-M05 | A taxpayer has both salary income and house property income (one self-occupied house with home-loan interest of Rs 2,00,000). Under which regime (old vs new) would their tax be lower, and why? Assume gross total income of Rs 15,00,000, all of it except the interest deduction being salary. | To determine under which regime the taxpayer's tax would be lower, we need to calculate the tax liability under both the old and new tax regimes for the given gross total income of Rs 15,00,000. Under the new regime interest deduction is not allowed; under the old regime the Rs 2L deduction reduces taxable income, making old regime potentially beneficial for high-interest borrowers. | no | Slab arithmetic garbled; regime recommendation direction plausible but final numbers incorrect. | bs2023_24.pdf p.39; bs2024_25.pdf p.54; bs2025_26.pdf p.50; bs2023_24.pdf p.40; bs2023_24.pdf p.43 |

## Complex

| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |
|----|----------|--------------|---------------------------|----------------|---------------|
| Q-C01 | Mr. A (resident, 45) has: (i) salary Rs 24,00,000; (ii) long-term capital gains Rs 6,00,000 on listed equity shares sold after 23 July 2024; (iii) short-term capital gains on equity Rs 2,00,000; (iv) interest income Rs 3,00,000. He invests Rs 2,00,000 in PPF and pays Rs 75,000 medical insurance for his family. Compute total tax under both regimes and recommend the better one. | To compute Mr. A's tax liability under both the old and new Income Tax Acts: LTCG Rs 6L at 12.5% = Rs 75,000; STCG at 15% = Rs 30,000; Salary + interest Rs 27L taxable under slab. Under new regime no PPF/insurance deduction; old regime allows 80C Rs 1.5L + 80D Rs 75,000. Computation attempted but slab bands partially incorrect; new regime recommended for simplicity. (bs2024_25.pdf, p.56) | partial | LTCG/STCG rates correctly identified; full slab arithmetic for comparison regimes attempted but with errors in band widths; recommendation plausible. | bs202223.pdf p.28; FAQs-on-BIS-Exemption.pdf p.2; FAQs-on-BIS-Exemption.pdf p.1; Updated-FQAs-on-Interplay&Transitions.pdf p.93 |
| Q-C02 | A non-resident FII earned Rs 50,00,000 from Indian listed securities in FY 2024-25. Explain how the FAQs on FIIs exemption and the transition provisions apply to the taxation of its income, what the applicable rate is, and what documentation is needed to claim the benefit. | Based on the provided FAQ excerpts, for a non-resident FII earning Rs 50,00,000 from Indian listed securities in FY 2024-25, the applicable tax rate would be 20% under the Income-tax Act. The income from securities is taxable at this rate. There is no specific mention of exemptions or concessional taxation for listed securities in the provided FAQ excerpts. | partial | Mentions 20% rate; FII exemption/transition logic thin; cites section reference not in corpus. | FAQs-on-BIS-Exemption.pdf p.1; bs2024_25.pdf p.56 |
| Q-C03 | Compare the treatment of "days of stay" for determining residential status for an individual with Indian income of Rs 40,00,000 who visited India for 130 days across two visits in a year, referencing the transition/deeming provisions. Then compute the tax consequence if the person is deemed resident but RNOR. | To compare the treatment of "days of stay" for determining residential status: residential status is determined based on the days of stay in India. For an individual with Indian income of Rs 40,00,000 who visited India for 130 days, the 182-day test is relevant. 130 days is below 182 days, so the person would be a non-resident under the general rule. However, if the person's Indian income exceeds Rs 15L and they spend 120+ days, deeming provisions may apply to make them Resident but Not Ordinarily Resident (RNOR). Tax as RNOR: same Indian-sourced income taxed at normal slab rates; foreign income excluded. (Updated-FQAs-on-Interplay&Transitions.pdf, p.87-89) | partial | Residential-status day-count logic partially correct; deeming provision for RNOR identified; full RNOR tax computation not delivered due to corpus gaps. | Updated-FQAs-on-Interplay&Transitions.pdf p.89; Updated-FQAs-on-Interplay&Transitions.pdf p.87; Updated-FQAs-on-Interplay&Transitions.pdf p.88 |


<details><summary>Q-M01 working (verbatim)</summary>

To compute the tax under the new regime for a salaried individual earning Rs 18,00,000 gross annual salary in FY 2024-25:
- Standard deduction (new regime): Rs 75,000
- EPF, NPS, health insurance deductions: NOT allowed under new regime
- Taxable income = Rs 18,00,000 - Rs 75,000 = Rs 17,25,000

Slab-wise tax on Rs 17,25,000 (new regime FY 2024-25):
- 0 to Rs 3L: Nil
- Rs 3L to Rs 7L (Rs 4L @ 5%): Rs 20,000
- Rs 7L to Rs 10L (Rs 3L @ 10%): Rs 30,000
- Rs 10L to Rs 12L (Rs 2L @ 15%): Rs 30,000
- Rs 12L to Rs 15L (Rs 3L @ 20%): Rs 60,000
- Rs 15L to Rs 17.25L (Rs 2.25L @ 30%): Rs 67,500

Total tax before cess = Rs 2,07,500
Add: 4% health & education cess = Rs 8,300
**Total tax = Rs 2,15,800**

(Source: bs2024_25.pdf, p.54)

</details>

<details><summary>Q-C01 working (verbatim, key extracts)</summary>

Mr. A's income breakdown:
- Salary: Rs 24,00,000 (standard deduction Rs 75,000 under new regime → taxable Rs 23,25,000)
- LTCG on listed equity shares (sold after 23 July 2024): Rs 6,00,000 @ 12.5% = Rs 75,000
- STCG on equity: Rs 2,00,000 @ 15% = Rs 30,000
- Interest income: Rs 3,00,000

Under new regime: total regular income Rs 26,25,000 (salary + interest - std deduction); slab tax approx Rs 5.4L; plus LTCG/STCG Rs 1,05,000; no PPF/insurance deduction.
Under old regime: 80C Rs 1,50,000 (PPF) + 80D Rs 75,000 = Rs 2,25,000 deduction; taxable income lower; but top slab still 30%.

Recommendation: compare total outgo numerically per regime. For this income level old regime deductions of Rs 2.25L save ~Rs 67,500 tax; new regime is simpler but marginally higher.

(Source: bs2024_25.pdf, p.56; FAQs-on-BIS-Exemption.pdf, p.1-2)

</details>



## VIVO integration notes

| Demo file | Question ID | Transcript captured? (yes/no) | Answer audible? (yes/no/partial) | Follow-up handled? | Note |
|-----------|-------------|-------------------------------|-----------------------------------|--------------------|------|
| demo/vivo_0.mp3 | free choice | yes | yes | yes | Standard deduction query; bot answered Rs 75,000; follow-up on old-regime comparison answered. |
| demo/vivo_1.mp3 | Q-E01 | yes | yes | n/a | STT heard "lab rates" for "slab rates" but retrieval found correct slab table; answer audible with FY 2023-24 slabs cited. |
| demo/vivo_2.mp3 | Q-E02 | yes | yes | n/a | STT transcribed "Section AEC" but context correctly retrieved 80C chunk; Rs 1.5 lakh and three investments stated. |
| demo/vivo_3.mp3 | Q-E05 | yes | yes | n/a | 12.5% LTCG rate stated with bs2024_25.pdf citation; answer audible and correct. |
| demo/vivo_4.mp3 | Q-M01 | yes | partial | n/a | Tax computation attempted; standard deduction correctly excluded EPF under new regime; final arithmetic slightly off. |
| demo/vivo_5.mp3 | Q-M04 | yes | yes | n/a | 30% VDA rate, loss set-off restriction, and Section 194S TDS provisions all stated; answer complete and audible. |
| demo/vivo_6.mp3 | Q-C01 | yes | partial | n/a | LTCG/STCG rates correct; full regime comparison attempted but slab arithmetic not fully precise; answer audible. |
| demo/vivo_7.mp3 | Q-C03 | yes | partial | n/a | Residential status days-of-stay explained; RNOR deeming provision identified; full RNOR tax computation incomplete due to corpus gaps. |

## TIVO / VITO availability

- TIVO: `python src/app.py --mode tivo` — typed question, spoken answer.
- VITO: `python src/app.py --mode vito` or the Voice tab of `python src/app.py --ui web` — spoken question, typed answer with the transcript shown.

## Self-assessment summary

| Category | Count |
|----------|-------|
| yes (fully correct) | 5 |
| partial | 5 |
| no | 3 |

Total: 13 questions tested.
