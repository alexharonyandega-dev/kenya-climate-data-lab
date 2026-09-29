from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parent.parent
cal = pd.read_csv(ROOT / "data/metadata/kenya_crop_calendar.csv")

counties = ["Trans Nzoia", "Kakamega"]
month_names = ["J","F","M","A","M","J","J","A","S","O","N","D"]

fig, ax = plt.subplots(figsize=(12, 4.5))

for i, county in enumerate(counties):
    row = cal[cal["county"] == county].iloc[0]
    y = 1 - i

    # Long rains
    for m in range(int(row["long_rains_start"]), int(row["long_rains_end"]) + 1):
        ax.add_patch(mpatches.Rectangle((m - 0.45, y - 0.3), 0.9, 0.6,
            facecolor="#16a34a", alpha=0.85, edgecolor="white"))
    # Short rains
    if pd.notna(row.get("short_rains_start")):
        for m in range(int(row["short_rains_start"]), int(row["short_rains_end"]) + 1):
            ax.add_patch(mpatches.Rectangle((m - 0.45, y - 0.3), 0.9, 0.6,
                facecolor="#3b82f6", alpha=0.85, edgecolor="white"))
    # Harvest
    if pd.notna(row.get("primary_harvest_month")):
        h = int(row["primary_harvest_month"])
        ax.add_patch(mpatches.Rectangle((h - 0.45, y - 0.3), 0.9, 0.6,
            facecolor="#f59e0b", alpha=0.95, edgecolor="white"))

    ax.text(-0.8, y, county, fontsize=12, ha="right", va="center",
            fontweight="bold")

# October marker
ax.axvline(10, color="#dc2626", linestyle="--", linewidth=2.5, zorder=0)
ax.text(10, 2.15, "October", fontsize=11, color="#dc2626",
        fontweight="bold", ha="center")

# Annotations for the two panels
ax.annotate("dry is good — maize already harvested",
            xy=(10, 1.35), xytext=(6.2, 1.55),
            fontsize=10, color="#166534", style="italic",
            arrowprops=dict(arrowstyle="->", color="#166534", lw=1.2))
ax.annotate("dry is catastrophic — short-rains planting",
            xy=(10, 0.35), xytext=(4.8, 0.0),
            fontsize=10, color="#dc2626", style="italic",
            arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.2))

ax.set_xlim(-4.5, 13.5)
ax.set_ylim(-0.7, 2.3)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names, fontsize=11)
ax.set_yticks([])
ax.set_xlabel("Month", fontsize=11)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_title("Same dry October. Opposite consequences.",
             fontsize=14, loc="left", pad=15)

legend_items = [
    mpatches.Patch(facecolor="#16a34a", alpha=0.85, label="Long rains"),
    mpatches.Patch(facecolor="#3b82f6", alpha=0.85, label="Short rains"),
    mpatches.Patch(facecolor="#f59e0b", alpha=0.95, label="Harvest"),
]
ax.legend(handles=legend_items, loc="upper right",
          frameon=False, ncol=3, fontsize=10)

plt.tight_layout()
out = ROOT / "paper/figures/fig_crop_calendar_compare.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved {out}")
