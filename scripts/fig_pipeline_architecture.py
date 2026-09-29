from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parent.parent
fig, ax = plt.subplots(figsize=(14, 7))

def box(x, y, w, h, text, color, fontsize=9):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02",
        linewidth=1.2, edgecolor=color, facecolor=color, alpha=0.15))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, color=color, fontweight="bold")

def arrow(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#666666", lw=1.4))
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.03, label,
                ha="center", fontsize=8, color="#666666", style="italic")

ax.text(0.05, 0.95, "TIER 1 - Weekly rainfall (fast)",
        fontsize=12, fontweight="bold", color="#1e40af")
box(0.05, 0.62, 0.22, 0.20, "CHIRPS\ndaily GeoTIFFs\n5,479 files", "#3b82f6")
box(0.38, 0.62, 0.24, 0.20, "extract_chirps\n_counties.py", "#3b82f6")
box(0.73, 0.62, 0.22, 0.20, "chirps_counties\n_daily.csv\n5,479 x 47", "#1e40af")
arrow(0.27, 0.72, 0.38, 0.72, "3.1 min")
arrow(0.62, 0.72, 0.73, 0.72, "<30 s")

box(0.38, 0.32, 0.24, 0.16, "build_weekly\n_rainfall.py", "#1e40af")
box(0.73, 0.32, 0.22, 0.16, "county_weekly\n_rainfall.csv\n19,599 rows", "#1e40af")
arrow(0.84, 0.62, 0.84, 0.48)
arrow(0.62, 0.40, 0.73, 0.40, "<30 s")

ax.text(0.05, 0.20, "TIER 2 - Monthly composite (deeper signal)",
        fontsize=12, fontweight="bold", color="#166534")
box(0.05, -0.12, 0.22, 0.20, "Sentinel-2 NDVI\nGEE, 96 months", "#16a34a")
box(0.38, -0.12, 0.24, 0.20, "build_county\n_monthly_panel.py", "#16a34a")
box(0.73, -0.12, 0.22, 0.20, "county_monthly\n_stress.csv\nMASTER", "#166534")
arrow(0.27, -0.02, 0.38, -0.02)
arrow(0.62, -0.02, 0.73, -0.02, "<10 s")

ax.set_xlim(0, 1)
ax.set_ylim(-0.25, 1.05)
ax.axis("off")
ax.set_title("Two-tier pipeline: weekly rainfall + monthly composite",
             fontsize=13, loc="left", pad=15)

plt.tight_layout()
out = ROOT / "paper/figures/fig_pipeline_architecture.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
