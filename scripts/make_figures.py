"""Step 6: build the report figures from the labelled data (PNG, light theme)."""
import csv, re
from collections import Counter
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
P, OUT = ROOT / "data" / "processed", ROOT / "figures"
OUT.mkdir(exist_ok=True)
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#b8b7b1"
INK, INK2, SURF, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e6e5e0"
plt.rcParams.update({"font.family": "Lato", "font.size": 11, "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.dpi": 200})

ai = list(csv.DictReader(open(P / "ai_labels_full.csv", encoding="utf-8")))
rep = {r["report_number"]: r for r in csv.DictReader(open(P / "maude_reports.csv", encoding="utf-8"))}
groups = {}
for r in ai:
    if "VOIDED" not in r["note"]:
        groups.setdefault(r["complaint_group"], r)
U = list(groups.values())
yr = lambda r: rep[r["report_number"]]["date_received"][:4]
YEARS = ["2023", "2024", "2025"]


def style(ax, title, sub=None):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.set_title(title, loc="left", fontsize=14, fontweight="bold", pad=24 if sub else 10)
    if sub:
        ax.text(0, 1.02, sub, transform=ax.transAxes, color=INK2, fontsize=10)


# 1. Reports per quarter (full population)
q = list(csv.DictReader(open(P / "quarterly_totals.csv")))
fig, ax = plt.subplots(figsize=(8, 4))
x = range(len(q))
ax.plot(x, [int(r["reports_in_maude"]) for r in q], color=BLUE, lw=2, marker="o", ms=6, mec=SURF, mew=2)
ax.set_xticks(list(x), [r["quarter"].replace("-", "\n") for r in q], fontsize=9)
ax.yaxis.grid(color=GRID); ax.set_ylim(0, 1500); ax.set_yticks(range(0, 1401, 200))
style(ax, "FDA reports for long-term catheters per quarter", "All 11,466 MAUDE reports, product code LJS, 2023-2025")
fig.tight_layout(); fig.savefig(OUT / "fig1_reports_per_quarter.png"); plt.close(fig)

# 2. FM01 vs FM02 share by year
fig, ax = plt.subplots(figsize=(8, 4))
w = 0.36
for i, (code, lab, col) in enumerate([("FM01", "Catheter body break", BLUE), ("FM02", "External component (hub, connector, septum)", ORANGE)]):
    vals = [100 * sum(r["primary_fm"] == code for r in U if yr(r) == y) / sum(yr(r) == y for r in U) for y in YEARS]
    xs = [k + (i - 0.5) * (w + 0.02) for k in range(3)]
    ax.bar(xs, vals, w, color=col, label=lab)
    for xx, v in zip(xs, vals):
        ax.text(xx, v + 1.2, f"{v:.0f}%", ha="center", color=INK, fontsize=10)
ax.set_xticks(range(3), YEARS); ax.set_ylim(0, 65); ax.set_yticks([])
ax.legend(frameon=False, loc="upper left", fontsize=10)
style(ax, "Catheter body breaks rose while hub/connector failures fell", "Share of unique complaints in the 288-complaint sample, AI-coded")
fig.tight_layout(); fig.savefig(OUT / "fig2_failure_mode_trend.png"); plt.close(fig)

# 3. What FDA "leak" reports really are
lk = [r for r in U if "Leak" in rep[r["report_number"]]["device_problems"]]
c = Counter(r["primary_fm"] for r in lk)
cats = [("Catheter body break", c["FM01"], BLUE), ("External component", c["FM02"], GREY),
        ("Other / unclear", len(lk) - c["FM01"] - c["FM02"], GREY)]
fig, ax = plt.subplots(figsize=(8, 2.8))
for i, (lab, n, col) in enumerate(cats):
    ax.barh(i, n, color=col, height=0.6)
    ax.text(n + 1.5, i, f"{n}  ({100*n/len(lk):.0f}%)", va="center", fontsize=10)
ax.set_yticks(range(3), [x[0] for x in cats]); ax.invert_yaxis(); ax.set_xticks([]); ax.set_xlim(0, 125)
style(ax, f'What the {len(lk)} FDA "Fluid/Blood Leak" complaints actually describe', "Primary failure mode from reading the report text")
fig.tight_layout(); fig.savefig(OUT / "fig3_leak_code_breakdown.png"); plt.close(fig)

# 4. Septum / stopper cluster
pat = r"STOPPER|SEPTUM|T-LOCK|T LOCK|RUBBER|WIRE GOES|HOUSES THE WIRE|T CONNECTOR|T PIECE"
sep = [r for r in U if r["primary_fm"] == "FM02" and re.search(pat, rep[r["report_number"]]["event_description"], re.I)]
vals = [sum(yr(r) == y for r in sep) for y in YEARS]
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.bar(range(3), vals, 0.5, color=ORANGE)
for k, v in enumerate(vals):
    ax.text(k, v + 0.3, str(v), ha="center", fontsize=11)
ax.set_xticks(range(3), YEARS); ax.set_yticks([]); ax.set_ylim(0, 15)
style(ax, "Leaks and air entry at the stylet septum", "Complaints in the sample, by year received")
fig.tight_layout(); fig.savefig(OUT / "fig4_septum_cluster.png"); plt.close(fig)

# 5. Validation agreement
v = {r: None for r in []}
comp = list(csv.DictReader(open(P / "validation_comparison.csv", encoding="utf-8")))
fields = [("primary_fm", "Failure mode"), ("phase", "Phase of use"), ("retained_fragment", "Retained fragment"),
          ("user_harm", "User harm"), ("secondary_fm", "Secondary failure mode"), ("contributor", "Likely cause"), ("severity", "Severity")]
fig, ax = plt.subplots(figsize=(8, 3.8))
for i, (f, lab) in enumerate(fields):
    a = 100 * sum(r[f + "_manual"] == r[f + "_ai"] for r in comp) / len(comp)
    ax.barh(i, a, color=BLUE if a >= 80 else ORANGE, height=0.6)
    ax.text(a + 1, i, f"{a:.0f}%", va="center", fontsize=10)
ax.set_yticks(range(len(fields)), [x[1] for x in fields]); ax.invert_yaxis(); ax.set_xlim(0, 110); ax.set_xticks([])
style(ax, "AI vs blind human coding, 100 reports", "Exact agreement per field; orange = below 80%")
fig.tight_layout(); fig.savefig(OUT / "fig5_validation_agreement.png"); plt.close(fig)
print("done", sorted(p.name for p in OUT.iterdir()))
