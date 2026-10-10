# data/processed — Canonical Files

**Canonical master:** `county_monthly_stress_v3.csv`
**Shape:** 4,512 rows × 24 columns (47 counties × 96 months, 2017-01 → 2024-12)
**Reference:** `data/metadata/data_dictionary.md` — every column documented.

## What lives here

Everything in this folder is either the canonical master, a source
layer that feeds it, or a support file that documents it.

| File | Role |
|---|---|
| `county_monthly_stress_v3.csv` | **Master.** County-month stress index. Use this one. |
| `county_monthly_panel_2017_2024.csv` | Pre-composite panel, keeps raw rainfall + NDVI columns |
| `county_weekly_rainfall_2017_2024.csv` | Weekly rainfall tier (D04) |
| `county_weekly_stress_2017_2024.csv` | Weekly stress, derived from weekly rainfall |
| `chirps_counties_daily_2010_2024.csv` | Daily CHIRPS rainfall, 47 county columns |
| `ndvi_counties_monthly_2017_2024.csv` | Monthly NDVI from Sentinel-2 via GEE |
| `era5_counties_daily.csv` | Daily ERA5-Land variables (gitignored, 228 MB) |
| `era5_counties/` | Per-county ERA5 extracts |
| `isda_soil_raster_zonal.csv` | Soil properties per county |
| `leadlag_bootstrap_ci.csv` | Bootstrap CI for the soil→NDVI lead-lag |
| `leadlag_pooled_vs_within.csv` | Pooled vs within-county lead-lag comparison |
| `merged_dataset_v1.csv` | Yield-model sidecar (kept for plan compatibility; not used in the monitor) |
| `sensitivity_crop_weights_2022.csv` | 28-combination crop-weight sensitivity test |
| `severe_2022_by_county.csv` | Counties flagged severe in the 2022 drought |
| `SHA256SUMS.txt` | Checksums for pipeline outputs |
| `stress_join_audit.csv` | Row-count audit after joins |

## What is NOT here

Superseded versions and explicit broken artifacts live in
`data/_archive/`. If a file you remember from earlier weeks is
missing, check there before assuming it was deleted.

Archived:
- `merged_dataset_v1_BROKEN.csv`
- `README_BROKEN.md`
- `chirps_kenya_daily_2021_2022.csv` (scratch extraction)
- `ndvi_counties_monthly_2024_test.csv` (test extraction)
- `county_monthly_stress_2017_2024.csv` (superseded by v3)
- `county_monthly_stress_v2.csv` (superseded by v3)

## Do not

- Do not rename `county_monthly_stress_v3.csv`.
- Do not edit any `*_v3_cleaned` file in place.
- Do not commit the 228 MB ERA5 daily file — it is gitignored.
