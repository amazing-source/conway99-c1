"""(DO) breakdown: which doubly-odd functionals fail (outer-line blocks on the l side / m side, the C4 one),
per class (T>=0 or not, grid or not).  usage: python do_breakdown.py <glob> [...]"""
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
    w_, V = np.linalg.eigh(T); N = V[:, np.abs(w_) < 1e-7]
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    tpsd = np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] > -1e-9
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    def wv(a, b, y, z):
        w = np.zeros(n)
        for s1, sg1 in ((a, 1), (b, -1)):
            for s2, sg2 in ((y, 1), (z, -1)):
                w[idx[frozenset((s1, s2))]] += sg1 * sg2
        return w
    fl = sum(1 for ln in ((4, 5), (6, 7), (8, 9), (10, 11), (12, 13)) if N.shape[1] and np.max(np.abs(wv(0, 1, *ln) @ N)) > 1e-6)
    fm = sum(1 for ln in ((4, 5), (6, 7), (8, 9), (10, 11), (12, 13)) if N.shape[1] and np.max(np.abs(wv(2, 3, *ln) @ N)) > 1e-6)
    fc = int(bool(N.shape[1] and np.max(np.abs(wv(0, 1, 2, 3) @ N)) > 1e-6))
    k = ("T>=0" if tpsd else "T not psd", "grid" if grid else "nogrid", "fail l-lines %d m-lines %d C4 %d" % (fl, fm, fc))
    cnt[k] += 1; ex.setdefault(k, f)
for k in sorted(cnt): print(k, cnt[k], ex[k])
