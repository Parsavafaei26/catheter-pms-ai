# 5. AI classification results (step 4)

*October 2026. 300 reports coded with categories v1.1. These are AI results only: they are
checked against blind manual review in step 5 before any conclusion is drawn.*

## Sample

- 300 reports: 25 per quarter, Q1 2023 to Q4 2025, random (seed 2026), midline catheters and
  pilot reports excluded. List in `data/processed/classification_ids.txt`.
- 3 reports were voided by the manufacturer as duplicates and are excluded from counts.
- Reports describing the same complaint were grouped, leaving **288 unique complaints**
  (95 in 2023, 96 in 2024, 97 in 2025).
- Labels: `data/processed/ai_labels_full.csv`. Confidence: 185 high, 88 medium, 15 low.

## Failure modes (unique complaints)

| Code | Category | Total | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| FM01 | Catheter body break | 126 (44%) | 27 | 47 | 52 |
| FM02 | External component failure | 48 (17%) | 30 | 11 | 7 |
| FM05 | Insertion accessory failure | 41 (14%) | 14 | 18 | 9 |
| FM08 | Packaging / assembly defect before use | 18 | 6 | 3 | 9 |
| FM04 | Kink / deformation | 15 | 3 | 3 | 9 |
| FM03 | Occlusion | 11 | 4 | 4 | 3 |
| FM12 | Other / insufficient information | 9 | 2 | 3 | 4 |
| FM09 | Infection | 5 | 3 | 0 | 2 |
| FM06 | Malposition / migration | 4 | 1 | 3 | 0 |
| FM13 | Tissue / hypersensitivity reaction | 4 | 3 | 1 | 0 |
| FM10 | Thrombosis | 3 | 1 | 1 | 1 |
| FM07 | Difficult insertion / removal | 2 | 1 | 1 | 0 |
| FM11 | Vessel injury / extravasation | 2 | 0 | 1 | 1 |

Severity: S1 132, S2 122, S3 22, S4 12, S5 0. Phase: most events happened during use (170),
then insertion (76). 15 complaints involved a retained fragment; 2 involved harm to a user.

## Key findings (to be confirmed in validation)

**1. The FDA "Fluid/Blood Leak" code mostly hides catheter breakage.**
125 complaints carried the FDA code "Fluid/Blood Leak". Reading the text, **100 of them (80%)
describe a breach of the catheter body** (fracture, split, hole, crack); only 17 were leaks from
hubs, extensions or connectors. This confirms the pilot finding on a larger sample.

**2. The real trend is catheter body breakage, not "leaks".**
Catheter body breaks rose from **28% of complaints in 2023 to 49% in 2024 and 54% in 2025**.
Manufacturer investigations attributed 42 of them to "flexural fatigue" (repeated kinking of the
tube), rising from 7 (2023) to 16 (2024) and 19 (2025). Most breaks happened during use (101 of 126),
often a few centimetres from the exit site or the securement device. This matches FMEA row 2 "line
breaks" (severity 5), which is the most frequent failure mode in the data.

**3. A component signal that appeared and then faded.**
15 complaints described leaks or air entry at the rubber septum / stopper / T-lock that holds the
stylet at the hub, 13 of them in 2023. Several reporters linked it to a "new" stopper design and the
manufacturer confirmed a manufacturing or supplier cause in some. Only 2 appeared in 2024 and none
in 2025, consistent with a problem being found and corrected. Air entry through this part is an
air-embolism hazard. **This is exactly the kind of signal PMS trend review is meant to catch.**

**4. Hazards missing from the reference FMEA.**

| Category with no FMEA row | Complaints | Severe cases |
|---|---|---|
| FM05 Insertion accessory failure (guidewires, sheaths, stylets, tip-location system) | 41 (14%) | 5 at S4, incl. guidewire fragments in the heart |
| FM04 Kink / deformation | 15 | clusters of 4-6 kinked PICCs at single sites |
| FM06 Malposition / migration | 4 | arterial placement with stroke (S4) |
| FM11 Vessel injury / extravasation | 2 primary + 10 secondary | chemotherapy extravasation needing surgical review |
| User harm (any category) | 2 | blood splash to the eye from an HIV-positive patient; sharps injury |

The reference FMEA also considered only harm to patients; ISO 14971 includes users.

**5. Where MAUDE under-represents the FMEA's top risks.**
The reference FMEA rated infection (rows 1 and 4) as its highest initial risks (R = 20), but
infection appears in only 5 complaints. Infections are rarely attributed to the device by the
reporter, so MAUDE is a weak source for this hazard. A PMS plan would need other data (e.g.
literature, registries) to monitor it.

## Limitations

- The AI codes come from Claude reading the report text in this project. They have **not yet
  been validated**: step 5 compares them with blind manual coding of 100 reports.
- Report text is often short; 15 complaints were coded with low confidence.
- The likely contributor is unknown for 84% of complaints; manufacturer investigations were
  often incomplete or pending.
- The sample is 25 reports per quarter, not the full population; percentages describe the sample.
- One manufacturer group accounts for most reports, so results describe reporting for this device
  type overall and must not be used to compare manufacturers.
