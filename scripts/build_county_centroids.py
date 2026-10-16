"""
Compute county centroids from the Kenya geojson and join them
onto the master stress table.

Produces: data/processed/county_monthly_stress_v3_geo.csv
  = county_monthly_stress_v3.csv + (centroid_lon, centroid_lat)

Purpose: Tableau Public's geocoder does not recognize Kenya's 47
counties as an administrative level, so maps using the built-in
"County" geographic role return zero marks. Explicit centroid
coordinates fix this — Tableau plots them directly.

Centroid definition: simple average of all polygon vertices. Not
the strict geometric centroid, but accurate to within a few km for
Kenyan counties (all reasonably convex). Adequate for a dot map.

Idempotent: overwrites county_monthly_stress_v3_geo.csv. The
source file county_monthly_stress_v3.csv is never modified.

Exits with a non-zero status if any county name mismatch is found
between the geojson and the master CSV, so silent drift is
impossible.
"""
import json
import sys
import pandas as pd
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GEOJSON = REPO / "data/external/kenya_counties.geojson"
MASTER = REPO / "data/processed/county_monthly_stress_v3.csv"
OUT = REPO / "data/processed/county_monthly_stress_v3_geo.csv"


def centroid(geometry):
    """Return (lon, lat) = average of all polygon vertices."""
    coords = geometry["coordinates"]
    points = []
    if geometry["type"] == "Polygon":
        for ring in coords:
            points.extend(ring)
    elif geometry["type"] == "MultiPolygon":
        for poly in coords:
            for ring in poly:
                points.extend(ring)
    if not points:
        return None, None
    lons = [p[0] for p in points]
    lats = [p[1] for p in points]
    return sum(lons) / len(lons), sum(lats) / len(lats)


def main():
    gj = json.loads(GEOJSON.read_text())
    centroids = {}
    for feat in gj["features"]:
        name = feat["properties"]["shapeName"]
        lon, lat = centroid(feat["geometry"])
        if lon is not None:
            centroids[name] = {"centroid_lon": lon, "centroid_lat": lat}
    print(f"Computed {len(centroids)} centroids from {GEOJSON.name}")

    df = pd.read_csv(MASTER, dtype={"county": str})
    print(f"Master CSV: {len(df)} rows, {df['county'].nunique()} unique counties")

    csv_names = set(df["county"].unique())
    geo_names = set(centroids.keys())
    only_csv = csv_names - geo_names
    only_geo = geo_names - csv_names

    print(f"Matched: {len(csv_names & geo_names)} / {len(geo_names)}")
    if only_csv or only_geo:
        if only_csv:
            print(f"  In CSV not geojson: {sorted(only_csv)}")
        if only_geo:
            print(f"  In geojson not CSV: {sorted(only_geo)}")
        sys.exit("County name mismatch — refusing to write.")

    df["centroid_lon"] = df["county"].map(lambda c: centroids[c]["centroid_lon"])
    df["centroid_lat"] = df["county"].map(lambda c: centroids[c]["centroid_lat"])

    df.to_csv(OUT, index=False)
    print(f"Wrote {OUT.relative_to(REPO)}")
    print(f"  Rows: {len(df)}  Cols: {len(df.columns)}")


if __name__ == "__main__":
    main()
