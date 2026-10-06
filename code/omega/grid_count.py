"""Induced 3x3 grids (rook graph K3 x K3 = Paley9) through each vertex, for srg with lambda=1 (each edge in one triangle).
A grid through x is determined by two triangles T1, T2 at x and must close: count by checking all 9-vertex candidates."""
import numpy as np, sys, itertools
def triangles_at(M, x):
    nb = np.nonzero(M[x])[0]; out = []
    for y in nb:
        for z in np.nonzero(M[y] & M[x])[0]:
            if y < z: out.append((y, z))
    return out
def grids_at(M, x):
    T = triangles_at(M, x); cnt = 0
    for (a, b), (c, d) in itertools.combinations(T, 2):
        # rows {x,a,b}, columns {x,c,d}; need g = the unique vertex completing (a,c),(a,d),(b,c),(b,d)
        def comp(p, q):
            # common neighbours of p,q other than x (p,q non adjacent -> mu=2 common nbrs: x and one more)
            cn = [w for w in np.nonzero(M[p] & M[q])[0] if w != x]
            return cn[0] if len(cn) == 1 else None
        if M[a, c] or M[a, d] or M[b, c] or M[b, d]: continue
        e = [comp(a, c), comp(a, d), comp(b, c), comp(b, d)]
        if None in e: continue
        e1, e2, e3, e4 = e  # grid: a-c->e1, a-d->e2, b-c->e3, b-d->e4 ; need rows/cols triangles
        S = [x, a, b, c, d, e1, e2, e3, e4]
        if len(set(S)) != 9: continue
        sub = M[np.ix_(S, S)]
        if sub.sum() == 36 and (sub.sum(1) == 4).all():
            cnt += 1
    return cnt
if __name__ == "__main__":
    from graphs_test import bvls243
    for name, M in (("BvLS", bvls243()), ("twin", np.load("twin243.npy"))):
        c = [grids_at(M, x) for x in range(243)]
        vals, cn = np.unique(c, return_counts=True)
        print(name, "grids through a vertex: distribution", dict(zip(vals.tolist(), cn.tolist())), " total grids", sum(c) // 9, flush=True)
