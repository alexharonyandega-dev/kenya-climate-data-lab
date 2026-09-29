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
# Tuesday - Crop calendar integration (D34)

Add `crop_stage_weight` per `(county, month)`, then `stress_weighted`.

The weight answers: *if this month is dry, how much does it hurt?*

- 1.0 during planting / vegetative / flowering
- 0.7 during grain fill
- 0.3 during primary harvest month
- 0.0 during fallow
- NaN for urban (Nairobi)

Source: `data/metadata/kenya_crop_calendar.csv`
""")

code("""
# 1. Expand crop calendar to (county, month_num) with stage label + weight

STAGE_WEIGHT = {
    "planting":      1.0,
    "vegetative":    1.0,
    "grain_fill":    0.7,
    "harvest":       0.3,
    "fallow":        0.0,
}

def months_in_range(start, end):
    \"\"\"Inclusive integer month range, wrapping across year boundary.\"\"\"
    start, end = int(start), int(end)
    if start <= end:
        return list(range(start, end + 1))
    return list(range(start, 13)) + list(range(1, end + 1))

def build_weights(cal):
    rows = []
    for _, r in cal.iterrows():
        county = r["county"]
        harvest = int(r["primary_harvest_month"]) if pd.notna(r["primary_harvest_month"]) else None
        seasons = []
        if r["n_seasons"] >= 1 and pd.notna(r["long_rains_start"]):
            seasons.append(("long", r["long_rains_start"], r["long_rains_end"]))
        if r["n_seasons"] >= 2 and pd.notna(r["short_rains_start"]):
            seasons.append(("short", r["short_rains_start"], r["short_rains_end"]))

        # Per-month label for this county
        for m in range(1, 13):
            label = "fallow"
            for _name, s, e in seasons:
                in_season = months_in_range(s, e)
                if m in in_season:
                    # Split the season: first half = planting/vegetative, second half = grain fill
                    pos = in_season.index(m)
                    if pos < len(in_season) // 2:
                        label = "planting"
                    else:
                        label = "grain_fill"
                    break
            if harvest is not None and m == harvest:
                label = "harvest"
            rows.append({
                "county": county,
                "month_num": m,
                "crop_stage": label,
                "crop_stage_weight": STAGE_WEIGHT[label],
            })

    w = pd.DataFrame(rows)
    # Nairobi is urban: NaN
    w.loc[w["county"] == "Nairobi", "crop_stage_weight"] = np.nan
    return w

calendar_weights = build_weights(calendar)
print("Calendar weights built:", calendar_weights.shape)
print(calendar_weights.head(15))
print()
print("Weight distribution:")
print(calendar_weights["crop_stage"].value_counts())
""")

code("""
# 2. Add month_num to stress for the join
stress = stress.copy()
stress["month_num"] = pd.to_datetime(stress["month_start"]).dt.month

# 3. Join weights onto stress
stress_v2 = logged_join(
    stress,
    calendar_weights,
    on=["county", "month_num"],
    how="left",
    label="J01_calendar",
    right_name="calendar_weights",
)

# 4. Compute weighted stress
stress_v2["stress_weighted"] = stress_v2["stress_avg"] * stress_v2["crop_stage_weight"]

print()
print("stress_v2 shape:", stress_v2.shape)
print("New columns added: crop_stage, crop_stage_weight, stress_weighted")
print()
print("Sample (Trans Nzoia, Oct 2022 vs Oct 2021):")
sample = stress_v2[(stress_v2["county"] == "Trans Nzoia") &
                   (stress_v2["month_num"] == 10) &
                   (stress_v2["year"].isin([2021, 2022]))]
print(sample[["county","year","month","crop_stage","crop_stage_weight",
              "stress_avg","stress_weighted"]].to_string(index=False))
""")

code("""
# 5. Sanity: how many rows lost crop_stage_weight?
missing_w = stress_v2["crop_stage_weight"].isna().sum()
print(f"Rows with NaN crop_stage_weight: {missing_w}")
if missing_w > 0:
    print("  Affected counties:")
    print(stress_v2[stress_v2["crop_stage_weight"].isna()]["county"].value_counts())
""")

md("""
## Save the enhanced master
""")

code("""
out = PROC / "county_monthly_stress_v2.csv"
stress_v2.to_csv(out, index=False)
print(f"Saved {out.name}: {stress_v2.shape}")
print(f"Columns: {stress_v2.columns.tolist()}")
""")

nb["cells"] = CELLS
nb_path.write_text(json.dumps(nb, indent=1))
print(f"Wrote {nb_path} — now {len(CELLS)} cells total")
