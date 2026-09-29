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

md("""
## NaN pattern in the weekly product (documented, not fixed)

The weekly product inherits NaN from two documented sources:

| Source | Affected | Reason | Prior decision |
|---|---|---|---|
| NDVI missing months | 260 county-months | Cloud cover, no clear-sky Sentinel-2 obs | D14 |
| Nairobi | 96 county-months | Urban county, no crop signal | D34 |

`stress_avg` is NaN whenever `ndvi_anomaly` is NaN, because the
composite formula requires both components. `stress_weighted` is
NaN whenever either `stress_avg` or `crop_stage_weight` is NaN.

**Decision: we do not interpolate either.** Interpolating NDVI would
fabricate a satellite observation that never happened. Interpolating
Nairobi would fabricate a crop that does not exist.

Aggregate NaN counts in the weekly product (19,599 rows):

- `latest_monthly_stress_avg`        1,129 NaN (~5.8%)
- `latest_monthly_stress_weighted`   1,480 NaN (~7.6%)
- `latest_monthly_ndvi_anomaly`      1,129 NaN (~5.8%)
- `latest_monthly_swvl1_anomaly`         0 NaN
- `latest_monthly_stress_category`       0 NaN  (categorical, default filled)
""")

nb["cells"] = CELLS
nb_path.write_text(json.dumps(nb, indent=1))
print(f"Added NaN documentation. Total cells: {len(CELLS)}")
