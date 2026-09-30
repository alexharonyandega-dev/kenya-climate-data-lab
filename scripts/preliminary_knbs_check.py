"""Pre-Week-5: does stress_weighted predict 2022 yield drop in the 5 KNBS counties?"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"

# --- KNBS yield, 2021 vs 2022 ---
knbs = pd.read_csv(RAW / "knbs_county_agriculture.csv")
knbs["yield_t_ha"] = knbs["Production_Tons"] / knbs["Area_Ha"]
knbs = knbs.rename(columns={"County": "county", "Year": "year"})

y = knbs.pivot(index="county", columns="year", values="yield_t_ha")
y["change_2022_vs_2021"] = y[2022] - y[2021]
y["pct_change"] = (y["change_2022_vs_2021"] / y[2021] * 100).round(1)

print("=== KNBS yield (t/ha), 5 counties ===")
print(y[[2021, 2022, "change_2022_vs_2021", "pct_change"]].round(2).to_string())
print()

# --- stress_weighted, 2022 for these counties ---
stress = pd.read_csv(PROC / "county_monthly_stress_v3.csv", parse_dates=["month_start"])
s22 = stress[stress["month_start"].dt.year == 2022]
s22_agg = (s22.groupby("county")
           .agg(mean_stress_weighted=("stress_weighted", "mean"),
                min_stress_weighted=("stress_weighted", "min"),
                mean_crop_weight=("crop_stage_weight", "mean"))
           .round(3))

print("=== stress_weighted, 2022 ===")
print(s22_agg.loc[s22_agg.index.isin(y.index)].to_string())
print()

# --- Merge side by side ---
combined = y.join(s22_agg, how="inner")
combined["yield_down"] = combined["change_2022_vs_2021"] < 0
print("=== Combined view: yield change vs stress ===")
print(combined[[2021, 2022, "pct_change",
                "mean_stress_weighted", "min_stress_weighted", "yield_down"]].to_string())
print()

# --- Correlation ---
import numpy as np
valid = combined.dropna(subset=["mean_stress_weighted", "pct_change"])
if len(valid) >= 3:
    from scipy.stats import pearsonr
    r, p = pearsonr(valid["mean_stress_weighted"], valid["pct_change"])
    print(f"Correlation between mean stress_weighted and % yield change: r = {r:.3f}, p = {p:.3f}, n = {len(valid)}")
else:
    print("Not enough paired observations for correlation")
