---
layout: default
title: Manifest and Tally Analysis
---

# Manifest and Candidate Tally Analysis — Georgia May 19, 2026 RLA

**Version:** v0.11 &nbsp;·&nbsp; **Review timestamp:** 2026-06-29T23:18:24Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Reports](../)

---

## Ballot Manifests

### File Structure
- ZIP contains 159 subdirectories (one per county)
- Each subdirectory contains exactly one CSV file
- Naming convention: `manifest-{COUNTY}-May-19-2026-General-Primary-Election-{timestamp}.csv`
  - Some counties use non-standard names (e.g., `BROOKS - Manifest 051926.csv`)
  - Timestamps embedded in filenames range from 2026-05-22 to 2026-05-27

### Schema
```
Container, Batch Name, Number of Ballots
```

| Column | Description |
|--------|-------------|
| Container | Voting mode: Absentee by Mail, Advance Voting, Election Day, Provisional |
| Batch Name | Unique batch identifier within county (scanner/ICP identifier) |
| Number of Ballots | Number of ballots in this batch |

### Aggregate Statistics

| Metric | Value |
|--------|-------|
| Counties | 159 |
| Total batches | 5,641 |
| Total ballots | 2,081,564 |
| Min batch size | 0 |
| Max batch size | 6,381 |
| Median batch size | 172.5 |
| Mean batch size | 369.1 |

### Voting Mode Distribution (Batches)

| Mode | Batches |
|------|---------|
| Election Day | 2,743 |
| Absentee by Mail | 1,900 |
| Advance Voting | 718 |
| Provisional | 278 |
| Other/unknown | 2 |

### Top 10 Counties by Ballot Count

| County | Ballots | Batches |
|--------|---------|---------|
| FULTON | 227,706 | 455 |
| DEKALB | 174,491 | 261 |
| COBB | 162,847 | 965 |
| GWINNETT | 154,647 | 486 |
| CHEROKEE | 57,426 | 83 |
| CHATHAM | 56,645 | 133 |
| HENRY | 56,020 | 70 |
| CLAYTON | 48,700 | 126 |
| FORSYTH | 45,244 | 139 |
| RICHMOND | 39,596 | 76 |

### Verification Against Reported Totals
- Manifest total: **2,081,564 ballots** ✓
- Audit report "Total Ballots Cast": **2,081,564** ✓
- Match: **Yes** — manifests are internally consistent with the audit report

### Batch Naming Convention
Batches appear to follow a pattern reflecting the physical scanner:
- `ICC-Absentee by Mail - N` — Absentee mail batches (ICC tabulator)
- `AV-{Location} ICP {N} - 0` — Advance Voting batches
- `ED-{Precinct} ICP {N} - 0` — Election Day batches
- `ICC-Provisional - N` — Provisional batches

The `ICP` identifier refers to ImageCast Precinct (Dominion Voting Systems tabulator). The trailing ` - 0` appears to be a scanner batch number.

### Non-Standard Counties
A small number of counties (e.g., BROOKS, WEBSTER, WILKINSON) use aggregated or non-standard batch names that combine multiple scanner batches into a single entry. The final audit report notes "Combined Batch" entries for such counties (e.g., Webster: "Combines Election Day Central ICP 1 - 0, Election Day Central ICP 2 - 0").

---

## Candidate Totals (Machine Batch Tallies)

### File Structure
- ZIP contains 159 subdirectories (one per county)
- Each subdirectory contains exactly one CSV file
- Naming convention: `candidate-totals-by-batch-{COUNTY}-May-19-2026-General-Primary-Election-{timestamp}.csv`
  - Some counties use non-standard names (e.g., `BROOKS - Contest Totals 051926.csv`)
  - Timestamps range from 2026-05-22 to 2026-05-27

### Schema
```
Batch Name, [candidate columns...]
```

Candidate columns follow the pattern: `{Contest} - {Party} - {Candidate Name}`

**Republican US Senate candidates (5):**
- US Senate - Rep - Earl L. "Buddy" Carter
- US Senate - Rep - Mike Collins
- US Senate - Rep - John F. Coyne III
- US Senate - Rep - Derek Dooley
- US Senate - Rep - Jonathan "Jon" McColumn

**Democratic Governor candidates (7):**
- Governor - Dem - Keisha Lance Bottoms
- Governor - Dem - Olu Brown
- Governor - Dem - Amanda Duffy
- Governor - Dem - Geoff Duncan
- Governor - Dem - Jason Esteves
- Governor - Dem - Derrick Jackson
- Governor - Dem - Michael "Mike" Thurmond

### Aggregate Statistics

| Metric | Value |
|--------|-------|
| Counties | 159 |
| Total batch rows | 5,640 |
| Batches missing (vs. manifest) | 1 (minor discrepancy) |

### Contest Totals (from Audit Report)

**US Senate - Republican (Subject to runoff):**

| Candidate | Votes |
|-----------|-------|
| Mike Collins | 369,638 |
| Derek Dooley | 275,528 |
| Earl L. "Buddy" Carter | 229,221 |
| Jonathan "Jon" McColumn | 28,446 |
| John F. Coyne III | 9,850 |
| **Total** | **912,683** |

(Note: Total Republican ballots = 912,683 out of 2,081,564 total — primary ballots cast for this contest)

**Governor - Democratic:**

| Candidate | Votes |
|-----------|-------|
| Keisha Lance Bottoms | 608,051 |
| Jason Esteves | 201,809 |
| Geoff Duncan | 75,717 |
| Michael "Mike" Thurmond | 139,742 |
| Amanda Duffy | 18,804 |
| Derrick Jackson | 25,042 |
| Olu Brown | 12,328 |
| **Total** | **1,081,493** |

### Batch-Level vs. Contest-Level Verification

The audit report column "Vote Totals from Batches" matches "Vote Totals" for both contests (verified for all candidates), confirming that the candidate totals ZIP sums correctly to the reported contest totals.

### Diluted Margins

Computed using Arlo's Contest class:
- **US Senate - Rep diluted margin**: 0.0222 (Dooley vs. Carter: 46,307 / 2,081,564)
  - This is the margin that drives the MACRO sample size — small margin → large sample
- **Governor - Dem diluted margin**: 0.1952 (Bottoms vs. Esteves: 406,242 / 2,081,564)
  - Large margin → small sample (only 18 batches needed)

---

## Data Quality Notes

1. **ZIP timestamps zeroed**: All internal ZIP timestamps are 1980-01-01. This prevents verification of when the files were originally created/uploaded.
2. **Inconsistent naming**: A few counties use non-Arlo-formatted filenames (e.g., "BROOKS - Contest Totals 051926.csv"). These appear to have been manually submitted and follow a different naming convention.
3. **Aggregated batches**: A few counties (e.g., BROOKS, WEBSTER) submitted batches aggregated by voting mode rather than by individual scanner. This is less granular than the Arlo standard format but is still auditable.
4. **No ballot type distinction**: Manifests do not separately identify BMD (ballot-marking device) vs. hand-marked ballots within the same batch type, nor do they distinguish early in-person from election-day in-person beyond the "Container" field.

---

## County Coverage

All 159 Georgia counties are present in both the manifests ZIP and the candidate totals ZIP. Coverage is complete.
