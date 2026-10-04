# Week 6 Reflection

**Week:** 6 of 72
**Dates:** 2026-10-05 to 2026-10-11
**Theme:** Preprint draft — Abstract, Methods, Validation

---

## 1. Does the abstract make me want to read the paper?

Yes. It leads with the NDMA finding — "zero overlap, both systems were
right" — which is the most distinctive claim. The 2022 drought detection
without calibration is the second hook. The null result at the end reads
as honest, not as a failure.

## 2. What decision from Week 3 did I omit?

The anomaly computation method. The Preprocessing section described
pixel masks, temporal aggregation, and missing values — but the actual
formula that turns raw anomalies into a standardized score was
undocumented until I added D43 at the end of the week.

That is exactly the kind of decision that looks obvious in hindsight
but is invisible to a reader. It is now documented.

## 3. Was the workflow diagram useful?

Yes. It forced me to check every script reference. Two scripts were
named incorrectly in the draft and the diagram is what caught them.

## 4. What is missing that a reviewer will ask about?

Three things:
- Introduction — Week 7–8 work.
- Data availability statement — added Sunday.
- Ethics statement — not needed for computational work but preprints
  increasingly require it.

## 5. What did the four-decision verification catch?

Two wrong decision references in the Preprocessing section: I cited D03
(master table filename) for temporal aggregation when the correct
reference was D04, and D14 (GEE asset format) for NDVI cloud gaps when
it should have been D13. Both fixed.

## 6. Is the paper ready for a mentor read?

Almost. The methods and validation sections are complete. The abstract
is final. The workflow diagram is in place. The paper is missing the
Introduction, which is what a mentor will most want to read first.
That is Week 7–8 work.

**Draft is ready for internal review. Not yet ready to send to a mentor.**
