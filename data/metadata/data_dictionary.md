# Data Dictionary

Every column in every processed dataset, with dtype, unit, source, and
transformation applied. This is the canonical reference for anyone reading
or joining the project's outputs.

---

## Conventions

- **dtype** reflects the on-disk representation. Note that pandas reads many
  numeric columns as `float64` because of NaN support — this is expected.
- **unit** is the unit of measurement in the column. `-` means dimensionless.
- **source** is the origin dataset or the pipeline script that produced it.
- **transformation** describes what was done between raw input and stored value.

## Common keys

Several files share the same keys. Where they appear, they mean the same thing.

| Column | dtype | Unit | Source | Transformation |
|---|---|---|---|---|
| `county` | string | - | Kenya Constitution 2010 | Standardised to 1 of 47 canonical names via `COUNTY_MAP` (D01, D05) |
| `year` | int | - | various | Parsed from raw date; ISO calendar year |
| `month` | int | 1-12 | various | Parsed from raw date |
| `date` | string | ISO YYYY-MM-DD | various | Parsed via `pd.to_datetime` |
| `season` | string | - | derived | `long_rains` (Mar-Aug) or `short_rains` (Oct-Jan) |
| `iso_year` | int | - | derived | ISO 8601 week-based year |
| `iso_week` | int | 1-53 | derived | ISO 8601 week number |

---

## 1. `chirps_counties_daily_2010_2024.csv`

**Source:** CHIRPS 2.0 Africa daily GeoTIFFs from UCSB Climate Hazards Center
**Produced by:** `scripts/extract_chirps_counties.py`
**Shape:** 5,479 rows x 48 columns
**Coverage:** 2010-01-01 to 2024-12-31, daily
**Grain:** one row per day

This file contains daily rainfall totals for each of Kenya's 47 counties,
plus a date column. It's the primary rainfall signal for the project.

| Column | dtype | Unit | Transformation |
|---|---|---|---|
| `date` | string | ISO YYYY-MM-DD | Extracted from GeoTIFF filename |
| 47 county columns | float64 | mm/day | Spatial mean over county polygon, computed once per file |

**County columns (in alphabetical order):**
`Baringo, Bomet, Bungoma, Busia, Elgeyo-Marakwet, Embu, Garissa, Homa Bay,
Isiolo, Kajiado, Kakamega, Kericho, Kiambu, Kilifi, Kirinyaga, Kisii,
Kisumu, Kitui, Kwale, Laikipia, Lamu, Machakos, Makueni, Mandera,
Marsabit, Meru, Migori, Mombasa, Murang'a, Nairobi, Nakuru, Nandi, Narok,
Nyamira, Nyandarua, Nyeri, Samburu, Siaya, Taita Taveta, Tana River,
Tharaka, Trans Nzoia, Turkana, Uasin Gishu, Vihiga, Wajir, West Pokot`

**Missing values:** 1,457 cells are NaN. This is exactly 31 days x 47 counties
= December 2021, a known gap in the CHIRPS 2.0 Africa daily archive (D07).
No interpolation was applied.

**Known bias:** CHIRPS overestimates rainfall in Kenya's northern ASALs by
+20% to +85% (D08). This cancels out in anomaly-based analysis.

**Notes:** Ocean pixels (nodata = -9999) were masked to NaN before averaging.
County means computed using precomputed pixel masks (D06).

---

## 2. `county_weekly_rainfall_2017_2024.csv`

**Source:** Derived from `chirps_counties_daily_2010_2024.csv`
**Produced by:** `scripts/build_weekly_rainfall.py`
**Shape:** 19,599 rows x 9 columns
**Coverage:** ISO weeks 2017-2024
**Grain:** one row per (county, ISO year, ISO week)

Weekly rainfall tier of the two-tier monitor design (D04). This is the
fast-update layer that can refresh weekly.

| Column | dtype | Unit | Transformation |
|---|---|---|---|
| `iso_year` | int | - | ISO 8601 week-based year |
| `iso_week` | int | 1-53 | ISO 8601 week number |
| `county` | string | - | From daily rainfall CSV |
| `rainfall_mm` | float64 | mm/week | Sum of daily rainfall over the ISO week |
| `rain_clim_mean` | float64 | mm/week | Mean rainfall for that (county, ISO week) across 2017-2024 |
| `rain_clim_std` | float64 | mm/week | Std dev of that climatology |
| `n_years` | int | - | Number of years contributing to the climatology (max 8) |
| `rainfall_anomaly` | float64 | z-score | (rainfall_mm - rain_clim_mean) / rain_clim_std |
| `rainfall_anomaly_4wk` | float64 | z-score | 4-week rolling mean of rainfall_anomaly, per county |

**Missing values:** `rainfall_anomaly` and `rainfall_anomaly_4wk` are NaN
during the December 2021 window.

**Notes:** ISO-year edge rows (Jan 1-3 belonging to ISO year 2016; Dec
30-31 belonging to ISO year 2025) were filtered out (D10). ISO week 53
exists in some years and is preserved.

---

## 3. `ndvi_counties_monthly_2017_2024.csv`

**Source:** Sentinel-2 SR imagery via Google Earth Engine
**Produced by:** `scripts/gee/ndvi_counties_monthly.js`
**Shape:** 4,512 rows x 5 columns
**Coverage:** January 2017 to December 2024, monthly
**Grain:** one row per (county, year, month)

Monthly NDVI means per county. This is the vegetation-health signal.

| Column | dtype | Unit | Transformation |
|---|---|---|---|
| `name` | string | - | County name (equivalent to `county` in other files) |
| `year` | float64 | - | Calendar year |
| `month` | float64 | 1-12 | Calendar month |
| `date` | string | ISO YYYY-MM-DD | First day of month |
| `mean` | float64 | NDVI | Spatial mean of cloud-masked NDVI over the county polygon |

**Missing values:** 252 rows (5.6%) have NaN `mean`, corresponding to
county-months where Sentinel-2 saw no clear-sky observations (D13).

**Notes:**
- NDVI values outside [0, 1] were set to NaN before aggregation (D12).
- Cloud mask threshold: 40% cloudy pixel percentage.
- Scale: 1000m (D11).
- Extracted at 1000m resolution instead of 500m to avoid GEE memory limits.
- `year` and `month` are float64 rather than int due to GEE CSV export
  behaviour. Cast to int before joining.

---

## 4. `county_monthly_panel_2017_2024.csv`

**Source:** Joins of files 1, 2, and 3
**Produced by:** `scripts/build_county_monthly_panel.py`
**Shape:** 4,512 rows x 9 columns
**Coverage:** 2017-2024, monthly
**Grain:** one row per (county, year, month)

The joined monthly panel: rainfall (from CHIRPS aggregated to monthly) plus
NDVI, with per-county per-calendar-month anomalies for both.

| Column | dtype | Unit | Transformation |
|---|---|---|---|
| `county` | string | - | From CHIRPS CSV |
| `year` | int | - | Calendar year |
| `month` | int | 1-12 | Calendar month |
| `date` | string | ISO YYYY-MM-DD | First day of month |
| `season` | string | - | `long_rains`, `short_rains`, `cool_dry`, or `hot_dry` |
| `rainfall_mm` | float64 | mm/month | Sum of daily rainfall over the month |
| `rainfall_anomaly` | float64 | z-score | (rainfall_mm - per-county-month mean) / std |
| `ndvi` | float64 | NDVI | From NDVI CSV |
| `ndvi_anomaly` | float64 | z-score | (ndvi - per-county-month mean) / std |

**Missing values:** Inherited from CHIRPS (December 2021) and NDVI (252 rows).
Total NaN rows: 260.

**Notes:** Anomalies are computed per-county-per-calendar-month. This means
each county's October 2022 rainfall is compared to its own Octobers from
2017-2024 — the correct per-county baseline. This is why a drought in the
normally-wet western highlands produces larger anomalies than the same
absolute rainfall in the always-dry northern ASALs (see D24).

---

## 5. `county_monthly_stress_2017_2024.csv`

**Source:** Derived from `county_monthly_panel_2017_2024.csv`
**Produced by:** `scripts/compute_stress_index.py`
**Shape:** 4,512 rows x 12 columns
**Coverage:** 2017-2024, monthly
**Grain:** one row per (county, year, month)

This is the **master table** of the project (D03). It contains the composite
stress index — the primary output of the stress monitor.

| Column | dtype | Unit | Transformation |
|---|---|---|---|
| `county` | string | - | - |
| `year` | int | - | - |
| `month` | int | 1-12 | - |
| `date` | string | ISO YYYY-MM-DD | - |
| `season` | string | - | - |
| `rainfall_mm` | float64 | mm/month | Inherited from panel |
| `rainfall_anomaly` | float64 | z-score | Inherited from panel |
| `ndvi` | float64 | NDVI | Inherited from panel |
| `ndvi_anomaly` | float64 | z-score | Inherited from panel |
| `stress_avg` | float64 | z-score | 0.35 * rainfall_anomaly + 0.65 * ndvi_anomaly (D24) |
| `stress_min` | float64 | z-score | min(rainfall_anomaly, ndvi_anomaly) (D26) |
| `stress_category` | string | - | Derived from stress_avg (see below) |

**Stress categories (D25):**

| Category | Threshold (stress_avg) |
|---|---|
| `severe_stress` | < -1.25 |
| `moderate_stress` | -1.25 to -0.50 |
| `normal` | -0.50 to +0.50 |
| `good` | +0.50 to +1.25 |
| `very_good` | > +1.25 |
| `no_data` | stress_avg is NaN |

**Observed distribution (2017-2024):**
- severe_stress: 138 rows (3.1%)
- moderate_stress: 1,105 rows (24.5%)
- normal: 1,863 rows (41.3%)
- good: 912 rows (20.2%)
- very_good: 234 rows (5.2%)
- no_data: 260 rows (5.8%)

**Notes:** `stress_avg` reflects the overall condition. `stress_min` follows
the early-warning convention: a location is only as healthy as its worst
signal. Both are retained because they serve different purposes (D26).

---

## 6. `isda_soil_raster_zonal.csv`

**Source:** iSDAsoil Cloud-Optimized GeoTIFFs on AWS S3
**Produced by:** `scripts/fetch_isda_soil_raster.py`
**Shape:** 5 rows x 97 columns
**Coverage:** 5 target counties (Nakuru, Kakamega, Bungoma, Trans Nzoia,
Uasin Gishu)
**Grain:** one row per county

Zonal statistics from iSDAsoil 30m rasters. Every column follows the same
naming pattern, so the table is documented by pattern rather than by
individual column.

**Naming pattern:** `{property}_{stat}_{depth}[_agg]`

| Component | Values | Meaning |
|---|---|---|
| `property` | see table below | Soil property |
| `stat` | `mean` or `stdev` | Band of the COG. `mean` = the property's spatial mean. `stdev` = the property's spatial standard deviation |
| `depth` | `0_20` or `20_50` | Soil depth in cm |
| `_agg` | `_std`, `_n`, or absent | `_std` = std dev of the band across pixels. `_n` = pixel count. Absent = mean of the band across pixels |

**Soil properties (8):**

| Property name | Unit | Description |
|---|---|---|
| `ph` | - | Soil pH (x10 in storage, back-transformed) |
| `nitrogen_total` | g/kg | Total soil nitrogen |
| `phosphorous_extractable` | ppm | Extractable phosphorus |
| `potassium_extractable` | ppm | Extractable potassium |
| `carbon_organic` | g/kg | Soil organic carbon |
| `cation_exchange_capacity` | cmol(+)/kg | Effective cation exchange capacity |
| `clay_content` | % | Clay fraction |
| `sand_content` | % | Sand fraction |

**Example columns:**
- `ph_mean_0_20` — mean of pH 0-20cm band across county pixels
- `ph_mean_0_20_std` — std of that mean across pixels
- `ph_mean_0_20_n` — pixel count (typically ~2.8 million per county)
- `ph_stdev_0_20` — mean of the pH stdev band across pixels
- `ph_mean_20_50` — mean of pH 20-50cm band
- ...and so on for each property

**Back-transformations (D17):**

Some properties are stored with a mathematical transform that must be
undone. The transformations were reverse-engineered by comparing raster
values against iSDAsoil's point API.

| Property | Back-transform |
|---|---|
| `ph` | divide by 10 (stored as pH x 10) |
| `nitrogen_total` | `exp(x/100) - 1` |
| `phosphorous_extractable` | `exp(x/10) - 1` |
| `potassium_extractable` | `exp(x/10) - 1` |
| `carbon_organic` | `exp(x/10) - 1` |
| `cation_exchange_capacity` | `exp(x/10) - 1` |
| `clay_content`, `sand_content` | stored raw (no transform) |

**Notes:** This file supersedes the earlier centroid-only and 15-point
sampling versions (D15, D16). Pixel counts are ~2.8 million per county per
property — approximately 20 million values per property across the 5
counties.

---

## 7. `kenya_crop_calendar.csv`

**Source:** Compiled from FAO GIEWS, KALRO, and FEWS NET livelihood-zone
descriptions
**Produced by:** `scripts/build_crop_calendar.py`
**Shape:** 47 rows x 9 columns
**Coverage:** All 47 Kenyan counties
**Grain:** one row per county

Classifies each county into one of seven agro-ecological zones with the
seasons that matter for maize.

| Column | dtype | Unit | Meaning |
|---|---|---|---|
| `county` | string | - | Canonical county name |
| `zone` | string | - | One of 7 zones (see below) |
| `zone_description` | string | - | Human-readable zone description |
| `n_seasons` | int | 0, 1, or 2 | Number of maize-growing seasons |
| `long_rains_start` | float64 | month 1-12 | Start of long rains season |
| `long_rains_end` | float64 | month 1-12 | End of long rains season |
| `short_rains_start` | float64 | month 1-12 | Start of short rains season |
| `short_rains_end` | float64 | month 1-12 | End of short rains season |
| `primary_harvest_month` | float64 | month 1-12 | Month when primary harvest typically occurs |

**Zones (7):**

| Zone | Seasons | Counties |
|---|---|---|
| `highland_west` | Long + short rains | 14 |
| `central_highlands` | Long + short rains | 8 |
| `rift_valley` | Long rains only | 7 |
| `asal_north` | Short rains only | 7 |
| `coastal` | Long + short rains | 6 |
| `eastern` | Short rains dominant | 4 |
| `urban` | None | 1 (Nairobi) |

**Missing values:** None for `county`, `zone`, `zone_description`,
`n_seasons`. Months are NaN where the season doesn't apply (e.g., short rains
for a rift_valley county).

**Notes (D05):** Kenya is not homogeneous. Western highlands are bimodal,
Rift Valley is unimodal long-rains, northern ASAL is short-rains-only. This
file allows downstream analysis to weight the stress index by in-season
months for each county.

---

## File inventory

| File | Rows | Cols | Grain | Source |
|---|---|---|---|---|
| `chirps_counties_daily_2010_2024.csv` | 5,479 | 48 | county x day | CHIRPS |
| `county_weekly_rainfall_2017_2024.csv` | 19,599 | 9 | county x ISO week | derived |
| `ndvi_counties_monthly_2017_2024.csv` | 4,512 | 5 | county x month | Sentinel-2 |
| `county_monthly_panel_2017_2024.csv` | 4,512 | 9 | county x month | joined |
| `county_monthly_stress_2017_2024.csv` | 4,512 | 12 | county x month | derived (master) |
| `isda_soil_raster_zonal.csv` | 5 | 97 | county | iSDAsoil |
| `kenya_crop_calendar.csv` | 47 | 9 | county | compiled |

---

*Last updated: 2026-09-27*  
*Companion documents: `docs/DECISIONS_LOG.md`, `docs/architecture.md`*
