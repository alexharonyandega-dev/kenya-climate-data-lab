"""Test three aggregations of stress_weighted against 2022 KNBS yield change."""
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"

# KNBS yield 2021 vs 2022
knbs = pd.read_csv(RAW / "knbs_county_agriculture.csv")
knbs["yield_t_ha"] = knbs["Production_Tons"] / knbs["Area_Ha"]
knbs = knbs.rename(columns={"County": "county", "Year": "year"})
y = knbs.pivot(index="county", columns="year", values="yield_t_ha")
y["pct_change"] = ((y[2022] - y[2021]) / y[2021] * 100).round(1)

# Stress, 2022
stress = pd.read_csv(PROC / "county_monthly_stress_v3.csv", parse_dates=["month_start"])
s22 = stress[stress["month_start"].dt.year == 2022].copy()

# Three aggregations
agg = s22.groupby("county").agg(
    mean_all        = ("stress_weighted", "mean"),
    min_all         = ("stress_weighted", "min"),
    weighted_mean   = ("stress_weighted", lambda x: x.mean()),
).round(3)

# Weighted-by-crop-stage: only growing-season months
growing = s22[s22["crop_stage"].isin(["planting", "grain_fill"])]
agg["growing_season_mean"] = growing.groupby("county")["stress_weighted"].mean().round(3)

# Combine with yield
combined = y.join(agg, how="inner")

print("=== Aggregation test, 2022 ===\n")
print(combined[["pct_change", "mean_all", "min_all", "growing_season_mean"]].to_string())
print()

print("=== Correlations with yield pct_change ===\n")
for col in ["mean_all", "min_all", "growing_season_mean"]:
    valid = combined.dropna(subset=[col, "pct_change"])
    if len(valid) >= 3:
        r, p = pearsonr(valid[col], valid["pct_change"])
        direction = "correct (more drought → more loss)" if r > 0 else "WRONG SIGN"
        print(f"  {col:25s}  r = {r:+.3f}  p = {p:.3f}  → {direction}")
    else:
        print(f"  {col:25s}  insufficient data")
