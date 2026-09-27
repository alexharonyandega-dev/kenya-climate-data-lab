"""Aggregate ERA5-Land variables to per-county daily means.

Reads each of the 18 ERA5 NetCDF files (9 variables x 2 periods),
applies the precomputed county pixel masks, and writes a long-format
CSV: date, county, variable, value.

For the temperature variable we output Celsius. Others are output in
native ERA5 units (see data_dictionary.md).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
from rasterio.features import geometry_mask
from shapely.geometry import mapping
from affine import Affine

ROOT = Path(__file__).resolve().parent.parent
RAW_ERA5 = ROOT / "data" / "raw" / "era5_variables"
BOUNDARIES = ROOT / "data" / "external" / "kenya_counties.geojson"
OUT = ROOT / "data" / "processed" / "era5_counties_daily.csv"

print("Loading county boundaries...")
gdf = gpd.read_file(BOUNDARIES)
print(f"  {len(gdf)} counties")

records = []

for f in sorted(RAW_ERA5.glob("*.nc")):
    var = f.stem.split("_")[1]  # e.g. "t2m"
    print(f"\nProcessing {f.name} (var={var})...")
    ds = xr.open_dataset(f)
    arr = ds[var].values
    lats = ds["latitude"].values
    lons = ds["longitude"].values
    times = ds["valid_time"].values

    # Convert temperature to Celsius
    if var == "t2m":
        arr = arr - 273.15

    # Build a transform for pixel indexing
    dlat = lats[1] - lats[0]
    dlon = lons[1] - lons[0]
    # Account for descending latitude
    if dlat < 0:
        top = lats[0]
        transform = Affine(dlon, 0, lons[0] - dlon/2,
                           0, dlat, top - dlat/2)
    else:
        transform = Affine(dlon, 0, lons[0] - dlon/2,
                           0, dlat, lats[0] - dlat/2)

    # Precompute mask per county
    county_masks = {}
    for _, row in gdf.iterrows():
        county = row["shapeName"]
        geom = mapping(row["geometry"])
        mask = geometry_mask(
            [geom],
            out_shape=(len(lats), len(lons)),
            transform=transform,
            invert=True,
        )
        county_masks[county] = mask

    # Apply per timestep
    for t_idx, t in enumerate(times):
        date_str = str(t)[:10]
        for county, mask in county_masks.items():
            if mask.sum() == 0:
                continue
            vals = arr[t_idx][mask]
            mean_val = float(np.nanmean(vals))
            records.append({
                "date": date_str,
                "county": county,
                "variable": var,
                "value": mean_val,
            })

    ds.close()
    print(f"  done — {len(records):,} total records so far")

df = pd.DataFrame(records)
df = df.sort_values(["county", "variable", "date"]).reset_index(drop=True)
df.to_csv(OUT, index=False)
print(f"\nWrote {OUT}")
print(f"  Rows: {len(df):,}")
print(f"  Counties: {df['county'].nunique()}")
print(f"  Variables: {sorted(df['variable'].unique())}")
print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
