"""Add IQR-based outlier flags to the master stress table.

Per DECISIONS_LOG D05 (plan compatibility): outliers are flagged, not
removed. Extreme rainfall and vegetation are often real events (droughts,
floods) that the model must see.

Adds four boolean columns to county_monthly_stress_2017_2024.csv:
  - rainfall_mm_is_outlier
  - ndvi_is_outlier
  - stress_avg_is_outlier
  - stress_min_is_outlier

Rule: 1.5 x IQR above Q3 or below Q1.
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "processed" / "county_monthly_stress_2017_2024.csv"

print(f"Loading {MASTER.name}...")
df = pd.read_csv(MASTER)
print(f"  Shape: {df.shape}")

FLAG_COLUMNS = ["rainfall_mm", "ndvi", "stress_avg", "stress_min"]


def iqr_bounds(s):
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


print("\nApplying IQR flags:")
for col in FLAG_COLUMNS:
    if col not in df.columns:
        print(f"  SKIP {col}: not in master")
        continue

    lo, hi = iqr_bounds(df[col].dropna())
    flag_col = f"{col}_is_outlier"

    # Use pd.Series of booleans, NaN values get False
    mask = (df[col] < lo) | (df[col] > hi)
    df[flag_col] = mask.fillna(False).astype(bool)

    n_flagged = int(df[flag_col].sum())
    pct = 100 * n_flagged / len(df)
    print(f"  {col:14s} bounds=({lo:>8.2f}, {hi:>8.2f})  "
          f"flagged={n_flagged:>4d} ({pct:>5.1f}%)")

# Any month flagged by any column?
any_flag = df[[f"{c}_is_outlier" for c in FLAG_COLUMNS]].any(axis=1)
n_any = int(any_flag.sum())
print(f"\nRows flagged by at least one column: {n_any} ({100*n_any/len(df):.1f}%)")

# Save back to the same file (additive change, existing columns preserved)
df.to_csv(MASTER, index=False)
print(f"\nWrote {MASTER.name}: {df.shape}")

print("\nSample flagged rows (rainfall_mm_is_outlier=True):")
sample = df[df["rainfall_mm_is_outlier"]][
    ["county", "year", "month", "rainfall_mm", "ndvi", "stress_avg"]
].head(10)
print(sample.to_string(index=False))
