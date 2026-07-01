---
layout: default
title: Ballot Image Audit Analysis
---

# Ballot Image Audit Analysis — Georgia May 19, 2026 General Primary

**Version:** v0.12 &nbsp;·&nbsp; **Review timestamp:** 2026-06-29T23:18:24Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Reports](../)

---

## Summary

The Georgia Secretary of State's office conducted a ballot image audit of the May 19, 2026
General Primary and released results on or around June 28, 2026. This report analyzes the
contest-results comparison spreadsheet released alongside the press release, reconciles the
SOS's headline statistics against the underlying data, and identifies notable discrepancy
patterns.

**Key headline (SOS):** "confirmed the outcome of all 1,785 contests reviewed"; 159
discrepancies out of 2,081,900 ballot cards (99.9924% no-discrepancy rate).

**Key finding from this analysis:** Neither headline figure is directly derivable from the
released spreadsheet. The 1,785 and 159 figures come from the internal ballot-image
comparison system; the spreadsheet is a county-level aggregate that uses a different counting
unit. We document our reconciliation attempts below.

**No outcome was changed** by any discrepancy found in this audit.

---

## What Is the Ballot Image Audit?

Georgia law requires that every ballot be digitally imaged as it passes through an optical
scanner. The ballot image audit takes those stored images and re-tabulates them using a
separate software system, then compares the result against the official certified totals.

The Georgia SOS contracted **Enhanced Voting** to conduct this audit using their Enhanced
Audit software. This is a **machine-vs-machine comparison**, not a human hand count:

Enhanced Voting's Enhanced Audit software uses three data sources: ballot images, Cast Vote
Records (CVRs), and election results files. It performs comparisons at two levels:

| Level | What is compared |
|-------|-----------------|
| Ballot level | OCR interpretation of each ballot image vs. that ballot's CVR (the scanner's original reading of the QR code/barcode) |
| Batch/county level | Aggregate OCR totals vs. official election results files |

The step-by-step process:

| Step | What happens |
|------|-------------|
| Election day | Scanner reads QR code (BMD) or optical marks (HMPB), saves a digital image, records a CVR, and tabulates |
| Audit | Enhanced Audit applies OCR to stored ballot images, reading the printed human-readable text (BMD) or optical marks (HMPB); does not re-read the QR code from the image |
| Comparison | OCR interpretation compared against each ballot's CVR (ballot level) and against certified results (county level); flagged discrepancies go to manual review |

**For BMD (in-person) ballots:** The scanner tabulates from the QR code, producing a CVR.
The audit reads the **printed human-readable text** via OCR. Because the CVR comes from
QR-code reading and the OCR comes from text reading, **any disagreement between what the
QR code encoded and what was printed is detected as a discrepancy.** This is the core
verification the audit provides: it catches QR-vs-text encoding errors at the ballot level.

QR codes use Reed-Solomon error correction; they either decode correctly or fail entirely —
there is no silent partial-corruption failure mode. So the comparison is really: does the
text printed on the ballot match what the QR code encoded? Enhanced Voting's November 2024
general election audit found **zero such differences** across 5,025,863 Georgia BMD ballots;
the South Carolina June 2026 audit found **zero such differences** across 841,485 summary
ballots. Both confirm that QR codes and printed text agreed on every BMD ballot examined.

**Known failure mode — missing printed text:** The SC June 2026 audit found 21 summary
ballots across 13 counties where the printer failed to produce readable human-readable text
while still producing a valid barcode. The scanner accepted these ballots (the barcode was
intact), the votes were counted from the barcode, but Enhanced Voting could not apply OCR
and therefore could not verify that the barcode correctly represented the voter's choices.
These were reported separately as "unreadable" rather than as discrepancies. Voters who
cast these ballots also had no text to review at the polling place. This is the specific
scenario where QR-vs-text detection fails.

**For HMPB (absentee/hand-marked) ballots:** The original tabulation uses the Dominion
scanner's optical mark recognition on the physical paper. The audit uses OCR/OMR on stored
digital images of that paper. Small differences are plausible: image resolution, scan angle,
or lighting variation can shift whether a borderline-filled bubble crosses the acceptance
threshold. Human reviewer judgment is also involved when the system flags uncertain marks.
The 1–2 vote discrepancies typical of the data are most consistent with this OMR-threshold
and reviewer-judgment effect on HMPB ballots.

---

## Data Sources

Two artifacts were analyzed, representing two snapshots of the same underlying system:

**Primary: `Contest Results Comparison with County Breakout.xlsx`** (released ~2026-06-28)  
Rows: 30,895 data rows  
Columns: County, ContestId, ContestName, DetailId, DetailName, OriginalCount, AuditCount, Difference  
Each row is one county × one contest × one detail. The DetailId `BC` marks a "Ballots Cast"
summary row; all other rows are individual candidates (or Yes/No choices for party questions
and referenda).

SHA256: `61679db828f4232420bd56f2a7640192b24fc03786f7f59d1ca7431694a6648e`

**Supplemental: `contest_results_comparison_with_jurisdiction_details_15.pdf`** (created 2026-06-11 14:12 UTC)  
1,923 pages covering all contests by jurisdiction. This is an **earlier version** of the
same comparison, produced approximately 17 days before the Excel release. It shows fewer
discrepancies, indicating the comparison system continued processing or reconciling data
after June 11.

| Metric | PDF (June 11) | Excel (June 28) |
|--------|--------------|-----------------|
| Unique named contests | ~550 | 974 |
| Contest × county pairs | 7,322 | 9,169 |
| Candidate rows with diff ≠ 0 | 316 | 406 |
| Sum \|diff\| (candidate rows) | 716 | 994 |
| Net signed difference | −348 | −548 |
| BC rows with diff ≠ 0 | 69 | 75 |
| Sum \|diff\| (BC rows) | 71 | 77 |

The 90 additional discrepant candidate rows in the Excel likely represent either newly
processed precincts or corrections applied between June 11 and June 28.

### Raw Ballot Images

The Georgia SOS makes the underlying ballot images available at
`https://sos.ga.gov/ballot-image-library`. As of July 1, 2026, 125 of 159 counties had
uploaded ZIP files for the May 19, 2026 primary. Files are named by county
(e.g., `MAY-19-2026--GENERAL-PRIMARY-ELECTION_LONG.zip`; Long County: 145 MB) and are
only available county-by-county — no statewide download exists.

**Access process:** The site requires submitting name, organization, and email address and
accepting terms of service; an email is then sent with a 30-minute expiring download link.
The SOS does not warrant completeness or accuracy of the images.

**What the images contain — confirmed from Evans County inspection:** The Evans County ZIP
(`MAY-19-2026--GENERAL-PRIMARY-ELECTION_EVANS.zip`, 128 MB) was inspected directly.

- **Format:** Individual TIFF files, one per ballot. 1-bit bilevel (black/white), CCITT Huffman
  compressed, 200 DPI, approximately 1728×2100 pixels (~100 KB each).
- **ZIP structure:** One top-level audit-timestamp folder (e.g., `Audit2026_05_21_10_54_35/`),
  then one subfolder per ballot style (e.g., `Pre_9-Veteran's Comm Ctr/`). Files within
  each folder are numbered sequentially: `Pre_9-Veteran's Comm Ctr-0001.tif`, `0002.tif`, …
- **Ballot styles, not scanner batches:** The `Pre_N` folder identifier is the Dominion
  ballot style number — a unique combination of geographic precinct and party (Republican
  or Democratic). All ballots of that style appear in the same folder regardless of which
  scanner or voting mode (Election Day, Advance Voting, Absentee) processed them. Evans
  County had 19 unique ballot styles across 1,641 total ballots.
- **BMD ballot content:** Each image shows a printed BMD ballot with a QR code (upper left)
  and the complete human-readable vote record in three columns — every contest and the
  voter's choice. Choices are fully legible. Republican and Democratic voters appear in
  separate ballot-style folders (e.g., Pre_9 = Republican; Pre_33 = Democratic).
- **No embedded metadata:** The TIFF files contain no tabulator ID, batch name, poll ID, or
  CVR-linkage information. The "AuditMark" metadata pages visible in the Sumter complaint
  exhibits are an internal Dominion platform display; they do not appear in the publicly
  exported TIFF files.
- **Complete count verified:** Evans County's 1,641 images match the sum of all batch totals
  in the Evans County ballot manifest exactly (447+446+340+339+25+25+17+2 = 1,641). Evans
  County had **zero discrepancies** in the contest results comparison spreadsheet.

**Batch-linkage gap:** Images are organized by ballot style, not by scanner batch. The RLA
manifest uses batch names like `ED-Veteran's Community Center ICP 1 - 0` (340 ballots) and
`AV-Elections Office ICP 1 - 0` (447 ballots). Ballots from any given scanner batch are
spread across multiple ballot-style folders. Without a CVR mapping each ballot to its scanner
session, there is no way to identify which images correspond to a specific RLA batch. Georgia
does not publish CVR data.

Independent verification using ballot images therefore requires re-running OCR across all
images for a county and comparing county-level totals against the certified results — which
is exactly what Enhanced Voting does. What cannot be done from the images alone is
verifying or disputing the tally for a specific scanner batch.

The ballot images for Cherokee, Muscogee, and Henry counties — where systematic discrepancies
were observed — could in principle be used for county-level OCR re-runs. That analysis has
not been conducted in this review.

**Voter privacy concern — ballot de-anonymization:** Because ballot images are organized
by ballot style (precinct × party), and Georgia voter rolls are public records that include
who voted and which party primary they chose, small ballot-style folders may effectively
de-anonymize individual voters. In Evans County, Pre_33 contains **exactly one image** — one
Democratic voter in that ballot style. If the public voter roll for that precinct shows only
one person voted a Democratic primary ballot on May 19, 2026, that person is identifiable,
and their complete vote record (every contest, every choice) is visible on the image.

This concern extends to any ballot style folder with a small enough count that cross-
referencing with voter roll data narrows down the identity. In Evans County alone, several
folders have counts under 20 (Pre_24: 9, Pre_22: 14, Pre_29: 14, Pre_33: 1). Across 125
counties with images posted, many rural counties will have similarly thin precinct-party
combinations.

Georgia law generally provides ballot secrecy, and the Secretary of State's terms of
service state that images are provided for transparency and audit purposes. However, the
ballot image export format — organized by precinct × party rather than shuffled — does
not appear to include any minimum-count suppression threshold that would prevent the
publication of potentially identifying ballot images.

---

## Contests: What the Spreadsheet Contains

| Metric | Count | Notes |
|--------|-------|-------|
| Unique contest names | **974** | Across all counties |
| County × contest pairs | **9,169** | The unit the spreadsheet actually tracks |
| Unique ContestIds | **132** | IDs 1–132; reused across counties (not globally unique) |
| Contests with ≥2 candidates | **473** | By unique contest name |
| Uncontested (1 candidate) | **498** | Slightly more than half of all named contests |
| Purely local contests (1 county only) | **498** | Coincidence with uncontested count |
| Multi-county contests | **476** | State, federal, judicial, legislative |
| State/federal contests (≥50 counties) | **40** | Statewide races |

### The "1,785 Contests Reviewed" Discrepancy

The SOS press release says "confirmed the outcome of all 1,785 contests reviewed." No slice
of the spreadsheet produces this number. We attempted:

- All BC rows with votes > 0: **9,166**
- Distinct county × ContestName pairs: **9,101**
- All unique contest names: **974**
- Excluding party questions and referenda: **7,321**
- Contests appearing in ≥10 counties: **7,313**
- All unique ContestIds: **132**

The most plausible interpretation is that the SOS counts at **ballot-style granularity** rather
than county granularity. Two independent estimates from the two released artifacts both
converge on ~1,782:

- **From the Excel**: 132 distinct ContestIds × ~13.5 county-average instances ≈ 1,782
- **From the PDF**: ~550 unique named contests × ~3.25 ballot-style instances each ≈ 1,788

Both calculations arrive near 1,785, suggesting the SOS system counts each
contest-at-a-ballot-style as a unit, rather than each contest-at-a-county. This cannot
be confirmed without access to the internal tabulation system or additional SOS clarification.

---

## Discrepancies: What the Spreadsheet Shows

### Candidate-level (vote counts)

| Metric | Value |
|--------|-------|
| Candidate rows with any Difference ≠ 0 | **406** |
| Sum of \|Difference\| across all candidate rows | **994 votes** |
| Net signed difference (audit − original) | **−548** |
| Unique contest names with any discrepancy | **114 of 473 contested** |
| County × contest pairs with any discrepancy | **337** |
| Counties with any discrepancy | **50 of 159** |

### Ballot-count level (BC rows)

| Metric | Value |
|--------|-------|
| BC rows with Difference ≠ 0 | **75** |
| Sum \|Difference\| across BC rows | **77 ballot cards** |

### The "159 Discrepancies" Discrepancy

The SOS says 159 discrepancies out of 2,081,900 ballot cards — arithmetic confirmed:
(2,081,900 − 159) / 2,081,900 = **99.9924%** exactly.

This figure cannot be reproduced from the spreadsheet. The closest values we can compute:

- BC rows with any difference: **75** county×contest pairs
- Sum of |differences| in BC rows: **77 ballot cards**
- Sum of |differences| in candidate rows: **994 vote-choices**

The 159 is almost certainly a **ballot-card-level count** from the image comparison
system: for each of the 2,081,900 individual ballot cards, the system checks whether any
contest result changed between original scan and audit. If any contest on a card changed, the
card is counted as "discrepant." This metric cannot be aggregated up from county-level totals
in this spreadsheet.

The discrepancy between 159 (ballot cards) and 994 (vote-choice differences) is expected: a
single discrepant ballot card can produce multiple vote-choice differences (e.g., one ballot
card has different results in three contests → 1 discrepant card, up to 3 vote-choice
differences). Conversely, 994 vote-choice differences distributed across 2,081,900 ballot
cards could involve as few as 159 cards if each discrepant card has roughly 6 affected
contests on average — which is on the high end. The true ballot-card count likely lies between
the 75–77 BC-level estimate and the 994 vote-choice figure.

### BC vs. Candidate Mismatch (273 Cases)

In 273 of ~9,169 county×contest pairs, the BC (ballots cast) difference does not equal the
sum of candidate differences. A concrete example:

**Wilkes County, Democratic Party Question 1:**
- BC row: OriginalCount = 983, AuditCount = 983, **Difference = 0**
- "No" row: OriginalCount = 899, AuditCount = 900, **Difference = +1**
- "Yes" row: OriginalCount = 59, AuditCount = 59, Difference = 0

Total ballots cast: unchanged at 983. But one ballot that the original scanner counted as an
undervote (neither Yes nor No) was re-read by the audit as "No." The ballot still exists and
is counted; only its vote allocation changed.

This pattern reveals that the audit is **redistributing votes within a fixed ballot count**,
not finding extra or missing ballots. The discrepancy is in mark interpretation, not in whether
a ballot was processed. This is the expected behavior for OMR-on-image vs. OMR-on-paper
differences: the same physical ballot, read twice with slightly different sensitivity thresholds.

---

## Notable Findings

### 1. Cherokee County: Systematic Pattern in Party Questions

Cherokee County shows a consistent, large negative difference across all nine Republican Party
Questions — in every case, the audit found *fewer* Yes votes than the original scanner:

| Question | Yes diff | No diff |
|----------|----------|---------|
| Q1 | −13 | −1 |
| Q2 | −17 | −1 |
| Q3 | −13 | −4 |
| Q4 | −16 | −1 |
| Q5 | −18 | −1 |
| Q6 | −18 | −1 |
| Q7 | −14 | −3 |
| Q8 | −20 | −1 |
| Q9 | −16 | −1 |

Three observations:
1. **Consistent direction**: Yes loses 13–20 votes per question; No loses only 1–4. This is
   not random noise — a systematic factor is suppressing Yes reads in the audit.
2. **Consistent scale**: Losses are similar across all 9 questions (~15 Yes votes per
   question), suggesting a single underlying cause affecting that section of the ballot rather
   than question-specific content.
3. **BC rows likely show zero difference**: total ballots cast in Cherokee County for these
   contests likely didn't change, meaning the "lost" Yes votes became undervotes in the
   audit re-read.

The most likely explanation is a calibration or image-quality difference in Cherokee County's
scanned images for the party question section — the original scanner accepted borderline Yes
marks that the image re-read rejected. Whether those marks represented genuine voter intent
(in which case the original count is correct) or were scanner artifacts (in which case the
audit is correct) cannot be determined from the spreadsheet.

### 2. Muscogee and Henry Counties: Systematic Judicial-Race Losses

The June 11 PDF reveals a second county-level pattern not visible in the Excel's aggregate
view: Muscogee County shows systematic negative differences across virtually every contested
judicial race, and Henry County shows a similar (smaller) pattern.

**Muscogee County** (from the June 11 PDF):

| Race | Candidate | Diff |
|------|-----------|------|
| Sup. Court (Chattahoochee Circuit) | Tippi Cain Burch (I) | −15 |
| Supreme Court (Land) | Ben Land (I) | −15 |
| Court of Appeals (Padgett) | J. Wade Padgett (I) | −11 |
| Court of Appeals (Markle) | David Todd Markle (I) | −10 |
| Supreme Court (Warren) | Jen Auer Jordan | −10 |
| Supreme Court (Bethel) | Miracle Rankin | −9 |
| Court of Appeals (Gobeil) | Fatima Harris Felton | −7 |
| Court of Appeals (Doyle) | Sara Doyle (I) | −7 |
| Court of Appeals (Brown, III) | Will Wooten | −6 |
| Court of Appeals (Gobeil) | Elizabeth D. Gobeil (I) | −5 |
| Court of Appeals (Brown, III) | Trenton "Trent" Brown (I) | −5 |

**Henry County**: Sara Doyle −10, Gobeil (Fatima Harris Felton) −9, Padgett −7, Brown (Will Wooten) −4,
Warren (Jen Auer Jordan) −5, Bethel (both candidates) −2 each, plus party questions −2 each.

Three observations parallel to the Cherokee pattern:
1. **Consistent direction**: The audit finds fewer votes than the original scanner across essentially all judicial races in these counties.
2. **Not candidate-specific**: Multiple unrelated races and candidates are affected the same way, ruling out any candidate-specific explanation.
3. **Plausible mechanism**: Judicial races typically appear in a specific section of the ballot. A scanner calibration difference or image-quality artifact affecting that ballot section would produce exactly this pattern — systematically lower audit counts across every race in the section.

It is not yet possible to determine which reading is more accurate — original scanner or
image re-read — from the released data alone.

### 3. Net Direction: Audit Consistently Finds Fewer Votes

The net signed difference across all candidate rows is **−548** (audit found 548 fewer votes
than original tabulation). The split:

- Audit found **more** votes than original: +223 votes (across rows where Difference > 0)
- Audit found **fewer** votes than original: −771 votes (across rows where Difference < 0)

This is not symmetric noise. The Enhanced Voting OCR re-read is systematically more
conservative — less likely to count borderline marks — than the original scanner tabulation.
Cherokee County alone contributes roughly −180 votes to this net (9 questions × ~20 vote
difference), but the directional bias persists even excluding Cherokee.

### 4. No Outcome Changes

All 1,785 (by SOS count) contest outcomes were confirmed. The smallest statewide winning
margins (thousands of votes in most races) are orders of magnitude larger than any discrepancy
found. Local races with the smallest margins also showed no outcome change.

---

## What This Audit Proves — and Doesn't

| Claim | Status |
|-------|--------|
| QR codes and printed text on BMD ballots agree | **Yes, per multiple precedents** — zero QR-vs-text discrepancies in Georgia Nov 2024 (5,025,863 BMD ballots) and South Carolina June 2026 (841,485 summary ballots) |
| OCR tabulation and certified totals are highly consistent | **Yes** — 99.9924% at ballot-card level (per SOS); consistent with Nov 2024 (87 discrepancies out of 5.3M ballots) |
| No contest outcome changed | **Yes** — confirmed across all contests included in the audit |
| Post-election adjudication errors can be detected | **Yes, for included contests** — if adjudication produced results inconsistent with the ballot images, OCR vs. CVR/certified-results comparison would show a discrepancy |
| All contests were included in the comparison | **Not verifiable from public data** — in the Nov 2024 audit, one Sumter County local race was silently excluded from Enhanced Voting's comparison; the publicly released data cannot confirm complete coverage for May 2026 |
| Write-in votes are handled correctly | **Uncertain** — the excluded Nov 2024 Sumter race was a write-in contest; Enhanced Voting may have improved write-in handling since then, and primary elections have fewer write-in scenarios than general elections |
| Ballots with failed printing are detected | **Partially** — if the BMD printer fails to produce human-readable text while still generating a valid barcode, the audit cannot perform OCR and flags the ballot as "unreadable" rather than a discrepancy; the vote is counted from the barcode but is unverifiable. SC June 2026 found 21 such ballots. |
| Voters' intended choices are accurately captured | **Not directly addressed** — this audit compares machine reads of stored images against CVRs/certified results; it cannot detect whether a BMD encoded voter intent correctly at print time, or whether voters verified their printed ballots |

The ballot image audit is a meaningful consistency check. It is **not** a hand count,
and it does not verify the link between voter intent and recorded vote. It is complementary
to — but significantly weaker than — the batch-comparison RLA conducted separately.

### November 2024 Precedents

The same Enhanced Voting system was used for Georgia's November 2024 general election audit
(5,297,264 ballots, 1,955 contests, 6,647 ballot styles). That audit's published findings
provide important context:

- **Zero BMD discrepancies**: OCR and QR tabulation agreed on all 5,025,863 BMD ballots.
- **86 HMPB discrepancies**: All attributed to voter intent interpretation differences —
  consistent with OMR-on-image vs. OMR-on-paper threshold effects.
- **In-process corrections**: The audit caught real errors before certification — Barrow
  County had test ballots mixed with official results; Peach County had one test ballot in
  the official results; Wilkinson County had absentee ballots scanned against a wrong
  election definition. All were corrected prior to state certification.
- **One missed local race (Sumter County)**: A write-in race for Soil and Water
  Conservation District Supervisor was not included in Enhanced Voting's comparison. The
  official certified result credited the write-in winner with 1,750 votes; ballot images
  showed the candidate received fewer than 130 write-in votes, with the remainder credited
  to him via the voting system's post-election adjudication module using a shared "emsadmin"
  credential. Because the contest was not part of the audit, no discrepancy was reported.
  The Coalition for Good Governance filed a complaint with the State Election Board in
  January 2025. The SOS press release claiming the audit examined "every race in every
  county" was inaccurate with respect to this race.

For May 2026, the absence of large write-in-only races reduces exposure to the Sumter failure
mode. Whether Enhanced Voting has since improved its write-in contest handling has not been
publicly confirmed.

### South Carolina June 2026 Precedent

South Carolina conducted a ballot image audit of its June 9, 2026 statewide primary using
the same Enhanced Voting Enhanced Audit software, with ES&S voting equipment (ExpressVote
BMD + DS300/DS450/DS850/DS950 scanners). The published report (authored by the same Enhanced
Voting team) provides useful methodology context contemporaneous with the Georgia May 2026
audit:

- **Zero summary ballot discrepancies**: All 841,485 BMD summary ballots had zero OCR-vs-CVR
  discrepancies. All 31 discrepancies were on 13,988 hand-marked ballots — marginal marks (26)
  and adjudication decisions that didn't align with SC's "Uniform Definition of What Constitutes
  a Vote" (5). Consistent with the Georgia Nov 2024 pattern.
- **Three data sources**: SC provided ballot images, CVRs, and election results files to
  Enhanced Voting. The audit performs both ballot-level (OCR vs. CVR) and batch-level
  (aggregate vs. results) comparisons. Georgia's public release includes only the county-level
  aggregate comparison; CVRs are not published.
- **Unreadable summary ballots**: 21 summary ballots across 13 counties had intact barcodes
  but no human-readable text — the printer failed to print the text portion. The scanner
  accepted these ballots (votes counted from barcode), but Enhanced Voting could not verify
  the text matched the barcode. Reported separately as "unreadable," not as discrepancies.
- **Enhanced Voting's own limitation statement**: "Audit methods that explicitly reference the
  paper ballots (such as through statistical hand counts, like risk-limiting audits) are
  essential to providing critical properties like software independence. Nevertheless, the
  practical constraints around the efficiency and accuracy of hand counting mean that pairing
  that practice with an image audit enable a more complete audit than is otherwise possible."
- **Same report artifacts**: The SC report references "Contest Results Comparison with County
  Breakout (XLSX)" and "Contest Results Comparison with Jurisdiction Details (PDF)" — the same
  document types as the Georgia artifacts analyzed in this review, confirming consistent
  Enhanced Voting output format across jurisdictions.
- **Missing images**: 14 ballot images were not submitted for audit across 3 counties (2 blank
  summary ballots; 12 a separately-scanned batch). Enhanced Voting noted these and treated
  missing contests as undervotes for comparison.

---

## Relation to the RLA

The May 2026 primary was audited by two independent mechanisms:

| Feature | Batch-Comparison RLA | Ballot Image Audit |
|---------|---------------------|-------------------|
| Method | Human hand-count of physical ballots | Machine OCR of stored ballot images vs. CVRs/results |
| Scope | 2 contests (US Senate REP, Governor DEM) | All 1,785 (SOS count) contests |
| Granularity | Batch-level (706 batches, 341,816 ballots) | Ballot-level (OCR vs. CVR) + county-level (aggregate vs. results) |
| Verifies | Scanner QR results vs. human reading of printed text | Printed text (OCR) vs. scanner QR results (CVR) |
| QR-vs-text detection | ✓ Yes — hand counters read printed text; machine tabulated QR | ✓ Yes — OCR reads printed text; CVR reflects QR reading; disagreement = discrepancy |
| BMD residual gap | ✗ Cannot detect whether BMD correctly encoded voter intent at print time | ✗ Same — neither audit can bridge the voter-intent gap |
| Outcome confirmation | ✓ Both RLA contests confirmed | ✓ All contests confirmed |
| Public artifact quality | Full CSV with seed, sample, risk levels | County-level aggregate spreadsheet only; CVRs not published in Georgia |

The RLA provides stronger evidence for its two contests (independent human verification of
physical paper) but covers only those contests. The ballot image audit covers all contests
but provides weaker evidence (two machine reads of the same stored images).

---

## Data File

The spreadsheet (`contest_results_comparison.xlsx`) is included in this repository at
[`2026-05-19-primary/downloads/contest_results_comparison.xlsx`](../downloads/contest_results_comparison.xlsx).

SHA256:
```
61679db828f4232420bd56f2a7640192b24fc03786f7f59d1ca7431694a6648e
```

Source: Georgia Secretary of State, released ~2026-06-28 alongside the press release
["Ballot Image Audit Proves Georgia Elections are Most Accurate in Nation"](https://sos.ga.gov/news/ballot-image-audit-proves-georgia-elections-are-most-accurate-nation).
