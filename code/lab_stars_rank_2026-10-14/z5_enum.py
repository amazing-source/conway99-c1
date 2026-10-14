"""Exhaustive search of the Z5-invariant admissible structures on stars 0,1,2 (14/10/2026).

rho fixes the letters 0,1,2,3 and permutes the five other mate pairs cyclically (x -> x+2 on 4..11, 12 -> 4, 13 -> 5).
Invariant structures are far fewer; a symmetric structure can satisfy the exact rank condition "for a reason" (the
kernel splits into Fourier modes). All invariant admissible structures are enumerated with blocking clauses on one
representative per pair orbit; for each: PSD test, exact rank of T_S (rational elimination of 8 T_S).
usage: python z5_enum.py <max solutions> <out.json> [stars, default 0,1,2]
"""
import itertools
import json
import random
import sys
import time
from fractions import Fraction

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval

RHO = {i: i for i in range(4)}
for x in range(4, 14):
    RHO[x] = x + 2 if x < 12 else x - 8


def exact_rank(M):
    A = [[Fraction(v) for v in row] for row in M]
    n, r = len(A), 0
    for c in range(n):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r


def main():
    cap, out = int(sys.argv[1]), sys.argv[2]
    stars = [int(t) for t in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0, 1, 2]
    rng = random.Random(1)
    S, idx, e, F = build(stars, rng)
    n = len(S)
    rl = {i: idx[frozenset(RHO[y] for y in S[i])] for i in range(n)}
    sol = Solver()
    for c in F.clauses:
        sol.add_clause(c)
    reps = []
    seen = set()
    for i, j in itertools.combinations(range(n), 2):
        a, b = i, j
        orbit = []
        for _ in range(5):
            orbit.append((min(a, b), max(a, b)))
            a, b = rl[a], rl[b]
        key = min(orbit)
        if key in seen:
            continue
        seen.add(key)
        reps.append(key)
        for p in orbit[1:]:
            sol.add_clause([-e[key], e[p]])
            sol.add_clause([e[key], -e[p]])
    Ks = np.array([[kval(a, b) for b in S] for a in S])
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T
    t0 = time.time()
    count = psd = 0
    found = []
    ranks = {}
    best = -9
    while count < cap:
        ok, model = sol.solve()
        if not ok:
            print("enumeration complete", flush=True)
            break
        count += 1
        G = np.zeros((n, n))
        for (i, j), v in e.items():
            if i < j and model[v]:
                G[i, j] = G[j, i] = 1
        T = 3 * np.eye(n) - G - Ks
        ev, V = np.linalg.eigh(Pp @ T @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        lam = float(ev[keep].min())
        best = max(best, lam)
        if lam > -1e-9:
            psd += 1
            rk = exact_rank([[int(round(8 * T[i][j])) for j in range(n)] for i in range(n)])
            ranks[rk] = ranks.get(rk, 0) + 1
            r = rk
            if r <= 30 and len(found) < 50:
                found.append({"labels": [sorted(l) for l in S], "gamma": G.astype(int).tolist(), "rank": r,
                              "eigenvalues": np.linalg.eigvalsh(T).tolist()})
                json.dump(found, open(out, "w"))
                print("solution %d: PSD with exact rank %d -> saved" % (count, r), flush=True)
            elif r <= 30:
                found_more = True
        sol.add_clause([-e[p] if model[e[p]] else e[p] for p in reps])
        if count % 500 == 0:
            print("%d invariant structures, %d PSD (exact ranks of the PSD ones: %s), best lambda_perp %.4f (%.0f s)"
                  % (count, psd, dict(sorted(ranks.items())), best, time.time() - t0), flush=True)
    print("total %d invariant structures, %d PSD (exact ranks: %s), best lambda_perp %.5f (%.0f s)"
          % (count, psd, dict(sorted(ranks.items())), best, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
