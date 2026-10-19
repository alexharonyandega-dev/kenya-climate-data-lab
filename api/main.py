from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np

app = FastAPI(
    title="Kenya Climate Data Lab API",
    description="REST API for querying county-level drought and vegetation stress data.",
    version="1.0.0"
)

# Load the master dataset
df = pd.read_csv('data/processed/county_monthly_stress_v3.csv')

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Kenya Climate Data Lab API",
        "docs": "Go to /docs to see the interactive Swagger UI",
        "endpoints": ["/counties", "/stress/{county_name}"]
    }

@app.get("/counties")
def get_counties():
    """Returns a list of all 47 Kenyan counties."""
    counties = sorted(df['county'].unique().tolist())
    return {"count": len(counties), "counties": counties}

@app.get("/stress/{county_name}")
def get_stress(county_name: str):
    """Returns the full historical stress record for a specific county."""
    # Case-insensitive match
    county_data = df[df['county'].str.lower() == county_name.lower()].copy()
    
    if county_data.empty:
        raise HTTPException(status_code=404, detail=f"County '{county_name}' not found.")
    
    # Select columns and format dates
    county_data = county_data[['month_start', 'stress_avg', 'stress_category', 'crop_stage']]
    county_data['month_start'] = county_data['month_start'].astype(str)
    
    # THE FIX: Handle Infinity and NaN
    county_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    county_data = county_data.astype(object).where(pd.notnull(county_data), None)
    
    # Convert to list of dictionaries
    records = county_data.to_dict(orient="records")
    
    return {
        "county": county_name.title(),
        "records": len(records),
        "data": records
    }
