"""Download MAUDE adverse event reports from openFDA and save them as a CSV file.

Usage
-----
Download directly (needs internet access to api.fda.gov):
    python3 scripts/fetch_maude.py --product-code LJS --start 20230101 --end 20251231 --max 500

Convert JSON files you saved from your browser instead:
    python3 scripts/fetch_maude.py --from-json data/raw/*.json

Only the Python standard library is used, so nothing needs installing.
"""

import argparse
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.fda.gov/device/event.json"
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed" / "maude_reports.csv"

COLUMNS = [
    "report_number", "date_received", "quarter_received", "date_of_event", "event_type",
    "brand_name", "generic_name", "manufacturer", "product_code",
    "device_problems", "patient_problems", "event_description",
    "manufacturer_narrative",
]


def build_url(product_code, start, end, limit, skip):
    search = (f"device.device_report_product_code:{product_code}"
              f"+AND+date_received:[{start}+TO+{end}]")
    return f"{API}?search={search}&sort=date_received:desc&limit={limit}&skip={skip}"


def fetch(product_code, start, end, max_records):
    results, skip = [], 0
    while len(results) < max_records:
        limit = min(100, max_records - len(results))
        url = build_url(product_code, start, end, limit, skip)
        print(f"Requesting records {skip + 1} to {skip + limit} ...")
        with urllib.request.urlopen(url, timeout=60) as r:
            page = json.load(r)
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / f"{product_code}_{start}_{end}_{skip:05d}.json").write_text(json.dumps(page))
        batch = page.get("results", [])
        results.extend(batch)
        if len(batch) < limit:
            break
        skip += limit
        time.sleep(0.5)  # stay well inside the openFDA rate limit
    return results


def quarter(yyyymmdd):
    if len(yyyymmdd) < 6:
        return ""
    return f"{yyyymmdd[:4]}-Q{(int(yyyymmdd[4:6]) - 1) // 3 + 1}"


def flatten(rec):
    devices = rec.get("device") or [{}]
    d = devices[0]
    texts = rec.get("mdr_text") or []

    def text_of(kind):
        return " ".join(t.get("text", "") for t in texts
                        if kind in (t.get("text_type_code") or "")).strip()

    patient_problems = []
    for p in rec.get("patient") or []:
        patient_problems.extend(p.get("patient_problems") or [])

    return {
        "report_number": rec.get("report_number", ""),
        "date_received": rec.get("date_received", ""),
        "quarter_received": quarter(rec.get("date_received", "")),
        "date_of_event": rec.get("date_of_event", ""),
        "event_type": rec.get("event_type", ""),
        "brand_name": d.get("brand_name", ""),
        "generic_name": d.get("generic_name", ""),
        "manufacturer": d.get("manufacturer_d_name", ""),
        "product_code": d.get("device_report_product_code", ""),
        "device_problems": "; ".join(rec.get("product_problems") or []),
        "patient_problems": "; ".join(sorted(set(patient_problems))),
        "event_description": text_of("Description of Event"),
        "manufacturer_narrative": text_of("Manufacturer Narrative"),
    }


def write_csv(records):
    seen, rows = set(), []
    for rec in records:
        row = flatten(rec)
        if row["report_number"] in seen:  # drop exact duplicate report numbers
            continue
        seen.add(row["report_number"])
        rows.append(row)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved {len(rows)} reports to {OUT.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--product-code", default="LJS")
    ap.add_argument("--start", default="20230101")
    ap.add_argument("--end", default="20251231")
    ap.add_argument("--max", type=int, default=500)
    ap.add_argument("--from-json", nargs="+", metavar="FILE",
                    help="convert saved openFDA JSON files instead of downloading")
    a = ap.parse_args()

    if a.from_json:
        records = []
        for name in a.from_json:
            records.extend(json.loads(Path(name).read_text()).get("results", []))
    else:
        records = fetch(a.product_code, a.start, a.end, a.max)
    write_csv(records)


if __name__ == "__main__":
    main()
