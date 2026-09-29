from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

decisions = [
    ("D01-D05", 5, "Scope",            "#ef4444"),
    ("D06-D10", 5, "Rainfall",         "#3b82f6"),
    ("D11-D14", 4, "Vegetation",       "#16a34a"),
    ("D15-D17", 3, "Soil",             "#a16207"),
    ("D18-D21", 4, "Climate",          "#0891b2"),
    ("D22-D23", 2, "Yield",            "#f59e0b"),
    ("D24-D26", 3, "Stress index",     "#7c3aed"),
    ("D27",     1, "Missing-value",    "#ec4899"),
    ("D28-D30", 3, "Infrastructure",   "#64748b"),
    ("D31-D33", 3, "Outliers & ERA5",  "#0f766e"),
]

fig, ax = plt.subplots(figsize=(14, 4))

x = 0
total = 0
for label, n, name, color in decisions:
    for i in range(n):
        ax.scatter(x + i, 0.5, s=230, color=color, alpha=0.92,
                   edgecolor="white", linewidth=1.5, zorder=3)
    ax.text(x + (n-1)/2, 0.14, label, ha="center", fontsize=8,
            color=color, fontweight="bold")
    ax.text(x + (n-1)/2, 0.82, name, ha="center", fontsize=9,
            color="#555555")
    x += n + 0.7
    total += n

ax.set_xlim(-0.6, x - 0.4)
ax.set_ylim(-0.1, 1.15)
ax.axis("off")
ax.set_title(f"{total} documented decisions. Every choice, written down, in the open.",
             fontsize=13, loc="left", pad=20)

plt.tight_layout()
out = ROOT / "paper/figures/fig_decisions_log.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
print(f"Total decisions plotted: {total}")
