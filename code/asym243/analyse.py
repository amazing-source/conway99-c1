"""Structural profile of an srg(243,22,1,2): Aut, orbits, grids, twisting, prisms, hexagons (Reimbayev),
regular spreads (equitable line partitions), and local-to-global symmetry:
for a sample of triangles T, |Aut(ball(T))| (induced subgraph on T and its 60 neighbours) vs |Stab_Aut(G)(T)|."""
import sys, collections, numpy as np
from lib243 import *

H0 = 243 * 22 * 20 * (2 * 22 ** 2 - 21 * 22 + 53) // 12
PMAX = 8910


def load_any(path):
    return np.load(path) if path.endswith(".npy") else load_edges(path)


def regular_spreads_in_parallel_classes(G):
    """which of the 121 affine parallel classes of AG(5,3) are spreads of lines of G forming an equitable partition."""
    from lines_model import PTS, IDX, lines_of_direction, norm_dir
    import itertools
    tri = set(triangles(G))
    out = []
    dirs = sorted({norm_dir(v) for v in itertools.product(range(3), repeat=5) if any(v)})
    for v in dirs:
        Ls = lines_of_direction(v)
        if all(tuple(l) in tri for l in Ls):
            # equitable?
            where = {p: i for i, l in enumerate(Ls) for p in l}
            ok = True
            for l in Ls:
                cnt = collections.Counter(where[q] for p in l for q in np.nonzero(G[p])[0] if where[q] != where[p])
                if any(c not in (3,) for c in cnt.values()):
                    ok = False; break
            out.append((v, ok))
    return out


def ball_aut(G, T):
    ball = sorted(set(T) | set(np.nonzero(G[list(T)].sum(0))[0]))
    sub = G[np.ix_(ball, ball)]
    o, orb, gens = aut(sub)
    return o, len(ball)


def stab_order(G, T, gens_order):
    o, orb, gens = aut(G, partition=[list(T), [x for x in range(len(G)) if x not in T]])
    return o


def profile(G, ntri=6, seed=0):
    rep = {}
    rep["srg"] = is_srg(G)
    o, orb, gens = aut(G)
    rep["aut"] = o; rep["orbits"] = sorted(len(x) for x in orb)
    g, ng = grids_per_vertex(G)
    rep["grids"] = ng; rep["grid_dist"] = sorted(collections.Counter(g.tolist()).items())
    tw, pr = twisted_pairs(G)
    rep["twisted_pairs"] = tw; rep["prisms"] = pr
    rep["hexagons"] = H0 + 3 * (PMAX - pr)
    rep["n3_check"] = (tw == 3 * (PMAX - pr))
    tris = triangles(G)
    rng = np.random.default_rng(seed)
    sample = [tris[i] for i in rng.choice(len(tris), size=min(ntri, len(tris)), replace=False)]
    loc = []
    for T in sample:
        bo, bs = ball_aut(G, T)
        so = stab_order(G, T, o)
        loc.append((T, bo, so))
    rep["local_global"] = loc
    return rep


if __name__ == "__main__":
    for path in sys.argv[1:]:
        G = load_any(path)
        r = profile(G)
        print("==", path)
        for k, v in r.items():
            if k != "local_global": print(f"  {k}: {v}")
        for T, bo, so in r["local_global"]:
            print(f"  triangle {T}: |Aut(ball)| = {bo}, |Stab_Aut(G)(T)| = {so}")
        sp = regular_spreads_in_parallel_classes(G)
        print("  affine parallel classes that are spreads of lines:", len(sp), " equitable:", sum(1 for _, ok in sp if ok))


def local_grid_graph(G, x, tri=None):
    """graph on the 11 lines through x: two lines adjacent iff they span an induced 3x3 grid."""
    if tri is None: tri = triangles(G)
    L = [t for t in tri if x in t]
    M = np.zeros((len(L), len(L)), dtype=np.int64)
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            a = [p for p in L[i] if p != x]; b = [p for p in L[j] if p != x]
            pts = set(L[i]) | set(L[j]); ok = True
            for p in a:
                for q in b:
                    c = set(np.nonzero(G[p] & G[q])[0].tolist()) - {x}
                    if len(c) != 1: ok = False
                    pts |= c
            if ok and len(pts) == 9 and G[np.ix_(sorted(pts), sorted(pts))].sum() == 36:
                M[i, j] = M[j, i] = 1
    return M


def local_vs_global(G, reps):
    tri = triangles(G); out = []
    for x in reps:
        M = local_grid_graph(G, x, tri)
        lo = aut(M)[0] if M.any() else "11!"
        so = aut(G, partition=[[x], [y for y in range(len(G)) if y != x]])[0]
        out.append((x, int(M.sum()) // 2, lo, so))
    return out
