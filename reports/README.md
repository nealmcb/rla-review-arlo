---
layout: default
title: Executive Summary
---

# Georgia May 19, 2026 General Primary RLA — Executive Summary

**Investigation date:** 2026-06-29  
**Repository:** [github.com/nealmcb/ga-rla-2026-05-replication](https://github.com/nealmcb/ga-rla-2026-05-replication) &nbsp;·&nbsp; [Back to main page](../)

---

## Executive Summary

Georgia conducted a statewide Risk-Limiting Audit (RLA) of its May 19, 2026 General Primary and Nonpartisan General Election. The audit used Arlo (VotingWorks) software with BATCH_COMPARISON/MACRO math, covering two contests — the Republican US Senate primary and the Democratic Governor's primary — across all 159 counties, with a 5% risk limit.

Three artifact files were publicly posted on June 3, 2026:
1. Final audit report (CSV) — includes seed, sample, hand counts, risk levels
2. Ballot manifests (ZIP, 159 county CSVs)
3. Machine batch tallies / candidate totals (ZIP, 159 county CSVs)

On May 28, 2026 at 11:52 AM EDT, @GaSecofState published a four-tweet thread committing SHA256 hashes of **both** the ballot manifests and the machine-counted batch totals before the hand-counting began. The thread explicitly explained the rationale: publishing the files themselves before auditing concluded might give counters "a number to hit," so hashes were used instead.

**Both committed hashes have been independently verified.** The files currently posted for download are byte-for-byte identical to the files hashed in the tweet. This is a meaningful and successful transparency measure.

**Individual batch ticket numbers ARE reproducible** from the public seed using the open-source `consistent_sampler` library. Four ticket numbers from the audit report were independently verified with exact matches.

**The audit outcome is credible.** The risk limit was met for both contests (p-values 4.91% and 4.17%), 706 batches were hand-counted across all 159 counties, and discrepancies were minor and not outcome-changing.

**Remaining limitations:** The hash commitment was made ~3 minutes after the random seed was entered (post-seed, not pre-seed), and lives only on X/Twitter rather than a durable official page. The full MACRO sample draw requires the Arlo/numpy version used (not published). No independent verification scripts were provided.

---

## Timeline

| Date/Time (EDT) | Event |
|----------------|-------|
| May 19, 2026 | Election day |
| May 22–27, 2026 | Counties upload manifests and candidate totals to Arlo (per file timestamps in ZIPs) |
| May 28, ~11:49 AM EDT | Public dice roll; seed `06712221796172622814` entered into Arlo; sample drawn (15:49:15 UTC) |
| May 28, 11:52 AM EDT | @GaSecofState tweets SHA256 hashes of **both** manifests.zip and candidate_totals.zip (15:52 UTC, ~3 min after seed entry) |
| May 28–June 2 | 159 counties hand-count 706 batches |
| June 2, ~9:28 PM EDT | Round 1 completed in Arlo (21:28:20 UTC) |
| June 3, 2026 | SOS press release with artifact download links on MailChimp |
| June 5, 2026 | Election certification deadline |

---

## Key Computed Values

| Item | Value |
|------|-------|
| Random seed | `06712221796172622814` |
| Audit type | BATCH_COMPARISON (MACRO) |
| Risk limit | 5% |
| US Senate Rep — p-value | 0.0491 (4.91%) — risk met |
| Governor Dem — p-value | 0.0417 (4.17%) — risk met |
| Batches sampled | 706 |
| Ballots in sample | 341,816 |
| Total ballots in manifests | 2,081,564 |
| Counties | 159 |
| Total manifest batches | 5,641 |
| US Senate Rep diluted margin | 0.0222 (Dooley vs. Carter) |
| Gov Dem diluted margin | 0.1952 (Bottoms vs. Esteves) |

---

## Full SHA256 Hashes of Posted Artifacts

```
1efa76b808f82527f72bb5bd81d14de1b820bf9b76534fbfc1a5d71663b042a8  final_audit_report.csv
c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf  manifests.zip        ← tweeted ✓
2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312  candidate_totals.zip ← tweeted ✓
```

---

## Whether the Social Media Commitment Was Found

**Status: Confirmed — tweet thread text provided by investigator.**

The @GaSecofState thread from May 28, 2026 at 11:52 AM EDT (shown as 9:52 AM MDT in the viewer's timezone) committed both artifact hashes. The thread explained the rationale in plain language. The tweet URL was not provided in the SOS press release and is not durably archived on sos.ga.gov, but the content is confirmed.

**Note:** The investigation briefing specified a "known prefix" of `7d00771bf178007f4c6f43bf45b6`. This prefix does not match either of the actual tweeted hashes and appears to have been incorrect. The actual committed hashes are the full 64-character values shown above.

---

## Whether the Hash Matched

**Status: ✓ VERIFIED — both hashes match exactly.**

| File | Tweeted Hash | Computed Hash | Match |
|------|-------------|---------------|-------|
| `manifests.zip` | `c31d1f67...17aaf` | `c31d1f67...17aaf` | ✓ |
| `candidate_totals.zip` | `2842be86...0312` | `2842be86...0312` | ✓ |

The files currently posted are the same bytes committed in the May 28 tweet. The MailChimp URL timestamps (`2026_06_02T...`) reflect the press-release link creation date, not file regeneration.

---

## Whether Sample Selection Was Reproducible

**Status: SUBSTANTIALLY YES (ticket numbers verified; full PPEB draw requires numpy version).**

- ✓ Seed is public: `06712221796172622814`
- ✓ Individual batch ticket numbers reproduced exactly (4/4 verified)
- ✓ Sampler algorithm (consistent_sampler) is public and pip-installable
- ✓ Manifests and candidate totals are public
- ✗ Full PPEB/MACRO weighted draw requires exact numpy version (not published)
- ✗ No official sampler-inputs artifact published

---

## Most Important Transparency Gaps

1. **Hash commitment is post-seed, not pre-seed**: The tweet came ~3 minutes after the Arlo round started (seed entered, sample drawn). The SOS deliberately chose this timing to prevent "a number to hit," but a true pre-commitment would precede the dice roll by hours or days, eliminating even the theoretical insider-knowledge risk.

2. **Commitment lives only on X/Twitter**: The tweet is the sole durable record. It is not archived on sos.ga.gov, not linked from the permanent audit information page, and X/Twitter imposes access barriers. Future platform changes could make it inaccessible.

3. **No sampler-inputs artifact**: No structured file documents all inputs to the PPEB sampler (contest totals, batch totals, risk limit, seed) as a single machine-readable artifact.

4. **Arlo/numpy version not specified**: Exact reproducibility of the PPEB sample draw requires knowing which software versions were used.

5. **Artifacts hosted on MailChimp, not sos.ga.gov**: Subject to link rot; not linked from the permanent SOS audit information page.

6. **No county-level standardized posting**: Batch assignment lists and tally sheets are posted by counties inconsistently (only Jasper County PDF found in this investigation).

7. **No observer verification scripts**: No published `replicate_sample.py` or `replicate_risk_level.py` scripts.

---

## Recommendations

### Immediate (no law change)
1. **Archive the tweet** via web.archive.org and link the archive from sos.ga.gov/page/elections-audit-information
2. **Post full hashes as plain text on sos.ga.gov** alongside the artifact links
3. **Commit hashes before the dice roll** — export, hash, post to sos.ga.gov, *then* roll the dice. This is the single highest-impact improvement.
4. Publish the Arlo version and numpy version used
5. Publish a structured sampler-inputs file
6. Host all artifacts on sos.ga.gov with permanent, durable URLs

### Medium term
7. Require standardized county-level batch result posting
8. Publish `replicate_sample.py` and `replicate_risk_level.py` as companion scripts
9. Publish a machine-readable JSON audit report endpoint alongside the CSV

### Policy
10. Formalize the pre-seed commitment protocol in the state RLA procedures manual

---

## Files in This Repository

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
| `hashes/downloads.sha512.txt` | SHA512 of all downloaded files |
| `hashes/extracted_files.sha256.txt` | SHA256 of all extracted files |
| `scripts/download_artifacts.sh` | Shell script to reproduce downloads |
| `scripts/hash_artifacts.sh` | Shell script to reproduce hash computation |
| `scripts/reproduce_sample.py` | Python: reproduce ticket numbers from public seed |
| `scripts/search_for_hash.py` | Python: search for hash values |
| `scripts/inspect_artifacts.py` | Python: inspect and summarize audit report structure |
| `scripts/summarize_manifests.py` | Python: summarize ballot manifest data |
| `reports/artifact_inventory.md` | File inventory with hashes and HTTP header notes |
| `reports/hash_commitment.md` | Hash commitment verification analysis (VERIFIED) |
| `reports/manifest_and_tally_analysis.md` | Manifest and candidate tally schema analysis |
| `reports/sample_reproducibility.md` | Sample selection reproducibility analysis |
| `reports/transparency_gap_analysis.md` | PR #2350 comparison and gap analysis |
| `notes/updates.md` | Running investigation updates |

---

## Comparison to Arlo PR #2350 Transparency Framework

[Arlo PR #2350](https://github.com/votingworks/arlo/pull/2350) ("docs: Arlo comparison audit transparency report and guide", opened June 20, 2026) establishes a three-phase transparency framework for comparison audits — pre-seed, post-seed/pre-comparison, and post-audit — and distinguishes "audit was conducted" from "audit is independently reproducible." The full checklist comparison appears in the [Transparency Gap Analysis](transparency_gap_analysis/).

**What Georgia already does well:**
Georgia posts all three major artifact types (report, manifests, tallies) in machine-readable CSV format, includes the random seed in the report, lists per-batch ticket numbers, held a public dice-roll event, expanded to two contests in 2026, achieved a 5% risk limit, and committed both artifact hashes on social media before hand-counting began — placing it ahead of most US jurisdictions.

**Remaining transparency gaps:**
The hash commitment was made post-seed (~3 minutes after seed entry) rather than pre-seed, and is hosted only on X/Twitter rather than a durable official location. The sampler-inputs artifact, Arlo/numpy version, independent verification scripts, standardized county-level result posting, and an explicit ballot-type field in the manifests are absent.

**Path forward:**
Commit hashes before the dice roll; archive the commitment and link it from sos.ga.gov; publish the Arlo/numpy versions and a sampler-inputs file; host artifacts on sos.ga.gov; add an explicit BMD/HMPB field to manifests to enable cleaner post-audit analysis.

Comments and suggestions are welcome as [GitHub Issues](https://github.com/nealmcb/ga-rla-2026-05-replication/issues).
