Kenya lacks a public drought monitor that works at county level for all 47 counties. Tools that exist either fail at county resolution or publish so late the harvest is already lost.

We present a composite stress index built from CHIRPS satellite rainfall, Sentinel-2 vegetation health, and ERA5-Land soil moisture. The index compares each county-month to that county's own historical climatology, so no calibration or training data is required.

Applied to the 2022 Horn of Africa drought, the index identified severe stress without calibration. Of 31 counties with severe drought in 2022, only 8 had it while maize was growing.

Cross-checked against NDMA's drought classifications, the index flagged a different set of counties. Zero overlap. Both systems were right: NDMA tracks pastoral drought in 23 ASAL counties; the index tracks crop-region vegetation stress in all 47.

Soil moisture anomaly leads NDVI anomaly by one month (r = 0.461, 95% CI [0.436, 0.485]).

We also tested whether the index predicts maize yield loss. It does not. We document the null result.

The full pipeline is open source at github.com/alexharonyandega-dev/kenya-climate-data-lab.

---

## 2. Data Sources

The monitor uses five sources. All are publicly accessible. All are reproducible without institutional access.

### CHIRPS 2.0 — Rainfall

Rainfall data comes from the Climate Hazards Group Infrared Precipitation with Station data version 2.0 (CHIRPS 2.0), a 0.05° (~5 km) daily gridded product distributed by the University of California, Santa Barbara. CHIRPS combines satellite thermal infrared estimates with ground station records and has been widely used in East African agricultural research. We use the Africa daily tile archive for the years 2010–2024 (5,448 files, 4.3 GB). County-level daily rainfall is extracted by precomputing a pixel mask for each of the 47 county polygons, then aggregating all pixels within the mask per day. This reduces extraction runtime from an estimated three hours (polygon intersection per day per county) to 3.1 minutes for the full 15-year archive.

### Sentinel-2 NDVI — Vegetation health

Vegetation health comes from the Normalized Difference Vegetation Index (NDVI) derived from Sentinel-2 multispectral imagery (European Space Agency Copernicus programme, 10 m native resolution). We use monthly maximum-value composite NDVI, generated via Google Earth Engine and aggregated to county-level monthly means across the 47 counties for the years 2017–2024. The composite approach reduces cloud contamination by selecting, per pixel, the clearest observation within each month. Approximately 5.6% of county-months have no clear-sky observation and are left as missing, not interpolated.

### ERA5-Land — Soil moisture and temperature

Soil moisture and temperature come from ERA5-Land, a global land-surface reanalysis produced by the European Centre for Medium-Range Weather Forecasts, available at 0.1° (~9 km) hourly resolution from 1950 to present. We use daily means of four variables: volumetric soil water at 0–7 cm (swvl1) and 7–28 cm (swvl2), 2m air temperature (t2m), and potential evaporation (pev). County-level daily values are computed by masking the ERA5-Land grid to each county polygon and averaging across all covered pixels. The 1990–2024 archive provides a 35-year baseline for anomaly computation.

### iSDAsoil — Soil properties

Soil properties come from iSDAsoil, a 30 m resolution African soil property map derived from machine learning over 130,000 field samples. We use 14 properties — including pH, organic carbon, total nitrogen, cation exchange capacity, and texture fractions — aggregated to county-level means via zonal statistics over the 47 county polygons. Unlike the climate sources, iSDAsoil is static: it provides one value per county rather than a time series. We include it as a contextual covariate, not as a dynamic input to the composite index.

### Kenya crop calendar — Crop-stage weighting

Crop-stage information comes from a Kenya county crop calendar compiled from FEWS NET livelihood profiles, FAO crop calendars, and county agronomy extension reports. The calendar assigns each of the 47 counties to one of seven agro-ecological zones and specifies, for each county, the start and end months of the long-rains and short-rains seasons and the primary harvest month. We use this to weight each county-month by maize growth stage: planting and vegetative stages receive weight 1.0, grain fill 0.7, harvest 0.3, and fallow 0.0. Nairobi, an urban county, receives a missing weight.

### Summary

| Source | Resolution | Coverage | Role |
|---|---|---|---|
| CHIRPS 2.0 | 0.05° daily | 2010–2024 | Primary rainfall signal |
| Sentinel-2 NDVI | 10 m monthly composite | 2017–2024 | Primary vegetation signal |
| ERA5-Land | 0.1° daily | 1990–2024 | Soil moisture, temperature |
| iSDAsoil | 30 m static | static | Soil covariates (contextual) |
| Kenya crop calendar | county-month | static | Crop-stage weighting |

---

## 3. Preprocessing

The pipeline converts raw gridded climate data into a county-month panel of standardized anomalies. Four preprocessing decisions shape the final product.

### 3.1 Spatial aggregation via precomputed pixel masks

For each of the 47 counties, a binary pixel mask is computed once from the geoBoundaries ADM1 polygon. All gridded climate sources (CHIRPS, ERA5-Land) are then masked and averaged within each county per day. This avoids per-file polygon intersection, which is the standard bottleneck for county-level satellite aggregation. Runtime for the full CHIRPS archive drops from an estimated three hours to 3.1 minutes (D06).

### 3.2 Temporal aggregation

CHIRPS daily rainfall is aggregated to two products: ISO-week totals (for the weekly monitor) and calendar-month sums (for the composite stress index). ERA5-Land daily means are aggregated to calendar-month means. Sentinel-2 NDVI is delivered as monthly composites directly from Google Earth Engine; no further temporal aggregation is applied.

### 3.3 Anomaly computation

For each county and each calendar month, the anomaly is defined as the standardized deviation of the observed value from the county's own historical climatology:

    anomaly(county, month) = (observed - climatology_mean) / climatology_std

Climatological means and standard deviations are computed per county per calendar month across all available years. This means each county is compared to its own historical distribution — not to a national average, and not to neighbouring counties. The three input anomalies (rainfall, NDVI, soil moisture) are computed with the same method.

### 3.4 Missing-value policy

Missing values are left as NaN. No interpolation is applied to any climate or vegetation signal. This decision has three components:

- **December 2021 CHIRPS gap.** The Africa daily tile archive is missing all 31 daily files for December 2021. Those 1,457 county-days (31 days × 47 counties) are left as missing rather than estimated from the monthly aggregate. Interpolating across a full month would fabricate a rainfall signal that the satellites never recorded (D07).
- **Sentinel-2 cloud gaps.** Approximately 5.6% of county-months have no clear-sky Sentinel-2 observation. Those county-months are left as NaN. The composite stress index for those months is also NaN, since NDVI is a required input (D14).
- **Nairobi crop-stage weight.** Nairobi is an urban county with no significant maize production. Its crop-stage weight is set to NaN by design, so any crop-weighted stress value for Nairobi is NaN. The unweighted stress index is still computed for Nairobi (D34).

The consequence of this policy is that downstream analyses must handle NaN. In practice: the composite stress index has NaN for approximately 5.8% of county-months, concentrated in the western highlands during the long-rains season.

### Summary

| Decision | Method | Reference |
|---|---|---|
| Spatial aggregation | Precomputed pixel masks | D06 |
| Temporal aggregation | Weekly (rainfall) / monthly (all) | D03 |
| Anomaly | Standardized deviation from county climatology | D03 |
| Missing values | NaN — no interpolation | D07, D14, D34 |
