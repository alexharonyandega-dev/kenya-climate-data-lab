import json
from pathlib import Path

CELLS = []

def md(text):
    lines = text.strip("\n").split("\n")
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    CELLS.append({"cell_type": "markdown", "metadata": {}, "source": src})

def code(text):
    lines = text.strip("\n").split("\n")
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    CELLS.append({"cell_type": "code", "metadata": {},
                  "execution_count": None, "outputs": [], "source": src})

md("""
# 03 - Integration

**Project:** Kenya Climate Data Lab
**Author:** Alex Haro Nyandega
**Date:** 2026-10-12
**Purpose:** Audit the existing drought-stress pipeline, then integrate
the crop calendar and ERA5 soil-moisture signals.

## Rules
1. Every merge goes through `logged_join()`.
2. Every dropped row is accounted for.
3. Notebook reruns on a fresh kernel in under 60 seconds.
4. No new raw data. Everything comes from Week 3 outputs.
""")

code("""
import hashlib
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", 120)
pd.set_option("display.width", 240)
sns.set_style("whitegrid")

ROOT  = Path("..").resolve()
PROC  = ROOT / "data" / "processed"
META  = ROOT / "data" / "metadata"
PAPER = ROOT / "paper"
FIGS  = PAPER / "figures"
for p in [PROC, META, PAPER, FIGS]:
    p.mkdir(parents=True, exist_ok=True)
print("Setup OK. ROOT =", ROOT)
""")

md("""
## 1. `logged_join()` - the audit discipline

Every merge in this notebook goes through this function. It records
rows before, rows after, rows dropped, and duplicate keys in the
right table (the number one cause of silent row explosions).
""")

code("""
JOIN_AUDIT = []

def logged_join(left, right, on, how="inner", label="J", right_name="right"):
    on_list = on if isinstance(on, list) else [on]
    before = len(left)
    right_before = len(right)

    dupes_right = right.duplicated(subset=on_list).sum()
    if dupes_right > 0:
        print(f"  WARNING {label}: right table '{right_name}' has "
              f"{dupes_right} duplicate keys on {on_list}")

    out = left.merge(right, on=on, how=how, suffixes=("", "_r"))
    after = len(out)
    dropped = before - after if how == "inner" else 0
    unmatched = int(out[on_list[0]].isna().sum()) if how == "left" else 0

    JOIN_AUDIT.append({
        "join": label, "left_rows": before, "right_rows": right_before,
        "type": how, "keys": ", ".join(on_list), "result_rows": after,
        "dropped": dropped, "unmatched": unmatched,
    })
    print(f"  {label}: {before:>7,} {how:>5} {right_before:>7,} "
          f"-> {after:>7,}  (dropped {dropped}, unmatched {unmatched})")
    return out

print("logged_join() ready.")
""")

md("""
## 2. Load every existing processed file

Column names as they actually are on disk (confirmed before this notebook
was written):

- stress master: `county, year, month, date, ...`
- weekly rain  : `iso_year, iso_week, county, rainfall_mm, ...` (no date column)
- crop calendar: `county, zone, ..., long_rains_start, long_rains_end, ...`
- ERA5 long    : `date, county, variable, value`
- NDVI monthly : `name, year, month, date, mean` (county column is `name`)
""")

code("""
def try_load(path, **kw):
    p = Path(path)
    if not p.exists():
        print(f"  MISSING  {p.name}")
        return None
    df = pd.read_csv(p, **kw)
    print(f"  {p.name:45s} {df.shape}")
    return df

print("Loading processed files:")

stress   = try_load(PROC / "county_monthly_stress_2017_2024.csv", parse_dates=["date"])
panel    = try_load(PROC / "county_monthly_panel_2017_2024.csv",  parse_dates=["month"])
ndvi     = try_load(PROC / "ndvi_counties_monthly_2017_2024.csv", parse_dates=["date"])
weekly   = try_load(PROC / "county_weekly_rainfall_2017_2024.csv")
chirps   = try_load(PROC / "chirps_counties_daily_2010_2024.csv", parse_dates=["date"])
calendar = try_load(META / "kenya_crop_calendar.csv")

# Rename NDVI county column so downstream joins always use 'county'
if ndvi is not None and "name" in ndvi.columns and "county" not in ndvi.columns:
    ndvi = ndvi.rename(columns={"name": "county"})
    print("  Renamed ndvi['name'] -> 'county'")

# Build month_start on any monthly dataset so joins are consistent
def add_month_start(df):
    if df is None:
        return None
    d = df.copy()
    if "month_start" not in d.columns:
        y = d["year"].astype(int).astype(str)
        m = d["month"].astype(int).astype(str).str.zfill(2)
        d["month_start"] = pd.to_datetime(y + "-" + m + "-01")
    return d

stress = add_month_start(stress)
ndvi   = add_month_start(ndvi)
panel  = add_month_start(panel) if panel is not None and {"year","month"}.issubset(panel.columns) else panel

print()
print("After month_start normalization:")
for name, df in [("stress", stress), ("ndvi", ndvi), ("panel", panel)]:
    if df is not None:
        print(f"  {name:8s} {df.shape}")
""")

md("""
## 3. Pipeline row-count trail

The audit that proves the pipeline is internally consistent from raw
CHIRPS files down to the master stress table.
""")

code("""
print("=== PIPELINE ROW COUNT TRAIL ===\\n")

if chirps is not None:
    n_days = chirps["date"].nunique()
    n_counties = chirps.shape[1] - 1
    print(f"CHIRPS daily           : {n_days:,} days x {n_counties} counties "
          f"= {n_days * n_counties:,} county-days")

if weekly is not None:
    print(f"Weekly rainfall        : {len(weekly):,} rows  "
          f"({weekly['county'].nunique()} counties, "
          f"{weekly['iso_year'].nunique()} years)")

if ndvi is not None:
    print(f"NDVI monthly           : {len(ndvi):,} rows  "
          f"({ndvi['county'].nunique()} counties)")

if panel is not None:
    print(f"Monthly panel          : {len(panel):,} rows")

if stress is not None:
    print(f"Stress master          : {len(stress):,} rows")
    print(f"  unique counties      : {stress['county'].nunique()}")
    print(f"  month range          : {stress['month_start'].min().date()} -> "
          f"{stress['month_start'].max().date()}")
    print(f"  stress columns       : {stress.columns.tolist()}")
""")

md("""
## 4. Duplicate key check

The master must be unique on `(county, month_start)`. If it is not,
the rest of the pipeline is silently broken.
""")

code("""
if stress is not None:
    dupes = stress.duplicated(subset=["county", "month_start"]).sum()
    print(f"Duplicate (county, month_start) rows in stress master: {dupes}")
    if dupes > 0:
        print("  INVESTIGATE - the master should be unique on that key")
    else:
        print("  OK - master is unique on (county, month_start)")
""")

md("""
## 5. Save the audit and commit

Monday's job ends here. Tuesday adds the crop calendar.
""")

code("""
audit_df = pd.DataFrame(JOIN_AUDIT) if JOIN_AUDIT else pd.DataFrame(
    columns=["join","left_rows","right_rows","type","keys",
             "result_rows","dropped","unmatched"])
audit_path = PROC / "stress_join_audit.csv"
audit_df.to_csv(audit_path, index=False)
print(f"Saved {audit_path.name} ({len(audit_df)} rows)")
print(audit_df)
""")

md("""
---

## Monday complete

Next (Tuesday): join the crop calendar on `(county, month_start)` to
add `crop_stage_weight` and `stress_weighted` columns.
""")

nb = {
    "cells": CELLS,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = Path("notebooks/03_integration.ipynb")
out.write_text(json.dumps(nb, indent=1))
print(f"Wrote {out}")
print(f"Cells: {len(CELLS)}  (markdown {sum(1 for c in CELLS if c['cell_type']=='markdown')}, "
      f"code {sum(1 for c in CELLS if c['cell_type']=='code')})")
