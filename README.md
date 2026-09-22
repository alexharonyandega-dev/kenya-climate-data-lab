# Kenya Climate Data Lab

An open-source machine-learning pipeline that predicts maize yield (t/ha) for Kenyan counties from historical rainfall and temperature data.

## Status
Week 1 of 72 — Foundation phase. Repository bootstrapped, environment configured, raw datasets downloaded.

## Structure
- `data/raw` — original downloads (never edited)
- `data/processed` — cleaned/merged tables
- `data/metadata` — dataset documentation (`sources.md`)
- `notebooks` — exploration, cleaning, features, modelling
- `dashboard` — Tableau Public workbook
- `app` — Streamlit web application
- `paper` — draft, figures, references
- `workshops` — Data Science for Youth curriculum
- `metrics` — tracker + monthly reports

## Data sources
See [`data/metadata/sources.md`](data/metadata/sources.md) for full details.

| Dataset | Source | Coverage | Status |
|---|---|---|---|
| KMD rainfall | kmddl.meteo.go.ke | 1981-2024 | not obtained - substituted with CHIRPS |
| CHIRPS precip | data.chc.ucsb.edu | 2010-2024 | ok |
| ERA5-Land temp | cds.climate.copernicus.eu | 2010-2024 | ok |
| FAOSTAT yield | fao.org/faostat | 2010-2024 | ok |
| KNBS county maize | knbs.or.ke | 2020-2024 | ok |
| Kaggle maize | kaggle.com/datasets/yvvonjemmy/kenyan-maize-dataset | 1990-2013 | ok |
| HDX indicators | data.humdata.org | 1960-2025 | ok |
| Mendeley 5-season | data.mendeley.com | 4 seasons | ok |
| Zenodo push-pull | zenodo.org | 2005-2016 | ok |

## Setup

    conda create -n kenya-climate python=3.11 -y
    conda activate kenya-climate
    pip install -r requirements.txt

## Contact
Alex Haro Nyandega - alexharonyandega@gmail.com - @alexharonyandega-dev
