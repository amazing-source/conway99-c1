"""Switchability test of candidate free regions F = V minus ball(X): a switch supported in F exists only if both
E_4(F) and E_{-5}(F) (eigenvectors supported on F) are non-zero.  Prints dims for several kinds of X."""
import sys, itertools, collections, numpy as np
from lib243 import *
from frame import supported_eigvecs

def ball(G, X):
    s = set(X)
    for x in X: s |= set(np.nonzero(G[x])[0].tolist())
    return s

def grids_list(G):
    tri = triangles(G); at = collections.defaultdict(list)
    for t in tri:
        for p in t: at[p].append(t)
    out = set()
    for p in range(len(G)):
        for L1, L2 in itertools.combinations(at[p], 2):
            pts = set(L1) | set(L2)
            a = [x for x in L1 if x != p]; b = [x for x in L2 if x != p]
            for x in a:
                for y in b:
                    c = set(np.nonzero(G[x] & G[y])[0].tolist()) - {p}
                    if len(c) == 1: pts |= c
            if len(pts) == 9 and G[np.ix_(sorted(pts), sorted(pts))].sum() == 36:
                out.add(frozenset(pts))
    return [sorted(g) for g in out]

if __name__ == "__main__":
    G = np.load(sys.argv[1]) if sys.argv[1].endswith(".npy") else load_edges(sys.argv[1])
    n = len(G); tri = triangles(G)
    rng = np.random.default_rng(1)
    kinds = {}
    kinds["vertex"] = [[int(v)] for v in rng.choice(n, 3, replace=False)]
    kinds["edge"] = [list(tri[i][:2]) for i in rng.choice(len(tri), 3, replace=False)]
    kinds["line"] = [list(tri[i]) for i in rng.choice(len(tri), 3, replace=False)]
    gl = grids_list(G)
    kinds["grid"] = [gl[i] for i in rng.choice(len(gl), min(4, len(gl)), replace=False)]
    # two lines through a point that do NOT span a grid (twisted pair through p), and disjoint lines with 2 edges
    for name, Xs in kinds.items():
        for X in Xs:
            F = sorted(set(range(n)) - ball(G, X))
            d4 = supported_eigvecs(G, F, 4).shape[1]; d5 = supported_eigvecs(G, F, -5).shape[1]
            print(f"{name:7s} |X|={len(X):2d} |F|={len(F):3d}  dim E4(F)={d4:3d}  dim E-5(F)={d5:3d}", flush=True)
