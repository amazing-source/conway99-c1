"""Staged rank gains (LAB 15/10/2026 evening, (N9-NG) mechanism): for every distinct T, U PSD structure of a corpus
(nullity >= NUMIN, or non-grid of any nullity), exact g2 = rank(X_l + outer labels of star 2) - rank(X_l) and
g3 = rank(S4) - rank(X_l + star 2), on both sides (side m: X_m, then star 0, then star 1).  nu = 21 + c - g2 - g3.
usage: python staged_gain_scan.py <dir> [...]"""
import glob, json, os, sys
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from stars_rank import kval, LABELS
from z5_enum import exact_rank
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
numin = int(os.environ.get("NUMIN", "13"))
files = []
for a in sys.argv[1:]:
    files += sorted(glob.glob(os.path.join(a, "*.json"))) if os.path.isdir(a) else [a]
seen = set(); tab = Counter(); ex = {}
for f in files:
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if not isinstance(d, dict) or "edges" not in d or len(d.get("labels", [])) != 44:
        continue
    S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    key = frozenset(frozenset((S[a], S[b])) for a, b in d["edges"])
    if key in seen:
        continue
    seen.add(key)
    G = np.zeros((n, n), dtype=np.int64)
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
    M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    T = M8 / 8.0
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
    if nu < numin and grid:
        continue
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9:
        continue
    U = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    if np.linalg.eigvalsh(P @ U @ P + 50 * Q @ Q.T)[0] < -1e-9:
        continue
    rk = lambda ids: exact_rank(M8[np.ix_(ids, ids)].tolist())
    out = []
    for (a, a2, b, b2) in ((0, 1, 2, 3), (2, 3, 0, 1)):
        X = [i for i in range(n) if S[i] & {a, a2}]
        Lb = [idx[frozenset((b, y))] for y in range(4, 14)]
        Lb2 = [idx[frozenset((b2, y))] for y in range(4, 14)]
        r0 = rk(X); r1 = rk(X + Lb); r2 = rk(X + Lb + Lb2)
        out.append((23 - r0, r1 - r0, r2 - r1))
    k = ("grid" if grid else "no grid", nu, "l: c %d g2 %d g3 %d" % out[0], "m: c %d g2 %d g3 %d" % out[1])
    tab[k] += 1; ex.setdefault(k, f)
print("(grid, nu, side l (c, g2, g3), side m (c, g2, g3)): count, example")
for k, v in sorted(tab.items(), key=lambda kv: (kv[0][0], -kv[0][1])):
    print("  ", k, v, ex[k])
