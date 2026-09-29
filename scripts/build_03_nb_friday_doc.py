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
## Re-validation finding - two indices, two questions

The 2022 drought test produced the most important design finding of
Week 4:

| Index | 2022 severe counties | What it measures |
|---|---|---|
| `stress_avg` | 31 | Drought severity (any land use) |
| `stress_weighted` | 8 | Maize-crop damage specifically |

**Why the drop:** Most of Kenya's 2022 drought peaked when counties
were in harvest or fallow. Only 8 counties had maize in the ground
at peak stress. The other 23 lost pasture, water, and livestock —
but their maize was already harvested.

**Conclusion:** The two indices answer different questions.

- `stress_avg` = "how bad is the drought in this county?"
- `stress_weighted` = "how much does this drought hurt the maize crop?"

Both are legitimate. The tool now reports both. A county agriculture
officer reads `stress_weighted` (is my crop at risk?). A drought
response coordinator reads `stress_avg` (is the county in crisis?).

**Weighting never creates new severe flags.** No county triggers
severe under `stress_weighted` before triggering under `stress_avg`.
The weighting only ever suppresses false alarms. This is D34
working exactly as designed.
""")

nb["cells"] = CELLS
nb_path.write_text(json.dumps(nb, indent=1))
print(f"Added Friday interpretation. Total cells: {len(CELLS)}")
