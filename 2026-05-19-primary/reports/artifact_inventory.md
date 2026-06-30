---
layout: default
title: Artifact Inventory
---

# Artifact Inventory — Georgia May 19, 2026 RLA

**Version:** v0.5 &nbsp;·&nbsp; **Review timestamp:** 2026-06-29T23:18:24Z &nbsp;·&nbsp; [Repository](https://github.com/nealmcb/rla-review-arlo) &nbsp;·&nbsp; [← Reports](../)

---

## Source

Georgia Secretary of State June 3, 2026 press release:  
`https://sos.ga.gov/news/raffensperger-announces-primary-risk-limiting-audit-confirms-accurate-vote-count`

All files served via MailChimp CDN (mcusercontent.com → CloudFront).

---

## Downloaded Files

### 1. Final Audit Report

| Field | Value |
|-------|-------|
| URL | `https://mcusercontent.com/bb95d9c7cf4b94c9f44421f7c/files/3bfd233a-ba7a-b94e-5f0c-a43dacbf5aae/final_audit_report_May_19_2026_General_Primary_Election_2026_06_02T2128Z.csv` |
| Filename | `final_audit_report.csv` |
| Size | 430,773 bytes (421 KB) |
| MIME type | application/octet-stream |
| Last-Modified | not provided |
| ETag | not provided |
| SHA256 | `1efa76b808f82527f72bb5bd81d14de1b820bf9b76534fbfc1a5d71663b042a8` |
| Downloaded | 2026-06-29T15:28 UTC |
| Format | CSV (multi-section Arlo export) |

**Contents summary:**
- 726 lines total
- Sections: ELECTION INFO, CONTESTS, AUDIT SETTINGS, ROUNDS, SAMPLED BATCHES
- 706 sampled batch rows (plus 1 Totals row)
- Random seed: `06712221796172622814`
- Risk limit: 5%
- Audit type: BATCH_COMPARISON, MACRO
- Software: Arlo (VotingWorks)

### 2. Ballot Manifests

| Field | Value |
|-------|-------|
| URL | `https://mcusercontent.com/bb95d9c7cf4b94c9f44421f7c/files/161e79a4-c41b-a0b3-f066-21b3f3ceb961/May_19_2026_General_Primary_Election_2026_06_02T2146Z_manifests.zip` |
| Filename | `manifests.zip` |
| Size | 305,256 bytes (299 KB) |
| MIME type | application/zip |
| Last-Modified | not provided |
| ETag | not provided |
| SHA256 | `c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf` |
| Downloaded | 2026-06-29T15:29 UTC |
| Format | ZIP of 159 county CSVs |
| ZIP internal timestamps | 1980-01-01 00:00 (zeroed by tool) |

**Contents summary:**
- 159 county subdirectories, 1 CSV each
- Schema: `Container, Batch Name, Number of Ballots`
- 5,641 total batch rows
- 2,081,564 total ballots
- Voting modes: Election Day, Advance Voting, Absentee by Mail, Provisional

### 3. Candidate Totals (Machine Batch Tallies)

| Field | Value |
|-------|-------|
| URL | `https://mcusercontent.com/bb95d9c7cf4b94c9f44421f7c/files/212e9ebf-d71c-817d-0a44-051c9e192b2a/May_19_2026_General_Primary_Election_2026_06_02T2148Z_candidate_totals.zip` |
| Filename | `candidate_totals.zip` |
| Size | 431,956 bytes (422 KB) |
| MIME type | application/zip |
| Last-Modified | not provided |
| ETag | not provided |
| SHA256 | `2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312` |
| Downloaded | 2026-06-29T15:29 UTC |
| Format | ZIP of 159 county CSVs |
| ZIP internal timestamps | 1980-01-01 00:00 (zeroed) |

**Contents summary:**
- 159 county subdirectories, 1 CSV each
- Schema: `Batch Name, [candidate columns...]`
- 5,640 total batch rows
- Candidates: 5 Republican US Senate, 7 Democratic Governor
- Column headers follow pattern: `{Contest} - {Party} - {Candidate}`

---

## Additional Downloaded File

### Jasper County RLA Results Notice (PDF)

| Field | Value |
|-------|-------|
| URL | `https://jaspercountyga.org/wp-content/uploads/2026/05/RLA-Results-Notice.pdf` |
| Size | 198 KB |
| Created | 2026-05-29T15:53:07-04:00 (per PDF metadata) |
| Author | Amanda Hudgins, Supervisor, Jasper County BOE |

**Contents:** Jasper County successfully completed the RLA on May 29, 2026. Two batches totaling 742 votes were selected, hand-reviewed, and verified. Zero discrepancies. Contests: Republican US Senate and Democratic Governor.

---

## HTTP Header Notes

- Files served via AWS CloudFront with `x-gallery-source: s3` header (MailChimp S3 backend)
- `cache-control: public, max-age=28800` (8-hour cache)
- No `ETag`, `Last-Modified`, or `Content-Disposition` headers provided
- No way to determine original upload date from HTTP headers alone
- The filename in the URL contains a timestamp (`2026_06_02T2128Z`, `2026_06_02T2146Z`, `2026_06_02T2148Z`) suggesting files were generated June 2, 2026 at approximately 9:28 PM, 9:46 PM, and 9:48 PM UTC respectively

---

## Hash Cross-Reference

The SOS June 3 press release states:
> "You can confirm that these were the same batch tallies that we started the audit with by performing a SHA256 hash of the file and matching it to the tweet from Georgia Secretary of State Brad Raffensperger (@GASecofState) from 05/28/2026 at 11:52 AM."

**Both committed hashes verified.** The SHA256 hashes tweeted by @GaSecofState on May 28, 2026 match the currently posted files exactly:

| File | Tweeted hash | Match |
|------|-------------|-------|
| `manifests.zip` | `c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf` | ✓ |
| `candidate_totals.zip` | `2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312` | ✓ |

Note: An earlier version of this investigation used an incorrect prefix (`7d00771bf178007f4c6f43bf45b6`) that does not correspond to either file. The actual tweeted hashes are the full 64-character values above.

See the [Hash Commitment Analysis](../hash_commitment/) for full details.
