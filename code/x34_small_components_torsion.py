# Components of G(L) with m classes (2m labels) per layer, ANY P (triangles/4-cycles allowed), filtered by the local
# axioms visible inside the ball: G cubic, connected, no two triangles sharing an edge (lambda <= 1), no K_{2,3}
# (mu <= 2 inside the component).  Report spanning-tree counts mod 7 and Laplacian nullity mod 7.
import itertools, networkx as nx
from fractions import Fraction
from collections import Counter
def rank_mod(Mx, p=7):
    Mx = [[v % p for v in r] for r in Mx]; n, m = len(Mx), len(Mx[0]); r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if Mx[i][c]), None)
        if piv is None: continue
        Mx[r], Mx[piv] = Mx[piv], Mx[r]; inv = pow(Mx[r][c], p - 2, p); Mx[r] = [(v * inv) % p for v in Mx[r]]
        for i in range(n):
            if i != r and Mx[i][c]:
                f = Mx[i][c]; Mx[i] = [(a - f * b) % p for a, b in zip(Mx[i], Mx[r])]
        r += 1
    return r
def all_matchings(ls):
    if not ls: yield {}; return
    a = ls[0]
    for b in ls[1:]:
        rest = [c for c in ls if c not in (a, b)]
        for m in all_matchings(rest):
            d = dict(m); d[a] = b; d[b] = a; yield d
def ok_local(G):
    # lambda <= 1: every edge in at most one triangle; mu <= 2: no two vertices with 3 common neighbours
    for u, v in G.edges():
        if len(set(G[u]) & set(G[v])) > 1: return False
    nodes = list(G)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if len(set(G[nodes[i]]) & set(G[nodes[j]])) > 2: return False
    return True
for m in (2, 3):
    labels = list(range(2 * m)); mate = {i: i ^ 1 for i in labels}
    M = list(all_matchings(labels))
    stats = Counter(); total = 0
    for tu in M:
        for tb in M:
            for perm in itertools.permutations(labels):
                s = dict(zip(labels, perm))
                G = nx.Graph()
                for v in labels:
                    G.add_edge(('x', v), ('x', mate[v])); G.add_edge(('u', v), ('u', tu[v])); G.add_edge(('b', v), ('b', tb[v]))
                    G.add_edge(('x', v), ('u', v)); G.add_edge(('x', v), ('b', v)); G.add_edge(('u', v), ('b', s[v]))
                if G.number_of_edges() != 9 * m or not nx.is_connected(G): continue   # simple cubic (no double edges)
                if not ok_local(G): continue
                total += 1
                L = nx.laplacian_matrix(G, nodelist=sorted(G)).toarray().tolist()
                n7 = len(L) - rank_mod(L)
                tri = sum(nx.triangles(G).values()) // 3
                stats[(n7, tri > 0)] += 1
    print(f'm = {m} ({2*m} labels): {total} admissible connected components')
    for (n7, has_tri), c in sorted(stats.items()):
        print(f'    nullity_7(Laplacian) = {n7}  (7-torsion rank {n7 - 1}),  triangles: {has_tri}:  {c}')
