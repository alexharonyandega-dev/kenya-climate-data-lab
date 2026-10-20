import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import requests
import os

print('🚀 Starting Cloud PostGIS Migration...')

# 1. Download Kenya Counties GeoJSON
geojson_path = 'data/external/kenya_counties.geojson'
if not os.path.exists(geojson_path):
    print('📥 Downloading Kenya GeoJSON...')
    os.makedirs('data/external', exist_ok=True)
    url = 'https://raw.githubusercontent.com/geoffreynak/kenya-counties-geojson/master/kenya_counties.geojson'
    r = requests.get(url)
    with open(geojson_path, 'wb') as f:
        f.write(r.content)
    print('✅ GeoJSON downloaded.')

# 2. Load Master CSV and GeoJSON
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')
gdf = gpd.read_file(geojson_path)

if 'shapeName' in gdf.columns:
    gdf = gdf.rename(columns={'shapeName': 'county'})
elif 'COUNTY' in gdf.columns:
    gdf = gdf.rename(columns={'COUNTY': 'county'})

# 3. Merge spatial geometries with climate data
print('🔗 Merging climate data with spatial geometries...')
merged = gdf.merge(df, on='county', how='inner')

# THE FIX: Simplify geometries to reduce file size and prevent timeouts
print('✂️ Simplifying map geometries (reduces size by 90%)...')
merged['geometry'] = merged['geometry'].simplify(0.01)
print(f'✅ Merged dataset: {len(merged)} rows (counties x months)')

# 4. Push to Supabase
print('💾 Pushing to Supabase PostGIS (in chunks)...')
engine = create_engine('postgresql://postgres.pzerwmmhkroikovxgpnz:Alex%23%402345_100%25@aws-1-eu-west-3.pooler.supabase.com:5432/postgres', connect_args={'options': '-c statement_timeout=300000'})
merged.to_postgis('county_stress', engine, if_exists='replace', index=False, chunksize=100)

print('🎉 Migration Complete! Table county_stress is live in Supabase.')
