"""ODD9 at c(l) = 1 as the non-vanishing of ONE integer determinant (exploration, LAB 17/10/2026).
A = P^t (8 T_S) P, P = [unit columns of the 24 labels of l | the 10 odd vectors f_y = 1_{2y} - 1_{3y}] (44 x 34).
ker A contains z_0, z_1 (on l) and z_2 - z_3 (cross labels of l + sum of the f_y); restricted to the coordinates
{04, 14, f_4} these three are the identity.  Hence, if rank A = 31 (ODD9 and c(l) = 1), the principal minor A' on the
31 other coordinates is NONSINGULAR, and conversely det A' != 0 => rank A >= 31 => odd gain 9 (rank T_l = 22 at c = 1).
So  ODD9 at c(l) = 1  <=>  det A' != 0  (an integer).  A' = -K' + 8 X' with K' fixed (from K8) and X' = P^t(3I - Gamma)P:
A' is constant modulo 8.  This script reports, for c = 1 structures (positive data sides and walk structures), the
2-adic valuations of the invariant factors of A' (local Smith form, exact) and of the fixed K'.
usage: python c1_odd9_det.py <distinct cache.jsonl> [structure json ...]"""
import itertools
import json
import os
import sys
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import kval, LABELS  # noqa: E402
from gg_test import orient, line_graph, components  # noqa: E402
import c1_rank2adic as R2  # noqa: E402

S = [l for l in LABELS if l & {0, 1, 2, 3}]
IDX = {l: i for i, l in enumerate(S)}
n = len(S)
XL = [i for i, l in enumerate(S) if l & {0, 1}]
QQ = [i for i, l in enumerate(S) if not (l & {0, 1})]
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
P = np.zeros((n, 34), dtype=np.int64)
for a, i in enumerate(XL):
    P[i, a] = 1
for k, y in enumerate(range(4, 14)):
    P[IDX[frozenset((2, y))], 24 + k] = 1
    P[IDX[frozenset((3, y))], 24 + k] = -1
drop = [XL.index(IDX[frozenset((0, 4))]), XL.index(IDX[frozenset((1, 4))]), 24]
keep = [c for c in range(34) if c not in drop]


def val_profile(M):
    _, _, d = R2.smith2(M.tolist())
    c = Counter(R2.v2(x) if x else None for x in d)
    return c


def A_prime(G):
    T8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    A = P.T @ T8 @ P
    return A[np.ix_(keep, keep)]


def main():
    Kp = (P.T @ K8 @ P)[np.ix_(keep, keep)]
    print("fixed K' (31 x 31): 2-adic valuations of invariant factors:", dict(sorted(val_profile(Kp).items(), key=lambda t: (t[0] is None, t[0]))))
    prof = Counter()
    nz = 0
    tot = 0
    structs = []
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        for side in (0, 1):
            L, EE = orient(S0, d["edges"], side)
            V, pos, A = line_graph(L, EE)
            if not all(sum(r) == 3 for r in A) or components(A) != 1:
                continue
            G = np.zeros((n, n), dtype=np.int64)
            for i, j in itertools.combinations(range(n), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            structs.append(("data", G))
        if len(structs) >= 120:
            break
    for fn in sys.argv[2:]:
        dd = json.load(open(fn))
        lab = [frozenset(x) for x in dd["labels"]]
        G = np.zeros((n, n), dtype=np.int64)
        for i, j in dd["edges"]:
            a, b = IDX[lab[i]], IDX[lab[j]]
            G[a, b] = G[b, a] = 1
        structs.append((os.path.basename(fn), G))
    for name, G in structs:
        Ap = A_prime(G)
        c = val_profile(Ap)
        tot += 1
        if c.get(None, 0) == 0:
            nz += 1
        key = tuple(sorted(((k if k is not None else 99), v) for k, v in c.items()))
        prof[key] += 1
        if name != "data":
            v = sum((k if k is not None else 0) * m for k, m in c.items())
            print("  %s: valuations %s, det A' %s" % (name, dict(c), "= 0" if c.get(None, 0) else "!= 0 (v2 = %d)" % v))
    print("c = 1 structures: %d, det A' != 0 for %d" % (tot, nz))
    print("profiles (valuation: count, 99 = zero):")
    for k, v in prof.most_common(12):
        print("   ", dict(k), v)


if __name__ == "__main__":
    main()
