# Investigation Updates — Georgia May 19, 2026 RLA Transparency

**Last updated: 2026-06-29**

---

## Step 1 ✓ — Workspace created
Directory structure: downloads/, headers/, extracted/, hashes/, scripts/, reports/, webpages/, notes/

---

## Step 2 ✓ — All 3 artifacts downloaded

| File | Size | SHA256 |
|------|------|--------|
| final_audit_report.csv | 421 KB | 1efa76b808f82527f72bb5bd81d14de1b820bf9b76534fbfc1a5d71663b042a8 |
| manifests.zip | 299 KB | c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf |
| candidate_totals.zip | 422 KB | 2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312 |

Served via MailChimp / CloudFront. No ETag or Last-Modified headers. ZIP timestamps are 1980-01-01 (zeroed by MailChimp/tool).

---

## Step 3 ✓ — Hash commitment tested

**Known prefix from claimed @GASecofState tweet: `7d00771bf178007f4c6f43bf45b6`**

Result: **NOT FOUND** in any downloaded or extracted file.

None of the 3 downloaded files and none of the 318 extracted files match.

**Most likely explanation:** The candidate_totals.zip was regenerated or recompressed between the May 28 tweet and the June 3 public posting. MailChimp normalizes ZIP metadata (zeroing timestamps to 1980-01-01), which changes the SHA256. The tweeted hash likely corresponded to the original upload to Arlo/MailChimp on May 28, before the file was re-served.

**Status: CANNOT VERIFY from currently available public artifacts.**

---

## Step 4 ✓ — Social media commitment investigated

- @GaSecofState tweet thread beginning 11:52 AM EDT, 05/28/2026 — referenced in SOS June 3 press release
- Arlo round start time in audit report: `2026-05-28T15:49:15 UTC` = 11:49 AM EDT
- **The hash tweets came at least 8 minutes AFTER the dice roll** (8 minutes after the seed was entered into Arlo): manifests hash 15:57:06 UTC, batch totals hash 15:57:15 UTC (from the status IDs; see `src/snowflake_time.py`)
- This means the hash was committed AFTER the sample was drawn, not before — a transparency gap
- Gabriel Sterling X post status/2070235247657287995 — content not directly accessible; its status ID dates it to 2026-06-25 19:58:40 UTC, around the June 16 runoff audit, so it is not part of this thread
- The tweet text/hash were not found in any indexed public source via web search

---

## Step 5 ✓ — Final audit report analyzed

Key findings:
- **Audit type**: BATCH_COMPARISON, MACRO math
- **Risk limit**: 5%
- **Random seed**: `06712221796172622814` (public, in final_audit_report.csv)
- **Round 1 start**: 2026-05-28T15:49:15 UTC
- **Round 1 end**: 2026-06-02T21:28:20 UTC
- **US Senate Rep**: sample 138, p-value 0.0491, risk met
- **Governor Dem**: sample 18, p-value 0.0417, risk met
- **Batches sampled**: 148 jurisdictions × average 4.4 = 706 batches total
- **Ballots in sample total**: 341,816
- **Discrepancies**: 100 batches had some vote count difference (all minor, not outcome-changing)
- Software: Arlo (VotingWorks) confirmed
- NO random seed in the sense of "dice roll produces seed" — seed IS the dice number

---

## Step 6 ✓ — Manifest and candidate totals analyzed

Manifests:
- 159 counties, 5,641 batches, 2,081,564 total ballots
- Voting modes: Election Day (2,743), Absentee by Mail (1,900), Advance Voting (718), Provisional (278)
- Batch sizes: min=0, max=6,381, median=172.5, mean=369.1
- Total matches the reported "Total Ballots Cast" in the audit report ✓

Candidate totals: 159 counties, 5,640 batches with results
Both ZIPs contain one subdirectory per county with one CSV per county.

---

## Step 7 ✓ — Sample reproducibility tested

**FINDING: TICKET NUMBERS ARE REPRODUCIBLE**

Verified 4 ticket numbers from the audit report using:
- `consistent_sampler.first_fraction((county, batch_name), seed)` 
- Trimmed to 18 digits with `consistent_sampler.trim(ticket, 18)`

All 4 verified matches:
- BALDWIN/ED-North Baldwin ICP 1 - 0: `0.427297706310130710` ✓
- BARROW/ICC-Absentee by Mail - 2: `0.9088955580466120027` ✓
- BARTOW/ED-Cartersville West ICP 1 - 0: `0.468722862632969295` ✓
- WARE/AV-Administrative Building ICP 1 - 0: `0.239288422106382693` ✓

**The full MACRO sample DRAW is partially reproducible:**
- The weighted probabilities come from batch-level MACRO error bounds (public data)
- The numpy random.choice() call requires the exact numpy version
- We confirmed: numpy seed = `int(sha256_hex("06712221796172622814"), 16)`

---

## Step 8 ✓ — PR #2350 reviewed

Neal McBurnett's PR adds 3 docs to Arlo repo:
- transparency-report.md: gap analysis across pre-seed, post-seed, post-audit phases
- transparency-implementation-plan.md: two-track implementation (observer toolkit + Arlo improvements)
- cloud-testing-deployment-plan.md: deployment and testing survey

Key principles: software independence, mechanical verification, human/blind audit, public posting requirement.

---

## TIMELINE (constructed from evidence)

| Date/Time | Event | Source |
|-----------|-------|--------|
| May 19, 2026 | Election day | SOS press release |
| ~May 22–27 | Counties upload manifests and candidate totals to Arlo | File timestamps in ZIPs |
| May 28, ~11:49 AM EDT | Dice roll event; seed 06712221796172622814 entered into Arlo; round 1 started | final_audit_report.csv |
| May 28, 11:52 AM EDT | @GaSecofState begins its tweet thread (15:52:40 UTC) | status ID 2060026478759137692 |
| May 28, 11:57 AM EDT | @GaSecofState tweets SHA256 hashes of the manifests (15:57:06 UTC) and batch totals (15:57:15 UTC) | status IDs 2060027592845955437, 2060027632255639963; both hashes verified |
| May 28–June 2 | Counties count 706 batches (706 × 148 batches) | audit report |
| June 2, ~5:28 PM EDT | Audit round 1 completed in Arlo | final_audit_report.csv |
| June 3, 2026 | SOS press release published with artifact links | sos.ga.gov |
| June 5, 2026 | Election certification deadline | news reports |

---

## REPORTS IN PROGRESS

- [ ] reports/README.md — executive summary
- [ ] reports/artifact_inventory.md
- [ ] reports/hash_commitment.md
- [ ] reports/manifest_and_tally_analysis.md
- [ ] reports/sample_reproducibility.md
- [ ] reports/transparency_gap_analysis.md

---

## ALL REPORTS COMPLETE ✓ (2026-06-29 ~15:47 UTC)

- [x] reports/README.md — executive summary + Verified Voting email language
- [x] reports/artifact_inventory.md — all URLs, hashes, HTTP headers
- [x] reports/hash_commitment.md — commitment analysis and timing
- [x] reports/manifest_and_tally_analysis.md — schema, counts, anomalies
- [x] reports/sample_reproducibility.md — 4 ticket numbers verified, PPEB analysis
- [x] reports/transparency_gap_analysis.md — full PR #2350 comparison table

## SCRIPTS COMPLETE ✓

- [x] scripts/download_artifacts.sh
- [x] scripts/hash_artifacts.sh
- [x] scripts/inspect_artifacts.py
- [x] scripts/summarize_manifests.py
- [x] scripts/reproduce_sample.py — all 4 ticket verifications PASS ✓
- [x] scripts/search_for_hash.py — 318 files checked, NO MATCH for prefix 7d00771

---

## 2026-06-29 ~16:05 UTC — Tweet text received

User provided the full @GaSecofState tweet thread text from May 28, 2026.

### Findings from the tweet text:

1. **BOTH HASHES VERIFIED** — not "not found" as initially concluded
   - manifests.zip: `c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf` ✓ EXACT MATCH
   - candidate_totals.zip: `2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312` ✓ EXACT MATCH

2. **The briefing's "known prefix" `7d00771bf178007f4c6f43bf45b6` was WRONG**
   — it does not appear in the actual tweet and does not match any artifact

3. **TWO hashes were committed, not one** — both manifests AND candidate_totals

4. **SOS's explicit rationale**: committed hashes after sample draw but before hand-counting,
   to prevent giving counters "a number to hit" — a deliberate, explained design choice

5. **Account is @GaSecofState** (mixed case), not @GASecofState (all caps) as in the briefing

6. **Tweet timing**: the thread began at 15:52:40 UTC (shown as 9:52 AM MDT); the hash tweets
   are 15:57:06 and 15:57:15 UTC, at least 8 minutes after the dice roll (the seed was entered at 15:49:15 UTC)

7. **Files were NOT regenerated** — the MailChimp URL timestamps reflect link creation,
   not file regeneration; the actual bytes match the May 28 commitment exactly

### Updated reports:
- reports/README.md — executive summary rewritten, hash = VERIFIED
- reports/hash_commitment.md — completely rewritten, status = VERIFIED
- reports/transparency_gap_analysis.md — Check 1 corrected to VERIFIED, gaps updated
