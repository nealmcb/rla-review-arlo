---
layout: default
title: Transparency Gap Analysis
---

# Transparency Gap Analysis — Georgia May 19, 2026 RLA
## Comparison to VotingWorks/Arlo PR #2350

**Version:** v0.18 &nbsp;·&nbsp; **Review timestamp:** 2026-07-01T00:00:00Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Reports](../)

---

> **AI-assisted analysis, partially reviewed.** This analysis was produced with significant AI assistance (Claude, Anthropic). Findings are ongoing and some claims may require further verification. Corrections welcome via [GitHub Issues](https://github.com/nealmcb/rla-review-arlo/issues).

## PR #2350 Overview

**Title:** "docs: Arlo comparison audit transparency report and guide"  
**Opened:** June 20, 2026  
**Repository:** `github.com/votingworks/arlo`  
**Related Issue:** #2351 — "Document and support best practices for running robust transparent reproducible audits"

The PR adds three planning documents to Arlo:
- `docs/transparency-report.md` — Current gap analysis across three audit phases
- `docs/transparency-implementation-plan.md` — Two-track implementation plan
- `docs/cloud-testing-deployment-plan.md` — Deployment/testing infrastructure

### Core Transparency Principles (from PR #2350)

1. **Software Independence**: The public must be able to detect election-system or audit-system errors without relying only on the same software stack that produced the audit outputs.

2. **Mechanical Verification**: Observers should be able to replicate the sample draw and risk calculation from published artifacts alone.

3. **Human Verification**: Physically present observers should be able to independently record audit-board interpretations and compare those against Arlo's record, without exposing the audit board to CVRs or expected votes.

4. **Blind Audit Principle**: Audit boards must interpret each ballot without seeing the CVR or expected machine interpretation. Observer tools must not contaminate the audit-board process.

5. **Public Posting Requirement**: Public posting of phase artifacts is required because observers do not have access to the Arlo instance. Arlo-internal availability is not public transparency.

6. **Phase-Based Artifacts**: Transparency is organized around three phases: pre-seed, post-seed/pre-comparison, and post-audit.

---

## Georgia vs. PR #2350 Transparency Checklist

### PRE-SEED PHASE

| Requirement | Georgia Status | Notes |
|-------------|---------------|-------|
| Committed ballot manifest (pre-seed) | Partial | Hash committed at audit start (post-seed, ~3 min after seed entry), not before dice roll |
| Committed candidate totals / batch tallies (pre-seed) | Partial | Same — committed post-seed but before hand-counting began |
| SHA-256 hash or hash-index of committed artifacts | ✓ Present | Both hashes tweeted and **verified** to match currently posted files |
| Durable timestamp on commitment | Partial | X/Twitter post exists; not archived on sos.ga.gov; X imposes access barriers |
| Contest definitions | ✓ Present | In final audit report CONTESTS section |
| Reported outcomes | ✓ Present | In final audit report |
| Risk limit | ✓ Present | 5% (in final audit report) |
| Audit type and sampler parameters | ✓ Present | BATCH_COMPARISON, MACRO (in audit report) |
| Software/tool/version | Partial | Arlo confirmed, version not specified |

### POST-SEED / PRE-COMPARISON PHASE

| Requirement | Georgia Status | Notes |
|-------------|---------------|-------|
| Full random seed | ✓ Present | `06712221796172622814` in final audit report |
| Method for converting dice to seed | ✓ Partial | 20 ten-sided dice, 20-digit number — described in news coverage, not official SOS docs |
| Exact sampler algorithm | ✓ Partial | Arlo consistent_sampler + MACRO (deducible from audit report and Arlo source) |
| Sample size calculation | ✓ Partial | Sample sizes in audit report; MACRO formula in public Arlo code |
| Selected batches (list) | ✓ Present | Listed in final audit report SAMPLED BATCHES section |
| Draw order (ticket numbers) | ✓ Present | Ticket numbers in SAMPLED BATCHES section |
| Retrieval list for counties | Unknown | Not publicly posted; counties presumably received via Arlo |
| Per-jurisdiction sample assignments | Partial | Inferrable from audit report; no official per-county list separately published |
| Ability to reproduce selected sample from public inputs | Partial | Ticket numbers verified reproducible; full PPEB draw requires numpy version |
| Sampler inputs artifact | ✗ Missing | No structured file listing all contest/batch inputs to the sampler |

### POST-AUDIT PHASE

| Requirement | Georgia Status | Notes |
|-------------|---------------|-------|
| Hand-count results | ✓ Present | In final audit report "Audit Results" columns |
| Batch-level audit results | ✓ Present | Aggregate reported vs. hand-counted totals per batch — the expected output for a batch comparison audit |
| Per-ballot audit-board interpretations | N/A (batch audit) | Not expected for MACRO batch comparison; per-ballot interpretation records are only meaningful for ballot-level audits (ballot-comparison or ballot-polling). Batch audits produce aggregate batch totals, not per-ballot records. |
| Discrepancy records | ✓ Present | "Change in Results" and "Change in Margin" in audit report |
| Narrative discrepancy explanations | N/A (batch audit) | Numeric discrepancy counts are the standard and complete output for a batch comparison audit. Narrative explanations (e.g., "stray mark," "undervote") are a ballot-level concept, not applicable to MACRO. |
| County-level tally sheets | Partial | Jasper County PDF found; no systematic county posting |
| Final risk calculation | ✓ Present | Risk levels in final audit report (0.0491 Rep, 0.0417 Dem) |
| Final stopping rule / risk level | ✓ Present | Risk limit met? Yes (in audit report) |
| Machine-readable audit report | ✓ Present | CSV format (Arlo's standard export) |
| Risk calculation reproducible from public artifacts | Partial | MACRO source public; requires Arlo/numpy version |
| Arlo version or audit software version | ✗ Missing | Not published |

---

## Discrepancy Rate by Ballot Type (BMD vs. HMPB)

Georgia uses two ballot types with fundamentally different discrepancy sources:

- **BMD (Ballot Marking Device)**: In-person voting (Election Day, Advance Voting). The machine reads a QR code; the auditor reads the human-readable printed text on the same ballot. Discrepancies arise when the QR-code tally differs from what the auditor tallies from the printed text.
- **HMPB (Hand-Marked Paper Ballot)**: Absentee by Mail and Provisional. The voter hand-marks ovals; the scanner reads those optical marks; the auditor reads the same physical marks. Discrepancies arise from interpretive ambiguity in the ink marks themselves — partial fills, corrections, light marks.

Batch types were classified from the audit report batch name conventions:
- `ICC-Absentee by Mail` / `Absentee by Mail ICC` / `Absentee by Mail` → Absentee-by-Mail (HMPB)
- `ICC-Provisional` / `Provisional` → Provisional (HMPB)
- `AV-...` / `Advance Voting` → Advance Voting (BMD)
- `ED-...` / `Election Day` → Election Day (BMD)

### Results (706 audited batches) — two metrics

The per-batch discrepancy rate and the per-ballot vote discrepancy rate tell very different stories. **Both are shown; the per-ballot rate is the more meaningful comparison.**

| Batch Type | Batches | Median Batch Size | % Batches w/ Disc | \|Δ votes\| | **\|Δ votes\|/1000 bal** | Σ Margin Δ Rep | Σ Margin Δ Dem |
|------------|---------|------------------|-------------------|------------|--------------------------|----------------|----------------|
| Absentee-by-Mail **(HMPB)** | 284 | **24 ballots** | 6.7% | 31 | **2.12‰** | — | — |
| Provisional **(HMPB)** | 12 | 1 ballot | 8.3% | 2 | 111‰ *(18 ballots — not significant)* | — | — |
| Election Day **(BMD)** | 290 | **340 ballots** | 13.8% | 98 | **0.83‰** | 32 | 35 |
| Advance Voting **(BMD)** | 117 | **1,613 ballots** | 34.2% | 126 | **0.60‰** | 47 | 48 |
| **TOTAL** | **706** | — | **14.2%** | **257** | **0.75‰** | **91** | **106** |

### Findings

1. **The per-batch discrepancy rate is dominated by batch size, not ballot type.** The ~5× gap between BMD-AV (34.2%) and HMPB-ABM (6.7%) per-batch rates is almost entirely explained by batch size: a BMD-AV batch averages **1,613 ballots** while an absentee ICC container averages **24 ballots**. A single-vote difference in a 1,613-ballot batch shows up as a batch discrepancy; a single-vote difference in a 24-ballot batch is equally likely but constitutes a far smaller fraction of batches having any error.

2. **Per ballot, HMPB has a higher discrepancy rate than BMD.** At 2.12‰, absentee HMPB batches show 2.5–3.5× more vote discrepancies per ballot than BMD batches (0.60–0.83‰). This is the expected result from audit literature: hand-marked ovals are physically ambiguous in ways that printed BMD text is not. Partially filled marks, pen corrections, and light strokes that pass a scanner threshold but look empty to a human auditor are the primary source of HMPB discrepancies. BMD discrepancies, by contrast, most likely reflect auditor tallying errors on clear printed text — or, in principle, QR-vs-text encoding disagreements that cannot be distinguished from counting errors in the published artifacts.

3. **Within BMD types, Advance Voting (34.2%) far exceeds Election Day (13.8%)** — but the per-ballot rates are similar (0.60‰ vs. 0.83‰). The per-batch gap is again a batch-size artifact: AV median batch is 1,613 ballots vs. 340 for ED.

4. **Discrepancy magnitudes are small.** The total margin change across all 706 audited batches is 91 votes (Rep) and 106 votes (Dem) out of 341,816 ballots hand-counted. No discrepancy was large enough to approach changing the outcome of either contest.

5. **No separate "HMPB/BMD" flag in the published artifacts.** The ballot type must be inferred from batch names. Georgia could improve transparency by explicitly tagging each batch with its ballot type and ballot count in the manifest and audit report. This would also make the batch-size-driven discrepancy rate effect immediately visible in the official artifacts.

For deeper analysis — including the Derrick Jackson directional pattern, the TOOMBS 1-ballot anomaly, batch-size reduction recommendations, and the case that discrepancy causes are undocumented — see the [Discrepancy Analysis report](../discrepancy_analysis/).

---

## Three Independent Check Results

### Check 1: Hash Commitment Check
**Can a public observer confirm that the later-posted batch tallies are exactly the files committed at audit time?**

**Result: ✓ VERIFIED**

The @GaSecofState tweet thread (May 28, 2026, 11:52 AM EDT) committed SHA256 hashes of both artifact ZIPs, apparently after the random seed had been entered and the sample drawn (~3 minutes earlier). Both hashes match the currently posted files exactly:
- `manifests.zip`: `c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf` ✓
- `candidate_totals.zip`: `2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312` ✓

**Caveat — timing:** The tweet came ~3 minutes after the Arlo round was started (seed entered and sample drawn). The commitment is therefore post-seed rather than pre-seed. The tweet thread explains why the actual data files were withheld until hand-counting finished (to avoid giving counters "a number to hit"), but does not address why the hash itself wasn't committed before the seed was entered. The commitment proves the files were not altered after the tweet, but cannot rule out alteration in the brief window between seed entry and the tweet.

**Caveat — durability:** The commitment lives only on X/Twitter and is not archived on sos.ga.gov or linked from the official SOS audit page.

### Check 2: Sample Selection Check
**Can a public observer recompute the selected batches from the committed pre-seed artifacts and the dice-generated random seed?**

**Result: SUBSTANTIALLY YES (with caveats)**

- ✓ The seed is public (in the audit report)
- ✓ Individual batch ticket numbers are exactly reproducible using public `consistent_sampler` library
- ✓ Ticket numbers reproducible (verified for a selection of batches; any batch in the audit report can be independently verified)
- ✗ The full PPEB draw order requires the exact numpy version used by Arlo at audit time
- ✗ No official sampler-inputs artifact was published

An independent observer can verify that individual batches were correctly assigned their ticket numbers. The complete sample order requires matching the numpy random state.

### Check 3: Risk Calculation Check
**Can a public observer recompute the final risk level from the selected sample and hand-count results?**

**Result: SUBSTANTIALLY YES (with effort)**

- ✓ Hand-count results are in the final audit report
- ✓ Reported results per batch are in the audit report
- ✓ MACRO source code is publicly available in the Arlo repo
- ✓ Risk levels (0.0491 Rep, 0.0417 Dem) are stated in the audit report
- ✗ Exact floating-point calculation requires Arlo's Python Decimal arithmetic
- ✗ The ballot count per batch (from manifests) must be correctly joined to candidate totals

---

## What Georgia Does Well

1. **Posts all three major artifact types**: final audit report (with hand counts), ballot manifests, and machine batch tallies — more than most jurisdictions provide
2. **Hash commitment verified**: Both `manifests.zip` and `candidate_totals.zip` hashes were committed in a public tweet thread (apparently after the seed was entered) and match the currently posted files exactly
3. **Includes the random seed in the final audit report** — the seed (`06712221796172622814`) is publicly available
4. **Includes per-batch ticket numbers** — allowing independent verification of any batch in the audit report
5. **Provides machine-readable CSV exports** — not scanned images or PDFs
6. **Public dice-roll event** — 20 participants, observed by media and the public
7. **Covers all 159 counties** — complete statewide scope
8. **5% risk limit** — among the lowest in the country for RLA jurisdictions
9. **First time two contests were audited** — expanded scope is commendable
10. **Explicit transparency rationale communicated**: The tweet thread explained why hashes were committed before files were published — demonstrating deliberate transparency design

---

## Transparency Gaps

1. **Hash commitment is post-seed, not pre-seed**: The tweet appeared ~3 minutes after the Arlo round started (seed entered, sample drawn). It does not prevent a scenario where someone with advance knowledge of the seed and the batches to be drawn could alter batch tallies in that ~3-minute window. Committing the hash before the dice roll would eliminate this residual risk.
2. **Commitment is hosted on X/Twitter only**: Not archived on sos.ga.gov; not linked from the official audit page; X imposes login/payment barriers for access
3. **No sampler inputs file**: There is no structured artifact listing all inputs to the PPEB sampler (contest totals, batch totals, risk limit, numpy seed) as a single machine-readable document
4. **No Arlo version specified**: Observers cannot know which Arlo code version to use for reproduction
5. **No per-jurisdiction transparency artifacts**: No official per-county list of selected batches; counties post their own notices inconsistently
6. **No ballot-type flag in published artifacts**: Batch names encode ballot type (BMD vs. HMPB) implicitly but no explicit field separates them. This makes batch-level discrepancy pattern analysis harder than it needs to be. Discrepancy rates differ substantially by type (BMD: 14–34%, HMPB: 5–7%), and explicitly tagging ballot type in the manifest would enable cleaner post-audit analysis.
7. **No pre-seed manifest commitment**: The manifests were not publicly committed before the dice roll event
8. **Social media dependency**: The critical hash commitment is posted only on X/Twitter — a commercial platform with paywalls and link rot
9. **No durable timestamp**: The tweet commitment lacks cryptographic timestamping or archiving
10. **Arlo instance not accessible to observers**: Observers cannot independently verify what Arlo shows; they must rely on the exported report

---

## Immediate Improvements (No Law Change Required)

Georgia could improve transparency significantly without legislative change:

1. **Post the full SHA256 hash as plain text on the official SOS audit page**, not just in a tweet
2. **Archive the commitment tweet** via Web Archive or similar before publishing the audit results
3. **Commit artifact hashes before the dice roll**, not after — generate the manifests and candidate totals export from Arlo, hash them, post the hash, then roll the dice
4. **Publish the Arlo version** (or git commit) used for each audit
5. **Publish a sampler-inputs file** listing all contest parameters, batch parameters, and the structured inputs to the PPEB calculation
6. **Standardize county-level result posting** — require each county to publish its selected batches and tally sheets in a uniform format
7. **Host all artifacts directly on sos.ga.gov** rather than MailChimp, for durability and auditability
8. **Link all artifact URLs from the permanent SOS audit information page** at `sos.ga.gov/page/elections-audit-information`

---

## Implementation Items from PR #2350 vs. Georgia

| PR #2350 Item | Georgia 2026 Status |
|---------------|---------------------|
| A1: SHA-256 hashing at phase transitions | Partial (hash tweeted; not verifiable) |
| A2: Official export functions for phase artifacts | Partial (Arlo CSV export used; not formally named) |
| A3: replicate_sample.py script | ✗ Not published |
| A3: replicate_risk_level.py script | ✗ Not published |
| A3: end_to_end_verify.py script | ✗ Not published |
| A5: Observer excerpt generator | ✗ Not applicable (MACRO, not ballot-level) |
| B1: Machine-readable JSON audit report | ✗ CSV only (not JSON) |
| B2: Opportunistic contest risk levels | ✗ Not published |
| B3: Per-contest eligible ballot count | ✗ Not published |
| B4: Pre-seed hash-index JSON endpoint | ✗ Not published |
| B5: Per-jurisdiction phase exports | ✗ Not published (inconsistent county postings) |
| B6: UI transparency checklist at phase transitions | ✗ Not applicable externally |
| B8: Trusted timestamping | ✗ Not published |

---

## Distinction: "Audit Was Conducted" vs. "Audit Is Independently Reproducible"

Georgia's 2026 primary RLA was conducted using legitimate procedures: public dice roll, Arlo software, all 159 counties, two contests, 5% risk limit, 706 batches hand-counted. The audit confirmed the election outcome. The process was observed by media and public attendees.

However, from the publicly posted artifacts alone, the audit is **not yet fully independently reproducible** in the sense described by PR #2350:

- The pre-seed hash commitment cannot be verified from current artifacts
- The hash commitment appears to have been posted after (not before) the seed was entered
- The full PPEB sample draw requires an unspecified numpy version
- No independent verification scripts were published
- County-level tally sheet posting is inconsistent

These gaps do not mean the audit was wrong. They mean the audit record does not yet provide the level of public transparency that would allow an independent party to replicate every step from first principles, using only the official public record.

---

## Context and Further Reading

These gaps do not indicate the audit outcome was wrong. Georgia's 2026 RLA is among the strongest public audit records in the country. The goal of this analysis is to identify the specific procedural and publication steps that would move the record from "conducted and credible" to "independently reproducible by any member of the public."

See the [Executive Summary](../README/) for the full recommendation list, and [Arlo Issue #2351](https://github.com/votingworks/arlo/issues/2351) for the ongoing discussion of transparency best practices.

Comments on this analysis are welcome as [GitHub Issues](https://github.com/nealmcb/rla-review-arlo/issues).
