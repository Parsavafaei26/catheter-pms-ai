# 3. Data summary

*October 2026. Source: openFDA device adverse event API (MAUDE), product code LJS, reports received 1 Jan 2023 to 31 Dec 2025. Data last updated by FDA on 29 Sep 2026.*

## What was collected

| File | Contents |
|---|---|
| `data/raw/page1-16.json` | Raw openFDA downloads, saved from the browser |
| `data/processed/maude_reports.csv` | All 1,600 downloaded reports, one row each |
| `data/processed/maude_balanced_sample.csv` | 1,200 reports: 100 per quarter (Q1 2023 randomly cut from 500 to 100, seed 42) |
| `data/processed/quarterly_totals.csv` | Total number of LJS reports in MAUDE for every quarter (full population, from openFDA) |

The balanced sample is used for the analysis, so each quarter has equal weight.

## Full population: reports per quarter

These are counts of **all** 11,466 LJS reports, not just the sample.

| Quarter | Reports | Quarter | Reports | Quarter | Reports |
|---|---|---|---|---|---|
| 2023-Q1 | 537 | 2024-Q1 | 790 | 2025-Q1 | 1,311 |
| 2023-Q2 | 755 | 2024-Q2 | 952 | 2025-Q2 | 1,038 |
| 2023-Q3 | 856 | 2024-Q3 | 1,105 | 2025-Q3 | 1,113 |
| 2023-Q4 | 651 | 2024-Q4 | 1,396 | 2025-Q4 | 962 |
| **2023** | **2,799** | **2024** | **4,243** | **2025** | **4,424** |

Reports rose by about half from 2023 to 2024 and stayed high in 2025, peaking in late 2024. A rise
in reports does **not** mean devices got worse: it can reflect more devices sold, changes in
manufacturer reporting practice, a recall or field action raising awareness, or batch
submission of older reports. This is something PMS review would investigate, not conclude.

## Balanced sample: first look (FDA problem codes, % of reports)

| Year | Leak | Break / fracture / crack / separation | Deformation / kink | Injury or death | Largest manufacturer share |
|---|---|---|---|---|---|
| 2023 | 34% | 18% | 10% | 12% | 81% |
| 2024 | 54% | 16% | 8% | 8% | 82% |
| 2025 | 51% | 14% | 14% | 10% | 84% |

A report can carry more than one problem code, so rows do not add to 100%.

The rise in leak reports from 2023 to 2024 is the first signal worth checking in the AI
classification step: is it leaks from the catheter body, or from hubs and extension legs?

## Known limitations of this sample

- **Within-quarter clustering:** each link returned the first 100 reports of its quarter, so the sample is concentrated in the first month of each quarter.
- **Manufacturer concentration:** about 80% of reports come from one manufacturer group. This probably reflects market share and reporting practice. Manufacturers will not be compared.
- **Duplicates:** 37 reports share identical text with another report (e.g. one event involving four patients filed as four reports). To be flagged during classification.
- **Midline catheters:** 10 reports mention midline catheters, which are not central lines. Inclusion to be decided.
- General MAUDE limitations: under-reporting, missing details, no denominator data, reports are allegations not confirmed causes.
