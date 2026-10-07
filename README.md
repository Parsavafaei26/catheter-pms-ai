# AI-assisted post-market surveillance for long-term central venous catheters

A validated prototype that uses a large language model to classify FDA MAUDE adverse event
reports by failure mode, severity and phase of use, and feeds the results back into an
ISO 14971-style FMEA.

**[Read the full report](REPORT.md)**

## Key results

- **80%** of complaints carrying the FDA code "Fluid/Blood Leak" actually describe a
  **catheter body break** when the narrative is read.
- Catheter body breaks rose from **28% to 54%** of complaints between 2023 and 2025.
- A leak and air-entry cluster at the stylet septum appeared in 2023 and faded by 2025.
- Insertion accessories, air entry, kinking, malposition and harm to users were missing from
  the reference design FMEA.
- **Validation against blind expert coding (100 reports):** failure mode 93% agreement
  (Cohen's kappa 0.90). Severity rose from 61% to 85% agreement after a rule fix and an
  independent re-run.

![Failure mode trend](figures/fig2_failure_mode_trend.png)

## Intended use

Decision support for PMS trend review. Not for reportability decisions, incidence rates or
clinical decisions. Severity ratings and serious events are always reviewed by a person.
See [docs/01_intended_use.md](docs/01_intended_use.md).

## How it works

| Step | What | Where |
|---|---|---|
| 1 | Intended use and scope | `docs/01_intended_use.md` |
| 2 | Extract MAUDE reports (openFDA, product code LJS, 2023-2025) | `scripts/fetch_maude.py`, `docs/03_data_summary.md` |
| 3 | Failure-mode categories and coding rules, reviewed against an FMEA | `docs/02_failure_mode_categories.md` |
| 4 | AI classification of 300 reports | `docs/04_classification_method.md`, `docs/05_ai_classification_results.md` |
| 5 | Blind validation, root-cause fix and independent re-test | `docs/06_validation_results.md` |
| 6 | Figures and FMEA comparison | `figures/`, `docs/07_fmea_comparison.md` |
| 7 | Report and reusable Claude skill | `REPORT.md`, `skill/maude-pms-coder/` |

## Reproduce

Python 3 with `openpyxl` and `matplotlib`.

```
python3 scripts/fetch_maude.py --from-json data/raw/page*.json   # build the report CSV
python3 scripts/prepare_batches.py select                          # draw the coding sample
python3 scripts/compare_validation.py                              # AI vs human agreement
python3 scripts/make_figures.py                                    # figures
```

## Data

U.S. FDA MAUDE via openFDA (public domain). MAUDE is subject to under-reporting, missing
information and duplicates, contains allegations rather than confirmed causes, and cannot be
used to calculate event rates. Results must not be used to compare manufacturers.

## Author

Parsa Vafaei, MSc Biomedical Engineering · Regulatory affairs and quality
