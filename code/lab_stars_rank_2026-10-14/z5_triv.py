"""Square class of the Z5-trivial part vs the full det(8T_I) (Hermitian argument check, LAB 15/10/2026).
usage: python z5_triv.py <json> [...]   (structures invariant under (4 6 8 10 12)(5 7 9 11 13))"""
import json, sys

import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval

from disc_scan import sym_pivot_det, small_odd_primes

h = {4: 6, 6: 8, 8: 10, 10: 12, 12: 4, 5: 7, 7: 9, 9: 11, 11: 13, 13: 5, 0: 0, 1: 1, 2: 2, 3: 3}
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
    M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    perm = [idx[frozenset(h[y] for y in s)] for s in S]
    orbs, seen = [], set()
    for i in range(n):
        if i in seen:
            continue
        o, j = [], i
        while j not in o:
            o.append(j)
            j = perm[j]
        seen |= set(o)
        orbs.append(o)
    B = np.zeros((n, len(orbs)), dtype=np.int64)
    for k, o in enumerate(orbs):
        for i in o:
            B[i, k] = 1
    Gt = (B.T @ M8 @ B).tolist()
    r, det, piv = sym_pivot_det(Gt)
    odd, cof = small_odd_primes(int(det))
    rf, detf, _ = sym_pivot_det(M8.tolist())
    oddf, coff = small_odd_primes(int(detf))
    print("%s: trivial part rank %d, det odd primes %s cof %d | full rank %d odd primes %s cof %d"
          % (f, r, odd, cof, rf, oddf, coff))
