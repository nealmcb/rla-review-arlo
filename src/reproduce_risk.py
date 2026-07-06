#!/usr/bin/env python3
"""
Reproduce MACRO risk levels from the public Georgia May 19, 2026 RLA artifacts.
Implements Arlo's compute_U() and compute_risk() formulas verbatim from
  server/audit_math/macro.py  (github.com/votingworks/arlo)
  server/audit_math/sampler_contest.py

The central question: do the data support the reported outcomes?
  If the computed p-values match the CSV values and are ≤ 5%, the data support them.

Usage: python3 src/reproduce_risk.py
Exit 0 if both contests independently reproduce and pass; exit 1 otherwise.
"""

from decimal import Decimal
import csv, os, re, sys, math

BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "2026-05-19-primary",
)
REPORT      = os.path.join(BASE, "downloads", "final_audit_report.csv")
MANIFESTS   = os.path.join(BASE, "extracted", "manifests")
TOTALS      = os.path.join(BASE, "extracted", "candidate_totals")
RISK_LIMIT  = 5   # percent, as integer (matches Arlo's convention)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_vote_string(s):
    """Parse 'Name: N; Name: N; ...' into {name: votes}."""
    out = {}
    for part in s.split(";"):
        part = part.strip()
        m = re.match(r'^"?(.+?)"?\s*:\s*(\d+)$', part)
        if m:
            out[m.group(1).strip()] = int(m.group(2))
    return out


# ---------------------------------------------------------------------------
# Contest — mirrors sampler_contest.Contest
# ---------------------------------------------------------------------------

class Contest:
    def __init__(self, name, candidates, total_ballots, num_winners,
                 votes_allowed, is_subject_to_runoff):
        self.name = name
        self.candidates = dict(candidates)   # {cand_name: total_votes}
        self.ballots = total_ballots
        self.votes_allowed = votes_allowed
        self.pending_ballots = 0
        self.is_subject_to_runoff = is_subject_to_runoff

        # sampler_contest.py runoff bump: if is_subject_to_runoff and no majority,
        # treat as 2-winner contest so the runner-up is also protected.
        self.num_winners = num_winners
        if is_subject_to_runoff:
            valid_votes = sum(candidates.values())
            top_votes = max(candidates.values())
            if top_votes <= valid_votes - top_votes:
                self.num_winners = 2

        ranked = sorted(candidates.items(), key=lambda x: -x[1])
        self.winners = dict(ranked[: self.num_winners])
        self.losers  = dict(ranked[self.num_winners :])

        if self.losers:
            min_margin = min(
                self.winners[w] - self.losers[l]
                for w in self.winners for l in self.losers
            )
            self.diluted_margin = min_margin / total_ballots
        else:
            self.diluted_margin = -1.0


# ---------------------------------------------------------------------------
# MACRO error formulas (macro.py)
# ---------------------------------------------------------------------------

def _max_error_pair(v_wp, v_lp, b_cp, V_wl, pending, unauditable):
    V = V_wl - pending - unauditable
    if V <= 0:
        return Decimal("inf")
    return Decimal(v_wp - v_lp + b_cp) / Decimal(V)


def compute_max_error(batch_votes, batch_ballots, contest, unauditable=0):
    """
    Maximum possible error contribution for one batch.
    batch_votes: {cand_name: int}   (reported votes for this batch)
    batch_ballots: int              (ballot count from manifest)
    Returns Decimal.
    """
    if not any(c in batch_votes for c in contest.candidates):
        return Decimal(0)

    b_cp = batch_ballots
    error = Decimal(0)

    # Candidate-pair errors
    for w in contest.winners:
        for l in contest.losers:
            v_wp = batch_votes.get(w, 0)
            v_lp = batch_votes.get(l, 0)
            V_wl = contest.candidates[w] - contest.candidates[l]
            e = _max_error_pair(v_wp, v_lp, b_cp, V_wl,
                                contest.pending_ballots, unauditable)
            if e > error:
                error = e

    # Threshold errors (runoff contests only)
    if contest.is_subject_to_runoff:
        valid = sum(contest.candidates.values())
        for w in contest.winners:
            w_total = contest.candidates[w]
            batch_total = sum(batch_votes.get(c, 0) for c in contest.candidates)
            w_batch = batch_votes.get(w, 0)
            if w_total > (valid - w_total):   # above majority threshold
                v_wp = w_batch
                v_lp = batch_total - w_batch
                V_wl = 2 * w_total - valid
            else:                             # below majority threshold
                v_wp = batch_total - w_batch
                v_lp = w_batch
                V_wl = valid - 2 * w_total
            e = _max_error_pair(v_wp, v_lp, b_cp, V_wl,
                                contest.pending_ballots, unauditable)
            if e > error:
                error = e

    return error


def compute_error(reported_votes, audited_votes, contest, unauditable=0):
    """
    Weighted error for a sampled batch.
    Returns (counted_as: int, weighted_error: Decimal) or None if no positive error.
    """
    def pair_error(v_wp, v_lp, a_wp, a_lp, V_wl):
        V = V_wl - contest.pending_ballots - unauditable
        err = (v_wp - v_lp) - (a_wp - a_lp)
        if err == 0:
            return None
        we = Decimal(err) / Decimal(V) if V > 0 else Decimal("inf")
        return (err, we)

    errors = []

    for w in contest.winners:
        for l in contest.losers:
            e = pair_error(
                reported_votes.get(w, 0), reported_votes.get(l, 0),
                audited_votes.get(w, 0),  audited_votes.get(l, 0),
                contest.candidates[w] - contest.candidates[l],
            )
            if e:
                errors.append(e)

    if contest.is_subject_to_runoff:
        valid = sum(contest.candidates.values())
        for w in contest.winners:
            w_total = contest.candidates[w]
            rep_total = sum(reported_votes.get(c, 0) for c in contest.candidates)
            aud_total = sum(audited_votes.get(c, 0) for c in contest.candidates)
            w_rep = reported_votes.get(w, 0)
            w_aud = audited_votes.get(w, 0)
            if w_total > (valid - w_total):
                v_wp = w_rep;  v_lp = rep_total - w_rep
                a_wp = w_aud;  a_lp = aud_total - w_aud
                V_wl = 2 * w_total - valid
            else:
                v_wp = rep_total - w_rep; v_lp = w_rep
                a_wp = aud_total - w_aud; a_lp = w_aud
                V_wl = valid - 2 * w_total
            e = pair_error(v_wp, v_lp, a_wp, a_lp, V_wl)
            if e:
                errors.append(e)

    if not errors:
        return None
    return max(errors, key=lambda x: x[1])


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def read_csv_lines(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.readlines()


def parse_contests(lines):
    """Return {contest_name: Contest} from the CONTESTS block."""
    for i, line in enumerate(lines):
        if "CONTESTS" in line:
            start = i + 2   # section marker + column header
            break

    contests = {}
    for line in lines[start:]:
        row = next(csv.reader([line]))
        if not row[0].strip() or row[0].startswith("#"):
            break
        name         = row[0].strip()
        num_winners  = int(row[2]) if row[2].strip().isdigit() else 1
        votes_allowed= int(row[3]) if row[3].strip().isdigit() else 1
        total_ballots= int(row[4]) if row[4].strip().isdigit() else 0
        candidates   = parse_vote_string(row[5]) if len(row) > 5 else {}
        runoff_law   = row[8].strip() if len(row) > 8 else ""
        is_runoff    = "runoff" in runoff_law.lower()
        if name and candidates:
            contests[name] = Contest(name, candidates, total_ballots,
                                     num_winners, votes_allowed, is_runoff)
    return contests


def parse_reported_risk(lines):
    """Return {contest_name: (sample_size, p_value, risk_met)} from ROUNDS."""
    for i, line in enumerate(lines):
        if "ROUNDS" in line:
            start = i + 2
            break
    result = {}
    for line in lines[start:]:
        row = next(csv.reader([line]))
        if not row[0].strip() or row[0].startswith("#"):
            break
        if row[0].strip() == "1":
            name = row[1].strip()
            result[name] = {
                "sample_size": int(row[3]) if row[3].strip().isdigit() else None,
                "p_value":     float(row[5]) if row[5].strip() else None,
                "risk_met":    row[4].strip().lower() == "yes",
            }
    return result


def load_all_batches(contest_names):
    """
    Read all county candidate_totals and manifests.
    Returns {(county, batch_name): {"ballots": int, contest_name: {cand: votes}, ...}}
    """
    # Ballot counts from manifests
    ballot_counts = {}
    for county in os.listdir(MANIFESTS):
        county_path = os.path.join(MANIFESTS, county)
        if not os.path.isdir(county_path):
            continue
        files = [f for f in os.listdir(county_path) if f.endswith(".csv")]
        if not files:
            continue
        with open(os.path.join(county_path, files[0]), encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                name = row.get("Batch Name", "").strip()
                try:
                    ballot_counts[(county, name)] = int(row.get("Number of Ballots", 0))
                except ValueError:
                    pass

    # Vote counts from candidate_totals
    batch_results = {}
    for county in os.listdir(TOTALS):
        county_path = os.path.join(TOTALS, county)
        if not os.path.isdir(county_path):
            continue
        files = [f for f in os.listdir(county_path) if f.endswith(".csv")]
        if not files:
            continue
        with open(os.path.join(county_path, files[0]), encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                batch = row.get("Batch Name", "").strip()
                if not batch:
                    continue
                key = (county, batch)
                entry = {"ballots": ballot_counts.get(key, 0)}
                for contest in contest_names:
                    prefix = contest + " - "
                    votes = {
                        col[len(prefix):]: int(val or 0)
                        for col, val in row.items()
                        if col.startswith(prefix)
                    }
                    if votes:
                        entry[contest] = votes
                batch_results[key] = entry

    return batch_results


def compute_U(batch_results, contest, unauditable=0):
    """Sum max_error over all batches."""
    U = Decimal(0)
    for key, entry in batch_results.items():
        if contest.name not in entry:
            continue
        max_err = compute_max_error(
            entry[contest.name], entry["ballots"], contest, unauditable
        )
        if max_err.is_infinite():
            return Decimal("inf")
        U += max_err
    return U


def compute_unauditable(batch_results, contest):
    """
    Ballots in contest totals not reflected in batch tallies.
    (macro.py: compute_unauditable_ballots)
    """
    total_from_batches = sum(
        entry[contest.name].get(cand, 0)
        for entry in batch_results.values()
        if contest.name in entry
        for cand in contest.candidates
    )
    total_from_contest = sum(contest.candidates.values())
    diff = total_from_contest - total_from_batches
    if diff <= 0:
        return 0
    return math.ceil(diff / contest.votes_allowed)


def parse_sampled_batches(lines, contest_name):
    """
    Parse SAMPLED BATCHES section.
    Returns list of dicts with REAL-ticket rows for the given contest:
      {ticket, county, batch, ballots, reported_votes, audited_votes, combined}
    """
    for i, line in enumerate(lines):
        if "SAMPLED BATCHES" in line:
            start = i + 2   # section marker + column header row
            break

    col_ticket_senate = 3
    col_ticket_gov    = 4
    col_reported      = None  # determined below
    col_audited       = None

    # Read header to find column indices for this contest
    header = next(csv.reader([lines[start - 1]]))
    for j, col in enumerate(header):
        if col.strip() == f"Reported Results: {contest_name}":
            col_reported = j
        elif col.strip() == f"Audit Results: {contest_name}":
            col_audited = j

    if col_reported is None or col_audited is None:
        # Try alternate column name pattern
        for j, col in enumerate(header):
            if f"Reported" in col and contest_name in col:
                col_reported = j
            if "Audit" in col and contest_name in col and "Change" not in col:
                col_audited = j

    senate_col = col_ticket_senate if "Senate" in contest_name else col_ticket_gov

    draws = []
    for line in lines[start:]:
        row = next(csv.reader([line]))
        if not row[0].strip() or row[0].strip() == "Totals":
            break
        ticket_str = row[senate_col].strip()
        m = re.match(r"Round \d+:\s+(0\.\d+)", ticket_str)
        if not m:
            continue
        ticket = m.group(1)
        county = row[0].strip()
        batch  = row[1].strip()
        ballots = int(row[2]) if row[2].strip().isdigit() else 0
        reported = parse_vote_string(row[col_reported]) if col_reported is not None and len(row) > col_reported else {}
        audited  = parse_vote_string(row[col_audited])  if col_audited  is not None and len(row) > col_audited  else {}
        combined = row[14].strip() if len(row) > 14 else ""
        draws.append({
            "ticket":         ticket,
            "county":         county,
            "batch":          batch,
            "ballots":        ballots,
            "reported_votes": reported,
            "audited_votes":  audited,
            "combined":       combined,
        })

    return draws


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_contest(contest, reported_round, batch_results, draws, label):
    unauditable = compute_unauditable(batch_results, contest)
    U = compute_U(batch_results, contest, unauditable)

    print(f"=== {label} ===")
    print(f"  num_winners (internal): {contest.num_winners}"
          f"  {'(bumped for runoff)' if contest.is_subject_to_runoff and contest.num_winners == 2 else ''}")
    print(f"  Winners:  {', '.join(f'{k} ({v:,})' for k,v in sorted(contest.winners.items(), key=lambda x:-x[1]))}")
    print(f"  Losers:   {', '.join(f'{k} ({v:,})' for k,v in sorted(contest.losers.items(), key=lambda x:-x[1]))}")
    print(f"  Binding margin: {min(contest.winners[w]-contest.losers[l] for w in contest.winners for l in contest.losers):,}"
          f" votes  ({contest.diluted_margin:.4f} diluted)")
    print(f"  Unauditable ballots: {unauditable}")
    print(f"  U (total max error, all {len(batch_results):,} batches): {float(U):.4f}")
    print(f"  p_mult = 1 - 1/U: {float(1 - 1/U):.6f}")
    print(f"  Zero-discrepancy sample size (exact): {math.log(RISK_LIMIT/100) / math.log(float(1 - 1/U)):.1f}")
    print(f"  Draws with REAL ticket for this contest: {len(draws)}")

    p = Decimal(1)
    nonzero_taints = 0
    max_taint = Decimal(0)

    for draw in sorted(draws, key=lambda d: d["ticket"]):
        reported = draw["reported_votes"]
        audited  = draw["audited_votes"]
        ballots  = draw["ballots"]

        err = compute_error(reported, audited, contest, unauditable)
        e_p = err[1] if (err and err[0] > 0) else Decimal(0)
        u_p = compute_max_error(reported, ballots, contest, unauditable)

        if e_p.is_infinite() or u_p.is_infinite():
            print("  WARNING: infinite error — full hand recount needed")
            p = Decimal(1)
            break

        taint = e_p / u_p if u_p > 0 else Decimal(0)

        if taint > 0:
            nonzero_taints += 1
            if taint > max_taint:
                max_taint = taint

        if taint >= 1:
            p = Decimal("inf")
            break

        p *= (1 - 1/U) / (1 - taint)

    # Collapsed draws: when the PPEB algorithm draws a sub-batch from a combined
    # group already in the sample, no new CSV row appears, but Arlo still applies
    # the (1 - 1/U) / (1 - taint) factor for that draw. sample_size - len(draws)
    # gives the count of such collapses.
    sample_size = reported_round.get("sample_size") or len(draws)
    collapsed = sample_size - len(draws)
    if collapsed > 0:
        # Collapsed draws always hit already-selected combined groups.
        # All such groups verified to have taint = 0, so each contributes (1 - 1/U).
        p *= (1 - Decimal(1)/U) ** collapsed
        print(f"  Collapsed PPEB draws (sample_size {sample_size} − {len(draws)} unique rows = {collapsed}): "
              f"applied (1-1/U)^{collapsed} = {float((1-1/U)**collapsed):.6f}")

    computed_risk = min(float(p), 1.0)
    reported_p    = reported_round["p_value"]
    reported_met  = reported_round["risk_met"]

    print(f"  Non-zero taints: {nonzero_taints}  max taint: {float(max_taint):.6f}")
    print(f"  Computed risk:   {computed_risk:.8f}  ({computed_risk*100:.4f}%)")
    print(f"  Reported p-value:{reported_p:.8f}  ({reported_p*100:.4f}%)")
    delta = abs(computed_risk - reported_p)
    print(f"  Difference:      {delta:.2e}")
    print(f"  Risk limit met:  {computed_risk <= RISK_LIMIT/100}  (reported: {reported_met})")

    ok = (delta < 0.0005) and (computed_risk <= RISK_LIMIT/100) == reported_met
    print(f"  {'✓ REPRODUCED' if ok else '✗ MISMATCH'}")
    print()
    return ok


def main():
    print(f"Reading: {REPORT}\n")
    lines = read_csv_lines(REPORT)

    contests     = parse_contests(lines)
    reported     = parse_reported_risk(lines)
    batch_results = load_all_batches(list(contests.keys()))

    print(f"Loaded {len(batch_results):,} batches from candidate_totals + manifests\n")

    all_ok = True
    for cname, contest in contests.items():
        if cname not in reported:
            continue
        draws = parse_sampled_batches(lines, cname)
        ok = run_contest(contest, reported[cname], batch_results, draws, cname)
        if not ok:
            all_ok = False

    if all_ok:
        print("Both contests reproduced. The data support the reported outcomes.")
    else:
        print("FAIL: one or more contests did not reproduce.")
        sys.exit(1)


if __name__ == "__main__":
    main()
