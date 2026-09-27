# Kenya Climate Data Lab

**A county-level drought and vegetation stress monitor for all 47 Kenyan counties.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Build: 72 weeks](https://img.shields.io/badge/build-72%20weeks-brightgreen.svg)](https://kenyaclimatelab.substack.com)

[![Substack](https://img.shields.io/badge/Substack-Kenya%20Climate%20Lab-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://kenyaclimatelab.substack.com)
[![X](https://img.shields.io/badge/X-@KenyaClimateLab-000000?style=for-the-badge&logo=x)](https://x.com/KenyaClimateLab)
[![Email](https://img.shields.io/badge/Email-alexharonyandega@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:alexharonyandega@gmail.com)

---

## What this is

Kenya Climate Data Lab is a 72-week open-source project building a **weekly county-level drought and vegetation stress monitor** for all 47 counties in Kenya.

The tool combines CHIRPS satellite rainfall and Sentinel-2 vegetation health (NDVI) into a composite stress index, refreshed monthly. It answers one question for every county: *how unusual is this month compared to the historical norm for this time of year?*

## The gap

Existing Kenya monitoring tools each miss something:

| Tool | Updates | Granularity |
|---|---|---|
| FAO Agricultural Stress Index | Every 10 days | Sub-county, not administrative |
| FEWS NET Kenya | Monthly | Livelihood zone |
| GEOGLAM Crop Monitor | Monthly | Crop zone |
| KNBS National Agriculture Production Report | Annual, post-harvest | County |

**The tools that update often don't give county yields. The tool that gives county data comes out once a year — too late to help.**

This project fills that gap: fast, county-level, weekly updates for all 47 counties.

## Validation — the 2022 Horn of Africa drought

The monitor's first real test was the 2021–2022 Horn of Africa drought — the worst in 40 years, with five consecutive failed rainy seasons.

The tool detected it **without any calibration** — purely by comparing each county-month to its own historical average.

![Kenya county stress index October 2019-2024](paper/figures/fig_stress_october_series.png)

The 2022 panel shows severe or moderate stress in every county. NDVI values fell to −1.35 z-scores in December 2022, while rainfall anomaly peaked lower at −0.89.

**Key design implication:** NDVI captures accumulated drought damage; rainfall captures single-season failures. The composite index weights NDVI at 65% and rainfall at 35%.


## How it works

The pipeline runs in two tiers:

**Tier 1 — weekly rainfall** (fast update)
CHIRPS daily files -> weekly aggregates -> per-county weekly anomaly

**Tier 2 — monthly composite** (richer signal)
Rainfall (aggregated to monthly) + NDVI -> per-county monthly anomaly -> composite stress index

Full pipeline documentation: [docs/architecture.md](docs/architecture.md).

## Data sources

| Dataset | Source | Coverage | Role |
|---|---|---|---|
| CHIRPS rainfall | data.chc.ucsb.edu | 2010-2024, 47 counties | Primary rainfall signal |
| Sentinel-2 NDVI | Google Earth Engine | 2017-2024, 47 counties | Primary vegetation signal |
| ERA5-Land climate | Earth Data Hub | 1990-2024, 9 variables | Temperature, soil moisture |
| iSDAsoil | iSDA Africa | 8 properties, 20M px/county | Soil covariates |
| FAOSTAT yield | fao.org/faostat | 1961-2024, national | Validation |
| KNBS county maize | knbs.or.ke | 2020-2024, county | Validation |
| Kenya boundaries | geoBoundaries | 47 counties, GeoJSON | Spatial reference |

See `data/metadata/sources.md` for full details.

## Repository structure

    kenya-climate-data-lab/
    ├── data/
    │   ├── raw/                   Original downloads (never edited)
    │   ├── processed/             Cleaned and merged tables
    │   ├── external/              Kenya county boundaries (GeoJSON)
    │   └── metadata/              sources.md, data_dictionary.md, crop_calendar
    ├── notebooks/                 Exploration and diagnostics
    ├── scripts/                   Reproducible data pipelines
    │   └── gee/                   Google Earth Engine scripts
    ├── paper/figures/             Figures for posts and papers
    ├── dashboard/                 (planned) Public dashboard
    ├── app/                       (planned) Interactive tool
    ├── docs/
    │   ├── advisory/              External feedback notes
    │   ├── architecture.md        Pipeline documentation
    │   ├── why-maize.md           Problem statement
    │   └── weekNN_reflection.md   Weekly reflections
    ├── metrics/                   Weekly log + screenshots
    └── README.md

## Current status

- **Phase:** Foundation (Week 3 of 72)
- **Stress monitor:** Working prototype, monthly resolution
- **Coverage:** All 47 Kenyan counties, 2017-2024
- **Validated against:** 2022 Horn of Africa drought (detected without calibration)
- **Next milestone:** Weekly update resolution + public dashboard

## Development

    conda create -n kenya-climate python=3.11 -y
    conda activate kenya-climate
    pip install -r requirements.txt

## Contributing

Contributions welcome from anyone working in Kenyan agriculture, climate research, or data science.

- **Data** — county-level maize records, ground-truth rainfall, yield trial data — open an issue or email
- **Methodology** — if you see a flaw in the pipeline, open an issue with details
- **Code** — pull requests welcome, please open an issue first to discuss
- **Feedback** — reply to any post on the [Substack](https://kenyaclimatelab.substack.com)

## License

- **Code:** MIT
- **Data:** CC-BY-4.0 (where permitted by source licenses)

## Contact

**Alex Haro Nyandega** — alexharonyandega@gmail.com — Nairobi, Kenya

[GitHub](https://github.com/alexharonyandega-dev) · [X](https://x.com/KenyaClimateLab) · [Substack](https://kenyaclimatelab.substack.com)
