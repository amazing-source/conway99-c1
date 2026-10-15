"""Tally c, transversals, grid and square-class parities of rank-30 PSD objects not yet in the bundle (LAB 15/10/2026).
usage: python tally_new30.py <glob> [<glob> ...]"""
import glob
import json
import math
import sys

import numpy as np

from stars_rank import kval
from disc_scan import sym_pivot_det

files = sorted(f for g in sys.argv[1:] for f in glob.glob(g))
old = json.load(open('rank30_psd_objects_2026-10-15.json'))
seen = {tuple(tuple(e) for e in st["edges"]) for st in old["structures"]}
labels = old["labels"]
S = [frozenset(l) for l in labels]
n = len(S)
idx = {s: i for i, s in enumerate(S)}
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
sq = [(idx[frozenset((0, 2))], idx[frozenset((0, 3))]), (idx[frozenset((0, 2))], idx[frozenset((1, 2))]),
      (idx[frozenset((0, 3))], idx[frozenset((1, 3))]), (idx[frozenset((1, 2))], idx[frozenset((1, 3))])]
tally = {}
new = []
for f in files:
    d = json.load(open(f))
    if d["labels"] != labels:
        continue
    key = tuple(tuple(e) for e in d["edges"])
    if key in seen:
        continue
    seen.add(key)
    E = {frozenset(e) for e in d["edges"]}
    tl = sum(1 for x in range(2, 14) if frozenset((idx[frozenset((0, x))], idx[frozenset((1, x))])) in E)
    tm = sum(1 for x in [0, 1] + list(range(4, 14)) if frozenset((idx[frozenset((2, x))], idx[frozenset((3, x))])) in E)
    grid = all(frozenset(p) in E for p in sq)
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    r, det, _ = sym_pivot_det((24 * np.eye(n, dtype=np.int64) - 8 * G - K8).tolist())
    if r is None or r != 30:
        continue
    D = int(det)
    par = []
    for p in (2, 3, 5, 7):
        e = 0
        while D % p == 0:
            D //= p
            e += 1
        par.append(e % 2)
    other = D != 1 and math.isqrt(D) ** 2 != D
    k = (tuple(d.get("c", [])), tl, tm, grid, tuple(par), other, f.split('_H30_')[0])
    tally[k] = tally.get(k, 0) + 1
    new.append({"source": f, "c": d.get("c"), "t": [tl, tm], "grid": grid, "edges": d["edges"]})
print("new distinct exact rank-30 PSD objects:", len(new))
for k, v in sorted(tally.items(), key=lambda kv: -kv[1]):
    print("  c %s t (%d,%d) grid %s parities(v2,v3,v5,v7) %s other primes %s run %s : %d" % (k + (v,)))
json.dump({"labels": labels, "structures": new}, open('rank30_new_objects.json', 'w'))
