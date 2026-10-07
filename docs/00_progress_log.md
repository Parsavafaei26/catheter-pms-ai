# Progress log

## 6 October 2026

**Step 1: Intended use (draft done)**
- Wrote `docs/01_intended_use.md`: purpose, intended user, what the tool is not for, human oversight, scope, data limitations.

**Step 2: Data extraction (first batch done)**
- Wrote `scripts/fetch_maude.py` to download openFDA reports or convert saved JSON files into one CSV.
- Direct download from the FDA API is blocked by the Claude network settings, so pages were saved by hand from the browser.
- Saved 5 pages (500 reports) into `data/raw/` and converted them to `data/processed/maude_reports.csv`.
- Confirmed product code LJS = "catheter, intravascular, therapeutic, long-term greater than 30 days" (PICCs, Broviac, Groshong, etc.).

First look at the 500 reports:
- 443 malfunctions, 55 injuries, 2 deaths.
- Most common FDA problem codes: fluid/blood leak (266), material deformation (159), defective component (102), break/fracture/crack (190 combined).
- Every report has a narrative (median about 430 characters).

Issues found:
- **Time bias:** all 500 reports were received January to March 2023, while 11,466 reports exist for 2023-2025. A trend claim needs data from across the period. Fix: one page per quarter (`data/download_links.md`).
- **Manufacturer concentration:** 73% of reports are from one manufacturer (C.R. Bard). This may reflect market share and reporting practice rather than device quality, so results will not be compared between manufacturers.
- **Duplicates:** some events appear more than once (e.g. one event involving four patients reported as four records). To be handled in the analysis.

**Step 3: Failure-mode categories (draft v0.1)**
- Wrote `docs/02_failure_mode_categories.md`: 12 categories, priority rules, phase of use, 5-level severity, contributor, retained fragment flag, ISO 14971 mapping. Built from FDA problem codes and real report text. Awaiting review against the reference FMEA.

**Step 2 (continued): full data set**
- Saved pages 6-16: first 100 reports for each quarter from Q2 2023 to Q4 2025. All checked: correct product code and dates.
- Total 1,600 reports. Built a balanced sample of 1,200 (100 per quarter) for analysis.
- Recorded full-population report counts per quarter (11,466 in total): 2,799 in 2023, 4,243 in 2024, 4,424 in 2025.
- First signal: leak codes rose from 34% of reports (2023) to 54% (2024). To investigate in classification.
- Summary in `docs/03_data_summary.md`.

**Step 3: Failure-mode categories (v1.0, done)**
- Reviewed the draft against the reference FMEA (8 failure modes, transcribed in `docs/fmea_reference.md`).
- Confirmed the categories match; added FM13 (local tissue / hypersensitivity reaction) to cover FMEA row 3 "line rejected by the body".
- Mapped every category to its FMEA row and severity. FM04, FM05, FM06, FM07 and FM11 have no FMEA row: candidate gaps to test in step 6.
- Confirmed 5-level severity scale. Decided to exclude midline catheters from analysis.

**Step 4: AI classification (pilot done)**
- Wrote the fixed classification prompt and method (`docs/04_classification_method.md`).
- Pilot on 20 random reports (excluded from later validation). Results in `data/processed/ai_labels_pilot.csv`.
- Main finding: 8 of 10 reports with the FDA code "Fluid/Blood Leak" actually describe catheter body breakage.
- Found 5 rule problems; to be fixed (categories v1.1) before the full run.

**Step 4: AI classification (done)**
- Categories updated to v1.1 after the pilot (5 rule fixes).
- FMEA source anonymised; git history rebuilt so earlier versions are not published.
- 300 reports coded (25 per quarter). 288 unique complaints after removing 3 voided duplicates and grouping repeat reports.
- Results in `docs/05_ai_classification_results.md`. Main findings: 80% of FDA "leak" reports are catheter body breaks; catheter breaks rose from 28% to 54% of complaints 2023-2025; a septum/stopper leak cluster in 2023 that faded; insertion accessories (14%) are the biggest hazard missing from the reference FMEA.
- Built `data/step5_manual_coding.xlsx`: 100 reports for blind manual coding (no AI answers).

**Step 5: Validation (done)**
- Author coded 100 reports blind in `data/step5_manual_coding_completed.xlsx`.
- Primary failure mode: 93% agreement (kappa 0.90). Phase 93%, retained fragment 99%, user harm 100%. Severity 61% (kappa 0.44), AI systematically one level lower, mainly "new line inserted" cases.
- Found that the AI was given a shorter manufacturer narrative than the reviewer; to fix before any re-run.
- Results in `docs/06_validation_results.md`.

**Step 6: Figures and FMEA comparison (done)**
- `scripts/make_figures.py` builds five figures in `figures/` (palette checked for colour-blind safety).
- `docs/07_fmea_comparison.md`: FMEA rows vs field data, hazards with no FMEA row, six recommended FMEA updates.

**Optional re-test (done)**
- Categories v1.2: unplanned line replacement = S3; repair/trim/removal = S2; severity patient-only; full manufacturer narrative given to the model.
- Independent re-run by a separate Claude instance with only the rules and report text.
- Severity agreement 61% -> 85% (kappa 0.44 -> 0.78); failure mode 93% -> 92%; all fields identical 43% -> 63%.

**Step 7: Report (draft done)**
- `REPORT.md`: summary, background, intended use, method, results, validation and re-test, FMEA comparison, limitations, conclusions.
- `README.md` rewritten as the GitHub front page.
- `skill/maude-pms-coder/`: the coding method packaged as a reusable Claude skill.
