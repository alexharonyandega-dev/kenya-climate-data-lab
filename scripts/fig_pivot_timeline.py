from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parent.parent

events = [
    ("Mon", "5 counties.\nYield prediction.", "#94a3b8"),
    ("Tue", "Mark's advice.\nScope: 5 or 47?", "#f59e0b"),
    ("Wed", "PIVOT. GEE registered.\nCHIRPS: 3.1 min.", "#ef4444"),
    ("Thu", "Sentinel-2 NDVI.\nStress index built.", "#16a34a"),
    ("Fri", "2022 drought detected\nwithout calibration.", "#0891b2"),
    ("Sat", "ERA5: 5.4M rows.\n32 decisions logged.", "#7c3aed"),
    ("Sun", "Reproducibility audit\npasses.", "#a16207"),
]

fig, ax = plt.subplots(figsize=(13, 4.2))
y = 0
for i, (day, text, color) in enumerate(events):
    ax.add_patch(mpatches.FancyBboxPatch(
        (i - 0.42, y - 0.35), 0.84, 0.7,
        boxstyle="round,pad=0.02", linewidth=0,
        facecolor=color, alpha=0.9))
    ax.text(i, y + 0.12, day, ha="center", va="center",
            fontsize=11, color="white", fontweight="bold")
    ax.text(i, y - 0.12, text, ha="center", va="center",
            fontsize=8, color="white")

ax.axvline(2, ymin=0, ymax=1, color="#ef4444",
           linewidth=2, linestyle="--", alpha=0.4)
ax.text(2, y + 0.55, "The pivot", ha="center", fontsize=12,
        color="#ef4444", fontweight="bold")

ax.set_xlim(-0.7, len(events) - 0.3)
ax.set_ylim(-0.7, 0.95)
ax.axis("off")
ax.set_title("Week 3: how the pivot happened",
             fontsize=14, loc="left", pad=20)

plt.tight_layout()
out = ROOT / "paper/figures/fig_pivot_timeline.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
