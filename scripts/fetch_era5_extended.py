"""Download all 9 essential ERA5-Land variables for the Kenya bbox.

Reads from the Earth Data Hub Zarr store (no queue, no rate limits).
Saves each variable as a separate compressed NetCDF file to stay under
the GitHub 100 MB per-file limit.
"""
import os
import time
from pathlib import Path

import xarray as xr

# --- Config ---
URL = "https://api.earthdatahub.destine.eu/era5/era5-land-daily-utc-v1.zarr"
VARIABLES = [
    "t2m",    # 2m temperature (already had, re-download with the rest)
    "d2m",    # 2m dewpoint
    "ssrd",   # surface solar radiation downwards
    "swvl1",  # volumetric soil water layer 1 (topsoil)
    "swvl2",  # volumetric soil water layer 2 (root zone)
    "tp",     # total precipitation
    "u10",    # 10m wind U
    "v10",    # 10m wind V
    "pev",    # potential evaporation
]

KENYA = dict(
    latitude=slice(5.0, -4.7),
    longitude=slice(33.9, 41.9),
    valid_time=slice("2010-01-01", "2024-12-31"),
)

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "era5_variables"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Open the Zarr store once ---
print("Opening Earth Data Hub Zarr store...")
ds = xr.open_dataset(
    URL,
    storage_options={"client_kwargs": {"trust_env": True}},
    chunks={},
    engine="zarr",
    zarr_format=3,
)
print(f"  Store opened. Available variables: {list(ds.data_vars)}")

# --- Download each variable ---
for var in VARIABLES:
    if var not in ds.data_vars:
        print(f"  MISSING in store: {var} — skipping")
        continue

    out_path = OUT_DIR / f"era5_{var}_2010_2024.nc"
    if out_path.exists():
        size_mb = os.path.getsize(out_path) / 1024 / 1024
        print(f"  {var:6s} already exists ({size_mb:.1f} MB) — skipping")
        continue

    t0 = time.time()
    print(f"  {var:6s} downloading...", end=" ", flush=True)

    try:
        sliced = ds[var].sel(**KENYA)
        computed = sliced.compute()
        computed.to_netcdf(
            out_path,
            encoding={var: {"zlib": True, "complevel": 9, "dtype": "float32"}},
        )
        size_mb = os.path.getsize(out_path) / 1024 / 1024
        print(f"OK ({size_mb:.1f} MB, {time.time()-t0:.0f}s)")
    except Exception as e:
        print(f"FAILED: {e}")

print("\nDone.")
