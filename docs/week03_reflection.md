# Week 03 Reflection - The Pivot Week

This week did not go as planned. That's the point.

## What I set out to do

Week 3 was supposed to be "clean the raw data": standardise dates, apply
missing-value rules, flag outliers, aggregate the 5,449 CHIRPS files into
per-county rainfall, and save a merged_dataset_v1.csv. The plan estimated
12-16 hours across 7 days.

That work got done - but in a completely different shape.

## What actually happened

On Monday morning, a researcher I had emailed read my project plan and
wrote back with detailed feedback. His name is Mark. His central point:
existing tools already cover yield prediction reasonably well, but nothing
public gives fast, county-level, real-time updates for all 47 Kenyan
counties. The gap isn't in modelling - it's in monitoring.

By Monday evening I had:
- Deleted the 5-county scope and expanded to 47
- Pivoted from annual yield prediction to monthly stress monitoring
- Registered Google Earth Engine
- Extracted CHIRPS daily rainfall for all 47 counties (5,479 days, 3.1 min)
- Extracted Sentinel-2 NDVI for all 47 counties (96 months)
- Built the composite stress index and validated it against the 2022 drought
- Generated six figures, including the October 2019-2024 stress series

That's the whole technical core of the project. In one day.

## The most important thing I learned

The 2021-2022 Horn of Africa drought was the worst in 40 years. Five
consecutive failed rainy seasons. My tool detected it without any
calibration - purely by comparing each county-month to its own historical
average for that calendar month.

But here's the detail I didn't expect: when I looked at rainfall anomalies
alone, the driest year in the record wasn't 2022 - it was 2021. Rainfall
in 2021 was further below normal.

2021 crops survived. 2022 crops died.

The reason is drought accumulation. By 2022, Kenya had experienced five
failed seasons in a row. Soil moisture reserves were exhausted. Even the
partial rain that fell couldn't revive the vegetation - the roots had
nothing to draw on.

This is why I weight NDVI at 65% in the composite stress index and rainfall
at only 35%. Vegetation integrates the accumulated damage from prior
months. Rainfall only tells you what fell in one.

## The surprising thing about scope

Expanding from 5 counties to 47 made the project easier, not harder.

I had been assuming that "fewer counties = simpler". But the 47-county
approach used the exact same pipeline, the exact same scripts, the exact
same processing time. The only difference was iterating over 47 polygons
instead of 5. Runtime went from an estimated 30 minutes for 5 counties to
3.1 minutes for 47 - because the bottleneck wasn't the number of counties,
it was the number of files (5,479 GeoTIFFs), and that number is fixed.

I had been optimising the wrong variable.

## What I learned about Kenya

Kenya has seven distinct agro-ecological zones for maize, not one:

- Western highlands (bimodal) - 14 counties
- Central highlands (bimodal) - 8
- Rift Valley (unimodal long rains) - 7
- Northern ASAL (short rains only) - 7
- Coastal (bimodal) - 6
- Eastern (short rains dominant) - 4
- Urban (Nairobi) - 1

Counties 200 km apart can have completely different growing calendars.
Trans Nzoia and Bungoma are both highland maize producers, but Trans Nzoia
only has one season and Bungoma has two. This changes what "normal October
rainfall" means for each.

## The most technically frustrating moment

Google Earth Engine's memory limit. My first NDVI script computed the mean
across 12 monthly composites for 47 polygons at 500m scale, and it crashed
with "User memory limit exceeded". Fix: drop the size() call, double the
resolution to 1000m. Simple fix, 20 minutes of iteration, but the exact
kind of dead-end you don't anticipate when planning.

The second-most frustrating: discovering that GEE needed shapefiles, not
GeoJSON. So I built a shapefile from the GeoJSON, zipped the components,
and uploaded. That's three extra steps for a format question that shouldn't
matter.

## What's the weakest part of what I built?

The NDVI is monthly, not weekly. The rainfall is daily. So the monitor
runs on two tiers: fast weekly rainfall updates, richer monthly composites.
That's honest about what each data source can support - but it means the
"weekly stress monitor" is really a "weekly rainfall monitor with monthly
stress confirmation".

To do weekly NDVI, I'd need 96 months x 4 weeks = 384 GEE exports instead
of 96. Possible but heavy. Deferred to a later week.

## What I'd do differently

Nothing about the pivot itself. Mark's advice was right, and the one-day
execution showed it.

What I'd change: I would have registered for Google Earth Engine on day
one of the project, not on day ten. It's the single most important tool
for this kind of work, and I avoided it for two weeks because the signup
process looked complicated. It wasn't - fifteen minutes, no billing
required, non-commercial academic tier.

## The plan's original Week 3 checklist, reconciled

| Plan item | Status |
|---|---|
| 02_data_cleaning.ipynb re-runs clean | ✅ done |
| DECISIONS LOG with 10+ entries | ✅ 32 entries |
| County mapping dictionary works | ✅ 47 counties |
| All dates are ISO YYYY-MM-DD | ✅ implicit in pipeline |
| Sub-daily rainfall to monthly + seasonal | ✅ done |
| Missing-value policy applied | ✅ documented (D27) |
| IQR outlier flags added | ✅ done (D31) |
| CHIRPS per-county daily | ✅ 5,479 x 47 |
| ERA5 clipped + per-county | ✅ 9 variables x 35 years |
| FAOSTAT hg/ha to t/ha | ✅ done (D23) |
| Every cleaned file named *_v2_cleaned | 🟡 used descriptive names instead (D03) |
| data_dictionary.md complete | ✅ 345 lines, 7 files |
| merged_dataset_v1.csv built | ✅ sidecar (D32) |
| Metrics tracker updated | ✅ done |
| Reflection answered | ✅ this document |

The plan was written for a yield-prediction project. The project pivoted
on Monday. Everything worth keeping from the plan was kept; everything
built for a different project was adjusted.

## One paragraph

Week 3 was the week the project found its actual shape. It started as a
"clean the CSVs" week and became the week we built a working county-level
drought monitor for all 47 Kenyan counties, validated it against the worst
drought in forty years, and documented every design decision in a single
central reference. The plan was wrong about what needed doing; the project
is right about what got done.
