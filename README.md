# AI-assisted post-market surveillance for long-term central venous catheters

A small prototype that reads public FDA MAUDE adverse event reports for long-term
implanted intravascular catheters (including PICCs), uses a large language model to
classify each report by failure mode and harm severity, and compares the results with
an ISO 14971-style FMEA.

The project is **decision support for post-market surveillance (PMS) trend review**.
It does not decide whether an event is reportable, and every AI output is reviewed by
a person. See [docs/01_intended_use.md](docs/01_intended_use.md).

## Status

| Step | Description | Status |
|---|---|---|
| 1 | Intended use and scope | Draft |
| 2 | Data extraction from openFDA (MAUDE) | Done: 1,600 reports, balanced sample of 1,200 |
| 3 | Failure-mode categories and definitions (from FMEA) | Done (v1.0) |
| 4 | AI classification | Done (300 reports) |
| 5 | Validation against manual review (n = 100) | Done: 93% agreement on failure mode (kappa 0.90) |
| 6 | Results and FMEA comparison | Done |
| 7 | Write-up and limitations | Not started |

## Repository layout

```
docs/       intended use, category definitions, method, results
scripts/    data extraction and classification scripts
data/raw/        openFDA JSON downloads (public domain)
data/processed/  cleaned CSV files used for analysis
```

## Data source

U.S. FDA Manufacturer and User Facility Device Experience (MAUDE) database, accessed
through the openFDA device adverse event API (https://open.fda.gov/apis/device/event/).
MAUDE data are public. They are subject to under-reporting, duplicate reports and
missing information, and they cannot be used to calculate event rates because there is
no data on how many devices are in use.

## Author

Parsa Vafaei, MSc Biomedical Engineering (University of Sheffield)
