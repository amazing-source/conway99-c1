"""How many line graphs G_T are there, and of which kinds (LAB 20/10/2026).  Uniform random triples of bijections
(s01, s12, s20) (ll_test.gt_matrix): fraction with K >= 0 (admissible), number of components, and for connected ones
d = dim ker_7 (3I - G) and the Legendre symbol (tau | 7) when d = 1 (det of the reduced Laplacian mod 7).
Class count: (12!)^3 / ((2^6 6!)^3 * 6) assumes a free action of the relabelling group (partner-preserving
permutations of each class, and S3 on the classes).
usage: python lg_counts.py <samples> <seed>"""
import math
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "reduction_2026-10-19"))
sys.path.insert(0, os.path.join(HERE, "..", "treasure_2026-10-19"))
from ll_test import components, gt_matrix, k_matrix  # noqa: E402
from rank7_line import rank_mod  # noqa: E402

n, N = 12, 36


def det_mod7(L):
    m = [[int(v) % 7 for v in row] for row in L]
    k, det = len(m), 1
    for c in range(k):
        p = next((r for r in range(c, k) if m[r][c]), None)
        if p is None:
            return 0
        if p != c:
            m[c], m[p] = m[p], m[c]
            det = -det
        det = det * m[c][c] % 7
        inv = pow(m[c][c], 5, 7)
        for r in range(c + 1, k):
            f = m[r][c] * inv % 7
            if f:
                m[r] = [(a - f * b) % 7 for a, b in zip(m[r], m[c])]
    return det % 7


def main():
    T, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    adm, comps, ds, leg = 0, {}, {}, {1: 0, -1: 0}
    for _ in range(T):
        s01, s12, s20 = (rng.sample(range(n), n) for _ in range(3))
        G = gt_matrix(n, s01, s12, s20)
        if (k_matrix(n, G) < 0).any():
            continue
        adm += 1
        nc, _ = components(G)
        comps[nc] = comps.get(nc, 0) + 1
        if nc != 1:
            continue
        L = (3 * np.eye(N, dtype=np.int64) - G) % 7
        d = N - rank_mod(L, 7)
        ds[d] = ds.get(d, 0) + 1
        if d == 1:
            t = det_mod7(L[1:, 1:])
            leg[1 if pow(t, 3, 7) == 1 else -1] += 1
    classes = math.factorial(12) ** 3 / ((2 ** 6 * math.factorial(6)) ** 3 * 6)
    print("samples %d, admissible %d (%.4f), components %s" % (T, adm, adm / T, dict(sorted(comps.items()))))
    print("connected: d distribution %s, (tau|7) for d = 1: %s" % (dict(sorted(ds.items())), leg))
    print("classes %.3e, admissible %.3e, admissible connected %.3e" % (classes, classes * adm / T,
                                                                       classes * comps.get(1, 0) / T))


if __name__ == "__main__":
    main()
