"""Nakuru county: rainfall and NDVI anomalies, monthly, 2017-2024.

Single-county close-up. Shows the drought building and breaking over
one specific place, not the whole country.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PANEL = ROOT / "data" / "processed" / "county_monthly_panel_2017_2024.csv"
FIG = ROOT / "paper" / "figures" / "fig_nakuru_story.png"

df = pd.read_csv(PANEL)
df["date"] = pd.to_datetime(df["date"])
nak = df[df["county"] == "Nakuru"].sort_values("date").copy()

fig, ax = plt.subplots(figsize=(14, 6))

# Bars for rainfall anomaly
colors_rain = ["#1e40af" if v >= 0 else "#dc2626" for v in nak["rainfall_anomaly"]]
ax.bar(nak["date"], nak["rainfall_anomaly"], width=25,
       color=colors_rain, alpha=0.4, label="Rainfall anomaly")

# Line for NDVI anomaly
ax.plot(nak["date"], nak["ndvi_anomaly"], color="#16a34a",
        linewidth=2.5, marker="o", markersize=3,
        label="NDVI anomaly (vegetation health)")

ax.axhline(0, color="black", linewidth=1)

# Highlight 2022
ax.axvspan(pd.Timestamp("2022-01-01"), pd.Timestamp("2022-12-31"),
           color="#facc15", alpha=0.15, zorder=0)
ax.text(pd.Timestamp("2022-07-01"), 2.6, "2022",
        fontsize=14, weight="bold", color="#a16207",
        ha="center")

ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Anomaly (z-score)", fontsize=12)
ax.set_title("Nakuru County — five years of rainfall and vegetation",
             fontsize=15, weight="bold", pad=15)

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.legend(loc="upper left", fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.2)

ax.set_ylim(-2.6, 3.0)

plt.tight_layout()
plt.savefig(FIG, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {FIG}")
