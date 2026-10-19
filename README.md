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
1. : Python pipeline for data ingestion, anomaly calculation, and master table generation.
2. : XGBoost training pipeline using lagged soil moisture, rainfall, and NDVI to predict next-month severe drought probability (ROC-AUC: 0.82).
3. : The canonical dataset (4,512 rows × 26 columns).
4. : FastAPI backend serving JSON endpoints for county-level querying.
5. : Streamlit frontend providing an interactive UI and inference on the exported model.
6. : Comprehensive ============================= test session starts ==============================
platform darwin -- Python 3.11.16, pytest-8.3.4, pluggy-1.7.0
rootdir: /Users/AlexHaro/Desktop/kenya-climate-data-lab
plugins: anyio-4.15.1
collected 4 items

tests/test_api.py ....                                                   [100%]

=============================== warnings summary ===============================
../../Applications/homebrew/Caskroom/miniconda/base/envs/kenya-climate/lib/python3.11/site-packages/fastapi/testclient.py:1
  /Users/AlexHaro/Applications/homebrew/Caskroom/miniconda/base/envs/kenya-climate/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
========================= 4 passed, 1 warning in 1.84s ========================= suite covering API endpoints and data logic.
7. **Docker**: Complete , , and  for containerized deployments.

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
