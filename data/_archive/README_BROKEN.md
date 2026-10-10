# merged_dataset_v1_BROKEN.csv — DO NOT USE

This file contains a **Cartesian join bug**: national-level Kaggle yield
data was broadcast across all 47 counties without a county key, so every
county has the same yield_t_ha value (4.58 t/ha) for the same years
(2009–2013).

**Symptom:** identical yield for every county. 
**Cause:** `build_merged_yield_sidecar.py` merges on `year` only. 
**Fix:** use KNBS county-level data (see rebuilt version). 
**Date discovered:** 2026-09-30. 
**Affected findings:** none — this file was never used in the stress pipeline.

**See:** `docs/DECISIONS_LOG.md` D39.
