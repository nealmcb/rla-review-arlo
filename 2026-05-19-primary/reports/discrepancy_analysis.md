---
layout: default
title: Discrepancy Analysis
---

# Discrepancy Analysis — Georgia May 19, 2026 RLA

**Version:** v0.9 &nbsp;·&nbsp; **Review timestamp:** 2026-06-29T23:18:24Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Reports](../)

---

## Summary

The May 19, 2026 Georgia primary audit found discrepancies in 100 of 706 hand-counted
batches. Total absolute vote differences: **257 votes** across 341,816 audited ballots
(0.75‰). No discrepancy changed the outcome of either audited contest.

Key finding: **HMPB (hand-marked absentee) ballots show 2–3× more vote discrepancies per
ballot than BMD (ballot-marking device) ballots** — the opposite of naive expectation.
The per-*batch* BMD rate is higher, but that is an artifact of batch size, not a higher
underlying error rate. Georgia publishes no investigation or explanation of any individual
discrepancy.

---

## The Ballot Universe and Voting Methods

Georgia uses two ballot technologies with fundamentally different relationships to auditing:

**BMD (Ballot Marking Device):** Used for all in-person voting. The voter makes selections
on a touchscreen; the BMD prints a paper ballot containing a machine-readable QR code
*and* a human-readable text summary. The tabulator scans and counts the **QR code**.
The RLA auditor reads the **human-readable text** from the same paper.

**HMPB (Hand-Marked Paper Ballot):** Used for absentee-by-mail and provisional voting.
The voter hand-marks ovals on a paper ballot. The tabulator reads those optical ink marks.
The RLA auditor reads the same physical ink marks.

### How many ballots were cast by each method?

From the complete ballot manifests across all 159 counties:

| Voting Method | Ballot Type | Batches | Ballots | % of Total |
|---------------|-------------|---------|---------|-----------|
| Advance Voting (in-person, scanner) | **BMD-AV** | 718 | 995,641 | **47.8%** |
| Election Day (in-person, scanner) | **BMD-ED** | 2,744 | 1,040,814 | **50.0%** |
| Absentee-by-Mail | **HMPB-ABM** | 1,900 | 43,461 | **2.1%** |
| Provisional | **HMPB-PROV** | 278 | 1,648 | **0.1%** |
| **Total** | | **5,641** | **2,081,564** | **100%** |

Nearly **97.8% of ballots** were cast in-person using BMD. Absentee HMPB ballots represent
only 2.1% of the total — a small universe but, as the discrepancy data shows, an important
one for audit quality discussion.

---

## How a MACRO Batch-Comparison Discrepancy Is Defined

In Arlo's MACRO batch-comparison audit, a "discrepancy" occurs when the auditor's
hand count of votes in a batch differs from the vote total the tabulator reported for
that same batch. The standard is **exact agreement**: a single-vote difference in a
6,000-ballot batch counts the same as in a 10-ballot batch.

| Ballot type | Machine reads | Auditor reads | Discrepancy defined as |
|-------------|--------------|---------------|------------------------|
| **BMD** (in-person) | QR code on printed ballot | Human-readable text on same ballot | Any QR-count ≠ auditor tally |
| **HMPB** (absentee/provisional) | Optical ink marks on paper | The same ink marks | Any scanner count ≠ auditor tally |

Because the QR code and printed text on a BMD ballot are produced by the same device at
the same moment, they should normally encode identical information. Any difference between
the QR count and the auditor's read of the printed text is therefore surprising. When the
RLA produces BMD discrepancies, it is worth asking carefully what caused them.

---

## The Audit Sample by Ballot Type

The PPEB algorithm selects batches weighted by their maximum possible error contribution
(proportional to batch size and contest margin). This does not sample uniformly — it
preferentially selects larger batches because they contribute more to potential outcome
error.

| Ballot Type | Total Batches | Total Ballots | Audited Batches | Audited Ballots | Batch Coverage | Ballot Coverage |
|-------------|--------------|--------------|----------------|-----------------|---------------|----------------|
| HMPB-ABM | 1,900 | 43,461 | 284 | 14,634 | 14.9% | **33.7%** |
| HMPB-PROV | 278 | 1,648 | 12 | 18 | 4.3% | 1.1% |
| BMD-ED | 2,744 | 1,040,814 | 290 | 117,451 | 10.6% | 11.3% |
| BMD-AV | 718 | 995,641 | 117 | 208,495 | 16.3% | **20.9%** |

Notable observations:
- **33.7% of all absentee ballots were audited** — a very high proportion, driven by
  PPEB's selection of the larger absentee batches (audited average: 52 ballots vs
  universe average: 23 ballots per batch)
- **Only 14.9% of absentee batches were selected** (the largest ones were over-represented)
- **20.9% of all AV ballots** were hand-counted despite AV batches being only 16.3% of
  AV batches, again because PPEB preferentially selected the largest AV batches
- **Provisional ballots**: 12 batches audited from 278 total; the 18 audited ballots
  represent only 1.1% of the 1,648 provisional ballots cast

---

## Batch Size: The Dominant Factor in the Discrepancy Picture

The most important structural fact about the Georgia 2026 audit is the extreme variation
in batch size. This shapes almost everything in the discrepancy analysis.

### Batch size statistics (audited batches)

| Ballot Type | N | Mean | Median | P25 | P75 | Max |
|-------------|---|------|--------|-----|-----|-----|
| HMPB-ABM | 284 | 52 | 24 | 6 | 42 | 2,194 |
| HMPB-PROV | 12 | 2 | 1 | 1 | 2 | 3 |
| BMD-ED | 290 | 405 | 340 | 214 | 557 | 2,623 |
| BMD-AV | 117 | 1,782 | 1,613 | 874 | 2,261 | 6,381 |

**The median BMD-AV batch is 1,613 ballots** — 67× larger than the median absentee batch
(24 ballots). The largest single batch audited, NEWTON County `AV-Town ICP 1`, contained
**6,381 ballots**. Auditors hand-read and tallied 6,381 BMD printed receipts from a
single scanner as one audit unit.

### Batch size distribution (all 706 audited batches)

| Batch size range | Count |
|-----------------|-------|
| 0–9 | 93 |
| 10–49 | 164 |
| 50–99 | 58 |
| 100–199 | 39 |
| 200–499 | 155 |
| 500–999 | 101 |
| 1,000–1,999 | 53 |
| 2,000–4,999 | 40 |
| 5,000+ | 3 |

Nearly a quarter of all audited batches contained fewer than 10 ballots (mostly small
absentee ICC containers). But the three batches over 5,000 ballots collectively required
more hand-counting labor than all 93 single-digit batches combined.

---

## Discrepancy Rates by Ballot Type

### Per-batch discrepancy rate (misleading)

The per-batch rate — what fraction of batches have *any* vote discrepancy — is the
easiest to compute but the most misleading:

| Ballot Type | Batches Audited | Batches with Discrepancy | Rate |
|-------------|----------------|--------------------------|------|
| HMPB-ABM | 284 | 19 | 6.7% |
| HMPB-PROV | 12 | 1 | 8.3% |
| BMD-ED | 290 | 40 | 13.8% |
| BMD-AV | 117 | 40 | 34.2% |

BMD-AV appears to have the most discrepancies. This is primarily a batch-size effect,
not a higher underlying error rate.

### Per-ballot vote discrepancy rate (the meaningful metric)

Counting actual vote differences — the sum of absolute candidate-vote changes across
all batches:

| Ballot Type | Audited Ballots | Total \|Δ votes\| | Rate (‰) |
|-------------|----------------|------------------|---------|
| HMPB-ABM | 14,634 | 31 | **2.12‰** |
| HMPB-PROV | 18 | 2 | 111.1‰ *(2 batches, 18 ballots — not significant)* |
| BMD-ED | 117,451 | 98 | **0.83‰** |
| BMD-AV | 208,495 | 126 | **0.60‰** |
| **Total** | **341,816** | **257** | **0.75‰** |

**The per-ballot discrepancy rate is 2.5–3.5× higher for HMPB than for BMD.** This is
the opposite of what the per-batch rates suggest, and the opposite of the naive expectation
that BMD discrepancies (QR vs. text) would be as common as HMPB discrepancies
(ambiguous marks).

### Why the per-batch rate reverses

A BMD-AV batch averages 1,782 ballots. At 0.60‰ per ballot, the expected number of
vote discrepancies per AV batch is about 1.07. Even if the underlying auditor-error rate
is low, a batch this large will contain at least one error with high probability, producing
a high per-batch discrepancy rate.

An absentee ICC batch averages 52 ballots. At 2.12‰ per ballot, the expected
discrepancies per batch is about 0.11 — so only ~10% of batches have any discrepancy,
even though the per-ballot error rate is much higher.

**The per-batch discrepancy rate measures "how often does a batch have any error" — which
depends as much on batch size as on the underlying rate.**

---

## Why BMD Discrepancies Exist at All

The user's intuition is correct: in a rigorous MACRO audit of BMD printouts, the
expectation would be near-zero discrepancies. The human-readable text on a BMD ballot
is clear, structured, and readable — far less ambiguous than a hand-marked oval. Yet
BMD-ED shows 0.83‰ and BMD-AV shows 0.60‰. Where do these come from?

### Auditor tallying error (most likely source)

Counting 340 to 1,782 printed BMD receipts by hand — reading each one, maintaining a
tally, and checking it — is cognitively demanding work even when every receipt is perfectly
legible. A trained auditor who misreads zero individual receipts can still tally 1,000
receipts and produce a count that is off by one. The 0.6–0.83‰ rates translate to
approximately one tally error per 1,200–1,700 ballots counted. This is consistent with
human performance on sustained counting tasks.

The exact-agreement standard used in the MACRO audit makes every such error visible.
A less stringent audit (e.g., checking aggregate totals rather than batch-by-batch) would
not detect these.

### QR code vs. printed text mismatch (unquantifiable from public data)

The most consequential potential source of BMD discrepancy would be a case where the
QR code and the printed text encode *different vote choices* — meaning the scanner
counted a vote the voter did not intend (or vice versa). An RLA audit is the primary
mechanism by which such errors would be detected: the QR-based machine count would differ
from the text-based hand count.

Georgia's published artifacts make it **impossible to distinguish** auditor tallying
errors from genuine QR-vs-text disagreements. No discrepancy in the audit report was
investigated, explained, or categorized. The 257 total vote differences remain
collectively unexplained.

Most are almost certainly tallying errors. But "almost certainly" is not "known with
certainty," and the MACRO risk calculation treats all discrepancies identically.

### Mixed-ballot counting and batch composition

In a primary election, some ballots in any given batch may be from voters who chose
no contest (undervoted), or whose ballot was assigned to the batch after tabulation
in a way that differs slightly from physical batch composition. Small counting differences
in batch membership can produce 1–2 vote differences without any error in reading any
individual ballot.

### What Georgia documents about BMD discrepancies

**Nothing.** The audit report records the change in results for each batch. It provides
no categorization of discrepancy cause, no notation that a discrepancy was investigated,
no comparison of QR code content to printed text for discrepant batches, and no
discussion of the Jackson directional pattern (see below). The absence of discrepancy
investigation documentation is itself a transparency gap.

---

## Why HMPB Has a Higher Per-Ballot Error Rate

HMPB absentee discrepancies (2.12‰) are 2.5–3.5× more common per ballot than BMD
discrepancies. The user expected these rates to be comparable, since both involve human
reading. The difference reflects the source material, not just auditor performance:

**On an HMPB ballot**, both the scanner and the auditor read the same ink marks. The
scanner applies a pixel-threshold algorithm; the auditor applies judgment. Ambiguous marks
are genuinely ambiguous:
- Partially filled ovals that cross the scanner's threshold but look empty to an auditor
- "Clean" marks that the auditor counts but the scanner flags as too light
- Correction attempts (fill in, then cross out) that scanner and auditor interpret
  differently
- Stray marks in the voting area

These are physical artifacts of how voters fill out ballots. Even with perfect attention
and technique, an auditor and a scanner can reach different conclusions about the same
mark. This is the well-documented source of HMPB discrepancies in audits worldwide and
a known limitation of optical-mark ballots. It does not imply error by either the
scanner or the auditor — it reflects genuine ambiguity in the source material.

**On a BMD ballot**, the auditor reads clearly printed text, not ink marks. There is no
ambiguity about whether "Earl L. 'Buddy' Carter" is marked. The only source of
discrepancy is human tallying error or a genuine QR-vs-text disagreement — neither of
which involves interpreting ambiguous marks.

This is also why HMPB ballots are considered a more reliable audit substrate:
the discrepancy between machine and hand count is a meaningful signal about the
quality of the original scan decision, whereas BMD discrepancies between QR and text
are either auditor errors or (in principle) encoding errors worth investigating.

---

## The Derrick Jackson Pattern

Of all candidates in both contests, **Derrick Jackson (Governor Dem)** shows the most
concentrated directional pattern:

- 24 batches had at least one Jackson vote discrepancy
- **16 batches**: hand count found *fewer* Jackson votes than machine reported (machine
  overcounted); net −36 across these batches
- **8 batches**: hand count found *more* Jackson votes than machine reported (machine
  undercounted); net +9 across these batches
- **Net: −27**: across all audited batches, the machine reported 27 more Jackson votes
  than the hand count found

The pattern spans ballot types (BMD-ED: 8 batches, BMD-AV: 6, HMPB-ABM: 2) and 16
counties, with no single county accounting for more than 2 batches. TERRELL's
`ED-Dawson ICP 1 - 0` (356 ballots, BMD-ED) showed Jackson −8, the largest single-batch
instance.

### Interpretation

A net discrepancy of 27 votes across 341,816 audited ballots (0.079‰) did not affect
the contest outcome. Whether it is statistically notable depends on what comparisons we
make:

Among all five Gov Dem candidates with non-zero net discrepancies, Jackson is the sole
candidate with a large negative value (the machine overcounted relative to auditors),
while all other candidates with notable nets are positive (machine undercounted). The
asymmetry — Jackson consistently overrepresented in the QR/machine count relative to
the auditor text/mark read — could reflect:

- **Ballot position effect**: Jackson's candidate position on the printed BMD ballot or
  HMPB template may be adjacent to a position that confuses either the scanner or the
  auditor
- **Auditor perception**: If the name "Derrick Jackson" appears in a difficult-to-read
  position or shares visual similarity with adjacent entries, auditor undercounting is
  possible
- **Random variation**: With six Dem candidates across hundreds of batches, some degree
  of directional imbalance is expected by chance; 27 votes is not extreme in isolation
- **Scanner calibration**: For the 2 HMPB batches, if Jackson's oval position is
  borderline for a particular scanner, systematic overcounting is possible

**Georgia has published no investigation of this pattern.** The MACRO algorithm's risk
calculation treated these discrepancies identically to all others and produced p = 4.17%
for the Governor contest — just below the 5% limit.

---

## The TOOMBS 1-Ballot Anomaly

TOOMBS County, batch `ICC-Absentee by Mail - 9`, contains a single-ballot batch with
a genuinely puzzling discrepancy:

| | Machine (reported) | Auditor (hand count) |
|---|---|---|
| Earl L. "Buddy" Carter (Rep Senate) | **0** | **1** |
| Keisha Lance Bottoms (Dem Gov) | **1** | **0** |
| All other candidates | 0 | 0 |

The machine read this 1-ballot absentee batch as containing one Democratic Governor
vote for Bottoms. The auditor read it as containing one Republican Senate vote for Carter.

HMPB absentee ballots have no QR code — both machine and auditor read the same ink
marks. For machine and auditor to read opposite party contests on the same physical ballot
requires one of:

1. **Dual-party ballot**: Georgia's general primary allows voters to choose a party
   contest. If this 1-ballot batch contains a ballot where a voter marked both a Rep
   Senate choice AND a Dem Gov choice (an invalid overvote across party lines), the
   machine and auditor may have tallied different contests on the same ballot
2. **Two physical ballots**: If this "1-ballot batch" actually contained two ballots
   — one Rep, one Dem — the manifest count of 1 would be wrong and the two ballots
   were separated by the audit process
3. **Scanner column misalignment**: The scanner placed Bottoms' oval in the Carter
   column or vice versa due to ballot alignment error
4. **Auditor error**: The auditor read a Dem ballot and recorded a Rep vote (or
   vice versa)

Georgia has published no investigation of this batch. It is a single ballot with
zero net effect on any contest outcome, but it illustrates the gap between what the
audit detects and what it explains.

---

## Batch Size and the Case for Smaller Batches

The largest single batch audited — NEWTON County `AV-Town ICP 1` — contained 6,381
ballots. Auditors hand-read and tallied 6,381 BMD printed receipts in one audit unit.
Other large AV batches included 5,544 (COBB), 5,214 (PAULDING), 4,677 (CHEROKEE),
and 4,606 (HENRY). Fifteen audited batches exceeded 2,000 ballots, all of them BMD-AV.

### How batch size affects audit workload

In PPEB sampling, each batch's probability of selection is proportional to its maximum
error contribution, which scales approximately with ballot count. If a 6,381-ballot batch
were split into thirteen ~490-ballot sub-batches:

- Each sub-batch would have ~1/13 the selection weight of the original
- Total expected selections across all 13 sub-batches ≈ same as original (total weight
  unchanged)
- But each *actual* selection would require counting ~490 ballots instead of 6,381
- **Result: roughly 13× less counting work per draw**

More precisely: in the current audit, the NEWTON 6,381-ballot batch was selected once
and auditors counted 6,381 receipts. If it had been structured as 13 sub-batches, PPEB
would on average select approximately 1 of the 13 sub-batches, requiring ~490 ballots.
The risk reduction delivered (max_error coverage) is approximately the same.

This is the core argument: **smaller batches deliver the same statistical risk reduction
for proportionally less manual counting labor.**

### Additional benefits of smaller batches

1. **Discrepancy localization**: When a discrepancy is found in a 6,381-ballot batch,
   there are 6,381 candidates for its source. A 490-ballot batch narrows the search.
2. **Auditor fatigue**: Sustained hand-tallying of 6,000 receipts over hours is more
   error-prone than counting 490. The 0.60–0.83‰ BMD discrepancy rate likely reflects
   real auditor counting fatigue — smaller batches would reduce it.
3. **Higher batch-sample diversity**: With more (smaller) batches in the universe,
   a given number of PPEB draws covers more geographic and demographic diversity.
4. **Practical manageability**: A 490-ballot batch can be audited by a team in an
   hour. A 6,381-ballot batch may require an all-day session.

### Per-batch discrepancy rate would fall automatically

If BMD-AV batches were capped at 500 ballots (vs. current median of 1,613), the expected
number of vote discrepancies per batch would drop from ~0.97 to ~0.30. The per-batch
discrepancy rate would fall from ~34% to ~26%. The per-*ballot* rate would remain
unchanged — the underlying error rate is the same — but the per-batch rate would better
reflect the actual audit quality.

**Recommendation:** Georgia should consider establishing maximum batch sizes for AV
scanner batches, consistent with what is already common for HMPB absentee batches
(where ICC containers naturally create small batches of 20–50 ballots). A cap of 500
ballots per batch would make the per-batch discrepancy metric more comparable across
ballot types and make individual batch audits manageable in a standard work session.

---

## Georgia's (Non-)Documentation of Discrepancy Investigation

The published audit artifacts contain:

- ✓ A complete list of every discrepancy (batch, change in results, change in margin)
- ✗ No explanation or categorization of any discrepancy
- ✗ No record of whether any discrepancy was investigated
- ✗ No determination of whether BMD discrepancies reflect auditor error or QR/text mismatch
- ✗ No follow-up documentation on the Jackson directional pattern
- ✗ No investigation of the TOOMBS cross-party ballot anomaly

Several RLA implementations require auditors to record a reason code for each discrepancy
(e.g., ambiguous mark, tally correction, scanner misread) and to document re-examination
of batches with large discrepancies. Georgia's current MACRO batch audit does not require
this under published procedures.

The risk calculation passed at p = 4.91% (Senate) and 4.17% (Governor), well below
the 5% limit. The audit provides reasonable assurance — consistent with the risk-limit
framework — that the declared outcomes are correct. But discrepancy documentation
would convert an audit that *detects* anomalies into one that also *explains* them.

---

## Summary Table

| Finding | Detail |
|---------|--------|
| Total audited batches with discrepancy | 100 / 706 (14.2%) |
| Total absolute vote discrepancies | 257 votes across 341,816 audited ballots (0.75‰) |
| BMD share of all ballots cast | 97.8% (AV 47.8%, ED 50.0%) |
| Ballot coverage by type | ABM 33.7%, BMD-AV 20.9%, BMD-ED 11.3% |
| Per-ballot rate — HMPB-ABM | 2.12‰ — highest, driven by mark-interpretation ambiguity |
| Per-ballot rate — BMD | 0.60–0.83‰ — mostly consistent with auditor tallying error |
| Per-batch BMD rate higher than HMPB | Artifact of much larger BMD batch sizes (median 1,613 vs 24) |
| Largest audited batch | 6,381 ballots (NEWTON AV-Town ICP 1) |
| BMD discrepancy explanations | Not documented; could be auditor error or QR/text mismatch |
| Jackson net discrepancy | Machine overcounted Jackson by 27 net; unexplained |
| TOOMBS 1-ballot batch | Machine read Dem (Bottoms), auditor read Rep (Carter) — unexplained |
| Georgia discrepancy investigation | None published |
| Outcome change from discrepancies | None — risk limit met for both contests |
| Key recommendation | Cap batch sizes (≤ 500 ballots) to reduce audit labor ~proportionally |
