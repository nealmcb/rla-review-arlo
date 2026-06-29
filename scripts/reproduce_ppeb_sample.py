"""
Reproduce the full PPEB (Proportional-with-Error-Bound) sample draw for Georgia's
May 19, 2026 General Primary RLA using Arlo's sampler logic and numpy 1.26.4
(matching Arlo's poetry.lock pin).

Requires: pip install consistent_sampler "numpy==1.26.4"

Usage: python3 scripts/reproduce_ppeb_sample.py

Key findings on batch ordering (required for exact reproduction):
  - Counties must be in ALPHABETICAL order (how Arlo queries its database:
    ORDER BY jurisdiction.name).
  - Batches within each county must be in CSV ROW ORDER (the order Arlo
    inserted them when the county uploaded its candidate-totals CSV).
  - Two county directory names use hyphens where Arlo stores spaces:
    BEN-HILL -> BEN HILL, JEFF-DAVIS -> JEFF DAVIS.

Fulton County container batches:
  Fulton uploaded many scanner batches split across multiple containers, e.g.
  "ICC - AV-Grant Park Rec Ctr ICP 3 - 1" through "- 8". Arlo's PPEB draw
  selects one container (the one with the highest weight / selected index),
  then the audit report strips the suffix and combines all containers of the
  same scanner for counting. The ticket number on the drawn container matches
  the ticket shown for the aggregate in the audit report.
"""
import csv, sys, re, pathlib, consistent_sampler as cs

# ── Sanity-check numpy version ────────────────────────────────────────────────
import numpy as np
if not np.__version__.startswith("1.26"):
    print(f"WARNING: numpy {np.__version__} loaded; Arlo pins to 1.26.4. "
          "Results may differ from the original audit draw.", file=sys.stderr)

# ── Load patched Arlo source files from /tmp ──────────────────────────────────
# Patched files replace relative imports with absolute imports.
# Created by fetching Arlo's audit_math/macro.py, sampler.py, sampler_contest.py
# from github.com/votingworks/arlo and substituting relative import paths.
sys.path.insert(0, "/tmp")
import arlo_sampler_contest, arlo_macro2, arlo_sampler2

draw_ppeb_sample = arlo_sampler2.draw_ppeb_sample
Contest          = arlo_sampler_contest.Contest

# ── Parse audit report for contest totals and sample sizes ────────────────────
SEED      = "06712221796172622814"
ROOT      = pathlib.Path(__file__).parent.parent
AUDIT_CSV = ROOT / "downloads/final_audit_report.csv"

with open(AUDIT_CSV) as f:
    lines = f.readlines()

def section_start(lines, keyword):
    return next(i for i, l in enumerate(lines) if keyword in l) + 1

def parse_vote_totals(s):
    """'Earl L. "Buddy" Carter: 229221; Mike Collins: 369638' -> dict"""
    result = {}
    for part in s.split(";"):
        part = part.strip()
        if ": " not in part:
            continue
        cand, votes = part.rsplit(": ", 1)
        result[cand.strip()] = int(votes.strip())
    return result

# CONTESTS section
contests_start  = section_start(lines, "CONTESTS")
contest_header  = list(csv.reader([lines[contests_start]]))[0]
contest_rows    = []
for line in lines[contests_start + 1:]:
    if not line.strip() or line.startswith("#"):
        break
    row = list(csv.reader([line]))[0]
    if row and row[0]:
        contest_rows.append(dict(zip(contest_header, row)))

# ROUNDS section — sample sizes per contest
rounds_start = section_start(lines, "ROUNDS")
round_header = list(csv.reader([lines[rounds_start]]))[0]
sample_sizes = {}
for line in lines[rounds_start + 1:]:
    if not line.strip() or line.startswith("#"):
        break
    row = dict(zip(round_header, list(csv.reader([line]))[0]))
    if row.get("Round Number") == "1" and row.get("Contest Name"):
        sample_sizes[row["Contest Name"]] = int(row["Sample Size"])

print("Sample sizes from audit report:", sample_sizes)

# Build Contest objects
CONTESTS = {}
for row in contest_rows:
    cname = row.get("Contest Name", "").strip()
    if not cname:
        continue
    info = {
        "ballots":           int(row["Total Ballots Cast"].replace(",", "")),
        "numWinners":        int(row["Number of Winners"]),
        "votesAllowed":      int(row["Votes Allowed"]),
        "isSubjectToRunoff": "runoff" in row.get("Runoff Law", "").lower(),
    }
    info.update(parse_vote_totals(row["Vote Totals"]))
    CONTESTS[cname] = Contest(cname, info)

print("\nContests loaded:")
for name, c in CONTESTS.items():
    print(f"  {name}: winners={c.num_winners}, runoff={c.is_subject_to_runoff}, "
          f"diluted_margin={c.diluted_margin:.4f}, ballots={c.ballots:,}")

# ── County name normalization ─────────────────────────────────────────────────
COUNTY_NAME_MAP = {
    "BEN-HILL":  "BEN HILL",
    "JEFF-DAVIS": "JEFF DAVIS",
}

def norm_county(dir_name):
    return COUNTY_NAME_MAP.get(dir_name.upper(), dir_name.upper())

# ── Build batch_results: alphabetical county + CSV row order within county ────
# Schema: {(county, batch_name): {contest_name: {"ballots": n, cand: votes}}}

MANIFEST_DIR = ROOT / "extracted/manifests"
TOTALS_DIR   = ROOT / "extracted/candidate_totals"

# Load manifest ballot counts (county/batch → count)
ballot_counts = {}
for county_dir in sorted(MANIFEST_DIR.iterdir()):
    county = norm_county(county_dir.name)
    for csv_file in county_dir.glob("*.csv"):
        with open(csv_file, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                bn_keys = [k for k in row if "batch" in k.lower() or "name" in k.lower()]
                n_keys  = [k for k in row if "number" in k.lower() or "ballot" in k.lower()]
                if not bn_keys or not n_keys:
                    continue
                batch = row[bn_keys[0]].strip()
                try:
                    count = int(row[n_keys[0]].strip())
                except (ValueError, KeyError):
                    count = 0
                ballot_counts[(county, batch)] = count

print(f"\nManifest batches loaded: {len(ballot_counts):,}")

# Load candidate totals in ALPHABETICAL county order + CSV row order per county
CONTEST_NAMES = list(CONTESTS.keys())
ALL_CANDS     = {cn: list(c.candidates.keys()) for cn, c in CONTESTS.items()}

def col_to_contest_cand(col):
    """'US Senate - Rep - Derek Dooley' -> ('US Senate - Rep', 'Derek Dooley')"""
    for cn in CONTEST_NAMES:
        if col.startswith(cn + " - "):
            return cn, col[len(cn) + 3:]
    return None, None

ordered_keys = []
cand_votes   = {}
seen_keys    = set()

for county_dir in sorted(TOTALS_DIR.iterdir(), key=lambda d: d.name.upper()):
    county = norm_county(county_dir.name)
    for csv_file in county_dir.glob("*.csv"):
        with open(csv_file, encoding="utf-8-sig") as f:
            reader    = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            for row in reader:
                batch = row.get("Batch Name", "").strip()
                if not batch:
                    continue
                key   = (county, batch)
                votes = {}
                for col in fieldnames:
                    if col == "Batch Name":
                        continue
                    try:
                        votes[col] = int(row[col])
                    except (ValueError, KeyError):
                        votes[col] = 0
                cand_votes[key] = votes
                if key not in seen_keys:
                    ordered_keys.append(key)
                    seen_keys.add(key)

# Append any manifest-only keys at the end
for k in ballot_counts:
    if k not in seen_keys:
        ordered_keys.append(k)
        seen_keys.add(k)

print(f"Candidate-totals batches loaded (unique): {len(ordered_keys):,}")

# Build batch_results in ordered_keys order
batch_results = {}
for key in ordered_keys:
    n_ballots = ballot_counts.get(key, 0)
    votes     = cand_votes.get(key, {})
    entry = {cn: {"ballots": n_ballots, **{c: 0 for c in ALL_CANDS[cn]}}
             for cn in CONTEST_NAMES}
    for col, v in votes.items():
        cn, cand = col_to_contest_cand(col)
        if cn is None or cand not in entry.get(cn, {}):
            continue
        entry[cn][cand] = v
    batch_results[key] = entry

print(f"batch_results built: {len(batch_results):,} batches")

# ── Load expected sample from audit report ────────────────────────────────────
batch_start = next(i for i, l in enumerate(lines) if "SAMPLED BATCHES" in l) + 1
audit_rows  = []
for line in lines[batch_start + 1:]:
    if not line.strip() or "########" in line:
        break
    r = list(csv.reader([line]))[0]
    if len(r) >= 6 and r[0] not in ("", "Totals", "Jurisdiction Name"):
        audit_rows.append(r)

expected_rep = {}  # county -> set of batch base names (suffix stripped)
expected_dem = {}
for r in audit_rows:
    county = COUNTY_NAME_MAP.get(r[0].upper().strip(), r[0].upper().strip())
    batch  = r[1].strip()
    tk_rep = r[3].strip() if len(r) > 3 else ""
    tk_dem = r[4].strip() if len(r) > 4 else ""
    # Strip trailing " - N" container suffix for comparison (Fulton container aggregation)
    base_batch = re.sub(r"\s+-\s+\d+$", "", batch)
    if tk_rep.startswith("Round") and "EXTRA" not in tk_rep:
        expected_rep.setdefault(county, set()).add((county, base_batch))
    if tk_dem.startswith("Round") and "EXTRA" not in tk_dem:
        expected_dem.setdefault(county, set()).add((county, base_batch))

exp_rep_set = {b for s in expected_rep.values() for b in s}
exp_dem_set = {b for s in expected_dem.values() for b in s}
print(f"\nExpected sampled batches: Rep={len(exp_rep_set)}, Dem={len(exp_dem_set)}")

def strip_container_suffix(batch_name):
    """Strip trailing ' - N' container number so drawn containers match audit aggregate names."""
    return re.sub(r"\s+-\s+\d+$", "", batch_name)

# ── Run PPEB draw and compare ─────────────────────────────────────────────────
for contest_name, contest in CONTESTS.items():
    ss = sample_sizes.get(contest_name)
    if not ss:
        print(f"\nNo sample size for {contest_name}, skipping")
        continue
    print(f"\n── {contest_name}: drawing {ss} batches ──")
    try:
        result = draw_ppeb_sample(SEED, contest, ss, [], batch_results)
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback; traceback.print_exc()
        continue

    # Normalise drawn batch keys: strip container suffix for comparison
    drawn_normalised = {(county, strip_container_suffix(batch))
                        for county, batch in {bk for _, bk in result}}
    drawn_raw        = {bk for _, bk in result}

    expected = exp_rep_set if "Senate" in contest_name else exp_dem_set
    hit   = drawn_normalised & expected
    miss  = expected - drawn_normalised
    extra = drawn_raw - {(c, b) for c, b in drawn_normalised if (c, b) in expected}

    print(f"  Drew {len(result)} tickets → {len(drawn_raw)} unique batches (raw)")
    print(f"  Match vs audit report: {len(hit)}/{len(expected)}  "
          f"{'✓ FULL MATCH' if not miss else ''}")
    if miss:
        print(f"  MISSING: {sorted(miss)[:10]}")
    if extra and miss:
        print(f"  EXTRA (raw batch names): {sorted(extra)[:10]}")

# ── Verify ticket numbers for all sampled batches ────────────────────────────
print("\n── Spot-check: ticket verification for first 8 sampled Rep batches ──")
verified = 0
total    = 0
for r in audit_rows[:30]:
    county = COUNTY_NAME_MAP.get(r[0].upper().strip(), r[0].upper().strip())
    batch  = r[1].strip()
    tk_rep = r[3].strip() if len(r) > 3 else ""
    if not (tk_rep.startswith("Round") and "EXTRA" not in tk_rep):
        continue
    expected_tk = tk_rep.replace("Round 1: ", "")
    computed_tk = cs.trim(cs.first_fraction((county, batch), SEED), 18)
    # For Fulton aggregates the audit batch name is the base name, but the
    # ticket was computed on the individual container. Match is confirmed separately.
    match = computed_tk == expected_tk
    total += 1
    if match:
        verified += 1
    status = "✓" if match else "✗"
    if total <= 8:
        print(f"  {status} ({county}, {batch!r}: {computed_tk})")
    if total >= 8:
        break
print(f"\n  {verified}/{total} spot-check tickets verified")
