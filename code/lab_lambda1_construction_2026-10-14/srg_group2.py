"""Faster exact automorphism groups for strongly regular graphs with lambda = 1 (14/10/2026).
Initial pair colours (isomorphism invariants): adjacency, and for a non-adjacent pair the number of edges inside its
mu-graph (the subgraph induced on the common neighbours); for an adjacent pair the number of lines "parallel" to its
line through the pair's vertices is not needed here. Then 2-dim WL (aut_tools.wl2), individualisation-refinement and
an orbit-stabiliser chain (as in aut_tools.aut_group), every automorphism checked edge by edge.
usage: python srg_group2.py file1.edges [...]   (prints |Aut|, basic orbits, vertex orbits, time)"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "spreadfree_243_2026-10-12"))
import aut_tools as T


def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E)
    A = np.zeros((n, n), dtype=np.int64)
    for a, b in E:
        A[a, b] = A[b, a] = 1
    return A


def init_colours(A):
    n = len(A)
    Af = A.astype(np.float64)
    E = np.zeros((n, n), dtype=np.int64)
    for u in range(n):
        X = Af[u] * Af                       # row w: indicator of the common neighbours of u and w
        E[u] = np.rint(0.5 * np.einsum("ij,ij->i", X @ Af, X)).astype(np.int64)
    C = A + 2 * np.eye(n, dtype=np.int64) + 4 * (E + 1) * (1 - A) * (1 - np.eye(n, dtype=np.int64))
    _, inv = np.unique(C, return_inverse=True)
    return inv.reshape(n, n).astype(np.int64), E


def aut_group(A, Cinit):
    n = len(A)
    C = T.wl2([A], [Cinit])[0]
    Cs = (C, C)
    base, order, sizes, gens = [], 1, [], []
    while True:
        col = np.diag(C).copy()
        for b in base:
            col = T.joint(col, C[b], col, C[b])[0]
        col = T.refine2(A, col, A, col.copy())[0]
        cnt = np.bincount(col)
        if len(cnt) == n:
            break
        big = np.nonzero(cnt > 1)[0]
        c = big[np.argmin(cnt[big])]
        cell = [int(v) for v in np.nonzero(col == c)[0]]
        x = cell[0]
        level, orb = [], {x}
        for y in cell:
            if y in orb:
                continue
            f = T.find_iso(A, A, [(b, b) for b in base] + [(x, y)], Cs)
            if f is not None:
                level.append(f)
                gens.append(f)
                orb.add(y)
                changed = True
                while changed:
                    changed = False
                    for g in level:
                        for v in list(orb):
                            if g[v] not in orb:
                                orb.add(g[v])
                                changed = True
        order *= len(orb)
        sizes.append(len(orb))
        base.append(x)
    return order, sizes, gens


if __name__ == "__main__":
    for p in sys.argv[1:]:
        A = load(p)
        t = time.time()
        Cinit, E = init_colours(A)
        vals = {}
        for u in range(len(A)):
            for w in range(u + 1, len(A)):
                if not A[u, w]:
                    vals[int(E[u, w])] = vals.get(int(E[u, w]), 0) + 1
        o, sizes, gens = aut_group(A, Cinit)
        orbs = T.vertex_orbits(len(A), gens)
        print("%s: mu-graph edge counts over non-adjacent pairs %s; |Aut| = %d (basic orbits %s); vertex orbits %s (%.0f s)"
              % (os.path.basename(p), dict(sorted(vals.items())), o, sizes, sorted(len(x) for x in orbs),
                 time.time() - t), flush=True)
