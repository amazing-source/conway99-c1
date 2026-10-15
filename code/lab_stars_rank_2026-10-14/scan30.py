"""Batch scan of harvested rank <= 30 PSD four-star structures (LAB 15/10/2026).
For each json: exact rank over Q of 8T_S4, rank over F_7, DISC verdict (rank 30: det(8T_I) = 2 x square required;
robust failure = a prime other than 2, 7 with odd exponent), exact odd gains beyond X_l and X_m (ODD9), c(l), c(m),
and the exact PSD check (symmetric pivots).  Duplicates (same edge set) are skipped.
usage: python scan30.py <json> [...]"""
import json
import math
import sys

import numpy as np

from stars_rank import kval
from z5_enum import exact_rank
from r7_scan import rank_mod
from disc_scan import sym_pivot_det, small_odd_primes
from odd9_check import gain

seen = set()
summary = {}
for f in sys.argv[1:]:
    d = json.load(open(f))
    key = tuple(tuple(e) for e in d["edges"])
    if key in seen:
        continue
    seen.add(key)
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
    M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    r, det, piv = sym_pivot_det(M8.tolist())
    if r is None:
        print("%s: T not PSD (exact)" % f, flush=True)
        continue
    r7 = rank_mod(M8.tolist(), 7)
    odd, cof = small_odd_primes(int(det))
    cof_sq = math.isqrt(cof) ** 2 == cof
    if r == 30:
        disc = "OK" if (odd == [2] and cof_sq) else ("2/7 only" if (all(p in (2, 7) for p in odd) and cof_sq) else
                                                     "FAILS at %s" % [p for p in odd if p not in (2, 7)])
    else:
        disc = "n/a"
    cs, gains = [], []
    for (a, a2, b, b2) in ((0, 1, 2, 3), (2, 3, 0, 1)):
        Xl = [i for i in range(n) if S[i] & {a, a2}]
        cs.append(23 - exact_rank(M8[np.ix_(Xl, Xl)].tolist()))
        oddv = []
        for y in range(4, 14):
            v = np.zeros(n, dtype=np.int64)
            v[idx[frozenset((b, y))]] = 1
            v[idx[frozenset((b2, y))]] = -1
            oddv.append(v)
        gains.append(gain(M8, Xl, oddv))
    k = (r, r7, disc.split(" ")[0], tuple(gains))
    summary[k] = summary.get(k, 0) + 1
    print("%s: rank %d, rank_7 %d, DISC %s, odd gains %s, c %s" % (f, r, r7, disc, gains, cs), flush=True)
print("summary (rank, rank_7, DISC, odd gains): count")
for k, v in sorted(summary.items()):
    print("  ", k, v)
