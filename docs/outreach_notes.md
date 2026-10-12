# Outreach Notes — KNBS and County Government

**Date:** 2026-10-02
**Status:** Documented barrier. Pivoting to alternative channels.

## Summary

On 2 October 2026, 13 emails were sent to KNBS, Nakuru County,
Kakamega County, and Bungoma County using publicly listed email
addresses. **Every single email bounced.** The failure is systematic,
not incidental.

## What was tried

| Org | Address | Result |
|---|---|---|
| KNBS | datarequest@knbs.or.ke | 500 error |
| KNBS | info@knbs.or.ke | Address not found |
| KNBS | directorgeneral@knbs.or.ke | Address not found |
| Nakuru | info@nakuru.go.ke | Address not found |
| Nakuru | lmmaculate.njuthe.maina@nakuru.go.ke | Address not found |
| Nakuru | supplychain@nakuru.go.ke | Address not found |
| Kakamega | cec-agriculture@kakamega.go.ke | Address not found |
| Kakamega | co-agriculture@kakamega.go.ke | Address not found |
| Kakamega | agriculture@kakamega.go.ke | Address not found |
| Kakamega | info@kakamega.go.ke | Address not found |
| Bungoma | info@bungoma.go.ke | Address not found |
| Bungoma | bungomacountygov@gmail.com | Address not found |
| Bungoma | bungomacountygovt@gmail.com | Address not found |

Total: **13 emails sent. 0 delivered.**

## Why they bounced

Two overlapping causes:

### 1. Kenyan government mail servers reject Gmail

Most Kenyan government `.go.ke` mail servers use aggressive
anti-spam filtering that rejects mail from `@gmail.com` and other
free email providers. This is a well-known barrier that affects
students, independent researchers, and small NGOs across East Africa.
The rejection is silent or returns "Address not found" — which is
misleading, because the address may be valid but the sender is not
trusted.

### 2. Some listed addresses are stale

County contact pages are updated infrequently. Addresses listed in
2023 may be dead in 2026. Government staff rotations also leave dead
mailboxes behind.

## What this means

**Email is not the right channel for first contact with Kenyan
government offices when the sender uses a free email provider.**

Alternative channels, in order of likelihood of success:

1. **LinkedIn** — search for the named official, connect, and send a
   short message. LinkedIn DMs are read by most Kenyan public servants.
2. **Phone calls** — county agriculture departments expect phone
   inquiries. A 2-minute call asking for the correct email address is
   faster than any email.
3. **X / Twitter** — the Kenyan climate and agriculture community is
   active on X. Public posts get signal-boosted to government
   accounts.
4. **Substack** — publish a post specifically for county agriculture
   officers, and let them come to you. The channel is public, indexed,
   and cannot bounce.
5. **Physical visit** — for KNBS specifically, a walk-in at Real
   Towers, Upper Hill, Nairobi. Same for county headquarters, if
   physically reachable.

## What would unblock email

If email must be used, the sender needs a domain-based address:

- Register a `.co.ke` or `.org` domain (~$10–15/year)
- Set up Zoho Mail's free tier (allows custom domain)
- Send from `alex@kenyaclimatelab.org` instead of Gmail

A domain-based address is recognised as legitimate by spam filters
and will pass. This is a 30-minute setup and unlocks every future
outreach attempt.

## What this means for the project

The outreach is not failing because the project is wrong or the
emails are bad. It is failing because of an infrastructure barrier
that affects every Kenyan student researcher using free email. This
is not a personal failure — it is a documented systemic issue.

The workaround is channel selection, not content improvement. Same
messages, different medium.

## Lessons for other student researchers

1. Do not rely on cold email to Kenyan government offices from a
   Gmail account. It will usually fail.
2. Register a custom domain early. It costs ~$10/year and unlocks
   every future outreach.
3. Use LinkedIn for first contact when possible.
4. Phone calls work better than email for county offices.
5. Publish your work publicly — people find it through search and
   social, not through cold email.
6. When email fails, do not keep retrying. Change the channel.

## Next steps

1. Set up a custom domain and Zoho Mail (Week 6)
2. Reach out to the named officials on LinkedIn (Week 6)
3. Publish an open letter to county agriculture officers on
   Substack, with the tool and the ask (Week 6)
4. Call the numbers listed below to request working email
   addresses (Week 6)

### Phone numbers (from official county pages)

- **Nakuru County:** 051 2214142
- **Kakamega County:** 056 2031850 / 056 2031852 / 056 2031853
- **Bungoma County:** 055-2030144 / 055-203-0545
- **KNBS:** 020 3317583 / 020 3317584 (Real Towers, Upper Hill)

---

## Update (2026-10-05): LinkedIn activated

After the email channel was documented as blocked (D41), LinkedIn was
activated as the alternate outreach channel.

**What was done:**
- Profile fully set up at linkedin.com/in/alexharonyandega
- Intro post published on the feed with the 31-vs-8 map
- 30 accounts followed (Kenyan research, government, climate-tech)
- 1 connection request sent (Dinah Makokha, Chief Officer Agriculture, Bungoma County)

**What this changes:**
- LinkedIn is now the primary outreach channel for county officials
- The Substack open letter remains the secondary channel (public, forwardable)
- Phone calls remain the fallback for officials not on LinkedIn

**Officials status:**
| Official | Channel tried | Status |
|---|---|---|
| Dinah Makokha (Bungoma) | LinkedIn | Connection request sent |
| Leonard Bor (Nakuru) | LinkedIn | Not found — phone fallback |
| Monicah Salano Fedha (Bungoma) | LinkedIn | Not found — phone fallback |

---

## LinkedIn company page blocked (2026-10-06)

**Attempted:** Create a company page for "Kenya Climate Data Lab" at
linkedin.com/company/setup/new/

**Result:** LinkedIn returned "Feature not available — Please verify
your workplace before creating a LinkedIn Page."

**Cause:** LinkedIn requires new or low-activity accounts to verify
workplace association before creating company pages. The original
alexharonyandega@gmail.com address is on LinkedIn's free-provider
blacklist. The verified `.ac.ke` school email is already associated
with a dormant LinkedIn account that requires ID verification to
recover — not available to the user.

**Resolution path:** On 2026-10-08 (after Student Pack activates),
claim free `.me` domain via Namecheap. Set up Zoho Mail free tier on
the new domain. Get `alex@kenyaclimatelab.me`. Use that address for
LinkedIn workplace verification.

**Impact on outreach:** None. The KNBS + county officer outreach
emails can be sent today from `alex.haro@mpesafoundationacademy.ac.ke`
without waiting for the domain.

**Date:** 2026-10-06

---

## Update (2026-10-09): Domain + Zoho + LinkedIn unblocked

**Student Developer Pack status:** Confirmed active. Benefits valid
through 2026-10-08 → 2028-10-06. Copilot sign-ups paused per GitHub
email, but the Namecheap + Zoho path is unaffected.

**What is now possible (per D41 / D42 resolution path):**
1. Claim free `.me` domain from Namecheap via Student Pack.
2. Set up Zoho Mail Free Forever on that domain.
3. Create `alex@kenyaclimatelab.me`.
4. Use that address to verify LinkedIn workplace.
5. Create the LinkedIn company page for Kenya Climate Data Lab.

**Action taken:** Work executed 2026-10-09. Outcomes recorded below.

- Domain: kenyaclimatelab.me registered via Namecheap Student Pack
  (free, expires 2027-10-09).
- Mail: Zoho Mail Free Forever. Mailbox alex@kenyaclimatelab.me
  created and operational.
- DNS: 3 MX records (mx / mx2 / mx3.zoho.com, priorities 10 / 20 / 50),
  1 SPF TXT (v=spf1 include:zohomail.com ~all), 1 DKIM TXT
  (zmail._domainkey). All records verified by Zoho on 2026-10-09.
- Send/receive test: bidirectional test with Gmail passed.
- LinkedIn primary email: switched to alex@kenyaclimatelab.me.
- LinkedIn company page: BLOCKED by account-age gate. See D46 in
  docs/DECISIONS_LOG.md.

---

## Update (2026-10-11): First mentor reply — Ogembo call booked

Vincent Ogembo (Vrije Universiteit Brussel / ICPAC) replied to the
Week 7 mentor email on 2026-10-11. Response verbatim, in part:
"This is a great effort! We can have a 20mins online meeting on
Thursday 15th October at 12:30pm EAT."

Call booked: Thursday 2026-10-15, 12:30pm EAT, 20 minutes.

Prep plan: send draft methods + abstract 24h in advance; send Zoom
link 48h in advance; run the call as listening-first (project summary
in ≤3 min, rest of time on his critique).

Source email: docs/week07_reflection.md §1 (Ogembo listed as the
mentor of most interest).

**2026-10-11 follow-up:** Confirmation email sent to Ogembo with the
Zoom link for Thursday 2026-10-15 12:30pm EAT / 11:30am Brussels.
Draft methods and workflow figure to be sent Tuesday 2026-10-13.

Zoom link is stored in Gmail only (contains Personal Meeting ID) —
not committed to the repo.

## Update (2026-10-11): Week 8 publishing trail

**Substack:** Week 8 post published.
URL: https://substack.com/@kenyaclimatelab/note/c-357677451

**LinkedIn:** Feed post published, linking to the Substack post.
URL: https://lnkd.in/p/eXBubQMN

**Engagement:** First comment received from Muhammad Khalid Fayyaz:
"Is it a designed research?" Reply sent: Reply not yet sent.

**Log entries added to metrics/outreach_log.csv for both posts.**

---

## Update (2026-10-11): New LinkedIn contact — Adeola Boluwatife

**Contact:** Adeola Boluwatife
**Location:** Nigeria
**Role:** Agricultural Data Analyst, Research Analyst, Founder,
Agriculture Literacy Initiative
**Profile:** linkedin.com/in/[her-handle, if you have it]
**Connections:** 500+

**Origin:** Sent a connection request 2026-10-11 with a one-line
introduction to the project. Accepted same day.

**Follow-up sent (2026-10-11):** Short message with no ask. Named
her Agriculture Literacy Initiative and offered the Week 8 Substack
post as reciprocal reading. Framed the literacy problem and the
climate data problem as "cousins."

**Why she is on the list:** Her work is at the intersection of
agricultural data and non-specialist legibility — the exact problem
Kenya Climate Data Lab has to solve at Week 13 (the app) and beyond.
If she engages, she is a candidate for early feedback on the
public-facing pieces of the project.

**No asks made.** If she replies, next step is a specific question
about how her initiative communicates agricultural data to
non-specialists. If she does not reply, this stays a warm contact
with no follow-up scheduled.

---

## Update (2026-10-12): CGIAR responds — introductory call proposed

**Routing chain (from the CGIAR internal emails visible in the reply):**

1. 2026-10-07 — Alex submits via the CGIAR public contact form
   (Chief-Scientist office)
2. 2026-10-09 — Sandra Milach (CGIAR Chief-Scientist office) forwards
   to Nancy Koyo (ILRI)
3. 2026-10-12 09:36 — Nancy Koyo forwards to Todd Rosenstock and
   Ram Dhulipala (CGIAR System Organization)
4. 2026-10-12 09:46 — Todd Rosenstock replies, ccs Pete Steward and
   Michelle Tigchelaar (WorldFish)
5. 2026-10-12 10:48 — Pete Steward (Alliance Bioversity-CIAT) replies
   to Alex directly

**The reply (Pete Steward, verbatim in part):**
"Congratulations on the impressive initiative and dedication you are
demonstrating with the Kenya Climate Data Lab... we see strong
potential for a mutually beneficial partnership."

Pete leads analytics and modeling for the Africa Agriculture
Adaptation Atlas at Alliance Bioversity International and CIAT.
Works alongside Todd Rosenstock (Climate Action Science Program)
and RCMRD (Rose Waswa) and SERVIR East Africa (Anastasia Wahome).

**Four collaboration modes offered by CGIAR:**

1. **Providers of Data** — historical sub-county + county maize yield
   registries; ERA (Evidence for Resilient Agriculture) and CAROB
   experimental agronomic trial datasets
2. **Consumers of Data** — ingest the project's automated weekly
   county telemetry feed into their county climate risk work
3. **Hosts & Amplifiers** — host, spotlight, and amplify the
   open-source tools into regional decision-maker networks
4. **Mutual Testers** — mutual user-testing of outputs and
   decision-support products

**People cc'd on the reply:**

| Name | Org | Note |
|---|---|---|
| Benson Kenduiywo | SERVIR East Africa / JKUAT | **Also on the Week 7 mentor list** (mentor_targets.csv, sent 2026-10-08, status sent_unconfirmed). This reply is now a warm introduction. |
| Anastasia Wahome | SERVIR Eastern & Southern Africa | — |
| Majambo Gamoyo | SERVIR Eastern & Southern Africa | — |
| Rose Waswa | RCMRD | — |
| Michelle Tigchelaar | WorldFish | — |
| Todd Rosenstock | CGIAR System Organization | — |

**Proposed call windows (all EAT):**

- Wed 2026-10-14, 14:30–16:00
- Thu 2026-10-15, 10:00–11:30 or 15:00–16:30
- Fri 2026-10-16, 11:00–12:30

**Decision:** Friday 2026-10-16, 11:00–12:30 EAT. Thursday afternoon
is the Ogembo preprint critique call (12:30pm EAT). Friday morning
gives time to prepare properly for the CGIAR conversation.

**Safaricom context (referenced in the original enquiry):**

The Oct 7 CGIAR enquiry stated that Safaricom's Head of Innovation
"has reviewed the repository and reached out to schedule a technical
meeting." The email thread (2026-10-05 entry above) shows:
- Stephen Chege forwarded to Andrew Masila on 2026-10-05
- Masila replied 2026-10-05: "Will look for some time to meet and
  appreciate further your initiative."
- Alex replied 2026-10-05 confirming readiness for technical review

Per Alex, Masila reviewed the repository via an additional channel.
No meeting has been formally scheduled as of 2026-10-12. The CGIAR
enquiry's phrasing was stronger than the email thread alone shows.

**Boundaries for the CGIAR call:**

- MIT licence stays. No CLA, no copyright assignment, no exclusive
  hosting arrangement.
- No co-authorship commitments on the preprint before scope is
  discussed.
- No data-ingestion cadence commitments before understanding what
  a weekly telemetry feed means operationally.
- No delivery timelines on results.
- Pre-read (1-page) to be sent by Wednesday evening (2026-10-14):
  pipeline scope + limits, null result, specific data gap (yield
  registries for validation), telemetry offer.

**Reply to Pete Steward:** to be sent Monday 2026-10-12, confirming
Friday 11:00–12:30 EAT.

**Log entries:** metrics/outreach_log.csv updated once the call is
formally confirmed by Pete.

**Significance:** first institutional research partnership offer.
Two high-stakes calls on consecutive days (Ogembo Thu, CGIAR Fri).

**2026-10-12 11:23 EAT:** Reply sent to Pete Steward in the CGIAR
thread, cc to the full distribution (Michelle, Benson, Todd, Nancy,
Ram, Anastasia, Majambo, Rose). Confirmed Friday 16 Oct 2026,
11:00-12:30 EAT. Committed to 1-page pre-read by Wednesday evening.
Stated MIT licence boundary and no co-authorship before scope
discussion. Flagged that Dr. Kenduiywo has a Week 7 mentor email in
his inbox.
