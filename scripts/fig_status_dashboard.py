"""Week 02 status dashboard — three numbers that describe the state of the project.

Shows what exists and what doesn't yet, which is more honest than a
list of accomplishments. The three zeros are a feature, not a bug —
Week 2 is exploration, not building.

Design:
  - Background #1B4332
  - Big numbers in yellow #FFD60A (Archivo Black if available)
  - Labels in #D8F3DC
  - Footer in muted mint
"""

from pathlib import Path

import matplotlib
matplotlib.rcParams['font.family'] = ['Archivo Black', 'Montserrat',
                                       'DejaVu Sans', 'sans-serif']

import matplotlib.pyplot as plt

# --- Paths ---
ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / 'paper' / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

# --- Palette ---
BG = '#1B4332'
NUMBER = '#FFD60A'
LABEL = '#FFFFFF'
FOOTER = '#95D5B2'

# --- Data ---
METRICS = [
    ('0',       'Cleaned tables\nin /processed'),
    ('5,449',   'Daily CHIRPS files\nuncompressed'),
    ('0',       'Lines of\nmodeling code'),
]

# --- Figure ---
fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis('off')

# --- Three columns ---
col_centers = [2.0, 6.0, 10.0]
top_y = 3.9
label_y = 2.7

for (number, label), cx in zip(METRICS, col_centers):
    ax.text(cx, top_y, number, fontsize=72, weight='bold',
            color=NUMBER, ha='center', va='center')
    ax.text(cx, label_y, label, fontsize=13,
            color=LABEL, ha='center', va='center', linespacing=1.4)

# --- Thin dividers between columns ---
ax.plot([4.0, 4.0], [1.8, 4.8], color=FOOTER, alpha=0.25, linewidth=1)
ax.plot([8.0, 8.0], [1.8, 4.8], color=FOOTER, alpha=0.25, linewidth=1)

# --- Header (subtle, upper-left) ---
ax.text(0.5, 5.6, 'S T A T U S', fontsize=10, weight='bold',
        color=FOOTER, ha='left', va='center', alpha=0.6)

# --- Footer ---
ax.text(6, 0.6, 'KENYA CLIMATE DATA LAB  ·  WEEK 02 / 72',
        fontsize=12, weight='bold', color=FOOTER,
        ha='center', va='center')

# --- Save ---
plt.tight_layout()
out = FIG_DIR / 'fig_status_week02.png'
plt.savefig(out, dpi=100, bbox_inches='tight', facecolor=BG)
print(f'Saved: {out}')
for number, label in METRICS:
    print(f'  {number:>6s}  {label.replace(chr(10), " ")}')
