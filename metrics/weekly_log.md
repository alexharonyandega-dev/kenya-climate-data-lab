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

## Week 4 (2026-10-12 to 2026-10-18)

**Theme:** Formal merge - crop calendar, ERA5, weekly product, re-validation

**Deliverables:**
- notebooks/03_integration.ipynb (55 cells)
- county_monthly_stress_v3.csv (4,512 x 27)
- county_weekly_stress_2017_2024.csv (19,599 x 21)
- stress_join_audit.csv (3 joins, 0 dropped)
- SHA256SUMS.txt
- paper/data_notes.md
- 4 figures: stress timeseries, three-way divergence, soil lead, lineage
- D34-D37 in DECISIONS_LOG

**Findings:**
- Crop stage weighting: 31 -> 8 severe counties in 2022 drought
- Soil moisture leads NDVI by 1 month (r=0.461, p=2e-220)
- Two indices: stress_avg (drought severity) vs stress_weighted (crop damage)

**Commits:**
- 5af93e0 feat(week4): integration notebook + stress pipeline audit
- a6e4cd5 feat(week4): crop calendar integration (D34) + audit trail
- 8c24805 feat(week4): ERA5 integration + soil moisture lead-lag (D35)
- 90d81ea feat(week4): weekly stress product (D36) + NaN documentation
- 348f65c feat(week4): re-validation + three story figures (D37)
- 01ed19b docs(week4): data notes + data lineage diagram

**Next:** Week 5 - formal validation against KNBS county yield

## Week 5 (2026-09-28 to 2026-10-05)

**Theme:** Null result + first public outreach

**Deliverables:**
- docs/week05_null_result.md — null result on yield prediction
- docs/week05_reflection.md — Week 5 reflection
- docs/data_acquisition_plan.md — plan to close the data gap
- docs/outreach_notes.md — outreach barrier documented
- metrics/outreach_log.csv — 17 rows
- paper/one_pager/Kenya_Climate_Data_Lab_One_Pager.pdf

**Public artifacts:**
- Blog post: "I Tried to Validate My Tool. It Failed."
- Open letter: "An open letter to Kenya's county agriculture officers"
- Both cross-posted on X

**Findings:**
- Stress index does not predict county-level yield loss (n=5 to n=20)
- Kakamega outlier — fall armyworm compounded the 2022 drought
- 13/13 emails to .go.ke bounced (D41)

**Commits:**
- 5d07e96 docs(week5): commit all diagnostics + D40 + armyworm confirmation
- ee5517a docs(week5): reflection
- 0b448d9 docs(week5): data acquisition plan
- 237868f docs: update scripts/README
- 149128f feat: one-page outreach PDF generator
- ce11feb docs: D41 — outreach blocked by government spam filters
- 4667b5b docs: link Week 5 blog post from README
- 651c20d docs: log blog post and open letter

**Next:** Week 6 — draft preprint abstract and methods
