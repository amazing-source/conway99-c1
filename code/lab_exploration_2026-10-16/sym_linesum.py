"""Test of the LINE-SUM hypothesis for the symmetric part of ker Q (exploration, LAB 16/10/2026).
Side l = {v,0,1}, other line m = {v,2,3}; Y rows r = 2, 3; columns s = 4..13 (the five lines {4,5}, ..., {12,13}).
For w in ker Q put f(s) = w_{2s} + w_{3s}.  LINE-SUM: f(s) + f(s') is the same for the five lines {s, s'}.
Also tests a few other candidate linear laws on f: total sum zero; f(s) = f(s') (line-constant).
Over all PSD structures, both sides, non-grid only: counts of sides where each law holds for the whole kernel.
usage: python sym_linesum.py <root dir> [max structures]"""
import collections
import itertools
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from q_split_scan import kval, MATE  # noqa: E402

root = sys.argv[1]
maxs = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9


def kernels(L, E):
    S = [l for l in L if l & {0, 1, 2, 3}]
    if len(S) != 44:
        return None
    verts = ["v"] + [("L", s) for s in range(14)] + S
    pos = {x: i for i, x in enumerate(verts)}
    n = len(verts)
    A = np.zeros((n, n))
    for s in range(14):
        A[pos["v"], pos[("L", s)]] = A[pos[("L", s)], pos["v"]] = 1
        A[pos[("L", s)], pos[("L", MATE(s))]] = 1
    for l in S:
        for s in l:
            A[pos[l], pos[("L", s)]] = A[pos[("L", s)], pos[l]] = 1
    for a, b in itertools.combinations(S, 2):
        if frozenset((a, b)) in E:
            A[pos[a], pos[b]] = A[pos[b], pos[a]] = 1
    iS = [pos[l] for l in S]
    T = 3 * np.eye(44) - A[np.ix_(iS, iS)] - np.array([[kval(a, b) for b in S] for a in S])
    if np.linalg.eigvalsh(T)[0] < -1e-8:
        return None
    out = []
    for (p, q), (r1, r2) in (((0, 1), (2, 3)), ((2, 3), (0, 1))):
        Nset = [("L", s) for s in range(14) if s not in (p, q)] + [l for l in S if l & {p, q}]
        cols = [s for s in range(14) if s not in (0, 1, 2, 3)]
        Yset = [frozenset((r, s)) for r in (r1, r2) for s in cols]
        iN = [pos[x] for x in Nset]
        iY = [pos[x] for x in Yset]
        ev, V = np.linalg.eigh(3 * np.eye(36) - A[np.ix_(iN, iN)])
        inv = (V[:, ev > 1e-9] / ev[ev > 1e-9]) @ V[:, ev > 1e-9].T
        AYN = A[np.ix_(iY, iN)]
        Q = 3 * np.eye(20) - A[np.ix_(iY, iY)] - AYN @ inv @ AYN.T
        eq, VQ = np.linalg.eigh(Q)
        K = VQ[:, np.abs(eq) < 1e-8]
        null = V[:, ev < 1e-9]
        i0 = Nset.index(("L", r1))
        same = [j for j in range(36) if np.allclose(null[j], null[i0], atol=1e-8)]
        out.append((K, cols, len(same) == 6))
    g = out[0][2] or out[1][2]
    return [(K, cols, g) for K, cols, _ in out]


laws = collections.Counter()
nst = 0
seen = set()
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".json") or nst >= maxs:
            continue
        try:
            d = json.load(open(os.path.join(dp, f)))
            L = [frozenset(x) for x in d["labels"]]
            E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
        except Exception:
            continue
        key = frozenset(E)
        if key in seen:
            continue
        seen.add(key)
        r = kernels(L, E)
        if r is None:
            continue
        nst += 1
        for K, cols, grid in r:
            if grid:
                continue
            laws["sides"] += 1
            F = K[:10, :] + K[10:, :]                  # symmetric parts, 10 x corank
            lines = [(cols[2 * i], cols[2 * i + 1]) for i in range(5)]
            idx = {s: i for i, s in enumerate(cols)}
            sums = np.array([F[idx[a], :] + F[idx[b], :] for a, b in lines])   # 5 x corank
            if np.allclose(sums - sums[0], 0, atol=1e-7):
                laws["LINE-SUM"] += 1
            if np.allclose(F.sum(0), 0, atol=1e-7):
                laws["total sum 0"] += 1
            diffs = np.array([F[idx[a], :] - F[idx[b], :] for a, b in lines])
            if np.allclose(diffs, 0, atol=1e-7):
                laws["line-constant"] += 1
            if np.allclose(sums, 0, atol=1e-7):
                laws["line sums all 0"] += 1
print("structures %d; non-grid sides %d; law counts %s" % (nst, laws["sides"], dict(laws)))
