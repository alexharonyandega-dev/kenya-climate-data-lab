# Datasets — current state (2026-09-26)

| # | Dataset | Status | Range / Coverage | Notes |
|---|---|---|---|---|
| 1 | Kaggle Maize | ✅ fixed | 1990–2013 | Original data, no upgrade possible |
| 2 | FAOSTAT Yield | ✅ maxed | 1961–2024 (64 rows) | Extended from 15 to 64 years |
| 3 | CHIRPS Rainfall | ⚠️ partial | 2010–2024 (5,448 files) | Could extend to 1981 |
| 4 | HDX Indicators | ✅ complete | 1960–2025 (1,709 rows) | Whole World Bank file |
| 5 | Mendeley | ✅ complete | 4 seasons | All 3 sheets |
| 6 | Zenodo Push-Pull | ✅ complete | 2005–2016 | Both files |
| 7 | KNBS County | ✅ sufficient | 2020–2024 (25 rows) | One report |
| 8 | ERA5-Land | ✅ maxed | 1990–2024, 9 variables | Extended from 1 var, 15 yrs |
| 9 | KMD Rainfall | ⚠️ substitute | CHIRPS used instead | Server broken, documented |
| 10 | iSDAsoil | ✅ maxed | 20M px/county, 2 depths, ±std | Raster COG, 8 properties |
| 11 | Kenya boundaries | ✅ | 47 counties, geoBoundaries ADM1 | External file |

## Maxed in this session
- FAOSTAT: 15 → 64 years
- ERA5: 1 variable → 9 variables, 15 years → 35 years
- iSDAsoil: 1 centroid → 20M pixels/county, added 20–50 cm depth + std dev

## Remaining gap
CHIRPS extension from 2010 to 1990 would increase Kaggle-Chirps overlap from 4 to 24 years.
