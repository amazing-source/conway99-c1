"""Norm budget of a two-mate-star base (14/10/2026; Codex's suggestion, message 725).

In a Conway graph, for the line l = {v,a,a'} with base X = L_a u L_a' (24 labels), the 60 other labels have residuals
(Schur complement of T after X) forming 7 x a projector of rank 7 + c(l): their residual norms 5/2 - c^T T_X^+ c sum to
49 + 7 c(l) (56 if l is non-special). Each other label {x,y} has exactly 2 neighbours in L_a and 2 in L_a' (mu with a
and a'), never two adjacent ones (lambda), so its column c is one of at most C(12,2)^2 profiles.
Upper bound: U_max = sum over the 60 labels of the best residual over its admissible profiles. If U_max < 49 + 7 c,
the base occurs in no Conway graph. This script computes U_max (and the per-label maxima) for random bases.
usage: python base_budget.py <samples> <seed>
"""
import itertools
import random
import sys

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS, count_needed
from z5_enum import exact_rank


def budget(S, G):
    n = len(S)
    T_X = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    Tp = np.linalg.pinv(T_X)
    M8 = [[int(round(8 * T_X[i][j])) for j in range(n)] for i in range(n)]
    c = 23 - exact_rank(M8)
    La = [i for i in range(n) if 0 in S[i]]
    Lap = [i for i in range(n) if 1 in S[i]]
    others = [l for l in LABELS if not (l & {0, 1})]
    best = []
    for u in others:
        k = np.array([kval(S[i], u) for i in range(n)])
        top = -1e9
        for p in itertools.combinations(La, 2):
            if G[p[0], p[1]]:
                continue
            for q in itertools.combinations(Lap, 2):
                if G[q[0], q[1]]:
                    continue
                nb = list(p) + list(q)
                # partial counts towards the letters of the base labels
                if any(sum(1 for i in nb if y in S[i]) > count_needed(u, y) for y in range(2, 14)):
                    continue
                cvec = -k.copy()
                cvec[nb] -= 1
                res = 2.5 - cvec @ Tp @ cvec
                top = max(top, res)
        best.append(top)
    return c, float(sum(best)), float(min(best)), float(max(best))


def main():
    samples, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    for t in range(samples):
        S, idx, e, F = build([0, 1], rng)
        n = len(S)
        sol = Solver(options={"polar": "rnd", "seed": str(rng.randrange(1, 10 ** 9))})
        for cl in F.clauses:
            sol.add_clause(cl)
        ok, model = sol.solve()
        G = np.zeros((n, n))
        for (i, j), v in e.items():
            if i < j and model[v]:
                G[i, j] = G[j, i] = 1
        c, U, lo, hi = budget(S, G)
        print("base %d: c(l) = %d, U_max = %.3f (needed %d), best residual per label in [%.3f, %.3f]"
              % (t, c, U, 49 + 7 * c, lo, hi), flush=True)


if __name__ == "__main__":
    main()
