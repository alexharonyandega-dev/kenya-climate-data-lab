# Data Sources

All datasets used in the Kenya Climate Data Lab project. Downloaded between September 21–22, 2026.

## 1. Kaggle — Kenyan Maize Dataset

- **File:** `data/raw/kaggle_kenyan_maize.csv`
- **Source:** https://www.kaggle.com/datasets/yvvonjemmy/kenyan-maize-dataset
- **Coverage:** Kenya, 1990–2013 (4,121 rows)
- **Fields:** Year, Item, hg/ha_yield, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area
- **Notes:** Yield in hg/ha — divide by 10,000 for t/ha.

## 2. FAOSTAT — Maize Yield for Kenya

- **File:** `data/raw/faostat_maize_yield_kenya.csv`
- **Source:** https://www.fao.org/faostat/en/#data/QCL
- **Coverage:** Kenya, Maize, Yield, 2010–2024 (15 rows)
- **Fields:** Domain, Area, Element, Item, Year, Unit, Value, Flag, etc.
- **Notes:** Unit is **kg/ha** (not hg/ha as the original plan stated) — divide by 1,000 for t/ha.

## 3. CHIRPS 2.0 — Precipitation

- **Files:** `data/raw/chirps_daily/YYYY/chirps-v2.0.YYYY.MM.DD.tif.gz`
- **Source:** https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_daily/tifs/p05/
- **Coverage:** Africa daily, 2010–2024 (5,448 files, 4.3 GB)
- **Notes:** December 2021 daily files missing from archive; monthly aggregate (`2021_monthly/chirps-v2.0.2021.12.monthly.tif.gz`) downloaded as fallback. Excluded from git via `.gitignore`.

## 4. HDX / World Bank — Kenya Agriculture Indicators

- **File:** `data/raw/hdx_kenya_agriculture.csv`
- **Source:** https://data.humdata.org/dataset/world-bank-agriculture-and-rural-development-indicators-for-kenya
- **Coverage:** Kenya, 1960–2025 (1,709 rows, 37 indicators)
- **Fields:** Country Name, Country ISO3, Year, Indicator Name, Indicator Code, Value
- **Notes:** Includes `Cereal yield (kg per hectare)`, `Average precipitation in depth (mm per year)`, `Fertilizer consumption`, and 34 other agriculture indicators.

## 5. Mendeley — Kenya Maize & Soil Dataset

- **Files:**
  - `data/raw/mendeley_maize_experiment.csv` (384 rows, 12 cols — agronomic use efficiency)
  - `data/raw/mendeley_soil_physical.csv` (78 rows, 16 cols)
  - `data/raw/mendeley_soil_chemical.csv` (272 rows, 13 cols)
- **Source:** Mutuku, Eunice (2020). "Raw data set". Mendeley Data, V1. doi: 10.17632/6mrwj2p3cb.1
- **Coverage:** Sub-humid (Kibugu) and semi-arid (Machang'a) sites in Kenya; 4 seasons of conservation agriculture trial.
- **Notes:** Original file was Excel with 3 sheets; converted to 3 CSVs.

## 6. Zenodo — Push-Pull Farming System

- **Files:**
  - `data/raw/zenodo_push_pull.csv` (4,932 rows, 99 cols)
  - `data/raw/zenodo_west_kenya_climate.csv` (50,349 rows, 61 cols)
- **Source:** Clough, Y., Lutter, R., et al. (2026). "Data and code for 'Push-pull farming system helps insure smallholder maize production under climate change'". Zenodo. doi: 10.5281/zenodo.21131592
- **Coverage:** Western Kenya, 2005–2016, farmer-level field trial data
- **Fields:** farmer, region, year, season, trt (treatment), stem, striga, yield + 90 climate covariate columns
- **Notes:** Original files were RData; converted to CSV using R.

## 7. KNBS — County Maize Production

- **File:** `data/raw/knbs_county_agriculture.csv`
- **Source:** Kenya National Bureau of Statistics, National Agriculture Production Report 2025, Annex 1, pp. 162.
  - PDF: `data/metadata/National-Agriculture-Production-Report-2025.pdf`
  - PDF available from: https://www.knbs.or.ke
- **Coverage:** 5 target counties, 2020–2024 (25 rows)
- **Fields:** County, Year, Area_Ha, Production_Tons
- **Notes:** Extracted from PDF Annex 1 using pypdfium2. Only rows for Nakuru, Kakamega, Bungoma, Trans Nzoia, Uasin Gishu retained.

## 8. ERA5-Land — Temperature

- **File:** `data/raw/era5_temperature_2010_2024.nc`
- **Source:** Earth Data Hub — ERA5-Land Daily UTC v1
  - URL: https://data.earthdatahub.destine.eu/era5/era5-land-daily-utc-v1.zarr
  - Registration: https://earthdatahub.destine.eu
- **Coverage:** Kenya bbox (Lat −4.7 to 5.0, Lon 33.9 to 41.9), daily mean 2m temperature, 2010–2024
- **Dimensions:** 5,479 days × 97 latitude × 80 longitude
- **Units:** Kelvin (subtract 273.15 for °C)
- **Notes:** Served as Zarr store, sliced and saved as NetCDF with zlib compression level 9 → 40.6 MB.

## 9. KMD — Rainfall (Not obtained)

- **File:** `data/raw/kmd_rainfall_1981_2024.csv` (not obtained)
- **Source:** Kenya Meteorological Department, ENACTS daily rainfall
  - Dataset: `SOURCES/.KMD/.Kenya_v03r05/.ALL/.Rainfall/.daily/.precip/`
  - Portal: https://kmddl.meteo.go.ke
  - Email: data@meteo.go.ke
- **Requested:** Daily rainfall for Nakuru, Kakamega, Bungoma, Trans Nzoia, Uasin Gishu, 1981–2024
- **Status (2026-09-23):** Attempted exhaustively over two days. All web interface tabs return 404 (Data Selection, Data Files, Data Tables). Direct `data.nc`, `dods`, and `data.tsv` endpoints on both v02 and v03r05 datasets return 404. Server runs Ingrid 0.9 with unfixable bugs. Email sent to data@meteo.go.ke; no response. **KMD ENACTS is not retrievable via any known method.**
- **Substitute:** CHIRPS 2.0 daily precipitation (see entry 3) is used as the primary rainfall dataset. Same spatial resolution (0.05°) and overlapping period (2010–2024). CHIRPS is the standard alternative in Kenyan climate-maize research.

---

*Last updated: 2026-09-22*

## 10. iSDAsoil — Soil Properties

- **File:** `data/raw/isda_soil_properties_by_county.csv`
- **Source:** iSDA (Innovative Solutions for Decision Agriculture)
  - API: https://api.isda-africa.com/isdasoil/v2/soilproperty
  - Docs: https://isda-africa.com/api/registration/
  - Login: email/password (environment variables `ISDA_USERNAME` / `ISDA_PASSWORD`)
- **Coverage:** 5 target counties (Nakuru, Kakamega, Bungoma, Trans Nzoia, Uasin Gishu)
- **Variables:** 14 properties at 0–20 cm depth:
  - Chemical: nitrogen_total (g/kg), phosphorous_extractable (ppm),
    potassium_extractable (ppm), carbon_organic (g/kg), ph,
    cation_exchange_capacity (cmol/kg), sulphur_extractable (ppm),
    magnesium_extractable (ppm), calcium_extractable (ppm),
    zinc_extractable (ppm)
  - Physical: bulk_density (g/cm3), clay_content (%), sand_content (%),
    silt_content (%)
- **Notes:** Queried at county centroid (not area-averaged) because the API
  is point-based. For a fully representative county value, a raster mask
  over the county polygon would be needed. This is a known limitation.

