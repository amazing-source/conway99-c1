"""C1, lab session, 2026-10-08. A line in six grids: the COLUMN part of the 60 names and the Petersen graph (checks).
  python pencil6_petersen.py
Names (NOTE 17.46): each far vertex b gives a 2-to-1 map {six grids} -> {three columns}: a syntheme of the six grids
with a bijection of its duads to the columns ("labelled syntheme", 15 * 6 = 90). Column conditions on the multiset of
60 names: (C1) each (duad, column) in exactly 4 names; (C2) for k, j in different duads and columns i != i', exactly 8.
Checked here, exactly: the canonical solution (all labelled synthemes outside a synthematic total), its description by
the Petersen graph, the column-agreement numbers between two names, the failure of the obvious symmetric graph on it,
and the dimension of the solution space of (C1) at the level of synthemes. Pure combinatorics, a few seconds."""
from itertools import combinations, permutations
import networkx as nx
import numpy as np
pts = range(6); duads = [frozenset(d) for d in combinations(pts, 2)]
synth = []
for a in combinations(duads, 3):
    if len(frozenset().union(*a)) == 6: synth.append(frozenset(a))
assert len(synth) == 15
# synthematic totals: 5 pairwise disjoint synthemes (as sets of duads) covering the 15 duads
totals = [t for t in combinations(synth, 5) if len(frozenset().union(*t)) == 15]
print("synthemes %d, totals %d" % (len(synth), len(totals)))
T = totals[0]; out = [s for s in synth if s not in T]
P = nx.Graph(); P.add_nodes_from(range(10))
for x, y in combinations(range(10), 2):
    if out[x] & out[y]: P.add_edge(x, y, duad=next(iter(out[x] & out[y])))
print("graph on the 10 synthemes outside a total (adjacent = sharing a duad): %d edges, degrees %s, isomorphic to Petersen: %s" % (
    P.number_of_edges(), sorted(set(dict(P.degree()).values())), nx.is_isomorphic(P, nx.petersen_graph())))
for k in pts:
    M = [(x, y) for x, y, d in P.edges(data="duad") if k in d]
    assert len(M) == 5 and len({v for e in M for v in e}) == 10
print("each of the six grids = a perfect matching of that Petersen graph (5 edges covering the 10 vertices): checked; 15 duads = 15 edges")
names = [(x, lam) for x in range(10) for lam in permutations(range(3))]     # lam[t] = column of the t-th duad of out[x]
def col(nm, k):
    x, lam = nm; ds = sorted(out[x], key=sorted)
    return next(lam[t] for t in range(3) if k in ds[t])
c1 = {}; c2 = {}
for nm in names:
    cs = [col(nm, k) for k in pts]
    for k, j in combinations(pts, 2):
        if cs[k] == cs[j]: c1[(k, j, cs[k])] = c1.get((k, j, cs[k]), 0) + 1
        else: c2[(k, j, cs[k], cs[j])] = c2.get((k, j, cs[k], cs[j]), 0) + 1
print("canonical 60 names: (duad, column) counts %s (need 4, %d cases); (k->i, j->i') counts %s (need 8, %d cases)" % (
    sorted(set(c1.values())), len(c1), sorted(set(c2.values())), len(c2)))
# column agreements between two names, by distance of the syntheme-vertices in the Petersen graph
dist = dict(nx.all_pairs_shortest_path_length(P)); tab = {}
for a in names:
    for b in names:
        if a == b: continue
        ag = sum(col(a, k) == col(b, k) for k in pts); key = (dist[a[0]][b[0]], ag); tab[key] = tab.get(key, 0) + 1
print("column agreements of two distinct names, (Petersen distance, agreements): count per name = %s" % {k_: v // 60 for k_, v in sorted(tab.items())})
# the obvious symmetric graph H0: rotations at a vertex, and along a Petersen edge with the same column on that edge
def adj0(a, b):
    if a[0] == b[0]:
        s = [a[1].index(t) for t in b[1]]                                     # permutation relating the labellings
        return sorted(s) == [0, 1, 2] and all(a[1][t] != b[1][t] for t in range(3))
    if P.has_edge(a[0], b[0]):
        d = P[a[0]][b[0]]["duad"]; k = min(d); return col(a, k) == col(b, k)
    return False
H0 = nx.Graph(); H0.add_nodes_from(names)
for a, b in combinations(names, 2):
    if adj0(a, b): H0.add_edge(a, b)
bad = 0
for a in names:
    for k in pts:
        same = sum(col(b, k) == col(a, k) for b in H0[a])
        if same != 2: bad += 1
print("H0 (rotations + Petersen edges with equal column): %d edges, degrees %s; (name, grid) cases violating 'exactly two neighbours in the same column': %d of 360" % (
    H0.number_of_edges(), sorted(set(dict(H0.degree()).values())), bad))
# level of synthemes: W(s) = number of names on the syntheme s; (C1) summed over columns: for every duad, sum of W over its 3 synthemes = 12
N = np.array([[1 if d in s else 0 for s in synth] for d in duads])
print("duad-syntheme incidence: rank %d, so the solutions W of 'sum = 12 on every duad' form W = 4 + (a 5-dimensional kernel); kernel vectors from totals: -4 on a total, +2 outside" % np.linalg.matrix_rank(N))
