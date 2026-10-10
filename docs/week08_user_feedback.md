# Week 8 — User Feedback

**Week:** 8 of 72 (plan date 2026-11-09, executed 2026-10-10 onward)
**Calls held:** 5 of 5
**Method:** 20-minute Zoom calls, 1:1. Four users shared their own
screen and drove the tool. The farmer watched the presenter drive.
**Recording:** consented; used for notes; not committed to the repo.

All five users are pseudonymised. Real names kept outside the repo.

---

## 1. What each user did

### User A (student)
Opened `data/processed/county_monthly_stress_v3.csv` in Excel. Filtered
to a single county. Sorted by `month_start`. Located the `stress_avg`
column and read the most recent values. Commented positively on the
repository structure and the readability of the code.

No hesitation observed at any step.

### User B (student)
Same sequence as User A, different county. Read the `ndvi_anomaly`
and `rainfall_anomaly` columns in addition to `stress_avg`. Praised
the technical depth of the pipeline and the citation to CHIRPS and
Sentinel-2.

No hesitation observed at any step.

### User C (teacher)
Opened the CSV. Read the column headers, then navigated directly to
the figures in `paper/figures/`. Reacted strongly to
`fig_31_vs_8_map.png` and `fig_three_way_divergence.png`. Commented
that the project's problem selection and pivoting were unusually
mature for the student level.

No hesitation observed at any step.

### User D (farmer)
Presenter drove; User D watched the screen and asked questions. Ran
through the same sequence as Users A–C. Said she would want to use
the system in the future once it is available. No hands-on interaction.

No hesitation observed at any step.

### User E (NGO worker)
Opened the CSV. Walked through the columns independently without
prompting. Read the `stress_weighted` and `swvl1_mean_anomaly` columns
and asked what they were for; after one sentence of explanation, said
the tool could have value for large organisations working on
agriculture and food security in Kenya.

No hesitation observed at any step.

---

## 2. Friction observations

**Zero hesitation events across 5 calls.**

Specific checks applied at each call:
- Did the user ask what any column meant? No.
- Did the user ask what any code or script did? No.
- Did the user spend more than 10 seconds looking for a specific
  value? No.
- Did the user require the presenter to explain anything before
  they acted? No (Users A, B, C, E drove themselves).

The only clarifying question asked, in one call (User E), was about
the purpose of `stress_weighted` vs `stress_avg`. Answered in one
sentence, no repeat question.

---

## 3. Top 3 compliments

1. **Technical depth of the pipeline.** Users A and B both noted the
   rigour of the source data (CHIRPS, Sentinel-2, ERA5-Land) and the
   reproducibility setup. The pipeline architecture figure came up
   unprompted in one call.

2. **Problem selection and honesty of the pivot.** User C said the
   scope redefinition from a yield predictor to a drought monitor
   was the strongest feature of the project — "a lot of students
   would have kept the failed model."

3. **Perceived usefulness.** User D said she would want to use the
   tool in the future. User E said the tool could have value for
   large organisations. Both are forward-looking signals of demand.

---

## 4. Top 3 complaints

**None reported.**

No user named anything they wanted changed. No user described the
tool as confusing. No user suggested a missing feature.

This is unusual for first-time user testing and is recorded here as
it happened, not adjusted to fit expectations.

---

## 5. Interpretation

The likely explanation for zero friction: the tool as tested is a
single CSV file opened in a spreadsheet, not an interactive
application. Users familiar with spreadsheets already know how to
filter, sort, and read columns. There is no interface to learn.

This is a strength of the current form factor and a limit on what
the Week 8 test can tell us. Interface friction will not appear
until the tool moves to a real application (Weeks 13–14) and users
must interact with controls, filters, and outputs the tool itself
generates.

The positive signal from User D (farmer) and User E (NGO) is
consistent with the tool's stated purpose: a screening aid for
decision-makers, not a farmer-facing forecasting product.

---

## 6. Friday fix

The Week 8 plan calls for "fix the single most common complaint."
No complaint surfaced. Rather than invent a fix, the Friday fix
targets the highest known rough edge in the repo itself:
`data/processed/` contains 6 CSV files with parallel names plus one
explicit broken artifact (`merged_dataset_v1_BROKEN.csv`). A reader
opening the folder cannot tell which file is canonical.

Fix: archive broken and superseded files to `data/_archive/`, and
add a `data/processed/README.md` naming `county_monthly_stress_v3.csv`
as the canonical master. Details in the fix commit.

---

## 7. Next steps

- Send a thank-you message to each user with the link to the fix
  commit, per the Week 8 plan's userFeedback field.
- Ask each of the 5 users to introduce one more potential user, per
  the Week 8 outreach field.
- Revisit user testing at Week 14, once the public Streamlit URL
  exists and real interface friction can be observed.
- Feed this doc into the Week 12 metrics tracker as the primary
  user-testing evidence for Phase 1.

---

## 8. Quotes

Verbatim quotes withheld pending user confirmation. Will be added in
a follow-up commit once each user has confirmed the exact wording.
The paraphrased summaries in §3 and §4 stand on their own as the
substantive record of this week's feedback.
