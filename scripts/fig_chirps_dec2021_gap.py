"""CHIRPS daily rainfall time series for Kenya, highlighting the Dec 2021 gap.

Reads one CHIRPS GeoTIFF per day from 2021-01-01 to 2022-12-31, masks to
the Kenya bounding box (lat -4.7 to 5.0, lon 33.9 to 41.9), computes the
spatial mean, and plots the resulting daily time series.

The December 2021 archive gap (31 missing days) appears as a visible break.

Results are cached to data/processed/chirps_kenya_daily_2021_2022.csv so
re-runs are instant.
"""

import gzip
import shutil
import tempfile
from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import rasterio
from rasterio.io import MemoryFile

# --- Paths ---
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / 'data' / 'raw'
PROC = ROOT / 'data' / 'processed'
FIG_DIR = ROOT / 'paper' / 'figures'
PROC.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

CACHE = PROC / 'chirps_kenya_daily_2021_2022.csv'

# --- Kenya bounding box in pixel indices ---
# CHIRPS Africa tile: 1600 rows x 1500 cols, bounds (-20, -40, 55, 40), 0.05 deg
# Row index for lat: (40 - lat) / 0.05
# Col index for lon: (lon - (-20)) / 0.05
KENYA_ROW_START = int((40 - 5.0) / 0.05)       # lat 5.0 -> row 700
KENYA_ROW_END   = int((40 - (-4.7)) / 0.05)    # lat -4.7 -> row 894
KENYA_COL_START = int((33.9 - (-20)) / 0.05)   # lon 33.9 -> col 1078
KENYA_COL_END   = int((41.9 - (-20)) / 0.05)   # lon 41.9 -> col 1238


def load_chirps_kenya_mean(gz_path):
    """Read one CHIRPS file, return Kenya-bbox spatial mean (mm/day) or None."""
    try:
        with gzip.open(gz_path, 'rb') as f:
            data = f.read()
        with MemoryFile(data) as memfile:
            with memfile.open() as src:
                arr = src.read(1).astype('float32')
                nodata = src.nodata if src.nodata is not None else -9999
                arr[arr == nodata] = np.nan
                kenya = arr[
                    KENYA_ROW_START:KENYA_ROW_END,
                    KENYA_COL_START:KENYA_COL_END,
                ]
                return float(np.nanmean(kenya))
    except Exception as e:
        print(f'  ERR {gz_path.name}: {e}')
        return None


def build_time_series():
    """Iterate every day 2021-01-01 to 2022-12-31, return DataFrame."""
    start = date(2021, 1, 1)
    end = date(2022, 12, 31)

    rows = []
    d = start
    total_days = (end - start).days + 1
    i = 0
    while d <= end:
        i += 1
        fname = f'chirps-v2.0.{d.year}.{d.month:02d}.{d.day:02d}.tif.gz'
        path = RAW / 'chirps_daily' / str(d.year) / fname

        if not path.exists():
            rows.append({'date': d, 'rainfall_mm': np.nan, 'present': False})
        else:
            mean_mm = load_chirps_kenya_mean(path)
            rows.append({'date': d, 'rainfall_mm': mean_mm, 'present': True})

        if i % 50 == 0:
            print(f'  {i}/{total_days} days processed (up to {d})')
        d += timedelta(days=1)

    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'])
    return df


# --- Build or load cached time series ---
if CACHE.exists():
    print(f'Loading cached time series: {CACHE}')
    df = pd.read_csv(CACHE, parse_dates=['date'])
else:
    print('Processing 699 CHIRPS files (this takes 5-15 minutes)...')
    df = build_time_series()
    df.to_csv(CACHE, index=False)
    print(f'Cached to {CACHE}')

# --- Identify the Dec 2021 gap ---
dec_2021 = df[
    (df['date'] >= '2021-12-01') & (df['date'] <= '2021-12-31')
]
missing = dec_2021[~dec_2021['present']]
n_missing = len(missing)
print(f'\nDecember 2021 missing days: {n_missing}')
print(f'Total days in range: {len(df)}')
print(f'Days with data: {df["present"].sum()}')

# --- Plot ---
fig, ax = plt.subplots(figsize=(14, 5))

# Daily mean as a faint line
ax.plot(df['date'], df['rainfall_mm'], color='#0ea5e9',
        linewidth=0.7, alpha=0.6, label='Daily mean over Kenya')

# 30-day rolling mean to show the seasonal signal clearly
rolling = df.set_index('date')['rainfall_mm'].rolling('30D', min_periods=15).mean()
ax.plot(rolling.index, rolling.values, color='#0369a1',
        linewidth=2, label='30-day rolling mean')

# Highlight the Dec 2021 gap
if n_missing > 0:
    gap_start = pd.Timestamp('2021-12-01')
    gap_end = pd.Timestamp('2021-12-31')
    ax.axvspan(gap_start, gap_end, color='#ef4444', alpha=0.15, zorder=0)
    ax.annotate(
        f'Missing data — {n_missing} days\n(December 2021 archive gap)',
        xy=(gap_start + (gap_end - gap_start) / 2, 12),
        xytext=(pd.Timestamp('2021-08-01'), 14),
        fontsize=11,
        ha='center',
        color='#991b1b',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                  edgecolor='#ef4444', lw=1.5),
        arrowprops=dict(arrowstyle='->', color='#991b1b', lw=1.5),
    )

ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Rainfall (mm/day, spatial mean)', fontsize=11)
ax.set_title(
    'CHIRPS daily rainfall over Kenya — January 2021 to December 2022',
    fontsize=13, weight='bold',
)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 18)

plt.tight_layout()
out = FIG_DIR / 'fig_chirps_dec2021_gap.png'
plt.savefig(out, dpi=300, bbox_inches='tight', facecolor='white')
print(f'\nSaved: {out}')
