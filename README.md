# 🌾 Kenya Climate Data Lab (KCDL) v3.0

An open-source, county-level drought and vegetation stress monitor for all 47 Kenyan counties. This platform leverages satellite data, advanced machine learning, and spatial databases to provide real-time drought risk assessments and automated early warnings.

## 🚀 Live Deployments
- **Frontend Dashboard:** [https://kenya-climate-data-lab.streamlit.app](https://kenya-climate-data-lab.streamlit.app)
- **Backend API Docs:** [https://api.kenyaclimatelab.me/docs](https://api.kenyaclimatelab.me/docs)

## 🏗️ Architecture
- **Frontend:** Streamlit, Plotly, Folium (Interactive Maps)
- **Backend API:** FastAPI, Uvicorn (Deployed on Render)
- **Database:** Supabase (Cloud PostgreSQL + PostGIS spatial extension)
- **Machine Learning:** Scikit-learn Voting Ensemble (XGBoost + LightGBM + Random Forest)
- **Explainability:** Dynamic SHAP (TreeExplainer)
- **Data Pipeline:** GitHub Actions (Monthly data refresh & Automated email alerts)

## 🧠 Machine Learning Model
The system trains a 6-feature Voting Ensemble to predict next-month severe drought risk:
1. `swvl1_mean_anomaly` (ERA5-Land Soil Moisture)
2. `rainfall_anomaly` (CHIRPS Rainfall)
3. `ndvi_anomaly` (Sentinel-2 Vegetation Health)
4. `crop_stage_weight` (Agricultural Phenology)
5. `spei_12` (Standardized Precipitation-Evapotranspiration Index)
6. `lst_anomaly` (MODIS Land Surface Temperature)

*Metric:* Achieves a ROC-AUC of **0.787** across 3,553 validated samples.

## ✨ Key Features
- **Interactive Drought Map:** Click any of the 47 counties to instantly update the dashboard, KPIs, and charts.
- **Dynamic SHAP Explainability:** Real-time AI transparency showing exactly *why* a county is at risk (positive features push toward drought).
- **Cloud PostGIS:** Sub-second spatial queries powering the map and timeseries data.
- **Early Warning Subscriptions:** Users can subscribe to receive automated email alerts if their county enters a severe drought category.

## 💻 Local Setup
1. Clone the repository:
   git clone https://github.com/alexharonyandega-dev/kenya-climate-data-lab.git
   cd kenya-climate-data-lab

2. Create and activate the environment:
   conda create -n kenya-climate python=3.11
   conda activate kenya-climate
   pip install -r requirements.txt

3. Set your database environment variable:
   export DATABASE_URL="postgresql://postgres.user:password@host:port/postgres"

4. Run the API and Frontend locally:
   uvicorn api.main:app --reload
   streamlit run app/app.py

## 📊 Data Sources
- **CHIRPS:** Rainfall
- **Sentinel-2:** NDVI (Vegetation Condition)
- **ERA5-Land:** Soil Moisture & Evapotranspiration
- **NASA POWER:** Temperature & PET
- **MODIS:** Land Surface Temperature (LST)
- **TAMSAT:** Root-zone Soil Moisture

## 🤝 Contributing
This project is open-source. If you are a researcher, developer, or policymaker looking to improve climate resilience in Kenya, please reach out or submit a pull request.

---
*Built with passion for a climate-resilient Kenya.*
