# 4. AI classification method

## Model and set-up

- Model: Claude (Anthropic), used through the Claude app.
- Input per report: event type, FDA device and patient problem codes, event description, manufacturer narrative.
- Instructions: the fixed prompt below plus `docs/02_failure_mode_categories.md` (v1.0 for the pilot, v1.1 for the full run), unchanged between reports.
- Output per report: one row in `data/processed/ai_labels_*.csv`.

## Fixed prompt

> You are assisting a post-market surveillance review of adverse event reports for long-term
> central venous catheters (FDA product code LJS). Using only the coding rules in
> "Failure-mode categories and coding rules", code the report below.
>
> Return: primary failure mode (FM01-FM13), secondary failure mode (or none), phase of use
> (P1-P5), harm severity (S1-S5), likely contributor (DEV, USE, PAT, UNK), retained fragment
> (Y/N), user harm (Y/N), complaint group, confidence (high, medium, low), a short quote from the report that supports the
> primary code, and a note if the rules did not fit the report well.
>
> Base every answer on the report text only. Do not use the FDA problem codes as the answer;
> they are a hint only. If the report does not give enough information, choose the more
> cautious option and set confidence to low. Do not decide whether the event is reportable.

## Pilot (20 reports)

20 reports were chosen at random (seed 7) from the balanced sample, excluding midline
catheters. They are listed in `data/processed/pilot_ids.txt` and will be **excluded from the
100-report validation set**, so the validation is not influenced by rule changes made after
the pilot.

### Pilot results

| Primary code | Reports |
|---|---|
| FM01 Catheter body break | 11 |
| FM02 External component failure | 6 |
| FM05 Insertion accessory failure | 2 |
| FM06 Malposition / migration | 1 |

Confidence: 14 high, 4 medium, 2 low. One retained fragment (peel-apart sheath, surgical removal).

**Finding 1: the FDA "Fluid/Blood Leak" code hides breakages.** 10 of the 20 reports carried the
FDA code "Fluid/Blood Leak". Reading the text, 8 of those 10 describe a breach of the catheter
body (fracture, split, tear or hole) and only 2 a leak from an external part. If this holds in
the full sample, the rise in leak reports seen in step 3 may partly reflect how reports are
coded, and catheter body breakage (FMEA row 2, severity 5) may be under-counted by the FDA codes.
This is only 10 reports and must be tested in the full run.

**Finding 2: a repeated component issue.** Three reports describe leaks or air entry at the
rubber septum / stopper that holds the stylet or guidewire at the catheter hub, one confirmed
by the manufacturer as a manufacturing condition. This part is not in the reference FMEA.

### Rule problems found in the pilot (fixed in v1.1)

1. **External shaft vs hub:** a break in the part of the catheter shaft outside the body was
   hard to place. Rule to add: any breach of the catheter tube itself, inside or outside the
   body, is FM01; FM02 is only for hubs, extension legs, clamps, connectors, valves, septa and wings.
2. **Missing component out of the box** (e.g. no cuff attached) fits no category well.
   Option: widen FM08 to "packaging, labelling or assembly defect found before use".
3. **Harm to users:** a nurse was sprayed with blood. The severity scale only covers patients.
   ISO 14971 includes harm to users, so add a yes/no field "user exposed to harm".
4. **Leak at insertion site with no visible breach:** coded FM01 with low confidence. Rule to
   add so both coders handle it the same way.
5. **Several reports for one complaint** (e.g. five devices, five reports): add a field linking
   reports from the same complaint so they are counted once in the trend analysis.
