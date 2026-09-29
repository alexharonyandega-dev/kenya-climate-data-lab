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
## Final audit save (runs after all joins)

The Monday audit save cell runs before Tuesday/Wednesday joins are
performed, so it always shows 0 rows on the first pass. This cell
re-saves the audit *after* every join in the notebook has executed.
""")

code("""
audit_df_final = pd.DataFrame(JOIN_AUDIT)
audit_df_final.to_csv(PROC / "stress_join_audit.csv", index=False)
print(f"Saved stress_join_audit.csv ({len(audit_df_final)} rows)")
print(audit_df_final.to_string(index=False))
""")

nb["cells"] = CELLS
nb_path.write_text(json.dumps(nb, indent=1))
print(f"Appended audit fix. Total cells: {len(CELLS)}")
