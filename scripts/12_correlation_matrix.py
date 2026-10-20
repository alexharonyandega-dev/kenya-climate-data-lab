import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("⏳ Generating correlation matrix...")
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')

cols = ['spei_12', 'rainfall_anomaly', 'ndvi_anomaly', 'swvl1_mean_anomaly']
corr = df[cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
plt.title('Correlation: SPEI vs Raw Anomalies')
plt.tight_layout()

os.makedirs('paper/figures', exist_ok=True)
plt.savefig('paper/figures/fig_spei_correlation.png')
print("✅ Saved correlation matrix to paper/figures/fig_spei_correlation.png")
