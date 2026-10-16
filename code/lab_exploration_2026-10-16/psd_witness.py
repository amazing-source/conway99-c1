"""T and 7I - T on a label set of a structure (exploration, LAB 16/10/2026).
T = 3I - Gamma - K with K_xy = (3|x n y| + m_xy - 2)/8 (m_xy = number of mate relations between the letters of x and
y), the Schur complement of 3I - A over the root and its 14 letters.  In a Conway graph T on all 84 labels equals 7P (P a
projector of rank 30), so every principal submatrix has eigenvalues in [0, 7] and rank <= 30.
Prints lambda_min(T), lambda_max(T), rank (tolerance 1e-7) and, if T is not PSD, an integer-rounded negative direction.
usage: python psd_witness.py <structure json (labels, edges)> [...]"""
import itertools
import json
import sys

import numpy as np

MATE = lambda i: i ^ 1
for path in sys.argv[1:]:
    d = json.load(open(path))
    L = [frozenset(x) for x in d["labels"]]
    n = len(L)
    G = np.zeros((n, n))
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    Kmat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a, b = L[i], L[j]
            s = len(a & b)
            m = sum(1 for p in a for q in b if q == MATE(p))
            Kmat[i, j] = (3 * s + m - 2) / 8.0
    T = 3 * np.eye(n) - G - Kmat
    ev, V = np.linalg.eigh(T)
    rank = int(np.sum(ev > 1e-7))
    print("%s: %d labels, lambda_min(T) %.4f, lambda_max(T) %.4f, rank %d (Conway needs >= 0, <= 7, <= 30)"
          % (path.replace("\\", "/").split("/")[-1], n, ev[0], ev[-1], rank), flush=True)
