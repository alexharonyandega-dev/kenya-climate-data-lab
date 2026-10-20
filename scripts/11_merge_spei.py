import pandas as pd
import numpy as np

print("⏳ Aggregating PET and calculating SPEI...")

# 1. Load and aggregate daily PET to monthly
df_pet = pd.read_csv('data/raw/nasa_power_pet_all.csv', parse_dates=['date'])
df_pet['year'] = df_pet['date'].dt.year
df_pet['month'] = df_pet['date'].dt.month

monthly_pet = df_pet.groupby(['county', 'year', 'month'])['pet_mm_day'].sum().reset_index()
monthly_pet.rename(columns={'pet_mm_day': 'pet_mm'}, inplace=True)

# 2. Load the Master table
master = pd.read_csv('data/processed/county_monthly_stress_v3.csv', parse_dates=['month_start'])
master = master.sort_values(by=['county', 'month_start']).reset_index(drop=True)

# 3. Merge PET into Master
master = master.merge(monthly_pet, on=['county', 'year', 'month'], how='left')

# 4. Calculate Water Balance (Precipitation - PET)
master['water_balance'] = master['rainfall_mm'] - master['pet_mm']

# 5. Calculate SPEI (Simplified 12-month rolling z-score)
# We calculate the 12-month rolling sum of water balance, then standardize it per county
def calc_spei(group):
    # Rolling sum (12 months)
    rolling_wb = group['water_balance'].rolling(window=12, min_periods=6).sum()
    # Standardize (z-score)
    mean_wb = rolling_wb.mean()
    std_wb = rolling_wb.std()
    return (rolling_wb - mean_wb) / std_wb

master['spei_12'] = master.groupby('county', group_keys=False).apply(calc_spei)

# 6. Save the updated master table
master.to_csv('data/processed/county_monthly_stress_v3.csv', index=False)
print("✅ SPEI successfully merged into the master table!")
print(master[['county', 'month_start', 'rainfall_mm', 'pet_mm', 'water_balance', 'spei_12']].dropna().head())
