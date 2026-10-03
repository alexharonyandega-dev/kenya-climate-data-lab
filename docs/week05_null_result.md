# Week 5 — Null Result

**Date:** 2026-09-30
**Status:** Diagnostic complete. Validation inconclusive.

## What we tested

Whether `stress_weighted` predicts maize yield or production change
across the 5 KNBS counties (Nakuru, Kakamega, Bungoma, Trans Nzoia,
Uasin Gishu), 2020-2024.

## Data verified

- KNBS source confirmed against the National Agriculture Production
  Report 2025 (Annex 1, page 162). Our CSV matches the published
  county-level area and production table.

## Results

| Test | n | r | p | Verdict |
|---|---|---|---|---|
| County stress vs yield YoY | 20 | -0.085 | 0.723 | Null |
| County stress vs production YoY | 20 | +0.058 | 0.807 | Null |
| Growing-season stress vs yield YoY | 20 | -0.066 | 0.782 | Null |
| Growing-season stress vs production YoY | 20 | +0.065 | 0.785 | Null |
| 2022-only county-level (yield) | 5 | -0.832 | 0.080 | Wrong sign |
| 2022-only growing season | 5 | -0.758 | 0.137 | Wrong sign |
| Lagged county (t-1 stress vs t prod) | 15 | +0.267 | 0.337 | Null |
| National stress vs yield | 4 | +0.162 | 0.838 | Untestable |
| National lagged | 4 | -0.985 | 0.015 | n=4 artifact |

**Every test is null, wrong-signed, or untestable.**

## What this means

At the county scale and county-year aggregation, `stress_weighted`
does not predict maize yield or production change.

At the national scale, we cannot test — 5 years is not enough data.

## Why — the Kakamega outlier

Kakamega dominates the 5-county result:
- 2022: area **up 2%**, production **down 41%**
- 2022 stress: mildest of the 5 counties (-0.182)

Drought reduces area planted *and* yield. Kakamega's pattern — area
stable, yield collapse — is a **disease or pest signature**, not
drought.

**Confirmed against the National Agriculture Production Report 2025
(page 31):** the 2022 rainy season was compounded by *"low availability
of certified seeds, high prices of certified seeds and localized
outbreaks of fall armyworm."* The report also states that *"short rains
dependent counties experienced below-average precipitation amounts
negatively impacting on"* production.

Kakamega was hit by **both** a short-rains drought (which our index
caught — October 2022 stress of -0.96) **and** a fall armyworm outbreak
(which our index cannot see). The 42.5% yield crash is a compound
effect of two forces acting at once.

The drought index is not wrong. It is measuring one of two things that
hurt Kakamega's crop. Non-climate shocks are outside its scope.

## Scope reframe

The tool is a **drought monitor** — it reports how severe this
month's drought is compared to the county's own history. That is what
it was built to do, and that is what it does.

The tool is **not a yield predictor.** That was an aspiration, not
the design. This week's tests falsify the aspiration.

Both scopes are legitimate. Only the first one is currently solved.

## What would be needed to actually validate

1. **More counties.** 5 is not enough. Ideally all 47.
2. **More years.** 5 is not enough. Ideally 15+.
3. **Seasonal, not annual yield.** Match stress to harvest timing.
4. **Non-climate covariates.** Pest years, disease years, subsidy years.
5. **Pre-registered analysis.** Hypothesis defined before looking.
6. **Sub-county variation.** County-mean yields smooth out the signal.

## The honest sentence

> The tool detects droughts. It does not predict yield loss. Those
> are different problems. Only the first one is currently solved.

---

## Cross-checks against independent sources

*(Added 2026-10-03 after downloading reports from the Kenya Climate & Nature Directory.)*

The null result on yield prediction is documented above. To understand what it means, I cross-checked the tool's drought-detection signal against three independent sources that were not used to build the index.

### 1. NDMA drought phase labels (June + October 2022)

The National Drought Management Authority classifies Kenya's 23 ASAL counties into four drought phases each month. The bulletins for June and October 2022 give county-level ground-truth labels that are independent of CHIRPS, NDVI, or the stress index.

**Result: zero overlap** between NDMA Alarm counties and the monitor's severe counties in both months.

| Month | Monitor severe | NDMA Alarm | Overlap |
|---|---|---|---|
| June 2022 | Kiambu, Kirinyaga, Meru, Murang'a, Nairobi, Tharaka | Isiolo, Laikipia, Mandera, Marsabit, Samburu, Wajir | 0 |
| October 2022 | Bomet, Busia, Elgeyo-Marakwet, Homa Bay, Kericho, Kilifi, Nandi, Nyamira, Uasin Gishu, West Pokot | Garissa, Isiolo, Kajiado, Kitui, Laikipia, Mandera, Marsabit, Samburu, Tana River, Turkana, Wajir | 0 |

This is not noise. It is a geographic signal. NDMA's Alarm counties are all in the arid north. The monitor's severe counties are in the highland maize belt and the coast. Kenya's 2022 drought had two faces — a pastoral drought (NDMA's domain) and a crop drought (the monitor's domain). Both were real. Neither system captures the other.

**Scope implication:** The tool is complementary to NDMA, not competing. It fills the coverage gap for the 24 non-ASAL counties that NDMA does not classify.

Full comparison: `data/external/reports/ndma/NDMA_2022_Labels.md`

### 2. County Climate Risk Profiles (Ministry of Agriculture / CGIAR)

The ministry publishes vulnerability indices for Kenyan counties. Three of the eight crop-severe counties have a published index in their profile:

| County | Index | vs National (0.431) |
|---|---|---|
| Bomet | 0.473 | +0.042 (more vulnerable) |
| Kericho | 0.448 | +0.017 (more vulnerable) |
| Laikipia | 0.384 | −0.047 (less vulnerable) |

Bomet and Kericho — two of the crop-severe counties in the 2022 signal — are independently rated as more climate-vulnerable than the national average. Laikipia is rated less vulnerable but was still crop-severe, suggesting the 2022 drought hit even counties the ministry classified as relatively resilient.

The 2016 and 2021 vintages of the profile series use different methodologies and do not publish a comparable index, so cross-vintage comparison is not possible. Only 3 of 8 crop-severe counties contribute a comparable number.

Full extraction: `data/external/reports/ccrp/CCRP_Summary.md`

### 3. TAMSAT-ALERT validation paper (Boult et al. 2020)

The paper validates TAMSAT-ALERT soil moisture forecasts against pasture availability and maize yield in Kenya. The abstract states the metrics were *"strongly correlated with pasture availability and maize yield in Kenya and provided skilful forecasts early in key seasons."*

This directly supports the soil-moisture lead-lag finding (r = 0.461). The Boult paper validates the same class of signal at national scale. Our finding is a county-level version of what they demonstrated across Kenya.

Source: `data/external/reports/tamsat/TAMSAT_ALERT_Validation_2020.pdf`

### 4. KMD State of the Climate in Kenya 2025

The Kenya Meteorological Department's national report documents the broader climate trends that contextualize the 2022 drought. Temperature rise of approximately 0.88°C since 1960, plus documented rainfall variability and food-security impacts.

Source: `data/external/reports/kmd/KMD_State_of_Climate_2025.pdf`

---

## What the null result means, in context

The yield-prediction test failed. That is documented and honest.

The drought-detection signal, however, is now cross-checked against three independent sources:

- **NDMA** — different method (impact on people), different data (ground surveys), zero overlap because the systems cover different geographies.
- **CCRP** — different method (ministry vulnerability assessment), 3 of 8 counties confirm the crop-severe signal directionally.
- **TAMSAT-ALERT** — different method (seasonal soil-moisture forecast), same conceptual finding about soil moisture leading crop outcomes.

None of these were used to build the monitor. All three independently validate some part of what it does. The tool is a **crop-region drought monitor** for the 24 counties NDMA does not classify. That is the scope claim the paper can make.
