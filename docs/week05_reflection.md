# Week 5 Reflection

**Week:** 5 of 72
**Dates:** 2026-10-19 to 2026-10-25
**Theme:** Null result — the stress index does not predict yield loss

---

## 1. What did I expect to find when I ran the validation?

I expected the stress index to correlate with yield loss. Negative stress
should mean lower yield. The correlation came back at r = -0.832 for 2022
alone — which looked strong until I realised the sign was wrong.

## 2. What did I actually find?

Every meaningful test was null, wrong-signed, or untestable:

| Test | n | r | Verdict |
|---|---|---|---|
| County stress vs yield YoY | 20 | -0.085 | Null |
| County stress vs production YoY | 20 | +0.058 | Null |
| 2022-only (yield) | 5 | -0.832 | Wrong sign |
| Lagged | 15 | +0.267 | Null |
| National | 4 | +0.162 | Untestable |

The stress index does not predict county-level yield change.

## 3. Why is Kakamega the outlier?

Kakamega had the mildest 2022 stress (-0.182) and the worst yield crash
(-42.5%). Area went up 2% while production dropped 41%. That is not a
drought signature — drought reduces both area and yield. It is a disease
or pest signature.

The National Agriculture Production Report 2025 (page 31) confirmed:
*"localized outbreaks of fall armyworm"* compounded the 2022 season.

Kakamega was hit by BOTH a drought and a pest outbreak. The index caught
the drought. It cannot see the pest.

## 4. Was the null result a failure?

No. It is a scope discovery. The tool is a drought monitor. It is not a
yield predictor. Those are different problems. Only the first one is
currently solved. That is an honest, defensible finding — not a failure.

## 5. What would I do differently next time?

I would not run a validation test with n = 5. I would wait until I had
data for at least 20 counties before publishing any correlation. Five
points can produce any correlation you want.

I would also disaggregate by season. Annual yield masks short-rains
failures that show up in the wrong calendar year.

## 6. What is the honest sentence?

> The tool detects droughts. It does not predict yield loss. Those are
> different problems, and only the first one is currently solved.

---

## Week 5 deliverables

- `docs/week05_null_result.md` ✓
- 6 diagnostic scripts committed ✓
- D39 + D40 + D41 in DECISIONS_LOG ✓
- Armyworm confirmation from NAPR 2025 ✓
- Broken sidecar quarantined ✓
- Blog post published on Substack ✓
- Open letter published on Substack ✓
- One-pager PDF ✓
- 13 emails attempted, all bounced (D41) — pivot to public channels

## Week 5's unexpected lesson

The plan called for cold email. Cold email failed. The alternative —
publishing publicly on Substack and X — is the fallback that worked.
Not because the tool is wrong, but because Kenyan government mail
servers reject Gmail. That is an infrastructure barrier, not a
project failure. Documented as D41.

## Week 5 in one sentence

I tried to validate my tool and it failed — and that failure taught me
more than a success would have.

---

## Extended session (2026-10-03): KCND integration

After publishing the null result, I downloaded and integrated 12 reports from the Kenya Climate & Nature Directory. This changed how I understand the tool.

**The main new finding:** NDMA and the monitor flagged completely different counties in 2022. Zero overlap. My first instinct was to frame this as "two droughts." I tested it against CHIRPS rainfall and found something more precise:

| Group | Mean Oct 2022 rainfall z-score |
|---|---|
| Monitor severe counties | −1.14 |
| NDMA Alarm counties | −0.71 |

Both groups were in drought. The difference is not two events — it's two tracking methodologies on one event. NDMA classifies by cumulative pastoral impact. The monitor classifies by current-month rainfall and vegetation anomaly.

**Three errors caught during this session:**

1. I wrote "national average = 0.431" in a summary. It was fabricated. Bomet's actual national baseline is 0.4311. Fixed in `a3b32d0`.
2. I claimed "two droughts" without testing. CHIRPS verification proved it was one drought. Fixed in `736ee0d`.
3. I claimed Boult et al. (2020) "directly supports" our lead-lag finding. Reading their methods: they tested contemporaneous seasonal correlation (r = 0.68 MAM), not lead-lag. Fixed in `5dbb827`.

**What I learned:** Every claim that sounds interesting needs to be verified. Every number needs a source. Every "supports" needs to specify *what* it supports and *what* it doesn't. The verification scripts did the work here — they're now part of the workflow.

**What this means for the paper:** The contribution statement is sharper. Not "we built a monitor." Not "our tool detects a second drought." Rather:

> *"Kenya's drought monitoring infrastructure has a coverage gap. NDMA tracks 23 ASAL counties by cumulative pastoral impact. This project builds a complementary monitor for all 47 counties that tracks current-month rainfall and vegetation anomaly. In 2022, these two systems flagged entirely different counties. Both were correct. They answer different questions about the same event."*
