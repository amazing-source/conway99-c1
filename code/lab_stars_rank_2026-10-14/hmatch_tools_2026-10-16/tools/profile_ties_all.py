"""Pure-twist test: for PSD structures of nullity >= 14, pairs of labels in the same star whose kernel profiles
(rows of an orthonormal kernel basis) coincide.  A pure l-matching twist preserving the kernel needs such ties.
usage: python profile_ties.py <glob> [...]"""
import glob, json, sys, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval, LABELS
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l: D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
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
    w, V = np.linalg.eigh(T); N = V[:, np.abs(w) < 1e-7]
    if N.shape[1] < 6: continue
    Us = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    tpsd = np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] > -1e-9
    upsd = np.linalg.eigvalsh(P @ Us @ P + 50 * Q @ Q.T)[0] > -1e-9
    ties = 0
    for a in (0, 1, 2, 3):
        lab = [i for i in range(n) if a in S[i]]
        for i, j in itertools.combinations(lab, 2):
            if np.max(np.abs(N[i] - N[j])) < 1e-7: ties += 1
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    k = ("TU" if tpsd and upsd else ("T" if tpsd else "none"), "nu %d" % N.shape[1], "ties>0" if ties else "ties=0")
    cnt[k] += 1; ex.setdefault(k, f)
for k in sorted(cnt): print(k, cnt[k], ex[k])
