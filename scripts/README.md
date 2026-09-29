# scripts/

Reproducible data pipelines and figure generators. Each script is
self-contained: run with the `kenya-climate` conda env activated.

## Pipeline scripts (run in this order)

| Script | Produces | Runtime |
|---|---|---|
| `extract_chirps_counties.py` | `data/processed/chirps_counties_daily_2010_2024.csv` | 3.1 min |
| `extract_era5_counties.py` | `data/processed/era5_counties/*.csv` (9 files) | ~30 min |
| `build_crop_calendar.py` | `data/metadata/kenya_crop_calendar.csv` | < 5 s |
| `build_weekly_rainfall.py` | `data/processed/county_weekly_rainfall_2017_2024.csv` | < 30 s |
| `build_county_monthly_panel.py` | `data/processed/county_monthly_panel_2017_2024.csv` | < 30 s |
| `compute_stress_index.py` | `data/processed/county_monthly_stress_2017_2024.csv` | < 10 s |
| `add_outlier_flags.py` | Adds IQR boolean columns | < 5 s |
| `build_merged_yield_sidecar.py` | `data/processed/merged_dataset_v1.csv` | < 10 s |
| `split_era5.py` | Splits combined ERA5 by variable (git-limit workaround) | < 1 min |
| `recompress_era5.py` | int16 recompression of ERA5 NetCDFs | < 5 min |

## Integration notebook

`notebooks/03_integration.ipynb` — Week 4's formal merge. Builds
`county_monthly_stress_v3.csv` and `county_weekly_stress_2017_2024.csv`.
Wraps every merge in `logged_join()`. Runs in < 3 min on a fresh kernel.

## Figure scripts

| Script | Produces |
|---|---|
| `fig_the_gap.py` | Existing tools vs county-level gap |
| `fig_rainfall_ndvi_divergence.py` | Rainfall vs NDVI time series |
| `fig_nakuru_story.py` | Single-county drought timeline |
| `fig_chirps_dec2021_gap.py` | CHIRPS December 2021 missing-file heatmap |
| `fig_stress_map_october_series.py` | 6-panel county stress map |
| `fig_county_venn.py` | County coverage overlap (KNBS vs Zenodo) |
| `fig_era5_ocean_nan.py` | ERA5 ocean-NaN diagnostic |
| `fig_status_dashboard.py` | Week status card |
| `fig_pivot_timeline.py` | Week 3 pivot timeline |
| `fig_pipeline_architecture.py` | Two-tier pipeline diagram |
| `fig_data_gaps.py` | CHIRPS + NDVI missing-data panels |
| `fig_decisions_log.py` | 33 decisions by category |
| `fig_data_lineage.py` | End-to-end lineage diagram |
| `fig_stress_timeseries.py` | National + 5-county stress, 2017-2024 |
| `fig_three_way_divergence.py` | Rainfall / NDVI / soil moisture, 2020-2024 |
| `fig_soil_moisture_lead.py` | Lead-lag curve (r=0.461 at lag +1) |

## Verification

| Script | Purpose |
|---|---|
| `verify_reproducibility.py` | Re-runs pipeline, confirms byte-identical outputs |

## GEE

`scripts/gee/ndvi_counties_monthly.js` — browser-based Sentinel-2
extraction. Run once per year range. ~20 min per export.

## Convention

- Every paper figure gets a matching `fig_*.py` script.
- Scripts are idempotent — running twice produces the same output.
- Pipeline outputs go to `data/processed/` and are committed if under
  100 MB per file (larger files are split by variable or gitignored).
