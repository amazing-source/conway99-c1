"""Skeleton-guided grid covers of K_{9,9,9}.
A skeleton assigns to every triangle (A,B,C) of the quotient the number of transversal lines over it: 9 ('full'),
3, or 0.  Given the skeleton, the holonomy constraints are
   full : sigma_BC o sigma_AB = sigma_AC (on all 9 points);
   3    : exactly 3 points a with sigma_BC(sigma_AB(a)) = sigma_AC(a);
   0    : no such point.
They are consequences of lambda = 1, mu = 2 once the skeleton is known, and they make propagation much stronger.
The full srg conditions are imposed as well (block_model), so every solution is an srg(243,22,1,2).
Library: build(skel) where skel maps sorted cell triples (i,j,k) (one cell per part) to 9 or 3; absent = 0."""
import itertools, numpy as np
from ortools.sat.python import cp_model
from regluing import block_model
from gridgauge import add_gauge

STD = np.zeros((9, 9), dtype=np.int64)
for a in range(9):
    for b in range(9):
        if a != b and (a // 3 == b // 3 or a % 3 == b % 3): STD[a, b] = 1


def build(skel, with_srg=True):
    n = 243
    cells = [list(range(9 * i, 9 * i + 9)) for i in range(27)]
    part = [i // 9 for i in range(27)]
    G = np.zeros((n, n), dtype=np.int64)
    for c in cells: G[np.ix_(c, c)] = STD
    free = [(i, j) for i in range(27) for j in range(i + 1, 27) if part[i] != part[j]]
    m, var, nc = block_model(G, cells, free, k=22, lam=1, mu=2, forbid_original=False) if with_srg else (None, None, 0)
    ref = {j: 0 for j in range(9, 27)}; ref.update({j: 9 for j in range(1, 9)})
    add_gauge(m, var, cells, ref)
    X = lambda i, j, a, b: var[(cells[i][a], cells[j][b])]
    AND = m._and
    def common(x, y, z):          # existing AND(edge x-z, edge z-y) from block_model
        u, v = var[(x, z)], var[(z, y)]
        return AND[(min(u.Index(), v.Index()), max(u.Index(), v.Index()))]
    for (i, j, k) in itertools.product(range(9), range(9, 18), range(18, 27)):
        L = skel.get((i, j, k), 0)
        clos = []
        for a in range(9):
            x = cells[i][a]; terms = []
            for b in range(9):
                y = cells[j][b]
                w = m.NewBoolVar("")
                m.AddMaxEquality(w, [common(x, y, cells[k][c]) for c in range(9)])
                t = m.NewBoolVar(""); u = X(i, j, a, b)
                m.AddImplication(t, u); m.AddImplication(t, w); m.AddBoolOr([u.Not(), w.Not(), t]); terms.append(t)
            clos.append(sum(terms))
        m.Add(sum(clos) == L)
    return m, var, G, cells


def skeleton_of(G, part):
    """skeleton of a known graph in a given grid partition (cells reordered by part)."""
    import collections
    from lib243 import triangles
    cell = {p: i for i, g in enumerate(part) for p in g}
    cnt = collections.Counter()
    for t in triangles(G):
        cs = tuple(sorted(cell[p] for p in t))
        if len(set(cs)) == 3: cnt[cs] += 1
    return dict(cnt)
