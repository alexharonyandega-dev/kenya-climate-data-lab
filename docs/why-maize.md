# Why maize?

**Status:** Original problem statement, pre-pivot. Kept for history.
**See also:** `docs/architecture.md` for the current scope.

## The original question

Why did this project start with maize?

1. **Food security.** Maize is Kenya's staple. It accounts for roughly
   30% of calories consumed nationally and is the primary food crop in
   every agro-ecological zone where it can grow.

2. **Data richness.** More public data exists for maize than for any
   other Kenyan crop: FAOSTAT yield series back to 1961, KNBS county
   production reports, Kaggle Kenyan maize datasets, Mendeley
   experimental trials, and Zenodo push-pull farming system data.

3. **Policy relevance.** Maize is named in Kenya's Vision 2030 and in
   every National Agriculture Production Report. A tool that informs
   maize decisions has a direct line to policy.

4. **Alignment with global efforts.** Kenya is a priority country for
   FEWS NET, GEOGLAM, and FAO's Agricultural Stress Index. Any
   improvement to maize monitoring plugs into existing infrastructure.

## What changed

**Week 3 (2026-09-27):** After external advice from Mark, the project
pivoted from predicting maize yield for 5 counties to monitoring
drought and vegetation stress for all 47 counties.

**Why the pivot:** Yield prediction is well covered by existing tools.
The gap is real-time, county-level monitoring. The tool became a
monitor, not a predictor.

**What survived:** Maize remains the crop of interest. The crop
calendar in `data/metadata/kenya_crop_calendar.csv` weights stress
by maize growth stage. The validation target (Week 5+) is still
maize yield.

See `docs/DECISIONS_LOG.md` D01–D02 for the full pivot rationale.
