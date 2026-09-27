"""Build county-monthly panel: rainfall + NDVI + anomalies.

Steps:
1. Load CHIRPS daily rainfall (5,479 days x 47 counties)
2. Aggregate to monthly totals
3. Load NDVI monthly (96 months x 47 counties)
4. Clip NDVI to [0, 1], flag missing
5. Join on (county, year, month)
6. Compute per-county anomalies for rainfall and NDVI

Output: data/processed/county_monthly_panel_2017_2024.csv
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"

CHIRPS_DAILY = PROC / "chirps_counties_daily_2010_2024.csv"
NDVI_MONTHLY = PROC / "ndvi_counties_monthly_2017_2024.csv"
OUT = PROC / "county_monthly_panel_2017_2024.csv"

print("Loading CHIRPS daily...")
chirps = pd.read_csv(CHIRPS_DAILY, parse_dates=["date"])
print(f"  Shape: {chirps.shape}")

# Aggregate to monthly
chirps["year"] = chirps["date"].dt.year
chirps["month"] = chirps["date"].dt.month
chirps["days_in_month"] = chirps["date"].dt.days_in_month

counties = [c for c in chirps.columns if c not in ("date", "year", "month", "days_in_month")]
print(f"  Counties: {len(counties)}")

# Monthly sum of rainfall (mm)
monthly_rain = chirps.groupby(["year", "month"])[counties].sum().reset_index()

# Reshape to long format
rain_long = monthly_rain.melt(
    id_vars=["year", "month"],
    value_vars=counties,
    var_name="county",
    value_name="rainfall_mm",
)

print(f"\nMonthly rainfall rows: {len(rain_long)}")

print("Loading NDVI monthly...")
ndvi = pd.read_csv(NDVI_MONTHLY)
print(f"  Shape: {ndvi.shape}")

# Standardize columns and types
ndvi = ndvi.rename(columns={"name": "county", "mean": "ndvi"})
ndvi["year"] = ndvi["year"].astype(int)
ndvi["month"] = ndvi["month"].astype(int)

# Clip NDVI to [0, 1] — negatives are water/residual cloud artefacts
ndvi.loc[(ndvi["ndvi"] < 0) | (ndvi["ndvi"] > 1), "ndvi"] = np.nan

print(f"\nJoining on (county, year, month)...")
panel = rain_long.merge(ndvi[["county", "year", "month", "ndvi"]],
                        on=["county", "year", "month"],
                        how="outer")
print(f"  Joined rows: {len(panel)}")

# Restrict to common range 2017-2024
panel = panel[(panel["year"] >= 2017) & (panel["year"] <= 2024)].copy()
print(f"  After year filter 2017-2024: {len(panel)}")

# Add month labels and season
def season(month):
    if month in (3, 4, 5): return "long_rains"
    if month in (10, 11, 12): return "short_rains"
    if month in (6, 7, 8, 9): return "cool_dry"
    return "hot_dry"

panel["season"] = panel["month"].apply(season)
panel["date"] = pd.to_datetime(panel[["year", "month"]].assign(day=1))

# Compute anomalies per county per calendar month
print("\nComputing anomalies per county per month...")

panel = panel.sort_values(["county", "year", "month"]).reset_index(drop=True)

# Rainfall anomaly: (value - climatology_mean) / climatology_std
rain_clim = panel.groupby(["county", "month"])["rainfall_mm"].transform(
    lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0
)
panel["rainfall_anomaly"] = rain_clim

ndvi_clim = panel.groupby(["county", "month"])["ndvi"].transform(
    lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0
)
panel["ndvi_anomaly"] = ndvi_clim

# Reorder columns
panel = panel[["county", "year", "month", "date", "season",
               "rainfall_mm", "rainfall_anomaly",
               "ndvi", "ndvi_anomaly"]]

# Save
panel.to_csv(OUT, index=False)
print(f"\nWrote {OUT}")
print(f"  Rows: {len(panel)}")
print(f"  Columns: {list(panel.columns)}")

print("\nSample (first 10 rows, sorted by county, date):")
print(panel.head(10).to_string(index=False))

print("\nSummary stats:")
print(panel[["rainfall_mm", "rainfall_anomaly", "ndvi", "ndvi_anomaly"]].describe().round(3).to_string())
