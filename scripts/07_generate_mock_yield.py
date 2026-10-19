import pandas as pd
import numpy as np

np.random.seed(42)

print("Generating mock CGIAR yield dataset...")
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')
counties = df['county'].unique()

records = []
for county in counties:
    base_yield = np.random.uniform(1.2, 2.5) # tonnes per hectare
    for year in range(1990, 2025):
        # Simulate a drought effect every few years
        drought_impact = np.random.normal(0, 0.3)
        if year in [2000, 2009, 2017, 2022]:
            drought_impact -= np.random.uniform(0.5, 1.2)
            
        yield_val = max(0.1, base_yield + drought_impact)
        
        records.append({
            'county': county,
            'year': year,
            'yield_tonnes_ha': round(yield_val, 2)
        })

mock_df = pd.DataFrame(records)
mock_df.to_csv('data/processed/mock_yield_data.csv', index=False)
print(f"✅ Generated {len(mock_df)} yield records at data/processed/mock_yield_data.csv")
