import pandas as pd
import numpy as np
import glob
import os

print("⏳ Calculating Hargreaves-Samani PET...")
all_data = []

for file in glob.glob('data/raw/nasa_power/*.csv'):
    county = os.path.basename(file).replace('.csv', '').replace('_', ' ')

    # Header block is 11 lines; line 12 is the actual CSV header
    df = pd.read_csv(file, skiprows=11)
    df['county'] = county
    df['date'] = pd.to_datetime(df['YEAR'].astype(str) + df['DOY'].astype(str), format='%Y%j')

    # Handle NASA POWER missing values
    df = df.replace(-999, np.nan)

    Ra = 15.0
    df['pet_mm_day'] = 0.0023 * (df['T2M'] + 17.8) * np.sqrt(df['T2M_MAX'] - df['T2M_MIN']) * Ra
    all_data.append(df[['county', 'date', 'pet_mm_day']])

final_df = pd.concat(all_data)
final_df = final_df.dropna(subset=['pet_mm_day'])
final_df.to_csv('data/raw/nasa_power_pet_all.csv', index=False)
print(f"✅ PET calculated for {final_df['county'].nunique()} counties → {len(final_df)} rows saved.")
