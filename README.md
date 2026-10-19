# Kenya Climate Data Lab 🌾

An open-source, county-level drought and vegetation stress monitor for all 47 Kenyan counties.

This repository contains the full data pipeline, REST API, interactive web application, and Docker configurations.

## 🚀 Live Services

**1. Interactive Dashboard (Streamlit)**
Frontend for non-technical users to explore the data.
👉 [https://kenya-climate-data-lab.streamlit.app](https://kenya-climate-data-lab.streamlit.app)

**2. Developer API (FastAPI)**
REST API for programmatic access to the dataset.
👉 **Live Swagger Docs:** [https://kenya-climate-api.onrender.com/docs](https://kenya-climate-api.onrender.com/docs)

## 📊 Data Sources
The pipeline ingests open satellite data:
- **CHIRPS:** Rainfall estimates (0.05° resolution)
- **Sentinel-2:** Vegetation health (NDVI) via Google Earth Engine
- **ERA5-Land:** Soil moisture and temperature anomalies

## 🏗️ Architecture
1. scripts/: Python pipeline for data ingestion, anomaly calculation, and master table generation.
2. data/processed/county_monthly_stress_v3.csv: The canonical dataset (4,512 rows × 26 columns).
3. api/: FastAPI backend serving JSON endpoints for county-level querying.
4. app/: Streamlit frontend providing an interactive UI for non-technical users.
5. tests/: Comprehensive pytest suite covering API endpoints and data logic.
6. Docker: Complete Dockerfile.api, Dockerfile.app, and docker-compose.yml for containerized deployments.

## 🛠️ Local Setup

1. Clone the repository
   git clone https://github.com/alexharonyandega-dev/kenya-climate-data-lab.git
   cd kenya-climate-data-lab

2. Create the environment
   conda create -n kenya-climate python=3.11 -y
   conda activate kenya-climate
   pip install -r requirements.txt

3. Run the Tests
   pytest tests/ -v

4. Run the Streamlit App
   streamlit run app/app.py

5. Run the FastAPI Backend
   uvicorn api.main:app --reload
   (API documentation is auto-generated at http://127.0.0.1:8000/docs)

## 🐳 Docker Deployment
To spin up both the API and the frontend simultaneously:
   docker-compose up --build

## 📄 License
MIT License
