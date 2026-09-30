"""Does national-mean stress predict national-mean yield across the 5 KNBS counties?"""
from pathlib import Path
import pandas as pd
from scipy.stats import pearsonr

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
RAW  = ROOT / "data" / "raw"

knbs = pd.read_csv(RAW / "knbs_county_agriculture.csv")
knbs["yield_t_ha"] = knbs["Production_Tons"] / knbs["Area_Ha"]
knbs = knbs.rename(columns={"County": "county", "Year": "year"})

# National mean across the 5 KNBS counties
national_yield = knbs.groupby("year").agg(
    yield_mean=("yield_t_ha", "mean"),
    prod_total=("Production_Tons", "sum"),
    area_total=("Area_Ha", "sum"),
).reset_index()
national_yield["prod_yoy"] = national_yield["prod_total"].pct_change() * 100
national_yield["yield_yoy"] = national_yield["yield_mean"].pct_change() * 100

# National mean stress across the SAME 5 counties
stress = pd.read_csv(PROC / "county_monthly_stress_v3.csv", parse_dates=["month_start"])
stress["year"] = stress["month_start"].dt.year
knbs_counties = knbs["county"].unique()
s5 = stress[stress["county"].isin(knbs_counties)]
national_stress = s5.groupby("year").agg(
    stress_mean=("stress_weighted", "mean"),
    stress_growing=("stress_weighted", lambda x: x[s5["crop_stage"].isin(["planting","grain_fill"])].mean()),
).reset_index()

# Join
panel = national_yield.merge(national_stress, on="year", how="inner")
print("=== National panel, 5 KNBS counties ===\n")
print(panel.round(3).to_string(index=False))
print()

# Correlations, excluding NaN YoY for 2020
valid = panel.dropna(subset=["stress_mean", "yield_yoy"])
if len(valid) >= 3:
    r, p = pearsonr(valid["stress_mean"], valid["yield_yoy"])
    print(f"National stress_mean vs national yield YoY:    r = {r:+.3f}  p = {p:.3f}  n = {len(valid)}")

valid = panel.dropna(subset=["stress_mean", "prod_yoy"])
if len(valid) >= 3:
    r, p = pearsonr(valid["stress_mean"], valid["prod_yoy"])
    print(f"National stress_mean vs national production:   r = {r:+.3f}  p = {p:.3f}  n = {len(valid)}")

# Lagged: year t stress vs year t+1 yield
panel["stress_lag"] = panel["stress_mean"].shift(1)
valid = panel.dropna(subset=["stress_lag", "yield_yoy"])
if len(valid) >= 3:
    r, p = pearsonr(valid["stress_lag"], valid["yield_yoy"])
    print(f"Lagged stress(t-1) vs yield(t):                 r = {r:+.3f}  p = {p:.3f}  n = {len(valid)}")
