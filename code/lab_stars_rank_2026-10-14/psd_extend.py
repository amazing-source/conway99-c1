"""Extend a fixed three-star structure to four stars and maximise lambda_perp(T_S) (14/10/2026).

The edges among the labels of the base structure (stars 0,1,2; JSON from psd_lns.py) are fixed by SAT assumptions;
only the pairs touching the new labels {3,x} (x >= 4) are searched, by large-neighbourhood moves (re-complete the new
pairs touching r random new labels) with greedy-plus-annealing acceptance. If the best score stays negative for many
bases, positive semidefiniteness at four stars looks impossible (evidence only, not a proof).
usage: python psd_extend.py <base.json> <moves> <r> <seed> <out prefix>
"""
import json
import math
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval


def main():
    base, moves, r, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    stars = [0, 1, 2, 3]
    rng = random.Random(seed)
    S, idx, e, F = build(stars, rng)
    n = len(S)
    b = json.load(open(base))
    bl = [frozenset(l) for l in b["labels"]]
    bG = b["gamma"]
    fixed = []
    for i, l1 in enumerate(bl):
        for j in range(i + 1, len(bl)):
            v = e[(idx[l1], idx[bl[j]])]
            fixed.append(v if bG[i][j] else -v)
    new = [idx[l] for l in S if l not in set(bl)]
    sol = Solver(options={"polar": "rnd", "seed": str(seed)})
    for c in F.clauses:
        sol.add_clause(c)
    Ks = np.array([[kval(a, c) for c in S] for a in S])
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]

    def score(model):
        G = np.zeros((n, n))
        for i, j in pairs:
            if model[e[(i, j)]]:
                G[i, j] = G[j, i] = 1
        ev, V = np.linalg.eigh(Pp @ (3 * np.eye(n) - G - Ks) @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        return float(ev[keep].min()), G

    ok, model = sol.solve(fixed)
    if not ok:
        print("the base does not extend to four stars at all (UNSAT)", flush=True)
        return
    cur, G = score(model)
    best = cur
    temp = 0.02
    t0 = time.time()
    newset = set(new)
    for mv in range(moves):
        R = set(rng.sample(new, r))
        assum = list(fixed)
        for i, j in pairs:
            if (i in newset or j in newset) and not (i in R or j in R):
                v = e[(i, j)]
                assum.append(v if model[v] else -v)
        ok2, m2 = sol.solve(assum)
        if not ok2:
            continue
        s2, G2 = score(m2)
        if s2 >= cur or rng.random() < math.exp((s2 - cur) / temp):
            model, cur = m2, s2
            if s2 > best:
                best = s2
                json.dump({"stars": stars, "labels": [sorted(l) for l in S], "gamma": G2.astype(int).tolist(),
                           "lambda_perp": best}, open(out + "_best.json", "w"))
                if best >= -1e-9:
                    print("move %d: PSD four-star structure found, lambda_perp %.6f" % (mv, best), flush=True)
                    return
        temp = max(0.001, temp * 0.9995)
        if mv % 200 == 0:
            print("move %d: current %.4f, best %.4f (%.0f s)" % (mv, cur, best, time.time() - t0), flush=True)
    print("end: best lambda_perp %.5f" % best, flush=True)


if __name__ == "__main__":
    main()
