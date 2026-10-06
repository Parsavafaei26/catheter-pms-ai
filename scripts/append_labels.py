"""Append AI labels (pipe-separated lines on stdin) to data/processed/ai_labels_full.csv.

Line format:
report_number|primary|secondary|phase|severity|contributor|retained|user_harm|group|confidence|quote|note
"""
import csv, sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "processed" / "ai_labels_full.csv"
H = ["report_number", "primary_fm", "secondary_fm", "phase", "severity", "contributor",
     "retained_fragment", "user_harm", "complaint_group", "confidence", "supporting_quote", "note"]
new = not OUT.exists()
done = set() if new else {r["report_number"] for r in csv.DictReader(open(OUT, encoding="utf-8"))}
n = 0
with open(OUT, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new:
        w.writerow(H)
    for line in sys.stdin:
        p = [x.strip() for x in line.rstrip("\n").split("|")]
        if len(p) != len(H):
            if line.strip():
                print("SKIPPED (wrong field count):", line[:60])
            continue
        if p[0] in done:
            continue
        if not p[8]:
            p[8] = p[0]
        w.writerow(p); done.add(p[0]); n += 1
print(f"Added {n}; total {len(done)}")
