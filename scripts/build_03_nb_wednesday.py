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
# Wednesday - ERA5 integration (D35)

Add four ERA5-Land anomalies as diagnostic columns:

- `swvl1_mean_anomaly`  - soil moisture 0-7 cm
- `swvl2_mean_anomaly`  - soil moisture 7-28 cm
- `t2m_mean_anomaly`    - 2m air temperature
- `pev_mean_anomaly`    - potential evaporation

Then test the central scientific question: does soil moisture lead
vegetation in the 2022 drought? A positive lead would prove why the
tool needs soil-moisture as an early-warning column.
""")

code("""
# 1. Load the four ERA5 variables we need
ERA5 = PROC / "era5_counties"

def load_era5(var):
    p = ERA5 / f"era5_{var}_counties_daily.csv"
    df = pd.read_csv(p, parse_dates=["date"])
    print(f"  {var:6s} {df.shape}  counties={df['county'].nunique()}")
    return df

print("Loading ERA5 county daily:")
swvl1 = load_era5("swvl1")
swvl2 = load_era5("swvl2")
t2m   = load_era5("t2m")
pev   = load_era5("pev")
""")

code("""
# 2. Aggregate daily -> monthly per county
def era5_to_monthly(df, var):
    d = df.copy()
    d["month_start"] = d["date"].values.astype("datetime64[M]").astype("datetime64[ns]")
    m = (d.groupby(["county", "month_start"], as_index=False)["value"]
           .mean()
           .rename(columns={"value": f"{var}_mean"}))
    return m

swvl1_m = era5_to_monthly(swvl1, "swvl1")
swvl2_m = era5_to_monthly(swvl2, "swvl2")
t2m_m   = era5_to_monthly(t2m,   "t2m")
pev_m   = era5_to_monthly(pev,   "pev")

print("Monthly aggregates:")
for name, df in [("swvl1",swvl1_m),("swvl2",swvl2_m),
                 ("t2m",t2m_m),("pev",pev_m)]:
    print(f"  {name:6s} {df.shape}")
""")

code("""
# 3. Compute anomalies per (county, month_num) vs own history
def add_anomaly(df, value_col):
    d = df.copy()
    d["month_num"] = pd.to_datetime(d["month_start"]).dt.month
    stats = (d.groupby(["county","month_num"])[value_col]
               .agg(["mean","std"]).reset_index()
               .rename(columns={"mean": f"{value_col}_clim_mean",
                                "std":  f"{value_col}_clim_std"}))
    d = d.merge(stats, on=["county","month_num"], how="left")
    d[f"{value_col}_anomaly"] = (
        (d[value_col] - d[f"{value_col}_clim_mean"])
        / d[f"{value_col}_clim_std"].replace(0, np.nan)
    )
    return d

swvl1_m = add_anomaly(swvl1_m, "swvl1_mean")
swvl2_m = add_anomaly(swvl2_m, "swvl2_mean")
t2m_m   = add_anomaly(t2m_m,   "t2m_mean")
pev_m   = add_anomaly(pev_m,   "pev_mean")

print("Anomalies computed. Sample swvl1:")
print(swvl1_m[["county","month_start","swvl1_mean","swvl1_mean_anomaly"]].head())
""")

code("""
# 4. Join the four anomaly columns onto stress_v2
era5_features = (swvl1_m[["county","month_start","swvl1_mean","swvl1_mean_anomaly"]]
    .merge(swvl2_m[["county","month_start","swvl2_mean_anomaly"]],
           on=["county","month_start"], how="outer")
    .merge(t2m_m[["county","month_start","t2m_mean_anomaly"]],
           on=["county","month_start"], how="outer")
    .merge(pev_m[["county","month_start","pev_mean_anomaly"]],
           on=["county","month_start"], how="outer")
)

stress_v3 = logged_join(
    stress_v2, era5_features,
    on=["county","month_start"],
    how="left",
    label="J02_era5",
    right_name="era5_features",
)

print()
print("stress_v3 shape:", stress_v3.shape)
print("New ERA5 columns added: swvl1_mean_anomaly, swvl2_mean_anomaly,")
print("                        t2m_mean_anomaly, pev_mean_anomaly")
print()
print("NaN check for ERA5 columns (should be 0 - all months covered 1990-2024):")
print(stress_v3[["swvl1_mean_anomaly","swvl2_mean_anomaly",
                 "t2m_mean_anomaly","pev_mean_anomaly"]].isna().sum())
""")

code("""
# 5. Does soil moisture LEAD vegetation? Lead-lag correlation, 2017-2024
from scipy.stats import pearsonr

work = stress_v3.dropna(subset=["swvl1_mean_anomaly","ndvi_anomaly"]).copy()
work = work.sort_values(["county","month_start"])

def corr_at_lag(lag):
    if lag == 0:
        a = work["swvl1_mean_anomaly"]
        b = work["ndvi_anomaly"]
        mask = a.notna() & b.notna()
    else:
        a = work.groupby("county")["swvl1_mean_anomaly"].shift(lag)
        b = work["ndvi_anomaly"]
        mask = a.notna() & b.notna()
    r, p = pearsonr(a[mask], b[mask])
    return r, p, int(mask.sum())

print("Lead-lag: soil moisture (swvl1) vs NDVI")
print("  negative lag = swvl1 leads NDVI by N months")
print()
print(f"{'lag':>5s}  {'r':>8s}  {'p':>10s}  {'n':>6s}")
for lag in [-4,-3,-2,-1,0,1,2,3,4]:
    r, p, n = corr_at_lag(lag)
    marker = " <-- strongest" if False else ""
    print(f"{lag:>5d}  {r:>8.3f}  {p:>10.2e}  {n:>6d}")
""")

md("""
## Save the enhanced master
""")

code("""
out = PROC / "county_monthly_stress_v3.csv"
stress_v3.to_csv(out, index=False)
print(f"Saved {out.name}: {stress_v3.shape}")
print(f"Columns: {stress_v3.columns.tolist()}")
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
print(f"Wrote {nb_path} — now {len(CELLS)} cells total")
