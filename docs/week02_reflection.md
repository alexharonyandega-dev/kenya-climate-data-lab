# Week 02 Reflection — 2026-09-28 to 2026-10-04

## 1. Which dataset surprised me most, and why?

The Zenodo push-pull dataset. Its 99 columns already contain a full climate-covariate
engineering pipeline — daily temperature percentiles, dry-spell counts, cumulative
rainfall, soil-moisture accumulations, and log-transformed yields and pest counts.
Whoever prepared that dataset did most of the Week 4 feature engineering for us.
It also surprised me that it covers only 8 counties, none of which include the
Rift Valley highlands that dominate Kenyan maize production. The richest data
covers the smallest geographic footprint.

## 2. Which dataset is the weakest, and why?

Mendeley. Three CSVs totalling 734 rows, split across soil physics, soil chemistry,
and agronomic use efficiency. It is a 4-season field trial on two sites in Embu
and Kibugu. The `Unnamed` columns are artefacts of the original Excel formatting.
It is too small and too site-specific to model against directly. But it is the
only source of soil properties I have, so it stays as a context dataset.

## 3. Can I explain in plain English what CHIRPS is versus KMD rainfall?

CHIRPS is a satellite-based rainfall estimate. The Climate Hazards Center in
California blends three signals: thermal infrared satellite cold-cloud duration,
passive microwave satellite estimates, and actual rain-gauge station observations
from national meteorological services. It produces a 0.05-degree daily grid from
1981 to the present. KMD's ENACTS product uses the same kind of input data but is
produced by the Kenya Meteorological Department and covers Kenya specifically.
The two should correlate at r > 0.85 for most of Kenya. KMD's server is currently
broken, so I am using CHIRPS as the primary rainfall source.

## 4. What is one column I do not yet understand?

`zenodo_pushpull.avgsmoistbefNdayswthobs`. It appears to measure the average soil
moisture over some window before a "wet day threshold" event. The column is
integer-typed (0-10) but I do not know if the unit is volumetric water content
in percent, a scaled index, or a count. The related column `avgsmoistbef` is
float-typed (0-0.4). I will need to read the Zenodo paper's methods section in
Week 3 to understand exactly what this measures.

## 5. If I had to explain my project in one paragraph right now:

Maize is Kenya's most important food crop, and its yield swings year to year
because of rainfall and temperature variability. National agencies report maize
production at county level, but there is no open predictive model that tells a
county government what yield to expect given the climate of a given season. I am
building one. Over 72 weeks, I am combining satellite rainfall (CHIRPS), reanalysis
temperature (ERA5-Land), national statistics (FAOSTAT, KNBS), and two experimental
field-trial datasets (Zenodo push-pull, Mendeley) into a county-level maize yield
prediction pipeline. Everything is public: the data, the code, the notebooks, and
the weekly write-ups. The goal is a tool that Kenyan policymakers, extension
officers, and farmers can actually use — and a methodology that other East African
researchers can fork for their own crops and counties.
