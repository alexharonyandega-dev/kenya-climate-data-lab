# Architecture

End-to-end documentation of the Kenya Climate Data Lab stress monitor pipeline.

## Overview

The tool produces a monthly composite stress index for each of Kenya's 47
counties. The index compares current conditions to the historical average for
the same calendar month, county by county.

Two independent signals feed the composite:

1. Rainfall - CHIRPS 2.0 daily precipitation, aggregated to monthly totals
2. Vegetation - Sentinel-2 NDVI, monthly means per county

These are joined on (county, year, month) and standardized as z-scores against
each county's own 2017-2024 climatology for that calendar month.

## Pipeline

    CHIRPS daily (5,479 files)          Sentinel-2 monthly (GEE)
            |                                    |
            v                                    v
    extract_chirps_counties.py        ndvi_counties_monthly.js
            |                                    |
            v                                    v
    chirps_counties_daily_            ndvi_counties_monthly_
    2010_2024.csv                     2017_2024.csv
    5,479 days x 47 counties          96 months x 47 counties
            |                                    |
            v                                    |
    build_weekly_rainfall.py                     |
            |                                    |
            v                                    |
    county_weekly_rainfall_                      |
    2017_2024.csv                                |
            |                                    |
            +------------------+-----------------+
                               v
                  build_county_monthly_panel.py
                  (aggregate rainfall to monthly,
                   join with NDVI, compute anomalies)
                               |
                               v
                  county_monthly_panel_2017_2024.csv
                  4,512 rows
                               |
                               v
                  compute_stress_index.py
                  (0.35*rain + 0.65*ndvi, minimum, category)
                               |
                               v
                  county_monthly_stress_2017_2024.csv

### Canonical output file

The pipeline diagram above shows the intermediate output of
`compute_stress_index.py` as `county_monthly_stress_2017_2024.csv`.
The canonical working table is **`county_monthly_stress_v3.csv`**
(4,512 rows x 27 cols), which adds:

- Crop-stage weighting (D34) — `crop_stage`, `crop_stage_weight`,
  `stress_weighted`
- ERA5 diagnostic columns (D35) — `swvl1_mean_anomaly`,
  `swvl2_mean_anomaly`, `t2m_mean_anomaly`, `pev_mean_anomaly`
- Outlier flags (D31) — four boolean columns

`county_monthly_stress_2017_2024.csv` and `county_monthly_stress_v2.csv`
are pre-v3 versions, archived in `data/_archive/`. The v3 file is the
one referenced in the README, the paper, and the data dictionary.

## Two-tier design

CHIRPS is daily. Sentinel-2 is monthly. So the monitor runs in two tiers:

Tier 1 - Weekly rainfall (fast update)
- Source: CHIRPS daily files
- Output: county_weekly_rainfall_2017_2024.csv
- Cadence: refreshable weekly

Tier 2 - Monthly composite (richer signal)
- Source: monthly rainfall + monthly NDVI
- Output: county_monthly_stress_2017_2024.csv
- Cadence: monthly

FEWS NET and FAO ASI use the same split.

## Composite stress index

    stress_avg = 0.35 * rainfall_anomaly + 0.65 * ndvi_anomaly
    stress_min = min(rainfall_anomaly, ndvi_anomaly)

Why NDVI is weighted higher:

The 2021-2022 drought produced an important finding. Rainfall anomaly was
lowest in 2021 (-0.193 yearly mean), but vegetation collapsed in 2022
(NDVI -1.35 in December). Drought is cumulative - five failed rainy seasons
drained soil moisture reserves, so even partial rain couldn't revive the crops.

Rainfall captures what fell this month. NDVI captures what the crop actually
experienced, including the cumulative effect of prior months.

stress_min follows operational early-warning conventions: a location is only
as healthy as its worst signal.

## Stress categories

| Category | Threshold (stress_avg) |
|---|---|
| Severe stress | < -1.25 |
| Moderate stress | -1.25 to -0.50 |
| Normal | -0.50 to +0.50 |
| Good | +0.50 to +1.25 |
| Very good | > +1.25 |

Observed distribution (2017-2024): 3.1% severe, 24.5% moderate, 41.3% normal,
20.2% good, 5.2% very good.

## Crop calendar

Each county is assigned to one of seven agro-ecological zones based on FAO
GIEWS, KALRO, and FEWS NET livelihood-zone descriptions:

| Zone | Seasons | Counties |
|---|---|---|
| highland_west | Long + short rains | 14 |
| central_highlands | Long + short rains | 8 |
| rift_valley | Long rains only | 7 |
| asal_north | Short rains only | 7 |
| coastal | Long + short rains | 6 |
| eastern | Short rains dominant | 4 |
| urban | None | 1 |

Used to weight the stress index by in-season months.

## Scripts reference

| Script | Input | Output | Runtime |
|---|---|---|---|
| extract_chirps_counties.py | CHIRPS daily GeoTIFFs | daily rainfall CSV | 3.1 min |
| build_weekly_rainfall.py | daily rainfall CSV | weekly anomalies CSV | under 30 s |
| build_crop_calendar.py | static definitions | county-zone mapping | under 5 s |
| build_county_monthly_panel.py | daily rainfall + NDVI | monthly panel CSV | under 30 s |
| compute_stress_index.py | monthly panel | stress CSV | under 10 s |
| fig_stress_map_october_series.py | stress CSV | 6-panel map PNG | about 30 s |
| fig_the_gap.py | static definitions | gap diagram PNG | under 5 s |
| fig_rainfall_ndvi_divergence.py | monthly panel | divergence chart PNG | under 10 s |
| fig_nakuru_story.py | monthly panel | single-county chart PNG | under 10 s |
| gee/ndvi_counties_monthly.js | GEE asset | NDVI CSV (Google Drive) | about 20 min |

## Reproducing the pipeline

    conda create -n kenya-climate python=3.11 -y
    conda activate kenya-climate
    pip install -r requirements.txt

    python scripts/extract_chirps_counties.py
    python scripts/build_weekly_rainfall.py
    python scripts/build_crop_calendar.py
    python scripts/build_county_monthly_panel.py
    python scripts/compute_stress_index.py
    python scripts/fig_stress_map_october_series.py

The GEE NDVI step is browser-based - paste scripts/gee/ndvi_counties_monthly.js
into code.earthengine.google.com, download the resulting CSV from Drive.

## Known limitations

1. Monthly NDVI, not weekly. Weekly NDVI would need 384 GEE exports.
2. CHIRPS positive bias in arid regions (+20% to +85% in northern ASALs).
   Does not affect anomalies since those are relative.
3. County averages hide sub-county variation (Meru, Bungoma, Narok).
4. Validation is qualitative. Formal validation against KNBS yield data is
   scheduled for a later phase.

## References

- CHIRPS 2.0 - Funk et al. 2015, UCSB Climate Hazards Center
- Sentinel-2 SR - Copernicus programme, ESA
- ERA5-Land - Hersbach et al. 2020, ECMWF
- iSDAsoil - Hengl et al. 2021, iSDA Africa
- FAO Agricultural Stress Index (ASI)
- FEWS NET Kenya
- KNBS National Agriculture Production Report

---

## Week 4 additions

### Crop stage weighting (D34)

Every stress observation is weighted by maize growth stage, per
county-month, using `data/metadata/kenya_crop_calendar.csv`.

| Stage | Weight | Reasoning |
|---|---|---|
| planting / vegetative | 1.0 | Failure = no crop |
| grain_fill | 0.7 | Stress reduces yield, doesn't kill |
| harvest | 0.3 | Dry is *good* for harvest |
| fallow | 0.0 | No crop to stress |
| Nairobi | NaN | Urban, no crop signal |

New column: `stress_weighted = stress_avg * crop_stage_weight`

**Effect on 2022 drought:** unweighted flagged 31 counties severe,
weighted flagged 8. Robust across 28 harvest/fallow weight combinations
(see `docs/week04_hardening.md`).

### ERA5 integration (D35)

Four ERA5-Land variables are aggregated to monthly anomalies per
county-month and joined as diagnostic columns (not composite inputs):

- `swvl1_mean_anomaly` — soil moisture 0-7 cm (the lead signal)
- `swvl2_mean_anomaly` — soil moisture 7-28 cm
- `t2m_mean_anomaly` — 2m air temperature
- `pev_mean_anomaly` — potential evaporation

**Lead-lag finding:** `swvl1_mean_anomaly` at t-1 predicts `ndvi_anomaly`
at t with r = 0.461 (95% CI [0.436, 0.485], p = 6e-223). Survives
county demeaning without shrinkage (within-county r = 0.4634).

### Weekly stress product (D36)

`county_weekly_stress_2017_2024.csv` — 19,599 rows.
Weekly rainfall is fresh. Monthly companions are prefixed
`latest_monthly_` and carried forward from the most recent confirmed
month.

**Design principle:** we do not interpolate NDVI to weekly cadence.
That would fabricate satellite observations that never happened.

### Two indices (D37)

The tool reports both:

- `stress_avg` — drought severity (any land use)
- `stress_weighted` — maize-crop damage specifically

A county agriculture officer reads `stress_weighted`. A drought
response coordinator reads `stress_avg`. Both are correct.

### Hardening (D38)

Four robustness tests run before closing Week 4. Full method and
results in `docs/week04_hardening.md`. Artifacts:

- `sensitivity_crop_weights_2022.csv` — 84 weight combinations
- `leadlag_pooled_vs_within.csv` — spatial vs temporal test
- `leadlag_bootstrap_ci.csv` — 1,000-resample CI
- `severe_2022_by_county.csv` — per-county severity table

---

## Week 5 additions

### Null result — scope boundary (D40)

An attempt to extend the monitor to maize yield prediction returned a
null result. No tested formulation of the stress index predicted
county-level yield loss at a level distinguishable from noise.

**Three independent cross-checks confirm the finding is not a data
problem:**

1. **NDMA cross-check** — Kenya's National Drought Management
   Authority flagged 11 counties as Alarm in October 2022, all in the
   arid north. The monitor flagged a different set of 10 counties —
   the highland maize belt and the coast. Zero overlap. CHIRPS
   verification: monitor counties averaged z = -1.14; NDMA counties
   averaged z = -0.71. Both groups were in drought. The two systems
   track different things.
2. **CCRP cross-check** — County Climate Risk Profiles directionally
   confirm 3 of 8 crop-severe counties.
3. **TAMSAT-ALERT cross-check** — Same conceptual finding: soil
   moisture leads crop outcomes.

**Diagnosed cause of the null:** the composite index measures
environmental drought, not crop damage. The 2022 Kakamega outlier
(mildest stress, worst yield crash) was traced to a fall armyworm
outbreak, confirmed against the National Agriculture Production
Report 2025. A climate index cannot capture a pest shock.

**Scope statement:** the tool detects droughts, not yield loss.
The null result is documented at `docs/week05_null_result.md` and
published at
https://kenyaclimatelab.substack.com/p/i-tried-to-validate-my-tool-it-failed.

### Cross-check data

| Source | What it confirms | Direction |
|---|---|---|
| NDMA | Complementary drought regime | Zero overlap in 2022 |
| CCRP | Crop-region vulnerability | 3 of 8 crop-severe counties |
| TAMSAT-ALERT | Soil moisture lead-lag | Same conceptual finding |

---

## Weeks 6-8 additions

- **Week 6** — preprint draft abstract + methods (`paper/draft_v1.md`)
- **Week 7** — mentor outreach to 9 Kenyan researchers (see
  `docs/outreach_notes.md`); custom domain `kenyaclimatelab.me` and
  Zoho Mail to bypass the Gmail-sender barrier (D41)
- **Week 8** — first user testing round, 5 calls
  (`docs/week08_user_feedback.md`); usage guide at `docs/usage.md`;
  data dictionary at `data/metadata/data_dictionary.md`

Full weekly history: `metrics/weekly_log.md` and
`docs/DECISIONS_LOG.md` (D1-D46).
