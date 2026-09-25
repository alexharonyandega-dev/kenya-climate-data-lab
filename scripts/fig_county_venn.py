"""Venn-style diagram: KNBS vs Zenodo county coverage.

Shows the single overlap (Kakamega) between the 5 KNBS counties and
the 8 Zenodo push-pull counties. Documents the Week 3 scope problem.

Design:
  - Background #1B4332 (dark forest green)
  - Left circle: #48CAE4 (sky blue) at 30% opacity
  - Right circle: #F9C74F (warm yellow) at 30% opacity
  - Text: #D8F3DC (pale mint)
"""

from pathlib import Path

import matplotlib
matplotlib.rcParams['font.family'] = ['Montserrat', 'DejaVu Sans', 'sans-serif']

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# --- Paths ---
ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / 'paper' / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

# --- Palette ---
BG = '#1B4332'
LEFT = '#48CAE4'
RIGHT = '#F9C74F'
TEXT = '#D8F3DC'

# --- Data ---
KNBS_COUNTIES = ['Nakuru', 'Kakamega', 'Bungoma', 'Trans Nzoia', 'Uasin Gishu']
ZENODO_COUNTIES = ['Homa Bay', 'Siaya', 'Vihiga', 'Kakamega',
                   'Migori', 'Kisumu', 'Narok', 'Busia']
KNBS_ONLY = [c for c in KNBS_COUNTIES if c not in ZENODO_COUNTIES]
ZENODO_ONLY = [c for c in ZENODO_COUNTIES if c not in KNBS_COUNTIES]
OVERLAP = [c for c in KNBS_COUNTIES if c in ZENODO_COUNTIES]

# --- Figure ---
fig, ax = plt.subplots(figsize=(12, 8), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')

# --- Circles ---
left_cx, right_cx = 4.6, 7.4
cy, r = 5.3, 2.4

ax.add_patch(Circle((left_cx, cy), r, facecolor=LEFT,
                    edgecolor='none', alpha=0.30, zorder=1))
ax.add_patch(Circle((right_cx, cy), r, facecolor=RIGHT,
                    edgecolor='none', alpha=0.30, zorder=1))
ax.add_patch(Circle((left_cx, cy), r, facecolor='none',
                    edgecolor=LEFT, linewidth=2.5, zorder=2))
ax.add_patch(Circle((right_cx, cy), r, facecolor='none',
                    edgecolor=RIGHT, linewidth=2.5, zorder=2))

# --- Circle labels ---
ax.text(left_cx - 1.0, cy + 0.9, 'KNBS', fontsize=24, weight='bold',
        color=TEXT, ha='center', va='center', zorder=3)
ax.text(left_cx - 1.0, cy + 0.2, '5 counties', fontsize=15,
        color=TEXT, ha='center', va='center', zorder=3)

ax.text(right_cx + 1.0, cy + 0.9, 'Zenodo', fontsize=24, weight='bold',
        color=TEXT, ha='center', va='center', zorder=3)
ax.text(right_cx + 1.0, cy + 0.2, '8 counties', fontsize=15,
        color=TEXT, ha='center', va='center', zorder=3)

# --- Overlap label ---
overlap_cx = (left_cx + right_cx) / 2
ax.text(overlap_cx, cy + 0.15, 'Kakamega', fontsize=15, weight='bold',
        color=TEXT, ha='center', va='center', zorder=3)
ax.text(overlap_cx, cy - 0.35, '1 county', fontsize=12,
        color=TEXT, ha='center', va='center', zorder=3)

# --- Title ---
ax.text(6, 7.5, 'County coverage overlap: KNBS vs Zenodo',
        fontsize=22, weight='bold', color=TEXT, ha='center', va='center')

# --- Bottom caption ---
ax.text(6, 1.35,
        'Only Kakamega appears in both datasets.',
        fontsize=14, color=TEXT, ha='center', va='center', style='italic')
ax.text(6, 0.95,
        'Week 3 scope decision: broaden to 12 counties, keep 5 and lose 86% of Zenodo, or pivot away from the Rift Valley.',
        fontsize=10, color=TEXT, ha='center', va='center', alpha=0.75)

# --- County lists ---
ax.text(2.0, 3.3, 'KNBS only', fontsize=11, weight='bold',
        color=TEXT, ha='center', va='center', alpha=0.85)
for i, c in enumerate(KNBS_ONLY):
    ax.text(2.0, 2.9 - i * 0.32, c, fontsize=10,
            color=TEXT, ha='center', va='center', alpha=0.75)

ax.text(10.0, 3.3, 'Zenodo only', fontsize=11, weight='bold',
        color=TEXT, ha='center', va='center', alpha=0.85)
for i, c in enumerate(ZENODO_ONLY):
    ax.text(10.0, 2.9 - i * 0.32, c, fontsize=10,
            color=TEXT, ha='center', va='center', alpha=0.75)

# --- Save ---
plt.tight_layout()
out = FIG_DIR / 'fig_county_venn.png'
plt.savefig(out, dpi=100, bbox_inches='tight', facecolor=BG)
print(f'Saved: {out}')
print(f'KNBS only:    {KNBS_ONLY}')
print(f'Zenodo only:  {ZENODO_ONLY}')
print(f'Overlap:      {OVERLAP}')
