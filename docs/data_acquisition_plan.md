# Data Acquisition Plan

**Purpose:** Close the yield-validation gap identified in Week 5.
**Owner:** Alex Haro Nyandega
**Date:** 2026-09-30

## The gap

We validated the stress index against 5 counties of KNBS yield data.
Five observations is not enough to draw a conclusion. We need more data
before we can claim (or deny) that the index predicts yield loss.

## What we need

### 1. County-level maize yield for all 47 counties, 2017-2024

- **Current coverage:** 5 counties (Nakuru, Kakamega, Bungoma,
  Trans Nzoia, Uasin Gishu), 2020-2024
- **Target coverage:** 47 counties, 2017-2024
- **Primary source:** Kenya National Bureau of Statistics
- **Request:** Annex 1 of the National Agriculture Production Report
  has this table. Request the full table in CSV format.
- **Fallback:** County agriculture offices, university theses,
  county integrated development plans (CIDPs)

### 2. Seasonal disaggregation (long rains vs short rains)

- **Current:** annual totals only
- **Why it matters:** Kakamega's worst 2022 drought was October
  (short rains). Its 2022 KNBS number covers the long-rains harvest.
  The short-rains failure shows up in 2023.
- **Source:** KNBS seasonal reports, KALRO

### 3. Non-climate covariates

- **Pest years:** Fall armyworm, MLN, locust outbreaks
- **Disease years:** Maize lethal necrosis
- **Policy:** Government subsidy years
- **Source:** KALRO, FAO Kenya country briefs, Plant Protection Services

### 4. Sub-county yield variation

- **Why:** County means smooth out the signal. A drought can hit one
  sub-county and miss another within the same county.
- **Source:** County agriculture offices, ward-level data

## Action plan

| Week | Action | Owner |
|---|---|---|
| 5 | Email KNBS requesting full 47-county table | Alex |
| 5 | Email 3 county agriculture officers | Alex |
| 7 | Follow up with KNBS | Alex |
| 8 | Contact KALRO for pest data | Alex |
| 12 | Compile everything into a single panel | Alex |
| 16 | Re-run validation with 20+ counties | Alex |

## What we will do with it

1. Re-run the county-level correlation with n ≥ 20
2. Disaggregate by season
3. Include non-climate covariates in the model
4. Pre-register the hypothesis before looking at the data
