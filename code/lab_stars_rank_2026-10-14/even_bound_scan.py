"""Robust scan of the even-absorption bound over many structures (LAB 15/10/2026): for every PSD structure read, the
explained T-norm E(y,y) of g_y = 1_{2y} + 1_{3y} (y outer) given B = X_l + span(f's), split by transversal (norm 5/2)
or not (norm 9/2), and the same with the roles of l and m exchanged.  Reports the maxima and the closest cases.
usage: python even_bound_scan.py <file with one json path per line> [max files] [max seconds]"""
import json
import sys
import time

import numpy as np

from stars_rank import kval

paths = [p.strip().replace(chr(92), '/') for p in open(sys.argv[1]) if p.strip()]
maxf = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
maxsec = float(sys.argv[3]) if len(sys.argv) > 3 else 270
t0 = time.time()
Kcache = {}
best_nt, best_t = (-1, ''), (-1, '')
done = 0
for p in paths[:maxf]:
    if time.time() - t0 > maxsec:
        break
    try:
        d = json.load(open(p))
        labels, edges = d["labels"], d["edges"]
    except Exception:
        continue
    key = tuple(tuple(l) for l in labels)
    S = [frozenset(l) for l in labels]
    n = len(S)
    if key not in Kcache:
        Kcache[key] = np.array([[kval(a, b) for b in S] for a in S])
    K = Kcache[key]
    idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for i, j in edges:
        G[i, j] = G[j, i] = 1
    T = 3 * np.eye(n) - G - K
    if np.linalg.eigvalsh(T)[0] < -1e-9:
        continue
    for (a, a2, b, b2) in ((0, 1, 2, 3), (2, 3, 0, 1)):
        Xl = [i for i in range(n) if S[i] & {a, a2}]
        Bv = [np.eye(n)[i] for i in Xl]
        F, Gv, trans = [], [], []
        for y in range(4, 14):
            u, w = idx[frozenset((b, y))], idx[frozenset((b2, y))]
            v = np.zeros(n); v[u] = 1; v[w] = -1; F.append(v)
            g = np.zeros(n); g[u] = 1; g[w] = 1; Gv.append(g)
            trans.append(G[u, w] == 1)
        B = np.array(Bv + F).T
        Gm = np.array(Gv).T
        GB = B.T @ T @ B
        wB, VB = np.linalg.eigh(GB)
        keep = wB > 1e-9
        C = B.T @ T @ Gm
        W2 = VB[:, keep].T @ C
        dE = np.einsum('ij,ij->j', W2, W2 / wB[keep][:, None])
        for k in range(10):
            if trans[k]:
                if dE[k] > best_t[0]:
                    best_t = (dE[k], p)
            elif dE[k] > best_nt[0]:
                best_nt = (dE[k], p)
    done += 1
print("structures scanned: %d (%.0f s)" % (done, time.time() - t0))
print("max explained norm, non-transversal letters (||g||^2 = 4.5): %.5f  [%s]" % best_nt)
print("max explained norm, transversal letters (||g||^2 = 2.5): %.5f  [%s]" % best_t)
