---
layout: home
title: Georgia May 2026 RLA — Transparency Analysis
---

# Georgia May 19, 2026 General Primary
## Risk-Limiting Audit — Transparency Analysis

**Version:** v0.1-draft &nbsp;·&nbsp; **Date:** 2026-06-29 &nbsp;·&nbsp;
[v0.1-draft tag](https://github.com/nealmcb/ga-rla-2026-05-replication/releases/tag/v0.1-draft) &nbsp;·&nbsp;
[Repository](https://github.com/nealmcb/ga-rla-2026-05-replication) &nbsp;·&nbsp;
[Comments / Issues](https://github.com/nealmcb/ga-rla-2026-05-replication/issues)

---

## Table of Contents

1. [Key Findings](#key-findings)
2. [BMD Verifiability and the Voter-Verification Gap](#bmd-verifiability-and-the-voter-verification-gap)
3. [Important Caveats](#important-caveats)
4. [About This Repository](#about-this-repository)
5. [Reports](#reports)
6. [Data Artifacts](#data-artifacts)
7. [Scripts](#scripts)
8. [Ballot Image Auditing and Enhanced Voting](#ballot-image-auditing-and-enhanced-voting)
9. [How to Replicate](#how-to-replicate)

---

## Key Findings

**What the audit covered:** Arlo BATCH\_COMPARISON/MACRO audit of two contests — US Senate Republican primary (Dooley vs. Carter runoff) and Democratic Governor's primary (Bottoms vs. Esteves) — across all 159 Georgia counties, 706 batches hand-counted, 5% risk limit met for both contests.

**What this repository verifies:**

- ✓ **Both committed SHA256 hashes verified.** The Georgia Secretary of State tweeted SHA256 hashes of both artifact ZIPs on May 28, 2026 (before any county hand-counting began). Both match the files currently posted for download exactly. The files were not altered during or after the audit.
- ✓ **Ticket numbers independently reproduced.** Four individual batch ticket numbers from the audit report were recomputed from the public seed (`06712221796172622814`) using the open-source `consistent_sampler` library — all four match exactly.
- ✓ **Risk limit met.** P-values 4.91% (Senate Rep) and 4.17% (Governor Dem) are below the 5% threshold.
- ⚠ **BMD batches show 5× higher discrepancy rates than HMPB batches** — expected from the QR-code vs. printed-text read split, but highlights the fundamental voter-verification gap in BMD auditing (see [below](#bmd-verifiability-and-the-voter-verification-gap)).
- ⚠ **Hash commitment was post-seed** (~3 minutes after the random seed was entered), not pre-seed. The SOS explained this was deliberate; it still protects against post-audit alteration but not against insider manipulation in that brief window.
- ⚠ **Commitment lives only on X/Twitter** — not archived on sos.ga.gov and subject to platform link rot.
- ✗ **Only two contests audited.** All other contests on the May 19 ballot have no RLA evidence of accuracy (see [Caveats](#important-caveats)).

---

## BMD Verifiability and the Voter-Verification Gap

Georgia uses two ballot technologies whose interaction with RLA is fundamentally different:

**HMPB (Hand-Marked Paper Ballot):** Used for absentee-by-mail and provisional voting. The voter hand-marks ovals; the scanner reads those same marks; the auditor reads the same physical marks. All three reads apply to the same artifact. HMPB is the gold standard for RLA because the paper ballot directly captures voter intent, and any deviation between scanner and auditor is visible in the audit.

**BMD (Ballot Marking Device):** Used for in-person voting (Election Day and Advance Voting). The voter interacts with a touchscreen; the BMD prints a paper ballot containing **both** a QR code and human-readable text; the scanner reads the QR code; the auditor reads the human-readable text. There are therefore *two independent readings of what the voter intended* — and they can disagree.

### Discrepancy Rates by Ballot Type (from the Audit Report)

The scripts in this repository classify the 706 sampled batches by ballot type using the batch-name conventions embedded in the official manifest:

| Ballot Type | Batches | Ballots | % Batches with Discrepancy |
|-------------|---------|---------|---------------------------|
| Absentee-by-Mail **(HMPB)** | 214 | 5,679 | **6.5%** |
| Provisional **(HMPB)** | 38 | 161 | **5.3%** |
| Election Day **(BMD)** | 269 | 108,070 | **13.8%** |
| Advance Voting **(BMD)** | 118 | 207,771 | **33.9%** |
| Combined/Unknown | 63 | 19,935 | 11.1% |

The ~5× gap between BMD and HMPB discrepancy rates is **expected and documented in the audit literature**: auditors reading printed text will occasionally disagree with machines reading QR codes by one vote in a large batch, without any malicious activity. These discrepancies were small (typically 1–2 votes per batch), varied in direction, and did not change the outcome of either audited contest.

### Why This Still Matters

The MACRO audit **proves that QR codes were counted correctly**. It does **not** prove that QR codes correctly encoded voter intent. That gap can only be closed by voters themselves reviewing the human-readable text at the time of voting and confirming it matches their choices.

Research consistently shows that most voters do not carefully verify their BMD printout before inserting it into the scanner. A systematic attack or error in the BMD encoding logic that produced QR codes inconsistent with printed text would be undetectable by batch-comparison RLA alone; it would only be detectable if voters noticed and reported discrepancies at the time of voting, or if a separate ballot-image audit compared scanner reads to optical reads of the same ballot.

**Policy implication:** The most direct improvement within the current framework is a voter-education campaign encouraging every BMD voter to pause and read the full printed text on their ballot before casting it. A longer-term improvement is expanding HMPB use (absentee by mail or in-person hand-marking options), which eliminates the QR-code trust gap entirely.

The Advance Voting BMD discrepancy rate (33.9%) is substantially higher than the Election Day BMD rate (13.8%), possibly because AV batches are larger (median ~1,760 ballots vs. ~400 for ED), giving more opportunities per batch for a single-vote text-vs-QR difference to appear. This warrants further investigation in future audits.

---

## Important Caveats

1. **Only two contests audited.** The May 19, 2026 ballot included many other contests — congressional primaries, state legislative races, local offices — for which **no statistical audit evidence exists**. The risk-limiting audit result for the US Senate and Governor races should not be interpreted as evidence of accuracy for any other contest.

2. **Post-seed commitment.** The hash commitment tweet arrived ~3 minutes after the random seed was entered and the sample was drawn. While the SOS explained this deliberately prevents giving hand-counters "a number to hit," a true pre-seed commitment (hash posted before the dice roll) would be stronger.

3. **Commitment durability.** The sole record of the hash commitment is an X/Twitter thread. It is not archived on sos.ga.gov or linked from the official SOS audit page.

4. **PPEB draw requires exact software version.** Individual ticket numbers are reproducible (4/4 verified), but fully replicating the complete weighted sample draw (PPEB/MACRO) requires the exact numpy version used by Arlo at audit time, which was not published.

5. **BMD voter verification not measured.** The audit report contains no data on whether voters reviewed their printed ballots. The batch discrepancy statistics in this repository are a proxy for QR-vs-text differences but cannot directly measure the voter-verification rate.

6. **Artifacts hosted on MailChimp, not sos.ga.gov.** Subject to link rot and without durable official archiving.

---

## About This Repository

This repository contains independently executable scripts, analysis, and all official artifacts needed to replicate the transparency checks described in the reports. **The code and analysis were produced by Claude Sonnet 4.6 (Anthropic) under prompts and direction from Neal McBurnett**, an election security researcher and author of [Arlo PR #2350](https://github.com/votingworks/arlo/pull/2350) ("docs: Arlo comparison audit transparency report and guide").

No part of this repository reflects the position of Georgia's Secretary of State, VotingWorks, Anthropic, or any official body. Comments and corrections are welcome as [GitHub Issues](https://github.com/nealmcb/ga-rla-2026-05-replication/issues).

---

## Reports

All reports are rendered as web pages via GitHub Pages:

| Report | Description |
|--------|-------------|
| [Executive Summary](https://nealmcb.github.io/ga-rla-2026-05-replication/reports/README/) | Timeline, key values, SHA256 hashes, recommendations |
| [Hash Commitment Analysis](https://nealmcb.github.io/ga-rla-2026-05-replication/reports/hash_commitment/) | Verification of the @GaSecofState tweet hashes — **VERIFIED** |
| [Transparency Gap Analysis](https://nealmcb.github.io/ga-rla-2026-05-replication/reports/transparency_gap_analysis/) | PR #2350 checklist, BMD vs. HMPB discrepancy table |
| [Sample Reproducibility](https://nealmcb.github.io/ga-rla-2026-05-replication/reports/sample_reproducibility/) | PPEB/MACRO algorithm; 4/4 ticket numbers verified |
| [Manifest & Tally Analysis](https://nealmcb.github.io/ga-rla-2026-05-replication/reports/manifest_and_tally_analysis/) | County statistics, voting-mode breakdown, diluted margins |
| [Artifact Inventory](https://nealmcb.github.io/ga-rla-2026-05-replication/reports/artifact_inventory/) | All download URLs, SHA256/SHA512 checksums, HTTP headers |

---

## Data Artifacts

The official SOS-published files are included verbatim. Checksums can be reproduced with `sha256sum` or `shasum -a 256`.

| File | SHA256 | Tweeted? |
|------|--------|----------|
| [final\_audit\_report.csv](https://github.com/nealmcb/ga-rla-2026-05-replication/blob/main/downloads/final_audit_report.csv) | `1efa76b8…042a8` | — |
| [manifests.zip](https://github.com/nealmcb/ga-rla-2026-05-replication/raw/main/downloads/manifests.zip) | `c31d1f67…17aaf` | ✓ VERIFIED |
| [candidate\_totals.zip](https://github.com/nealmcb/ga-rla-2026-05-replication/raw/main/downloads/candidate_totals.zip) | `2842be86…10312` | ✓ VERIFIED |
| [jasper\_rla\_results\_notice.pdf](https://github.com/nealmcb/ga-rla-2026-05-replication/raw/main/downloads/jasper_rla_results_notice.pdf) | — | — |

Extracted per-county CSVs (159 counties × 2 artifact types) are in [`extracted/manifests/`](https://github.com/nealmcb/ga-rla-2026-05-replication/tree/main/extracted/manifests) and [`extracted/candidate_totals/`](https://github.com/nealmcb/ga-rla-2026-05-replication/tree/main/extracted/candidate_totals).

---

## Scripts

| Script | Description |
|--------|-------------|
| [download\_artifacts.sh](https://github.com/nealmcb/ga-rla-2026-05-replication/blob/main/scripts/download_artifacts.sh) | Reproduce artifact downloads from SOS MailChimp URLs |
| [hash\_artifacts.sh](https://github.com/nealmcb/ga-rla-2026-05-replication/blob/main/scripts/hash_artifacts.sh) | Compute SHA256/SHA512 of all downloads |
| [reproduce\_sample.py](https://github.com/nealmcb/ga-rla-2026-05-replication/blob/main/scripts/reproduce_sample.py) | Verify ticket numbers from public seed using `consistent_sampler` |
| [inspect\_artifacts.py](https://github.com/nealmcb/ga-rla-2026-05-replication/blob/main/scripts/inspect_artifacts.py) | Parse and summarize audit report structure |
| [summarize\_manifests.py](https://github.com/nealmcb/ga-rla-2026-05-replication/blob/main/scripts/summarize_manifests.py) | Summarize ballot manifest statistics |
| [search\_for\_hash.py](https://github.com/nealmcb/ga-rla-2026-05-replication/blob/main/scripts/search_for_hash.py) | Search all files for a given hash prefix |

---

## Ballot Image Auditing and Enhanced Voting

A **ballot image audit** is a distinct and complementary transparency mechanism from an RLA. Georgia's Dominion ImageCast Precinct (ICP) scanners capture a digital image of each ballot as it is scanned. If those images are made public, any member of the public (or software tool) can:

- independently verify how each BMD ballot's printed text was read by the scanner
- compare scanner reads to hand-count reads, at the individual-ballot level
- detect systematic QR-code vs. printed-text disagreements across large numbers of ballots

**[Enhanced Voting](https://enhancedvoting.com)** is a company that operates a public ballot-image review platform and has worked with several jurisdictions to publish ballot images for public scrutiny. Such transparency is especially valuable for BMD-heavy election environments like Georgia's in-person voting.

**What this investigation found:** No public ballot image dataset, Enhanced Voting audit report, or equivalent artifact for Georgia's May 19, 2026 General Primary was identified through this investigation. If such a dataset exists or is available through a public records request to a Georgia county, it would substantially strengthen the transparency picture — particularly for the BMD discrepancies described above.

Readers aware of public Georgia 2026 ballot image availability are encouraged to [open an issue](https://github.com/nealmcb/ga-rla-2026-05-replication/issues) in this repository with details.

---

## How to Replicate

```bash
# Clone the repository (includes all artifacts)
git clone https://github.com/nealmcb/ga-rla-2026-05-replication.git
cd ga-rla-2026-05-replication

# Install Python dependencies
pip install consistent_sampler numpy

# Verify SHA256 hashes of the two committed ZIPs
sha256sum downloads/manifests.zip downloads/candidate_totals.zip
# Expected:
# c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf  downloads/manifests.zip
# 2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312  downloads/candidate_totals.zip

# Reproduce four sample ticket numbers from the public seed
python3 scripts/reproduce_sample.py

# Re-download artifacts from source (optional — to verify the repo copies match)
bash scripts/download_artifacts.sh
```

To replicate the full PPEB weighted draw, the Arlo version (and its numpy dependency version) used at audit time is also required. See the [Sample Reproducibility report](https://nealmcb.github.io/ga-rla-2026-05-replication/reports/sample_reproducibility/) for details.
