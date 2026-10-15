"""Even residual R of the m-side over the l-side (LAB 15/10/2026 night, (N9-NG) in the h-invariant case).
Even orbit sums u_y = 1_0y + 1_1y, g_y = 1_2y + 1_3y (y outer), p = 1_02 + 1_13, q = 1_03 + 1_12; A = their Gram under
T.  V_l = span(u, p, q), V_m = span(g, p, q).  R = A_gg - A_gL A_LL^+ A_Lg (10 x 10, outer letters): rank R = even gain
e_l of the m-even vectors over the l-side (h-invariant structures: odd and even sectors are T-orthogonal).
Prints h-invariance, grid flag, c, rank R, spectrum of R, the part indicators of H_m in ker R, tr R.
usage: python even_residual.py <json> [...]"""
import json, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval
hm = {0: 1, 1: 0, 2: 3, 3: 2}
for f in sys.argv[1:]:
    d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]: G[a, b] = G[b, a] = 1
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    hinv = bool(np.array_equal(G[np.ix_(hp, hp)], G))
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    def vec(pairs):
        v = np.zeros(n)
        for pq in pairs: v[idx[frozenset(pq)]] = 1
        return v
    U = [vec([(0, y), (1, y)]) for y in range(4, 14)]
    Gv = [vec([(2, y), (3, y)]) for y in range(4, 14)]
    p = vec([(0, 2), (1, 3)]); q = vec([(0, 3), (1, 2)])
    L = np.array(U + [p, q]).T; M = np.array(Gv).T
    ALL = L.T @ T @ L; ALg = L.T @ T @ M; Agg = M.T @ T @ M
    R = Agg - ALg.T @ np.linalg.pinv(ALL, rcond=1e-10) @ ALg
    R = (R + R.T) / 2
    w = np.linalg.eigvalsh(R)
    rk = int(np.sum(np.abs(w) > 1e-7))
    cl = 23 - int(np.sum(np.abs(np.linalg.eigvalsh(T[np.ix_([i for i in range(n) if S[i] & {0, 1}], [i for i in range(n) if S[i] & {0, 1}])])) > 1e-7))
    cm = 23 - int(np.sum(np.abs(np.linalg.eigvalsh(T[np.ix_([i for i in range(n) if S[i] & {2, 3}], [i for i in range(n) if S[i] & {2, 3}])])) > 1e-7))
    print("%s: h-inv %s, %s, c = (%d,%d), rank R = %d, tr R = %.4f, nonzero spectrum %s"
          % (f, hinv, "grid" if grid else "no grid", cl, cm, rk, np.trace(R), np.round(w[np.abs(w) > 1e-7], 4)))
