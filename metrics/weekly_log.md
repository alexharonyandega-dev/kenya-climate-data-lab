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

## Week 5 — Extended session (2026-10-03)

**Theme:** KCND report integration + independent validation

**Deliverables:**
- 8 County Climate Risk Profiles (Bomet, Busia, Homa Bay, Kericho, Kilifi, Laikipia, Nandi, Nyamira)
- KMD State of the Climate 2025
- 2 NDMA drought bulletins (June + October 2022)
- TAMSAT-ALERT validation paper (Boult et al. 2020)
- 4 new documentation files (CCRP_Summary, NDMA_2022_Labels, sources.md sections 11-14, cross-check in week05_null_result.md)

**Findings:**
- NDMA and monitor flagged zero overlapping counties in 2022. CHIRPS rainfall verified: monitor counties z = −1.14, NDMA counties z = −0.71. Both in drought.
- One drought event, two tracking systems. NDMA covers pastoral (ASAL). Monitor covers crop-region (47 counties).
- CCRP vulnerability indices: Bomet (0.473) > national (0.4311). Kericho (0.448) > ASAL (0.4381). Laikipia (0.3841) no baseline.
- TAMSAT-ALERT validates contemporaneous soil moisture ↔ VCI (r = 0.68 MAM). Our lead-lag (r = 0.461) extends this to finer resolution.

**Commits (this session):**
- e780f72 feat: add 8 CCRPs
- d120a79 feat: add KMD State of the Climate
- 490f824 feat: add NDMA bulletins
- d231042 fix: NDMA comparison interpretation
- 0d076dc feat: add TAMSAT-ALERT paper
- 261f2f6 docs: CCRP vulnerability indices
- dc3d0d5 docs: sources.md sections 11-14
- 89fcc20 docs: cross-check null result
- a3b32d0 fix: correct CCRP baselines (fabricated 0.431 removed)
- 736ee0d fix: correct "two droughts" framing (CHIRPS verified)
- 5dbb827 fix: correct TAMSAT comparison

**Reflection:** Three errors caught by verification scripts: a fabricated national average, an untested "two droughts" claim, and a misread of what TAMSAT tested. Every one was a claim that sounded right. The fix is in.

## Week 5 — LinkedIn setup session (2026-10-05)

**Theme:** Activate LinkedIn as the alternate outreach channel after email blocked (D41)

**Deliverables:**
- LinkedIn profile fully set up: headline, headshot, banner (31-vs-8 map), About section, Featured section (3 cards), custom URL, 10 skills
- Intro post published on the LinkedIn feed with the 31-vs-8 map attached
- 30 accounts followed (Kenyan research, government, climate-tech, researchers)
- 1 connection request sent (Dinah Makokha, Chief Officer Agriculture Bungoma)

**Outreach outcome:**
- 1 of 3 named officials found on LinkedIn (Dinah Makokha)
- 2 not on LinkedIn (Leonard Bor, Monicah Salano Fedha) — phone fallback remains

**Next:** Follow up with Dinah in 7 days. Phone calls for the other two officials.

## Week 6 (2026-10-05 to 2026-10-11)

**Theme:** Preprint draft — Abstract, Methods, Validation

**Deliverables:**
- paper/draft_v1.md — 2,431 words
  - Abstract (178 words, four findings compressed)
  - Title, author, contact, repository
  - Section 2: Data Sources (5 sources documented)
  - Section 3: Preprocessing (4 decisions)
  - Section 4: Stress Index (5 subsections)
  - Section 5: Validation (5 subsections)
  - Author contributions + data availability
- paper/figures/workflow.png (300 dpi, three-column layout)
- D43 added to DECISIONS_LOG (anomaly method)
- All decision references verified against DECISIONS_LOG
- NDMA cross-check reference corrected to labels file
- stress_mean → stress_avg consistency fix

**Findings:** The abstract compresses four findings (31-vs-8,
soil lead-lag, NDMA scope, null result) into 178 words. The methods
section documents every pipeline decision with a numbered reference.

**Commits:**
- f97ed7a paper: abstract v1
- a9d777c fix: sources.md — NDVI section
- ed3850f fix: reorder and renumber sources.md
- 29126f2 paper: data sources subsection
- 5bf0452 paper: preprocessing subsection
- 9b13fe7 fix: two decision references
- e694fe6 docs: D43 for anomaly method
- 5f6f260 paper: stress index + validation
- 3b4ebd2 fix: NDMA reference
- c5e4cec paper: workflow diagram
- b40d3b3 paper: title block + author info

**Next:** Week 7 — first deep external contact (KNBS + county officers).

## Week 6 — Extended (2026-10-05, Monday)

**Theme:** Preprint methods section published as a Substack milestone post

**Deliverables:**
- Substack post: "The methods section is done" (~1,200 words)
- LinkedIn post: short version of the same milestone
- Both cross-posted the day after ASM feature submission

**Context:** The methods section draft (3,018 words) was completed over the weekend. This post marks the milestone publicly, before Week 7's mentor outreach begins.

**Commits:** (this session)
- 42ade07 docs: log ASM feature post submission
- a62554a fix: dedupe ASM row in outreach log
