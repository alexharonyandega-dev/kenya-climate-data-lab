import pandas as pd
import joblib
import shap
import json

print("🔍 Calculating SHAP values...")
model = joblib.load('app/ensemble_model.pkl')
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')

features = ['swvl1_mean_anomaly', 'rainfall_anomaly', 'ndvi_anomaly', 'crop_stage_weight']
X = df[features].dropna()

explainer = shap.KernelExplainer(model.predict_proba, X.sample(50))
shap_values = explainer.shap_values(X.iloc[[-1]])

# FIX: Handle the varying shape of shap_values
if isinstance(shap_values, list):
    vals = shap_values[-1][0]  # Grabs the positive class (severe drought)
else:
    vals = shap_values[0]      # Grabs the only output array

feature_shaps = dict(zip(features, vals.tolist()))
with open('app/shap_values.json', 'w') as f:
    json.dump(feature_shaps, f)

print("✅ SHAP values saved to app/shap_values.json")
print(feature_shaps)
