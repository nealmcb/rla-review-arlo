---
layout: default
title: Ballot Image Audit Analysis — November 2025
---

# Ballot Image Audit Analysis — Georgia November 4, 2025 Special Election

**Version:** v0.19 &nbsp;·&nbsp; **Review timestamp:** 2026-07-01T21:50:00Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Reports](../)

---

> **DRAFT - AI-assisted analysis, partially reviewed.** This analysis was produced with significant AI assistance (Claude, Anthropic). Findings are ongoing and some claims may require further verification. Corrections welcome via [GitHub Issues](https://github.com/nealmcb/rla-review-arlo/issues).

## Summary

Enhanced Voting conducted a ballot image audit of Georgia's November 4, 2025 Statewide
Special and Municipal General Election. Their published report covers 1,564,630 BMD
(in-person) ballots and 16,909 HMPB (hand-marked) ballots across all 159 counties,
finding 14 total discrepancies — 3 BMD and 11 HMPB.

**Most significant finding:** In Hall County, Enhanced Voting found a ballot where the
printed human-readable text did not match the Dominion AuditMark on page 3 of the same
ballot image. The AuditMark — the scanner's scan-time record of what the QR code encoded
— showed different selections from the text the voter would have seen. The affected Advance
Voting batch was rescanned, Hall County recertified, and this discrepancy is **excluded
from the report's final totals**. Two votes for PSC District 2 and PSC District 3 were
restored by the rescan; one vote for a SPLOST contest was also restored.

This is the first publicly documented instance in Georgia's image audit program where the
AuditMark disagreed with the ballot face text — the central integrity check the methodology
is designed to perform.

**Second notable finding:** In Wilkinson County, the ballot face text and AuditMark agreed
with each other, but both differed from the tabulation CVR. The CVR file submitted for
tabulation showed a different result than either the AuditMark or the printed text. No
election outcome was affected.

---

## Methodology

Enhanced Voting's *Ballot Image Audit Report – November 2025* (27 pp.) describes the audit
methodology. Each Dominion ImageCast Precinct ballot image is a 3-page multi-page TIFF:

- **Page 1 ("1/2"):** BMD ballot face — QR code plus human-readable vote selections
- **Page 2 ("2/2"):** Ballot continuation for overflow contests, no QR code
- **Page 3 (AuditMark):** Monospaced machine-generated text printed by the tabulator at
  scan time, recording Tabulator ID, Poll ID, Ballot ID, and every contest with the
  scanner's recorded selection. This page represents what the scanner decoded from the QR
  code on the ballot face.

Three data sources were provided to Enhanced Voting:

| Source | Content |
|--------|---------|
| Ballot images (TIFFs) | Per-ballot images including QR code, text, and AuditMark |
| CVR files | County-submitted Cast Vote Records for all ballots |
| Election results files | County-level certified totals |

**OCR approach (Appendix A, pp. 21–22):** Enhanced Audit reads the ballot style name
printed on each ballot face, looks up the associated contest list, then OCRs the contest
titles and vote selections. If image quality is too poor for high-confidence OCR, the ballot
goes to a manual review list; county election officials then view the ballot image and
determine voter intent. The report notes the cause of poor image quality "could have been
the result of poor print quality, poor scan quality, or both."

The audit compares OCR results from pages 1–2 (human-readable text — what the voter was
shown) against the CVR file for each ballot. The AuditMark on page 3 provides a third
reference — the scan-time QR-decoding record — which is compared against both the text
and the CVR.

---

## Overall Results

**Totals (from Table 4, pp. 7–12):**

| Metric | Value |
|--------|-------|
| BMD ballots | 1,564,630 |
| HMPB ballots | 16,909 |
| Total ballots | 1,581,539 |
| BMD discrepancies (final) | **3** |
| HMPB discrepancies (final) | **11** |
| Total discrepancies (final) | **14** |

Hall County's 1 BMD discrepancy is excluded from these totals because the affected batch
was rescanned before the report was finalized.

**Counties with discrepancies:**

| County | BMD | HMPB | Total | Notes |
|--------|-----|------|-------|-------|
| Cherokee | 1 | 0 | 1 | Poor image quality (Image 7 in report) |
| Chatham | 0 | 1 | 1 | |
| Columbia | 0 | 1 | 1 | |
| Decatur | 0 | 4 | 4 | |
| Gwinnett | 1 | 0 | 1 | Cutoff ballot image (Image 6 in report) |
| Newton | 0 | 1 | 1 | |
| Rockdale | 0 | 1 | 1 | |
| Sumter | 0 | 2 | 2 | |
| Wilkes | 0 | 1 | 1 | |
| Wilkinson | 1 | 0 | 1 | AuditMark ≠ tabulation CVR (see §2.5 finding below) |
| **Hall** | *(1)* | — | *(1)* | *Excluded — batch rescanned before report finalized* |

---

## Key Finding 1: Hall County — AuditMark ≠ Ballot Text (§2.4)

The report states (§2.4):

> *"We observed a discrepancy between the text on one ballot and its tabulated CVR,
> including a discrepancy with the Dominion AuditMark CVR included as part of the ballot
> image. This caused a 2-vote understatement of the PSC 2 and PSC 3 margins, as well as
> a 1-vote understatement in the SPLOST contest. The Advance Voting batch containing the
> impacted ballot was rescanned because of this finding, and the correct totals were
> recertified. Due to recertification, this discrepancy is not included in the data
> included in this report."*

The report uses Hall County as a contrast case when describing Wilkinson (§2.5): *"Unlike
Hall County, this ballot image and its Dominion AuditMark were consistent."* This confirms
that in Hall County, the ballot image (printed text) and the AuditMark were **not**
consistent — they disagreed.

**What this means structurally:**

On a Dominion BMD ballot, the AuditMark (page 3 of the TIFF) records what the scanner
decoded from the QR code. The printed text (page 1) is the human-readable version the
voter reviews. These two encodings are generated at different points — text at BMD print
time, AuditMark at scan time — and should encode identical selections. When they disagree,
it indicates one of the following:

1. **QR scan error:** The scanner misread an otherwise-correct QR code, producing an
   AuditMark that doesn't reflect what was encoded. Rescanning the same ballot would
   re-decode the QR, potentially producing a correct result.
2. **QR encoding error (BMD failure):** The BMD encoded different selections in the QR
   than it printed as human-readable text. In this case, the AuditMark correctly reflects
   the wrong QR, and rescanning the same ballot would reproduce the same wrong result.

The Hall County batch was rescanned and produced the correct totals (adding 2 PSC votes
and 1 SPLOST vote), consistent with scenario 1 — a scan error, not a BMD encoding error.
However, the EV report does not state which scenario occurred, and scenario 2 cannot be
excluded without independent QR decoding of the original ballot.

**The ballot:** Image 1 in the report (p. 13) shows the Hall County ballot at precinct
212-Gillsville, displaying:
- "For Public Service Commission - District 2 / Vote for Tim Echols (I)(Rep)"
- "For Public Service Commission - District 3 / Vote for Fitz Johnson (I)(Rep)"
- Partially cut-off SPLOST text

The 2-vote understatement in PSC 2 and PSC 3 is consistent with these two contests being
the ones where the AuditMark and tabulation CVR recorded undervotes (or the wrong
candidate) while the printed text recorded valid selections.

---

## Key Finding 2: Wilkinson County — AuditMark = Text ≠ Tabulation CVR (§2.5)

The report states (§2.5):

> *"We observed a discrepancy between the text on one ballot and its tabulated CVR. Unlike
> Hall County, this ballot image and its Dominion AuditMark were consistent; only the CVR
> that was used for tabulation differed. The discrepancy did not cause differences in any
> election outcomes."*

In Wilkinson County: the ballot face text and the AuditMark (scan-time record) agreed with
each other. The CVR file submitted by the county for tabulation showed a different result.

This is a distinct failure mode from Hall County. Since the AuditMark is derived from the
QR-code reading at scan time, AuditMark = text implies the QR was read correctly and the
ballot content was consistent at the point of scanning. The tabulation CVR — a separate
data file — diverged from this correct scan-time record.

Possible causes include CVR file corruption or replacement after scanning, a database
mapping error associating the wrong ballot's CVR with this ballot image, or a re-export bug.
The EV report does not specify the cause. No election outcome was affected.

**Note:** Wilkinson County also had an election definition issue in the November 2024
general election audit (absentee ballots scanned against a wrong election definition,
corrected pre-certification). The 2025 Wilkinson finding is a different type of problem —
a CVR file integrity issue — but it is worth noting Wilkinson has appeared in consecutive
Enhanced Voting audit reports.

---

## Other BMD Discrepancies

### Cherokee County

The report includes Image 7 (p. 19) captioned "Cherokee County ballot with unreadable
image." The ballot image for precinct 286-Victoria shows severe degradation — multiple
horizontal artifacts, noise bands, and missing content — making OCR unreliable. The 1
Cherokee BMD discrepancy is consistent with the audit being unable to confirm the ballot's
vote selections from the degraded image.

### Gwinnett County

Image 6 (p. 18) shows a Gwinnett County ballot (711-012 Berkshire B) where the
human-readable portion is cut off — contests listed at the bottom of the ballot face
extend below the scanned area. The 1 Gwinnett BMD discrepancy is consistent with
incomplete OCR due to the cutoff image.

---

## HMPB Discrepancies

The 11 HMPB discrepancies across 6 counties (Chatham, Columbia, Decatur×4, Newton,
Rockdale, Sumter×2, Wilkes) are consistent with OMR algorithm-threshold differences
between the Dominion tabulation software and Enhanced Voting's re-read. Both systems run
optical mark recognition on the same stored TIFF image — the physical ballot paper is not
re-scanned. Any discrepancy reflects a difference in mark-acceptance threshold or
mark-detection algorithm between the two systems, or a human reviewer judgment call when
a borderline mark is flagged for manual review.

Decatur County's 4 HMPB discrepancies represent the highest county total in the report.
The cause is not specified in the published data.

---

## What This Audit Proves — and Doesn't

| Claim | Status |
|-------|--------|
| AuditMark and ballot text typically agree | **Yes** — 1,564,629 of 1,564,630 BMD ballots had consistent AuditMark/text; Hall County is the exception (excluded, rescanned) |
| The audit can detect AuditMark ≠ text discrepancies | **Yes** — Hall County demonstrates this capability |
| Hall County's discrepancy was a BMD encoding error (wrong QR content) | **Not confirmed** — rescanning produced the correct result, consistent with a scan error rather than a BMD error; original QR content unknown |
| Wilkinson County's CVR file was tampered with | **Not confirmed** — several data integrity failure modes could produce this pattern |
| No contest outcome changed | **Yes** — all election outcomes confirmed, including after rescan |
| The audit covers all contests in all counties | **Not verifiable from public data** — in Nov 2024, a Sumter County write-in race was silently excluded |
| All ballot images were submitted | **Unknown** — the report notes image quality issues but does not state whether any images were missing |

---

## Report Artifacts

| File | SHA256 | Source |
|------|--------|--------|
| `georgia_image_audit_report_2025.pdf` | `4277ba76…14b9f` | Georgia SOS / Enhanced Voting, Nov 2025 |
| `nov_2025_contest_results_comparison.pdf` | `ba6bdc25…5477` | Georgia SOS / Enhanced Voting, Nov 2025 |
| `contest_results_comparison_with_county_breakout_dqs_removed.zip` | `235b22b0…099` | Georgia SOS / Enhanced Voting, Nov 2025 |

Full SHA256 values:
```
4277ba7647ab4d126ccd93a5f59c7a4c1f5769fe6d2a9428fce9f01b95f14b9f  georgia_image_audit_report_2025.pdf
ba6bdc257450568620919fee23855d5cd2d45b15a02b099df4ef3fe956ae5477  nov_2025_contest_results_comparison.pdf
235b22b0fd5b6118ba2d9f9678b4bb4f08c23dcdeaac0c1c0792e6d84f834099  contest_results_comparison_with_county_breakout_dqs_removed.zip
```
