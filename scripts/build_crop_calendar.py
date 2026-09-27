"""Build county-level crop calendar for maize in Kenya.

Classifies each of Kenya's 47 counties into an agro-ecological zone,
with the seasons that matter for maize and the months of each season.

Sources:
- FAO GIEWS crop calendar for Kenya
- Kenya Agricultural and Livestock Research Organization (KALRO) zone maps
- FEWS NET Kenya livelihood zone descriptions
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "metadata" / "kenya_crop_calendar.csv"

# Zone definitions: (zone, seasons_active, long_rains_months, short_rains_months)
ZONES = {
    "highland_west": {
        "description": "Western highlands, bimodal, both seasons significant",
        "seasons": ["long_rains", "short_rains"],
        "long_rains": (3, 5),    # March - May
        "short_rains": (10, 12), # October - December
        "primary_harvest_month": 9,  # Sep for long rains crop
    },
    "rift_valley": {
        "description": "Rift Valley and North Rift, unimodal long rains",
        "seasons": ["long_rains"],
        "long_rains": (3, 8),    # March - August (extended)
        "short_rains": None,
        "primary_harvest_month": 10,
    },
    "central_highlands": {
        "description": "Central highlands, bimodal",
        "seasons": ["long_rains", "short_rains"],
        "long_rains": (3, 5),
        "short_rains": (10, 12),
        "primary_harvest_month": 9,
    },
    "eastern": {
        "description": "Eastern and southeastern, short rains dominant",
        "seasons": ["short_rains"],
        "long_rains": None,
        "short_rains": (10, 12),
        "primary_harvest_month": 2,  # Feb of following year
    },
    "coastal": {
        "description": "Coastal strip, long rains primary",
        "seasons": ["long_rains", "short_rains"],
        "long_rains": (4, 6),
        "short_rains": (10, 12),
        "primary_harvest_month": 8,
    },
    "asal_north": {
        "description": "Arid and semi-arid north, short rains only, unreliable",
        "seasons": ["short_rains"],
        "long_rains": None,
        "short_rains": (10, 12),
        "primary_harvest_month": 1,  # Jan following year (if at all)
    },
    "urban": {
        "description": "Urban, negligible maize production",
        "seasons": [],
        "long_rains": None,
        "short_rains": None,
        "primary_harvest_month": None,
    },
}

# County -> zone mapping (all 47 counties)
COUNTY_ZONE = {
    # Highland West
    "Kakamega": "highland_west",
    "Bungoma": "highland_west",
    "Busia": "highland_west",
    "Vihiga": "highland_west",
    "Kisii": "highland_west",
    "Nyamira": "highland_west",
    "Kisumu": "highland_west",
    "Siaya": "highland_west",
    "Homa Bay": "highland_west",
    "Migori": "highland_west",
    "Nandi": "highland_west",
    "Kericho": "highland_west",
    "Bomet": "highland_west",
    "Narok": "highland_west",

    # Rift Valley / North Rift
    "Trans Nzoia": "rift_valley",
    "Uasin Gishu": "rift_valley",
    "Nakuru": "rift_valley",
    "Elgeyo-Marakwet": "rift_valley",
    "West Pokot": "rift_valley",
    "Baringo": "rift_valley",
    "Laikipia": "rift_valley",

    # Central Highlands
    "Nyeri": "central_highlands",
    "Murang'a": "central_highlands",
    "Kiambu": "central_highlands",
    "Kirinyaga": "central_highlands",
    "Embu": "central_highlands",
    "Meru": "central_highlands",
    "Tharaka": "central_highlands",
    "Nyandarua": "central_highlands",

    # Eastern
    "Machakos": "eastern",
    "Makueni": "eastern",
    "Kitui": "eastern",
    "Kajiado": "eastern",

    # Coastal
    "Mombasa": "coastal",
    "Kwale": "coastal",
    "Kilifi": "coastal",
    "Lamu": "coastal",
    "Tana River": "coastal",
    "Taita Taveta": "coastal",

    # ASAL North
    "Turkana": "asal_north",
    "Marsabit": "asal_north",
    "Mandera": "asal_north",
    "Wajir": "asal_north",
    "Garissa": "asal_north",
    "Isiolo": "asal_north",
    "Samburu": "asal_north",

    # Urban
    "Nairobi": "urban",
}

rows = []
for county, zone_key in COUNTY_ZONE.items():
    z = ZONES[zone_key]
    rows.append({
        "county": county,
        "zone": zone_key,
        "zone_description": z["description"],
        "n_seasons": len(z["seasons"]),
        "long_rains_start": z["long_rains"][0] if z["long_rains"] else None,
        "long_rains_end": z["long_rains"][1] if z["long_rains"] else None,
        "short_rains_start": z["short_rains"][0] if z["short_rains"] else None,
        "short_rains_end": z["short_rains"][1] if z["short_rains"] else None,
        "primary_harvest_month": z["primary_harvest_month"],
    })

df = pd.DataFrame(rows)
df.to_csv(OUT, index=False)
print(f"Wrote {OUT}")
print(f"  Counties: {len(df)}")
print()
print("Zone distribution:")
print(df["zone"].value_counts().to_string())
print()
print("Sample rows:")
print(df.head(10).to_string(index=False))
