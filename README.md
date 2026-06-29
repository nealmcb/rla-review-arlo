# Georgia May 2026 RLA — Transparency Analysis

**Version:** v0.1-draft &nbsp;·&nbsp; **Date:** 2026-06-29

Independent replication and transparency analysis of Georgia's **May 19, 2026 General Primary Risk-Limiting Audit** — BATCH\_COMPARISON/MACRO, Arlo (VotingWorks), all 159 counties, 5% risk limit.

**Full analysis and reports:** https://nealmcb.github.io/ga-rla-2026-05-replication/

---

## What This Repository Contains

| Directory | Contents |
|-----------|----------|
| `downloads/` | Official SOS-published artifacts (final audit report CSV, manifests ZIP, candidate totals ZIP, Jasper County PDF) |
| `extracted/` | Per-county CSVs from both ZIPs (159 counties × 2 artifact types) |
| `reports/` | Six analysis reports (hash verification, sample reproducibility, transparency gap analysis, etc.) |
| `scripts/` | Reproducible Python and shell scripts for hash checking, ticket verification, and artifact inspection |
| `hashes/` | SHA256 and SHA512 checksums of all downloaded files |
| `headers/` | HTTP response headers from all downloads |

## Key Results

- ✓ Both SHA256 hashes committed in the May 28 @GaSecofState tweet **verified** — files are byte-identical to what was committed before hand-counting began
- ✓ Four sample ticket numbers **independently reproduced** from the public seed using `consistent_sampler`
- ✓ Risk limit met: p = 4.91% (Senate Rep), p = 4.17% (Governor Dem)
- ⚠ BMD batches show ~5× higher discrepancy rates than HMPB batches (33.9% AV vs. 6.5% absentee) — see [BMD verifiability discussion](https://nealmcb.github.io/ga-rla-2026-05-replication/#bmd-verifiability-and-the-voter-verification-gap)
- ⚠ Only two contests audited — no RLA evidence exists for any other contest on the May 19 ballot
- ⚠ Hash commitment was ~3 minutes post-seed, not pre-seed

## Quick Start

```bash
git clone https://github.com/nealmcb/ga-rla-2026-05-replication.git
cd ga-rla-2026-05-replication
pip install consistent_sampler numpy

# Verify the two committed hashes
sha256sum downloads/manifests.zip downloads/candidate_totals.zip

# Reproduce ticket numbers from the public seed
python3 scripts/reproduce_sample.py
```

## Credits

Code and analysis by Claude Sonnet 4.6 (Anthropic) under prompts and direction from Neal McBurnett. See [About This Repository](https://nealmcb.github.io/ga-rla-2026-05-replication/#about-this-repository) for details.

## Comments

Questions and corrections are welcome as [GitHub Issues](https://github.com/nealmcb/ga-rla-2026-05-replication/issues).
