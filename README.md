# Kenya Climate Data Lab 🌾

An open-source, county-level drought and vegetation stress monitor for all 47 Kenyan counties.

This repository contains the full data pipeline, REST API, interactive web application, machine learning models, and Docker configurations.

## 🚀 Live Services

**1. Interactive Dashboard (Streamlit)**
Frontend for non-technical users to explore the data and view next-month drought predictions.
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
1. `scripts/`: Python pipeline for data ingestion, anomaly calculation, and master table generation.
2. `scripts/06_drought_probability.py`: XGBoost training pipeline using lagged soil moisture, rainfall, and NDVI to predict next-month severe drought probability (ROC-AUC: 0.82).
3. `data/processed/county_monthly_stress_v3.csv`: The canonical dataset (4,512 rows × 26 columns).
4. `api/`: FastAPI backend serving JSON endpoints for county-level querying.
5. `app/`: Streamlit frontend providing an interactive UI and inference on the exported model.
6. `tests/`: Comprehensive `pytest` suite covering API endpoints and data logic.
7. **Docker**: Complete `Dockerfile.api`, `Dockerfile.app`, and `docker-compose.yml` for containerized deployments.

## 🛠️ Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/alexharonyandega-dev/kenya-climate-data-lab.git
cd kenya-climate-data-lab
