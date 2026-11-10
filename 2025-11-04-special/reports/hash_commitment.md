---
layout: default
title: Hash Commitment Analysis — November 2025
---

# Hash Commitment Analysis — Georgia November 4, 2025 Special Election RLA

**Version:** v0.23 &nbsp;·&nbsp; **Review timestamp:** 2026-11-10T00:51:00Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Review](../index.md)

---

> **DRAFT - AI-assisted analysis, partially reviewed.** This analysis was produced with significant AI assistance (Claude, Anthropic). Findings are ongoing and some claims may require further verification. Corrections welcome via [GitHub Issues](https://github.com/nealmcb/rla-review-arlo/issues).

## ✓ OVERALL RESULT: HASH COMMITMENT VERIFIED

Both committed hashes match the published files exactly. Both were posted 32 to 54 minutes after
the public dice roll that set the random seed, and before hand counting began the next day.

---

## The Tweet Thread

@GaSecofState posted a thread on November 12, 2025. Exact UTC times come from each post's status
ID, decoded with [`src/snowflake_time.py`](https://github.com/nealmcb/rla-review-arlo/blob/main/src/snowflake_time.py).

| Post | UTC | Text |
|------|-----|------|
| [1988711434394739062](https://x.com/GaSecofState/status/1988711434394739062) | 20:52:09.088 | "Tomorrow, Georgia counties are starting a random sample of ballot batches by hand as part of a Risk Limiting Audit (RLA) of the November 4th PSC/Municipal election. We want this audit to be as transparent as possible." |
| [1988711899169509447](https://x.com/GaSecofState/status/1988711899169509447) | 20:53:59.899 | "So, in order to achieve transparency and audit integrity at the same time, we are publishing a hash of the ballot manifests: `e05bcc4cfcf42c26eea6d2b4013d3e62f8226129555137828ae2d46addde4a47`" |
| [1988711984456503394](https://x.com/GaSecofState/status/1988711984456503394) | 20:54:20.233 | "and the machine-counted batch totals: `608508332b534b6847367c2e8de7901ea0527dd43e784eaedc3e33cd083ed61e`" |

The thread's other posts were not captured for this review.

---

## Hash Verification

### Ballot Manifests

| | Value |
|-|-------|
| Tweeted hash | `e05bcc4cfcf42c26eea6d2b4013d3e62f8226129555137828ae2d46addde4a47` |
| SHA256 of the inner ZIP `November-4-2025-Municipal-General-Special-Election-2025-11-17T18:43+00:00-manifests.zip` | `e05bcc4cfcf42c26eea6d2b4013d3e62f8226129555137828ae2d46addde4a47` |
| **Match** | **✓ EXACT MATCH** (also matches the bundled `.sha256sum`) |

### Machine Batch Tallies (Candidate Totals)

| | Value |
|-|-------|
| Tweeted hash | `608508332b534b6847367c2e8de7901ea0527dd43e784eaedc3e33cd083ed61e` |
| SHA256 of the inner ZIP `November-4-2025-Municipal-General-Special-Election-2025-11-17T18:46+00:00-candidate-totals.zip` | `608508332b534b6847367c2e8de7901ea0527dd43e784eaedc3e33cd083ed61e` |
| **Match** | **✓ EXACT MATCH** (also matches the bundled `.sha256sum`) |

The inner ZIPs are inside `manifests_bundle.zip` and `candidate_totals_bundle.zip` (see the
[Data Artifacts](../index.md#data-artifacts) table); extracted copies are under
`2025-11-04-special/extracted/`.

**Why the file names carry a later date.** The inner ZIPs are named for 2025-11-17, five days
after the tweets that commit their hashes. This is consistent: a file's name is not part of its
contents, and every entry in both ZIPs carries the fixed timestamp 1980-01-01 00:00. The ZIPs are
therefore deterministic, so their hashes depend only on the per-county CSV contents. The names
record when the files were packaged for publication, after the audit ended (Round 1 end
2025-11-17 17:02:15 UTC); the contents are byte-for-byte what was committed on November 12.
Deterministic packaging is good practice for exactly this reason.

---

## Timing Analysis

The seed `34363370190391208563` came from a public roll of twenty 10-sided dice at the
Secretary's press conference at the State Capitol, scheduled for 3:00 PM EST on Wednesday,
November 12 ([Local 3 News, 2025-11-11](https://www.local3news.com/local-news/ga-sec-of-state-to-kick-off-post-election-audit-for-public-service-commission-race/article_e73a49f8-09bb-4e31-92d3-614bf9ddaa8e.html)).
`final_audit_report.csv` records the Round 1 start, when the seed was entered into Arlo and the
sample drawn, as `2025-11-12T20:21:36.046696+00:00`. The roll therefore happened between 20:00 and
20:21:36 UTC. A post or recording from the event would fix it exactly.

| Event | UTC | EST | After the dice roll |
|-------|-----|-----|---------------------|
| Public dice roll (twenty 10-sided dice, State Capitol) | 20:00–20:21:36 | 3:00–3:21 PM | — |
| Arlo Round 1 started (seed entered, sample drawn) | 20:21:36.047 | 3:21:36 PM | 0–22 m |
| Post 1 (thread begins; no hash) | 20:52:09.088 | 3:52:09 PM | 31–52 m |
| Ballot manifests hash | 20:53:59.899 | 3:53:59 PM | **32–54 m** |
| Batch totals hash | 20:54:20.233 | 3:54:20 PM | **33–54 m** |
| Hand counting begins | November 13 | | next day |

As in the [May 2026 primary](../../2026-05-19-primary/reports/hash_commitment.md#timing-analysis),
the commitment is **post-seed and pre-count**. It proves the manifests and batch totals were not
changed after 20:54 UTC on November 12, including during the hand count. It does not cover the
32 to 54 minutes between the dice roll and the hash posts, or anything before the roll. Posting the hashes before the dice roll would close that gap with no change to the
public ceremony.

---

## Assessment

| Claim | Status |
|-------|--------|
| @GaSecofState posted SHA256 hashes of the manifests and batch totals on 2025-11-12 | **Verified** — post texts and status IDs above |
| Manifests hash matches the published manifests ZIP | **✓ VERIFIED** — exact match |
| Batch totals hash matches the published candidate totals ZIP | **✓ VERIFIED** — exact match |
| Hashes were committed before the dice were rolled | **Not met** — posted 32 to 54 min after the roll |
| Commitment is durably archived | **Partial** — X posts only; not on sos.ga.gov |
