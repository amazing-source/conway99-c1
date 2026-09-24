"""Analyse a near-solution (0/1 symmetric matrix) for srg(99,14,1,2): which conditions fail, and how does the
near-graph look (degrees, lambda/mu violations, lines, prisms P, twisting)."""
import sys, json
from collections import Counter
import numpy as np


def analyse(A, k=14, lam=1, mu=2):
    A = np.asarray(A, dtype=np.int64)
    n = len(A)
    deg = A.sum(1)
    A2 = A @ A
    off = ~np.eye(n, dtype=bool)
    adj = (A == 1) & off
    non = (A == 0) & off
    lam_viol = int(((A2 != lam) & adj).sum() // 2)
    mu_viol = int(((A2 != mu) & non).sum() // 2)
    out = {'n': n, 'degree hist': dict(Counter(deg.tolist())), 'lambda violations (pairs)': lam_viol,
           'mu violations (pairs)': mu_viol,
           'lambda values on edges': dict(Counter(A2[adj].tolist())), 'mu values on non-edges': dict(Counter(A2[non].tolist()))}
    # triangles and prisms
    tri = set()
    nb = [set(np.nonzero(A[i])[0].tolist()) for i in range(n)]
    for u in range(n):
        for v in nb[u]:
            if v > u:
                for w in nb[u] & nb[v]:
                    if w > v:
                        tri.add((u, v, w))
    out['triangles'] = len(tri)
    lines = list(tri)
    P = 0
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            L, M = lines[i], lines[j]
            if set(L) & set(M):
                continue
            e = sum(A[a, b] for a in L for b in M)
            if e == 3 and all(sum(A[a, b] for b in M) == 1 for a in L):
                P += 1
    out['prisms P'] = P
    return out


if __name__ == '__main__':
    A = json.load(open(sys.argv[1]))
    for key, v in analyse(A).items():
        print(f'{key}: {v}')
