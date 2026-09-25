# scripts/

Standalone, reproducible generators for the figures in `paper/figures/`.
Each script is self-contained: run it with the `kenya-climate` conda env
activated and it writes its output PNG (and any cache CSV) to disk.

## Scripts

| Script | Produces | Runtime | Notes |
|---|---|---|---|
| `fig_era5_ocean_nan.py` | `paper/figures/fig_era5_ocean_nan.png` | < 5 s | Shows 6.6% NaN pixels in ERA5 Kenya bbox = Indian Ocean |
| `fig_chirps_dec2021_gap.py` | `paper/figures/fig_chirps_dec2021_gap.png`<br>`data/processed/chirps_kenya_daily_2021_2022.csv` | 5–15 min first run<br>< 5 s cached | Caches the Kenya daily rainfall time series to CSV |
| `fig_county_venn.py` | `paper/figures/fig_county_venn.png` | < 5 s | KNBS vs Zenodo county coverage; only Kakamega overlaps |
| `fig_status_dashboard.py` | `paper/figures/fig_status_week02.png` | < 5 s | Week 02 status card (0 cleaned tables, 5,449 raw files, 0 model code) |

## How to regenerate everything

    conda activate kenya-climate
    for script in scripts/fig_*.py; do
        echo "Running $script"
        python "$script"
    done

Total runtime: ~15 minutes on first run (CHIRPS time series), ~20 seconds thereafter.

## Convention

- Every paper figure gets a matching `fig_*.py` script here.
- Scripts are idempotent — running twice produces the same output.
- Caches go in `data/processed/` and are committed if small.
