"""Generate the one-page PDF for outreach emails."""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = ROOT / "paper/figures/fig_31_vs_8_map.png"
OUT_DIR = ROOT / "paper/one_pager"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "Kenya_Climate_Data_Lab_One_Pager.pdf"

if not MAP_PATH.exists():
    raise SystemExit(f"Map not found: {MAP_PATH}")

# A4 landscape
fig = plt.figure(figsize=(11.69, 8.27), dpi=200)
fig.patch.set_facecolor("white")

# ---------- Header ----------
fig.text(0.05, 0.965,
         "Kenya Climate Data Lab",
         fontsize=22, fontweight="bold", color="#065f46",
         va="top")

fig.text(0.05, 0.915,
         "A county-level drought and vegetation stress monitor for all 47 Kenyan counties.",
         fontsize=12.5, color="#111827", va="top")

fig.text(0.05, 0.885,
         "Open source · Built in public · No calibration required",
         fontsize=10, color="#6b7280", style="italic", va="top")

# ---------- Map (tighter vertical bounds so no gap) ----------
ax = fig.add_axes([0.05, 0.32, 0.90, 0.54])
ax.axis("off")
img = mpimg.imread(MAP_PATH)
ax.imshow(img)

# ---------- Bottom left: the numbers ----------
# Row 1: 31
fig.text(0.05, 0.215, "31",
         fontsize=38, fontweight="bold", color="#dc2626",
         va="center", ha="left")
fig.text(0.118, 0.218, "counties had severe drought",
         fontsize=12, color="#374151", va="center", ha="left")

# Row 2: 8
fig.text(0.05, 0.115, "8",
         fontsize=38, fontweight="bold", color="#065f46",
         va="center", ha="left")
fig.text(0.082, 0.118, "had it while maize was growing",
         fontsize=12, color="#374151", va="center", ha="left")

# ---------- Bottom right: the ask ----------
fig.text(0.55, 0.215,
         "I am asking for 20 minutes.",
         fontsize=14, fontweight="bold", color="#065f46", va="center")

fig.text(0.55, 0.158,
         "Alex Haro Nyandega  ·  16 years old  ·  Nairobi",
         fontsize=10, color="#374151", va="center")

fig.text(0.55, 0.128,
         "alexharonyandega@gmail.com",
         fontsize=10, color="#374151", va="center")

fig.text(0.55, 0.098,
         "github.com/alexharonyandega-dev/kenya-climate-data-lab",
         fontsize=9, color="#6b7280", va="center")

# ---------- Footer ----------
fig.text(0.05, 0.025,
         "Data: CHIRPS rainfall · Sentinel-2 NDVI · ERA5-Land soil moisture   |   "
         "Method: composite stress index, weighted by maize growth stage",
         fontsize=8, color="#9ca3af", va="center")

plt.savefig(OUT, format="pdf", bbox_inches="tight", facecolor="white")
print(f"Saved: {OUT}")
