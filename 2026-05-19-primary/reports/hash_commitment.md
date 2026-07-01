---
layout: default
title: Hash Commitment Analysis
---

# Hash Commitment Analysis — Georgia May 19, 2026 RLA

**Version:** v0.18 &nbsp;·&nbsp; **Review timestamp:** 2026-07-01T00:00:00Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Reports](../)

---

> **AI-assisted analysis, partially reviewed.** This analysis was produced with significant AI assistance (Claude, Anthropic). Findings are ongoing and some claims may require further verification. Corrections welcome via [GitHub Issues](https://github.com/nealmcb/rla-review-arlo/issues).

## ✓ OVERALL RESULT: HASH COMMITMENT VERIFIED

Both committed hashes match the currently posted files exactly.

---

## The Claimed Commitment

The SOS June 3, 2026 press release states:

> "You can confirm that these were the same batch tallies that we started the audit with  
> by performing a SHA256 hash of the file and matching it to the tweet from  
> Georgia Secretary of State Brad Raffensperger (@GaSecofState) from 05/28/2026 at 11:52 AM."

Source: `https://sos.ga.gov/news/raffensperger-announces-primary-risk-limiting-audit-confirms-accurate-vote-count`

**Note on account handle:** The SOS press release uses `@GASecofState` but the actual tweet thread is from `@GaSecofState` (mixed case). These are the same account.

---

## The Tweet Thread (via copy-paste, 05/28/2026)

The following tweets were posted as a thread from @GaSecofState at 11:52 AM EDT on May 28, 2026:

> **Tweet 1:**
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

Both committed hashes verified. The files available for download on June 29, 2026 are byte-for-byte identical to the files committed in the May 28 tweet thread. The MailChimp URL filenames containing `2026_06_02T...` timestamps reflect the press-release link creation date, not file regeneration — the file bytes are unchanged.

---

## Timing Analysis

The official `final_audit_report.csv` records a Round 1 start timestamp of `2026-05-28T15:49:15` for both contests. This is Arlo's server-side record of when an audit administrator clicked "Start Round" in the Arlo web application — the moment the random seed was entered and the sample draw was triggered. The timestamp reflects the Arlo server clock (UTC), which may differ slightly from the wall clock at the dice-roll event. Arlo records this per-contest, and both contests show the same value: 15:49:15 UTC.

| Event | UTC | EDT |
|-------|-----|-----|
| Arlo Round 1 started (seed entered, sample drawn) | 15:49:15 | 11:49 AM |
| @GaSecofState tweet thread | ~15:52:00 | 11:52 AM |
| Gap | ~165 seconds | ~2.8 minutes |

**The tweet was committed approximately 3 minutes after the Arlo round was started** — that is, after the random seed was entered and the sample was already drawn.

### What the tweet explains — and what it doesn't

The tweet thread explains clearly why the actual data files were withheld until after hand-counting finished: publishing them first might give auditors "a number to hit." This is a reasonable concern about the integrity of the hand count.

What the tweet does not address is why the hash wasn't committed *before* the seed was entered. The ~3-minute window between seed entry and hash publication means that, in principle, someone with advance knowledge of which batches would be drawn could have made targeted alterations to the batch tally files before the hash was published. With sufficient preparation, such alterations could be made quickly. This is not evidence that this occurred — but it is a gap that a pre-seed commitment would close entirely.

### What this commitment does and does not protect against

**Protects against:**
- Rearranging or replacing batch tally files after the hand counts are completed, e.g. to make discrepancies disappear or to swap in a different set of tallies
- Undetected alteration of any audit artifact after the May 28 commitment

**Does not protect against:**
- Alterations made in the ~3 minutes between seed entry (15:49:15 UTC) and the hash publication (~15:52 UTC)
- Alterations made at any time before the seed was entered (counties uploaded files over the preceding week; Arlo stores them internally)
- Altering the ballot manifests to adjust the eligible population before the seed was entered

**The remaining gap:** A true pre-seed commitment would hash the files and post the hashes *before the dice are rolled*. This is achievable with no change to the public dice-roll ceremony — just hash and post hours earlier, then roll. Georgia's approach is a meaningful and successful transparency measure; this is the single procedural step that would strengthen it most.

---

## Assessment

| Claim | Status |
|-------|--------|
| @GaSecofState tweet thread with SHA256 hashes existed on 05/28/2026 | **Verified** — tweet text confirmed via copy-paste |
| Manifests hash matches currently posted `manifests.zip` | **✓ VERIFIED** — exact match |
| Candidate totals hash matches currently posted `candidate_totals.zip` | **✓ VERIFIED** — exact match |
| Hash was committed before the random seed was entered | **Not met** — tweet ~3 min post-seed |
| Commitment is durably archived | **Partial** — X/Twitter post only; not archived on sos.ga.gov |

**Overall finding:** The SHA256 hash commitment is **verified**. Both ZIPs are byte-identical to the files committed in the May 28, 2026 tweet thread. This is a meaningful and successful transparency measure. The remaining limitations are (1) the commitment was post-seed rather than pre-seed, and (2) the commitment lives only on X/Twitter rather than a durable official location.

---

## Recommendations

1. **Archive the tweet** via web.archive.org and link the archive from sos.ga.gov/page/elections-audit-information
2. **Post full hashes as plain text on sos.ga.gov** alongside the artifact links
3. **Commit hashes before the dice roll** — hash the files and post them to sos.ga.gov *in advance* of the dice-roll event; this is the highest-impact single improvement and requires no logistical change to the public ceremony
4. **Continue committing both files** — the current practice of committing both manifests and candidate totals hashes is the right approach and should be continued
