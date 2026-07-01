---
layout: home
title: Georgia May 2026 RLA — Review
---

# Georgia May 19, 2026 General Primary
## Risk-Limiting Audit — Transparency Review

**Version:** v0.12 &nbsp;·&nbsp; **Review timestamp:** 2026-06-29T23:18:24Z &nbsp;·&nbsp;
[v0.12 tag](https://github.com/nealmcb/rla-review-arlo/releases/tag/v0.12) &nbsp;·&nbsp;
[Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp;
[Comments / Issues](https://github.com/nealmcb/rla-review-arlo/issues)

---

## Table of Contents

1. [Key Findings](#key-findings)
2. [BMD Verifiability and the Voter-Verification Gap](#bmd-verifiability-and-the-voter-verification-gap)
3. [Important Caveats](#important-caveats)
4. [Reports](#reports)
5. [Data Artifacts](#data-artifacts)
6. [Scripts](#scripts)
7. [Ballot Image Audit (Enhanced Voting)](#ballot-image-audit-enhanced-voting)
8. [How to Replicate](#how-to-replicate)

---

## Key Findings

**What the audit covered:** Arlo BATCH\_COMPARISON/MACRO audit of two contests — US Senate Republican primary (Dooley vs. Carter runoff) and Democratic Governor's primary (Bottoms vs. Esteves) — across all 159 Georgia counties, 706 batches hand-counted, 5% risk limit met for both contests.

**What this review verifies:**

- ✓ **Both committed SHA256 hashes verified.** On May 28, 2026 at 11:52 AM EDT, @GaSecofState tweeted SHA256 hashes of both artifact ZIPs — apparently after the random seed had been entered and the sample drawn (~3 minutes earlier). Both hashes match the files currently posted for download exactly. The files were not altered after that point.
- ✓ **Full PPEB sample draw independently reproduced.** All 134 US Senate and 18 Governor batches (100%) were reproduced using numpy 1.26.4 (matching Arlo's `poetry.lock` pin) and the established batch ordering.
- ✓ **Risk limit met.** Risk levels 4.91% (Senate Rep) and 4.17% (Governor Dem) are below the 5% threshold.
- ⚠ **Hash commitment was post-seed** (~3 minutes after the random seed was entered and the sample drawn). The @GaSecofState tweet explains why they withheld the actual data files until after hand-counting finished (to avoid giving counters "a number to hit"). However, their stated rationale does not address why the hash itself wasn't committed before the seed was entered — which would be the stronger protection. In those ~3 minutes, someone with advance knowledge of the batches to be drawn could have altered the files before they were committed. See the [Hash Commitment Analysis](reports/hash_commitment/) for full discussion.
- ⚠ **Commitment lives only on X/Twitter** — not archived on sos.ga.gov and subject to platform link rot.
- ✗ **Only two contests audited.** All other contests on the May 19 ballot have no RLA evidence of accuracy (see [Caveats](#important-caveats)).

---

## BMD Verifiability and the Voter-Verification Gap

Georgia uses two ballot technologies whose interaction with RLA is fundamentally different:

**HMPB (Hand-Marked Paper Ballot):** Used for absentee-by-mail and provisional voting. The voter hand-marks ovals; the scanner reads those same marks; the auditor reads the same physical marks. All three reads apply to the same artifact. HMPB is the gold standard for RLA because the paper ballot directly captures voter intent, and any deviation between scanner and auditor is visible in the audit.

**BMD (Ballot Marking Device):** Used for in-person voting (Election Day and Advance Voting). The voter interacts with a touchscreen; the BMD prints a paper ballot containing **both** a QR code and human-readable text; the scanner reads the QR code; the auditor reads the human-readable text. There are therefore *two independent encodings of what the voter chose* — and they can disagree.

### What the audit does and does not establish

This MACRO audit compares, for each sampled batch, the sum of QR-code scanner reads against the sum of auditor reads of the printed text. When these match, it provides evidence of consistency between the two encodings. When they differ, it counts as a discrepancy in the MACRO risk calculation.

**What it cannot establish:** Whether QR codes correctly encoded voter intent at the time of printing. That gap can only be narrowed by voters themselves reviewing the human-readable text at the time of voting and confirming it matches their choices — something research consistently shows most voters do not do carefully.

### Discrepancy Rates by Ballot Type

The scripts in this repository classify the 706 audited batches by ballot type using batch-name conventions in the official manifest. Two metrics are shown; the per-ballot rate is the more meaningful one:

| Ballot Type | Batches | Median Batch Size | % Batches w/ Discrepancy | \|Δ votes\| / 1000 ballots |
|-------------|---------|------------------|--------------------------|---------------------------|
| Absentee-by-Mail **(HMPB)** | 284 | **24 ballots** | 6.7% | **2.12‰** |
| Election Day **(BMD)** | 290 | **340 ballots** | 13.8% | **0.83‰** |
| Advance Voting **(BMD)** | 117 | **1,613 ballots** | 34.2% | **0.60‰** |

**The per-batch column is misleading.** The ~5× gap in per-batch rates (6.7% HMPB vs. 34.2% AV-BMD) is overwhelmingly a batch-size artifact: an AV scanner batch averaging 1,613 ballots has far more opportunities per batch for a single-vote discrepancy to appear than a 24-ballot absentee container. When measured per ballot, the pattern inverts — **HMPB has 2.5–3.5× more vote discrepancies per ballot than BMD**, likely driven by interpretive ambiguity in hand-marked ovals.

Discrepancy magnitudes were small (typically 1–2 votes per batch) and did not change the outcome of either contest. The causes of individual discrepancies — whether auditor tallying error, QR-vs-text encoding disagreement, or other factors — are **not documented in any published Georgia artifact**. See the [Discrepancy Analysis report](reports/discrepancy_analysis/) for full detail.

### Why BMD discrepancies exist at all

On a BMD ballot, the printed text is clear and unambiguous — unlike hand-marked ovals. A discrepancy therefore reflects either (a) an auditor tallying error while counting a large batch of printed ballots, or (b) a genuine disagreement between what the QR code encoded and what the printed text says. The audit data does not distinguish these two cases.

Georgia does not recount discrepant batches to determine the cause, so the intrinsic ambiguity in the discrepancy totals cannot be resolved from the published artifacts. The published "Change in Results" numbers are the net differences observed, not a full accounting of what happened in any individual batch.

**The most important gap this audit cannot address:** We have no direct data on whether voters verified their BMD printouts. A systematic encoding error that affected QR codes but not printed text would not be detectable by batch-comparison RLA alone.

### Policy implications

The most direct improvement within the current framework is a voter-education effort encouraging every BMD voter to pause and read the full printed text before inserting the ballot. A longer-term improvement is expanding HMPB use (absentee by mail or in-person hand-marking options), which eliminates the QR-code trust gap entirely.

The per-batch BMD discrepancy rates are substantially higher than HMPB rates — but this is a batch-size effect, not a quality difference. See the [Discrepancy Analysis report](reports/discrepancy_analysis/) for batch size statistics, the Derrick Jackson net-discrepancy pattern, and the TOOMBS one-ballot anomaly.

---

## Important Caveats

1. **Only two contests audited.** The May 19, 2026 ballot included many other contests — congressional primaries, state legislative races, local offices — for which **no statistical audit evidence exists**. The risk-limiting audit result for the US Senate and Governor races should not be interpreted as evidence of accuracy for any other contest.

2. **Post-seed commitment.** The hash commitment tweet arrived ~3 minutes after the random seed was entered and the sample was drawn. A pre-seed commitment (hash posted before the dice roll) would be a stronger protection.

3. **Commitment durability.** The sole record of the hash commitment is an X/Twitter thread. It is not archived on sos.ga.gov or linked from the official SOS audit page.

4. **PPEB draw requires exact numpy version.** Full reproduction (134/134 Sen Rep + 18/18 Gov Dem) requires numpy 1.26.4, matching Arlo's `poetry.lock` pin. This version was not published with the audit artifacts, though it is derivable from Arlo's public lock file.

5. **BMD voter verification not measured.** The audit report contains no data on whether voters reviewed their printed ballots. The batch discrepancy statistics reflect differences between QR-code and printed-text reads but cannot measure the voter-verification rate.

6. **Artifacts hosted on MailChimp, not sos.ga.gov.** Subject to link rot and without durable official archiving.

---

## Reports

All reports are rendered as web pages via GitHub Pages:

| Report | Description |
|--------|-------------|
| [Executive Summary](reports/README/) | Timeline, key values, SHA256 hashes, recommendations |
| [Hash Commitment Analysis](reports/hash_commitment/) | Verification of the @GaSecofState tweet hashes — **VERIFIED** |
| [Transparency Gap Analysis](reports/transparency_gap_analysis/) | PR #2350 checklist, BMD vs. HMPB discrepancy table |
| [Sample Reproducibility](reports/sample_reproducibility/) | PPEB/MACRO algorithm; 134/134 + 18/18 full sample reproduced |
| [Discrepancy Analysis](reports/discrepancy_analysis/) | Per-ballot rates; batch size effects; Jackson pattern; TOOMBS anomaly |
| [Manifest & Tally Analysis](reports/manifest_and_tally_analysis/) | County statistics, voting-mode breakdown, diluted margins |
| [Artifact Inventory](reports/artifact_inventory/) | All download URLs, SHA256 checksums, HTTP headers |

---

## Data Artifacts

The official SOS-published files are included verbatim. Checksums can be reproduced with `sha256sum` or `shasum -a 256`.

| File | SHA256 | Tweeted? |
|------|--------|----------|
| [final\_audit\_report.csv](https://github.com/nealmcb/rla-review-arlo/blob/main/2026-05-19-primary/downloads/final_audit_report.csv) | `1efa76b8…042a8` | — |
| [manifests.zip](https://github.com/nealmcb/rla-review-arlo/raw/main/2026-05-19-primary/downloads/manifests.zip) | `c31d1f67…17aaf` | ✓ VERIFIED |
| [candidate\_totals.zip](https://github.com/nealmcb/rla-review-arlo/raw/main/2026-05-19-primary/downloads/candidate_totals.zip) | `2842be86…10312` | ✓ VERIFIED |
| [jasper\_rla\_results\_notice.pdf](https://github.com/nealmcb/rla-review-arlo/raw/main/2026-05-19-primary/downloads/jasper_rla_results_notice.pdf) | — | — |

Extracted per-county CSVs are in [`extracted/manifests/`](https://github.com/nealmcb/rla-review-arlo/tree/main/2026-05-19-primary/extracted/manifests) and [`extracted/candidate_totals/`](https://github.com/nealmcb/rla-review-arlo/tree/main/2026-05-19-primary/extracted/candidate_totals).

---

## Scripts

All scripts live in [`src/`](https://github.com/nealmcb/rla-review-arlo/tree/main/src) at the repository root and read data from `2026-05-19-primary/`.

| Script | Description |
|--------|-------------|
| [download\_artifacts.sh](https://github.com/nealmcb/rla-review-arlo/blob/main/src/download_artifacts.sh) | Reproduce artifact downloads from SOS MailChimp URLs |
| [hash\_artifacts.sh](https://github.com/nealmcb/rla-review-arlo/blob/main/src/hash_artifacts.sh) | Compute SHA256 of all downloads and extracted files |
| [reproduce\_sample.py](https://github.com/nealmcb/rla-review-arlo/blob/main/src/reproduce_sample.py) | Verify ticket numbers from public seed using `consistent_sampler` |
| [inspect\_artifacts.py](https://github.com/nealmcb/rla-review-arlo/blob/main/src/inspect_artifacts.py) | Parse and summarize audit report structure |
| [summarize\_manifests.py](https://github.com/nealmcb/rla-review-arlo/blob/main/src/summarize_manifests.py) | Summarize ballot manifest statistics |
| [search\_for\_hash.py](https://github.com/nealmcb/rla-review-arlo/blob/main/src/search_for_hash.py) | Search all files for a given SHA256 prefix |

---

## Ballot Image Audit (Enhanced Voting)

A **ballot image audit** is a distinct and complementary transparency mechanism from an RLA. Georgia's Dominion ImageCast Precinct (ICP) scanners capture a digital image of each ballot as it passes through. The Georgia SOS contracted **[Enhanced Voting](https://enhancedvoting.com)** to apply OCR to those stored images and compare the resulting vote totals against the county-certified results — for every contest, in every county.

For the May 2026 primary, the SOS released aggregate contest-results comparison data alongside a press release on approximately June 28, 2026. This review has analyzed that data in detail. See the [Ballot Image Audit report](reports/ballot_image_audit/) for full findings, including:

- Reconciliation of the SOS's headline figures ("1,785 contests reviewed," "159 discrepancies")
- Cherokee County: systematic audit losses across all 9 Republican Party Questions (−13 to −20 votes each)
- Muscogee and Henry counties: systematic OCR losses across contested judicial races
- Comparison of a June 11 jurisdiction-detail PDF against the June 28 Excel release
- Methodology context from the November 2024 general election audit, including the Sumter County write-in omission

---

## How to Replicate

```bash
# Clone the repository (includes all artifacts)
git clone https://github.com/nealmcb/rla-review-arlo.git
cd rla-review-arlo

# Install Python dependencies (numpy 1.26.4 required for exact PPEB reproduction)
pip install -r requirements.txt

# Verify SHA256 hashes of the two committed ZIPs
sha256sum 2026-05-19-primary/downloads/manifests.zip \
          2026-05-19-primary/downloads/candidate_totals.zip
# Expected:
# c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf  manifests.zip
# 2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312  candidate_totals.zip

# Verify individual batch ticket numbers from the public seed
python3 src/reproduce_sample.py

# Reproduce the full PPEB weighted sample draw
python3 src/reproduce_ppeb_sample.py
```
