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

Hypothesis: MLN (Maize Lethal Necrosis) or fall armyworm in western
Kenya in 2022. Not yet verified against public reports.

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
