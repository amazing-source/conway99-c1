"""c(l) = 1 cases split by a ZERO CUT at the root m, closed with FORCED kernel equalities (exploration, LAB 17/10/2026).
For a set C of rectangles at the root m = {v,2,3} with no edge of Gamma between Q_m(C) and the other labels of m
(cut_m(C) = 0), x = 1_{Q_m(C)} has x^t T x = cut = 0 (HtH = 7R, R = Laplacian of M_m), and T = 7 Pi_K >= 0 on the 84
labels, so T x = 0 EXACTLY: for every label r,  sum_{j in Q_m(C)} Gamma_rj = 3 x_r - (K x)_r   (linear in Gamma).
If some 3 x_r - (K x)_r is not a nonnegative integer, the sub-case is impossible by arithmetic alone.
Sub-cases: C contains the shared rectangle (0 1) (complements give the same vector up to the star vectors), C != all.
Model: case model of c1_cases.py (axioms, c(l) = 1, E3, 2-cut lemma, rectangle profile at l) + cut_m(C) = 0 + T x = 0.
usage: python c1_cm_split.py <case range a-b> <seconds per sub-case> [out.json]"""
import itertools
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

ROOTS_M = [(0, 1), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]
QM = [[C.IDX[frozenset((r, t))] for r in (2, 3) for t in rt] for rt in ROOTS_M]
ROOT_M_LABELS = sorted(set(i for q in QM for i in q))


def forced_rhs(Cset):
    x = np.zeros(C.n, dtype=np.int64)
    for k in Cset:
        x[QM[k]] = 1
    k8x = C.K8 @ x
    if np.any(k8x % 8):
        return None, x
    rhs = 3 * x - k8x // 8
    if np.any(rhs < 0):
        return None, x
    return rhs, x


def main():
    lo, hi = [int(t) for t in sys.argv[1].split("-")]
    secs = float(sys.argv[2])
    outf = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "unbiased_walks", "cm_split_status.json")
    status = json.load(open(outf)) if os.path.exists(outf) else {}
    subsets = [S for size in range(1, 6) for S in itertools.combinations(range(6), size) if 0 in S]
    cases = CS.all_cases()
    arith_dead = [S for S in subsets if forced_rhs(S)[0] is None]
    print("sub-cases per case: %d ; impossible by arithmetic alone (any case): %d %s" % (
        len(subsets), len(arith_dead), arith_dead), flush=True)
    for ci in range(lo, min(hi, len(cases))):
        case = cases[ci]
        tally = {}
        for S in subsets:
            key = "%d:%s|C=%s" % (ci, "".join(map(str, case)), "".join(map(str, S)))
            if key in status and status[key] in ("INFEASIBLE", "ARITH"):
                tally[status[key]] = tally.get(status[key], 0) + 1
                continue
            rhs, x = forced_rhs(S)
            if rhs is None:
                status[key] = "ARITH"
                tally["ARITH"] = tally.get("ARITH", 0) + 1
                continue
            m, e = CS.build(case, {}, random.Random(1), use_cuts=False)
            inside = set(i for k in S for i in QM[k])
            outside = set(ROOT_M_LABELS) - inside
            for i in inside:
                for j in outside:
                    m.Add(e[C.pid(i, j)] == 0)
            for r in range(C.n):
                lits = [e[C.pid(r, j)] for j in inside if j != r]
                m.Add(sum(lits) == int(rhs[r]))
            sv = cp_model.CpSolver()
            sv.parameters.num_search_workers = 2
            sv.parameters.max_time_in_seconds = secs
            st = sv.Solve(m)
            name = sv.StatusName(st)
            if name in ("OPTIMAL", "FEASIBLE"):
                name = "FEASIBLE"
            status[key] = name
            tally[name] = tally.get(name, 0) + 1
            json.dump(status, open(outf, "w"), indent=0)
        print("case %d %s: %s" % (ci, case, tally), flush=True)
    json.dump(status, open(outf, "w"), indent=0)


if __name__ == "__main__":
    main()
