"""2-adic Smith profile of the reduced matrix 8 T_S[J,J] (three stars), 14/10/2026.

J removes one label of each star outside the others ({0,4}, {1,4}, {2,4}), so det 8T[J,J] != 0 iff rank T_S = 31.
Elimination over Q with pivots of minimal 2-adic valuation gives the 2-adic invariant factors (valuations listed in
increasing order; 'inf' = zero invariant factor). Compared with c(l) (components of Codex's Q) and positivity.
usage: python smith2.py <samples> <seed> [json files of structures ...]
"""
import json
import random
import sys
from fractions import Fraction

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval
from z5_enum import exact_rank


def v2(x):
    if x == 0:
        return None
    x = Fraction(x)
    n, d = x.numerator, x.denominator
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    while d % 2 == 0:
        d //= 2
        v -= 1
    return v


def smith2(M):
    A = [[Fraction(x) for x in row] for row in M]
    n = len(A)
    rows, cols = list(range(n)), list(range(n))
    vals = []
    active_r, active_c = set(range(n)), set(range(n))
    while active_r:
        best = None
        for i in active_r:
            for j in active_c:
                if A[i][j] != 0:
                    vv = v2(A[i][j])
                    if best is None or vv < best[0]:
                        best = (vv, i, j)
        if best is None:
            vals += ["inf"] * len(active_r)
            break
        vv, i, j = best
        vals.append(vv)
        p = A[i][j]
        for r in list(active_r):
            if r != i and A[r][j] != 0:
                f = A[r][j] / p
                A[r] = [a - f * b for a, b in zip(A[r], A[i])]
        active_r.remove(i)
        active_c.remove(j)
    return vals


def analyse(S, G):
    n = len(S)
    T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    M8 = [[int(round(8 * T[i][j])) for j in range(n)] for i in range(n)]
    X = [i for i in range(n) if 0 in S[i] or 1 in S[i]]
    c = 23 - exact_rank([[M8[i][j] for j in X] for i in X])
    idx = {l: i for i, l in enumerate(S)}
    rem = [idx[frozenset((0, 4))], idx[frozenset((1, 4))], idx[frozenset((2, 4))]]
    J = [i for i in range(n) if i not in rem]
    vals = smith2([[M8[i][j] for j in J] for i in J])
    psd = bool(np.linalg.eigvalsh(T).min() > -1e-9)
    from collections import Counter
    prof = Counter(vals)
    return c, psd, dict(sorted(prof.items(), key=lambda kv: (kv[0] == "inf", kv[0] if kv[0] != "inf" else 99)))


def main():
    samples, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    for t in range(samples):
        S, idx, e, F = build([0, 1, 2], rng)
        n = len(S)
        sol = Solver(options={"polar": "rnd", "seed": str(rng.randrange(1, 10 ** 9))})
        for c in F.clauses:
            sol.add_clause(c)
        ok, model = sol.solve()
        G = np.zeros((n, n))
        for (i, j), v in e.items():
            if i < j and model[v]:
                G[i, j] = G[j, i] = 1
        c, psd, prof = analyse(S, G)
        print("random  c=%d psd=%s  2-adic profile {valuation: count} %s" % (c, psd, prof), flush=True)
    for f in sys.argv[3:]:
        d = json.load(open(f))
        S = [frozenset(l) for l in d["labels"]]
        n = len(S)
        if "gamma" in d:
            G = np.array(d["gamma"], dtype=float)
        else:
            G = np.zeros((n, n))
            ed = d["found"][0]["edges"] if "found" in d else d["valid_edges"][0]
            for i, j in ed:
                G[i, j] = G[j, i] = 1
        c, psd, prof = analyse(S, G)
        print("%-24s c=%d psd=%s  2-adic profile %s" % (f, c, psd, prof), flush=True)


if __name__ == "__main__":
    main()
