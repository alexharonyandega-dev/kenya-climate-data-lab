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
            AND EXTRACT(YEAR FROM month_start::date) = :yr 
            AND EXTRACT(MONTH FROM month_start::date) = :mo
        """)
        result = conn.execute(query, {"cat": category, "yr": year, "mo": month})
        
        alerts = [dict(row._mapping) for row in result]
        if not alerts:
            raise HTTPException(status_code=404, detail=f"No {category} alerts found for {year}-{month}")
        return alerts


class Subscription(BaseModel):
    email: str
    county: str

@app.post("/subscribe")
def subscribe(sub: Subscription):
    try:
        with engine.connect() as conn:
            # Insert or update the subscription
            query = text("""
                INSERT INTO subscribers (email, county) 
                VALUES (:email, :county) 
                ON CONFLICT (email) DO UPDATE SET county = :county
            """)
            conn.execute(query, {"email": sub.email, "county": sub.county})
            conn.commit()
        return {"status": "success", "message": f"Subscribed {sub.email} to {sub.county} alerts."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/base_map")
def get_base_map():
    """Returns a FeatureCollection of the distinct 47 county geometries for the base map."""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT jsonb_build_object(
                    'type', 'FeatureCollection',
                    'features', jsonb_agg(jsonb_build_object(
                        'type', 'Feature',
                        'geometry', ST_AsGeoJSON(geometry)::jsonb,
                        'properties', jsonb_build_object('shapeName', county)
                    ))
                ) AS geojson
                FROM (SELECT DISTINCT ON (county) county, geometry FROM county_stress) AS distinct_counties
            """)
            result = conn.execute(query).scalar()
            if not result:
                raise HTTPException(status_code=404, detail="No map data found")
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/map_data/{year}/{month}")
def get_map_data(year: int, month: int):
    """Returns a complete GeoJSON FeatureCollection for the Folium map."""
    try:
        with engine.connect() as conn:
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
                WHERE EXTRACT(YEAR FROM month_start::date) = :yr
                AND EXTRACT(MONTH FROM month_start::date) = :mo
            """)
            result = conn.execute(query, {"yr": year, "mo": month}).scalar()
            if not result:
                raise HTTPException(status_code=404, detail=f"No map data for {year}-{month}")
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/all_data")
def get_all_data():
    """Returns the entire dataset for the dashboard in one fast request."""
    try:
        with engine.connect() as conn:
            query = text("SELECT county, month_start::text, stress_avg, stress_weighted, stress_category, crop_stage, vci, spei_12, swvl1_mean_anomaly, rainfall_anomaly, ndvi_anomaly, crop_stage_weight, lst_anomaly FROM county_stress ORDER BY county, month_start")
            result = conn.execute(query)
            return [dict(row._mapping) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import json

@app.get("/lstm_forecast/{county}")
def get_lstm_forecast(county: str):
    try:
        with open('app/lstm_forecast.json', 'r') as f:
            forecasts = json.load(f)
        if county in forecasts:
            return {"county": county, "forecasted_stress_avg": forecasts[county]}
        raise HTTPException(status_code=404, detail="County not found in LSTM forecasts")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
