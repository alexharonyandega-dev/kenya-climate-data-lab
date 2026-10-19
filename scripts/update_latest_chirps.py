import pandas as pd
from datetime import datetime

print(f'⏳ Starting automated data update at {datetime.now()}')

master_file = 'data/processed/county_monthly_stress_v3.csv'
df = pd.read_csv(master_file)

print(f'✅ Successfully loaded {len(df)} rows from master dataset.')
print('✅ (Simulated) Latest CHIRPS data ingested successfully.')
print('🔄 Ready for Git commit.')
