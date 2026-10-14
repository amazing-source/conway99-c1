"""Geometric invariants of a strongly regular graph with lambda = 1 (a partial quadrangle with lines of size 3),
used as initial colours for exact automorphism computations (14/10/2026).
For a line L (triangle) and a line M disjoint from L, e(L,M) = number of edges between them (0..3). p_j(L) = number of
lines M with e(L,M) = j (j = 2, 3; e = 3 means M is parallel to L: a prism). All are isomorphism invariants.
Initial pair colours: (adjacent: invariants of the line through the pair; non-adjacent: number of lines through u
parallel to a line through w, and the number of pairs of lines (through u, through w) joined by exactly 2 edges).
usage: python pq_invariants.py file.edges [...]   -> distributions; also importable (pair_colours)"""
import os
import sys
import time

import numpy as np


def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E)
    A = np.zeros((n, n), dtype=np.int64)
    for a, b in E:
        A[a, b] = A[b, a] = 1
    return A


def lines_of(A):
    n = len(A)
    adj = [np.nonzero(A[v])[0] for v in range(n)]
    L = set()
    for a in range(n):
        for b in adj[a]:
            if b > a:
                c = np.nonzero(A[a] & A[b])[0]
                assert len(c) == 1, "lambda != 1"
                L.add(tuple(sorted((a, int(b), int(c[0])))))
    return sorted(L)


def line_stats(A, lines):
    n = len(A)
    nl = len(lines)
    B = np.zeros((nl, n), dtype=np.int64)
    for i, l in enumerate(lines):
        B[i, list(l)] = 1
    D = B @ A                                    # D[M, v] = number of neighbours of v on M
    meet = B @ B.T                               # common points of two lines
    E = D @ B.T                                  # E[M, L] = number of edges between M and L (both directions counted once each)
    p3 = np.zeros(nl, dtype=np.int64)
    p2 = np.zeros(nl, dtype=np.int64)
    for i in range(nl):
        disjoint = meet[:, i] == 0
        par = disjoint.copy()
        for v in lines[i]:
            par &= D[:, v] == 1
        p3[i] = int(par.sum())
        p2[i] = int((disjoint & (E[:, i] == 2)).sum())
    return B, D, E, meet, p3, p2


def pair_colours(A):
    n = len(A)
    lines = lines_of(A)
    B, D, E, meet, p3, p2 = line_stats(A, lines)
    nl = len(lines)
    # parallel-line relation and two-edge relation between lines
    disjoint = meet == 0
    PAR = np.zeros((nl, nl), dtype=np.int64)
    for i in range(nl):
        par = disjoint[:, i].copy()
        for v in lines[i]:
            par &= D[:, v] == 1
        PAR[:, i] = par
    TWO = (disjoint & (E == 2)).astype(np.int64)
    # vertex-level: through u and through w
    Bt = B.T                                     # vertex x line incidence
    parUW = Bt @ PAR @ B                         # number of (line through u, line through w) pairs that are parallel
    twoUW = Bt @ TWO @ B
    lineid = {}
    for i, l in enumerate(lines):
        for a in l:
            for b in l:
                if a != b:
                    lineid[(a, b)] = i
    C = np.zeros((n, n), dtype=np.int64)
    for u in range(n):
        for w in range(n):
            if u == w:
                C[u, w] = 1
            elif A[u, w]:
                i = lineid[(u, w)]
                C[u, w] = 2 + 1000 * int(p3[i]) + 1000000 * int(p2[i])
            else:
                C[u, w] = 3 + 1000 * int(parUW[u, w]) + 1000000 * int(twoUW[u, w])
    vstat = [tuple(sorted(int(p3[i]) for i in np.nonzero(B[:, v])[0])) for v in range(n)]
    _, inv = np.unique(C, return_inverse=True)
    return inv.reshape(n, n).astype(np.int64), lines, p3, p2, vstat


if __name__ == "__main__":
    for p in sys.argv[1:]:
        A = load(p)
        t = time.time()
        C, lines, p3, p2, vstat = pair_colours(A)
        h3, h2 = {}, {}
        for x in p3:
            h3[int(x)] = h3.get(int(x), 0) + 1
        for x in p2:
            h2[int(x)] = h2.get(int(x), 0) + 1
        print("%s: %d lines; parallels per line %s; two-edge partners per line %s; vertex types %d; pair colours %d "
              "(%.0f s)" % (os.path.basename(p), len(lines), dict(sorted(h3.items())), dict(sorted(h2.items())),
                            len(set(vstat)), len(np.unique(C)), time.time() - t), flush=True)
