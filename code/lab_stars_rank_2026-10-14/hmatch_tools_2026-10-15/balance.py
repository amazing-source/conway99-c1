"""Balance sheet of the four-star rank (LAB 15/10/2026, mechanism of the 13-wall for (H-MATCH)).

For side l (base X_l = labels meeting {0,1}; odd f_y = 1_{2y} - 1_{3y}; even g_y = 1_{2y} + 1_{3y}, y = 4..13) and
symmetrically side m (base X_m; odd 1_{0y} - 1_{1y}; even 1_{0y} + 1_{1y}):
    rank T = rank T_X + (odd gain) + (even gain),   nullity = 44 - rank T = 12 + c - e when the odd gain is 9,
with c = 23 - rank T_X.  Exact ranks (integer Gram matrices of 8T).  Per outer letter y: transversal of the OTHER line
at y (z_2y ~ z_3y for side l; z_0y ~ z_1y for side m), individual absorption of the even vector (rank gain 0 over
base + odd), and its residual T-norm (numerical Schur complement; 0 iff absorbed, for PSD T).
usage: python balance.py <json> [...]"""
import json
import sys

import numpy as np

sys.path.insert(0, '.')
from stars_rank import kval
from z5_enum import exact_rank


def gram_rank(M8, cols):
    B = np.array(cols, dtype=np.int64).T
    return exact_rank((B.T @ M8 @ B).tolist())


def side(S, idx, G, M8, T, a, a2, b, b2):
    n = len(S)
    base = []
    for i in range(n):
        if S[i] & {a, a2}:
            v = np.zeros(n, dtype=np.int64)
            v[i] = 1
            base.append(v)
    odd, even, tr = [], [], []
    for y in range(4, 14):
        p, q = idx[frozenset((b, y))], idx[frozenset((b2, y))]
        o = np.zeros(n, dtype=np.int64)
        o[p], o[q] = 1, -1
        g = np.zeros(n, dtype=np.int64)
        g[p], g[q] = 1, 1
        odd.append(o)
        even.append(g)
        tr.append(int(G[p, q]))
    r0 = gram_rank(M8, base)
    r1 = gram_rank(M8, base + odd)
    r2 = gram_rank(M8, base + odd + even)
    c = 23 - r0
    per = []
    Bm = np.array(base + odd, dtype=float).T
    GB = Bm.T @ T @ Bm
    GBp = np.linalg.pinv(GB, rcond=1e-10)
    for k, g in enumerate(even):
        absorbed = gram_rank(M8, base + odd + [g]) == r1
        gf = g.astype(float)
        cvec = Bm.T @ (T @ gf)
        resid = float(gf @ T @ gf - cvec @ GBp @ cvec)
        per.append((4 + k, tr[k], absorbed, resid))
    return c, r1 - r0, r2 - r1, r2, per


def main():
    for f in sys.argv[1:]:
        d = json.load(open(f))
        S = [frozenset(l) for l in d["labels"]]
        n = len(S)
        idx = {s: i for i, s in enumerate(S)}
        G = np.zeros((n, n), dtype=np.int64)
        for i, j in d["edges"]:
            G[i, j] = G[j, i] = 1
        K8 = np.rint(8 * np.array([[kval(x, y) for y in S] for x in S])).astype(np.int64)
        M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
        T = M8 / 8.0
        print("== %s" % f)
        for name, (a, a2, b, b2) in (("l", (0, 1, 2, 3)), ("m", (2, 3, 0, 1))):
            c, og, eg, rk, per = side(S, idx, G, M8, T, a, a2, b, b2)
            print("  side %s: c = %d, odd gain %d, even gain %d, rank %d, nullity %d (12 + c - e = %d)"
                  % (name, c, og, eg, rk, n - rk, 12 + c - eg))
            print("    y: transversal/absorbed/residual  " + "  ".join("%d:%d/%s/%.3f" % (y, t, "A" if ab else "-", r)
                                                            for y, t, ab, r in per))


if __name__ == "__main__":
    main()
