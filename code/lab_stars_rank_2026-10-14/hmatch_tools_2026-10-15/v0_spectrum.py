"""Spectrum of Gamma on V0 = {x : D x = 0} (dim 30), where T = 3 - Gamma and U = 4 + Gamma exactly (LAB 15/10/2026).
Reports lambda_min, lambda_max of Gamma on V0 and the full-space lambda_min of T, U (complement of the star vectors),
to locate a positivity failure inside V0 or in the 14 letter directions D^T.
usage: python v0_spectrum.py <json or dir> [...]"""
import glob, json, os, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, '..')
from stars_rank import kval, LABELS
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
files = []
for a in sys.argv[1:]:
    files += sorted(glob.glob(os.path.join(a, "*.json"))) if os.path.isdir(a) else [a]
tab = Counter()
for f in files:
    d = json.load(open(f))
    if "edges" not in d:
        continue
    S = [frozenset(l) for l in d["labels"]]; n = len(S)
    G = np.zeros((n, n))
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    D = D84[:, [pos[l] for l in S]]
    _, s, Vt = np.linalg.svd(D)
    W = Vt[int(np.sum(s > 1e-9)):].T
    g = np.linalg.eigvalsh(W.T @ G @ W)
    K = np.array([[kval(a, b) for b in S] for a in S])
    T = 3 * np.eye(n) - G - K
    U = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    lt = np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0]; lu = np.linalg.eigvalsh(P @ U @ P + 50 * Q @ Q.T)[0]
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    key = (nu, "T>=0" if lt > -1e-9 else "T fails", "U>=0" if lu > -1e-9 else "U fails",
           "V0 in [-4,3]" if g[0] > -4 - 1e-9 and g[-1] < 3 + 1e-9 else "V0: min %.3f max %.3f" % (g[0], g[-1]),
           "dimV0=%d" % W.shape[1])
    tab[key] += 1
for k, v in sorted(tab.items(), key=lambda kv: -kv[1]):
    print("  ", k, v)
