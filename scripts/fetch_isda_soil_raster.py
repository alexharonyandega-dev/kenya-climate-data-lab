"""Zonal statistics of iSDAsoil COGs for the 5 target counties.

Reads each soil property COG from S3 via /vsicurl/, masks to the county
polygon, and computes area-weighted mean + std for both depths.

Back-transforms verified empirically against iSDAsoil API values:
  pH         stored × 10
  nitrogen   exp(x/100) − 1
  others     exp(x/10) − 1
"""
import time
import warnings
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping

warnings.filterwarnings("ignore")

S3_BASE = "https://isdasoil.s3.amazonaws.com/soil_data"

# property -> (folder, filename, transform_type)
PROPERTIES = {
    "ph":                       ("ph", "ph", "div_10"),
    "nitrogen_total":           ("nitrogen_total", "nitrogen_total", "exp_x100"),
    "phosphorous_extractable":  ("phosphorous_extractable", "phosphorous_extractable", "exp_x10"),
    "potassium_extractable":    ("potassium_extractable", "potassium_extractable", "exp_x10"),
    "carbon_organic":           ("carbon_organic", "carbon_organic", "exp_x10"),
    "cation_exchange_capacity": ("cation_exchange_capacity", "cation_exchange_capacity", "exp_x10"),
    "clay_content":             ("clay_content", "clay_content", "none"),
    "sand_content":             ("sand_content", "sand_content", "none"),
}

TARGET_COUNTIES = ["Nakuru", "Kakamega", "Bungoma", "Trans Nzoia", "Uasin Gishu"]

ROOT = Path(__file__).resolve().parent.parent
BOUNDARIES = ROOT / "data" / "external" / "kenya_counties.geojson"
OUT = ROOT / "data" / "raw" / "isda_soil_raster_zonal.csv"


def back_transform(values, kind):
    if kind == "exp_x10":
        with np.errstate(over="ignore", invalid="ignore"):
            return np.exp(values / 10.0) - 1.0
    if kind == "exp_x100":
        with np.errstate(over="ignore", invalid="ignore"):
            return np.exp(values / 100.0) - 1.0
    if kind == "div_10":
        return values / 10.0
    return values


def zonal_stats(url, geom, prop, transform_kind):
    with rasterio.open(f"/vsicurl/{url}") as src:
        try:
            out_image, _ = mask(src, [geom], crop=True, filled=False)
            out_image = np.ma.filled(out_image.astype("float32"), np.nan)
        except Exception as e:
            return {"error": str(e)}

    results = {}
    bands = ["mean_0_20", "stdev_0_20", "mean_20_50", "stdev_20_50"]

    for i, band in enumerate(bands):
        if i >= out_image.shape[0]:
            results[f"{prop}_{band}"] = None
            continue
        arr = out_image[i]
        arr[arr >= 254] = np.nan       # nodata = 255
        valid = arr[np.isfinite(arr)]
        if len(valid) == 0:
            results[f"{prop}_{band}"] = None
            continue
        # Apply back-transform only on the mean band
        if "mean" in band and transform_kind != "none":
            valid = back_transform(valid, transform_kind)
            valid = valid[np.isfinite(valid)]
            if len(valid) == 0:
                results[f"{prop}_{band}"] = None
                continue
        results[f"{prop}_{band}"] = {
            "mean": float(np.mean(valid)),
            "std":  float(np.std(valid)),
            "n_pixels": int(len(valid)),
        }
    return results


def main():
    print("Loading county boundaries...")
    gdf = gpd.read_file(BOUNDARIES)
    gdf = gdf[gdf["shapeName"].isin(TARGET_COUNTIES)].reset_index(drop=True)
    print(f"  {len(gdf)} counties")

    all_rows = []
    for _, row in gdf.iterrows():
        county = row["shapeName"]
        poly = row["geometry"]
        poly_crs = gdf.crs
        print(f"\n{county}")
        out = {"county": county}

        # Reproject polygon once
        first_url = f"{S3_BASE}/{PROPERTIES['ph'][0]}/{PROPERTIES['ph'][1]}.tif"
        with rasterio.open(f"/vsicurl/{first_url}") as src:
            if poly_crs is not None and src.crs is not None:
                poly_reproj = gpd.GeoSeries([poly], crs=poly_crs).to_crs(src.crs).iloc[0]
            else:
                poly_reproj = poly
            geom = mapping(poly_reproj)

        for prop, (folder, fname, transform_kind) in PROPERTIES.items():
            url = f"{S3_BASE}/{folder}/{fname}.tif"
            t0 = time.time()
            print(f"  {prop:28s}", end=" ", flush=True)
            try:
                stats = zonal_stats(url, geom, prop, transform_kind)
                for k, v in stats.items():
                    if isinstance(v, dict):
                        out[k] = round(v["mean"], 4)
                        out[f"{k}_std"] = round(v["std"], 4)
                        out[f"{k}_n"] = v["n_pixels"]
                    else:
                        out[k] = v
                px = stats.get(f"{prop}_mean_0_20")
                n_px = px["n_pixels"] if isinstance(px, dict) else 0
                print(f"OK ({time.time()-t0:.1f}s, {n_px:,} px)")
            except Exception as e:
                print(f"FAILED: {e}")
                for band in ["mean_0_20", "stdev_0_20", "mean_20_50", "stdev_20_50"]:
                    out[f"{prop}_{band}"] = None
            time.sleep(0.3)

        all_rows.append(out)

    df = pd.DataFrame(all_rows)
    df.to_csv(OUT, index=False)
    print(f"\nWrote {OUT}\n")

    # Clean display: just mean_0_20 for the key properties
    cols = ["county"] + [f"{p}_mean_0_20" for p in PROPERTIES]
    print(df[cols].to_string(index=False))


if __name__ == "__main__":
    main()
