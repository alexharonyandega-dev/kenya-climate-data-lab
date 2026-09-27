"""National monthly anomalies: rainfall vs NDVI, 2017-2024.

Shows that rainfall and vegetation track together most years, but diverge
sharply in 2021-2022 — 2021 rainfall was worse, 2022 vegetation was worse.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PANEL = ROOT / "data" / "processed" / "county_monthly_panel_2017_2024.csv"
FIG = ROOT / "paper" / "figures" / "fig_rainfall_ndvi_divergence.png"

df = pd.read_csv(PANEL)
df["date"] = pd.to_datetime(df["date"])

# National monthly mean of anomalies
nat = df.groupby("date").agg(
    rain=("rainfall_anomaly", "mean"),
    ndvi=("ndvi_anomaly", "mean"),
).reset_index()

# 3-month rolling for smoothness
nat["rain_smooth"] = nat["rain"].rolling(3, center=True, min_periods=2).mean()
nat["ndvi_smooth"] = nat["ndvi"].rolling(3, center=True, min_periods=2).mean()

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(nat["date"], nat["rain_smooth"], color="#2563eb",
        linewidth=2, label="Rainfall anomaly (3-month smoothed)")
ax.plot(nat["date"], nat["ndvi_smooth"], color="#16a34a",
        linewidth=2, label="NDVI anomaly (3-month smoothed)")

ax.axhline(0, color="black", linewidth=1, linestyle="-", alpha=0.5)

# Shade the 2021-2022 drought period
ax.axvspan(pd.Timestamp("2021-01-01"), pd.Timestamp("2022-12-31"),
           color="#ef4444", alpha=0.1, zorder=0)
ax.text(pd.Timestamp("2021-07-01"), -2.4,
        "2021–22 drought\n(5 failed rainy seasons)",
        fontsize=11, weight="bold", color="#991b1b",
        ha="center",
        bbox=dict(boxstyle="round,pad=0.4",
                  facecolor="white", edgecolor="#991b1b"))

# Annotate the surprise
ax.annotate("2021: rainfall lowest\nbut crops OK",
            xy=(pd.Timestamp("2021-10-01"), -1.2),
            xytext=(pd.Timestamp("2020-02-01"), -2.0),
            fontsize=10, color="#1e40af", ha="center",
            arrowprops=dict(arrowstyle="->", color="#1e40af", lw=1.5))

ax.annotate("2022: crops collapse\ndespite less-bad rainfall",
            xy=(pd.Timestamp("2022-10-01"), -1.0),
            xytext=(pd.Timestamp("2023-04-01"), -2.2),
            fontsize=10, color="#166534", ha="center",
            arrowprops=dict(arrowstyle="->", color="#166534", lw=1.5))

ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Anomaly (z-score vs same-month climatology)", fontsize=12)
ax.set_title("Why vegetation matters more than rainfall alone",
             fontsize=15, weight="bold", pad=15)

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.legend(loc="lower left", fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.2)

ax.set_ylim(-2.8, 1.5)

plt.tight_layout()
plt.savefig(FIG, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {FIG}")
