import json
from pathlib import Path

nb_path = Path("notebooks/03_integration.ipynb")
nb = json.loads(nb_path.read_text())
CELLS = nb["cells"]

def md(text):
    lines = text.strip("\n").split("\n")
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    CELLS.append({"cell_type": "markdown", "metadata": {}, "source": src,
                  "id": f"md-{len(CELLS)}"})

def code(text):
    lines = text.strip("\n").split("\n")
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    CELLS.append({"cell_type": "code", "metadata": {}, "execution_count": None,
                  "outputs": [], "source": src, "id": f"code-{len(CELLS)}"})

md("""
# Thursday - Weekly stress product (D36)

A product a county officer can read *this week*.

Design principle: the weekly product is rainfall-led. Every monthly
signal is carried forward from the last confirmed month and prefixed
`latest_monthly_` so the reader always knows what is fresh and what
is the last confirmed reading.

We do not interpolate NDVI to weekly cadence. That would fabricate
signal the satellite did not see.
""")

code("""
# 1. Reload the weekly rainfall file (it has iso_year/iso_week, no date)
weekly = pd.read_csv(PROC / "county_weekly_rainfall_2017_2024.csv")
print("Weekly rainfall:", weekly.shape)
print("Columns:", weekly.columns.tolist())
print()
print(weekly.head())
""")

code("""
# 2. Reconstruct a calendar date from iso_year + iso_week (Monday of that week)
weekly = weekly.copy()
weekly["week_start"] = pd.to_datetime(
    weekly["iso_year"].astype(str) + "-" +
    weekly["iso_week"].astype(str).str.zfill(2) + "-1",
    format="%G-%V-%u",
)
weekly["month_start"] = weekly["week_start"].values.astype("datetime64[M]").astype("datetime64[ns]")

print("Sample with reconstructed dates:")
print(weekly[["iso_year","iso_week","county","week_start","month_start"]].head())
print()
print("Date range:", weekly["week_start"].min().date(), "->", weekly["week_start"].max().date())
""")

code("""
# 3. Build the monthly companion table (last confirmed readings)
monthly_companion = stress_v3[[
    "county", "month_start",
    "stress_avg", "stress_weighted", "stress_min", "stress_category",
    "crop_stage", "crop_stage_weight",
    "ndvi_anomaly", "swvl1_mean_anomaly",
    "t2m_mean_anomaly", "pev_mean_anomaly",
]].rename(columns={
    "stress_avg":         "latest_monthly_stress_avg",
    "stress_weighted":    "latest_monthly_stress_weighted",
    "stress_min":         "latest_monthly_stress_min",
    "stress_category":    "latest_monthly_stress_category",
    "crop_stage":         "latest_monthly_crop_stage",
    "crop_stage_weight":  "latest_monthly_crop_stage_weight",
    "ndvi_anomaly":       "latest_monthly_ndvi_anomaly",
    "swvl1_mean_anomaly": "latest_monthly_swvl1_anomaly",
    "t2m_mean_anomaly":   "latest_monthly_t2m_anomaly",
    "pev_mean_anomaly":   "latest_monthly_pev_anomaly",
})

print("Monthly companion:", monthly_companion.shape)
print("Columns:", monthly_companion.columns.tolist())
""")

code("""
# 4. Join weekly rainfall with monthly companions
weekly_stress = logged_join(
    weekly, monthly_companion,
    on=["county", "month_start"],
    how="left",
    label="J03_weekly_x_monthly",
    right_name="monthly_companion",
)

print()
print("weekly_stress shape:", weekly_stress.shape)
print("NaN in monthly companions (weeks whose month predates 2017-01 stress window):")
comp_cols = [c for c in weekly_stress.columns if c.startswith("latest_monthly_")]
print(weekly_stress[comp_cols].isna().sum())
""")

md("""
## Save the weekly product
""")

code("""
out = PROC / "county_weekly_stress_2017_2024.csv"
weekly_stress.to_csv(out, index=False)
print(f"Saved {out.name}: {weekly_stress.shape}")
print(f"Columns: {weekly_stress.columns.tolist()}")
""")

md("""
## Final audit save (re-run at end of notebook)
""")

code("""
audit_df_final = pd.DataFrame(JOIN_AUDIT)
audit_df_final.to_csv(PROC / "stress_join_audit.csv", index=False)
print(f"Saved stress_join_audit.csv ({len(audit_df_final)} rows)")
print(audit_df_final.to_string(index=False))
""")

nb["cells"] = CELLS
nb_path.write_text(json.dumps(nb, indent=1))
print(f"Wrote {nb_path} - now {len(CELLS)} cells total")
