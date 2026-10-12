"""Lab session, 2026-10-12. Independent check of note 166, section 3 of branch claude/v7-simultaneous: the number of
equitable partitions of a srg(243,22,1,2) into 27 induced 3 x 3 grids (quotient K_{9,9,9}).

A partition into 27 grids is equitable with internal degree 4 iff every vertex has the same number of neighbours in
every other cell; the quotient then has eigenvalues 22 and 4 or -5 shifted by... it is K_{9,9,9}: each vertex has
exactly one neighbour in 18 other grids and none in 8. So two cells are joined by a perfect matching (9 edges) or by
no edge. The script lists all induced grids, then all exact covers of the 243 vertices by 27 pairwise disjoint grids
such that any two are joined by 0 edges or by a perfect matching, by depth-first search on the least uncovered vertex.
It also checks the tripartite quotient.

python gridparts.py <file.edges>        One process, below 1 GB."""
import sys, itertools, time
import numpy as np
n = 243
A = np.zeros((n, n), dtype=np.int64)
for line in open(sys.argv[1]):
    if line.strip():
        i, j = map(int, line.split()); A[i, j] = A[j, i] = 1
adj = [set(int(y) for y in np.nonzero(A[x])[0]) for x in range(n)]
t0 = time.time()
grids = set()
for x in range(n):
    L = sorted({tuple(sorted((y, next(iter(adj[x] & adj[y]))))) for y in adj[x]})
    for (a, b), (c, d) in itertools.combinations(L, 2):
        e = []
        for p in (a, b):
            for q in (c, d):
                cn = (adj[p] & adj[q]) - {x}
                e.append(next(iter(cn)) if len(cn) == 1 else None)
        if None in e: continue
        S = [x, a, b, c, d] + e
        if len(set(S)) == 9 and all(len(adj[s] & set(S)) == 4 for s in S): grids.add(tuple(sorted(S)))
grids = sorted(grids); G = len(grids)
mask = [sum(1 << v for v in g) for g in grids]
nb = [0] * G                                              # union of the neighbourhoods of the points of a grid, as a count vector
cnt = np.array([A[list(g)].sum(axis=0) for g in grids])   # cnt[g][v] = number of neighbours of v in grid g
def compatible(i, j):
    if mask[i] & mask[j]: return False
    c = cnt[i][list(grids[j])]
    return (c == 0).all() or (c == 1).all()               # no edge, or every point of j has exactly one neighbour in i (then a perfect matching)
by_vertex = [[i for i in range(G) if v in grids[i]] for v in range(n)]
comp = {}
def ok(i, j):
    key = (i, j) if i < j else (j, i)
    if key not in comp: comp[key] = compatible(*key)
    return comp[key]
sols = []; nodes = [0]
def rec(chosen, covered):
    nodes[0] += 1
    if len(chosen) == 27:
        sols.append(tuple(chosen)); return
    v = next(u for u in range(n) if not (covered >> u) & 1)
    for i in by_vertex[v]:
        if mask[i] & covered: continue
        if all(ok(i, j) for j in chosen): rec(chosen + [i], covered | mask[i])
rec([], 0)
tri = 0
for s in sols:
    Q = np.zeros((27, 27), dtype=np.int64)
    for a in range(27):
        for b in range(a + 1, 27):
            if cnt[s[a]][grids[s[b]][0]] == 1: Q[a, b] = Q[b, a] = 1
    # K_{9,9,9}: 18-regular, complement = three disjoint K_9
    C = 1 - Q - np.eye(27, dtype=np.int64)
    if (Q.sum(0) == 18).all() and (C @ C == 7 * C + 8 * np.eye(27, dtype=np.int64)).all(): tri += 1
print("%s: induced grids %d; equitable partitions into 27 grids: %d (quotient K_{9,9,9} for %d of them); search nodes %d  [%.0f s]" % (
    sys.argv[1].replace("\\", "/").split("/")[-1], G, len(sols), tri, nodes[0], time.time() - t0))
