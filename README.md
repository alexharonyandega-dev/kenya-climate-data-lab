# Kenya Climate Data Lab

**An open-source machine learning project predicting maize yield across all 47 Kenyan counties using historical rainfall, temperature, and agricultural data.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Build: 72 weeks](https://img.shields.io/badge/build-72%20weeks-brightgreen.svg)](https://kenyaclimatelab.substack.com)

---

## What this is

Kenya Climate Data Lab is a 72-week open-source project to predict maize yield at the county level using CHIRPS rainfall, ERA5-Land temperature, FAOSTAT and KNBS production records, plus experimental trial data from Zenodo and Mendeley.

Everything is public: datasets, notebooks, models, and weekly write-ups. No proprietary data, no closed methodology.

**Read the launch post:** [Why I'm Spending 72 Weeks Modelling Maize Yield in Kenya](https://kenyaclimatelab.substack.com)
**Follow on X:** [@KenyaClimateLab](https://x.com/KenyaClimateLab)

---

## Connect with the project

<p align="left">
  <a href="https://kenyaclimatelab.substack.com">
    <img src="https://img.shields.io/badge/Substack-Kenya%20Climate%20Lab-FF6719?style=for-the-badge&logo=substack&logoColor=white" alt="Substack">
  </a>
  <a href="https://x.com/KenyaClimateLab">
    <img src="https://img.shields.io/badge/X-@KenyaClimateLab-000000?style=for-the-badge&logo=x" alt="Follow on X">
  </a>
  <a href="mailto:alexharonyandega@gmail.com">
    <img src="https://img.shields.io/badge/Email-alexharonyandega@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
  </a>
</p>


---

## Why maize

Maize is the staple crop for millions of Kenyan families. Climate variability is making its production increasingly unpredictable — and county-level agricultural decisions need county-level models, not national averages.

## Why open source

Almost all climate-yield research in East Africa is done by foreign research institutions using African data. The methods are published in journals most Kenyans cannot access, the code is not shared, and the datasets are not released. This project is the opposite of that. Everything is public.

## Why 72 weeks

Seventy-two weeks is long enough to do real work and short enough to stay accountable. The project is split into five phases:

| Phase | Weeks | Focus |
|---|---|---|
| **1. Foundation** | 1-12 | Repository, data acquisition, first models, dashboards |
| **2. Technical depth** | 13-28 | Refined models, research paper, preprint |
| **3. Leadership** | 29-48 | Data literacy workshops, competitions |
| **4. Professional proof** | 49-60 | Apprenticeship, industry engagement |
| **5. Packaging** | 61-72 | Final report, portfolio, applications |

---

## Data sources

| Dataset | Source | Coverage |
|---|---|---|
| KMD rainfall | kmddl.meteo.go.ke | 1981-2024 (inaccessible; see sources.md) |
| CHIRPS precip | data.chc.ucsb.edu | 2010-2024 |
| ERA5-Land temp | cds.climate.copernicus.eu | 2010-2024 |
| FAOSTAT yield | fao.org/faostat | national |
| KNBS county | knbs.or.ke | county |
| Kaggle maize | kaggle.com/datasets/yvvonjemmy/kenyan-maize-dataset | curated |
| HDX indicators | data.humdata.org | 1960-2025 |
| Mendeley 5-season | data.mendeley.com | 4 seasons |
| Zenodo push-pull | zenodo.org | 2005-2016 |

See `data/metadata/sources.md` for full details.

---

## Repository structure

    kenya-climate-data-lab/
    ├── data/
    │   ├── raw/            # Original downloads (never edited)
    │   ├── processed/      # Cleaned and merged tables
    │   └── metadata/       # sources.md + data_dictionary.md
    ├── notebooks/          # Exploration, cleaning, features, modelling
    ├── dashboard/          # Tableau Public workbook
    ├── app/                # Streamlit web application
    ├── paper/              # Draft, figures, references
    ├── workshops/          # Data Science for Youth curriculum
    ├── metrics/            # Tracker + monthly reports
    ├── docs/               # Why-maize, additional docs
    ├── blog/               # Weekly reflections
    └── README.md

---

## Current status

- **Phase:** Foundation (Week 2 of 72)
- **Repository:** Bootstrapped with structured notebook and figures
- **Environment:** Python 3.11 with all Week 2 dependencies pinned
- **Data:** 9 CSV datasets + 1 NetCDF + 5,449 CHIRPS GeoTIFFs, all loaded and profiled
- **First processed artifact:** `data/processed/chirps_kenya_daily_2021_2022.csv` — Kenya daily rainfall time series (730 rows, Dec 2021 gap documented)
- **Next milestone:** Week 3 — county-level CHIRPS aggregation, ERA5 county means, master table build

See the full weekly log in the [Substack](https://kenyaclimatelab.substack.com).

---

## How to contribute

This project welcomes contributions from anyone working in Kenyan agriculture, climate research, or data science.

- **Data:** If you have county-level maize production records, ground-truth rainfall data, or yield trial data, please open an issue or email.
- **Methodology:** If you see a flaw in the pipeline, open an issue with the details.
- **Code:** Pull requests are welcome. Please open an issue first to discuss what you want to change.
- **Feedback:** The [Substack](https://kenyaclimatelab.substack.com) is where I write about the work. Replies and comments are read.

---

## License

- **Code:** MIT
- **Data:** CC-BY-4.0 (where permitted by source licenses)

## Contact

**Alex Haro Nyandega**
alexharonyandega@gmail.com
Nairobi, Kenya

[GitHub](https://github.com/alexharonyandega-dev) · [X](https://x.com/KenyaClimateLab) · [Substack](https://kenyaclimatelab.substack.com) · [Email](mailto:alexharonyandega@gmail.com)
