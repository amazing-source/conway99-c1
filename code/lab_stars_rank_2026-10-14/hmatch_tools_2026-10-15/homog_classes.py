"""Distinct h-homogeneous kernel parts of broken structures (LAB 15/10/2026, task T3).

For each structure file (glob) whose star matchings are NOT h-related and whose T is PSD (numerical, complement of the
star vectors), compute exactly N n hN = ker(M + hMh) (M = 8T; valid as N n hN when T >= 0), key it by its reduced row
echelon form, and write one representative per distinct key to <out dir> (for kernel_sat_enum.py with KHOMOG=1).
usage: python homog_classes.py <out dir> <glob> [glob ...]"""
import glob
import json
import os
import random
import sys
from fractions import Fraction as Fr

import numpy as np

sys.path.insert(0, '.')
from stars_rank import build, kval
from cls_decomp import nullspace_int

outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)
S, idx, e, F = build([0, 1, 2, 3], random.Random(5))
n = len(S)
K8 = [[int(round(8 * kval(a, b))) for b in S] for a in S]
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T


def rref_key(vecs):
    A = [[Fr(x) for x in v] for v in vecs]
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return tuple(tuple(row) for row in A[:r])


keys = {}
seen = set()
tot = 0
for pat in sys.argv[2:]:
    for f in sorted(glob.glob(pat)):
        d = json.load(open(f))
        if "edges" not in d and isinstance(d.get("best"), dict):
            d["edges"] = d["best"]["edges"]
        if "edges" not in d or [sorted(l) for l in S] != d.get("labels"):
            print("skipped (no edges or other labels): %s" % f, flush=True)
            continue
        E = {tuple(sorted(x)) for x in d["edges"]}
        sk = frozenset(E)
        if sk in seen:
            continue
        seen.add(sk)
        tot += 1
        G = [[1 if tuple(sorted((a, b))) in E else 0 for b in range(n)] for a in range(n)]
        if not any(G[i][j] != G[hp[i]][hp[j]] for (i, j) in sl):
            continue
        M = [[(24 if a == b else 0) - 8 * G[a][b] - K8[a][b] for b in range(n)] for a in range(n)]
        T = np.array(M, dtype=float) / 8
        if float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0]) <= -1e-9:
            continue
        Mh = [[M[a][b] + M[hp[a]][hp[b]] for b in range(n)] for a in range(n)]
        Nh = nullspace_int(Mh)
        key = rref_key(Nh)
        if key not in keys:
            keys[key] = f
            json.dump({"labels": d["labels"], "edges": d["edges"], "source": f, "homog_dim": len(Nh)},
                      open(os.path.join(outdir, "hk_%d.json" % (len(keys) - 1)), "w"))
            print("new homogeneous kernel (dim %d) from %s" % (len(Nh), f), flush=True)
print("distinct structures %d, distinct homogeneous kernels of broken T-PSD structures: %d" % (tot, len(keys)))
