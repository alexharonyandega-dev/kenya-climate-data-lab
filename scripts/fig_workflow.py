"""Workflow diagram for the preprint draft.

A4 landscape. Three columns: Sources, Processing, Integration.
Arrows show data flow.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "paper/figures/workflow.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(14, 7))
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis("off")

def box(x, y, w, h, title, body, color, fontsize_t=10, fontsize_b=8):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.05",
        linewidth=1.4, edgecolor=color, facecolor=color, alpha=0.12))
    ax.text(x + w/2, y + h - 0.18, title, ha="center", va="top",
            fontsize=fontsize_t, fontweight="bold", color=color)
    ax.text(x + w/2, y + h - 0.45, body, ha="center", va="top",
            fontsize=fontsize_b, color="#374151", linespacing=1.4)

def arrow(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#6b7280", lw=1.4))
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.12, label,
                ha="center", fontsize=7, color="#6b7280", style="italic")

# Column headers
ax.text(1.55, 6.85, "SOURCES", fontsize=11, fontweight="bold",
        color="#1e293b", ha="center")
ax.text(6.5, 6.85, "PROCESSING", fontsize=11, fontweight="bold",
        color="#1e293b", ha="center")
ax.text(11.8, 6.85, "INTEGRATION", fontsize=11, fontweight="bold",
        color="#1e293b", ha="center")

# --- Stage 1: Sources ---
box(0.30, 5.65, 2.50, 0.90, "CHIRPS 2.0",
    "0.05° daily rainfall\n2010–2024 (5,448 files)", "#3b82f6")

box(0.30, 4.55, 2.50, 0.90, "Sentinel-2 NDVI",
    "10 m monthly composites\n2017–2024 (GEE)", "#16a34a")

box(0.30, 3.45, 2.50, 0.90, "ERA5-Land",
    "0.1° daily, 4 variables\n1990–2024 (18 files)", "#0891b2")

box(0.30, 2.35, 2.50, 0.90, "iSDAsoil",
    "30 m soil properties\nstatic, 14 variables", "#a16207")

box(0.30, 1.25, 2.50, 0.90, "Kenya crop calendar",
    "47 counties, 7 zones\ncrop-stage months", "#7c3aed")

# --- Stage 2: Processing ---
box(4.20, 5.65, 3.80, 0.90, "extract_chirps_counties.py",
    "Precomputed pixel masks → county-daily rainfall\nRuntime: 3.1 min for 15 years (D06)",
    "#3b82f6", 9, 7.5)

box(4.20, 4.55, 3.80, 0.90, "ndvi_counties_monthly.js (GEE)",
    "Monthly max-value composite → county-monthly mean\n5.6% cloud gap, left as NaN (D13)",
    "#16a34a", 9, 7.5)

box(4.20, 3.45, 3.80, 0.90, "extract_era5_counties.py",
    "NetCDF → county-daily → monthly anomalies\nRuntime: ~30 min for 5.4M rows",
    "#0891b2", 9, 7.5)

box(4.20, 2.35, 3.80, 0.90, "fetch_isda_soil_raster.py",
    "Zonal stats on cloud-optimized GeoTIFF\n14 properties × 47 counties",
    "#a16207", 9, 7.5)

box(4.20, 1.25, 3.80, 0.90, "build_crop_calendar.py",
    "FEWS NET + FAO + extension → county-stage weights\nFallow 0.0, harvest 0.3, grain 0.7, plant 1.0",
    "#7c3aed", 9, 7.5)

# --- Stage 3: Integration ---
box(9.30, 4.30, 4.40, 2.30, "compute_stress_index.py",
    "County-own-history anomaly\n"
    "(observed − clim_mean) / clim_std\n\n"
    "stress_avg = 0.35×rain + 0.65×ndvi\n"
    "stress_min = min(rain, ndvi)\n"
    "stress_weighted = stress_avg × crop_weight\n\n"
    "Categorised: severe / moderate / normal / good / very_good",
    "#166534", 10, 8)

box(9.30, 2.30, 4.40, 1.20, "county_monthly_stress_v3.csv",
    "MASTER TABLE · 4,512 rows (47 × 96)\n27 columns · all four findings cited from here",
    "#065f46", 10, 8)

box(9.30, 1.00, 4.40, 1.00, "county_weekly_stress_2017_2024.csv",
    "Weekly product · 19,599 rows\nMonthly companions carried forward",
    "#065f46", 10, 8)

# --- Arrows: Sources → Processing ---
for y in [6.10, 5.00, 3.90, 2.80, 1.70]:
    arrow(2.80, y, 4.20, y)

# --- Arrows: Processing → Integration ---
for y in [6.10, 5.00, 3.90, 2.80, 1.70]:
    arrow(8.00, y, 9.30, y)

# --- Arrows: Integration → outputs ---
arrow(11.50, 4.30, 11.50, 3.50)
arrow(11.50, 2.30, 11.50, 2.00)

# Footer
ax.text(0.30, 0.45,
        "Every processing script is reproducible. Every decision is logged in docs/DECISIONS_LOG.md.\n"
        "Full pipeline: github.com/alexharonyandega-dev/kenya-climate-data-lab",
        fontsize=8, color="#6b7280", va="bottom")

plt.tight_layout()
plt.savefig(OUT, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Saved {OUT}")
