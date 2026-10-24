"""Expérience 8 : test de simple connexité du 2-complexe X (triangles + quadrangles) par effondrement de la
présentation de pi_1.

Présentation standard : générateurs = arêtes orientées, relations = arêtes d'un arbre couvrant égales à 1, et bord de
chaque 2-cellule égal à 1. Si une relation a toutes ses arêtes triviales sauf une, celle-ci est triviale. Si la
propagation rend toutes les arêtes triviales, pi_1(X) = 1 : c'est une preuve (suite de transformations de Tietze).
Un blocage ne prouve rien ; il faut alors lire H_1.

Cas testés : H(3,3) et H(4,3) (témoins positifs), BvLS (pi_1 = Golay, doit bloquer), t2 et t3 (géométries tordues
de l'équipe), les quatre srg(243) et leurs revêtements triples (exp4/exp5)."""
import sys, json, itertools
from collections import deque
import numpy as np
sys.path.insert(0, '.')
import srg_tools as T
from exp6_cover_homology import squares_general
from exp5_cover_invariants import cover, files
from exp3_growth_comparison import hamming


def collapse(N, adj):
    edges = sorted({(min(u, w), max(u, w)) for u in range(N) for w in adj[u]})
    eid = {e: i for i, e in enumerate(edges)}
    cells = [[(a, b), (b, c), (a, c)] for (a, b, c) in T.lines_of(N, adj)]
    for (p, q, r, s) in squares_general(N, adj):
        cells.append([(p, q), (q, r), (r, s), (s, p)])
    cells = [[eid[(min(u, w), max(u, w))] for (u, w) in c] for c in cells]
    triv = [False] * len(edges)
    # arbre couvrant en largeur depuis 0
    seen = {0}; dq = deque([0])
    while dq:
        u = dq.popleft()
        for w in sorted(adj[u]):
            if w not in seen:
                seen.add(w); dq.append(w); triv[eid[(min(u, w), max(u, w))]] = True
    assert len(seen) == N, 'non connexe'
    inc = [[] for _ in edges]
    for ci, c in enumerate(cells):
        for e in c:
            inc[e].append(ci)
    left = [sum(1 for e in c if not triv[e]) for c in cells]
    q = deque(ci for ci in range(len(cells)) if left[ci] == 1)
    while q:
        ci = q.popleft()
        if left[ci] != 1:
            continue
        e = next(e for e in cells[ci] if not triv[e])
        triv[e] = True
        for cj in inc[e]:
            left[cj] -= 1
            if left[cj] == 1:
                q.append(cj)
    rest = triv.count(False)
    return dict(vertices=N, edges=len(edges), cells=len(cells), untrivialized_edges=rest,
                simply_connected=(rest == 0))


def from_matrix(A):
    n = len(A)
    return n, [set(j for j in range(n) if A[i][j]) for i in range(n)]


out = {}
for m in (3, 4):
    n, adj = hamming(m)
    out[f'H({m},3)'] = collapse(n, adj)
for name in ('t2_twisted', 't3_twisted'):
    out[name] = collapse(*from_matrix(json.load(open(f'../../../data/{name}.json'))))
for name, f in files.items():
    n, _, adj = T.load_edges(f)
    out[name] = collapse(n, adj)
    N, cadj = cover(f)
    out[name + '_cover3'] = collapse(N, cadj)
for k, v in out.items():
    print(k, v, flush=True)
json.dump(out, open('../data/exp8_simple_connectivity.json', 'w'), indent=1)
