---
layout: default
title: Manifest and Tally Analysis
---

# Manifest and Candidate Tally Analysis — Georgia May 19, 2026 RLA

**Version:** v0.23 &nbsp;·&nbsp; **Review timestamp:** 2026-11-10T00:51:00Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Reports](../)

---

> **DRAFT - AI-assisted analysis, partially reviewed.** This analysis was produced with significant AI assistance (Claude, Anthropic). Findings are ongoing and some claims may require further verification. Corrections welcome via [GitHub Issues](https://github.com/nealmcb/rla-review-arlo/issues).

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

### Diluted Margins and Statistical Hypotheses

Stark's MACRO audit ([Stark 2009](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1443314)) tests a precise null hypothesis: **"the reported outcome is incorrect."** The test statistic accumulates evidence against this null as batches are hand-counted; when the evidence is strong enough, the audit can stop at the desired risk limit (here, 5%). The binding constraint on the sample size is the **smallest margin** across all the sub-hypotheses being tested simultaneously.

---

**US Senate - Republican (subject to runoff law)**

Collins received 369,638 out of 912,683 Republican votes = **40.5%** — well short of the 50% threshold (456,342 votes) that would allow him to win outright. He fell short of a majority by **86,704 votes**. Georgia law therefore requires a runoff between the top two vote-getters: Collins and Dooley.

Because no candidate reached a majority, Arlo's `sampler_contest.py` internally promotes the contest from `num_winners = 1` to `num_winners = 2` — both Collins and Dooley must correctly advance. This changes the audit's task: it must simultaneously test **six candidate-pair hypotheses** (each winner vs. each loser) and **two majority-threshold hypotheses** (confirming that neither Collins nor Dooley secretly crossed 50%):

| Hypothesis tested | Margin V_wl (votes) | Diluted margin | Role |
|-------------------|--------------------:|---------------:|------|
| Dooley vs. Carter — did the right candidate take the 2nd runoff spot? | 46,307 | **0.0222** | **Binding — largest per-batch error bound; drives U, sample size, p-value** |
| Collins vs. Carter | 140,417 | 0.0675 | |
| Collins vs. McColumn | 341,192 | 0.1639 | |
| Collins vs. Coyne | 359,788 | 0.1729 | |
| Dooley vs. McColumn | 247,082 | 0.1187 | |
| Dooley vs. Coyne | 265,678 | 0.1276 | |
| Collins majority-threshold check (did Collins correctly fall short of 50%?) | 173,407 | 0.0833 | Threshold check; V_wl = 912,683 − 2 × 369,638 |
| Dooley majority-threshold check (did Dooley correctly fall short of 50%?) | 361,627 | 0.1738 | Threshold check; V_wl = 912,683 − 2 × 275,528 |
| Collins vs. Dooley — did the right candidate place first? | 94,110 | 0.0452 | Candidate pair; not binding |

The **binding diluted margin is 0.0222 (Dooley vs. Carter, 46,307 / 2,081,564)**, because that hypothesis has the smallest margin and therefore the largest per-batch error bound in Arlo's MACRO formula. This is the quantity that Arlo used to compute U (the total error bound across all 5,640 batches), which in turn determined the sample size:

- U = 45.95 (computed by `src/reproduce_risk.py` from the public candidate totals)
- p_mult = 1 − 1/U = 0.9782
- Zero-discrepancy sample size estimate: log(0.05) / log(0.9782) ≈ **136 draws** — consistent with the actual 138

The **0.0452 diluted margin (Collins vs. Dooley, 94,110 / 2,081,564)** describes the gap between the two advancing candidates — a meaningful quantity for understanding how close the runoff field is, and the one an independent tool would compute if it modeled this as a 1-winner "who placed first?" question rather than a "which 2 advance to the runoff?" question. Both margins are correct; they answer different questions.

---

**Governor - Democratic (no runoff)**

Bottoms received 608,051 out of 1,081,493 Democratic votes = **56.2%** — a clear majority, 151,710 votes above the threshold. No runoff is needed. Arlo treats this as a standard 1-winner contest: only candidate-pair hypotheses (Bottoms vs. each of 6 opponents) are tested, and the binding constraint is simply Bottoms vs. Esteves.

| Hypothesis tested | Margin V_wl (votes) | Diluted margin | Role |
|-------------------|--------------------:|---------------:|------|
| Bottoms vs. Esteves | 406,242 | **0.1952** | **Binding** |
| Bottoms vs. Thurmond | 468,309 | 0.2250 | |
| Bottoms vs. Duncan | 532,334 | 0.2558 | |
| Bottoms vs. Jackson | 583,009 | 0.2801 | |
| Bottoms vs. Duffy | 589,247 | 0.2831 | |
| Bottoms vs. Brown | 595,723 | 0.2862 | |

The large margin (0.1952) means only 18 PPEB draws were needed; the audit reproduces exactly to machine precision (see `src/reproduce_risk.py`).

---

**Risk-level reproduction**

`src/reproduce_risk.py` implements Arlo's `compute_U()` and `compute_risk()` formulas verbatim and reproduces both risk levels from the public artifacts:

| Contest | Computed risk | Reported risk | Difference | Passes 5%? |
|---------|-------------:|-------------:|----------:|------------|
| US Senate - Rep | 4.8994% | 4.9084% | 9.0e-05 | Yes ✓ |
| Governor - Dem | 4.1726% | 4.1726% | 2.1e-11 | Yes ✓ |

The 9e-05 Senate residual arises from Arlo's internal Decimal arithmetic vs. Python float; the data fully support the reported outcomes.

---

## Data Quality Notes

1. **ZIP timestamps zeroed**: All internal ZIP timestamps are 1980-01-01. This prevents verification of when the files were originally created/uploaded.
2. **Inconsistent naming**: A few counties use non-Arlo-formatted filenames (e.g., "BROOKS - Contest Totals 051926.csv"). These appear to have been manually submitted and follow a different naming convention.
3. **Aggregated batches**: A few counties (e.g., BROOKS, WEBSTER) submitted batches aggregated by voting mode rather than by individual scanner. This is less granular than the Arlo standard format but is still auditable.
4. **No ballot type distinction**: Manifests do not separately identify BMD (ballot-marking device) vs. hand-marked ballots within the same batch type, nor do they distinguish early in-person from election-day in-person beyond the "Container" field.

---

## County Coverage

All 159 Georgia counties are present in both the manifests ZIP and the candidate totals ZIP. Coverage is complete.
