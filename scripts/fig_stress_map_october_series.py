"""Six-panel map: October stress across Kenya, 2019-2024.

Same month each year, so the seasonal cycle is controlled and the
interannual signal dominates. Shows drought onset (2020 -> 2022) and
recovery (2023 -> 2024).
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
STRESS = ROOT / "data" / "processed" / "county_monthly_stress_2017_2024.csv"
BOUNDS = ROOT / "data" / "external" / "kenya_counties.geojson"
FIG = ROOT / "paper" / "figures" / "fig_stress_october_series.png"

stress = pd.read_csv(STRESS)
counties = gpd.read_file(BOUNDS)

# Merge stress onto geometry
counties = counties.rename(columns={"shapeName": "county"})

years = [2019, 2020, 2021, 2022, 2023, 2024]

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Diverging colormap: red=stress, blue=good
cmap = plt.get_cmap("RdYlBu")
norm = mcolors.Normalize(vmin=-2.5, vmax=2.5)

for ax, year in zip(axes.flat, years):
    oct_data = stress[(stress["year"] == year) & (stress["month"] == 10)]
    merged = counties.merge(oct_data[["county", "stress_avg"]], on="county", how="left")

    merged.plot(
        column="stress_avg",
        ax=ax,
        cmap=cmap,
        norm=norm,
        edgecolor="black",
        linewidth=0.3,
        missing_kwds={"color": "lightgray", "label": "No data"},
    )
    ax.set_title(f"October {year}", fontsize=14, weight="bold")
    ax.axis("off")

# Shared colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=axes, orientation="horizontal",
                    fraction=0.03, pad=0.05, aspect=40)
cbar.set_label("Stress index (negative = stressed)", fontsize=12)

fig.suptitle(
    "Kenya county stress index — October, 2019 to 2024",
    fontsize=16, weight="bold", y=0.98,
)

plt.savefig(FIG, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {FIG}")
