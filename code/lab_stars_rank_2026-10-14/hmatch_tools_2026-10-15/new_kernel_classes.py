"""New kernel classes from harvested rank-30 objects (LAB 15/10/2026, task T3 sweep).

Reads harvested structure files (glob), keeps those that are EXACTLY PSD (symmetric pivoting of 8T, disc_scan) with T of
rank exactly 30 and U PSD (numerical), computes the exact kernel (reduced row echelon form, a canonical key), and drops
the kernels already known (all structures in the given reference bundles).  Writes one representative json per NEW
kernel class into <out dir> (for kernel_sat_enum.py) and a summary.
usage: python new_kernel_classes.py <out dir> <glob of harvested files> [reference bundle ...]"""
import glob
import json
import os
import sys
from fractions import Fraction as Fr

import numpy as np

sys.path.insert(0, '.')
from stars_rank import kval, LABELS
from cls_decomp import nullspace_int
from disc_scan import sym_pivot_det

outdir, pat = sys.argv[1], sys.argv[2]
refs = sys.argv[3:]
os.makedirs(outdir, exist_ok=True)


def key_of(N, n):
    A = [[Fr(x) for x in row] for row in N]
    r = 0
    m = len(A)
    for c in range(n):
        p = next((i for i in range(r, m) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return tuple(tuple(row) for row in A[:r])


def items(f):
    d = json.load(open(f))
    if isinstance(d, dict) and "structures" in d:
        for s in d["structures"]:
            yield d["labels"], s["edges"]
    elif isinstance(d, dict) and "edges" in d:
        yield d["labels"], d["edges"]


cache = {}


def prep(labels):
    k = tuple(map(tuple, labels))
    if k not in cache:
        S = [frozenset(l) for l in labels]
        K8 = [[int(round(8 * kval(a, b))) for b in S] for a in S]
        D84 = np.zeros((14, 84))
        for jj, l in enumerate(LABELS):
            for y in l:
                D84[y, jj] = 1
        Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
        pos = {l: ii for ii, l in enumerate(LABELS)}
        PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
        Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
        Qz, _ = np.linalg.qr(Z)
        cache[k] = (S, K8, PiS, np.eye(len(S)) - Qz @ Qz.T)
    return cache[k]


def kernel_key(labels, edges):
    S, K8, PiS, Pp = prep(labels)
    n = len(S)
    E = {tuple(sorted(e)) for e in edges}
    M = [[(24 if a == b else 0) - 8 * (1 if tuple(sorted((a, b))) in E else 0) - K8[a][b] for b in range(n)] for a in range(n)]
    return M, key_of(nullspace_int(M), n)


known = set()
for f in refs:
    for labels, edges in items(f):
        known.add(kernel_key(labels, edges)[1])
print("known kernel classes:", len(known), flush=True)
new = {}
seen_struct = set()
nfiles = 0
for f in sorted(glob.glob(pat)):
    for labels, edges in items(f):
        nfiles += 1
        sk = frozenset(tuple(sorted(e)) for e in edges)
        if sk in seen_struct:
            continue
        seen_struct.add(sk)
        S, K8, PiS, Pp = prep(labels)
        n = len(S)
        M, key = kernel_key(labels, edges)
        r, det, _ = sym_pivot_det(M)
        if r is None or r != 30:
            continue
        T = np.array(M, dtype=float) / 8
        lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
        if lu <= -1e-9:
            continue
        if key in known or key in new:
            continue
        new[key] = (f, labels, edges)
print("harvested files %d, distinct structures %d, NEW kernel classes %d" % (nfiles, len(seen_struct), len(new)), flush=True)
for k, (key, (f, labels, edges)) in enumerate(new.items()):
    json.dump({"labels": labels, "edges": edges, "source": f}, open(os.path.join(outdir, "newk_%d.json" % k), "w"))
print("written to", outdir)
