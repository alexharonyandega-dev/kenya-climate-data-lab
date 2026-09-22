# Week 01 Reflection - 2026-09-21 to 2026-09-27

## 1. Why maize yield over air quality or rainfall anomalies?

Maize is Kenya's staple food crop and the primary source of calories for
most households, so any improvement in forecasting its yield has direct
food-security implications. Unlike air quality or rainfall anomalies,
maize yield is a measurable outcome that county governments can act on
through input subsidies, extension services, and drought-response
planning. Kenya's Vision 2030 explicitly targets agricultural
productivity as a pillar of economic growth, which gives the project a
policy-aligned purpose. I also chose maize because the data landscape is
genuinely rich - FAOSTAT, KNBS, Kaggle, and multiple research datasets
all publish maize-related variables, which means the model can be
validated against independent sources. On a personal level, I grew up
around smallholder farming, and I want the work I do to have a tangible
impact on the communities I come from.

## 2. Which data source was hardest to obtain? How did you solve it?

KMD rainfall was by far the hardest. Their public ENACTS server runs an
old IRI Data Library build that is partially broken: the DODS endpoints
return 404, the "Data Selection" tab returns 404, and any NetCDF request
- even for a single year and a single county's bounding box - returns
the error "too large for netcdf file". The tabular and CSV endpoints
don't exist on this version. I tried roughly a dozen URL variations,
browsed the Ingrid catalog tree in a browser, and even parsed the error
pages the server returned to try to reconstruct the correct path. None
of it worked.

I solved it by documenting the failure honestly in
`data/metadata/sources.md` and substituting CHIRPS 2.0 daily
precipitation, which is functionally equivalent for this analysis: same
0.05-degree resolution, overlapping time period (2010-2024), and it's
widely used in published Kenyan maize-climate research. I also sent an
email to data@meteo.go.ke in case they respond with the actual KMD
data, but I did not let the pipeline block on it. The lesson was that
data engineering is sometimes about accepting what is reachable and
documenting what is not.

## 3. What part of the plan felt intimidating this week? What is one small action that makes it less scary?

The most intimidating part was the sheer number of datasets and the
variety of formats they arrive in - CSV, Excel, RData, NetCDF, GeoTIFF,
PDF tables, Zarr. Each one demanded a different tool, and every time I
thought I was done with one, the next one introduced a new technical
obstacle. The KMD dead-end was especially discouraging because it was
the dataset the plan described as the primary rainfall source.

One small action that makes it less scary: writing down every failure
in `sources.md` as it happens, with the exact URL, error message, and
what I tried instead. That turns a frustrating dead-end into documented
evidence of work. When I look back at the sources file now, I see a
record of problem-solving rather than a list of things that didn't work.

## 4. Did I actually understand what each dataset measures, or did I just download files?

Before this week, I would have said I understood them. After building
the pipeline, I can articulate each one precisely:

- **Kaggle Kenyan Maize Dataset** - a curated Kenya-only CSV of annual
  maize yield (1990-2013) alongside rainfall, pesticide use, and average
  temperature. It's a good cross-validation source but its time coverage
  ends in 2013.
- **FAOSTAT Maize Yield** - the official national maize yield series
  reported by Kenya to the UN, in kg/ha. This will be the ground-truth
  target for the earliest modelling work.
- **CHIRPS Precipitation** - satellite-based daily rainfall estimates at
  0.05-degree resolution. This is the primary spatial rainfall input to
  the model and will be aggregated to county-level monthly totals.
- **HDX Kenya Agriculture** - 37 World Bank agriculture indicators for
  Kenya from 1960 to 2025, including cereal yield, fertilizer
  consumption, and agricultural land. These are national-level
  covariates rather than spatial ones.
- **Mendeley 5-season maize experiment** - soil physical, chemical, and
  agronomic efficiency data from a 4-season field trial in Kibugu and
  Machang'a. It's plot-level rather than county-level, so it will
  inform feature engineering rather than direct modelling.
- **Zenodo push-pull farming dataset** - farmer-level maize yield,
  stemborer, and striga counts across Western Kenya from 2005 to 2016,
  with 90 climate covariate columns already merged. This is the richest
  dataset for county-level feature discovery.
- **KNBS county maize data** - county-level maize area (ha) and
  production (tons) from the 2025 National Agriculture Production
  Report. Divided by area it gives an independent county-level yield
  series from 2020 to 2024.
- **ERA5-Land temperature** - daily mean 2-metre air temperature at 0.1-
  degree resolution, clipped to Kenya. This is the primary temperature
  input and will be averaged over each county's grid cells.
- **KMD rainfall (not obtained)** - would have been a 1981-2024 daily
  station-satellite blended rainfall product at 0.05 degrees. Because
  the server was inaccessible, CHIRPS serves as the substitute.

I genuinely understand what each measures and where it fits. The next
step is to load each one in a notebook and verify with my own eyes that
the shape, units, and time coverage match what the metadata claims.
