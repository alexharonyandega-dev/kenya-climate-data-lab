# Data Dictionary & Column Contract

This document defines the schema for `processed/county_monthly_stress_v3.csv`, the canonical dataset for the Kenya Climate Data Lab.

## Dataset Details
- **Row Count:** 4,512 (47 counties × 96 months)
- **Time Span:** 2017-01 to 2024-12
- **Grain:** One row per county per month

## Column Contract
| Column | Type | Description |
| :--- | :--- | :--- |
| `county` | String | Standardized name of the Kenyan county (47 unique). |
| `month_start` | Date | First day of the month (YYYY-MM-01). Primary time key. |
| `year` | Integer | Year extracted from `month_start`. |
| `month` | Integer | Month number (1-12). |
| `rainfall_mm` | Float | Total monthly rainfall aggregated from CHIRPS daily data. |
| `rainfall_anomaly` | Float | Standardized anomaly (z-score) against the county's historical baseline. |
| `ndvi` | Float | Mean monthly NDVI from Sentinel-2. |
| `ndvi_anomaly` | Float | Standardized anomaly (z-score) for vegetation health. |
| `stress_avg` | Float | The composite stress index. Formula: `(0.35 * rainfall_anomaly) + (0.65 * ndvi_anomaly)`. |
| `stress_category` | String | Binned category: `severe_stress`, `moderate_stress`, `normal`, `good`, `very_good`. |
| `crop_stage` | String | Current maize growth stage for the county in this month. |
| `crop_stage_weight` | Float | Weight applied to stress based on crop stage (0.0 to 1.0). |
| `stress_weighted` | Float | `stress_avg * crop_stage_weight`. Used to determine actual crop damage risk. |
| `swvl1_mean_anomaly` | Float | Topsoil moisture anomaly (0-7cm) from ERA5-Land. The early warning signal. |

## Machine Learning Artifacts
- `drought_model.json`: XGBoost classifier predicting next-month severe drought probability.
- `projection_coefs.json`: Per-county linear regression coefficients mapping soil moisture (t-1) to NDVI (t).
