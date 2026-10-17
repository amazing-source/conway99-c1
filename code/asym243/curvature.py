"""Curvature of a 3-cover of BH: for every 3x3 grid of BH (405 of them), the holonomy (a permutation of the fibre)
around its elementary squares.  Prediction: #grids(Gamma) = 270 + 3 * #flat grids of BH."""
import sys, itertools, collections, numpy as np
from lib243 import *
from cover import fibres_of, is_cover

def matching(G, fib, P, R):
    return {a: fib[R][int(np.nonzero(G[a, fib[R]])[0][0])] for a in fib[P]}

def bh_grids(Q):
    n = len(Q); nb = [set(np.nonzero(Q[P])[0].tolist()) for P in range(n)]
    lines = set()
    for P in range(n):
        for R in nb[P]:
            for S in nb[P] & nb[R]: lines.add(frozenset((P, R, S)))
    at = collections.defaultdict(list)
    for l in lines:
        for P in l: at[P].append(l)
    grids = set()
    for P in range(n):
        for l1, l2 in itertools.combinations(at[P], 2):
            a = sorted(l1 - {P}); b = sorted(l2 - {P}); pts = set(l1 | l2); rows = [sorted(l1)]
            ok = True
            for x in a:
                for y in b:
                    c = (nb[x] & nb[y]) - {P}
                    cc = [z for z in c if any(z in l and (x in l or y in l) for l in at[z])]
                    # 4th corner: common neighbour lying on a line with x parallel to l2 ... use grid closure test below
            # closure: points adjacent to both a-row and b-col appropriately
            corner = {}
            for x in a:
                for y in b:
                    c = sorted((nb[x] & nb[y]) - {P})
                    corner[(x, y)] = c
            # choose corners forming lines: try all combinations (each corner set has 5 elements)
            for combo in itertools.product(*[corner[k] for k in sorted(corner)]):
                cs = dict(zip(sorted(corner), combo))
                (x0, x1), (y0, y1) = a, b
                if Q[cs[(x0, y0)], cs[(x0, y1)]] and Q[cs[(x1, y0)], cs[(x1, y1)]] and Q[cs[(x0, y0)], cs[(x1, y0)]] and Q[cs[(x0, y1)], cs[(x1, y1)]] \
                   and Q[x0, cs[(x0, y0)]] and Q[x0, cs[(x0, y1)]] and Q[y0, cs[(x0, y0)]] and Q[y0, cs[(x1, y0)]]:
                    g = pts | set(cs.values())
                    if len(g) == 9 and Q[np.ix_(sorted(g), sorted(g))].sum() == 36:
                        grids.add(frozenset(g)); break
    return sorted(grids, key=sorted), nb

def grid_flat(G, fib, Q, g, nb):
    """flat iff every 4-cycle of the grid (non-adjacent diagonal pairs inside g) has trivial holonomy."""
    g = sorted(g)
    for P in g:
        for R in g:
            if P < R and not Q[P, R]:
                Zs = [Z for Z in g if Q[P, Z] and Q[Z, R]]
                assert len(Zs) == 2
                m1 = matching(G, fib, P, Zs[0]); m2 = matching(G, fib, Zs[0], R)
                m3 = matching(G, fib, P, Zs[1]); m4 = matching(G, fib, Zs[1], R)
                if any(m2[m1[x]] != m4[m3[x]] for x in fib[P]): return False
    return True

if __name__ == "__main__":
    A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
    grids, nb = bh_grids(Q)
    print("BH grids:", len(grids))
    for f in sys.argv[1:]:
        G = np.load(f) if f.endswith(".npy") else load_edges(f)
        okc, _ = is_cover(G, fib)
        flat = sum(1 for g in grids if grid_flat(G, fib, Q, g, nb))
        _, ng = grids_per_vertex(G)
        print(f"{f}: cover={okc} flat BH-grids={flat}  grids(Gamma)={ng}  270+3*flat={270 + 3 * flat}", flush=True)
