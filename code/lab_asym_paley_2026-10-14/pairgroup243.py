"""Common automorphisms Aut(G) n Aut(G') of graphs on one labelled vertex set, for srg(v,k,1,2) on a few hundred
vertices (asymmetry campaign, 14/10/2026). Reuses the 2-dim Weisfeiler-Leman + geometric initial colours of my
aut_tools.py (work/spreadfree_243_2026-10-12), with the pair colour = (colour in G, colour in G') and refinement by
both adjacency matrices; every map returned is checked on BOTH graphs. Hash collisions can only weaken pruning.
Aut(G) n Aut(G') = stabiliser in Aut(G) of the trade G xor G' (law: it lies in Aut(G'); the rest of Aut(G') is
created by the move).
usage: python pairgroup243.py A.edges B.edges [...]   (|Aut| of each, then every pair)
"""
import itertools
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T

RNG = np.random.default_rng(20261014)


def joint(c1, e1, c2, e2):
    n = len(c1)
    _, inv = np.unique(np.concatenate([np.stack([c1, e1], 1), np.stack([c2, e2], 1)]), axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    return inv[:n], inv[n:]


def refine_pair(Ms, col1, col2):
    n = len(col1)
    ncol = len(np.unique(col1))
    while True:
        k = int(max(col1.max(), col2.max())) + 1
        h1 = np.zeros(n, dtype=np.int64)
        h2 = np.zeros(n, dtype=np.int64)
        for M in Ms:
            r = RNG.integers(1, 1 << 40, size=k)
            h1 = h1 * 1000003 + M @ r[col1]
            h2 = h2 * 1000003 + M @ r[col2]
        n1, n2 = joint(col1, h1, col2, h2)
        if not np.array_equal(np.sort(n1), np.sort(n2)):
            return None
        kk = len(np.unique(n1))
        if kk == ncol:
            return n1, n2
        ncol = kk
        col1, col2 = n1, n2


def find_aut(Ms, C, pairs):
    n = len(Ms[0])
    col1 = np.diag(C).copy()
    col2 = col1.copy()
    for (a, b) in pairs:
        if col1[a] != col2[b]:
            return None
        col1, col2 = joint(col1, C[a], col2, C[b])

    def rec(col1, col2):
        r = refine_pair(Ms, col1, col2)
        if r is None:
            return None
        col1, col2 = r
        cnt = np.bincount(col1)
        if len(cnt) == n:
            inv = np.empty(n, dtype=np.int64)
            inv[col2] = np.arange(n)
            f = inv[col1]
            return f.tolist() if all(np.array_equal(M, M[np.ix_(f, f)]) for M in Ms) else None
        big = np.nonzero(cnt > 1)[0]
        c = big[np.argmin(cnt[big])]
        x = int(np.nonzero(col1 == c)[0][0])
        for y in np.nonzero(col2 == c)[0]:
            a1, a2 = joint(col1, C[x], col2, C[int(y)])
            f = rec(a1, a2)
            if f is not None:
                return f
        return None
    return rec(col1, col2)


def common_group(Ms):
    n = len(Ms[0])
    init = None
    for M in Ms:
        g = T.geom_init(M)
        init = g if init is None else init * (1 << 21) + g
    _, inv = np.unique(init, return_inverse=True)
    init = inv.reshape(n, n).astype(np.int64)
    C = T.wl2([Ms[0]], [init])[0]
    base, order, sizes, gens = [], 1, [], []
    while True:
        col = np.diag(C).copy()
        for b in base:
            col = joint(col, C[b], col, C[b])[0]
        col = refine_pair(Ms, col, col.copy())[0]
        cnt = np.bincount(col)
        if len(cnt) == n:
            break
        big = np.nonzero(cnt > 1)[0]
        c = big[np.argmax(cnt[big])]
        cell = [int(v) for v in np.nonzero(col == c)[0]]
        x = cell[0]
        level, orb = [], {x}

        def close():
            changed = True
            while changed:
                changed = False
                for g in level:
                    for v in list(orb):
                        if g[v] not in orb:
                            orb.add(g[v])
                            changed = True
        for y in cell:
            if y in orb:
                continue
            f = find_aut(Ms, C, [(b, b) for b in base] + [(x, y)])
            if f is not None:
                level.append(f)
                gens.append(f)
                orb.add(y)
                close()
        order *= len(orb)
        sizes.append(len(orb))
        base.append(x)
    return order, sizes, gens


def lines(A):
    n = len(A)
    adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
    out = set()
    for a in range(n):
        for b in adj[a]:
            if b > a:
                c = adj[a] & adj[b]
                if len(c) == 1:
                    out.add(tuple(sorted((a, b, c.pop()))))
    return out


if __name__ == "__main__":
    files = sys.argv[1:]
    As = {f: T.load(f) for f in files}
    nm = {f: os.path.basename(f).replace(".edges", "") for f in files}
    for f in files:
        t = time.time()
        o, s, g = common_group([As[f]])
        orbs = T.vertex_orbits(len(As[f]), g)
        print("|Aut(%s)| = %d (basic orbits %s; vertex orbits %s; %.0f s)"
              % (nm[f], o, s, sorted(len(x) for x in orbs), time.time() - t), flush=True)
    for f, g in itertools.combinations(files, 2):
        A, B = As[f], As[g]
        if A.shape != B.shape:
            continue
        diff = int(np.abs(A - B).sum()) // 2
        touched = int((np.abs(A - B).sum(axis=1) > 0).sum())
        LA, LB = lines(A), lines(B)
        t = time.time()
        o, s, gens = common_group([A, B])
        orbs = T.vertex_orbits(len(A), gens)
        print("%s vs %s: %d pairs differ, %d vertices touched, lines only in first %d, only in second %d; "
              "|Aut n Aut'| = %d (basic orbits %s; vertex orbits %s; %.0f s)"
              % (nm[f], nm[g], diff, touched, len(LA - LB), len(LB - LA), o, s, sorted(len(x) for x in orbs),
                 time.time() - t), flush=True)
