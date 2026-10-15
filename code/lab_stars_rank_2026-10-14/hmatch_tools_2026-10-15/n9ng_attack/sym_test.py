"""(SYM): ker T_S invariant under the formal letter swaps iota_l = (0 1) and iota_m = (2 3) (label permutations).
By the sign lemma (E(x +- g x) = -x^T Delta_g x / 4 for x in ker, Delta_g = g Gamma g^-1 - Gamma), for a T-PSD block
(SYM, m) <=> x^T Delta_m x = 0 on ker T_S <=> ODDCONST(m) + C4DO + 'x(02)-x(03) = x(2y)-x(3y)'.
usage: python sym_test.py <glob> [...]"""
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
    res = []
    for sw in ({0: 1, 1: 0}, {2: 3, 3: 2}):
        p = [idx[frozenset(sw.get(y, y) for y in s)] for s in S]
        gN = N[p, :]
        resid = gN - N @ (N.T @ gN)
        res.append(bool(np.max(np.abs(resid)) < 1e-6) if N.shape[1] else True)
    k = ("T>=0" if tpsd else "Tnot", "grid" if grid else "nogrid", "SYM l %s m %s" % tuple(res))
    cnt[k] += 1; ex.setdefault(k, (f, N.shape[1]))
for k in sorted(cnt): print(k, cnt[k], ex[k])
