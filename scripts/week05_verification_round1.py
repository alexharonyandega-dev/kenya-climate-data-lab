"""Week 5 verification: production vs yield, all years, with lags."""
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"

# --- KNBS with both production and yield ---
knbs = pd.read_csv(RAW / "knbs_county_agriculture.csv")
knbs["yield_t_ha"] = knbs["Production_Tons"] / knbs["Area_Ha"]
knbs = knbs.rename(columns={"County": "county", "Year": "year"})
knbs = knbs.sort_values(["county", "year"])

# Year-on-year change (percent)
knbs["prod_yoy_pct"]  = knbs.groupby("county")["Production_Tons"].pct_change() * 100
knbs["yield_yoy_pct"] = knbs.groupby("county")["yield_t_ha"].pct_change() * 100
knbs["area_yoy_pct"]  = knbs.groupby("county")["Area_Ha"].pct_change() * 100

print("=== KNBS year-on-year, all counties ===\n")
print(knbs[["county", "year", "Area_Ha", "Production_Tons",
            "yield_t_ha", "area_yoy_pct", "prod_yoy_pct", "yield_yoy_pct"]].round(1).to_string(index=False))
print()

# --- Stress yearly aggregates ---
stress = pd.read_csv(PROC / "county_monthly_stress_v3.csv", parse_dates=["month_start"])
stress["year"] = stress["month_start"].dt.year

yearly = stress.groupby(["county", "year"], as_index=False).agg(
    stress_mean        = ("stress_weighted", "mean"),
    stress_min         = ("stress_weighted", "min"),
    stress_std         = ("stress_weighted", "std"),
)

# Growing season only (planting + grain_fill)
growing = stress[stress["crop_stage"].isin(["planting", "grain_fill"])]
growing_yearly = growing.groupby(["county", "year"], as_index=False).agg(
    stress_growing_mean = ("stress_weighted", "mean"),
    stress_growing_min  = ("stress_weighted", "min"),
)

panel = knbs.merge(yearly, on=["county", "year"], how="inner") \
            .merge(growing_yearly, on=["county", "year"], how="left")

print("=== Combined panel (county-year) ===\n")
print(panel[["county", "year", "prod_yoy_pct", "yield_yoy_pct",
             "stress_mean", "stress_growing_mean"]].round(2).to_string(index=False))
print()

# --- Correlations (all county-years) ---
def corr(df, x, y, label):
    valid = df.dropna(subset=[x, y])
    if len(valid) < 5:
        print(f"  {label:40s}  n<5, skipped")
        return
    r, p = pearsonr(valid[x], valid[y])
    print(f"  {label:40s}  r = {r:+.3f}  p = {p:.3f}  n = {len(valid)}")

print("=== Correlations (all county-years, 2021-2024) ===")
corr(panel, "stress_mean",         "prod_yoy_pct",  "stress_mean vs production YoY")
corr(panel, "stress_mean",         "yield_yoy_pct", "stress_mean vs yield YoY")
corr(panel, "stress_growing_mean", "prod_yoy_pct",  "stress_growing_mean vs production YoY")
corr(panel, "stress_growing_mean", "yield_yoy_pct", "stress_growing_mean vs yield YoY")
print()

# --- 2022 only ---
p22 = panel[panel["year"] == 2022]
print("=== Correlations (2022 only, n=5) ===")
corr(p22, "stress_mean",         "prod_yoy_pct",  "2022 stress_mean vs production")
corr(p22, "stress_mean",         "yield_yoy_pct", "2022 stress_mean vs yield")
corr(p22, "stress_growing_mean", "prod_yoy_pct",  "2022 stress_growing vs production")
corr(p22, "stress_growing_mean", "yield_yoy_pct", "2022 stress_growing vs yield")
print()

# --- Lag test: 2022 stress vs 2023 yield ---
p22["stress_mean_next"] = p22.groupby("county")["stress_mean"].shift(0)  # placeholder
panel_lag = panel.sort_values(["county", "year"]).copy()
panel_lag["stress_next_year"] = panel_lag.groupby("county")["stress_mean"].shift(-1)
lag = panel_lag.dropna(subset=["stress_next_year", "prod_yoy_pct"])
print("=== Lagged: 2022 stress vs 2023 production change ===")
corr(lag, "stress_next_year", "prod_yoy_pct", "stress(t) vs production(t+1)")
