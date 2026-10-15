"""Sector nullities of four-star structures invariant under commuting involutions (h = (0 1)(2 3), f = (0 1)M):
nullity of T restricted to each joint eigenspace (exact ranks via numpy SVD with tolerance; small sizes).
usage: python sector_nullity.py <json> [...]"""
import json, sys, glob
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
M = {y: y ^ 1 for y in range(4, 14)}
GENS = {"h": {0: 1, 1: 0, 2: 3, 3: 2}, "f01": {**{0: 1, 1: 0}, **M}, "f23": {**{2: 3, 3: 2}, **M}}
def act(g, s): return frozenset(g.get(y, y) for y in s)
for f in sys.argv[1:]:
    d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]: G[a, b] = G[b, a] = 1
    inv = {}
    P = {}
    for k, g in GENS.items():
        p = [idx[act(g, s)] for s in S]
        inv[k] = bool(np.array_equal(G[np.ix_(p, p)], G))
        Pm = np.zeros((n, n))
        for i, j in enumerate(p): Pm[j, i] = 1
        P[k] = Pm
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    out = "%s: nu %d %s inv %s" % (f, nu, "grid" if grid else "nogrid", "".join(k + ("+" if v else "-") + " " for k, v in inv.items()))
    if inv["h"] and inv["f01"]:
        for sh in (1, -1):
            for sf in (1, -1):
                Pr = (np.eye(n) + sh * P["h"]) @ (np.eye(n) + sf * P["f01"]) / 4
                U, s, _ = np.linalg.svd(Pr); B = U[:, s > 0.5]
                w = np.linalg.eigvalsh(B.T @ T @ B)
                out += " [h%s f%s: dim %d null %d]" % ("+" if sh > 0 else "-", "+" if sf > 0 else "-", B.shape[1], int(np.sum(np.abs(w) < 1e-7)))
    print(out)
