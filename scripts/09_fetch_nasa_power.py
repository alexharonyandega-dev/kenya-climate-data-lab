import pandas as pd
import requests
import time
import os
from pathlib import Path

print("⏳ Fetching NASA POWER data for all 47 counties...")
os.makedirs('data/raw/nasa_power', exist_ok=True)

# Load centroids from our existing geo file
df = pd.read_csv('data/processed/county_monthly_stress_v3_geo.csv')
centroids = df[['county', 'centroid_lat', 'centroid_lon']].drop_duplicates()

for idx, row in centroids.iterrows():
    county = row['county']
    lat = row['centroid_lat']
    lon = row['centroid_lon']
    
    outfile = f"data/raw/nasa_power/{county.replace(' ', '_')}.csv"
    if os.path.exists(outfile):
        continue # Skip if we already downloaded it
        
    print(f"Fetching {county}...")
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX,T2M_MIN&community=AG&longitude={lon}&latitude={lat}&start=20170101&end=20241231&format=CSV"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(outfile, 'wb') as f:
            f.write(response.content)
        time.sleep(0.5) # Be nice to the NASA API
    except Exception as e:
        print(f"❌ Failed to fetch {county}: {e}")

print("✅ NASA POWER data downloaded.")
