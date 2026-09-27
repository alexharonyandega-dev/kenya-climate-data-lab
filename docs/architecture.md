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
