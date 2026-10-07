---
name: maude-pms-coder
description: Code FDA MAUDE adverse event reports for long-term central venous catheters (PICCs, tunnelled CVCs) into failure mode, severity, phase of use and contributor, for post-market surveillance trend review. Use when asked to classify or trend catheter adverse event or complaint narratives.
---

# MAUDE PMS coder

Decision support for post-market surveillance (PMS) trend review. It suggests codes for each
report; a person reviews them. It does **not** decide whether an event is reportable.

## Before coding

1. Read `references/coding_rules.md` in full (categories v1.2).
2. Confirm the reports are for long-term central venous catheters. Exclude midline catheters.

## For each report

Read the event description and the **full** manufacturer narrative. Use the FDA problem codes
as hints only; they often hide the real failure mode (e.g. "Fluid/Blood Leak" is usually a
catheter body break).

Return one row with:

| Field | Values |
|---|---|
| primary_fm | FM01-FM13 |
| secondary_fm | FM01-FM13 or none (different from primary) |
| phase | P1 before use, P2 insertion, P3 in use, P4 removal, P5 unknown |
| severity | S1-S5, patient harm only; unplanned line replacement = S3; repair, trim or removal = S2 |
| contributor | DEV, USE, PAT, UNK (use manufacturer conclusions when stated) |
| retained_fragment | Y / N |
| user_harm | Y / N |
| confidence | high / medium / low |
| quote | short quote supporting the primary code |
| note | one sentence |

Apply the priority rules: breach beats deformation and occlusion; device failure beats
clinical complication; cause beats effect; insertion-site leak with no visible breach = FM01
low confidence; leak with no location = FM12 low confidence.

## Human review is required for

- every severity rating (validation showed the model rates harm lower than a reviewer),
- every S3-S5 event, retained fragment or user harm,
- every low-confidence code.

## Validation record

On 100 reports coded blind by a reviewer: failure mode 92-93% agreement (kappa 0.89-0.90);
severity 85% (kappa 0.78) with rules v1.2. See the project report for method and limitations.
