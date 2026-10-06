"""Select the step 4 classification sample and print compact report text in batches.

Sample: 25 reports per quarter (300 in total) from the balanced sample, excluding midline
catheters and the 20 pilot reports. Random seed 2026.

    python3 scripts/prepare_batches.py select      # writes data/processed/classification_ids.txt
    python3 scripts/prepare_batches.py show 1      # prints batch 1 (reports 1-30)
"""
import csv, random, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "data" / "processed"
BATCH = 30
BOILER = re.compile(r"(THE INFORMATION PROVIDED BY BD REPRESENTS|DESPITE GOOD FAITH|H11: SECTION A|"
                    r"THE DATE OF EVENT WAS NOT PROVIDED|EACH EVENT REPORTED TO BD IS EVALUATED|"
                    r"THE INSTRUCTIONS FOR USE \(IFU\) IS ADEQUATE|LABELING REVIEW|\(B\)\(4\)\.)")


def is_midline(r):
    return bool(re.search("midline", r["event_description"] + r["brand_name"] + r["generic_name"], re.I))


def dedupe(text):
    """MAUDE often repeats the same paragraph twice; keep sentences once, in order."""
    seen, out = set(), []
    for s in re.split(r"(?<=[.!?])\s+", text):
        k = s.strip()
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return " ".join(out)


def mfr_summary(text):
    keep = [s for s in re.split(r"(?<=[.!?])\s+", dedupe(text)) if s and not BOILER.search(s)]
    return " ".join(keep)


def select():
    rows = [r for r in csv.DictReader(open(P / "maude_balanced_sample.csv", encoding="utf-8")) if not is_midline(r)]
    pilot = set((P / "pilot_ids.txt").read_text().split())
    by = defaultdict(list)
    for r in rows:
        if r["report_number"] not in pilot:
            by[r["quarter_received"]].append(r)
    random.seed(2026)
    ids = []
    for q in sorted(by):
        ids += [r["report_number"] for r in random.sample(by[q], 25)]
    (P / "classification_ids.txt").write_text("\n".join(ids) + "\n")
    print(f"Selected {len(ids)} reports")


def show(n):
    ids = (P / "classification_ids.txt").read_text().split()
    rows = {r["report_number"]: r for r in csv.DictReader(open(P / "maude_reports.csv", encoding="utf-8"))}
    for i, rid in enumerate(ids[(n - 1) * BATCH:n * BATCH], (n - 1) * BATCH + 1):
        r = rows[rid]
        print(f"\n#{i} {rid} | {r['event_type']} | {r['brand_name'][:45]} | DP: {r['device_problems'][:90]} | PP: {r['patient_problems'][:80]}")
        print(dedupe(r["event_description"])[:1000])
        m = mfr_summary(r["manufacturer_narrative"])[:350]
        if m:
            print("MFR:", m)


if __name__ == "__main__":
    select() if sys.argv[1] == "select" else show(int(sys.argv[2]))
