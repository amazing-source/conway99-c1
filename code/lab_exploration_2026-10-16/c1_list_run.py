"""Run the WHOLE c = 1 case list with the strongest exact model (exploration, LAB 17/10/2026), Codex's way: every case
gets the same model and the same short time; some die, the survivors are attacked next.
Model per case (all constraints valid in a Conway graph):
  case model of c1_cases.py: local axioms, c(l) = 1, E3 at both roots, 2-cut lemma at both roots, rectangle profile at l;
  FORCED KERNEL at the root m (reified, no case split): for every set C of root-m rectangles containing the shared one,
    b_C <=> cut_m(C) = 0, and b_C => T_S x_C = 0 exactly (x_C = 1_{Q_m(C)}, x^t T x = cut_m(C), T = 7 Pi_K >= 0):
    for every label r, sum_{j in Q_m(C)} Gamma_rj = 3 (x_C)_r - (K x_C)_r  (b_C forced false if this is not integral >= 0);
  optional MODE=cm2: at least one b_C (c(m) >= 2), to test the part of each case where m has a zero cut;
  optional pool of positivity cuts (POOL=file), hard constraints.
usage: python c1_list_run.py <case range a-b> <seconds> <status.json>"""
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
ROOT_M = sorted(set(i for q in QM for i in q))
SUBSETS = [S for size in range(1, 6) for S in itertools.combinations(range(6), size) if 0 in S]


def forced(Sset):
    x = np.zeros(C.n, dtype=np.int64)
    for k in Sset:
        x[QM[k]] = 1
    k8x = C.K8 @ x
    if np.any(k8x % 8):
        return None
    rhs = 3 * x - k8x // 8
    return None if np.any(rhs < 0) else rhs


def add_forced_kernel(m, e, mode):
    bs = []
    for S in SUBSETS:
        inside = set(i for k in S for i in QM[k])
        outside = [j for j in ROOT_M if j not in inside]
        cross = [e[C.pid(i, j)] for i in inside for j in outside]
        b = m.NewBoolVar("")
        m.Add(sum(cross) == 0).OnlyEnforceIf(b)
        m.Add(sum(cross) >= 1).OnlyEnforceIf(b.Not())
        rhs = forced(S)
        if rhs is None:
            m.Add(b == 0)
        else:
            for r in range(C.n):
                lits = [e[C.pid(r, j)] for j in inside if j != r]
                m.Add(sum(lits) == int(rhs[r])).OnlyEnforceIf(b)
        bs.append(b)
    if mode == "cm2":
        m.AddBoolOr(bs)
    return bs


def main():
    lo, hi = [int(t) for t in sys.argv[1].split("-")]
    secs = float(sys.argv[2])
    statf = sys.argv[3]
    mode = os.environ.get("MODE", "all")
    poolf = os.environ.get("POOL")
    pool = json.load(open(poolf)) if poolf else {}
    status = json.load(open(statf)) if os.path.exists(statf) else {}
    cases = CS.all_cases()
    for ci in range(lo, min(hi, len(cases))):
        case = cases[ci]
        key = "%d:%s" % (ci, "".join(map(str, case)))
        if status.get(key, {}).get("status") == "INFEASIBLE":
            continue
        t0 = time.time()
        m, e = CS.build(case, pool, random.Random(1), use_cuts=bool(poolf))
        add_forced_kernel(m, e, mode)
        sv = cp_model.CpSolver()
        sv.parameters.num_search_workers = 2
        sv.parameters.max_time_in_seconds = secs
        st = sv.Solve(m)
        name = sv.StatusName(st)
        res = {"status": "INFEASIBLE" if name == "INFEASIBLE" else ("FEASIBLE" if name in ("OPTIMAL", "FEASIBLE") else "UNKNOWN"),
               "mode": mode, "seconds": round(time.time() - t0, 1)}
        if res["status"] == "FEASIBLE":
            G = np.zeros((C.n, C.n), dtype=np.int64)
            for k, (i, j) in enumerate(C.PAIRS):
                if sv.Value(e[k]):
                    G[i, j] = G[j, i] = 1
            T8 = 24 * np.eye(C.n, dtype=np.int64) - 8 * G - C.K8
            res["lambda_min"] = round(float(C.perp_eigs(T8 / 8.0)[0].min()), 3)
        status[key] = res
        json.dump(status, open(statf, "w"), indent=0)
        print("case %s: %s" % (key, res), flush=True)
    tally = {}
    for v in status.values():
        tally[v["status"]] = tally.get(v["status"], 0) + 1
    print("TALLY (%s): %s" % (mode, tally), flush=True)


if __name__ == "__main__":
    main()
