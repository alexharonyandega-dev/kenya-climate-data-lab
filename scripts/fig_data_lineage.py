from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parent.parent

fig, ax = plt.subplots(figsize=(15, 9))

def box(x, y, w, h, text, color, fontsize=9):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.015",
        linewidth=1.3, edgecolor=color, facecolor=color, alpha=0.15))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, color=color, fontweight="bold")

def arrow(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#444444", lw=1.3))
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.02, label,
                ha="center", fontsize=7.5, color="#666666", style="italic")

# Column headers
ax.text(0.10, 0.97, "RAW", fontsize=11, fontweight="bold",
        color="#1e293b", ha="center")
ax.text(0.40, 0.97, "SCRIPTS", fontsize=11, fontweight="bold",
        color="#1e293b", ha="center")
ax.text(0.72, 0.97, "INTERMEDIATE", fontsize=11, fontweight="bold",
        color="#1e293b", ha="center")
ax.text(0.93, 0.97, "FINAL", fontsize=11, fontweight="bold",
        color="#1e293b", ha="center")

# Raw sources
box(0.00, 0.83, 0.19, 0.10, "CHIRPS 2.0\n5,479 daily GeoTIFFs", "#3b82f6", 8)
box(0.00, 0.70, 0.19, 0.10, "Sentinel-2 NDVI\n96 monthly composites (GEE)", "#16a34a", 8)
box(0.00, 0.57, 0.19, 0.10, "ERA5-Land\n18 NetCDF, 9 variables", "#0891b2", 8)
box(0.00, 0.44, 0.19, 0.10, "iSDAsoil\n8 soil properties, 30m", "#a16207", 8)
box(0.00, 0.31, 0.19, 0.10, "Kenya boundaries\n47 counties (geoBoundaries)", "#64748b", 8)
box(0.00, 0.18, 0.19, 0.10, "Crop calendar\n7 agro-ecological zones", "#7c3aed", 8)

# Scripts
box(0.28, 0.83, 0.22, 0.10, "extract_chirps_counties.py\n3.1 min (precomputed masks)", "#3b82f6", 8)
box(0.28, 0.70, 0.22, 0.10, "gee/ndvi_counties_monthly.js\n~20 min (browser)", "#16a34a", 8)
box(0.28, 0.57, 0.22, 0.10, "extract_era5_counties.py\n~30 min (5.4M rows)", "#0891b2", 8)
box(0.28, 0.44, 0.22, 0.10, "fetch_isda_soil_raster.py\nzonal stats", "#a16207", 8)
box(0.28, 0.31, 0.22, 0.10, "(static, no script)\ncommitted as GeoJSON", "#64748b", 8)
box(0.28, 0.18, 0.22, 0.10, "build_crop_calendar.py\n<5 s", "#7c3aed", 8)

# Intermediate
box(0.60, 0.83, 0.22, 0.10, "chirps_counties_daily\n2010_2024.csv", "#3b82f6", 8)
box(0.60, 0.70, 0.22, 0.10, "ndvi_counties_monthly\n2017_2024.csv", "#16a34a", 8)
box(0.60, 0.57, 0.22, 0.10, "era5_counties/\n9 files x 600,848 rows", "#0891b2", 8)
box(0.60, 0.44, 0.22, 0.10, "isda_soil_raster\n_zonal.csv", "#a16207", 8)

# Derived
box(0.60, 0.20, 0.22, 0.10, "county_weekly_rainfall\n2017_2024.csv", "#8b5cf6", 8)
box(0.60, 0.08, 0.22, 0.10, "county_monthly_panel\n2017_2024.csv", "#8b5cf6", 8)

# Final
box(0.85, 0.55, 0.15, 0.13, "county_monthly\n_stress_v3.csv\n\nMASTER\n4,512 x 27", "#166534", 9)
box(0.85, 0.20, 0.15, 0.13, "county_weekly\n_stress\n\n2017_2024\n19,599 x 21", "#166534", 9)

# Arrows: Raw -> Scripts
for y in [0.88, 0.75, 0.62, 0.49, 0.36, 0.23]:
    arrow(0.19, y, 0.28, y)

# Arrows: Scripts -> Intermediate
for y in [0.88, 0.75, 0.62, 0.49]:
    arrow(0.50, y, 0.60, y)

# Arrow: Intermediate -> Derived -> Final
arrow(0.71, 0.83, 0.71, 0.30, "")
arrow(0.71, 0.70, 0.71, 0.30, "")
arrow(0.71, 0.30, 0.71, 0.18, "")
arrow(0.71, 0.18, 0.71, 0.13, "")
arrow(0.71, 0.13, 0.85, 0.13, "")
arrow(0.82, 0.25, 0.85, 0.60, "")

# Calendar direct to final
arrow(0.50, 0.23, 0.60, 0.13, "")
arrow(0.60, 0.13, 0.85, 0.13, "")

ax.set_xlim(-0.02, 1.02)
ax.set_ylim(0.03, 1.02)
ax.axis("off")
ax.set_title("Data lineage - Kenya Climate Data Lab, Week 4",
             fontsize=14, loc="left", pad=10)

plt.tight_layout()
out = ROOT / "paper" / "figures" / "fig_data_lineage.png"
plt.savefig(out, dpi=180, bbox_inches="tight", facecolor="white")
print(f"Saved {out}")
