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

CHIRPS daily rainfall is aggregated to two products: ISO-week totals (for the weekly monitor) and calendar-month sums (for the composite stress index). ERA5-Land daily means are aggregated to calendar-month means. Sentinel-2 NDVI is delivered as monthly composites directly from Google Earth Engine; no further temporal aggregation is applied (D04).

### 3.3 Anomaly computation

For each county and each calendar month, the anomaly is defined as the standardized deviation of the observed value from the county's own historical climatology:

    anomaly(county, month) = (observed - climatology_mean) / climatology_std

Climatological means and standard deviations are computed per county per calendar month across all available years. This means each county is compared to its own historical distribution — not to a national average, and not to neighbouring counties. The three input anomalies (rainfall, NDVI, soil moisture) are computed with the same method (D43).

### 3.4 Missing-value policy

Missing values are left as NaN. No interpolation is applied to any climate or vegetation signal. This decision has three components:

- **December 2021 CHIRPS gap.** The Africa daily tile archive is missing all 31 daily files for December 2021. Those 1,457 county-days (31 days × 47 counties) are left as missing rather than estimated from the monthly aggregate. Interpolating across a full month would fabricate a rainfall signal that the satellites never recorded (D07).
- **Sentinel-2 cloud gaps.** Approximately 5.6% of county-months have no clear-sky Sentinel-2 observation. Those county-months are left as NaN. The composite stress index for those months is also NaN, since NDVI is a required input (D13).
- **Nairobi crop-stage weight.** Nairobi is an urban county with no significant maize production. Its crop-stage weight is set to NaN by design, so any crop-weighted stress value for Nairobi is NaN. The unweighted stress index is still computed for Nairobi (D34).

The consequence of this policy is that downstream analyses must handle NaN. In practice: the composite stress index has NaN for approximately 5.8% of county-months, concentrated in the western highlands during the long-rains season.

### Summary

| Decision | Method | Reference |
|---|---|---|
| Spatial aggregation | Precomputed pixel masks | D06 |
| Temporal aggregation | Weekly (rainfall) / monthly (all) | D04 |
| Anomaly | Standardized deviation from county climatology | D43 |
| Missing values | NaN — no interpolation | D07, D13, D34 |

---

## 4. Stress Index

The monitor produces two composite indices from the same underlying anomalies.

### 4.1 Composite formula

The composite stress index is a weighted average of the two primary anomaly signals:

    stress_avg = 0.35 × rainfall_anomaly + 0.65 × ndvi_anomaly

The 65/35 weighting is deliberately asymmetric. During the 2021–2022 drought, rainfall anomaly was lowest in 2021 (−0.193 annual mean), but vegetation collapse peaked a full year later in 2022 (December NDVI anomaly −1.35). Rainfall alone cannot explain that one-year lag. Vegetation integrates the accumulated soil-moisture deficit across multiple seasons. The composite therefore weights the slower-moving vegetation signal more heavily (D24).

### 4.2 Stress categories

Each county-month is assigned a category based on `stress_avg` (D25):

| Category | Threshold |
|---|---|
| severe_stress | stress_avg < −1.25 |
| moderate_stress | −1.25 ≤ stress_avg < −0.50 |
| normal | −0.50 ≤ stress_avg ≤ +0.50 |
| good | +0.50 < stress_avg ≤ +1.25 |
| very_good | stress_avg > +1.25 |

Thresholds are symmetric around zero at ±0.50 and ±1.25 standard deviations. Observed distribution across 2017–2024: 3.1% severe, 24.5% moderate, 41.3% normal, 20.2% good, 5.2% very good.

### 4.3 stress_min as a complementary signal

Alongside `stress_avg`, the monitor computes `stress_min` as the minimum of the two input anomalies:

    stress_min = min(rainfall_anomaly, ndvi_anomaly)

This follows the operational convention used by early-warning systems: a region is only as healthy as its worst signal. `stress_avg` is used for ranking and visualisation; `stress_min` is used for alerting (D26).

### 4.4 Crop-stage weighting

A second index weights the composite by maize growth stage, using the Kenya crop calendar (Section 2):

    stress_weighted = stress_avg × crop_stage_weight

Stage weights: planting and vegetative stages 1.0, grain fill 0.7, harvest 0.3, fallow 0.0. Nairobi, an urban county with no significant maize production, receives a NaN weight (D34).

The purpose of the weighting is to distinguish drought severity from crop damage. A dry October is severe drought in Kakamega (short-rains planting) and beneficial weather in Trans Nzoia (post-harvest). The weighted index encodes that distinction.

### 4.5 Two indices, two questions

The final product is therefore two indices, not one (D37):

- **`stress_avg`** answers: *how severe is drought in this county, regardless of land use?*
- **`stress_weighted`** answers: *how much does this drought threaten the maize crop?*

A county agriculture officer reads `stress_weighted`. A drought response coordinator reads `stress_avg`. The two indices agree in the direction of change but differ in magnitude. The distinction is preserved throughout the paper.

### Summary

| Component | Purpose | Reference |
|---|---|---|
| stress_avg | Composite drought severity | D24 |
| Stress categories | Categorical classification | D25 |
| stress_min | Worst-signal alerting | D26 |
| crop_stage_weight | Growth-stage weighting | D34 |
| stress_weighted | Crop-specific damage index | D37 |

---

## 5. Validation

### 5.1 The 2022 Horn of Africa drought

The 2021–2022 Horn of Africa drought was the worst in 40 years, with five consecutive failed rainy seasons. The monitor was applied to this period without any calibration or parameter fitting.

The composite index detected severe stress across multiple counties without prior training. Of 31 counties with severe drought in 2022, only 8 had severe drought while maize was actively growing: Bomet, Busia, Homa Bay, Kericho, Kilifi, Laikipia, Nandi, and Nyamira. The other 23 counties were in harvest or fallow when the drought peaked. Kenya's largest maize producers are not on the severe list — they had already harvested.

### 5.2 Sensitivity analysis

The crop-stage weighting uses parameters chosen by the analyst (planting 1.0, grain_fill 0.7, harvest 0.3, fallow 0.0). To test the robustness of the 31-vs-8 result, we recomputed the 2022 severe-count across 28 alternative combinations of harvest and fallow weights, holding planting and grain_fill fixed.

**Result:** every combination produces exactly 8 severe counties. The finding is not sensitive to the weight choices (D38).

Additional sensitivity: varying grain_fill from 0.4 to 0.8 keeps the count at 8. Above 0.9 (grain_fill ≈ planting), the count rises to 10 then 16. The chosen 0.7 sits comfortably inside the stable range.

### 5.3 Bootstrap confidence interval

For the soil-moisture lead-lag relationship (soil moisture at t−1 predicts NDVI at t), we computed a 95% confidence interval using 1,000 bootstrap resamples of the 4,205 paired observations.

**Result:** r = 0.461, 95% CI [0.436, 0.485]. The effect is entirely temporal: within-county demeaned correlation (0.4634) is indistinguishable from the pooled value (0.4610) (D38).

### 5.4 Cross-validation against NDMA

The National Drought Management Authority classifies Kenya's 23 ASAL counties into four drought phases each month. We compared the monitor's severe-stress counties against NDMA's Alarm phase in June and October 2022.

**Result:** zero overlap in both months. The monitor flagged highland and coastal counties; NDMA flagged arid-north counties. The two systems are not measuring the same thing.

CHIRPS rainfall verification (October 2022 against 2010–2021 baseline): monitor severe counties averaged z = −1.14; NDMA Alarm counties averaged z = −0.71. Both groups had below-normal rainfall. The two systems track different drought regimes: NDMA classifies pastoral impact in 23 ASAL counties by cumulative multi-season failure; the monitor classifies current-month crop-region vegetation stress across all 47 counties.

### 5.5 Null result: the index does not predict yield

We tested whether the stress index predicts county-level maize yield loss, using KNBS county production data for the 5 counties where both signals are available.

**Result:** the index does not predict yield loss. Across 20 county-year observations, correlation between stress_mean and yield change was r = −0.085 (p = 0.723). Across 5 counties in 2022 alone, r = −0.832 — but with the wrong sign, driven by a single outlier (D40).

The outlier is Kakamega. Kakamega had the mildest 2022 stress of the 5 counties (−0.182) and the worst yield crash (−42.5%). Its area planted increased 2% while production fell 41% — a signature of pest damage, not drought. The National Agriculture Production Report 2025 (page 31) confirms a fall armyworm outbreak in the region.

The tool detects droughts. It does not predict crop failure. Those are different problems, and only the first one is currently solved.

### Summary

| Test | Result | Reference |
|---|---|---|
| 2022 drought detection | 31 severe, 8 crop-severe | D24, D34 |
| Sensitivity analysis | 28/28 combos produce 8 | D38 |
| Bootstrap CI | r = 0.461, [0.436, 0.485] | D38 |
| NDMA cross-check | Zero overlap, verified by CHIRPS | D41 |
| Yield prediction | Null result | D40 |
