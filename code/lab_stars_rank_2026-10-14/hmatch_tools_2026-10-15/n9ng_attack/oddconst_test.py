"""(ODDCONST): for every x in ker T_S, x(2y) - x(3y) is the same for all ten outer y, and x(0y) - x(1y) likewise;
(C4DO): x(02) - x(03) - x(12) + x(13) = 0.  Corpus scan by class.  Also records nu, c and the EVEN' profile dimension
dim P0 (kernel vectors with x(2y) = x(3y) on all outer y: dimension of their profiles on the outer labels of star 2).
usage: python oddconst_test.py <glob> [...]"""
import glob, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
files = []
for g in sys.argv[1:]: files += sorted(glob.glob(g))
seen = set(); cnt = Counter(); ex = {}; p0 = Counter()
def rk(M, tol=1e-7):
    if M.size == 0: return 0
    s = np.linalg.svd(M, compute_uv=False); return int(np.sum(s > tol))
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
    w_, V = np.linalg.eigh(T); N = V[:, np.abs(w_) < 1e-7]; nu = N.shape[1]
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    tpsd = np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] > -1e-9
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    OUT = range(4, 14)
    def oddprof(a, b):
        return np.array([N[idx[frozenset((a, y))]] - N[idx[frozenset((b, y))]] for y in OUT])  # 10 x nu
    res = []
    for (a, b) in ((2, 3), (0, 1)):
        D = oddprof(a, b)
        res.append(rk(D - D.mean(axis=0, keepdims=True)) == 0)
    c4 = N[idx[frozenset((0, 2))]] - N[idx[frozenset((0, 3))]] - N[idx[frozenset((1, 2))]] + N[idx[frozenset((1, 3))]]
    c4ok = (np.max(np.abs(c4)) < 1e-6) if nu else True
    k = ("T>=0" if tpsd else "T not psd", "grid" if grid else "nogrid", "ODDCONST m %s l %s C4DO %s" % (res[0], res[1], c4ok))
    cnt[k] += 1; ex.setdefault(k, f)
    if tpsd and not grid:
        # P0: kernel vectors with x(2y) = x(3y) for all outer y -> their star-2 outer profiles
        D = oddprof(2, 3)
        # null space of D (coefficients c with D c = 0)
        u, s, vt = np.linalg.svd(D); r = int(np.sum(s > 1e-7)); C = vt[r:].T
        prof = np.array([N[idx[frozenset((2, y))]] for y in OUT]) @ C
        p0[(nu, rk(prof))] += 1
for k in sorted(cnt): print(k, cnt[k], ex[k])
print("non-grid T>=0: (nu, dim P0 on the m side):", dict(sorted(p0.items())))
