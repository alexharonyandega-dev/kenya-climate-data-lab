"""Two-axis plot showing the gap Kenya's monitoring tools leave.

X-axis: geographic coverage granularity (national -> county)
Y-axis: update frequency (annual -> weekly)

Existing tools cluster along the "frequent" axis without county granularity,
or the "county" axis without frequent updates. Our tool sits alone in the
top-right.
"""
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "paper" / "figures" / "fig_the_gap.png"

# (tool_name, granularity_score 0-10, frequency_score 0-10, color)
TOOLS = [
    ("FAO ASI",            7.5, 7.0, "#94a3b8"),   # sub-county, 10-daily
    ("FEWS NET\nKenya",    4.0, 6.5, "#94a3b8"),   # livelihood zone, monthly
    ("GEOGLAM",            7.0, 6.0, "#94a3b8"),   # crop-zone, monthly
    ("KMD / ICPAC",        4.5, 5.5, "#94a3b8"),   # regional, monthly
    ("KNBS Report",        9.5, 1.5, "#94a3b8"),   # county, annual
    ("FAOSTAT",            1.0, 1.5, "#94a3b8"),   # national, annual
    ("Kenya Climate\nData Lab", 10.0, 8.0, "#dc2626"),  # ours
]

fig, ax = plt.subplots(figsize=(11, 8))

for name, x, y, color in TOOLS:
    marker_size = 600 if "Kenya Climate" in name else 400
    edge_color = "#991b1b" if "Kenya Climate" in name else "#475569"
    linewidth = 3 if "Kenya Climate" in name else 1.5
    ax.scatter(x, y, s=marker_size, c=color, edgecolor=edge_color,
               linewidth=linewidth, zorder=3, alpha=0.85)

    if "Kenya Climate" in name:
        ax.annotate(name,
                    xy=(x, y),
                    xytext=(x - 2.3, y - 1.5),
                    fontsize=12, weight="bold", color="#991b1b",
                    ha="center",
                    arrowprops=dict(arrowstyle="->", color="#991b1b", lw=2))
    else:
        ax.annotate(name,
                    xy=(x, y),
                    xytext=(0, -18),
                    textcoords="offset points",
                    fontsize=10, color="#334155",
                    ha="center", va="top")

# Highlight the gap zone with a dashed rectangle
ax.axhspan(7, 9, xmin=0.85, xmax=0.98, color="#fee2e2",
           alpha=0.4, zorder=1)
ax.text(9.6, 8.6, "THE GAP", fontsize=13, weight="bold",
        color="#991b1b", ha="center", alpha=0.7)

# Axis labels and limits
ax.set_xlim(0, 11)
ax.set_ylim(0, 10)
ax.set_xlabel("Geographic coverage\n← national          county →",
              fontsize=12, labelpad=10)
ax.set_ylabel("Update frequency\n← annual          weekly →",
              fontsize=12, labelpad=10)

ax.set_xticks([1, 5, 10])
ax.set_xticklabels(["National", "Regional", "County"], fontsize=11)
ax.set_yticks([1.5, 5, 8])
ax.set_yticklabels(["Annual", "Monthly", "Weekly"], fontsize=11)

ax.grid(True, alpha=0.2, linestyle="--")
ax.set_title("Kenya maize monitoring: existing tools vs the gap",
             fontsize=15, weight="bold", pad=20)

ax.set_facecolor("#fafafa")
plt.tight_layout()
plt.savefig(FIG, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {FIG}")
