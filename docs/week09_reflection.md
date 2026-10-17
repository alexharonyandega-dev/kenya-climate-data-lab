# Week 9 Reflection

**Week:** 9 of 72
**Plan date:** 2026-11-16 (executed 2026-10-17)
**Theme:** Build the Public Drought Monitor Dashboard (5 Sheets)

---

## 1. Which sheet tells the strongest story?

The Lead-lag Curve. 

Visually, it's just a scatter plot with a line through it. But it represents the core scientific contribution of this project. It shows 4,252 individual months of data, proving that soil moisture drops *before* vegetation dies. 

A reader doesn't need to understand standard deviations or the CHIRPS data pipeline to look at that chart and understand: "When the soil dries up, the plants suffer a month later."

## 2. Which is most likely to be misunderstood?

The KPI Card. 

It just says "10 Severe Counties" in big bold text. Without context, a reader might think "Only 10? That's not too bad." 

It requires the title ("October 2022") and the context of the map (which is glowing red in the north) to understand that those 10 counties were specifically flagged during the maize growing season, representing a massive localized crop failure. 

## 3. What was the biggest technical hurdle?

Tableau's geocoding database has no idea where Kenya's counties are.

I dragged the `County` field to the map, expecting a map of Kenya to appear. Instead, Tableau plotted zero marks. It knows "Kenya" as a country, and it knows "Nairobi" as a city, but it refuses to recognize "Turkana," "Kakamega," or "Kwale" as counties. 

**The fix:** If the software can't find the geography, you have to hand it the exact coordinates. I wrote a Python script (`scripts/build_county_centroids.py`) that read the GeoJSON of Kenya's boundaries, calculated the geometric center of every county polygon, and appended `centroid_lat` and `centroid_lon` to the master CSV. 

Once Tableau had explicit coordinates, the 47 dots appeared perfectly.

## 4. What did the pivot to Tableau Web Authoring cost?

I couldn't install the Desktop app because of macOS admin privileges. So I used Web Authoring.

**Cost:** Web Authoring is glitchy. It doesn't let you save a `.twbx` file locally easily. The UI for applying filters to a dashboard is incredibly frustrating.

**Benefit:** It forced the project to be cloud-native. The dashboard is now a public URL that I can drop into any email or LinkedIn post. A `.twbx` file would have been stuck on my hard drive.

## 5. Is the dashboard ready to be shared publicly?

Yes. 

It has 5 sheets, 3 filters, and reads cleanly on mobile. It tells the story of the 2022 drought without needing a tutorial. 

However, I need feedback. I published the dashboard and posted it to LinkedIn and Substack. The next step is to ask 2 of the Week 8 users to look at it and tell me what they click first.

## 6. State of the project

- **Data:** Solid. 4,512 rows, verified.
- **Code:** Reproducible. The centroid script ensures the dashboard can be rebuilt from scratch.
- **Dashboard:** Live. [Link](https://public.tableau.com/views/KenyaDroughtMonitorWeek9/DroughtMonitorDashboard)
- **Paper:** Draft complete (Abstract + Intro + Methods). Ready for review.

Week 10 is about publishing the dashboard officially and writing the 2-page insight paper.
