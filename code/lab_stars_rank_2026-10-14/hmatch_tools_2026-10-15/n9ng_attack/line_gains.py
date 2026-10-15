"""Gain of the m-side blocks C_mn (labels 2y,2y',3y,3y' of an outer line n) over V_X (+ earlier blocks), per order.
Also: which outer lines are grids with l / with m, and the parts of H_l, H_m.
usage: python line_gains.py <json> [...]"""
import json, sys, itertools
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
LINES = [(4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]
def rk(M): 
    if M.shape[0] == 0: return 0
    w = np.linalg.eigvalsh(M); return int(np.sum(w > 1e-7))
for f in sys.argv[1:]:
    d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]: G[a, b] = G[b, a] = 1
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    def isgrid(a, b, ln):
        y, z = ln
        return all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((a, y), (a, z)), ((b, y), (b, z)), ((a, y), (b, y)), ((a, z), (b, z))))
    gl = [isgrid(0, 1, ln) for ln in LINES]; gm = [isgrid(2, 3, ln) for ln in LINES]
    X = [i for i in range(n) if S[i] & {0, 1}]
    base = rk(T[np.ix_(X, X)])
    blocks = [[idx[frozenset((s, y))] for s in (2, 3) for y in ln] for ln in LINES]
    nu = n - rk(T)
    res = {}
    for order in itertools.permutations(range(5)):
        cur = list(X); r0 = base; gains = []
        for k in order:
            cur = cur + blocks[k]; r1 = rk(T[np.ix_(cur, cur)]); gains.append(r1 - r0); r0 = r1
        res[order] = gains
    tot = sum(res[(0, 1, 2, 3, 4)])
    # gain of each block alone over V_X, and last-position gains
    alone = [res[o][0] for o in res if True][:0]
    alone = []
    for k in range(5):
        cur = X + blocks[k]; alone.append(rk(T[np.ix_(cur, cur)]) - base)
    last = []
    for k in range(5):
        others = [j for j in range(5) if j != k]
        cur = X + sum((blocks[j] for j in others), []); r1 = rk(T[np.ix_(cur, cur)])
        last.append(tot - (r1 - base))
    print("%s: nu %d gain20 %d | l-grid lines %s m-grid lines %s | alone %s last %s"
          % (f.split('/')[-1], nu, tot, [i for i in range(5) if gl[i]], [i for i in range(5) if gm[i]], alone, last))
