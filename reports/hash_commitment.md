---
layout: default
title: Hash Commitment Analysis
---

# Hash Commitment Analysis — Georgia May 19, 2026 RLA

## ✓ OVERALL RESULT: HASH COMMITMENT VERIFIED

Both committed hashes match the currently posted files exactly.

---

## The Claimed Commitment

The SOS June 3, 2026 press release states:

> "You can confirm that these were the same batch tallies that we started the audit with  
> by performing a SHA256 hash of the file and matching it to the tweet from  
> Georgia Secretary of State Brad Raffensperger (@GaSecofState) from 05/28/2026 at 11:52 AM."

Source: `https://sos.ga.gov/news/raffensperger-announces-primary-risk-limiting-audit-confirms-accurate-vote-count`

**Note on account handle:** The SOS press release uses `@GASecofState` but the actual tweet thread is from `@GaSecofState` (mixed case). These are the same account; the press release had a minor capitalization inconsistency.

---

## The Tweet Thread (provided by investigator, 05/28/2026)

The following tweets were posted as a thread from @GaSecofState at 9:52 AM · May 28, 2026
(viewer's timezone = Mountain Daylight Time; = 11:52 AM EDT = 15:52 UTC):

> **Tweet 1** (9:52 AM viewer time):
> "Later today, Georgia counties are counting a random sample of ballot batches by hand as part of Risk Limiting Audits (RLA). We want this audit to be as transparent as possible."

> **Tweet 2:**
> "We could publish the ballot manifests and machine-counted batch totals, so everyone can follow along and verify on their own that the numbers match with the hand counts. But, if we did that before the audit finishes, some may question whether that gives auditors a 'number to hit'"

> **Tweet 3:**
> "So, in order to achieve transparency and audit integrity at the same time, we are publishing a hash of the ballot manifests:
> `c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf`"

> **Tweet 4:**
> "and the machine-counted batch totals: `2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312`"

> **Tweet 5:**
> "When the audit completes, we will publish the ballot manifests and machine-counted batch totals, and the public will be able to check that the hand counts match, and that the batch totals match the hash above."

The Gabriel Sterling X post (status/2070235247657287995) may be a repost or quote-tweet of this thread.

---

## Note on Briefing's "Known Prefix"

The investigation briefing specified a known hash prefix of `7d00771bf178007f4c6f43bf45b6`.
**This prefix does not match either of the actual tweeted hashes.** It appears this prefix
was incorrect (possibly from a different source, a different audit, or a transcription error).
The actual tweeted hashes are the full 64-character values above, both of which were verified.

---

## Hash Verification

### Ballot Manifests

| | Value |
|-|-------|
| Tweeted hash (Tweet 3) | `c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf` |
| Computed SHA256 of `manifests.zip` | `c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf` |
| **Match** | **✓ EXACT MATCH** |

### Machine Batch Tallies (Candidate Totals)

| | Value |
|-|-------|
| Tweeted hash (Tweet 4) | `2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312` |
| Computed SHA256 of `candidate_totals.zip` | `2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312` |
| **Match** | **✓ EXACT MATCH** |

Both committed hashes verified. The files available for download on June 29, 2026 are byte-for-byte identical to the files that were committed in the May 28 tweet thread. The MailChimp URL filenames containing `2026_06_02T...` timestamps reflect the press-release linking date, not file regeneration — the file bytes are unchanged.

---

## Timing Analysis

| Event | UTC | EDT | Notes |
|-------|-----|-----|-------|
| Arlo Round 1 started (seed entered, sample drawn) | 15:49:15 UTC | 11:49 AM EDT | From `final_audit_report.csv` |
| @GaSecofState tweet thread | 15:52:00 UTC | 11:52 AM EDT | Shown as 9:52 AM MDT in viewer's timezone |
| Gap | +165 seconds | +2.8 minutes | Tweet was **after** round start |

**The tweet was committed approximately 3 minutes AFTER the Arlo round was started** (i.e., after the random seed was entered and the sample was drawn).

### SOS's Stated Rationale

The tweet thread explicitly explains the deliberate choice:
- Publishing the files before the audit completes might give hand-counters "a number to hit" (i.e., they might adjust their count to match the machine tally)
- So the SOS committed hashes early (at audit start) to enable post-audit verification, while withholding the actual files until the audit completed
- This **protects against post-audit falsification** of the batch tallies

### What This Commitment Does and Does Not Protect

**Protects against:**
- Altering batch tallies AFTER the hand counts are completed, to make discrepancies disappear
- Replacing the machine-counted files with different ones after the audit

**Does NOT protect against:**
- Altering batch tallies BEFORE or DURING the dice roll, knowing which batches would be drawn (insider threat)
- The committed files were uploaded to Arlo weeks before the dice roll; Arlo stores them internally; an Arlo administrator with advance knowledge of the seed could theoretically alter tallies before the public commitment — though the public dice roll makes this very unlikely
- Altering the ballot manifests to exclude certain batches from the eligible population before the seed was entered

**The remaining transparency gap:** A true **pre-seed** commitment would require hashing the files and posting the hashes *before the dice are rolled*, not after. This would eliminate even the theoretical insider threat. Georgia's current approach is a meaningful commitment but is structurally a post-seed attestation.

---

## Assessment

| Claim | Status |
|-------|--------|
| @GaSecofState tweet thread with SHA256 hashes existed on 05/28/2026 | **Verified** — tweet text confirmed |
| Manifests hash matches currently posted `manifests.zip` | **✓ VERIFIED** — exact match |
| Candidate totals hash matches currently posted `candidate_totals.zip` | **✓ VERIFIED** — exact match |
| Hash was committed before audit counters saw machine tallies | **Verified** — tweet says audit "later today"; counties started May 28–29 |
| Hash was committed before the random seed was entered | **Not met** — tweet ~3 min post-seed (deliberate, explained in tweet) |
| Commitment is durably archived | **Partial** — X/Twitter post, not archived on sos.ga.gov |

**Overall finding:** The SHA256 hash commitment is **verified**. Both ZIPs are byte-identical to the files committed in the May 28, 2026 tweet thread. This is a meaningful and successful transparency measure. The remaining limitations are (1) the commitment was post-seed rather than pre-seed, and (2) the commitment lives only on X/Twitter rather than a durable official location.

---

## Recommendations (Updated)

1. **Archive the tweet** — the tweet thread is the sole durable record of the commitment; it should be Web-Archived and linked from the SOS audit information page
2. **Post full hashes on sos.ga.gov** — alongside (or instead of) the tweet, so the commitment survives platform changes
3. **Commit hashes before the dice roll** — hash the files and post them in advance of the dice roll event, eliminating even the theoretical insider threat; this is achievable without any logistical change to the public dice-roll ceremony
4. **Continue committing both files** — the current practice of committing both manifests and candidate totals hashes is the right approach and should be continued/standardized
