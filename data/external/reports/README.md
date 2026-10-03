# External Reports — Index

PDFs and documentation downloaded from the Kenya Climate & Nature
Directory and related official sources. Used for independent
validation of the drought monitor's signal.

All files downloaded 2026-10-03. Sources documented in
`data/metadata/sources.md` sections 11–15.

---

## `ccrp/` — County Climate Risk Profiles

Eight profiles from the Ministry of Agriculture and Livestock
Development / CGIAR. Each covers a single county: vulnerability
index, historical rainfall trends (1985–2015), projected changes
(2021–2065), drought hazard assessments.

| File | County | Vintage |
|---|---|---|
| `CCRP_Bomet_2018.pdf` | Bomet | 2018 |
| `CCRP_Busia_2016.pdf` | Busia | 2016 |
| `CCRP_HomaBay_2016.pdf` | Homa Bay | 2016 |
| `CCRP_Kericho_2018.pdf` | Kericho | 2018 |
| `CCRP_Kilifi_2016.pdf` | Kilifi | 2016 |
| `CCRP_Laikipia_2018.pdf` | Laikipia | 2018 |
| `CCRP_Nandi_2021.pdf` | Nandi | 2021 |
| `CCRP_Nyamira_2021.pdf` | Nyamira | 2021 |

**Extracted values:** `CCRP_Summary.md` — vulnerability indices for
the 3 counties that publish a numeric index (Bomet 0.473, Kericho
0.448, Laikipia 0.3841). The other 5 use different methodologies
across report vintages.

---

## `kmd/` — Kenya Meteorological Department

**`KMD_State_of_Climate_2025.pdf`** — national climate report,
44 pages. Temperature rise (~0.88°C since 1960), 2024 rainfall
performance, drought impact on food security, climate outlook.

---

## `ndma/` — National Drought Management Authority

Two monthly drought bulletins plus extracted labels and comparison.

| File | Contents |
|---|---|
| `NDMA_Drought_Bulletin_2022-06.pdf` | June 2022 bulletin |
| `NDMA_Drought_Bulletin_2022-10.pdf` | October 2022 bulletin |
| `NDMA_2022_Labels.md` | Extracted drought phase labels + CHIRPS comparison |

**Key finding:** Zero overlap between NDMA Alarm counties (arid
north) and the monitor's severe counties (highland belt). CHIRPS
verification shows both groups had below-normal October 2022
rainfall — one drought event, two different tracking methodologies.

---

## `tamsat/` — TAMSAT-ALERT validation paper

**`TAMSAT_ALERT_Validation_2020.pdf`** — Boult et al. (2020),
*Meteorological Applications* 27(5):e1959.

Tests the correlation between TAMSAT-ALERT soil moisture and
Vegetation Condition Index (VCI) in Kenya: r = 0.68 (March–May,
contemporaneous seasonal mean). WRSI vs maize yield at national
level: r = 0.43.

**Relation to our work:** supports the general principle that soil
moisture is a useful proxy for vegetation in Kenya. Our finding
(r = 0.461 at county-month level with a 1-month lag) extends this
by specifying the temporal lag at finer resolution.

---

## `ada/` — Adaptation Consortium

Empty. The report on strengthening Kenya's climate data ecosystem
was not found via public search at download time. The D41 finding
(government email blocked) is documented in `docs/outreach_notes.md`
without this report as supporting context.

---

## How to use these files

1. **For the preprint draft (Week 6):** `NDMA_2022_Labels.md` and
   `CCRP_Summary.md` are the two files that go into the discussion
   section. They give independent validation context.
2. **For the null result:** `docs/week05_null_result.md` has the
   full cross-check against all four sources.
3. **For D41 documentation:** `docs/outreach_notes.md` documents
   the email barrier. The ADA report would have been supporting
   context if it had been found.

All findings from these reports are documented in:
- `docs/week05_null_result.md` — cross-check section
- `data/external/reports/ccrp/CCRP_Summary.md`
- `data/external/reports/ndma/NDMA_2022_Labels.md`
