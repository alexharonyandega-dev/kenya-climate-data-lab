import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine

print('🚀 Starting Cloud PostGIS Migration (Direct from DB)...')

# Your Supabase connection string (URL-encoded)
db_uri = 'postgresql://postgres.pzerwmmhkroikovxgpnz:Alex%23%402345_100%25@aws-1-eu-west-3.pooler.supabase.com:5432/postgres'

# 1. Load the updated CSV with the 6th feature
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')

# 2. Connect to PostGIS
engine = create_engine(db_uri)

# 3. Extract unique geometries from the existing database (No internet needed!)
print('🔗 Extracting spatial geometries directly from Supabase...')
gdf = gpd.read_postgis("SELECT DISTINCT ON (county) county, geometry FROM county_stress", con=engine, geom_col='geometry')

if gdf.empty:
    raise ValueError("Could not fetch geometries from PostGIS. Is the table empty?")

print(f'✅ Loaded {len(gdf)} unique county geometries.')

# 4. Merge updated CSV with geometries
print('🔗 Merging updated 6-feature climate data with geometries...')
merged = gdf.merge(df, on='county', how='inner')
print(f'✅ Merged dataset: {len(merged)} rows (counties x months)')

# 5. Push back to Supabase
print('💾 Pushing updated 6-feature dataset to Supabase...')
merged.to_postgis('county_stress', engine, if_exists='replace', index=False, chunksize=100)

print('🎉 Migration Complete! PostGIS now has the 6-feature dataset.')
