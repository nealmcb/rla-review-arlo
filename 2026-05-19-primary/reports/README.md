---
layout: default
title: Executive Summary
---

# Georgia May 19, 2026 General Primary RLA — Executive Summary

**Version:** v0.9 &nbsp;·&nbsp; **Review timestamp:** 2026-06-29T23:18:24Z  
**Repository:** [github.com/nealmcb/rla-review-arlo](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [Back to main page](../)

---

## Executive Summary

Georgia conducted a statewide Risk-Limiting Audit (RLA) of its May 19, 2026 General Primary. The audit used Arlo (VotingWorks) software with BATCH_COMPARISON/MACRO math, covering two contests — the Republican US Senate primary and the Democratic Governor's primary — across all 159 counties, with a 5% risk limit.

Three artifact files were publicly posted on June 3, 2026:
1. Final audit report (CSV) — includes seed, sample, hand counts, risk levels
2. Ballot manifests (ZIP, 159 county CSVs)
3. Machine batch tallies / candidate totals (ZIP, 159 county CSVs)

On May 28, 2026 at 11:52 AM EDT, @GaSecofState published a four-tweet thread committing SHA256 hashes of **both** the ballot manifests and the machine-counted batch totals. The official `final_audit_report.csv` records the Round 1 start time as 15:49:15 UTC (11:49 AM EDT) — approximately 3 minutes before the tweet. The tweet thread explains why the actual files were withheld until hand-counting finished (to avoid giving auditors "a number to hit"); it does not address why the hash wasn't committed before the seed was entered.

**Both committed hashes have been independently verified.** The files currently posted for download are byte-for-byte identical to the files hashed in the tweet.

**Individual batch ticket numbers are reproducible** from the public seed using the open-source `consistent_sampler` library. Ticket numbers for a selection of batches from the audit report were independently verified with exact matches; any batch in the audit report can be verified the same way.

**The risk limit was met for both contests** (risk levels 4.91% and 4.17%), 706 batches were hand-counted across all 159 counties, and discrepancies were minor and not outcome-changing.

**Remaining limitations:** The hash commitment was made ~3 minutes after the random seed was entered (post-seed, not pre-seed), and lives only on X/Twitter rather than a durable official page. The full MACRO sample draw requires the Arlo/numpy version used (not published with the audit artifacts).

---

## Timeline

| Date/Time (EDT) | Event |
|----------------|-------|
| May 19, 2026 | Election day |
| May 22–27, 2026 | Counties upload manifests and candidate totals to Arlo (per file timestamps in ZIPs) |
| May 28, 11:49 AM EDT | Random seed `06712221796172622814` entered into Arlo; Round 1 started (15:49:15 UTC per audit report) |
| May 28, 11:52 AM EDT | @GaSecofState tweets SHA256 hashes of **both** manifests.zip and candidate_totals.zip (~15:52 UTC, ~3 min after seed entry) |
| May 28–June 2 | 159 counties hand-count 706 batches |
| June 2, ~9:28 PM EDT | Round 1 completed in Arlo (21:28:20 UTC per audit report) |
| June 3, 2026 | SOS press release with artifact download links on MailChimp |
| June 5, 2026 | Election certification deadline |

---

## Key Computed Values

| Item | Value |
|------|-------|
| Random seed | `06712221796172622814` |
| Audit type | BATCH_COMPARISON (MACRO) |
| Risk limit | 5% |
| US Senate Rep — risk level | 0.0491 (4.91%) — risk limit met |
| Governor Dem — risk level | 0.0417 (4.17%) — risk limit met |
| Batches sampled | 706 |
| Ballots in sample | 341,816 |
| Total ballots in manifests | 2,081,564 |
| Counties | 159 |
| Total manifest batches | 5,641 |
| US Senate Rep diluted margin | 0.0222 (Dooley vs. Carter) |
| Gov Dem diluted margin | 0.1952 (Bottoms vs. Esteves) |

---

## SHA256 Hashes of Posted Artifacts

```
1efa76b808f82527f72bb5bd81d14de1b820bf9b76534fbfc1a5d71663b042a8  final_audit_report.csv
c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf  manifests.zip        ← tweeted ✓
2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312  candidate_totals.zip ← tweeted ✓
```

---

## Whether the Hash Commitment Was Verified

**Status: ✓ VERIFIED — both hashes match exactly.**

| File | Tweeted Hash | Computed Hash | Match |
|------|-------------|---------------|-------|
| `manifests.zip` | `c31d1f67...17aaf` | `c31d1f67...17aaf` | ✓ |
| `candidate_totals.zip` | `2842be86...0312` | `2842be86...0312` | ✓ |

The files currently posted are the same bytes committed in the May 28 tweet. The MailChimp URL timestamps (`2026_06_02T...`) reflect the press-release link creation date, not file regeneration. See the [Hash Commitment Analysis](../hash_commitment/) for full timing discussion.

---

## Whether Sample Selection Was Reproducible

**Status: SUBSTANTIALLY YES — ticket numbers verified; full PPEB draw requires matching numpy version.**

- ✓ Seed is public: `06712221796172622814`
- ✓ Individual batch ticket numbers reproducible from seed (verified for a selection of batches; any batch in the audit report can be independently verified using `consistent_sampler`)
- ✓ Sampler algorithm (`consistent_sampler`) is public and pip-installable
- ✓ Manifests and candidate totals are public
- ✓ Full PPEB weighted draw reproduced: 134/134 Senate Rep + 18/18 Governor Dem (requires numpy 1.26.4)
- ✗ Arlo/numpy versions not published alongside audit artifacts (numpy version derivable from Arlo's public `poetry.lock`)
- ✗ No sampler-inputs artifact published

---

## Most Important Transparency Gaps

1. **Hash commitment is post-seed, not pre-seed.** The tweet came ~3 minutes after the Arlo round was started (seed entered, sample drawn). The SOS explains why the data files were withheld (to avoid "a number to hit"), but the hash itself could have been committed hours before the dice roll with no procedural change.

2. **Commitment lives only on X/Twitter.** Not archived on sos.ga.gov, not linked from the permanent SOS audit information page. X/Twitter imposes access barriers and may not be durable.

3. **No sampler-inputs artifact.** No structured file documents all inputs to the PPEB sampler (contest totals, batch totals, risk limit, seed) as a single machine-readable artifact.

4. **Arlo/numpy version not specified** in published artifacts. Exact reproducibility of the PPEB sample draw depends on these versions.

5. **Artifacts hosted on MailChimp, not sos.ga.gov.** Subject to link rot.

6. **No county-level standardized posting.** Batch assignment lists and tally sheets are posted by counties inconsistently (only Jasper County PDF found).

---

## Recommendations

### Immediate (no law change required)
1. Archive the tweet via web.archive.org and link from sos.ga.gov/page/elections-audit-information
2. Post full SHA256 hashes as plain text on sos.ga.gov alongside the artifact links
3. **Commit hashes before the dice roll** — hash and post to sos.ga.gov *before* the seed is entered; this is the single highest-impact improvement
4. Publish the Arlo version and numpy version used
5. Publish a structured sampler-inputs file
6. Host all artifacts on sos.ga.gov with permanent, durable URLs

### Medium term
7. Require standardized county-level batch result posting
8. Publish `reproduce_sample.py` and `reproduce_risk_level.py` as official companion scripts
9. Publish a machine-readable JSON audit report endpoint alongside the CSV

### Policy
10. Formalize the pre-seed commitment protocol in the state RLA procedures manual

---

## Files in This Audit Directory (`2026-05-19-primary/`)

| File | Description |
|------|-------------|
| `downloads/final_audit_report.csv` | Final audit report (Arlo CSV export) |
| `downloads/manifests.zip` | Ballot manifests (159 county CSVs) — hash verified ✓ |
| `downloads/candidate_totals.zip` | Machine batch tallies (159 county CSVs) — hash verified ✓ |
| `downloads/jasper_rla_results_notice.pdf` | Jasper County RLA Results Notice |
| `headers/` | HTTP response headers from all downloads |
| `extracted/manifests/` | Extracted manifest CSVs (159 counties) |
| `extracted/candidate_totals/` | Extracted candidate totals CSVs (159 counties) |
| `hashes/downloads.sha256.txt` | SHA256 of all downloaded files |
| `hashes/extracted_files.sha256.txt` | SHA256 of all extracted files |

**Scripts** (in `src/` at the repository root):

| Script | Purpose |
|--------|---------|
| `src/download_artifacts.sh` | Reproduce artifact downloads |
| `src/hash_artifacts.sh` | Recompute SHA256 checksums |
| `src/reproduce_sample.py` | Verify ticket numbers from public seed |
| `src/search_for_hash.py` | Search for SHA256 hash values |
| `src/inspect_artifacts.py` | Inspect and summarize audit report |
| `src/summarize_manifests.py` | Summarize ballot manifest data |

---

## Comparison to Arlo PR #2350 Transparency Framework

[Arlo PR #2350](https://github.com/votingworks/arlo/pull/2350) ("docs: Arlo comparison audit transparency report and guide", opened June 20, 2026) establishes a three-phase transparency framework for comparison audits — pre-seed, post-seed/pre-comparison, and post-audit — and distinguishes "audit was conducted" from "audit is independently verifiable." The full checklist comparison appears in the [Transparency Gap Analysis](../transparency_gap_analysis/).

**What Georgia already does well:**
Georgia posts all three major artifact types (report, manifests, tallies) in machine-readable CSV format, includes the random seed in the report, lists per-batch ticket numbers, held a public dice-roll event, expanded to two contests in 2026, met the 5% risk limit, and committed both artifact hashes on social media before hand-counting began — placing it ahead of most US jurisdictions.

**Remaining transparency gaps:**
The hash commitment was made post-seed (~3 minutes after seed entry) rather than pre-seed, and is hosted only on X/Twitter. The sampler-inputs artifact, Arlo/numpy version, independent verification scripts, standardized county-level result posting, and an explicit ballot-type field in the manifests are absent.

**Path forward:**
Commit hashes before the dice roll; archive the commitment and link it from sos.ga.gov; publish the Arlo/numpy versions and a sampler-inputs file; host artifacts on sos.ga.gov; add an explicit BMD/HMPB field to manifests.

Comments and suggestions are welcome as [GitHub Issues](https://github.com/nealmcb/rla-review-arlo/issues).
