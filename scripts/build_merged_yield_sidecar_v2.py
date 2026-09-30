"""Build merged_dataset_v1.csv — county-level yield sidecar (KNBS-sourced).

Replaces the broken v1 (Kaggle Cartesian join). Uses KNBS county-level
production + area to compute actual yield per county, per year.

Coverage: 5 counties x 5 years (2020-2024), the KNBS county series.
For the other 42 counties, yield_t_ha is NaN (not fabricated).
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"

# --- Load KNBS (5 counties x 5 years) ---
knbs = pd.read_csv(RAW / "knbs_county_agriculture.csv")
knbs["yield_t_ha"] = knbs["Production_Tons"] / knbs["Area_Ha"]
knbs = knbs.rename(columns={"County": "county", "Year": "year"})
knbs = knbs[["county", "year", "yield_t_ha"]]

print("KNBS yield computed:")
print(knbs.to_string(index=False))
print()

# --- Load climate panel (already county-monthly) ---
panel = pd.read_csv(PROC / "county_monthly_panel_2017_2024.csv")
# panel already has a "year" column - no date parsing needed

# Aggregate to county-year (both seasons averaged)
climate = (panel.groupby(["county", "year"], as_index=False)
           .agg(rainfall_mm=("rainfall_mm", "mean"),
                rainfall_anomaly=("rainfall_anomaly", "mean"),
                ndvi_mean=("ndvi", "mean"),
                ndvi_anomaly=("ndvi_anomaly", "mean")))
print("Climate aggregated to county-year:", climate.shape)
print()

# --- Join ---
merged = climate.merge(knbs, on=["county", "year"], how="left")
print(f"Merged shape: {merged.shape}")
print(f"Rows with yield: {merged['yield_t_ha'].notna().sum()}")
print(f"Rows without yield: {merged['yield_t_ha'].isna().sum()}")
print()

# Sanity: yield should vary by county AND year now
print("Yield by county (mean):")
print(merged.groupby("county")["yield_t_ha"].mean().round(2).to_string())
print()

merged.to_csv(PROC / "merged_dataset_v1.csv", index=False)
print(f"Saved merged_dataset_v1.csv: {merged.shape}")
