"""HMATCH-style walk in the generalised star model (LAB 15/10/2026): calibration of the (H-MATCH) evidence.

Identity group.  Moves: free the pairs touching NFREE random labels, re-solve (random polarity) with the other pairs
fixed.  Score on PSD structures (T, U >= 0 on the complement of the star vectors): -3 max(0, target - nullity), minus
HPEN when the star matchings are h-related for EVERY pair of lines among the stars (i.e. a structure counts as broken
when at least one pair of lines has M_{a'} != h(M_a) or M_{b'} != h(M_b)); off the PSD set -100 + 3 min(lambda).
Metropolis at temperature TEMP (constant).  Reports records of the nullity of PSD broken structures and saves every
PSD broken structure of nullity >= target (cap 20).
usage: python walk_gen.py <seed json (labels in model order)> <target nullity> <seconds> <out prefix> [nfree] [hpen]
       [temp] [rng seed]"""
import itertools
import json
import math
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_gen import Model

seedf, target, maxsec, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
nfree = int(sys.argv[5]) if len(sys.argv) > 5 else 6
hpen = float(sys.argv[6]) if len(sys.argv) > 6 else 8.0
temp = float(sys.argv[7]) if len(sys.argv) > 7 else 0.4
rs = int(sys.argv[8]) if len(sys.argv) > 8 else 1
d = json.load(open(seedf))
M = Model(d["k"], d["r"], d["s"])
stars = d["stars"]
S, idx, e, F = M.build(stars, random.Random(1))
n = len(S)
assert [sorted(l) for l in S] == d["labels"]
rng = random.Random(rs)
sol = Solver(options={"polar": "rnd", "seed": str(rs)})
for c in F.clauses:
    sol.add_clause(c)
K, Pi = M.matrices(S)
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
lines = [(stars[2 * t], stars[2 * t + 1]) for t in range(len(stars) // 2)]
hinfo = []
for (a, a2), (b, b2) in itertools.combinations(lines, 2):
    hm = {a: a2, a2: a, b: b2, b2: b}
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    starp = [(i, j) for i, j in itertools.combinations(range(n), 2) if S[i] & S[j] & {a, a2, b, b2}]
    hinfo.append((hp, starp))
pairs = list(itertools.combinations(range(n), 2))


def evaluate(G):
    T = M.r * np.eye(n) - G - K
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ ((M.r - M.s) * Pi - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    asym = [sum(1 for i, j in sp if G[i, j] != G[hp[i], hp[j]]) for hp, sp in hinfo]
    return lt, lu, nul, asym


G = np.zeros((n, n))
for i, j in d["edges"]:
    G[i, j] = G[j, i] = 1
model = None
lt, lu, nul, asym = evaluate(G)
print("seed: nullity %d, lambda_T %.4f, lambda_U %.4f, star-matching asymmetry per pair %s" % (nul, lt, lu, asym), flush=True)


def score(lt, lu, nul, asym):
    if min(lt, lu) > -1e-9:
        return -3.0 * max(0, target - nul) - (hpen if max(asym) == 0 else 0.0)
    return -100.0 + 3.0 * min(lt, lu)


cur = score(lt, lu, nul, asym)
t0 = time.time()
rec = -1
saved = 0
mv = 0
hist = {}
while time.time() - t0 < maxsec:
    mv += 1
    R = set(rng.sample(range(n), nfree))
    assum = [e[p] if G[p] else -e[p] for p in pairs if p[0] not in R and p[1] not in R]
    ok, m2 = sol.solve(assum)
    if not ok:
        continue
    G2 = np.zeros((n, n))
    for p in pairs:
        if m2[e[p]]:
            G2[p] = 1
            G2[p[1], p[0]] = 1
    lt2, lu2, nul2, asym2 = evaluate(G2)
    psd = min(lt2, lu2) > -1e-9
    broken = max(asym2) > 0
    if psd:
        hist[(nul2, broken)] = hist.get((nul2, broken), 0) + 1
    if psd and broken and nul2 > rec:
        rec = nul2
        print("move %d: RECORD PSD broken nullity %d (asymmetry %s), %.0f s" % (mv, nul2, asym2, time.time() - t0),
              flush=True)
    if psd and broken and nul2 >= target and saved < 20:
        saved += 1
        json.dump({"k": M.k, "r": M.r, "s": M.s, "stars": stars, "labels": d["labels"], "asym": asym2,
                   "nullity_numeric": nul2, "lambda_T": lt2, "lambda_U": lu2,
                   "edges": [[i, j] for i, j in pairs if G2[i, j]]}, open("%s_T%d.json" % (out, saved), "w"))
        if saved <= 3:
            print("move %d: CALIBRATION TARGET: PSD broken nullity %d (asymmetry %s)" % (mv, nul2, asym2), flush=True)
    s2 = score(lt2, lu2, nul2, asym2)
    if s2 >= cur or rng.random() < math.exp((s2 - cur) / temp):
        G, cur = G2, s2
    if mv % 500 == 0:
        print("move %d: %.0f s, current score %.2f, PSD (nullity, broken) histogram %s" % (mv, time.time() - t0, cur,
                                                                                      dict(sorted(hist.items()))),
              flush=True)
print("end: %d moves, record PSD broken nullity %d, histogram %s" % (mv, rec, dict(sorted(hist.items()))), flush=True)
