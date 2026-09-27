"""Build merged_dataset_v1.csv — yield-model-compatible sidecar.

This is an optional sidecar. The project's primary master table is
county_monthly_stress_2017_2024.csv. This file preserves the plan's
original vocabulary for anyone wanting to attempt yield prediction.

Grain: one row per (county, year, season)
Columns:
  county | year | season
  rainfall_mm        seasonal total (from CHIRPS county daily)
  rainfall_anomaly   from the monthly panel (aggregated)
  mean_temp_c        seasonal mean (from ERA5 t2m)
  ndvi_mean          seasonal mean (from monthly NDVI)
  yield_t_ha         from Kaggle maize dataset (where available)
  season_year        handles short-rains January shift

The yield column is left as NaN where no Kaggle data exists for that
(county, year, season).
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"

# --- Load sources ---
print("Loading sources...")
rain_daily = pd.read_csv(PROC / "chirps_counties_daily_2010_2024.csv", parse_dates=["date"])
temp_panel = pd.read_csv(PROC / "county_monthly_panel_2017_2024.csv")
ndvi = pd.read_csv(PROC / "ndvi_counties_monthly_2017_2024.csv")
kaggle = pd.read_csv(RAW / "kaggle_kenyan_maize.csv")

print(f"  CHIRPS daily:      {rain_daily.shape}")
print(f"  Monthly panel:     {temp_panel.shape}")
print(f"  NDVI monthly:      {ndvi.shape}")
print(f"  Kaggle (raw):      {kaggle.shape}")

# --- Seasons ---
LONG_RAINS = [3, 4, 5, 6, 7, 8]
SHORT_RAINS = [10, 11, 12, 1]

def month_to_season(m):
    if m in LONG_RAINS: return "long_rains"
    if m in SHORT_RAINS: return "short_rains"
    return None

def season_year(y, m):
    return y - 1 if m == 1 else y

# --- Aggregate CHIRPS daily to seasonal ---
rain_long = rain_daily.melt(
    id_vars=["date"], var_name="county", value_name="rainfall_mm"
)
rain_long["year"] = rain_long["date"].dt.year
rain_long["month"] = rain_long["date"].dt.month
rain_long["season"] = rain_long["month"].apply(month_to_season)
rain_long["season_year"] = [
    season_year(y, m) for y, m in zip(rain_long["year"], rain_long["month"])
]

rain_season = (
    rain_long.dropna(subset=["season"])
    .groupby(["county", "season_year", "season"])["rainfall_mm"]
    .sum()
    .reset_index()
)
print(f"\nRain seasonal: {rain_season.shape}")

# --- Seasonal mean temperature (from panel) ---
temp_season = (
    temp_panel.dropna(subset=["season"])
    .groupby(["county", "year", "season"])
    .agg(
        rainfall_anomaly_mean=("rainfall_anomaly", "mean"),
        ndvi_season_mean=("ndvi", "mean"),
        ndvi_anomaly_mean=("ndvi_anomaly", "mean"),
    )
    .reset_index()
)
# The panel has already aggregated rainfall into monthly. We use the CHIRPS daily total
# above as the definitive seasonal total, not the panel's monthly sum.

# --- Merge seasonal rainfall + seasonal panel aggregates ---
merged = rain_season.merge(
    temp_season,
    left_on=["county", "season_year", "season"],
    right_on=["county", "year", "season"],
    how="outer",
)
# Prefer CHIRPS-derived year where available
merged["year"] = merged["season_year"].fillna(merged["year"])
merged = merged.drop(columns=["season_year"])

# --- Add ERA5 temperature (seasonal mean) ---
print("Loading ERA5 temperature...")
era5_files = sorted((ROOT / "data" / "raw" / "era5_variables").glob("era5_t2m_*.nc"))
try:
    import xarray as xr
    import geopandas as gpd
    from rasterio.features import geometry_mask
    from shapely.geometry import mapping
    from affine import Affine

    BOUNDARIES = ROOT / "data" / "external" / "kenya_counties.geojson"
    gdf = gpd.read_file(BOUNDARIES)

    all_temp = []
    for f in era5_files:
        ds = xr.open_dataset(f)
        var = "t2m"
        arr = ds[var].values - 273.15
        lats = ds["latitude"].values
        lons = ds["longitude"].values
        times = ds["valid_time"].values

        for _, row in gdf.iterrows():
            county = row["shapeName"]
            geom = mapping(row["geometry"])
            ny, nx = arr.shape[1], arr.shape[2]
            transform = Affine(
                lons[1] - lons[0], 0, lons[0] - (lons[1] - lons[0]) / 2,
                0, lats[1] - lats[0], lats[0] - (lats[1] - lats[0]) / 2,
            )
            # If latitude descending, adjust
            if lats[0] > lats[-1]:
                transform = Affine(
                    lons[1] - lons[0], 0, lons[0] - (lons[1] - lons[0]) / 2,
                    0, lats[1] - lats[0], lats[0] + (lats[0] - lats[1]) / 2,
                )
            mask = geometry_mask([geom], out_shape=(ny, nx),
                                 transform=transform, invert=True)
            # Take per-timestep mean over the county pixels
            county_mean = np.nanmean(arr[:, mask], axis=1)
            for t, v in zip(times, county_mean):
                all_temp.append({
                    "county": county,
                    "date": str(t)[:10],
                    "t2m_c": float(v),
                })
        ds.close()

    temp_df = pd.DataFrame(all_temp)
    temp_df["date"] = pd.to_datetime(temp_df["date"])
    temp_df["year"] = temp_df["date"].dt.year
    temp_df["month"] = temp_df["date"].dt.month
    temp_df["season"] = temp_df["month"].apply(month_to_season)
    temp_df["season_year"] = [
        season_year(y, m) for y, m in zip(temp_df["year"], temp_df["month"])
    ]
    temp_season_mean = (
        temp_df.dropna(subset=["season"])
        .groupby(["county", "season_year", "season"])["t2m_c"]
        .mean()
        .reset_index()
        .rename(columns={"t2m_c": "mean_temp_c"})
    )
    merged = merged.merge(
        temp_season_mean,
        left_on=["county", "year", "season"],
        right_on=["county", "season_year", "season"],
        how="left",
    )
    merged = merged.drop(columns=["season_year"])
    print(f"  After ERA5 merge: {merged.shape}")
except Exception as e:
    print(f"  ERA5 aggregation skipped: {e}")
    merged["mean_temp_c"] = np.nan

# --- Add Kaggle yield (national by year) ---
kaggle_clean = kaggle.copy()
if "Area" in kaggle_clean.columns:
    kaggle_clean = kaggle_clean[kaggle_clean["Area"] == "Kenya"]
if "hg/ha_yield" in kaggle_clean.columns:
    kaggle_clean["yield_t_ha"] = kaggle_clean["hg/ha_yield"] / 10000

# Kaggle is national-scale (same value for all counties in a year).
# Repeat it per county as a placeholder for national reference.
kaggle_nat = kaggle_clean[["Year", "yield_t_ha"]].rename(columns={"Year": "year"})
merged = merged.merge(kaggle_nat, on="year", how="left")

# --- Finalize ---
merged = merged.sort_values(["county", "year", "season"]).reset_index(drop=True)
merged = merged[[
    "county", "year", "season",
    "rainfall_mm",
    "rainfall_anomaly_mean",
    "mean_temp_c",
    "ndvi_season_mean",
    "ndvi_anomaly_mean",
    "yield_t_ha",
]]
merged = merged.rename(columns={
    "rainfall_anomaly_mean": "rainfall_anomaly",
    "ndvi_season_mean": "ndvi_mean",
    "ndvi_anomaly_mean": "ndvi_anomaly",
})

out = PROC / "merged_dataset_v1.csv"
merged.to_csv(out, index=False)
print(f"\nWrote {out}")
print(f"  Rows: {len(merged)}")
print(f"  Columns: {list(merged.columns)}")
print()
print("Sample:")
print(merged.head(10).to_string(index=False))
