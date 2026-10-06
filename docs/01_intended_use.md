# 1. Intended use and scope

*Draft, October 2026*

## Purpose

This tool supports post-market surveillance (PMS) trend review for long-term implanted
intravascular catheters, including peripherally inserted central catheters (PICCs) and
other central venous catheters intended to stay in place for more than 30 days.

It reads adverse event reports from the FDA MAUDE database and suggests, for each report:

- the failure mode, from a fixed list based on the device FMEA
- the harm severity
- whether the event looks device-related, use-related or patient-related
- a quote from the report that supports the suggestion
- a confidence level (high, medium or low)

The output is a summary of which failure modes occur most often in real-world reports and
how they compare with the hazards and occurrence ratings in the FMEA.

## Intended user

A regulatory affairs, quality or risk management professional carrying out periodic PMS
review, who understands the device and checks the AI suggestions.

## What the tool is not for

- Deciding whether an individual event is reportable under EU MDR, UK MDR or 21 CFR 803.
- Replacing complaint handling, trend reporting or vigilance processes.
- Calculating incidence rates. MAUDE has no data on how many devices are in use.
- Clinical decisions about individual patients.

## Human oversight

Every AI suggestion is reviewed by a person before it is used. Low-confidence outputs
are flagged for review first. The tool is validated by comparing its labels with an
independent manual review of 100 reports, and the agreement rate and disagreements are
reported.

## Scope of this prototype

| Item | Scope |
|---|---|
| Device | Long-term implanted intravascular catheters (FDA product code LJS, confirmed from report data) |
| Data | MAUDE reports received 1 Jan 2023 to 31 Dec 2025 |
| Sample | 300 to 500 reports for classification; 100 for manual validation |
| Market | U.S. reports only (MAUDE). UK and EU vigilance data are not publicly available in bulk |
| Model | Large language model (Claude), fixed prompt and category definitions |

## Known limitations of the data

- Reporting is voluntary for users and patients, so many events are never reported.
- Some events are reported more than once.
- Report narratives are often short or missing key details.
- Manufacturers redact some information.
- Report counts reflect reporting behaviour as well as device performance.
