"""Generate a diagnostic map showing ERA5-Land NaN over the Indian Ocean.

The Kenya bounding box (lat -4.7 to 5.0, lon 33.9 to 41.9) includes
part of the Indian Ocean on the southeast edge. ERA5-Land only has
data over land, so those ocean pixels appear as NaN.

This figure shows the pattern clearly — the missing pixels form a
coastline-shaped mask, which is the tell that it's water, not a bug.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import xarray as xr
from pathlib import Path

# --- Paths ---
RAW = Path(__file__).resolve().parent.parent / 'data' / 'raw'
FIG_DIR = Path(__file__).resolve().parent.parent / 'paper' / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

# --- Load ERA5 ---
ds = xr.open_dataset(RAW / 'era5_temperature_2010_2024.nc')
t2m_c = ds['t2m'] - 273.15  # Kelvin -> Celsius

# --- Compute monthly mean for July 2024 ---
# July = cool season in Kenya; highlands clearly visible
monthly = t2m_c.sel(valid_time='2024-07').mean(dim='valid_time', skipna=True)

# --- Build figure ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Colormap: RdYlBu_r is diverging, good for temperature
cmap = plt.get_cmap('RdYlBu_r').copy()
cmap.set_bad(color='#1a1a1a')  # NaN = near-black, unmistakable

# --- Panel 1: NaN visible as black ---
ax = axes[0]
im1 = ax.imshow(
    monthly.values,
    cmap=cmap,
    vmin=10, vmax=35,
    extent=[
        float(monthly.longitude.min()),
        float(monthly.longitude.max()),
        float(monthly.latitude.min()),
        float(monthly.latitude.max()),
    ],
    origin='upper',
    aspect='auto',
)
ax.set_title('ERA5-Land July 2024 mean 2m temperature\nNaN shown as black',
             fontsize=12, weight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.colorbar(im1, ax=ax, label='Temperature (°C)', fraction=0.046, pad=0.04)

# --- Panel 2: Land-only mask (where data exists) ---
ax = axes[1]
mask = np.where(np.isnan(monthly.values), 0, 1)
ax.imshow(
    mask,
    cmap=mcolors.ListedColormap(['#1a1a1a', '#4ade80']),
    extent=[
        float(monthly.longitude.min()),
        float(monthly.longitude.max()),
        float(monthly.latitude.min()),
        float(monthly.latitude.max()),
    ],
    origin='upper',
    aspect='auto',
)
ax.set_title('ERA5-Land data mask\nGreen = data, Black = NaN (ocean)',
             fontsize=12, weight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# --- Annotate ocean region on panel 2 ---
ax.annotate(
    'Indian Ocean\n(no ERA5-Land data)',
    xy=(40.5, -3.0),
    xytext=(42.5, 1.0),
    fontsize=10,
    color='white',
    ha='center',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1a1a', edgecolor='white'),
    arrowprops=dict(arrowstyle='->', color='white', lw=1.5),
)

plt.tight_layout()
out = FIG_DIR / 'fig_era5_ocean_nan.png'
plt.savefig(out, dpi=300, bbox_inches='tight', facecolor='white')
print(f'Saved: {out}')

# --- Print summary numbers ---
total = monthly.size
nan_count = int(np.isnan(monthly.values).sum())
print(f'Total pixels: {total}')
print(f'NaN pixels:   {nan_count} ({100*nan_count/total:.2f}%)')
print(f'Land pixels:  {total - nan_count} ({100*(total-nan_count)/total:.2f}%)')
