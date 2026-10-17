"""The odd window, read at the prime 2: an EXACT necessary condition for a c = 1 line (exploration, LAB 17/10/2026).
Derivation.  Let W = R^{X_l} + span(f_y) (X_l = 24 labels of l, f_y = 1_{2y} - 1_{3y}, 34 dims).  In a Conway graph
nu(T_S) >= 14, so dim(ker T_S n W) >= 14 + 34 - 44 = 4.  L = ker T_S n Z^W is saturated (intersection of saturated
lattices), of rank >= 4, so reduction mod 2 is injective on L/2L: its image has dimension >= 4.  Every primitive kernel
vector y reduces to a vector of the 2-adic radical, in label space {w in W36 : (Gamma - F) w in Z8} (c1_sat2adic_v2.py,
validated 150/150), and y in Z^W gives w_{2v} = w_{3v} for every v.  The known kernel vectors z_0, z_1, z_2 - z_3 reduce
to z_0, z_1, z_2 + z_3 (pivots 04, 14, 24).  HENCE, for c(l) = 1 (and for any c), Conway needs
   (*)  some w in F_2^44, w_{04} = w_{14} = w_{24} = 0, w != 0, w_{2v} = w_{3v} (v = 4..13), w in W36, (Gamma - F) w in Z8.
No size bound on the kernel vector is used.  For c(l) >= 2 the component vectors of l satisfy (*) automatically.
This script: for fixed structures, the dimension of the space of such w (F_2 linear algebra), on c = 1 data sides
(positive or not) and on the rank-30 objects (c >= 2), as a calibration of the strength of (*).
usage: python c1_window2.py <distinct cache.jsonl> [max sides]"""
import itertools
import json
import os
import sys
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c1_sv1_cuts as C  # noqa: E402
import c1_rank2adic as R2  # noqa: E402
from c1_sat2adic_v2 import Z8, FM  # noqa: E402
from gg_test import orient, line_graph, components  # noqa: E402

n = C.n
PIV = [C.IDX[frozenset((s, 4))] for s in (0, 1, 2)]
PAIRQ = [(C.IDX[frozenset((2, y))], C.IDX[frozenset((3, y))]) for y in range(4, 14)]


def nullity2(rows, ncols):
    A = [list(map(int, r)) for r in np.array(rows, dtype=np.int64) % 2]
    return ncols - R2.rank2(np.array(A)) if A else ncols


def window_dim(G):
    """dimension of {(w, p) : constraints} projected to w (p is determined by w when it exists); we compute the
    dimension of the solution space in (w, p) and subtract the dimension of solutions with w = 0 (p in ker Z8^t = 0)."""
    # unknowns: w (44) then p (8)
    rows = []
    # (Gamma - F) w + Z^t p = 0  (44 rows)
    M = (G - FM) % 2
    for i in range(n):
        rows.append(list(M[i]) + [int(Z8[t][i]) for t in range(len(Z8))])
    # w in W36: z . w = 0
    for z in Z8:
        rows.append(list(z) + [0] * len(Z8))
    # pairs w_{2v} = w_{3v}
    for a, b in PAIRQ:
        r = [0] * (n + len(Z8))
        r[a] = r[b] = 1
        rows.append(r)
    # pivots zero
    for pv in PIV:
        r = [0] * (n + len(Z8))
        r[pv] = 1
        rows.append(r)
    return nullity2(rows, n + len(Z8))


def main():
    maxs = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    stats = Counter()
    seen = 0
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        for side in (0, 1):
            L, EE = orient(S0, d["edges"], side)
            V, pos, A = line_graph(L, EE)
            if not all(sum(r) == 3 for r in A):
                continue
            c = components(A)
            G = np.zeros((n, n), dtype=np.int64)
            for i, j in C.PAIRS:
                if frozenset((C.S[i], C.S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            T8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - C.K8
            psd = bool(np.linalg.eigvalsh(T8 / 8.0)[0] >= -1e-9)
            nu = n - np.linalg.matrix_rank(T8.astype(float), tol=1e-6)
            wd = window_dim(G)
            stats[(min(c, 2), psd, wd)] += 1
            seen += 1
        if seen >= maxs:
            break
    print("(c(l) = 1 or >= 2, positive, dim of the window space (*) [Conway needs >= 1]): count")
    for k, v in sorted(stats.items()):
        print("   ", k, v)
    # rank-30 objects
    d = json.load(open(os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14", "rank30_psd_objects_2026-10-15.json")))
    lab = [frozenset(x) for x in d["labels"]]
    st2 = Counter()
    for s in d["structures"][:120]:
        G = np.zeros((n, n), dtype=np.int64)
        for a, b in s["edges"]:
            i, j = C.IDX[lab[a]], C.IDX[lab[b]]
            G[i, j] = G[j, i] = 1
        st2[window_dim(G)] += 1
    print("rank-30 objects (c >= 2), window dimension: count", dict(sorted(st2.items())))


if __name__ == "__main__":
    main()
