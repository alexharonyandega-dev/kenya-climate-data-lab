# Week 03 Reflection — 2026-09-27

## 1. What was the biggest surprise this week?

The pivot itself. I planned to build an annual yield predictor for 5 counties.
An external advisor read my plan and pointed out that existing tools already
cover annual yield reasonably well — what's missing is real-time county-level
monitoring. That reframing changed the scope from 5 counties to 47, from annual
to monthly, from yield prediction to stress detection.

The surprise wasn't that I was wrong. It's that the new approach is genuinely
more useful and also easier to build. The whole pivot took one day.

## 2. What did the 2022 drought look like in the data?

In October 2022, the composite stress index showed severe stress in 10
counties and moderate stress in 37 — 47 out of 47 counties were stressed.

But the more interesting finding: the rainfall anomaly was worse in 2021
than in 2022. It was the vegetation (NDVI) that collapsed in 2022. The reason
is drought accumulation — five consecutive failed rainy seasons had drained
the soil moisture. Rainfall told one story, vegetation told another, and the
second one was more accurate.

That's a real lesson about multi-signal monitoring.

## 3. What was technically hardest?

Getting Google Earth Engine to accept our county boundaries. GEE expects
shapefiles, and our GeoJSON file needed conversion. Also the first NDVI
script hit a "User memory limit exceeded" because we tried to compute
collection.size() on 12 monthly means across 47 polygons at 500m scale.
Fixed by removing the size() call and doubling the scale to 1000m.

Small details — but each one cost 20 minutes of iteration.

## 4. What is the weakest part of what we built?

The NDVI is monthly, not weekly. The rainfall is daily. So we have a two-tier
system: fast weekly rainfall updates, richer monthly composites. That's
honest but not ideal — a real operational system would have weekly NDVI.

Doing weekly NDVI means reprocessing 96 months x 4 weeks = 384 GEE exports
instead of 96. Possible but heavy. Deferred.

## 5. What did I learn about Kenya that I didn't know before?

Kenya has seven distinct agro-ecological zones for maize:
- Western highlands (bimodal) — 14 counties
- Central highlands (bimodal) — 8
- Rift Valley (unimodal long rains) — 7
- Northern ASAL (short rains only) — 7
- Coastal (bimodal) — 6
- Eastern (short rains dominant) — 4
- Urban (Nairobi) — 1

I knew Kenya had two rainy seasons in most places. I didn't know how
fragmented the actual growing zones were. Counties 200 km apart can
have completely different growing calendars.

## 6. One paragraph summary

Three weeks in, Kenya Climate Data Lab has pivoted from a yield predictor
to a county-level drought monitor. It uses CHIRPS rainfall and Sentinel-2
NDVI to compute monthly stress anomalies across all 47 counties from 2017
to 2024. The tool correctly identifies the 2022 Horn of Africa drought
without any calibration — purely from comparing each month to its historical
average. Next: weekly resolution, a public dashboard, and continued
crop-calendar-aware monitoring.
