"""Why is Kakamega an outlier? Look at its monthly stress profile in 2022."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"

stress = pd.read_csv(PROC / "county_monthly_stress_v3.csv", parse_dates=["month_start"])
s22 = stress[stress["month_start"].dt.year == 2022]

print("=== 2022 monthly stress, all 5 KNBS counties ===\n")
pivot = s22.pivot_table(
    index="county",
    columns=s22["month_start"].dt.month,
    values="stress_weighted",
).round(2)
print(pivot.loc[["Nakuru","Kakamega","Bungoma","Trans Nzoia","Uasin Gishu"]].to_string())
print()

print("=== 2022 monthly crop stage ===\n")
stage_pivot = s22.pivot_table(
    index="county",
    columns=s22["month_start"].dt.month,
    values="crop_stage_weight",
    aggfunc="first",
)
print(stage_pivot.loc[["Nakuru","Kakamega","Bungoma","Trans Nzoia","Uasin Gishu"]].to_string())
