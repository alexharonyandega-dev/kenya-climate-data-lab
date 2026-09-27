"""Extract daily rainfall for all 47 Kenyan counties from CHIRPS GeoTIFFs.

Precomputes pixel masks per county once, then streams over every daily
file computing the spatial mean inside each county polygon.

Output: data/processed/chirps_counties_daily_2010_2024.csv
        (one row per day, one column per county)
"""
import gzip
import time
from datetime import date, timedelta
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from affine import Affine
from rasterio.features import geometry_mask
from rasterio.io import MemoryFile
from shapely.geometry import mapping

ROOT = Path(__file__).resolve().parent.parent
CHIRPS_DIR = ROOT / "data" / "raw" / "chirps_daily"
BOUNDARIES = ROOT / "data" / "external" / "kenya_counties.geojson"
OUT = ROOT / "data" / "processed" / "chirps_counties_daily_2010_2024.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

# CHIRPS Africa tile constants (from our earlier diagnostics)
TILE_TOP_LAT = 40.0
TILE_LEFT_LON = -20.0
PIXEL_SIZE = 0.05
TILE_HEIGHT = 1600
TILE_WIDTH = 1500

START = date(2010, 1, 1)
END = date(2024, 12, 31)

print(f"Loading boundaries from {BOUNDARIES.name}...")
gdf = gpd.read_file(BOUNDARIES)
print(f"  {len(gdf)} counties")

# Precompute pixel indices for each county
print("Precomputing county pixel masks...")
county_masks = {}

for _, row in gdf.iterrows():
    county = row["shapeName"]
    geom = row["geometry"]
    minx, miny, maxx, maxy = geom.bounds

    # Convert geographic bounds to pixel indices in the tile
    r0 = max(0, int((TILE_TOP_LAT - maxy) / PIXEL_SIZE))
    r1 = min(TILE_HEIGHT, int((TILE_TOP_LAT - miny) / PIXEL_SIZE) + 1)
    c0 = max(0, int((minx - TILE_LEFT_LON) / PIXEL_SIZE))
    c1 = min(TILE_WIDTH, int((maxx - TILE_LEFT_LON) / PIXEL_SIZE) + 1)

    sub_h, sub_w = r1 - r0, c1 - c0
    sub_transform = Affine(
        PIXEL_SIZE, 0, TILE_LEFT_LON + c0 * PIXEL_SIZE,
        0, -PIXEL_SIZE, TILE_TOP_LAT - r0 * PIXEL_SIZE,
    )

    mask = geometry_mask(
        [mapping(geom)],
        out_shape=(sub_h, sub_w),
        transform=sub_transform,
        invert=True,
    )
    sr, sc = np.where(mask)
    county_masks[county] = (sr + r0, sc + c0)
    print(f"  {county:20s} {len(sr):>6d} px")

county_names = sorted(county_masks.keys())

# Resume support: check existing output
start_date = START
existing = pd.DataFrame()
if OUT.exists():
    existing = pd.read_csv(OUT, parse_dates=["date"])
    if len(existing) > 0:
        last = existing["date"].max().date()
        start_date = last + timedelta(days=1)
        print(f"\nResuming from {start_date} ({len(existing)} rows already done)")

print(f"\nProcessing {start_date} to {END}...")
records = []
d = start_date
t0 = time.time()
n = 0

while d <= END:
    fname = f"chirps-v2.0.{d.year}.{d.month:02d}.{d.day:02d}.tif.gz"
    path = CHIRPS_DIR / str(d.year) / fname
    row_data = {"date": d.strftime("%Y-%m-%d")}

    if not path.exists():
        for c in county_names:
            row_data[c] = np.nan
    else:
        try:
            with gzip.open(path, "rb") as f:
                data = f.read()
            with MemoryFile(data) as mem:
                with mem.open() as src:
                    arr = src.read(1).astype("float32")
                    arr[arr == -9999] = np.nan
            for county in county_names:
                r, c = county_masks[county]
                if len(r) > 0:
                    row_data[county] = float(np.nanmean(arr[r, c]))
                else:
                    row_data[county] = np.nan
        except Exception as e:
            print(f"  FAILED {fname}: {e}")
            for c in county_names:
                row_data[c] = np.nan

    records.append(row_data)
    n += 1

    if n % 200 == 0:
        elapsed = time.time() - t0
        rate = n / elapsed
        remaining = (END - d).days
        eta = remaining / rate / 60 if rate > 0 else 0
        print(f"  {n:>5d} days | {rate:.1f}/s | eta {eta:.1f}min")

    d += timedelta(days=1)

new_df = pd.DataFrame(records)
final = pd.concat([existing, new_df], ignore_index=True) if len(existing) else new_df
final.to_csv(OUT, index=False)

print(f"\nWrote {OUT}")
print(f"  Rows: {len(final)}")
print(f"  Counties: {len(county_names)}")
print(f"  Time: {(time.time()-t0)/60:.1f} min")
print()
print("Sample (first 3 rows, first 5 counties):")
print(final[["date"] + county_names[:5]].head(3).to_string(index=False))
