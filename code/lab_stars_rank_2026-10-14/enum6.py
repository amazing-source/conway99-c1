"""Exhaustive enumeration of admissible k-line structures invariant under a group (LAB 16/10/2026).

Generalises enum_group.py from four stars (two lines) to any union of lines through v, e.g. six stars = three lines
(60 labels).  Same SAT model (stars_rank.build: C1, C1', C2), edge variables tied on pair orbits, every solution
blocked on the orbit representatives, so the run is complete when the solver says UNSAT.
In a Conway graph the block on these labels has T >= 0, U = 7 Pi_S - T >= 0 and rank T <= 30, i.e. numerical nullity
>= |S| - 30 (30 for six stars).  For each structure: lambda_min of T and of U on the complement of the star vectors;
for the PSD ones the numerical nullity; every PSD structure with nullity >= |S| - 30 is saved, with its exact rank.
usage: python enum6.py <stars, e.g. 0,1,2,3,4,5> <generators as in sym4g.py, or 'none'> <out prefix> [max seconds]"""
import itertools
import json
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from z5_enum import exact_rank


def parse(cyc):
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    assert all(h[i ^ 1] == h[i] ^ 1 for i in range(14)), "generator must respect mates"
    return h


stars = [int(t) for t in sys.argv[1].split(",")]
gens_s, out = sys.argv[2], sys.argv[3]
maxsec = float(sys.argv[4]) if len(sys.argv) > 4 else 270.0
gens = [] if gens_s == "none" else [parse(c) for c in gens_s.split("|")]
for h in gens:
    assert set(h[y] for y in stars) == set(stars), "generator must preserve the star letters"
rng = random.Random(1)
S, idx, e, F = build(stars, rng)
n = len(S)
target = n - 30
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
# HREL (env, e.g. "0-2,0-4,2-4"): impose the (H-MATCH) matching relations at the given pairs of star lines, given by
# one letter of each line.  For lines P = {p, p^1}, Q = {q, q^1}: M_{p^1} = s(Q) M_p and M_{q^1} = s(P) M_q, where M_a
# is the matching induced on the labels {a, y} and s(Q) swaps the two letters of Q.  Matchings only, no invariance.
import os
hrel = [tuple(int(t) for t in pq.split("-")) for pq in os.environ.get("HREL", "").split(",") if pq]
nties = 0
for p, q in hrel:
    for a, other in ((p, q), (q, p)):
        a1 = a ^ 1
        o0, o1 = other & ~1, (other & ~1) | 1
        sw = {o0: o1, o1: o0}
        letters = [y for y in range(14) if y not in (a, a1)]
        for y, z in itertools.combinations(letters, 2):
            l1, l2 = frozenset((a, y)), frozenset((a, z))
            m1, m2 = frozenset((a1, sw.get(y, y))), frozenset((a1, sw.get(z, z)))
            if not all(t in idx for t in (l1, l2, m1, m2)):
                continue
            x1, x2 = e[(idx[l1], idx[l2])], e[(idx[m1], idx[m2])]
            sol.add_clause([-x1, x2])
            sol.add_clause([x1, -x2])
            nties += 1
print("labels %d, pair orbits %d, target nullity >= %d, HREL %s (%d ties)" % (n, len(reps), target, hrel, nties),
      flush=True)
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
t0 = time.time()
count = npsd = 0
hist, saved = {}, []
best = -99.0
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
    best = max(best, min(lt, lu))
    if min(lt, lu) <= -1e-9:
        continue
    npsd += 1
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    hist[nul] = hist.get(nul, 0) + 1
    if nul >= target:
        r = exact_rank(M8.tolist())
        print("HIT: PSD %d-label structure with exact rank %d (numerical nullity %d), lambda (%.4f, %.4f)"
              % (n, r, nul, lt, lu), flush=True)
        if len(saved) < 500:
            saved.append({"labels": [sorted(l) for l in S], "gens": gens_s, "exact_rank": r, "lambda_T": lt,
                          "lambda_U": lu, "edges": [[a, b] for a in range(n) for b in range(a + 1, n) if G[a, b]]})
print("%s | %s: %d invariant admissible structures (%s), %d with T, U PSD, best min(lambda_T, lambda_U) %.4f, %.0f s"
      % (sys.argv[1], gens_s, count, "COMPLETE" if complete else "stopped by time", npsd, best, time.time() - t0),
      flush=True)
print("PSD structures by numerical nullity:", sorted(hist.items(), reverse=True))
json.dump({"stars": stars, "gens": gens_s, "complete": complete, "count": count, "psd": npsd, "best": best,
           "nullity_hist": hist, "structures": saved}, open(out + "_enum6.json", "w"))
