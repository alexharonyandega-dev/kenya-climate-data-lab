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
