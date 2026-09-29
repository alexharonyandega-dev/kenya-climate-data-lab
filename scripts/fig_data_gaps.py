from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# --- Panel A: CHIRPS monthly coverage ---
chirps = pd.read_csv(ROOT / "data/processed/chirps_counties_daily_2010_2024.csv")
date_col = chirps.columns[0]
chirps[date_col] = pd.to_datetime(chirps[date_col])
chirps["year"] = chirps[date_col].dt.year
chirps["month"] = chirps[date_col].dt.month

per_month = chirps.groupby(["year","month"])[date_col].nunique().reset_index()
per_month.columns = ["year","month","days"]
pivot = per_month.pivot(index="year", columns="month", values="days")

im = axes[0].imshow(pivot.values, cmap="RdYlGn", vmin=0, vmax=31, aspect="auto")
axes[0].set_xticks(range(12))
axes[0].set_xticklabels(["J","F","M","A","M","J","J","A","S","O","N","D"])
axes[0].set_yticks(range(len(pivot.index)))
axes[0].set_yticklabels(pivot.index, fontsize=8)
axes[0].set_title("CHIRPS daily coverage by month\n(red = missing days)",
                  fontsize=11, loc="left")
plt.colorbar(im, ax=axes[0], label="Days present", fraction=0.046)

# --- Panel B: NDVI missing months per county ---
ndvi = pd.read_csv(ROOT / "data/processed/ndvi_counties_monthly_2017_2024.csv")
missing = ndvi.groupby("name")["mean"].apply(lambda s: s.isna().sum())
missing = missing[missing > 0].sort_values(ascending=False)

if len(missing) > 0:
    missing.plot(kind="bar", ax=axes[1], color="#dc2626", edgecolor="white")
    axes[1].set_ylabel("Missing months (of 96)")
    axes[1].set_xlabel("")
    axes[1].set_title(f"NDVI missing months by county\n({len(missing)} counties affected)",
                      fontsize=11, loc="left")
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)
    plt.setp(axes[1].get_xticklabels(), rotation=60, ha="right", fontsize=7)
else:
    axes[1].text(0.5, 0.5, "No missing NDVI months detected",
                 ha="center", va="center", fontsize=14, color="#16a34a")
    axes[1].axis("off")

plt.tight_layout()
out = ROOT / "paper/figures/fig_data_gaps.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
print(f"Counties with missing NDVI: {len(missing)}")
