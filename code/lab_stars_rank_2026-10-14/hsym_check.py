"""Symmetry and square class of saved four-star structures (LAB 15/10/2026, SQ30 test outside the h-symmetric family).
For each json (labels, edges): exact PSD/rank of 8T (symmetric pivoting), invariance under h = (0 1)(2 3) and under the
Z5 rotation of the outer lines, c(l), c(m), and the square class of the non-zero part of 8T (sign, odd-exponent primes).
usage: python hsym_check.py <json> [...]"""
import json
import sys

import numpy as np

from stars_rank import kval
from disc_scan import sym_pivot_det, small_odd_primes
from z5_enum import exact_rank


def perm_of(S, mp):
    idx = {s: i for i, s in enumerate(S)}
    return [idx[frozenset(mp.get(y, y) for y in s)] for s in S]


def main():
    hm = {0: 1, 1: 0, 2: 3, 3: 2}
    z5 = {4: 6, 6: 8, 8: 10, 10: 12, 12: 4, 5: 7, 7: 9, 9: 11, 11: 13, 13: 5}
    for f in sys.argv[1:]:
        d = json.load(open(f))
        S = [frozenset(l) for l in d["labels"]]
        n = len(S)
        G = np.zeros((n, n), dtype=np.int64)
        for i, j in d["edges"]:
            G[i, j] = G[j, i] = 1
        K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
        M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
        hp, zp = perm_of(S, hm), perm_of(S, z5)
        hasym = int(np.abs(G[np.ix_(hp, hp)] - G).sum()) // 2
        zasym = int(np.abs(G[np.ix_(zp, zp)] - G).sum()) // 2
        Xl = [i for i in range(n) if S[i] & {0, 1}]
        Xm = [i for i in range(n) if S[i] & {2, 3}]
        cl = 23 - exact_rank([[int(M8[i][j]) for j in Xl] for i in Xl])
        cm = 23 - exact_rank([[int(M8[i][j]) for j in Xm] for i in Xm])
        r, det, _ = sym_pivot_det(M8.tolist())
        if r is None:
            print("%s: T NOT PSD (exact) | h-asym %d, Z5-asym %d, c = (%d,%d)" % (f, hasym, zasym, cl, cm), flush=True)
            continue
        oddp, cof = small_odd_primes(int(det))
        print("%s: T PSD rank %d | h-asym %d, Z5-asym %d, c = (%d,%d) | det(8T_I) odd-exponent primes %s, cofactor %s"
              % (f, r, hasym, zasym, cl, cm, oddp, "square" if int(cof ** 0.5 + 0.5) ** 2 == cof else cof), flush=True)


if __name__ == "__main__":
    main()
