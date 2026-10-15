"""Which structures test the laws non-trivially: no symmetry among h, f01, f23, (0 1), (2 3) and their products,
and mixed relations present (nu > side count).  For those: C4DO, ODDCONST, EVEN' (dim P0 <= 7).
usage: python asym_law_test.py <glob> [...]"""
import glob, json, sys, itertools
from collections import Counter
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
M = {y: y ^ 1 for y in range(4, 14)}
GEN = [{0: 1, 1: 0, 2: 3, 3: 2}, {0: 1, 1: 0, **M}, {2: 3, 3: 2, **M}, {0: 1, 1: 0}, {2: 3, 3: 2}, {0: 1, 1: 0, 2: 3, 3: 2, **M}, M]
files = []
for g in sys.argv[1:]: files += sorted(glob.glob(g))
seen = set(); cnt = Counter(); ex = {}
def rk(A, tol=1e-7):
    if A.size == 0: return 0
    return int(np.sum(np.linalg.svd(A, compute_uv=False) > tol))
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
    sym = False
    for g in GEN:
        p = [idx[frozenset(g.get(y, y) for y in s)] for s in S]
        if np.array_equal(G[np.ix_(p, p)], G): sym = True; break
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    w_, V = np.linalg.eigh(T); N = V[:, np.abs(w_) < 1e-7]; nu = N.shape[1]
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    tpsd = np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] > -1e-9
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    def side(st):
        lab = [i for i in range(n) if S[i] & set(st)]
        return int(np.sum(np.abs(np.linalg.eigvalsh(T[np.ix_(lab, lab)])) < 1e-7))
    nl, nm = side((0, 1)), side((2, 3))
    sidecount = nl + nm - (1 if grid else 0)
    mixed = nu - sidecount
    OUT = range(4, 14)
    c4 = N[idx[frozenset((0, 2))]] - N[idx[frozenset((0, 3))]] - N[idx[frozenset((1, 2))]] + N[idx[frozenset((1, 3))]]
    c4ok = (np.max(np.abs(c4)) < 1e-6) if nu else True
    oc = []
    for (a, b) in ((2, 3), (0, 1)):
        D = np.array([N[idx[frozenset((a, y))]] - N[idx[frozenset((b, y))]] for y in OUT])
        oc.append(rk(D - D.mean(axis=0, keepdims=True)) == 0)
    k = ("sym" if sym else "nosym", "T>=0" if tpsd else "Tnot", "grid" if grid else "nogrid", "mixed>0" if mixed > 0 else "mixed=0",
         "C4DO %s ODDCONST %s/%s" % (c4ok, oc[0], oc[1]))
    cnt[k] += 1; ex.setdefault(k, (f, nu, mixed))
for k in sorted(cnt): print(k, cnt[k], ex[k])
