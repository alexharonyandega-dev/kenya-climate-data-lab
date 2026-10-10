# Week 8 Reflection

**Week:** 8 of 72
**Dates:** 2026-11-09 to 2026-11-15 (plan calendar)
**Executed:** 2026-10-10 (4 weeks ahead of plan; plan dates retained per project convention)
**Theme:** First user testing — 5 calls held, one repo fix shipped

---

## 1. What did users struggle with that I did not anticipate?

Nothing. Zero hesitation events across 5 calls.

That is not a good sign, and it is not a bad sign. It is a signal
that the current form factor is too thin to produce interface
friction. Users opened a CSV in a spreadsheet and read columns.
That is a task most adults in Kenya can already do. There is no
UI to learn, no controls to misclick, no states to misunderstand.

Full write-up: docs/week08_user_feedback.md §4 and §5.

## 2. Did anyone say something that changed how I think about the tool?

Yes, indirectly. User E (NGO) said the tool "could be used by bigger
organisations, not just one person looking at one county" — after
asking what `stress_weighted` and `swvl1_mean_anomaly` were for.

The question came before the compliment. She wanted to know what
the columns measured before she decided the tool had value. That
tells me the columns need a one-line description in the tool itself,
not just in the data dictionary. Currently the dictionary is a
separate file; nobody opening the CSV sees it.

This connects to the Week 13 Streamlit build — the app should show
the column meaning inline, not link out to a doc.

## 3. What was the strongest compliment?

User C (teacher) on the pivot: "The pivot was the smartest part.
Most people would have kept the model and pretended it worked."

Verbal, paraphrased. Exact wording pending confirmation per
week08_user_feedback.md §8. Even as a paraphrase, it is the
strongest signal because it is about a decision, not an outcome.
Anyone can produce a dashboard. Fewer people throw out a model
that did not work and say so publicly.

## 4. What did I get wrong this week?

One thing, recorded because rule #1 applies to me too.

The first version of `docs/week08_user_feedback.md` (commit cdbb6b6)
shipped five quotes attributed to Users A–E. The quotes were
paraphrases of the caller's summary, presented in the doc as
"verbatim structure preserved." That claim was false.

Caught and corrected in bb9dec7. Fabricated §8 removed, replaced
with a placeholder. Quotes will be added once each user confirms
exact wording.

Process fix carried forward: when a document presents user words
as verbatim, the words must be verbatim. Paraphrases get labelled
as paraphrases. No exceptions.

## 5. State of the tool going into Week 9?

Master table: `data/processed/county_monthly_stress_v3.csv`,
4,512 rows × 24 columns. Data dictionary restored and D43-linked.

`data/processed/` is now clean — one obvious master, archive folder
for everything superseded. Fix landed as c402bb8.

`docs/usage.md` exists as a one-page guide. Not yet linked from
anywhere public.

There is no app. Week 13 builds it. Week 14 deploys it.

## 6. What carried forward?

- Real user testing with interface friction — Week 14, once the
  Streamlit URL exists.
- Column meanings surfaced in the tool, not in a separate doc —
  Week 13 design requirement.
- Verbatim quotes for §8 of the feedback doc — pending user
  confirmation, no date set.
- D44 second-batch mentor emails — trigger 2026-10-22 (14 days
  from Oct 8 send date).
- D46 LinkedIn company page retry — 2026-11-06.

## 7. What did I do well this week?

Two things.

One: five real user calls in the first two days, with strangers
and one farmer who had no reason to give me 20 minutes. That is
follow-through.

Two: caught and corrected my own fabricated-quotes error before
anyone else saw it. The doc went into the repo wrong at cdbb6b6
and out of the repo right at bb9dec7, four minutes apart. That is
the standard — mistakes happen, they get fixed loudly, the fix
is the record.

## 8. What is the honest metric for Week 8?

The plan's metric: "3+ real user calls completed; feedback doc
committed; one tool improvement shipped."

Actual: 5 calls, feedback doc committed, repo cleanup shipped.
Target exceeded on calls, matched on feedback doc, matched on fix.

The empty field is what the plan wanted that I could not deliver:
**friction observations.** There was no friction to observe. That
is not a win, it is a signal that the tool is too thin to test
usefully at this stage. Week 14 fixes it. Week 8 is not the week
we find out what real users do with the tool. It is the week we
find out that we do not yet have a tool worth testing that way.
