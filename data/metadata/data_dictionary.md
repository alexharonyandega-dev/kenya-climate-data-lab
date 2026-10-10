# Data Dictionary — county_monthly_stress_v3.csv

**Rows:** 4,512 (47 counties × 96 months, 2017-01 → 2024-12)
**Last updated:** 2026-10-10
**Pipeline source:** see `docs/DECISIONS_LOG.md` for all decisions.

## Columns

| Column | Type | Units | Meaning |
|---|---|---|---|
| `county` | string | — | County name (one of 47) |
| `year` | int | — | Year of the month |
| `month` | int | 1–12 | Month number |
| `date` | date | — | First day of the month |
| `season` | string | — | hot_dry, long_rains, cool_dry, short_rains |
| `rainfall_mm` | float | mm | Total monthly rainfall |
| `rainfall_anomaly` | float | σ (z-score) | Standardized rainfall deviation from same-month climatology |
| `ndvi` | float | 0–1 | Mean monthly NDVI, county-averaged |
| `ndvi_anomaly` | float | σ (z-score) | Standardized NDVI deviation from same-month climatology |
| `stress_avg` | float | σ (z-score) | Composite: 0.65 × ndvi_anomaly + 0.35 × rainfall_anomaly |
| `stress_min` | float | σ (z-score) | min(ndvi_anomaly, rainfall_anomaly) |
| `stress_category` | string | — | Binned stress_avg, see below |
| `rainfall_mm_is_outlier` | bool | — | IQR outlier flag, do not delete |
| `ndvi_is_outlier` | bool | — | IQR outlier flag |
| `stress_avg_is_outlier` | bool | — | IQR outlier flag |
| `stress_min_is_outlier` | bool | — | IQR outlier flag |
| `month_start` | date | — | Same as date, kept for compatibility |
| `month_num` | int | 1–12 | Same as month, kept for compatibility |
| `crop_stage` | string | — | Maize stage: planting / growing / tasseling / harvest / fallow |
| `crop_stage_weight` | float | 0–1 | Weight applied to stress during the crop stage. 0 during fallow |
| `stress_weighted` | float | σ (z-score) | stress_avg × crop_stage_weight |
| `swvl1_mean` | float | m³/m³ | Soil moisture, layer 1 (0–7 cm) |
| `swvl1_mean_anomaly` | float | σ (z-score) | Standardized soil moisture anomaly, topsoil |
| `swvl2_mean_anomaly` | float | σ (z-score) | Soil moisture anomaly, layer 2 (7–28 cm) |
| `t2m_mean_anomaly` | float | σ (z-score) | 2 m air temperature anomaly |
| `pev_mean_anomaly` | float | σ (z-score) | Potential evaporation anomaly |

## Stress categories

| Category | Rule |
|---|---|
| `severe_stress` | stress_avg < -1.25 |
| `moderate_stress` | -1.25 ≤ stress_avg < -0.5 |
| `normal` | -0.5 ≤ stress_avg ≤ 0.5 |
| `good` | 0.5 < stress_avg ≤ 1.25 |
| `very_good` | stress_avg > 1.25 |

## Anomaly definition

For every `*_anomaly` column:

    anomaly(county, month) = (observed - climatology_mean) / climatology_std

where climatology is computed per county from the same calendar month
across the reference period. Full definition and reference periods:
`docs/DECISIONS_LOG.md` D43.

## Known issues

- `stress_avg` uses a 65/35 NDVI/rainfall weighting. Sensitivity was
  tested against 6 alternative weightings in Week 4.
- Outlier flags are informational — do not delete flagged rows without
  reviewing them.
- Reference periods differ per source. Magnitudes are comparable within
  a source but not across sources.

## Related files

- `county_monthly_stress_2017_2024.csv` — pre-v3 version, superseded by v3
- `county_weekly_stress_2017_2024.csv` — weekly resolution
- `docs/DECISIONS_LOG.md` — all pipeline decisions, D1–D46
