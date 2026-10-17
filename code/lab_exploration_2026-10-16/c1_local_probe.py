"""How local is the failure of positivity? (exploration, LAB 17/10/2026)
For integral c = 1 structures of the case model (with the current cut pool as hard constraints), find small label sets W
whose principal submatrix T_W or U_W is already not PSD (principal submatrices of T = 7 Pi_K and of 7 Pi - T are PSD
in a Conway graph, so each such W is an exact local obstruction).  Greedy: labels sorted by |x_i| for the most negative
direction, then pruning (remove a label if the rest stays non-PSD).  Reports the minimal sizes found.
usage: python c1_local_probe.py <pool.json> <case index> <solutions> [seconds per solve]"""
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


def mats(G):
    T = (24 * np.eye(C.n) - 8 * G - C.K8) / 8.0
    return T, 7 * C.PiS - T


def min_sub(M, x):
    """greedy + pruning: a small index set W with lambda_min(M_W) < 0."""
    order = list(np.argsort(-np.abs(x)))
    W = None
    for k in range(2, C.n + 1):
        Wk = order[:k]
        if np.linalg.eigvalsh(M[np.ix_(Wk, Wk)])[0] < -1e-9:
            W = list(Wk)
            break
    if W is None:
        return None
    changed = True
    while changed:
        changed = False
        for w in list(W):
            W2 = [u for u in W if u != w]
            if len(W2) >= 2 and np.linalg.eigvalsh(M[np.ix_(W2, W2)])[0] < -1e-9:
                W = W2
                changed = True
    return W


def main():
    poolf, ci, nsol = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    secs = float(sys.argv[4]) if len(sys.argv) > 4 else 40.0
    pool = json.load(open(poolf)) if os.path.exists(poolf) else {"PV": [], "R": [], "B2": []}
    case = CS.all_cases()[ci]
    rng = random.Random(7)
    for s in range(nsol):
        m, e = CS.build(case, pool, rng, use_cuts=True)
        sv = cp_model.CpSolver()
        sv.parameters.num_search_workers = 2
        sv.parameters.max_time_in_seconds = secs
        sv.parameters.random_seed = 100 + s
        st = sv.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("solve %d: %s" % (s, sv.StatusName(st)))
            continue
        G = np.zeros((C.n, C.n), dtype=np.int64)
        for k, (i, j) in enumerate(C.PAIRS):
            if sv.Value(e[k]):
                G[i, j] = G[j, i] = 1
        T, U = mats(G)
        out = []
        for typ, M in (("T", T), ("U", U)):
            ev, V = C.perp_eigs(M)
            for idx in np.argsort(ev)[:3]:
                if ev[idx] > -1e-9:
                    break
                W = min_sub(M, V[:, idx])
                if W is None:
                    out.append("%s %.3f: no small W" % (typ, ev[idx]))
                    continue
                labs = ["".join("%x" % t for t in sorted(C.S[w])) for w in W]
                ne = sum(G[a, b] for a in W for b in W) // 2
                out.append("%s %.3f: |W| %d (%d edges) %s" % (typ, ev[idx], len(W), ne, " ".join(labs)))
        print("solve %d:" % s)
        for o in out:
            print("   ", o)
        # add the cuts so that the next solve differs
        for coeffs, rhs, (typ, xv) in C.psd_cuts(G, maxcuts=8):
            pool["PV"].append([typ, list(xv)])


if __name__ == "__main__":
    main()
