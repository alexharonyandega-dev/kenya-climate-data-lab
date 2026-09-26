"""Download all 9 essential ERA5-Land variables for Kenya, 1990-2024.

Extended from 2010-2024 to 1990-2024 to match Kaggle maize yield start year.
Reads from Earth Data Hub Zarr store. Skips files that already cover the range.
"""
import os
import time
from pathlib import Path

import xarray as xr

URL = "https://api.earthdatahub.destine.eu/era5/era5-land-daily-utc-v1.zarr"
VARIABLES = [
    "t2m", "d2m", "ssrd", "swvl1", "swvl2", "tp", "u10", "v10", "pev",
]
KENYA = dict(
    latitude=slice(5.0, -4.7),
    longitude=slice(33.9, 41.9),
    valid_time=slice("1990-01-01", "2024-12-31"),
)

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "era5_variables"
OUT_DIR.mkdir(parents=True, exist_ok=True)

print("Opening Earth Data Hub Zarr store...")
ds = xr.open_dataset(
    URL,
    storage_options={"client_kwargs": {"trust_env": True}},
    chunks={},
    engine="zarr",
    zarr_format=3,
)
print(f"  Store opened. Variables: {list(ds.data_vars)}")

for var in VARIABLES:
    if var not in ds.data_vars:
        print(f"  MISSING: {var}")
        continue

    out_path = OUT_DIR / f"era5_{var}_1990_2024.nc"
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
