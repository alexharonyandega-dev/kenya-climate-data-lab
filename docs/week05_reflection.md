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
