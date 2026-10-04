# DECISIONS LOG

Every material decision made in this project, in order. Each entry has:
- **Number** (D01, D02, ...)
- **Decision** (what was decided)
- **Reason** (why)
- **Data affected** (which files or datasets)
- **Date** (when)

This log exists so that future-you (or an advisor, or a reviewer) can answer
"why did you do X?" without re-reading the entire commit history.

---

## Scope and direction

### D01 — Expanded scope from 5 counties to all 47
- **Reason:** An external advisor (Mark) pointed out that existing tools
  cover Kenya at sub-county or livelihood-zone granularity, not administrative
  county. Monitoring all 47 counties fills the actual operational gap.
- **Data affected:** All pipelines; CHIRPS extraction, NDVI extraction, stress
  index, crop calendar.
- **Date:** 2026-09-27

### D02 — Pivoted from annual yield prediction to monthly/weekly stress monitoring
- **Reason:** Existing tools (FAO ASI, FEWS NET, GEOGLAM) update frequently
  but not by county. The only county-level yield source (KNBS) is annual and
  post-harvest. A fast county-level stress monitor fills this gap.
- **Data affected:** Project narrative, README, all downstream analysis.
- **Date:** 2026-09-27

### D03 — Master table is `county_monthly_stress_2017_2024.csv`, not `merged_dataset_v1.csv`
- **Reason:** The plan's expected filename assumed a yield-prediction model.
  We pivoted to stress monitoring. The descriptive filename is more honest
  than the plan-compatible one.
- **Data affected:** `data/processed/county_monthly_stress_2017_2024.csv`
- **Date:** 2026-09-27

### D04 — Two-tier monitor design: weekly rainfall (fast) + monthly composite (rich)
- **Reason:** CHIRPS is daily; Sentinel-2 NDVI is monthly. A single-tier system
  would be limited by the slower signal. FEWS NET and FAO ASI use the same split.
- **Data affected:** `county_weekly_rainfall_2017_2024.csv` (Tier 1);
  `county_monthly_stress_2017_2024.csv` (Tier 2).
- **Date:** 2026-09-27

### D05 — Crop calendar assigns each county to one of 7 agro-ecological zones
- **Reason:** Kenya is not homogeneous. Western highlands are bimodal; Rift
  Valley is unimodal long-rains; northern ASAL is short-rains-only. A single
  "Kenya maize calendar" would misclassify half the country.
- **Data affected:** `data/metadata/kenya_crop_calendar.csv`
- **Date:** 2026-09-27

---

## Rainfall (CHIRPS)

### D06 — CHIRPS extraction used precomputed county pixel masks
- **Reason:** Reading each GeoTIFF and masking 47 polygons per file would
  require 47 × 5,479 = 257,513 polygon intersection operations. Precomputing
  pixel indices once reduces the per-file work to a single mean over cached
  coordinates.
- **Data affected:** `scripts/extract_chirps_counties.py`,
  `data/processed/chirps_counties_daily_2010_2024.csv`
- **Runtime:** 3.1 minutes (vs. an estimated 3+ hours for the naive approach).
- **Date:** 2026-09-27

### D07 — December 2021 CHIRPS gap left as NaN, not interpolated
- **Reason:** The CHIRPS 2.0 Africa daily archive is missing all 31 days of
  December 2021 (a known archive defect). The monthly aggregate exists but
  cannot be decomposed back into daily values. Interpolating across 31 days
  would fabricate data.
- **Data affected:** `chirps_counties_daily_2010_2024.csv` — 1,457 NaN rows
  (31 days × 47 counties).
- **Date:** 2026-09-27

### D08 — CHIRPS positive bias in arid regions documented, not corrected
- **Reason:** Independent comparison against published Kenya climatology showed
  CHIRPS overestimates rainfall by +10% (western highlands) to +85% (northern
  ASALs). This is a well-known property of the cold-cloud-duration satellite
  input. Corrections would introduce more uncertainty than the bias itself.
  Anomaly-based analysis (our stress index) cancels out uniform bias.
- **Data affected:** All CHIRPS-derived files.
- **Date:** 2026-09-27

### D09 — CHIRPS extension to 1990 was attempted and deferred
- **Reason:** UCSB server rate on 2026-09-27 was 0.1–0.2 files/s, giving an
  estimated 12+ hours for the 7,305 files needed. Combined with lower
  pre-2000 data quality (fewer contributing satellites), the extension was
  deferred. Script preserved as `fetch_chirps_1990_2009_DEFERRED.py`.
- **Data affected:** N/A — no data was added.
- **Date:** 2026-09-27

### D10 — ISO-year edge rows filtered from weekly rainfall
- **Reason:** Jan 1–3, 2017 belong to ISO year 2016; Dec 30–31, 2024 belong
  to ISO year 2025. These boundary weeks would create spurious partial-year
  entries. Filtered to ISO years 2017–2024 inclusive.
- **Data affected:** `county_weekly_rainfall_2017_2024.csv` (19,693 → 19,599 rows)
- **Date:** 2026-09-27

---

## Vegetation (NDVI)

### D11 — NDVI extraction at 1000m scale, not 500m
- **Reason:** At 500m scale, computing monthly NDVI means across 47 county
  polygons for all 12 months hit Google Earth Engine's user memory limit.
  Doubling the scale halves the per-polygon pixel count.
- **Data affected:** `scripts/gee/ndvi_counties_monthly.js`,
  `data/processed/ndvi_counties_monthly_2017_2024.csv`
- **Date:** 2026-09-27

### D12 — NDVI values outside [0, 1] clipped to NaN
- **Reason:** Sentinel-2 NDVI theoretically ranges −1 to +1. Negative values
  arise from water pixels (Lake Victoria in Kisumu/Siaya/Homa Bay) and
  residual cloud edges that survived the 40% cloud mask. These are not
  vegetation, so they're set to NaN.
- **Data affected:** `ndvi_counties_monthly_2017_2024.csv`
- **Date:** 2026-09-27

### D13 — NDVI missing county-months left as NaN, not interpolated
- **Reason:** 252 county-months (5.6% of the dataset) had no clear-sky
  Sentinel-2 observations. Interpolating would fabricate vegetation signals
  in months where the satellite saw only clouds. Downstream analysis can
  flag missing values; the raw data should not.
- **Data affected:** `ndvi_counties_monthly_2017_2024.csv`
- **Date:** 2026-09-27

### D14 — Google Earth Engine asset uploaded from shapefile, not GeoJSON
- **Reason:** GEE's shapefile uploader rejected the GeoJSON format. A zip of
  shapefile components (.shp/.shx/.dbf/.prj) was accepted. Asset saved as
  `projects/kenya-maize-monitor/assets/kenya_counties_shp`.
- **Data affected:** `data/external/kenya_counties_shp.zip`
- **Date:** 2026-09-27

---

## Soil (iSDAsoil)

### D15 — iSDAsoil centroid sampling superseded by 15-point sampling
- **Reason:** County centroids frequently sit on urban land with compacted,
  disturbed soils. Sample of one county showed organic carbon differed by
  +93% between centroid and 15-point average. Point sampling is more
  representative.
- **Data affected:** `isda_soil_properties_by_county.csv` (centroid),
  `isda_soil_properties_by_county_sampled.csv` (15-point)
- **Date:** 2026-09-26

### D16 — 15-point sampling superseded by raster zonal statistics
- **Reason:** The 15-point sample was itself superseded by direct extraction
  from iSDAsoil's cloud-optimized GeoTIFFs on AWS S3. Zonal statistics over
  the full county polygon (~20 million pixels/county) is the definitive method.
- **Data affected:** `isda_soil_raster_zonal.csv`
- **Date:** 2026-09-26

### D17 — iSDAsoil back-transformations verified empirically
- **Reason:** iSDAsoil stores properties with property-specific transforms
  that aren't documented in the COG metadata. Back-transforms were reverse-
  engineered by comparing raster values against the API's point values.
  pH ÷ 10, nitrogen exp(x/100)−1, most others exp(x/10)−1.
- **Data affected:** `isda_soil_raster_zonal.csv`
- **Date:** 2026-09-26

---

## Climate (ERA5-Land)

### D18 — ERA5-Land extended from 1 variable to 9 variables
- **Reason:** `t2m` alone cannot compute GDD (needs `ssrd`), VPD (needs `d2m`),
  or drought stress (needs `swvl1` + `swvl2`). Extended to include all
  variables needed for agronomic feature engineering.
- **Variables added:** d2m, ssrd, swvl1, swvl2, tp, u10, v10, pev
- **Data affected:** `data/raw/era5_variables/*.nc`
- **Date:** 2026-09-26

### D19 — ERA5-Land extended from 2010–2024 to 1990–2024
- **Reason:** Kaggle maize dataset starts at 1990. Extending ERA5 back to
  match increases overlapping training years from 4 to 24.
- **Data affected:** All `era5_*_1990_2024.nc` files
- **Date:** 2026-09-26

### D20 — ERA5-Land split into two periods per variable (1990–2007, 2008–2024)
- **Reason:** Single 1990–2024 files exceeded GitHub's 100 MB per-file hard
  limit for 6 of 9 variables. Splitting keeps every file under the limit
  while preserving full temporal coverage.
- **Data affected:** `data/raw/era5_variables/*_1990_2007.nc` and `*_2008_2024.nc`
- **Date:** 2026-09-26

### D21 — ERA5-Land recompressed as int16 with scale_factor metadata
- **Reason:** Float32 storage was 40% larger than necessary. Int16 quantization
  with explicit scale/offset preserves values within instrument accuracy
  (ERA5-Land native precision is ~0.01 K anyway).
- **Data affected:** All ERA5 NetCDF files (after split).
- **Date:** 2026-09-26

---

## Yield (FAOSTAT, Kaggle, KNBS)

### D22 — FAOSTAT yield extended from 2010–2024 to 1961–2024
- **Reason:** Original download arbitrarily selected the last 15 years.
  Full series (64 rows) provides the complete national yield history for
  cross-validation and long-term trend analysis.
- **Data affected:** `data/raw/faostat_maize_yield_kenya.csv` (15 → 64 rows)
- **Date:** 2026-09-26

### D23 — FAOSTAT units are kg/ha (not hg/ha)
- **Reason:** The original project plan described FAOSTAT yield as "hg/ha".
  Actual file header shows "kg/ha". Conversion for t/ha is therefore ÷1,000,
  not ÷10,000.
- **Data affected:** All downstream uses of FAOSTAT yield.
- **Date:** 2026-09-21

---

## Stress index

### D24 — Composite stress weights: 0.65 × NDVI + 0.35 × rainfall
- **Reason:** The 2021–2022 drought showed rainfall anomaly was lowest in 2021
  (−0.193), but vegetation collapse peaked in 2022 (NDVI −1.35). Drought is
  cumulative — five failed seasons drained soil moisture reserves. NDVI
  captures the accumulated damage, so it carries more weight in the composite.
- **Data affected:** `county_monthly_stress_2017_2024.csv` — `stress_avg` column
- **Date:** 2026-09-27

### D25 — Stress category thresholds at ±0.50 and ±1.25 standard deviations
- **Reason:** Observed distribution on 2017–2024 data is roughly bell-shaped
  (3.1% severe, 24.5% moderate, 41.3% normal, 20.2% good, 5.2% very good).
  Tighter thresholds would over-flag; looser thresholds would under-flag.
- **Data affected:** `county_monthly_stress_2017_2024.csv` — `stress_category` column
- **Date:** 2026-09-27

### D26 — `stress_min` (minimum of the two anomalies) retained alongside `stress_avg`
- **Reason:** Operational early-warning systems (FEWS NET, FAO ASI) use a
  conservative "worst-signal" convention. `stress_min` flags when either
  rainfall OR vegetation is severely stressed. `stress_avg` is for ranking
  and visualization; `stress_min` is for alerting.
- **Data affected:** `county_monthly_stress_2017_2024.csv` — `stress_min` column
- **Date:** 2026-09-27

---

## Missing-value policy

### D27 — Missing-value policy per dataset
- **CHIRPS (December 2021):** Left as NaN. No interpolation. Reason: archive
  gap cannot be reconstructed.
- **NDVI (5.6% county-months):** Left as NaN at raw level. Downstream may
  interpolate but must flag.
- **iSDAsoil (raster):** No missing values after zonal aggregation; ocean
  pixels were masked before averaging.
- **FAOSTAT (pre-2010 rows):** Flagged as "Estimated value" in the Flag column.
  Used as-is; the flag is preserved for downstream filtering.
- **Data affected:** All processed files.
- **Date:** 2026-09-27

---

## Infrastructure

### D28 — KMD rainfall documented as inaccessible; CHIRPS substituted
- **Reason:** KMD's IRI Data Library server (kmddl.meteo.go.ke) returned 404
  on every programmatic endpoint tested (data.nc, DODS, Data Selection tab,
  Data Files tab). Server runs an old, partially broken Ingrid build. CHIRPS
  is the standard substitute in published Kenyan maize-climate research.
- **Data affected:** `data/metadata/sources.md` (documented);
  no KMD files exist in the project.
- **Date:** 2026-09-22

### D29 — Repo organized with `scripts/` and `notebooks/` for pipeline + audit
- **Reason:** Separate reproducible pipeline scripts (`scripts/`) from
  exploratory and audit notebooks (`notebooks/`). Keeps the audit trail
  distinct from the production code.
- **Data affected:** Repository structure.
- **Date:** 2026-09-25

### D30 — Google Earth Engine registered as non-commercial academic
- **Reason:** Needed for Sentinel-2 NDVI access. Registered as "Academic
  institution" → "Community" tier to avoid any billing setup.
- **Data affected:** All NDVI extractions.
- **Date:** 2026-09-27

---



### D31 — IQR outlier flags added to master stress table
- **Reason:** Extreme rainfall and vegetation values are often real events
  (droughts, floods) that the model must learn from. Deleting them would
  lose signal. Flagging preserves the data while allowing downstream
  filtering. Follows the plan's D05 convention.
- **Method:** 1.5 x IQR rule applied to `rainfall_mm`, `ndvi`, `stress_avg`,
  and `stress_min`. Four boolean columns added:
  `{col}_is_outlier`.
- **Data affected:** `county_monthly_stress_2017_2024.csv` — 4 new columns
  (12 -> 16 total).
- **Date:** 2026-09-27

---



### D32 — `merged_dataset_v1.csv` produced as optional yield-model sidecar
- **Reason:** The plan expected a merged CSV in yield-prediction format.
  Our pivot to stress monitoring changed the master table, but keeping a
  sidecar preserves plan compatibility for anyone wanting to try yield
  prediction later. It is NOT the master table.
- **Grain:** one row per (county, year, season)
- **Columns:** county, year, season, rainfall_mm, rainfall_anomaly,
  mean_temp_c, ndvi_mean, ndvi_anomaly, yield_t_ha
- **Data affected:** new file `data/processed/merged_dataset_v1.csv`
- **Note:** The `yield_t_ha` column is Kaggle national-scale yield (same
  value for all counties in a year), not a per-county yield.
- **Date:** 2026-09-27

---

## Summary by category

| Category | Decisions |
|---|---|
| Scope and direction | D01–D05 |
| Rainfall (CHIRPS) | D06–D10 |
| Vegetation (NDVI) | D11–D14 |
| Soil (iSDAsoil) | D15–D17 |
| Climate (ERA5-Land) | D18–D21 |
| Yield | D22–D23 |
| Stress index | D24–D26 |
| Missing-value policy | D27 |
| Infrastructure | D28–D30 |

**Total: 32 numbered decisions.**

### D33 - ERA5 county aggregation split by variable

**Decision:** Commit ERA5 county daily data as 9 per-variable CSVs under `data/processed/era5_counties/`, gitignore the combined long-format file.

**Reason:** Combined file (`era5_counties_daily.csv`) is 218 MB, exceeding GitHub's 100 MB per-file hard limit. Split yields 9 files of ~23-24 MB each, safely under the limit. Combined file remains on disk and is regenerable in ~30 min via `scripts/extract_era5_counties.py`.

**Data affected:** `data/processed/era5_counties/*.csv` (committed), `data/processed/era5_counties_daily.csv` (gitignored).

**Trade-off:** Downstream code reads 9 files instead of 1. Mitigation: a loader helper can concatenate on demand.

**Date:** 2025-09-27

### D34 - Crop stage weighting

**Decision:** Every stress observation is weighted by crop stage, per county-month, using `data/metadata/kenya_crop_calendar.csv`.

**Weights:** planting/vegetative 1.0, grain_fill 0.7, harvest 0.3, fallow 0.0, Nairobi NaN.

**Reason:** A dry October means planting failure in Kakamega (bimodal, short-rains) and harvest benefit in Trans Nzoia (unimodal, Sept harvest). Unweighted stress treats them identically. Wrong.

**Data affected:** `county_monthly_stress_v2.csv`, `county_monthly_stress_v3.csv`. New columns `crop_stage`, `crop_stage_weight`, `stress_weighted`.

**Trade-off:** Two indices now exist. `stress_avg` measures drought; `stress_weighted` measures crop damage. Both are reported.

---

### D35 - ERA5 anomalies as diagnostic columns, not composite inputs

**Decision:** Add `swvl1_mean_anomaly`, `swvl2_mean_anomaly`, `t2m_mean_anomaly`, `pev_mean_anomaly` as separate columns. Do NOT recompute `stress_avg`.

**Reason:** The 65/35 composite already validated against the 2022 drought without calibration. Recomputing it would break that validation. The new signals sit alongside.

**Data affected:** `county_monthly_stress_v3.csv`. Four new anomaly columns.

**Result - the lead-lag finding:** Soil moisture anomaly (0-7cm) leads NDVI anomaly by **one month**: r = 0.461, p = 2e-220, n = 4,205. Contemporaneous correlation is r = 0.364. `swvl1_mean_anomaly` becomes the earliest signal in the weekly product.

---

### D36 - Weekly stress product is rainfall-led, monthly companions carried forward

**Decision:** `county_weekly_stress_2017_2024.csv` updates on weekly rainfall. Every monthly signal from `stress_v3` is prefixed `latest_monthly_` and carried forward.

**Reason:** NDVI is monthly. Faking weekly NDVI would fabricate satellite observations that don't exist. The prefix tells the reader exactly which numbers are fresh (weekly rainfall) and which are last-confirmed (monthly stress, NDVI, soil moisture).

**Data affected:** `county_weekly_stress_2017_2024.csv` (19,599 rows, 21 columns).

**Trade-off:** The product is honest about its own latency. A weekly reader sees rainfall this week, plus the most recent confirmed monthly reading.

---

### D37 - Two indices, two questions

**Decision:** The tool reports BOTH `stress_avg` (drought severity) and `stress_weighted` (maize-crop damage).

**Reason - the 2022 re-validation finding:** The 2022 drought re-validation showed:
- Unweighted severe flags: **31 counties**
- Weighted severe flags: **8 counties**

The drop is because most Kenyan counties were in harvest or fallow at peak 2022 stress. Only 8 had maize in the ground. Weighting never creates new severe flags — no county triggered earlier under weighted than unweighted.

**Data affected:** Reporting logic, blog, dashboard (future).

**Trade-off:** A reader must know which index answers their question. A county agriculture officer reads `stress_weighted`. A drought response coordinator reads `stress_avg`. Both are correct.

---

### SHA-256 checksums (Week 4)

- `county_monthly_stress_v3.csv` — see `data/processed/SHA256SUMS.txt`
- `county_weekly_stress_2017_2024.csv` — see `data/processed/SHA256SUMS.txt`
- `stress_join_audit.csv` — see `data/processed/SHA256SUMS.txt`

### D38 - Week 4 hardening pass

**Decision:** After the main Week 4 deliverables were committed, run four
sensitivity tests on the two headline findings before closing the week.

**Tests run:**
1. Crop weight sensitivity (28 combinations)
2. Within-county vs pooled lead-lag correlation
3. Bootstrap CI on lead-lag (n=1,000)
4. Severity table (which 8 counties)

**Result:** Both findings survive all four tests. The 2022 severe-count
is 8 across every plausible weight combination. The lead-lag correlation
is 0.463 within-county, essentially identical to the pooled 0.461. The
95% CI on the lead-lag is [0.436, 0.485].

**Reframing adopted:** The "31 → 8" finding is a sharper claim than
originally stated: 31 counties had severe drought; only 8 had severe
drought while maize was actively growing. These 8 are the counties
where the 2022 drought actually damaged maize yield.

**Data affected:** Four new CSVs in data/processed/. Notebook markdown
updated for clarity. No changes to the master data.

**See:** `docs/week04_hardening.md` for full method and results.

**Date:** 2026-10-18

### D39 — Quarantine v1 sidecar, rebuild with KNBS

**Discovery (2026-09-30):** `merged_dataset_v1.csv` was built by
`build_merged_yield_sidecar.py`, which used the **Kaggle national-level**
maize dataset as its yield source. Kaggle has one national value per
year. Merging that to a 47-county × 9-season climate table on `year`
alone broadcast the national mean (4.58 t/ha) across every county.

**Symptom:** identical yield_t_ha for all 47 counties, same years
(2009-2013) — the Cartesian join signature.

**Fix:**
- v1 file renamed to `merged_dataset_v1_BROKEN.csv` and documented as
  unusable in `data/processed/README_BROKEN.md`.
- New `scripts/build_merged_yield_sidecar_v2.py` uses KNBS county-level
  production + area (5 counties × 5 years, 2020-2024). Yield is computed
  from `Production_Tons / Area_Ha`.
- For the 42 counties without KNBS coverage, `yield_t_ha` is left as NaN.

**Impact on published findings:** none. The sidecar was never used in
the stress pipeline. The Week 4 findings (31→8, soil-moisture lead-lag)
do not depend on this file.

**Impact on Week 5 plan:** the validation set is 5 counties, not 47.
The 8 crop-severe counties identified in Week 4 are not in the KNBS
coverage. Week 5 validates on the 5 we have; the other 42 remain a
data-acquisition problem.

**Date:** 2026-09-30

### D40 - Null result: stress index does not predict yield

**Test:** Correlation between `stress_weighted` and maize yield /
production change, at multiple aggregations.

**Data:** KNBS county-level production and area (5 counties, 2020-2024),
verified against the National Agriculture Production Report 2025,
Annex 1 (page 162).

**Results:**

| Test | n | r | p | Verdict |
|---|---|---|---|---|
| County stress vs yield YoY | 20 | -0.085 | 0.723 | Null |
| County stress vs production YoY | 20 | +0.058 | 0.807 | Null |
| Growing-season stress vs yield | 20 | -0.066 | 0.782 | Null |
| Growing-season stress vs production | 20 | +0.065 | 0.785 | Null |
| 2022-only (yield) | 5 | -0.832 | 0.080 | Wrong sign |
| 2022-only growing season | 5 | -0.758 | 0.137 | Wrong sign |
| Lagged (t-1 stress vs t production) | 15 | +0.267 | 0.337 | Null |
| National stress vs yield | 4 | +0.162 | 0.838 | Untestable |
| National lagged | 4 | -0.985 | 0.015 | n=4 artifact |

**Every test is null, wrong-signed, or untestable.**

**Diagnosis - the Kakamega outlier:**
Kakamega 2022: area **up 2%**, production **down 41%**, stress mildest
of the 5 counties (-0.182).

Drought reduces both area planted *and* yield. Kakamega's signature —
area stable, yield collapse — is not a drought pattern. It is a
disease or pest pattern.

**Confirmed against NAPR 2025 page 31:** the 2022 rainy season was
compounded by *"localized outbreaks of fall armyworm"* and short-rains
counties had below-average precipitation. Kakamega was hit by both.

**Scope reframe:**
The tool detects drought. It does not predict yield. Those are
different problems. Only the first one is currently solved.

**What this does NOT mean:**
The 8-county Week 4 finding stands. The lead-lag r=0.461 stands. The
composite index is still a valid drought monitor. This null result
only falsifies the *yield prediction* aspiration.

**Date:** 2026-09-30

### D41 - Email outreach blocked by government spam filters

**Discovery (2026-10-02):** All 13 emails sent to KNBS, Nakuru,
Kakamega, and Bungoma county governments bounced. Zero delivered.

**Cause:** Kenyan government .go.ke mail servers reject email from
free providers (@gmail.com). The rejection returns "Address not
found" — a misleading error that suggests the address is wrong when
actually the sender is filtered.

**Impact:** Cannot reach county agriculture officers or KNBS via
cold email from a Gmail account.

**Response:**
1. Register a custom domain (alexharonyandegа.org or
   kenyaclimatelab.org) with Zoho Mail — 30-min setup, ~$10/year.
2. Reach the named officials via LinkedIn DM.
3. Publish an open letter to county agriculture officers on
   Substack — public, indexed, cannot bounce.
4. Call the county phone numbers for working email addresses.

**Data affected:** None. This is an outreach infrastructure decision,
not a data or pipeline decision.

**Documented in:** `docs/outreach_notes.md` (full writeup with all
13 attempts, lessons for other student researchers, and phone
numbers).

**Date:** 2026-10-02

### D42 - LinkedIn as the alternate outreach channel after D41

**Context:** D41 documented that Kenyan government .go.ke email
servers reject Gmail. All 13 outbound emails bounced. Outreach was
blocked.

**Decision:** Activate LinkedIn as the primary outreach channel for
county officials.

**Reason:** LinkedIn DMs are read by most Kenyan public servants. The
platform does not have the same spam-filtering problem as .go.ke
servers. It also allows public profile visibility — a county officer
can see who I am before deciding whether to reply.

**Data affected:** None. This is an outreach infrastructure decision.

**Outreach attempts:**
- 1 LinkedIn connection request sent (Dinah Makokha)
- 2 officials not on LinkedIn (Leonard Bor, Monicah Salano Fedha)
- Phone call fallback remains for the 2 not on LinkedIn

**Documented in:** `docs/outreach_notes.md`

**Date:** 2026-10-05

### D43 - Anomaly definition and reference period

**Decision:** For each county-month, the anomaly is the standardized
deviation of the observed value from that county's own climatological
mean and standard deviation for the same calendar month.

    anomaly(county, month) = (observed - climatology_mean) / climatology_std

**Reason:** Each Kenyan county has a different baseline. Comparing
Turkana's rainfall to Kakamega's rainfall produces meaningless
numbers. Comparing Turkana's rainfall this October to Turkana's own
historical October rainfall produces something a county officer can
act on.

**Reference period:** Full available record per source. CHIRPS
2010–2024 (15 years), Sentinel-2 NDVI 2017–2024 (8 years), ERA5-Land
1990–2024 (35 years). The reference period is not fixed across
sources because each source has a different native coverage.

**Consequence:** The anomaly is a z-score. Positive = wetter /
greener / wetter soil than normal. Negative = drier / browner /
drier soil than normal. Magnitudes are comparable within a source
but not across sources with different reference periods.

**Data affected:** `county_monthly_stress_2017_2024.csv`,
`county_monthly_stress_v3.csv`, `county_weekly_rainfall_2017_2024.csv`.

**Date:** 2026-10-04
