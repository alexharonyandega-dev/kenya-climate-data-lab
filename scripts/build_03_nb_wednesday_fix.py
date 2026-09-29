import json
from pathlib import Path

nb_path = Path("notebooks/03_integration.ipynb")
nb = json.loads(nb_path.read_text())
CELLS = nb["cells"]

# Find and fix the wrong comment in the lead-lag cell
for cell in CELLS:
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell["source"])
    if "negative lag = swvl1 leads NDVI" in src:
        src = src.replace(
            'print("  negative lag = swvl1 leads NDVI by N months")',
            'print("  POSITIVE lag = swvl1 leads NDVI by N months")'
        )
        lines = src.split("\n")
        cell["source"] = [l + "\n" for l in lines[:-1]] + [lines[-1]]
        print("Fixed comment in lead-lag cell.")

# Append interpretation markdown at end of the notebook (before final audit cell if possible)
def md(text):
    lines = text.strip("\n").split("\n")
    src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
    CELLS.append({"cell_type": "markdown", "metadata": {}, "source": src,
                  "id": f"md-{len(CELLS)}"})

md("""
## Lead-lag interpretation (D35 result)

Positive lag = soil moisture leads NDVI by that many months.

| lag | r | meaning |
|---|---|---|
| -4 | 0.084 | NDVI leads swvl1 by 4 months (weak) |
| -2 | 0.175 | NDVI leads swvl1 by 2 months (weak) |
| 0 | 0.364 | Contemporaneous |
| **+1** | **0.461** | **swvl1 leads NDVI by 1 month (strongest)** |
| +2 | 0.372 | swvl1 leads by 2 months |
| +4 | 0.272 | swvl1 leads by 4 months |

**Result: soil moisture anomaly leads vegetation anomaly by one month
(r = 0.461, p = 2e-220, n = 4205).**

This is consistent with the physical mechanism of drought: soil dries
first, vegetation follows. The lead is modest (1 month) but the effect
is statistically overwhelming.

**Operational consequence:** `swvl1_mean_anomaly` becomes the earliest
signal in the weekly product. A county whose soil moisture collapsed
this month is likely to show vegetation stress next month.
""")

nb["cells"] = CELLS
nb_path.write_text(json.dumps(nb, indent=1))
print(f"Notebook now has {len(CELLS)} cells")
