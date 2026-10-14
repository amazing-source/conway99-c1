"""Test of H3'' ("every three-star relation is carried by the two mate stars"), 14/10/2026.

Fix a two-mate-star base X = L_a u L_a' whose multigraph Q is connected (rank T_X = 22, so X carries no extra
relation). Then a rank-30 three-star structure on this base needs a relation with a nonzero part on the third star.
Search: draw the B-columns (pairs between the labels {b,x}, x outside the two lines, and the labels of X outside L_b)
from cryptominisat (random polarity), then enumerate EVERY admissible matching tau_b on L_b for these columns
(blocking clauses on the 66 pairs inside L_b); for each structure compute lambda_perp of T_S, U_S; on near-singular
PSD ones compute the exact rank. A PSD (T and U) rank-30 structure found here refutes H3''.
usage: python h3pp_inner.py <base.json> <column draws> <seed> <out prefix>
"""
import itertools
import json
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from z5_enum import exact_rank


def main():
    base, draws, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    stars = [0, 1, 2]
    rng = random.Random(seed)
    S, idx, e, F = build(stars, rng)
    n = len(S)
    b = json.load(open(base))
    bl = [frozenset(l) for l in b["labels"]]
    bG = b["gamma"]
    X = [i for i in range(n) if 0 in S[i] or 1 in S[i]]
    Xset = set(X)
    LB = [i for i in range(n) if 2 in S[i]]
    BE = [i for i in LB if i not in Xset]
    fixed = []
    for i in X:
        for j in X:
            if i < j:
                bi, bj = bl.index(S[i]), bl.index(S[j])
                v = e[(i, j)]
                fixed.append(v if bG[bi][bj] else -v)
    Ks = np.array([[kval(p, q) for q in S] for p in S])
    T_X = 3 * np.eye(len(X)) - np.array([[bG[bl.index(S[i])][bl.index(S[j])] for j in X] for i in X]) \
        - Ks[np.ix_(X, X)]
    r2 = exact_rank([[int(round(8 * T_X[p][q])) for q in range(len(X))] for p in range(len(X))])
    print("base two-mate-star rank %d (22 means Q connected)" % r2, flush=True)
    D = np.zeros((14, 84))
    for j, l in enumerate(LABELS):
        for y in l:
            D[y, j] = 1
    Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
    pos = {l: i for i, l in enumerate(LABELS)}
    ix = [pos[l] for l in S]
    PiS = Pi[np.ix_(ix, ix)]
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T

    def perp_min(M):
        ev, V = np.linalg.eigh(Pp @ M @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        return float(ev[keep].min())

    colvars = [e[(i, j)] for i in BE for j in X if j not in set(LB)]
    tauvars = [e[(i, j)] for i, j in itertools.combinations(LB, 2)]
    sol = Solver(options={"polar": "rnd", "seed": str(seed)})
    for c in F.clauses:
        sol.add_clause(c)
    t0 = time.time()
    total = psd = near = 0
    best = -9
    for d in range(draws):
        ok, model = sol.solve(fixed)
        if not ok:
            print("base does not extend", flush=True)
            return
        cols = [v if model[v] else -v for v in colvars]
        inner = Solver()
        for c in F.clauses:
            inner.add_clause(c)
        cnt = 0
        while True:
            ok2, m2 = inner.solve(fixed + cols)
            if not ok2:
                break
            cnt += 1
            total += 1
            G = np.zeros((n, n))
            for (i, j), v in e.items():
                if i < j and m2[v]:
                    G[i, j] = G[j, i] = 1
            T = 3 * np.eye(n) - G - Ks
            lt = perp_min(T)
            best = max(best, lt)
            if lt > -1e-9:
                psd += 1
                lu = perp_min(7 * PiS - T)
                if lu > -1e-9 and lt < 1e-6:
                    near += 1
                    r = exact_rank([[int(round(8 * T[i][j])) for j in range(n)] for i in range(n)])
                    if r <= 30:
                        json.dump({"labels": [sorted(l) for l in S],
                                   "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                  open(out + "_found.json", "w"))
                        print("RANK 30 ON A Q-CONNECTED BASE: H3'' is false (saved)", flush=True)
                        return
            inner.add_clause([-v if m2[v] else v for v in tauvars])
        sol.add_clause([-x for x in cols])
        if d % 10 == 0:
            print("draw %d: %d tau_b completions this draw; totals: %d structures, %d T-PSD, %d near-singular PSD,"
                  " best lambda_perp %.4f (%.0f s)" % (d, cnt, total, psd, near, best, time.time() - t0), flush=True)
    print("end: %d structures, %d T-PSD, %d near-singular, best %.4f" % (total, psd, near, best), flush=True)


if __name__ == "__main__":
    main()
