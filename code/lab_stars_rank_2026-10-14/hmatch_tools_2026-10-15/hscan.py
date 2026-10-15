import json, sys, glob
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval
files = []
for pat in sys.argv[1:]:
    files += glob.glob(pat)
hm = {0: 1, 1: 0, 2: 3, 3: 2}
from collections import Counter
cnt = Counter(); bad = []
Kc = {}
for f in sorted(set(files)):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if "edges" not in d:
        if "best" in d and "edges" in d["best"]:
            d["edges"] = d["best"]["edges"]
        else:
            continue
    S = [frozenset(l) for l in d["labels"]]; n = len(S)
    idx = {s: i for i, s in enumerate(S)}
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in d["edges"]: G[i, j] = G[j, i] = 1
    key = tuple(sorted(map(tuple, d["labels"])))
    if key not in Kc:
        Kc[key] = np.array([[kval(a, b) for b in S] for a in S])
    T = 3*np.eye(n) - G - Kc[key]
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    has = int(np.abs(G[np.ix_(hp, hp)] - G).sum()) // 2
    cnt[(nul >= 14, has == 0)] += 1
    if nul >= 14 and has > 0:
        bad.append((f, nul, has, d.get("gens")))
print("(nullity>=14, h-invariant) counts:", dict(cnt))
for b in bad[:40]: print("NOT h-invariant with nullity >= 14:", b)
