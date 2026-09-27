"""Aggregate daily CHIRPS rainfall to weekly, compute anomalies."""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"

IN = PROC / "chirps_counties_daily_2010_2024.csv"
OUT = PROC / "county_weekly_rainfall_2017_2024.csv"

print("Loading daily CHIRPS...")
df = pd.read_csv(IN, parse_dates=["date"])
print(f"  Rows: {len(df)}, columns: {df.shape[1]}")

df = df[(df["date"] >= "2017-01-01") & (df["date"] <= "2024-12-31")].copy()
print(f"  After 2017-2024 filter: {len(df)}")

df["iso_year"] = df["date"].dt.isocalendar().year.astype(int)
df["iso_week"] = df["date"].dt.isocalendar().week.astype(int)

counties = [c for c in df.columns if c not in ("date", "iso_year", "iso_week")]
print(f"  Counties: {len(counties)}")

print("\nAggregating to weekly totals...")
weekly = df.groupby(["iso_year", "iso_week"])[counties].sum().reset_index()

weekly_long = weekly.melt(
    id_vars=["iso_year", "iso_week"],
    value_vars=counties,
    var_name="county",
    value_name="rainfall_mm",
)

print("Computing per-county per-week climatology (8-year mean)...")
clim = weekly_long.groupby(["county", "iso_week"])["rainfall_mm"].agg(
    ["mean", "std", "count"]
).reset_index()
clim.columns = ["county", "iso_week", "rain_clim_mean", "rain_clim_std", "n_years"]

weekly_long = weekly_long.merge(clim, on=["county", "iso_week"], how="left")

weekly_long["rainfall_anomaly"] = (
    (weekly_long["rainfall_mm"] - weekly_long["rain_clim_mean"]) /
    weekly_long["rain_clim_std"].replace(0, np.nan)
)

# Filter out ISO-year edge rows (Jan 1-3 -> prior year; Dec 30-31 -> next year)
# Keeps only ISO years 2017-2024. Added to fix script/file drift discovered
# in the reproducibility audit (2026-09-27).
weekly_long = weekly_long[
    (weekly_long["iso_year"] >= 2017) & (weekly_long["iso_year"] <= 2024)
].copy()

weekly_long = weekly_long.sort_values(["county", "iso_year", "iso_week"]).reset_index(drop=True)

weekly_long["rainfall_anomaly_4wk"] = (
    weekly_long.groupby("county")["rainfall_anomaly"]
    .transform(lambda s: s.rolling(4, min_periods=2).mean())
)

weekly_long.to_csv(OUT, index=False)
print(f"\nWrote {OUT}")
print(f"  Rows: {len(weekly_long)}")
print(f"  Counties: {weekly_long['county'].nunique()}")

print("\n2022 weekly national 4-week anomaly:")
nat = weekly_long.groupby(["iso_year", "iso_week"])["rainfall_anomaly_4wk"].mean().reset_index()
y22 = nat[nat["iso_year"] == 2022]
for _, r in y22.iterrows():
    bar = "#" * max(0, int((r["rainfall_anomaly_4wk"] + 2) * 8))
    print(f"  W{int(r['iso_week']):02d}  {r['rainfall_anomaly_4wk']:>+6.2f}  {bar}")

print("\nYearly mean 4-week anomaly:")
yearly = weekly_long.groupby("iso_year")["rainfall_anomaly_4wk"].mean().round(3)
print(yearly.to_string())
