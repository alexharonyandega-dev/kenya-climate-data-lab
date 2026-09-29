from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent

sev = pd.read_csv(ROOT / "data/processed/severe_2022_by_county.csv")
gdf = gpd.read_file(ROOT / "data/external/kenya_counties.geojson")

# Match column name (shapeName)
county_col = "shapeName" if "shapeName" in gdf.columns else "name"
gdf = gdf.merge(sev, left_on=county_col, right_on="county", how="left")

fig, axes = plt.subplots(1, 2, figsize=(16, 8.5))

def plot_map(ax, flag_col, title, subtitle):
    base = gdf.plot(ax=ax, color="#f1f5f9",
                    edgecolor="white", linewidth=0.5)
    flagged = gdf[gdf[flag_col] == True]
    flagged.plot(ax=ax, color="#dc2626", edgecolor="white", linewidth=0.6)
    ax.set_axis_off()
    ax.set_title(f"{title}\n{subtitle}", fontsize=13, loc="left", pad=12)

plot_map(axes[0], "severe_unweighted",
         "31 counties had severe drought in 2022",
         "Drought severity — any land use")

plot_map(axes[1], "severe_weighted",
         "Only 8 had severe drought while maize was growing",
         "Maize-crop damage specifically")

# Label the 8 on the right panel
eight = gdf[gdf["severe_weighted"] == True]
for _, r in eight.iterrows():
    c = r.geometry.centroid
    ax = axes[1]
    ax.annotate(r[county_col], xy=(c.x, c.y), fontsize=8,
                ha="center", va="center", color="white",
                fontweight="bold", path_effects=[
                    __import__("matplotlib.patheffects", fromlist=["withStroke"])
                    .withStroke(linewidth=2, foreground="#7f1d1d")])

fig.suptitle("The 2022 drought was 31 counties. The 2022 maize crop loss was 8.",
             fontsize=15, x=0.06, ha="left", y=0.97)

plt.tight_layout(rect=[0, 0, 1, 0.94])
out = ROOT / "paper/figures/fig_31_vs_8_map.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved {out}")
