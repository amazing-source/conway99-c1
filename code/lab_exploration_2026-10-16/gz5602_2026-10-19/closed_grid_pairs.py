"""Closed grid pairs of a root template (LAB 19/10/2026).  For two DISJOINT grids G, G' (no common line) every vertex
outside G has exactly one neighbour in G (perfect domination) and two labels of G and G' share no letter.  A label w
of a NON-grid rectangle q can be a common neighbour of u in G and v in G' only if q avoids the four lines of G and G'
(otherwise w is adjacent to a letter of G or of G' and has no label-neighbour there).  If no non-grid rectangle avoids
those four lines, the pair (G, G') is CLOSED: all common neighbours of u, v lie in grids, and C2 is an equality:
   2 - [u ~ v] = [pi(u) ~_G' v] + [pi^-1(v) ~_G u] + sum over grids K disjoint from G and G' of [pi_GK(u) = pi_G'K(v)]
where pi = pi_GG' is the perfect matching G -> G' and ~_G is adjacency inside the grid (its 4-cycle).  With
sigma_K = pi_G'K^-1 o pi_GK (a bijection G -> G'), this is a finite system in the bijections pi, sigma_K.
For each template: the closed pairs, and the number of solutions of the system of each closed pair alone
(bijections as permutations of the 4 corners; corners 00, 01, 11, 10 in cycle order).
usage: python closed_grid_pairs.py <catalogue.json.gz> <index list comma separated>"""
import gzip
import json
import sys
from itertools import combinations, permutations, product

recs = json.load(gzip.open(sys.argv[1]))["open"]
idxs = [int(x) for x in sys.argv[2].split(",")]
CORN = [(0, 0), (0, 1), (1, 1), (1, 0)]


def adj(i, j):
    a, b = CORN[i], CORN[j]
    return (a[0] == b[0]) != (a[1] == b[1])


PERMS = list(permutations(range(4)))
for idx in idxs:
    t = recs[idx]["template"]
    ng = {tuple(e) for e in t["nongrid_edges"]}
    grids = [q for q in combinations(range(7), 2) if q not in ng]
    out = []
    for G, H in combinations(grids, 2):
        if set(G) & set(H):
            continue
        four = set(G) | set(H)
        if any(not (set(q) & four) for q in ng):
            continue                                   # not closed
        Ks = [K for K in grids if K not in (G, H) and not (set(K) & four)]
        # count solutions: pi in PERMS (G -> H), sigma_K in PERMS for each K
        sols = 0
        for pi in PERMS:
            inv = [0] * 4
            for u in range(4):
                inv[pi[u]] = u
            base = [[(1 if adj(pi[u], v) else 0) + (1 if adj(inv[v], u) else 0) for v in range(4)] for u in range(4)]
            need = [[2 - (1 if pi[u] == v else 0) - base[u][v] for v in range(4)] for u in range(4)]
            if any(need[u][v] < 0 for u in range(4) for v in range(4)):
                continue
            # need[u][v] = number of K with sigma_K(u) = v ; each sigma_K is a permutation
            for sig in product(PERMS, repeat=len(Ks)):
                ok = True
                for u in range(4):
                    for v in range(4):
                        if sum(1 for s in sig if s[u] == v) != need[u][v]:
                            ok = False; break
                    if not ok:
                        break
                if ok:
                    sols += 1
        out.append({"pair": ["%d%d" % G, "%d%d" % H], "middle_grids": ["%d%d" % K for K in Ks], "solutions": sols})
    print(idx, "dim", t["kernel_dimension"], "k", len(grids), "closed pairs:", out, flush=True)
