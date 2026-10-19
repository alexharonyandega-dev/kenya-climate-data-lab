cat > README.md << 'EOF'
# 🌾 Kenya Climate Data Lab

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://kenya-climate-data-lab.streamlit.app)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://kenya-climate-api.onrender.com/docs)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An open-source, county-level drought and vegetation stress monitor for all 47 Kenyan counties. 

This repository contains the full data pipeline, REST API, interactive web application, machine learning models, and Docker configurations.

## 🚀 Live Services

| Service | Description | Link |
| :--- | :--- | :--- |
| **Interactive Dashboard** | Frontend for non-technical users to explore data and view next-month drought predictions. | [Launch App](https://kenya-climate-data-lab.streamlit.app) |
| **Developer API** | REST API for programmatic access to the dataset. | [Swagger Docs](https://kenya-climate-api.onrender.com/docs) |

## 📊 Data Sources
The pipeline ingests the following open satellite datasets:
- **CHIRPS:** Rainfall estimates (0.05° resolution)
- **Sentinel-2:** Vegetation health (NDVI) via Google Earth Engine
- **ERA5-Land:** Soil moisture and temperature anomalies

## 🏗️ Architecture
- `scripts/`: Python pipeline for data ingestion, anomaly calculation, and master table generation.
- `scripts/06_drought_probability.py`: XGBoost training pipeline predicting next-month severe drought probability (ROC-AUC: 0.82).
- `data/processed/`: The canonical dataset (4,512 rows x 26 columns).
- `api/`: FastAPI backend serving JSON endpoints for county-level querying.
- `app/`: Streamlit frontend providing an interactive UI and ML inference.
- `tests/`: Comprehensive `pytest` suite covering API endpoints and data logic.
- **Docker**: Complete `Dockerfile.api`, `Dockerfile.app`, and `docker-compose.yml` for containerized deployments.

## 🧠 Machine Learning Model
The pipeline includes an XGBoost classifier that uses lagged soil moisture, rainfall, and NDVI anomalies to predict the probability of severe drought in the following month. The model achieves an **ROC-AUC of 0.82** and is integrated directly into the Streamlit frontend.

## 🛠️ Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/alexharonyandega-dev/kenya-climate-data-lab.git
   cd kenya-climate-data-lab
