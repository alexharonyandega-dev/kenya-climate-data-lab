# Data Dictionary

## Quick reference for column names, units, and coverage

### kaggle_kenyan_maize.csv
- `Year` — integer, 1990–2013
- `hg/ha_yield` — hectograms per hectare (divide by 10,000 for t/ha)
- `average_rain_fall_mm_per_year` — mm
- `pesticides_tonnes` — tonnes
- `avg_temp` — °C
- `Area` — "Kenya"

### faostat_maize_yield_kenya.csv
- `Year` — 2010–2024
- `Unit` — "kg/ha" (divide by 1,000 for t/ha)
- `Value` — yield value
- Other columns are metadata (Flag, Note, etc.) — ignore

### hdx_kenya_agriculture.csv
- Long format: `Indicator Name`, `Year`, `Value`
- 37 indicators, 1960–2025

### knbs_county_agriculture.csv
- `County` — e.g., "Nakuru"
- `Year` — 2020–2024
- `Area_Ha` — harvested area in hectares
- `Production_Tons` — production in metric tonnes
- (Derived: yield = Production_Tons / Area_Ha in t/ha)

### zenodo_push_pull.csv
- 99 columns — field trial data
- Key: `farmer`, `region`, `year`, `season`, `trt`, `stem`, `striga`, `yield`
- `trt` values: `p` = push-pull, others = control variants

### era5_temperature_2010_2024.nc
- Dimensions: time × latitude × longitude
- Variable: `t2m` in **Kelvin** (subtract 273.15 for °C)
- Daily mean, 2010–2024, Kenya bbox

### chirps_daily/*/*.tif.gz
- One GeoTIFF per day, 0.05° resolution
- Units: mm/day
- CRS: EPSG:4326
- Coverage: full Africa tile (lon -20 to 55, lat -40 to 40); Kenya inside
- **Important:** nodata sentinel is -9999 but NOT declared in file metadata
- Must mask manually in code: `arr = np.where(arr == -9999, np.nan, arr)`
