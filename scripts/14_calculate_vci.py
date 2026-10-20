import pandas as pd
import numpy as np

print("⏳ Calculating VCI...")
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')
df['ndvi_min'] = df.groupby(['county', 'month'])['ndvi'].transform('min')
df['ndvi_max'] = df.groupby(['county', 'month'])['ndvi'].transform('max')

df['vci'] = np.where(
    (df['ndvi_max'] - df['ndvi_min']) == 0,
    50.0,
    ((df['ndvi'] - df['ndvi_min']) / (df['ndvi_max'] - df['ndvi_min'])) * 100
)

df.to_csv('data/processed/county_monthly_stress_v3.csv', index=False)
print("✅ VCI calculated successfully!")
