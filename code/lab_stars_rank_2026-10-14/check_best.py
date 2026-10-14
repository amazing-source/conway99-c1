"""Exact rank, c(l) and spectrum summary of saved three-star structures (14/10/2026).
usage: python check_best.py <json files with 'labels' and 'gamma'>"""
import json
import sys
import numpy as np
from stars_rank import kval
from z5_enum import exact_rank

for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    G = np.array(d["gamma"], dtype=float)
    T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    M8 = [[int(round(8 * T[i][j])) for j in range(n)] for i in range(n)]
    r = exact_rank(M8)
    X = [i for i in range(n) if 0 in S[i] or 1 in S[i]]
    c = 23 - exact_rank([[M8[i][j] for j in X] for i in X])
    ev = np.sort(np.linalg.eigvalsh(T))
    small = sorted(np.abs(ev))[:5]
    print("%s: exact rank %d, c(l) = %d, lambda_min %.4f, smallest |eigenvalues| %s"
          % (f, r, c, ev[0], ["%.2e" % x for x in small]), flush=True)
