"""Scan saved structures: numerical nullity, PSD (numerical), full h-asymmetry, star-matching h-asymmetry."""
import json, sys, glob
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval, LABELS
from collections import Counter, defaultdict
files = []
for pat in sys.argv[1:]:
    files += glob.glob(pat)
hm = {0: 1, 1: 0, 2: 3, 3: 2}
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l: D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
best = defaultdict(lambda: -1); bestf = {}
cache = {}
for f in sorted(set(files)):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if "edges" not in d:
        if "best" in d and isinstance(d["best"], dict) and "edges" in d["best"]:
            d["edges"] = d["best"]["edges"]
        else:
            continue
    if "labels" not in d: continue
    key = tuple(map(tuple, d["labels"]))
    if key not in cache:
        S = [frozenset(l) for l in d["labels"]]; n = len(S)
        idx = {s: i for i, s in enumerate(S)}
        hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
        K = np.array([[kval(a, b) for b in S] for a in S])
        PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
        Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
        Qz, _ = np.linalg.qr(Z); Pp = np.eye(n) - Qz @ Qz.T
        sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
        cache[key] = (S, n, hp, K, PiS, Pp, sl)
    S, n, hp, K, PiS, Pp, sl = cache[key]
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in d["edges"]: G[i, j] = G[j, i] = 1
    T = 3*np.eye(n) - G - K
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    psd = min(lt, lu) > -1e-9
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    has = int(np.abs(G[np.ix_(hp, hp)] - G).sum()) // 2
    mas = sum(1 for (i, j) in sl if G[i, j] != G[hp[i], hp[j]])
    cls = ("PSD" if psd else "T-only" if lt > -1e-9 else "notPSD", "h-inv" if has == 0 else ("match-inv" if mas == 0 else "match-broken"))
    if nul > best[cls]:
        best[cls] = nul; bestf[cls] = f
print("max numerical nullity by (positivity, symmetry class):")
for k in sorted(best): print("  ", k, best[k], bestf[k])
