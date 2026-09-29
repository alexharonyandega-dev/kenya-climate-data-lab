# Week 4 Reflection

**Week:** 4 of 72
**Dates:** 2026-10-12 to 2026-10-18
**Theme:** Formal merge - crop calendar, ERA5, weekly product, re-validation

---

## 1. What did the crop calendar change about the 2022 signal?

The 2022 drought re-validation produced the clearest result of the week:
unweighted stress flagged 31 counties severe; weighted stress flagged 8.

That 23-county gap is not a modelling artifact. It's agronomy. Most Kenyan
counties were in harvest or fallow at peak 2022 stress. Only 8 counties had
maize in the ground and were actively stressed by the drought.

The lesson: "how bad is the drought" and "how bad is the drought for my
maize crop" are different questions. The tool now answers both.

Trans Nzoia, October 2022:
- `stress_avg` = -1.05 (severe under the old index)
- `stress_weighted` = -0.32 (mild under the new index)

The raw drought signal is real. But October is harvest in Trans Nzoia. A
dry October helps, not hurts. The weighted index reflects that.

## 2. Does soil moisture lead NDVI? By how many months?

Yes. By one month.

Lead-lag correlation between `swvl1_mean_anomaly` (0-7 cm soil moisture)
and `ndvi_anomaly`:

| Lag | r | p |
|---|---|---|
| 0 | 0.364 | 1.45e-133 |
| **+1** | **0.461** | **2.13e-220** |
| +2 | 0.372 | 1.83e-136 |

The strongest correlation is at lag +1. Soil dries first, vegetation
follows. This is the physical mechanism of cumulative drought.

Operational consequence: `swvl1_mean_anomaly` becomes the earliest signal
in the weekly product. A county whose soil moisture collapsed this month
is likely to show vegetation stress next month.

## 3. Can I defend the 65/35 weighting in three sentences?

Yes.

First: the 2021 rainfall anomaly was lower than the 2022 rainfall anomaly,
but 2022 crops died and 2021 crops mostly survived. Rainfall alone cannot
explain that. Second: the reason is cumulative soil-moisture depletion.
By 2022, five failed seasons had drained the reserves that carry a crop
through a dry spell. Third: NDVI captures accumulated vegetation stress
across those seasons; rainfall captures single-season failures. Weighting
NDVI at 0.65 and rainfall at 0.35 encodes that.

## 4. What is the most uncertain assumption in the enhanced stress index?

The crop stage weights. They're my estimates, not agronomic measurements.

- Planting = 1.0, grain_fill = 0.7, harvest = 0.3, fallow = 0.0

The direction is right: planting stress is catastrophic, harvest stress
is beneficial. But the magnitude is a guess. A reviewer could reasonably
argue harvest should be 0.1, not 0.3. Or that grain_fill should be 0.8.

The clean way to resolve it would be to calibrate the weights against
KNBS county yield data - find the weights that maximize correlation
between `stress_weighted` and actual yield loss. That's a Week 5+ task.

## 5. Most surprising county?

**Bomet.** Unweighted stress flagged Bomet severe in April 2022;
weighted stress only flagged it in October 2022 - a 183-day shift.

Bomet sits in a rift-valley zone with a long-rains-only season. April
is planting there. But the crop stage at April 2022 was grain_fill (0.7),
not planting. Grain_fill stress reduces yield but doesn't kill the crop,
so 0.7 was enough to keep the observation out of the severe category.

By October, when the short-rains period began, the accumulated stress
crossed the threshold. The county's actual maize damage in 2022 was
severe, but it happened later than the raw drought signal suggested.

## 6. What does next week look like?

Week 5 is the first formal validation week. Three tasks:

1. Load KNBS county-level maize yield (5 counties, 2020-2024).
2. Correlate `stress_weighted` against yield loss year-on-year.
3. If the correlation is weak, investigate. If it's strong, publish.

This is the step that turns the tool from "detects droughts" to
"predicts crop losses." That's the difference between a weather report
and an agricultural early-warning system.

---

## Week 4 deliverables

- `notebooks/03_integration.ipynb` - 55 cells, re-runs clean
- `data/processed/county_monthly_stress_v3.csv` - 4,512 x 27, new master
- `data/processed/county_weekly_stress_2017_2024.csv` - 19,599 x 21
- `data/processed/stress_join_audit.csv` - 3 joins, 0 rows dropped
- `data/processed/SHA256SUMS.txt` - checksums for all master files
- `paper/data_notes.md` - 190-line methods preview
- `paper/figures/fig_stress_timeseries.png`
- `paper/figures/fig_three_way_divergence.png`
- `paper/figures/fig_soil_moisture_lead.png`
- `paper/figures/fig_data_lineage.png`
- D34-D37 in `docs/DECISIONS_LOG.md`

## Week 4 in one sentence

Crop stage weighting turned a 31-county drought signal into an 8-county
crop-damage signal, and soil moisture was shown to lead vegetation by
one month - turning the monitor from descriptive to predictive.
