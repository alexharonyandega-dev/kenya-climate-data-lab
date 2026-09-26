"""Fetch iSDAsoil properties for the 5 target counties.

The iSDAsoil v2 API accepts only ONE property per request, so we loop
over properties and combine the results into a single row per county.
"""
import os
import time
from pathlib import Path

import pandas as pd
import requests

USERNAME = os.environ.get("ISDA_USERNAME")
PASSWORD = os.environ.get("ISDA_PASSWORD")
if not USERNAME or not PASSWORD:
    raise SystemExit("ERROR: Set ISDA_USERNAME and ISDA_PASSWORD.")

BASE_URL = "https://api.isda-africa.com"

print("Logging in to iSDAsoil API...")
login_resp = requests.post(f"{BASE_URL}/login",
                           data={"username": USERNAME, "password": PASSWORD})
login_resp.raise_for_status()
access_token = login_resp.json().get("access_token")
print("  Token acquired")

PROPERTIES = [
    "nitrogen_total",
    "phosphorous_extractable",
    "potassium_extractable",
    "carbon_organic",
    "ph",
    "cation_exchange_capacity",
    "sulphur_extractable",
    "magnesium_extractable",
    "calcium_extractable",
    "zinc_extractable",
    "bulk_density",
    "clay_content",
    "sand_content",
    "silt_content",
]

COUNTIES = {
    "Nakuru":      {"lat": -0.3031, "lon": 36.0800},
    "Kakamega":    {"lat":  0.2827, "lon": 34.7519},
    "Bungoma":     {"lat":  0.5635, "lon": 34.5606},
    "Trans Nzoia": {"lat":  1.0566, "lon": 34.9519},
    "Uasin Gishu": {"lat":  0.5143, "lon": 35.2698},
}

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = RAW_DIR / "isda_soil_properties_by_county.csv"

headers = {"Authorization": f"Bearer {access_token}"}
records = []

for county, coords in COUNTIES.items():
    print(f"Querying {county}...")
    row = {"county": county, "lat": coords["lat"], "lon": coords["lon"]}

    for prop in PROPERTIES:
        params = {
            "lat": coords["lat"],
            "lon": coords["lon"],
            "property": prop,
            "depth": "0-20",
        }
        try:
            resp = requests.get(f"{BASE_URL}/isdasoil/v2/soilproperty",
                                params=params, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            entries = data.get("property", {}).get(prop, [])
            if entries:
                row[prop] = entries[0]["value"]["value"]
            else:
                row[prop] = None
        except Exception as e:
            print(f"    FAILED {prop}: {e}")
            row[prop] = None
        time.sleep(0.3)  # be polite to the API

    records.append(row)
    non_null = sum(1 for p in PROPERTIES if row.get(p) is not None)
    print(f"  OK  {county}: {non_null}/{len(PROPERTIES)} values returned")

df = pd.DataFrame(records)
df.to_csv(OUTPUT_FILE, index=False)
print(f"\nWrote {len(df)} rows x {len(df.columns)} cols to {OUTPUT_FILE}")
print()
print(df.to_string(index=False))
