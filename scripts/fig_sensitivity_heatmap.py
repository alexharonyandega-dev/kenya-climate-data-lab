from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

df = pd.read_csv(ROOT / "data/processed/sensitivity_crop_weights_2022.csv")

# Pivot for grain_fill = 0.7 (our choice)
sub = df[df["grain_fill_weight"] == 0.7]
pivot = sub.pivot(index="harvest_weight", columns="fallow_weight",
                  values="severe_count")

fig, ax = plt.subplots(figsize=(9.5, 6.5))
im = ax.imshow(pivot.values, cmap="RdYlGn_r", vmin=6, vmax=12, aspect="auto")

ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels([f"{c:.2f}" for c in pivot.columns])
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels([f"{i:.2f}" for i in pivot.index])

# Annotate every cell
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        ax.text(j, i, str(int(pivot.values[i, j])),
                ha="center", va="center", fontsize=15,
                color="white", fontweight="bold")

# Circle our choice
our_row = list(pivot.index).index(0.3)
our_col = list(pivot.columns).index(0.0)
ax.scatter([our_col], [our_row], s=900, facecolor="none",
           edgecolor="#1e40af", linewidth=4, zorder=5)
ax.annotate("our choice", xy=(our_col, our_row),
            xytext=(our_col + 1.2, our_row - 1.2),
            fontsize=12, color="#1e40af", fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="#1e40af", lw=1.8))

ax.set_xlabel("fallow weight", fontsize=12)
ax.set_ylabel("harvest weight", fontsize=12)
ax.set_title("2022 severe-count across 28 crop-weight combinations",
             fontsize=13, loc="left", pad=15)

cbar = plt.colorbar(im, ax=ax, label="Severe counties", fraction=0.046)
cbar.ax.tick_params(labelsize=10)

plt.tight_layout()
out = ROOT / "paper/figures/fig_sensitivity_heatmap.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved {out}")
