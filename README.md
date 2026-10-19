# Kenya Climate Data Lab 🌾

An open-source, county-level drought and vegetation stress monitor for all 47 Kenyan counties.

This repository contains the full data pipeline, REST API, and interactive web application.

## 🚀 Live Application
**View the dashboard here:** [https://kenya-climate-data-lab.streamlit.app](https://kenya-climate-data-lab.streamlit.app)

## 📊 Data Sources
The pipeline ingests open satellite data:
- **CHIRPS:** Rainfall estimates (0.05° resolution)
- **Sentinel-2:** Vegetation health (NDVI) via Google Earth Engine
- **ERA5-Land:** Soil moisture and temperature anomalies

## 🏗️ Architecture
1. : Python pipeline for data ingestion, anomaly calculation, and master table generation.
2. : The canonical dataset (4,512 rows × 26 columns).
3. : FastAPI backend serving JSON endpoints for county-level querying.
4. : Streamlit frontend providing an interactive UI for non-technical users.

## 🛠️ Local Setup

1. Clone the repository
    git clone https://github.com/alexharonyandega-dev/kenya-climate-data-lab.git
    cd kenya-climate-data-lab

2. Create the environment
    conda create -n kenya-climate python=3.11 -y
    conda activate kenya-climate
    pip install -r requirements.txt

3. Run the Streamlit App
    streamlit run app/app.py

4. Run the FastAPI Backend
    uvicorn api.main:app --reload

(API documentation is auto-generated at http://127.0.0.1:8000/docs)

## 📄 License
MIT License
