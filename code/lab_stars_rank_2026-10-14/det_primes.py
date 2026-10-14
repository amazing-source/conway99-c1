"""Arithmetic of the three-star determinant (14/10/2026, after the user's 'why does the door close' remark).

J removes one label of each star outside the others ({0,4}, {1,4}, {2,4}), so det 8T[J,J] != 0 iff rank T_S = 31.
For random admissible structures (no positivity), compute the exact integer determinant (Bareiss) and its p-adic
valuations for small primes. If some prime p NEVER divides the determinant when c(l) = 1, that would point to a
mechanism forcing rank 31 (a mod-p proof of (A) without positivity). Random integers are divisible by p with
frequency 1/p.  usage: python det_primes.py <samples> <seed>
"""
import random
import sys
from collections import Counter, defaultdict

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval
from z5_enum import exact_rank


def bareiss_det(M):
    A = [row[:] for row in M]
    n = len(A)
    sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            p = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if p is None:
                return 0
            A[k], A[p] = A[p], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def vp(x, p):
    if x == 0:
        return None
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def main():
    samples, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    primes = [2, 3, 5, 7, 11, 13]
    stats = defaultdict(Counter)
    counts = Counter()
    for t in range(samples):
        S, idx, e, F = build([0, 1, 2], rng)
        n = len(S)
        sol = Solver(options={"polar": "rnd", "seed": str(rng.randrange(1, 10 ** 9))})
        for c in F.clauses:
            sol.add_clause(c)
        ok, model = sol.solve()
        G = np.zeros((n, n), dtype=int)
        for (i, j), v in e.items():
            if i < j and model[v]:
                G[i, j] = G[j, i] = 1
        M8 = [[int(round(8 * ((3 if i == j else 0) - G[i][j] - kval(S[i], S[j])))) for j in range(n)] for i in range(n)]
        X = [i for i in range(n) if 0 in S[i] or 1 in S[i]]
        c = 23 - exact_rank([[M8[i][j] for j in X] for i in X])
        rem = [idx[frozenset((0, 4))], idx[frozenset((1, 4))], idx[frozenset((2, 4))]]
        J = [i for i in range(n) if i not in rem]
        d = bareiss_det([[M8[i][j] for j in J] for i in J])
        key = "c=%d" % c
        counts[key] += 1
        if d == 0:
            stats[key]["det=0"] += 1
            continue
        for p in primes:
            stats[key][(p, vp(d, p))] += 1
    for key in sorted(counts):
        print("%s: %d samples, det = 0 in %d" % (key, counts[key], stats[key]["det=0"]))
        for p in primes:
            dist = sorted((v, k) for (pp, v), k in stats[key].items() if not isinstance(pp, str) and pp == p)
            nz = sum(k for v, k in dist if v and v > 0)
            tot = sum(k for v, k in dist)
            print("   p=%-2d  divides det in %d of %d (random: %.3f)  valuation distribution %s"
                  % (p, nz, tot, 1 / p, dict(dist)))


if __name__ == "__main__":
    main()
