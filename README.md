# rla-review-arlo

Code and results for independent review and transparency analysis of Risk-Limiting Audits using the [Arlo RLA software](https://github.com/votingworks/arlo) (VotingWorks).

Each audit review independently verifies official artifacts, reproduces the sample selection, analyzes discrepancy patterns, and evaluates transparency against the checklist in [Arlo PR #2350](https://github.com/votingworks/arlo/pull/2350).

**Full reports:** https://nealmcb.github.io/rla-review-arlo/

---

## Audit Reviews

| Audit | Date | Contests | Reports |
|-------|------|----------|---------|
| [Georgia November 4, 2025 Special Election](2025-11-04-special/index.md) | 2025-11-04 | PSC District 2 | [Review](https://nealmcb.github.io/rla-review-arlo/2025-11-04-special/) |
| [Georgia May 19, 2026 General Primary](2026-05-19-primary/index.md) | 2026-05-19 | US Senate (R), Governor (D) | [Reports](https://nealmcb.github.io/rla-review-arlo/2026-05-19-primary/reports/) |

---

## Code (`src/`)

Scripts are designed to run from the repository root. Each audit's data lives in its own dated subdirectory (e.g., `2026-05-19-primary/`).

| Script | Purpose |
|--------|---------|
| `src/download_artifacts.sh` | Download official artifacts from SOS-published URLs |
| `src/hash_artifacts.sh` | Compute SHA256 checksums of all downloaded and extracted files |
| `src/inspect_artifacts.py` | Parse and summarize Arlo audit report CSV structure |
| `src/summarize_manifests.py` | Ballot manifest statistics (county, batch, and ballot counts) |
| `src/reproduce_sample.py` | Verify individual batch ticket numbers from the public seed |
| `src/reproduce_ppeb_sample.py` | Reproduce the full PPEB weighted sample draw |
| `src/search_for_hash.py` | Search all artifact files for a given SHA256 prefix |

### Dependencies

```
pip install -r requirements.txt
```

`requirements.txt` pins `numpy==1.26.4` to match Arlo's `poetry.lock` — required for exact reproduction of the PPEB weighted draw. Other versions of numpy give different results due to changes in `SeedSequence` behavior across major versions.

---

## Methodology

Each review applies a common checklist:

1. **Artifact integrity** — Download official files; compute and compare SHA256 hashes against any public commitments
2. **Hash commitment timing** — Determine when hashes were published relative to the audit seed entry; assess what that timing does and does not protect
3. **Sample reproducibility** — Independently reproduce batch ticket numbers (verifiable for any batch) and, where possible, the full weighted draw
4. **Risk level verification** — Confirm that the reported risk levels follow from the published batch totals, hand counts, and MACRO formula
5. **Discrepancy analysis** — Examine batch-level discrepancies by ballot type and batch size; note what the data does and does not reveal about actual counting accuracy

This framework follows the transparency principles in [Arlo PR #2350](https://github.com/votingworks/arlo/pull/2350), which distinguishes "audit was conducted" from "audit is independently verifiable by any member of the public."

---

## Quick Start (Georgia May 2026 Primary)

```bash
git clone https://github.com/nealmcb/rla-review-arlo.git
cd rla-review-arlo
pip install -r requirements.txt

# Verify SHA256 hashes of the two hash-committed ZIPs
sha256sum 2026-05-19-primary/downloads/manifests.zip \
          2026-05-19-primary/downloads/candidate_totals.zip
# Expected:
# c31d1f67404634ea04b4c68a5272655c9bd3879fe2233f4878819963cfc17aaf  manifests.zip
# 2842be86bd615160f36f0af8f6d52a2fe1192103163dd51de8d8a1617ca10312  candidate_totals.zip

# Verify individual batch ticket numbers from the public seed
python3 src/reproduce_sample.py

# Reproduce the full PPEB weighted sample draw (134/134 + 18/18 match)
python3 src/reproduce_ppeb_sample.py
```

---

## Credits

The Georgia May 2026 review was directed by Neal McBurnett, an election security researcher and author of [Arlo PR #2350](https://github.com/votingworks/arlo/pull/2350) ("docs: Arlo comparison audit transparency report and guide").

Questions and corrections are welcome as [GitHub Issues](https://github.com/nealmcb/rla-review-arlo/issues).
