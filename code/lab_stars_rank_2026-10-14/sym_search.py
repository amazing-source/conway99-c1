"""Test of hypothesis H3 (rank 30 at three stars forces the grid) inside symmetric families (14/10/2026).

A letter permutation rho (fixing 0,1,2,3, preserving mates) acts on the admissible structures of stars 0,1,2;
invariant structures are sampled with cryptominisat (random polarity) under equality clauses on pair orbits, then
improved by large-neighbourhood moves inside the invariant space towards T_S >= 0 and U_S = 7 Pi_S - T_S >= 0.
Every structure with both PSD is checked for the exact rank of T_S and for the grid square on the four cross labels.
A PSD pair with rank 30 and NO grid refutes H3.
rho is given as a cycle string, e.g. "4,6,8;5,7,9" (Z3 on three mate pairs, the two other pairs fixed).
usage: python sym_search.py <cycles> <moves> <seed> <out prefix>
"""
import itertools
import json
import math
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from z5_enum import exact_rank


def main():
    cyc, moves, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rho = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            rho[c[k]] = c[(k + 1) % len(c)]
    assert all(rho[i ^ 1] == rho[i] ^ 1 for i in range(14)), "rho must preserve mates"
    stars = [0, 1, 2]
    rng = random.Random(seed)
    S, idx, e, F = build(stars, rng)
    n = len(S)
    rl = {i: idx[frozenset(rho[y] for y in S[i])] for i in range(n)}
    sol = Solver(options={"polar": "rnd", "seed": str(seed)})
    for c in F.clauses:
        sol.add_clause(c)
    reps, orbit_of = [], {}
    seen = set()
    for i, j in itertools.combinations(range(n), 2):
        a, b = i, j
        orb = []
        while True:
            p = (min(a, b), max(a, b))
            if p in orb:
                break
            orb.append(p)
            a, b = rl[a], rl[b]
        key = min(orb)
        if key in seen:
            continue
        seen.add(key)
        reps.append(key)
        for p in orb:
            orbit_of[p] = key
            if p != key:
                sol.add_clause([-e[key], e[p]])
                sol.add_clause([e[key], -e[p]])
    D = np.zeros((14, 84))
    for j, l in enumerate(LABELS):
        for y in l:
            D[y, j] = 1
    Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
    pos = {l: i for i, l in enumerate(LABELS)}
    ix = [pos[l] for l in S]
    PiS = Pi[np.ix_(ix, ix)]
    Ks = np.array([[kval(a, b) for b in S] for a in S])
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T
    X = [idx[frozenset(p)] for p in [(0, 2), (0, 3), (1, 2), (1, 3)]]

    def perp_min(M):
        ev, V = np.linalg.eigh(Pp @ M @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        return float(ev[keep].min())

    def evaluate(model):
        G = np.zeros((n, n))
        for (i, j), v in e.items():
            if i < j and model[v]:
                G[i, j] = G[j, i] = 1
        T = 3 * np.eye(n) - G - Ks
        return min(perp_min(T), perp_min(7 * PiS - T)), G, T

    ok, model = sol.solve()
    if not ok:
        print("no invariant admissible structure", flush=True)
        return
    cur, G, T = evaluate(model)
    best = cur
    temp = 0.05
    found = []
    checked = set()
    t0 = time.time()
    for mv in range(moves):
        Rlab = set(rng.sample(range(n), 4))
        assum = []
        for key in reps:
            i, j = key
            if i in Rlab or j in Rlab or rl[i] in Rlab or rl[j] in Rlab:
                continue
            v = e[key]
            assum.append(v if model[v] else -v)
        ok2, m2 = sol.solve(assum)
        if not ok2:
            continue
        s2, G2, T2 = evaluate(m2)
        if s2 > -1e-9:
            sig = tuple(int(m2[e[k]]) for k in reps)
            if sig not in checked:
                checked.add(sig)
                r = exact_rank([[int(round(8 * T2[i][j])) for j in range(n)] for i in range(n)])
                grid = bool(G2[X[0], X[1]] and G2[X[0], X[2]] and G2[X[1], X[3]] and G2[X[2], X[3]])
                two = [i for i in range(n) if 0 in S[i] or 1 in S[i]]
                r2 = exact_rank([[int(round(8 * T2[i][j])) for j in two] for i in two])
                print("move %d: T and U PSD, exact rank %d, grid %s, two-mate-star rank %d" % (mv, r, grid, r2),
                      flush=True)
                if r <= 30 and r2 == 22:
                    found.append({"rank": r, "grid": grid, "two_star_rank": r2,
                                  "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G2[i, j]]})
                    json.dump({"labels": [sorted(l) for l in S], "rho": cyc, "found": found}, open(out + ".json", "w"))
                    print("RANK 30 WITH Q CONNECTED (relation uses the third star): H3'' is false", flush=True)
                    return
                if r <= 30:
                    found.append({"rank": r, "grid": grid,
                                  "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G2[i, j]]})
                    json.dump({"labels": [sorted(l) for l in S], "rho": cyc, "found": found}, open(out + ".json", "w"))
                    if not grid:
                        print("non-grid rank-30 structure (relation carried by the two mate stars)", flush=True)
        if s2 >= cur or rng.random() < math.exp((s2 - cur) / temp):
            model, cur = m2, s2
            best = max(best, cur)
        temp = max(0.002, temp * 0.9995)
        if mv % 500 == 0:
            print("move %d: current %.4f best %.4f, PSD pairs checked %d, rank-30 found %d (%.0f s)"
                  % (mv, cur, best, len(checked), len(found), time.time() - t0), flush=True)
    print("end: best %.4f, PSD pairs %d, rank-30 %d (grid %d)" % (best, len(checked), len(found),
                                                                  sum(1 for f in found if f["grid"])), flush=True)


if __name__ == "__main__":
    main()
