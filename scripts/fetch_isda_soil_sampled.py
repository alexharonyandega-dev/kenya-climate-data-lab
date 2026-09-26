"""Sample 8 critical iSDAsoil properties across county polygons.

Rate-limit-aware: 15 points x 8 properties x 5 counties = 600 calls.
Includes exponential backoff if 429 responses appear.
"""

import os, random, time
from pathlib import Path
import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import Point

USERNAME = os.environ["ISDA_USERNAME"]
PASSWORD = os.environ["ISDA_PASSWORD"]
BASE_URL = "https://api.isda-africa.com"

N_POINTS = 15
PROPERTIES = [
    "ph", "nitrogen_total", "phosphorous_extractable",
    "potassium_extractable", "carbon_organic",
    "cation_exchange_capacity", "clay_content", "sand_content",
]
TARGET_COUNTIES = ["Nakuru", "Kakamega", "Bungoma", "Trans Nzoia", "Uasin Gishu"]

ROOT = Path(__file__).resolve().parent.parent
BOUNDARIES = ROOT / "data" / "external" / "kenya_counties.geojson"
RAW = ROOT / "data" / "raw"
OUT_AVG = RAW / "isda_soil_properties_by_county_sampled.csv"
OUT_RAW = RAW / "isda_soil_properties_points_raw.csv"

# --- Login ---
print("Logging in...")
r = requests.post(f"{BASE_URL}/login", data={"username": USERNAME, "password": PASSWORD})
r.raise_for_status()
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("  OK")

# --- Load polygons ---
gdf = gpd.read_file(BOUNDARIES)
gdf = gdf[gdf["shapeName"].isin(TARGET_COUNTIES)].reset_index(drop=True)
print(f"Loaded {len(gdf)} counties")


def sample_points(poly, n):
    minx, miny, maxx, maxy = poly.bounds
    pts, attempts = [], 0
    while len(pts) < n and attempts < n * 200:
        attempts += 1
        x, y = random.uniform(minx, maxx), random.uniform(miny, maxy)
        if poly.contains(Point(x, y)):
            pts.append((y, x))
    return pts


def query(lat, lon, prop):
    """One call, one property. Exponential backoff on 429."""
    for delay in [0, 5, 15, 60]:
        if delay:
            time.sleep(delay)
        try:
            r = requests.get(
                f"{BASE_URL}/isdasoil/v2/soilproperty",
                params={"lat": lat, "lon": lon, "property": prop, "depth": "0-20"},
                headers=headers, timeout=30,
            )
            if r.status_code == 429:
                print(f"      429 — backing off {delay or 'next'}s")
                continue
            r.raise_for_status()
            entries = r.json().get("property", {}).get(prop, [])
            return entries[0]["value"]["value"] if entries else None
        except requests.exceptions.HTTPError:
            return None
        except Exception:
            time.sleep(2)
    return None


county_rows, raw_rows = [], []
call_count = 0

for _, row in gdf.iterrows():
    county = row["shapeName"]
    poly = row["geometry"]
    print(f"\n{county}...")

    coords = sample_points(poly, N_POINTS)
    print(f"  {len(coords)} points")

    per_prop = {p: [] for p in PROPERTIES}

    for i, (lat, lon) in enumerate(coords):
        pt = {"county": county, "lat": round(lat, 4), "lon": round(lon, 4)}
        for prop in PROPERTIES:
            v = query(lat, lon, prop)
            call_count += 1
            pt[prop] = v
            if v is not None:
                per_prop[prop].append(v)
            time.sleep(0.4)   # steady throttle to stay under rate limit
        raw_rows.append(pt)
        got = sum(1 for p in PROPERTIES if pt[p] is not None)
        print(f"    {i+1}/{len(coords)} (this point: {got}/8) | total calls: {call_count}")

    summary = {"county": county, "n_points": len(coords)}
    for p in PROPERTIES:
        vals = per_prop[p]
        summary[p] = round(sum(vals)/len(vals), 4) if vals else None
    county_rows.append(summary)
    print(f"  Done {county}")

avg_df = pd.DataFrame(county_rows)
avg_df.to_csv(OUT_AVG, index=False)
pd.DataFrame(raw_rows).to_csv(OUT_RAW, index=False)

print(f"\nWrote {OUT_AVG}")
print(f"Wrote {OUT_RAW}")
print()
print(avg_df.to_string(index=False))
