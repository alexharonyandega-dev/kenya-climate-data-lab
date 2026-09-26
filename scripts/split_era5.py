"""Split each ERA5 1990-2024 file into two time periods.

Keeps per-file size under GitHub's 100 MB limit without any loss of
resolution or time coverage. Uses the same int16 encoding as the
recompressed source files.
"""
from pathlib import Path
import os
import xarray as xr

# Same encoding as recompress_era5.py (int16 with scale/offset)
ENCODING = {
    "t2m":   (0.01,     285.0),
    "d2m":   (0.01,     275.0),
    "ssrd":  (1000.0,   17500000.0),
    "swvl1": (0.0001,   0.3),
    "swvl2": (0.0001,   0.3),
    "tp":    (0.00001,  0.075),
    "u10":   (0.002,    0.0),
    "v10":   (0.002,    0.0),
    "pev":   (0.000001, -0.015),
}

FOLDER = Path("data/raw/era5_variables")
CUTOFF = "2008-01-01"   # split here

for f in sorted(FOLDER.glob("era5_*_1990_2024.nc")):
    var = f.stem.split("_")[1]
    if var not in ENCODING:
        print(f"SKIP {f.name}")
        continue

    scale, offset = ENCODING[var]
    size_before = os.path.getsize(f) / 1024 / 1024
    print(f"{var:6s} {size_before:6.1f} MB -> ", end="", flush=True)

    ds = xr.open_dataset(f)
    first = ds.sel(valid_time=slice("1990-01-01", "2007-12-31"))
    second = ds.sel(valid_time=slice("2008-01-01", "2024-12-31"))

    f1 = FOLDER / f"era5_{var}_1990_2007.nc"
    f2 = FOLDER / f"era5_{var}_2008_2024.nc"

    enc = {var: {
        "dtype": "int16",
        "scale_factor": scale,
        "add_offset": offset,
        "_FillValue": -32767,
        "zlib": True,
        "complevel": 9,
    }}

    first.to_netcdf(f1, encoding=enc)
    second.to_netcdf(f2, encoding=enc)

    ds.close()
    f.unlink()   # remove the original combined file

    s1 = os.path.getsize(f1) / 1024 / 1024
    s2 = os.path.getsize(f2) / 1024 / 1024
    print(f"{s1:.1f} + {s2:.1f} MB")

print("\nDone.")
