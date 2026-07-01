---
layout: home
title: Georgia November 2025 Special Election — Review
---

# Georgia November 4, 2025 Special Election
## Risk-Limiting Audit and Ballot Image Audit — Transparency Review

**Version:** v0.19 &nbsp;·&nbsp; **Review timestamp:** 2026-07-01T21:50:00Z &nbsp;·&nbsp;
[v0.19 tag](https://github.com/nealmcb/rla-review-arlo/releases/tag/v0.19) &nbsp;·&nbsp;
[Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp;
[Comments / Issues](https://github.com/nealmcb/rla-review-arlo/issues)

---

> **DRAFT - AI-assisted analysis, partially reviewed.** This analysis was produced with significant AI assistance (Claude, Anthropic). Findings are ongoing and some claims may require further verification. Corrections welcome via [GitHub Issues](https://github.com/nealmcb/rla-review-arlo/issues).

## Overview

The November 4, 2025 election was a Statewide Special Election for **Public Service
Commissioner District 2**, combined with the municipal general election for Georgia's
counties and cities. Candidates for PSC District 2: Tim Echols (R, incumbent) and Alicia
M. Johnson (D).

Two independent post-election audit mechanisms were applied:

1. **Risk-Limiting Audit (RLA):** A batch-comparison (MACRO) hand-count audit of PSC
   District 2, conducted statewide across all 159 counties. The audit met its 5% risk
   limit with 355 batches hand-counted.

2. **Ballot Image Audit:** Enhanced Voting applied OCR to all 1,581,539 ballot images
   and compared against CVR data and election results, finding 14 discrepancies. The
   most significant finding — a Hall County ballot where the AuditMark (page 3 of the
   ballot TIFF) disagreed with the printed text — was identified pre-certification and
   resolved by rescanning the affected batch.

---

## Risk-Limiting Audit

Georgia conducted a statewide batch-comparison (MACRO) RLA of the PSC District 2 contest.

| Item | Value |
|------|-------|
| Audit type | BATCH\_COMPARISON (MACRO) |
| Contest | Public Service Commissioner District 2 |
| Risk limit | 5% |
| Random seed | `34363370190391208563` |
| Batches sampled | 355 |
| Batches with no deviation | 351 (98.9%) |
| Batches with discrepancy | 4 |
| Risk level achieved | p = 0.034 (3.4%) — risk limit met |

Secretary Raffensperger announced on November 18, 2025 that the audit confirmed the outcome
of the PSC District 2 contest. The 4 discrepant batches were described as "within an expected
margin of error for a hand count."

The RLA artifact files — final audit report CSV, ballot manifests ZIP, and candidate totals
ZIP — were published by the SOS. The manifests and candidate totals ZIPs contain inner ZIP
files with per-county data, each accompanied by a `.sha256sum` file for verification.

---

## Ballot Image Audit

Enhanced Voting conducted a ballot image audit using their Enhanced Audit software. The
published report is 27 pages and includes per-county discrepancy totals, example ballot
images illustrating image quality issues, and an OCR methodology appendix.

**Key findings:**

- **Hall County (pre-certification, excluded from final totals):** A ballot at precinct
  212-Gillsville showed a discrepancy between the printed human-readable text (PSC D2:
  Echols, PSC D3: Johnson, SPLOST vote) and the Dominion AuditMark on page 3 of the
  ballot image. The AuditMark — the scan-time record of what the QR code encoded — differed
  from the printed text. This caused a 2-vote understatement in PSC D2 and PSC D3 margins
  and a 1-vote SPLOST understatement. The Advance Voting batch was rescanned, Hall County
  recertified, and this discrepancy is not counted in the report's final totals.

- **Wilkinson County (counted in final totals):** A ballot's printed text and AuditMark
  agreed with each other, but the tabulation CVR file showed a different result. No
  election outcome was affected.

- **14 total discrepancies** in the final report: 3 BMD (Cherokee, Gwinnett, Wilkinson),
  11 HMPB (Chatham, Columbia, Decatur×4, Newton, Rockdale, Sumter×2, Wilkes).

See the [Ballot Image Audit report](reports/ballot_image_audit/) for full analysis.

---

## Data Artifacts

| File | SHA256 | Notes |
|------|--------|-------|
| `final_audit_report.csv` | `7e1d514c…b0` | RLA final report (Arlo CSV) |
| `manifests_bundle.zip` | `2d1c37d1…c6` | Ballot manifests (outer wrapper) |
| `candidate_totals_bundle.zip` | `f35dbcb5…da` | Candidate totals (outer wrapper) |
| `georgia_image_audit_report_2025.pdf` | `4277ba76…9f` | EV ballot image audit report (27 pp.) |
| `nov_2025_contest_results_comparison.pdf` | `ba6bdc25…77` | Contest results comparison (PDF) |
| `contest_results_comparison_with_county_breakout_dqs_removed.zip` | `235b22b0…99` | County-level breakout (XLSX inside ZIP) |

Full SHA256 values:
```
7e1d514c5b1fe25005a54f9be685508e9c6d088703c59625372a5c660a3e14b0  final_audit_report.csv
2d1c37d16b7ff04c0d76da058d96a2a6008e600eef4bcf86d93c9a4ac4725ce6  manifests_bundle.zip
f35dbcb5669fab920097ee4f61097f12a95a5921addada33a5dbb88acab8abda  candidate_totals_bundle.zip
4277ba7647ab4d126ccd93a5f59c7a4c1f5769fe6d2a9428fce9f01b95f14b9f  georgia_image_audit_report_2025.pdf
ba6bdc257450568620919fee23855d5cd2d45b15a02b099df4ef3fe956ae5477  nov_2025_contest_results_comparison.pdf
235b22b0fd5b6118ba2d9f9678b4bb4f08c23dcdeaac0c1c0792e6d84f834099  contest_results_comparison_with_county_breakout_dqs_removed.zip
```

The manifests and candidate totals bundles each contain an inner ZIP with a `.sha256sum`
file. Inner ZIP hashes have been verified against those bundled checksums.

Artifact source: Georgia Secretary of State / Enhanced Voting. The SOS elections audit
page (sos.ga.gov/page/elections-audit-information) returned 403 to automated fetches;
files were obtained manually.

---

## Reports

| Report | Description |
|--------|-------------|
| [Ballot Image Audit](reports/ballot_image_audit/) | Analysis of the Enhanced Voting report — AuditMark findings, county discrepancy table, methodology |
