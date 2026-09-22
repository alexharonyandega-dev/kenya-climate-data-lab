<p align="center">
  <img src="https://raw.githubusercontent.com/alexharonyandega-dev/kenya-climate-data-lab/main/assets/launch-graphic.png" alt="Kenya Climate Data Lab Launch Graphic" width="100%">
</p>

<h1 align="center">Kenya Climate Data Lab</h1>

<p align="center">
  An open-source machine-learning pipeline that predicts maize yield (t/ha) for Kenyan counties from historical rainfall and temperature data.
</p>

<p align="center">
  <a href="https://x.com/KenyaClimateLab">
    <img src="https://img.shields.io/badge/X-@KenyaClimateLab-000000?style=for-the-badge&logo=x" alt="Follow on X">
  </a>
  <a href="https://www.instagram.com/kenyaclimatedatalab/">
    <img src="https://img.shields.io/badge/Instagram-@kenyaclimatedatalab-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Follow on Instagram">
  </a>
</p>

---
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
- `assets` — project graphics
## Data sources
See [`data/metadata/sources.md`](data/metadata/sources.md) for full details.

| Dataset | Source | Coverage | Status |
|---|---|---|---|
| KMD rainfall | kmddl.meteo.go.ke | 1981-2024 | not obtained - substituted with CHIRPS |
| CHIRPS precip | data.chc.ucsb.edu | 2010-2024 | done |
| ERA5-Land temp | cds.climate.copernicus.eu | 2010-2024 | done |
| FAOSTAT yield | fao.org/faostat | 2010-2024 | done |
| KNBS county maize | knbs.or.ke | 2020-2024 | done |
| Kaggle maize | kaggle.com/datasets/yvvonjemmy/kenyan-maize-dataset | 1990-2013 | done |
| HDX indicators | data.humdata.org | 1960-2025 | done |
| Mendeley 5-season | data.mendeley.com | 4 seasons | done |
| Zenodo push-pull | zenodo.org | 2005-2016 | done |
## Setup

    conda create -n kenya-climate python=3.11 -y
    conda activate kenya-climate
    pip install -r requirements.txt

## Contact
Alex Haro Nyandega - alexharonyandega@gmail.com - [@alexharonyandega-dev](https://github.com/alexharonyandega-dev)
