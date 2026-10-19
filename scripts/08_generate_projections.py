import pandas as pd
from scipy.stats import linregress
import json

print("⏳ Computing per-county projection coefficients...")
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')
coefs = {}

for county, g in df.groupby('county'):
    g = g.dropna(subset=['swvl1_mean_anomaly', 'ndvi_anomaly']).sort_values('month_start')
    if len(g) < 60:
        continue
    
    # Predict next month's NDVI anomaly using this month's soil moisture
    x = g.swvl1_mean_anomaly.iloc[:-1]
    y = g.ndvi_anomaly.shift(-1).dropna()
    
    # Ensure matching lengths
    min_len = min(len(x), len(y))
    x = x.iloc[:min_len]
    y = y.iloc[:min_len]
    
    r = linregress(x, y)
    coefs[county] = {
        'a': round(r.slope, 4),
        'b': round(r.intercept, 4),
        'r': round(r.rvalue, 3),
        'n': len(y)
    }

with open('data/projection_coefs.json', 'w') as f:
    json.dump(coefs, f, indent=4)
    
print(f"✅ Saved projections for {len(coefs)} counties to data/projection_coefs.json")
