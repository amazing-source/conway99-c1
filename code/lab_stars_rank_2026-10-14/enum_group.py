"""Exhaustive enumeration of the admissible four-star structures invariant under a group (LAB 15/10/2026).

Same SAT model as sym4g.py (C1, C1', C2 on the 44 labels of the stars 0,1,2,3; edge variables tied on pair orbits);
every solution is blocked on the orbit representatives, so the enumeration is complete when the solver says UNSAT.
For each structure: lambda_min of T and of U = 7 Pi_S - T on the complement of the star vectors (numerical), and for
the PSD ones the numerical nullity, c(l), c(m) (exact ranks of T_X), t(l), t(m), grid on (l,m).  Every PSD structure
of numerical nullity >= 14 is saved (cap 2000) for exact checks.
usage: python enum_group.py <generators as in sym4g.py> <out prefix> [max seconds]"""
import itertools
import json
import os
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from z5_enum import exact_rank
import random


def parse(cyc):
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    assert all(h[i ^ 1] == h[i] ^ 1 for i in range(14))
    return h


gens_s, out = sys.argv[1], sys.argv[2]
maxsec = float(sys.argv[3]) if len(sys.argv) > 3 else 270.0
gens = [parse(c) for c in gens_s.split("|")]
rng = random.Random(1)
S, idx, e, F = build([0, 1, 2, 3], rng)
n = len(S)
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
gl = [{i: idx[frozenset(h[y] for y in S[i])] for i in range(n)} for h in gens]
reps, seen = [], set()
for i, j in itertools.combinations(range(n), 2):
    orb, stack = {(i, j)}, [(i, j)]
    while stack:
        a, b = stack.pop()
        for m in gl:
            p = (min(m[a], m[b]), max(m[a], m[b]))
            if p not in orb:
                orb.add(p)
                stack.append(p)
    key = min(orb)
    if key in seen:
        continue
    seen.add(key)
    reps.append(key)
    for p in orb:
        if p != key:
            sol.add_clause([-e[key], e[p]])
            sol.add_clause([e[key], -e[p]])
print("pair orbits: %d" % len(reps), flush=True)
HP = [idx[frozenset({0: 1, 1: 0, 2: 3, 3: 2}.get(y, y) for y in s_)] for s_ in S]
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
Xl = [i for i in range(n) if S[i] & {0, 1}]
Xm = [i for i in range(n) if S[i] & {2, 3}]
trans_l = [(idx[frozenset((0, x))], idx[frozenset((1, x))]) for x in range(2, 14)]
trans_m = [(idx[frozenset((2, x))], idx[frozenset((3, x))]) for x in [0, 1] + list(range(4, 14))]
sqp = [(idx[frozenset((0, 2))], idx[frozenset((0, 3))]), (idx[frozenset((0, 2))], idx[frozenset((1, 2))]),
       (idx[frozenset((0, 3))], idx[frozenset((1, 3))]), (idx[frozenset((1, 2))], idx[frozenset((1, 3))])]
t0 = time.time()
count = npsd = 0
hist = {}
saved = []
complete = False
while time.time() - t0 < maxsec:
    ok, model = sol.solve()
    if not ok:
        complete = True
        break
    count += 1
    G = np.zeros((n, n), dtype=np.int64)
    for (i, j), v in e.items():
        if i < j and model[v]:
            G[i, j] = G[j, i] = 1
    sol.add_clause([-e[k] if model[e[k]] else e[k] for k in reps])
    M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    T = M8 / 8.0
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    if min(lt, lu) <= -1e-9:
        continue
    npsd += 1
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    cl = 23 - exact_rank([[int(M8[a][b]) for b in Xl] for a in Xl])
    cm = 23 - exact_rank([[int(M8[a][b]) for b in Xm] for a in Xm])
    tl = sum(1 for (a, b) in trans_l if G[a, b])
    tm = sum(1 for (a, b) in trans_m if G[a, b])
    grid = all(G[a, b] for a, b in sqp)
    # 15/10 morning: h-invariance (h = (0 1)(2 3)); every saved structure of nullity >= 14 so far is h-invariant
    hinv = bool((G[np.ix_(HP, HP)] == G).all())
    k = (nul, cl, cm, tl, tm, grid, hinv)
    if nul >= 14 and not hinv:
        print("HINV TARGET HIT: PSD structure of numerical nullity %d NOT invariant under h, c = (%d,%d)" % (nul, cl, cm),
              flush=True)
    hist[k] = hist.get(k, 0) + 1
    if nul >= 14 and len(saved) < 2000:
        saved.append({"c": [cl, cm], "t": [tl, tm], "grid": grid, "hinv": hinv, "nullity_numeric": nul, "lambda_T": lt, "lambda_U": lu,
                      "edges": [[a, b] for a in range(n) for b in range(a + 1, n) if G[a, b]]})
print("%s: %d invariant admissible structures enumerated (%s), %d with T, U PSD, %.0f s"
      % (gens_s, count, "COMPLETE" if complete else "stopped by time", npsd, time.time() - t0), flush=True)
print("PSD structures by (numerical nullity, c(l), c(m), t(l), t(m), grid, h-invariant):")
for k, v in sorted(hist.items(), reverse=True):
    print("  ", k, v)
json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "complete": complete, "count": count, "psd": npsd,
           "structures": saved}, open(out + "_enum.json", "w"))
