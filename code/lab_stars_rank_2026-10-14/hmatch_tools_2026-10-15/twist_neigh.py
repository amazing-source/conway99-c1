"""Exhaustive neighbourhood of an h-invariant rank-30 object with ALL 24 transversals forced and BROKEN star matchings
required (LAB 15/10/2026, mechanism of the 13-wall).  Free labels: those meeting the given outer letters.  Every
solution: numerical nullity, T and U PSD, and the rank balance of both sides (as balance.py): c, odd gain, even gain,
individually absorbed even vectors.  Saves the solutions of nullity >= 13 (cap 30) for inspection.
usage: python twist_neigh.py <seed json> <outer letters, e.g. 4,5,6,7> <out prefix> [max seconds]"""
import itertools
import json
import random
import sys
import time
from collections import Counter

import numpy as np
from pycryptosat import Solver

sys.path.insert(0, '.')
from stars_rank import build, kval, LABELS
from balance import side

seedf, lets, out = sys.argv[1], [int(t) for t in sys.argv[2].split(",")], sys.argv[3]
maxsec = float(sys.argv[4]) if len(sys.argv) > 4 else 280
S, idx, e, F = build([0, 1, 2, 3], random.Random(1))
n = len(S)
d = json.load(open(seedf))
assert [sorted(l) for l in S] == d["labels"]
E0 = {tuple(sorted(x)) for x in d["edges"]}
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
L = lambda *x: idx[frozenset(x)]
for x in range(2, 14):
    sol.add_clause([e[(L(0, x), L(1, x))]])
for x in [0, 1] + list(range(4, 14)):
    sol.add_clause([e[(L(2, x), L(3, x))]])
h = {0: 1, 1: 0, 2: 3, 3: 2}
nv = F.n
xs = []
for (a, a2) in ((0, 1), (2, 3)):
    others = [t for t in range(14) if t not in (a, a2)]
    for y, z in itertools.combinations(others, 2):
        p = e[(L(a, y), L(a, z))]
        q = e[(L(a2, h.get(y, y)), L(a2, h.get(z, z)))]
        nv += 1
        sol.add_clause([-nv, p, q])
        sol.add_clause([-nv, -p, -q])
        xs.append(nv)
sol.add_clause(xs)
free = {i for i in range(n) if S[i] & set(lets)}
pairs = list(itertools.combinations(range(n), 2))
assum = [e[p] if p in E0 else -e[p] for p in pairs if p[0] not in free and p[1] not in free]
var_pairs = [p for p in pairs if p[0] in free or p[1] in free]
K = np.array([[kval(a, b) for b in S] for a in S])
K8 = np.rint(8 * K).astype(np.int64)
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
t0 = time.time()
hist = Counter()
cnt = 0
saved = 0
complete = False
while time.time() - t0 < maxsec:
    ok, model = sol.solve(assum)
    if not ok:
        complete = True
        break
    cnt += 1
    sol.add_clause([-e[p] if model[e[p]] else e[p] for p in var_pairs])
    G = np.zeros((n, n), dtype=np.int64)
    for p in pairs:
        if model[e[p]]:
            G[p] = 1
            G[p[1], p[0]] = 1
    T = 3 * np.eye(n) - G - K
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    cl, ogl, egl, _, perl = side(S, idx, G, M8, T, 0, 1, 2, 3)
    cm, ogm, egm, _, perm = side(S, idx, G, M8, T, 2, 3, 0, 1)
    key = (min(lt, lu) > -1e-9, nul, (cl, ogl, egl), (cm, ogm, egm))
    hist[key] += 1
    if nul >= 13 and saved < 30:
        saved += 1
        json.dump({"labels": d["labels"], "edges": [[i, j] for i, j in pairs if G[i, j]], "nullity_numeric": nul,
                   "lambda_T": lt, "lambda_U": lu}, open("%s_%d.json" % (out, saved), "w"))
print("%d structures (%s), %.0f s; free labels %d" % (cnt, "COMPLETE" if complete else "stopped", time.time() - t0,
                                                     len(free)), flush=True)
print("(PSD, nullity, (c, odd gain, even gain) side l, same side m): count")
for k, v in sorted(hist.items(), key=lambda t: (-t[0][1], str(t[0]))):
    print("  ", k, v)
