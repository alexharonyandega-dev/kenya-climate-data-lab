"""Compute composite stress index for each county-month.

Combines rainfall_anomaly and ndvi_anomaly into:
- stress_avg: weighted average (NDVI weighted higher — it's the integrated signal)
- stress_min: minimum of the two (conservative, matches operational early-warning)
- stress_category: 5-tier label for public outputs

Input:  data/processed/county_monthly_panel_2017_2024.csv
Output: data/processed/county_monthly_stress_2017_2024.csv
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"

IN = PROC / "county_monthly_panel_2017_2024.csv"
OUT = PROC / "county_monthly_stress_2017_2024.csv"

print("Loading panel...")
panel = pd.read_csv(IN)
print(f"  Rows: {len(panel)}")

# Weights: NDVI higher because it integrates soil moisture + crop response
W_RAIN = 0.35
W_NDVI = 0.65

# Composite stress
panel["stress_avg"] = (
    W_RAIN * panel["rainfall_anomaly"] + W_NDVI * panel["ndvi_anomaly"]
)
panel["stress_min"] = panel[["rainfall_anomaly", "ndvi_anomaly"]].min(axis=1)

# Propagate NaN: if either component is missing, stress is missing
either_nan = panel["rainfall_anomaly"].isna() | panel["ndvi_anomaly"].isna()
panel.loc[either_nan, "stress_avg"] = np.nan
panel.loc[either_nan, "stress_min"] = np.nan

# 5-tier classification on stress_avg
def classify(x):
    if pd.isna(x):
        return "no_data"
    if x < -1.25:
        return "severe_stress"
    if x < -0.50:
        return "moderate_stress"
    if x < 0.50:
        return "normal"
    if x < 1.25:
        return "good"
    return "very_good"

panel["stress_category"] = panel["stress_avg"].apply(classify)

# Order columns
panel = panel[[
    "county", "year", "month", "date", "season",
    "rainfall_mm", "rainfall_anomaly",
    "ndvi", "ndvi_anomaly",
    "stress_avg", "stress_min", "stress_category",
]]

panel.to_csv(OUT, index=False)
print(f"\nWrote {OUT}")
print(f"  Rows: {len(panel)}")
print(f"  Columns: {list(panel.columns)}")

# Distribution check
print("\nStress category distribution (2017-2024):")
counts = panel["stress_category"].value_counts()
total = len(panel)
for cat in ["severe_stress", "moderate_stress", "normal", "good", "very_good", "no_data"]:
    n = counts.get(cat, 0)
    print(f"  {cat:18s}  {n:>5d}  ({100*n/total:>5.1f}%)")

# Drought year check — how many severe months in 2022?
print("\nSevere stress months by year (should peak in 2022):")
yearly = panel[panel["stress_category"] == "severe_stress"].groupby("year").size()
for y in range(2017, 2025):
    n = yearly.get(y, 0)
    print(f"  {y}: {n:>3d} county-months")

# Sample: how does stress vary across counties in Oct 2022?
print("\nOct 2022 — stress_avg by county (sorted):")
oct22 = panel[(panel["year"] == 2022) & (panel["month"] == 10)].sort_values("stress_avg")
print(oct22[["county", "rainfall_anomaly", "ndvi_anomaly", "stress_avg", "stress_category"]].round(3).to_string(index=False))
