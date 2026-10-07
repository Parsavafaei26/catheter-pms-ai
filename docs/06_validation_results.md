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

## Re-test after the fix (categories v1.2)

The validation found two causes of error: an ambiguous severity rule and a shortened manufacturer
narrative. Following a CAPA-style approach, both were corrected:

- **Rule fix (v1.2):** any unplanned replacement of the central line = S3; repair, trim or removal
  without replacement = S2; severity covers the patient only.
- **Input fix:** the model received the full manufacturer narrative.

To keep the re-test independent, the 100 reports were re-coded by a **separate Claude instance**
that received only the v1.2 rules and the report text. It had no access to the human labels, the
first AI labels or the project discussion. Results: `data/rerun/rerun_labels_v1_2.csv`,
comparison `data/rerun/validation_comparison_v1_2.csv`.

| Field | v1.1 agreement (kappa) | v1.2 agreement (kappa) |
|---|---|---|
| Primary failure mode | 93% (0.90) | 92% (0.89) |
| Secondary failure mode | 86% (0.61) | 93% (0.83) |
| Phase of use | 93% (0.88) | 96% (0.93) |
| **Severity** | **61% (0.44)** | **85% (0.78)** |
| Likely contributor | 86% (0.62) | 88% (0.75) |
| Retained fragment | 99% (0.93) | 100% (1.00) |
| User harm | 100% (1.00) | 100% (1.00) |
| All seven fields identical | 43% | 63% |

Severity agreement rose from moderate to substantial; failure-mode agreement stayed at about 92-93%.
The remaining severity differences still lean one way (the reviewer higher in 15 of 15), so human
review of severity stays in place. Three of the eight remaining failure-mode differences sit on
the same boundary, a leak or separation at the joint between the tube and the hub (catheter body
vs external component), which is the next rule to clarify.

**Caveat:** the v1.2 severity rule was written after seeing where the reviewer and the AI
disagreed, and the re-test used the same 100 reports. The improvement shows that the clarified
rule removes most of the ambiguity; it is not a fully independent estimate of accuracy. A fresh
set of reports coded by both would be needed for that.

![Before and after](../figures/fig6_validation_before_after.png)
