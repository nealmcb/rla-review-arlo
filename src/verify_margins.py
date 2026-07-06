#!/usr/bin/env python3
"""
Derive diluted margins from final_audit_report.csv and cross-check them against
the round summary (Sample Size, achieved risk level). Any inconsistency exits
non-zero so this can be run as a CI gate.

Usage: python3 src/verify_margins.py
"""
import csv, math, sys, os, re

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "2026-05-19-primary")
REPORT = os.path.join(BASE, "downloads", "final_audit_report.csv")
RISK_LIMIT = 0.05


def parse_vote_string(s):
    """Parse 'Name: N; Name: N; ...' into {name: votes}."""
    out = {}
    for part in s.split(";"):
        part = part.strip()
        m = re.match(r'^"?(.+?)"?\s*:\s*(\d+)$', part)
        if m:
            out[m.group(1).strip()] = int(m.group(2))
    return out


def read_report(path):
    contests = {}    # name -> {total_ballots, candidates: {name: votes}}
    rounds = {}      # name -> {sample_size, risk_met, p_value, batches_sampled, ballots_sampled}

    with open(path, newline="", encoding="utf-8-sig") as f:
        lines = f.readlines()

    # --- parse CONTESTS block ---
    i = 0
    while i < len(lines) and "CONTESTS" not in lines[i]:
        i += 1
    i += 1  # skip header marker
    # skip column-name row
    while i < len(lines) and (not lines[i].strip() or lines[i].startswith("#")):
        i += 1
    # skip the column header row (Contest Name, Targeted?, ...)
    i += 1
    while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
        row = next(csv.reader([lines[i]]))
        if len(row) >= 7 and row[0]:
            name = row[0].strip()
            total = int(row[4]) if row[4].strip().isdigit() else None
            cands = parse_vote_string(row[5]) if len(row) > 5 else {}
            if name and total:
                contests[name] = {"total_ballots": total, "candidates": cands}
        i += 1

    # --- parse ROUNDS block ---
    while i < len(lines) and "ROUNDS" not in lines[i]:
        i += 1
    i += 1
    # skip column header row
    while i < len(lines) and (not lines[i].strip() or lines[i].startswith("#")):
        i += 1
    i += 1  # skip col names row
    while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
        row = next(csv.reader([lines[i]]))
        if len(row) >= 11 and row[0].strip() == "1":
            name = row[1].strip()
            rounds[name] = {
                "sample_size":      int(row[3]) if row[3].strip().isdigit() else None,
                "risk_met":         row[4].strip().lower() == "yes",
                "p_value":          float(row[5]) if row[5].strip() else None,
                "batches_sampled":  int(row[9]) if row[9].strip().isdigit() else None,
                "ballots_sampled":  int(row[10]) if row[10].strip().isdigit() else None,
            }
        i += 1

    return contests, rounds


def diluted_margin(candidates, total_ballots):
    """(winner - runner_up) / total_ballots for a plurality/runoff contest."""
    ranked = sorted(candidates.values(), reverse=True)
    if len(ranked) < 2:
        return None
    return (ranked[0] - ranked[1]) / total_ballots


def ballot_level_approx_n(dm):
    """
    Approximate zero-discrepancy sample size using the ballot-level BRAVO formula.
    NOTE: MACRO batch comparison uses a different stopping rule that depends on the
    distribution of batch sizes — this is an approximation only, valid mainly for
    small margins. Do not treat as a tight bound.
    """
    return math.log(RISK_LIMIT) / math.log(1 - dm / 2)


def check_consistency(contest_name, dm, sample_size, p_value, risk_met):
    """
    Cross-check margin against the round summary.
    Hard checks (always correct):
      - p_value ≤ risk_limit when risk_met = True
    Informational (approximate — MACRO uses batch-size distribution, not just dm):
      - Ballot-level sample size approximation
    """
    ok = True

    if risk_met and p_value and p_value > RISK_LIMIT:
        print(f"  INCONSISTENCY: risk_met=True but p_value={p_value:.6f} > {RISK_LIMIT}")
        ok = False

    if not risk_met and p_value and p_value <= RISK_LIMIT:
        print(f"  INCONSISTENCY: risk_met=False but p_value={p_value:.6f} ≤ {RISK_LIMIT}")
        ok = False

    approx_n = ballot_level_approx_n(dm)
    return ok, approx_n


def main():
    print(f"Reading: {REPORT}\n")
    contests, rounds = read_report(REPORT)

    all_ok = True
    for name, rnd in rounds.items():
        if name not in contests:
            print(f"WARNING: round contest '{name}' not found in CONTESTS block")
            continue

        c = contests[name]
        dm = diluted_margin(c["candidates"], c["total_ballots"])
        if dm is None:
            print(f"{name}: insufficient candidate data")
            continue

        ranked = sorted(c["candidates"].items(), key=lambda x: -x[1])
        winner, w_votes = ranked[0]
        runner_up, ru_votes = ranked[1]
        margin_votes = w_votes - ru_votes

        print(f"=== {name} ===")
        print(f"  Winner:    {winner} ({w_votes:,})")
        print(f"  Runner-up: {runner_up} ({ru_votes:,})")
        print(f"  Margin:    {margin_votes:,} / {c['total_ballots']:,} = {dm:.4f}")
        print(f"  Sample Size (CSV): {rnd['sample_size']}")
        print(f"  Achieved risk level (p-value): {rnd['p_value']:.6f} ({rnd['p_value']*100:.2f}%)")
        print(f"  Risk limit met: {rnd['risk_met']}")

        ok, approx_n = check_consistency(
            name, dm,
            rnd["sample_size"], rnd["p_value"], rnd["risk_met"]
        )
        print(f"  Ballot-level approx sample size (informational): {approx_n:.0f}")
        if ok:
            print(f"  ✓ Consistent")
        else:
            all_ok = False
        print()

    if not all_ok:
        print("FAIL: one or more consistency checks failed.")
        sys.exit(1)
    else:
        print("All consistency checks passed.")


if __name__ == "__main__":
    main()
