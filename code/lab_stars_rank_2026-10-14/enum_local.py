"""Exhaustive local neighbourhood of a four-star structure (LAB 15/10/2026, (H-MATCH) test).

All admissible structures (same SAT model as sym4g.py, identity group) that agree with the start structure on every pair
of labels NOT touching a chosen set F of free labels are enumerated (blocking clauses on the pairs touching F, complete
when UNSAT).  For each: T, U PSD (numerical, on the complement of the star vectors), numerical nullity, h-asymmetry of
the four star matchings (masym = pairs of labels sharing a star letter whose adjacency differs from that of their
h-images; masym > 0 <=> M_1 != h(M_0) or M_3 != h(M_2)).  Saves every PSD structure of nullity >= 14 with masym > 0.
usage: python enum_local.py <start json> <free labels, e.g. 0-4,1-4,0-6> <out prefix> [max solutions] [max seconds]"""
import itertools
import json
import sys
import time
from collections import Counter

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
import random

start, free_s, out = sys.argv[1], sys.argv[2], sys.argv[3]
maxsol = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 7
maxsec = float(sys.argv[5]) if len(sys.argv) > 5 else 3000
rng = random.Random(1)
S, idx, e, F = build([0, 1, 2, 3], rng)
n = len(S)
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
d = json.load(open(start))
assert [sorted(l) for l in S] == d["labels"]
E0 = {tuple(x) for x in d["edges"]}
free = {idx[frozenset(int(t) for t in p.split("-"))] for p in free_s.split(",")}
fixed = [(i, j) for i, j in itertools.combinations(range(n), 2) if i not in free and j not in free]
var_pairs = [(i, j) for i, j in itertools.combinations(range(n), 2) if i in free or j in free]
assum = [e[p] if p in E0 else -e[p] for p in fixed]
K = np.array([[kval(a, b) for b in S] for a in S])
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
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
print("free labels %s (%d), free pairs %d" % (sorted(sorted(S[i]) for i in free), len(free), len(var_pairs)), flush=True)
t0 = time.time()
hist = Counter()
count = 0
saved = 0
complete = False
while count < maxsol and time.time() - t0 < maxsec:
    ok, model = sol.solve(assum)
    if not ok:
        complete = True
        break
    count += 1
    sol.add_clause([-e[p] if model[e[p]] else e[p] for p in var_pairs])
    G = np.zeros((n, n))
    for (i, j), v in e.items():
        if i < j and model[v]:
            G[i, j] = G[j, i] = 1
    T = 3 * np.eye(n) - G - K
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    psd = min(lt, lu) > -1e-9
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    masym = sum(1 for (i, j) in sl if G[i, j] != G[hp[i], hp[j]])
    hist[(psd, nul, masym > 0)] += 1
    if psd and nul >= 14 and masym > 0:
        saved += 1
        if saved <= 50:
            json.dump({"labels": d["labels"], "masym": masym, "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul,
                       "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                      open(out + "_LOC_%d.json" % saved, "w"))
        if saved <= 3:
            print("LOCAL TARGET HIT: PSD, nullity %d, matchings not h-related (%d pairs), saved %s_LOC_%d.json"
                  % (nul, masym, out, saved), flush=True)
print("%d admissible structures in the neighbourhood (%s), %.0f s" % (count, "COMPLETE" if complete else "stopped",
                                                                      time.time() - t0), flush=True)
print("(PSD, numerical nullity, matchings broken): count")
for k, v in sorted(hist.items(), key=lambda t: (t[0][0], t[0][1], t[0][2]), reverse=True):
    print("  ", k, v)
