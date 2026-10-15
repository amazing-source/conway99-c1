"""Exact det(3I - Gamma^odd) (22 x 22 signed odd quotient) for h-invariant structures with lambda_max(Gamma^odd) <= 3;
is it a perfect square?  Distribution by grid / non-grid.  usage: python odd_det.py <glob> [...]"""
import glob, json, sys, math
from collections import Counter
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, '.')
hm = {0: 1, 1: 0, 2: 3, 3: 2}
def idet(M):
    M = [[F(x) for x in r] for r in M]; n = len(M); det = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return 0
        if p != c: M[c], M[p] = M[p], M[c]; det = -det
        det *= M[c][c]
        for r in range(c + 1, n):
            if M[r][c] != 0:
                fac = M[r][c] / M[c][c]; M[r] = [a - fac * b for a, b in zip(M[r], M[c])]
    return int(det)
files = []
for g in sys.argv[1:]: files += sorted(glob.glob(g))
seen = set(); cnt = Counter(); vals = {}
for f in files:
    try: d = json.load(open(f))
    except Exception: continue
    if not isinstance(d, dict) or "edges" not in d or len(d.get("labels", [])) != 44: continue
    S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    key = frozenset(frozenset((S[a], S[b])) for a, b in d["edges"])
    if key in seen: continue
    seen.add(key)
    G = np.zeros((n, n), dtype=int)
    for a, b in d["edges"]: G[a, b] = G[b, a] = 1
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    if not np.array_equal(G[np.ix_(hp, hp)], G): continue
    reps = [frozenset((0, y)) for y in range(4, 14)] + [frozenset((2, y)) for y in range(4, 14)] + [frozenset((0, 2)), frozenset((0, 3))]
    R = [idx[s] for s in reps]
    Sg = [[int(G[R[i], R[j]] - G[R[i], hp[R[j]]]) for j in range(22)] for i in range(22)]
    w = np.linalg.eigvalsh(np.array(Sg, dtype=float))
    if w[-1] > 3 + 1e-9: continue
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    dt = idet([[(3 if i == j else 0) - Sg[i][j] for j in range(22)] for i in range(22)])
    sq = dt >= 0 and math.isqrt(dt) ** 2 == dt
    k = ("grid" if grid else "nogrid", "det 0" if dt == 0 else ("square" if sq else "NOT square"))
    cnt[k] += 1; vals.setdefault(k, []).append(dt)
for k in sorted(cnt):
    v = sorted(set(vals[k]))
    print(k, cnt[k], "values (first 12):", v[:12])
