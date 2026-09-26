"""Recompress ERA5 files as int16 with scale_factor metadata.

Halves file size vs float32 without meaningful precision loss.
xarray reads the data back as float automatically.
"""

from pathlib import Path
import os
import xarray as xr

# variable -> (scale_factor, add_offset)
# Chosen so max(abs(data)) < 32000 (int16 max is 32767)
ENCODING = {
    "t2m":   (0.01,     285.0),    # 220-320 K -> -6500 to +3500
    "d2m":   (0.01,     275.0),    # 240-310 K -> -3500 to +3500
    "ssrd":  (1000.0,   17500000.0),  # 0-35M -> -17500 to +17500
    "swvl1": (0.0001,   0.3),      # 0-0.6 -> -3000 to +3000
    "swvl2": (0.0001,   0.3),
    "tp":    (0.00001,  0.075),    # 0-0.15 -> -7500 to +7500
    "u10":   (0.002,    0.0),      # ±30 -> ±15000
    "v10":   (0.002,    0.0),
    "pev":   (0.000001, -0.015),   # -0.03-0 -> -15000 to +15000
}

FOLDER = Path("data/raw/era5_variables")

for f in sorted(FOLDER.glob("era5_*_1990_2024.nc")):
    var = f.stem.split("_")[1]
    if var not in ENCODING:
        print(f"SKIP {f.name} (no encoding rule)")
        continue

    scale, offset = ENCODING[var]
    size_before = os.path.getsize(f) / 1024 / 1024

    print(f"{var:6s} {size_before:6.1f} MB -> ", end="", flush=True)

    # Read, convert, save to temp, rename
    ds = xr.open_dataset(f)
    tmp = f.with_name(f.stem + "_tmp.nc")

    ds.to_netcdf(
        tmp,
        encoding={
            var: {
                "dtype": "int16",
                "scale_factor": scale,
                "add_offset": offset,
                "_FillValue": -32767,
                "zlib": True,
                "complevel": 9,
            }
        },
    )
    ds.close()

    # Replace original
    size_after = os.path.getsize(tmp) / 1024 / 1024
    os.replace(tmp, f)
    print(f"{size_after:6.1f} MB  ({size_after/size_before*100:.0f}%)")

print("\nDone.")
