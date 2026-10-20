from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="Kenya Climate Data Lab API", version="3.0.0 (PostGIS)")

# Allow your Streamlit app to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the Database URL from the environment
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres.pzerwmmhkroikovxgpnz:YOUR_PASSWORD@aws-1-eu-west-3.pooler.supabase.com:5432/postgres")
engine = create_engine(DB_URL, pool_size=10, max_overflow=20)

class AlertResponse(BaseModel):
    county: str
    month_start: str
    stress_category: str
    stress_avg: float

@app.get("/")
def root():
    return {"status": "healthy", "database": "Cloud PostGIS", "version": "3.0.0"}

@app.get("/counties")
def get_counties():
    """Returns a list of all 47 counties."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT county FROM county_stress ORDER BY county"))
        return [row[0] for row in result]

@app.get("/alerts/{category}", response_model=List[AlertResponse])
def get_alerts(
    category: str, 
    year: int = Query(2022, description="Year to query"), 
    month: int = Query(10, description="Month to query")
):
    """Returns all counties in a specific stress category."""
    with engine.connect() as conn:
        query = text("""
            SELECT county, month_start::text, stress_category, stress_avg 
            FROM county_stress 
            WHERE stress_category = :cat 
            AND EXTRACT(YEAR FROM month_start) = :yr 
            AND EXTRACT(MONTH FROM month_start) = :mo
        """)
        result = conn.execute(query, {"cat": category, "yr": year, "mo": month})
        
        alerts = [dict(row._mapping) for row in result]
        if not alerts:
            raise HTTPException(status_code=404, detail=f"No {category} alerts found for {year}-{month}")
        return alerts

@app.get("/map_data/{year}/{month}")
def get_map_data(year: int, month: int):
    """Returns a complete GeoJSON FeatureCollection for the Folium map."""
    with engine.connect() as conn:
        # ST_AsGeoJSON converts the PostGIS geometry into standard JSON
        query = text("""
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features', jsonb_agg(jsonb_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(geometry)::jsonb,
                    'properties', jsonb_build_object(
                        'county', county,
                        'stress_avg', stress_avg,
                        'stress_category', stress_category,
                        'spei_12', spei_12,
                        'vci', vci
                    )
                ))
            ) AS geojson
            FROM county_stress
            WHERE EXTRACT(YEAR FROM month_start) = :yr 
            AND EXTRACT(MONTH FROM month_start) = :mo
        """)
        result = conn.execute(query, {"yr": year, "mo": month}).scalar()
        
        if not result:
            raise HTTPException(status_code=404, detail=f"No map data for {year}-{month}")
        return result

@app.get("/timeseries/{county}")
def get_timeseries(county: str):
    """Returns the full 8-year history for a single county."""
    with engine.connect() as conn:
        query = text("""
            SELECT month_start::text, stress_avg, stress_category, vci, spei_12 
            FROM county_stress 
            WHERE county = :county 
            ORDER BY month_start
        """)
        result = conn.execute(query, {"county": county})
        data = [dict(row._mapping) for row in result]
        
        if not data:
            raise HTTPException(status_code=404, detail=f"County {county} not found")
        return data
