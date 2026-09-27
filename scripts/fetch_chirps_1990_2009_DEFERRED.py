"""Download CHIRPS 2.0 Africa daily files for 1990-2009.

Extends the existing 2010-2024 CHIRPS archive backward to 1990 to match
the Kaggle maize yield dataset's start year.

Files are stored in data/raw/chirps_daily/YYYY/chirps-v2.0.YYYY.MM.DD.tif.gz
and are gitignored (not committed to the repo, only local).
"""
import os
import ssl
import time
import urllib.request
from datetime import date, timedelta
from pathlib import Path

# Use certifi's CA bundle (avoids the SSL issue from the original download)
try:
    import certifi
    ctx = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    ctx = ssl.create_default_context()

BASE = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/"
RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "chirps_daily"

start = date(1990, 1, 1)
end = date(2009, 12, 31)

total_days = (end - start).days + 1
print(f"Downloading CHIRPS {start} to {end} ({total_days} days)")
print(f"Destination: {RAW}")
print()

d = start
count_ok = 0
count_skip = 0
count_fail = 0
t_start = time.time()

while d <= end:
    fname = f"chirps-v2.0.{d.year}.{d.month:02d}.{d.day:02d}.tif.gz"
    url = f"{BASE}{d.year}/{fname}"
    dest_dir = RAW / str(d.year)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / fname

    if dest.exists():
        count_skip += 1
    else:
        try:
            with urllib.request.urlopen(url, context=ctx, timeout=30) as r, open(dest, "wb") as f:
                f.write(r.read())
            count_ok += 1
        except Exception as e:
            count_fail += 1
            print(f"FAILED {fname}: {e}")

    done = count_ok + count_skip
    if done % 100 == 0 and count_ok > 0:
        elapsed = time.time() - t_start
        rate = count_ok / elapsed if elapsed > 0 else 0
        remaining = total_days - done
        eta = remaining / rate / 60 if rate > 0 else 0
        print(f"{done}/{total_days}  ok={count_ok}  skip={count_skip}  fail={count_fail}  "
              f"rate={rate:.1f}/s  eta={eta:.0f}min")

    d += timedelta(days=1)

print()
print(f"DONE. Downloaded {count_ok}, skipped {count_skip}, failed {count_fail}.")
