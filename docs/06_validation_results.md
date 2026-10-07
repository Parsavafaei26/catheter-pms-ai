# 6. Validation: AI vs blind manual coding (step 5)

*October 2026. 100 reports, stratified by year (seed 5), coded independently by the author using
categories v1.1, without seeing the AI labels (confirmed blind), then compared with the AI labels. Script: `scripts/compare_validation.py`.
Row-by-row comparison: `data/processed/validation_comparison.csv`.*

## Agreement

| Field | Agreement | Cohen's kappa | Reading |
|---|---|---|---|
| Primary failure mode | **93%** | **0.90** | almost perfect |
| Phase of use | 93% | 0.88 | almost perfect |
| Retained fragment | 99% | 0.93 | almost perfect |
| User harm | 100% | 1.00 | perfect |
| Secondary failure mode | 86% | 0.61 | substantial |
| Likely contributor | 86% | 0.62 | substantial |
| Severity | 61% | 0.44 | moderate |
| Severity within one level | 98% | | |

Kappa corrects for agreement expected by chance (Landis and Koch scale: 0.41-0.60 moderate,
0.61-0.80 substantial, above 0.80 almost perfect). All seven fields matched exactly in 43% of reports.

## What the disagreements show

**1. Failure mode: the AI is reliable for the main question.** 7 of 100 reports differed. Three
were borderline between related categories (catheter body vs hub joint; external component vs
unknown leak source; insertion accessory found in the pack vs packaging defect). Three came from
information the AI did not see (see point 3).

**2. Severity: the AI rated harm lower than the human reviewer.** In 38 of 39 severity
disagreements the reviewer chose a higher level, mostly S3 instead of S2 (26 reports). Almost all
were cases where the PICC had to be removed and a **new line inserted**. The rules said "line
replaced at the bedside" is S2 and "replacement under imaging" is S3, but reports rarely say how
the new line was placed. This is a weakness in the coding rules, not only in the AI.
Under-rating severity is the less safe direction of error for PMS, so **AI severity ratings
should not be used without human review**. Rule fix for v1.2: any unplanned replacement of a
central line = S3.

**3. The AI saw less of the manufacturer narrative.** To save reading time, the AI pipeline gave
the model the first 350 characters of the manufacturer narrative; the review workbook showed up to
1,200. Several disagreements on failure mode and contributor came from investigation findings
beyond the cut-off (e.g. "split on luer extension leg confirmed", "manufacturing condition",
"use related"). This explains most contributor differences (reviewer DEV or USE, AI UNK in 12
reports). Fix: give the model the full narrative.

**4. Scope of severity.** In one report a nurse was sprayed with blood from an HIV-positive
patient; the reviewer rated severity S3, the AI S1 because the severity field covers the patient
only. Both flagged user harm. Rule clarification needed: report user harm severity separately.

## Conclusion

For the question PMS trend review needs most, "what failed?", the AI agreed with blind expert
coding in 93% of reports (kappa 0.90). For severity it agreed in 61% and was systematically more
lenient. The tool is fit for its intended use as **decision support for failure-mode trending, with
human review of severity and of every serious event**, as stated in the intended use.

## Limitations of the validation

- One human reviewer; no second reviewer to measure human-human agreement.
- The reviewer is also the author of the coding rules.
- AI and reviewer inputs differed in narrative length (point 3).
- 100 reports from the same 300-report sample used for the main analysis.
