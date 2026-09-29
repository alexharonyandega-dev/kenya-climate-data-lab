# Data Notes - Kenya Climate Data Lab

**Author:** Alex Haro Nyandega
**Date:** 2026-10-17
**Version:** v2 (enhanced stress monitor, Week 4)
**Master file:** `data/processed/county_monthly_stress_v3.csv`

---

## 1. Study area

All **47 Kenyan counties**. Seven agro-ecological zones for maize:
highland west, central highlands, rift valley, ASAL north, coastal,
eastern, and urban (Nairobi). County boundaries from geoBoundaries
ADM1.

## 2. Time period

| Layer | Coverage | Resolution |
|---|---|---|
| Stress monitor (master) | 2017-2024 | monthly |
| Weekly rainfall | 2017-2024 | ISO week |
| Rainfall history | 2010-2024 | daily |
| ERA5 climate | 1990-2024 | daily |

## 3. Data sources

| Dataset | Role | Resolution | Coverage |
|---|---|---|---|
| CHIRPS 2.0 | Primary rainfall | 0.05 deg daily | 2010-2024 |
| Sentinel-2 NDVI | Vegetation stress | 10m, monthly composite | 2017-2024 |
| ERA5-Land | Soil moisture, temperature, evaporation | 0.1 deg daily | 1990-2024 |
| iSDAsoil | Soil properties (pH, CEC, N, P, etc.) | 30m static | static |
| geoBoundaries ADM1 | County boundaries | vector | static |
| Kenya crop calendar | Crop stage weighting | county-month | static |
| KNBS | Yield validation (deferred) | county-year | 2020-2024 |
| FAOSTAT | National yield validation (deferred) | national-year | 1961-2024 |

**Substitution note.** The Kenya Meteorological Department (KMD)
portal was not responsive during data collection. CHIRPS 2.0 was
substituted as the primary rainfall source, consistent with existing
East African agricultural research practice.

## 4. Preprocessing

### 4.1 Date standardisation
Every date column parsed with `pd.to_datetime(..., errors="coerce")`
and stored as ISO `YYYY-MM-DD`.

### 4.2 Spatial aggregation
CHIRPS GeoTIFFs masked per county polygon using **precomputed pixel
masks** (D06). This reduced runtime from an estimated 3 hours to
3.1 minutes for 47 counties. ERA5-Land clipped to Kenya bbox and
aggregated per county.

### 4.3 Temporal aggregation
- Daily CHIRPS -> weekly totals (ISO weeks)
- Daily CHIRPS -> monthly rainfall sums
- Daily ERA5 -> monthly means per county

### 4.4 Anomaly computation
For each `(county, month_num)`, anomaly = (value - climatological mean)
/ climatological std. Each county is compared to **its own history**,
not a national average. This is the core of the "how unusual is this
month for this county?" question.

### 4.5 Missing values
- December 2021 CHIRPS files missing from source -> left as NaN (D07).
  1,457 county-days. Not interpolated.
- NDVI cloud-gap months -> left as NaN (D14). 5.6% of county-months.
- Nairobi crop stage weight -> NaN by design (D34). Urban county,
  no maize signal.
- **No interpolation of any climate or vegetation signal.** Fabricating
  a satellite observation would be worse than reporting the gap.

### 4.6 Outliers
IQR rule applied to rainfall, temperature, and stress. Outliers
flagged with `*_is_outlier` boolean columns but **not removed** (D31).
Extreme values are signal, not noise.

## 5. Stress index construction

**Composite:**

    stress_avg      = 0.35 * rainfall_anomaly + 0.65 * ndvi_anomaly
    stress_min      = min(rainfall_anomaly, ndvi_anomaly)
    stress_weighted = stress_avg * crop_stage_weight

**Crop stage weights (D34):**

| Stage | Weight | Reasoning |
|---|---|---|
| Planting / vegetative | 1.0 | Failure = no crop |
| Grain fill | 0.7 | Stress reduces yield, doesn't kill |
| Harvest | 0.3 | Dry is *good* for harvest |
| Fallow | 0.0 | No crop to stress |
| Nairobi | NaN | Urban, no crop signal |

**Weight rationale.** The 65/35 split reflects the 2021-2022 drought
finding (D24): rainfall anomaly was lowest in 2021, but vegetation
collapse peaked in 2022. Drought is cumulative - soil moisture
reserves deplete over multiple seasons, so the vegetation signal
lags the rainfall signal by roughly a season.

## 6. Merge strategy

Full audit in `data/processed/stress_join_audit.csv`.

| # | Left | Right | Keys | Type | Result | Dropped |
|---|---|---|---|---|---|---|
| J01 | stress | crop_calendar_weights | (county, month_num) | left | 4,512 | 0 |
| J02 | stress_v2 | era5_monthly_anomalies | (county, month_start) | left | 4,512 | 0 |
| J03 | weekly_rainfall | monthly_companion | (county, month_start) | left | 19,599 | 0 |

**No silent merges.** Every join is wrapped in `logged_join()`.
Duplicate keys in the right table are flagged before merging.
Left joins used throughout because the master table defines the
universe of county-months; auxiliary data enriches but does not
filter.

## 7. Week 4 findings

**7.1 Crop-stage weighting differentiates the 2022 signal.**
Under the 2022 drought:
- Unweighted index (`stress_avg`) flagged **31 counties** severe
- Weighted index (`stress_weighted`) flagged **8 counties** severe

The drop is because most Kenyan counties were in harvest or fallow
at peak 2022 stress. Only 8 had maize in the ground. The two
indices answer different questions:
- `stress_avg` = "how bad is the drought?"
- `stress_weighted` = "how much does it hurt the maize crop?"

**7.2 Soil moisture leads vegetation by one month.**
Lead-lag correlation between `swvl1_mean_anomaly` (0-7 cm soil
moisture) and `ndvi_anomaly`:
- Lag +1 month: **r = 0.461, p = 2e-220, n = 4,205**
- Contemporaneous: r = 0.364
- Lag +2: r = 0.372

Soil dries first, vegetation follows. `swvl1_mean_anomaly` becomes
the earliest signal in the weekly product.

**7.3 Three-signal divergence (2020-2024).**
Rainfall anomaly bottomed out in 2021. Soil moisture collapsed
earliest. NDVI collapsed last and hardest (December 2022, -1.35 sigma).
This is the physical mechanism of cumulative drought, visible in the
data.

## 8. Final dataset shape

**Monthly master** (`county_monthly_stress_v3.csv`):
- Rows: 4,512 (47 counties x 96 months)
- Columns: 27
- Unique keys: (county, month_start)
- No duplicates

**Weekly product** (`county_weekly_stress_2017_2024.csv`):
- Rows: 19,599
- Columns: 21
- Monthly companions prefixed `latest_monthly_`
- Weekly rainfall is fresh; monthly signal is last-confirmed

## 9. Reproduction

Run in order on a fresh kernel:

1. `notebooks/01_data_exploration.ipynb`
2. `notebooks/02_data_cleaning.ipynb`
3. `notebooks/03_integration.ipynb`

Every cell completes without error. Total runtime < 3 minutes.
`scripts/verify_reproducibility.py` confirms byte-identical output.

## 10. Known limitations

1. **CHIRPS positive bias** in arid regions (+10% to +85%). Anomaly-based
   analysis cancels uniform bias (D08), but absolute values in ASAL
   counties should be read as relative.
2. **Monthly NDVI.** Weekly vegetation monitoring would need 384 GEE
   exports instead of 96. The weekly product is rainfall-led with
   monthly companions carried forward.
3. **County averages hide sub-county variation.** Meru, Bungoma, and
   Narok in particular have internal climate gradients the county mean
   smooths out.
4. **Formal validation is deferred.** The tool detected the 2022 drought
   without calibration, but a systematic comparison against KNBS county
   yield data is Week 5+ work.
5. **No pest, fertiliser, or market data.** These affect crop outcomes
   independently of weather.
