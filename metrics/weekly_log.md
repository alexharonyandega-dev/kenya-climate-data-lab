# Weekly Metrics Log

## Week 01 - 2026-09-21 to 2026-09-27

| Date | Activity | Category | Output | Metric | Link | Next |
|---|---|---|---|---|---|---|
| 2026-09-21 to 22 | Bootstrap repo + download data | Technical | Public repo + 8 raw datasets | 1 repo, 8 datasets, 21 commits | https://github.com/alexharonyandega-dev/kenya-climate-data-lab | Start Week 2: exploration |

## Week 02 - 2026-09-28 to 2026-10-04

| Date | Activity | Category | Output | Metric | Link | Next |
|---|---|---|---|---|---|---|
| 2026-09-28 to 10-04 | Data exploration notebook | Technical | 01_data_exploration.ipynb + 8 figures + Week 2 reflection | 9 datasets inspected, 8 missingness/analysis figures | https://github.com/alexharonyandega-dev/kenya-climate-data-lab/blob/main/notebooks/01_data_exploration.ipynb | Start Week 3: cleaning + CHIRPS county aggregation |

## Week 03 - 2026-09-21 to 2026-09-27

The week the project found its shape. Pivoted from yield prediction
to county-level drought monitoring after advisor feedback, then built
and validated the full pipeline in two days.

| Date | Activity | Category | Output | Metric | Link | Next |
|---|---|---|---|---|---|---|
| 2026-09-25 | GEE registration + pivoted scope | Technical | Google Earth Engine access (academic tier) | 47 counties, no billing | - | Build pipeline |
| 2026-09-26 | iSDAsoil raster extraction + FAOSTAT + ERA5 extension | Technical | isda_soil_raster_zonal.csv, FAOSTAT 1961-2024, ERA5 9 vars x 35 yrs | 20M pixels x 8 properties, 18 NetCDF files | - | CHIRPS extraction |
| 2026-09-27 | CHIRPS + NDVI + stress index + validation | Technical | 7 processed files, 4 figures, 8 scripts, 32-entry DECISIONS_LOG, architecture.md, data_dictionary.md (345 lines), Week 3 reflection (151 lines) | 5,479 days x 47 counties, 96 months x 47 counties, 2022 drought detected | [fig_stress_october_series.png](https://github.com/alexharonyandega-dev/kenya-climate-data-lab/blob/main/paper/figures/fig_stress_october_series.png) | Week 4: weekly resolution + crop calendar weighting |
| 2026-09-27 | Documentation alignment | Docs | README rewritten, DECISIONS_LOG (32 entries), data_dictionary, architecture | Repo reflects actual project state | - | Continue |

### Week 3 deliverables checklist

- [x] 02_data_cleaning.ipynb (audit, reruns clean)
- [x] DECISIONS_LOG.md with 32 numbered decisions
- [x] data_dictionary.md expanded to cover all 7 processed files
- [x] IQR outlier flags added to master stress table
- [x] Reproducibility audit passes (all 7 outputs byte-identical)
- [x] merged_dataset_v1.csv sidecar built (1,457 rows)
- [x] Week 3 reflection rewritten for the pivot
- [x] All committed and pushed

### Metrics

- **Total commits this week**: ~15
- **Datasets processed**: 12 (4 raw CSVs + 7 derived + 1 sidecar)
- **Validated finding**: 2022 Horn of Africa drought detected without calibration
- **Documentation coverage**: 100% of processed files
- **Reproducibility**: PASS

**Week 3 Substack post:** https://kenyaclimatelab.substack.com

### ERA5 county aggregation — COMPLETE
- 5,407,632 rows generated (47 counties x 9 vars x 12,784 days)
- Split into 9 per-variable CSVs (~23-24 MB each, 213 MB total)
- Combined file (218 MB) gitignored (>100 MB GitHub limit)
- Script: scripts/extract_era5_counties.py (committed 3fd7f04)
