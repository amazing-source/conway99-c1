"""V4 = <(0 1), (2 3)> (formal letter swaps). W++ = span(u_y = e0y+e1y, g_y = e2y+e3y, 1_C) (21 V4-invariant vectors).
A++ = Gram of W++ under T_S (depends only on V4-orbit edge counts).  Under (SYM) nu(T_S) = 2 + nu(A++).
Prints, per class: nu, 2 + nu(A++), c, whether equal.  usage: python v4_quotient.py <glob> [...]"""
import glob, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
files = []
for g in sys.argv[1:]: files += sorted(glob.glob(g))
seen = set(); cnt = Counter(); ex = {}
for f in files:
    try: d = json.load(open(f))
    except Exception: continue
    if not isinstance(d, dict) or "edges" not in d or len(d.get("labels", [])) != 44: continue
    S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    key = frozenset(frozenset((S[a], S[b])) for a, b in d["edges"])
    if key in seen: continue
    seen.add(key)
    G = np.zeros((n, n))
    for a, b in d["edges"]: G[a, b] = G[b, a] = 1
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    tpsd = np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] > -1e-9
    if not tpsd: continue
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
    W = []
    for (a, b) in ((0, 1), (2, 3)):
        for y in range(4, 14):
            v = np.zeros(n); v[idx[frozenset((a, y))]] = 1; v[idx[frozenset((b, y))]] = 1; W.append(v)
    v = np.zeros(n)
    for p in ((0, 2), (0, 3), (1, 2), (1, 3)): v[idx[frozenset(p)]] = 1
    W.append(v); W = np.array(W).T
    App = W.T @ T @ W
    nupp = int(np.sum(np.abs(np.linalg.eigvalsh(App)) < 1e-7))
    def side(st):
        lab = [i for i in range(n) if S[i] & set(st)]
        return int(np.sum(np.abs(np.linalg.eigvalsh(T[np.ix_(lab, lab)])) < 1e-7)) - 1
    cl, cm = side((0, 1)), side((2, 3))
    k = ("grid" if grid else "nogrid", "nu == 2 + nu(A++)" if nu == 2 + nupp else "nu > 2 + nu(A++)")
    cnt[k] += 1; ex.setdefault(k, (f, nu, nupp, cl, cm))
    if not grid:
        cnt[("nogrid", "nu(A++) - 7 - min c", nupp - 7 - min(cl, cm))] += 1
for k in sorted(cnt, key=str): print(k, cnt[k], ex.get(k, ""))
