import pandas as pd
import numpy as np
import joblib
import shap
import json

print("🔍 Calculating SHAP values (positive-class, 5 features)...")
model = joblib.load('app/ensemble_model.pkl')
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')

features = ['swvl1_mean_anomaly', 'rainfall_anomaly', 'ndvi_anomaly', 'crop_stage_weight', 'spei_12']
X = df[features].dropna()

explainer = shap.KernelExplainer(model.predict_proba, X.sample(50, random_state=42))
shap_values = explainer.shap_values(X.iloc[[-1]])

# --- Normalize to a 1-D array of positive-class SHAP values ---
if isinstance(shap_values, list):
    vals = np.asarray(shap_values[1][0]).ravel()
else:
    sv = np.asarray(shap_values)
    if sv.ndim == 3:
        vals = sv[0, :, 1]      # sample 0, all features, class 1
    elif sv.ndim == 2:
        vals = sv[0]            # sample 0, all features
    else:
        vals = sv.ravel()

feature_shaps = {f: float(v) for f, v in zip(features, vals)}

with open('app/shap_values.json', 'w') as fh:
    json.dump(feature_shaps, fh, indent=2)

print("✅ SHAP values saved. Positive = pushes TOWARD drought:")
for k, v in feature_shaps.items():
    print(f"   {k:22s}: {v:+.4f}")
