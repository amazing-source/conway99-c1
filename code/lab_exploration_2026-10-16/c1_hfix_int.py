"""Integral completions of fixed root graphs (exploration, LAB 17/10/2026).
c1_hfix_lp.py shows that fixed (H_l, H_m) from the case model admit FRACTIONAL positive completions on P x Q.  Here the
P x Q pairs stay binary: the full case model (c1_cases.build: axioms, c(l) = 1, E3, 2-cut lemma, case) with all pairs
inside the roots fixed to an integral start, and the positivity cut loop on the 400 P x Q pairs only.
  INFEASIBLE  => no positive integral completion of this (H_l, H_m);
  positive    => a positive E3-free c = 1 block: tested against the norm-14 lattice (RL) and balanced 2-cuts (C2b);
                 if neither applies it is a counterexample to (SV1) as encoded (saved).
usage: python c1_hfix_int.py <case index> <start seed> <seconds> [CP-SAT seconds for the start]"""
import json
import os
import random
import sys
import time

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c1_sv1_cuts as C  # noqa: E402
import c1_cases as CS  # noqa: E402
from c1_hfix_lp import integral_start, FIXED, lam8  # noqa: E402


def main():
    ci, seed, secs = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    s0 = float(sys.argv[4]) if len(sys.argv) > 4 else 20.0
    case = CS.all_cases()[ci]
    g0 = integral_start(ci, s0, seed)
    if g0 is None:
        print("no integral start")
        return
    rng = random.Random(seed)
    pool = {"PV": [], "R": [], "B2": []}
    t0 = time.time()
    rounds = 0
    while time.time() - t0 < secs:
        rounds += 1
        m, e = CS.build(case, pool, rng, use_cuts=True)
        for k in FIXED:
            m.Add(e[k] == int(g0[k]))
        sv = cp_model.CpSolver()
        sv.parameters.num_search_workers = 2
        sv.parameters.max_time_in_seconds = max(5.0, secs - (time.time() - t0))
        sv.parameters.random_seed = rng.randint(0, 10 ** 6)
        st = sv.Solve(m)
        if st == cp_model.INFEASIBLE:
            print("round %d: INFEASIBLE: no positive integral completion of this (H_l, H_m) (%.0f s, %d vectors)" % (
                rounds, time.time() - t0, len(pool["PV"])), flush=True)
            return
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("round %d: %s (%.0f s)" % (rounds, sv.StatusName(st), time.time() - t0), flush=True)
            return
        g = np.array([sv.Value(x) for x in e], dtype=np.int64)
        G = np.zeros((C.n, C.n), dtype=np.int64)
        for k, (i, j) in enumerate(C.PAIRS):
            if g[k]:
                G[i, j] = G[j, i] = 1
        _, _, eT, _, eU, _ = lam8(g)
        lm = 8 * min(eT.min(), eU.min())
        pc = C.psd_cuts(G, maxcuts=8)
        if pc:
            for coeffs, rhs, (typ, xv) in pc:
                pool["PV"].append([typ, list(xv)])
            if rounds % 5 == 1:
                print("round %d: 8 lambda_min %.3f, +%d cuts (%.0f s)" % (rounds, lm, len(pc), time.time() - t0), flush=True)
            continue
        nu = int(np.sum(np.abs(np.linalg.eigvalsh((24 * np.eye(C.n) - 8 * G - C.K8) / 8.0)) < 1e-7))
        c = C.rl_violation(G)
        b = C.b2_cut(G) if c is None else None
        verdict = "killed by RL" if c is not None else ("killed by C2b" if b is not None else "NOT KILLED: (SV1) counterexample")
        fn = os.path.join(HERE, "unbiased_walks", "hfix_pos_case%d_seed%d.json" % (ci, seed))
        json.dump({"labels": [sorted(l) for l in C.S], "case": case, "nu": nu, "verdict": verdict,
                   "edges": [[i, j] for i, j in C.PAIRS if G[i, j]]}, open(fn, "w"))
        print("round %d: POSITIVE integral completion, 8 lambda_min %.3f, nu(T_S) = %d ; %s ; saved %s (%.0f s)" % (
            rounds, lm, nu, verdict, fn, time.time() - t0), flush=True)
        return
    print("time out after %d rounds (%d vectors)" % (rounds, len(pool["PV"])), flush=True)


if __name__ == "__main__":
    main()
