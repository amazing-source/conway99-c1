# Single-component balance test for 6-label components at P = 0 (triangle-free), S unrestricted (4-cycles allowed).
# Far vertices meet C in 3 points; pair multiplicities K[n,n'] = far common neighbours:
#   same layer: 0 (partners) / 1;  cross-layer: (1 if adjacent else 2) - |N_G(n) & N_G(n')|.
# Admissible triple: no pair with K = 0, not all in one layer, at most one G-edge.  Balanced phi (L_G phi = 0, layer sums
# 0, supported on C) needs every pair to be covered K times by admissible zero-sum triples.
import itertools, networkx as nx
from collections import Counter
exec(open('x34_small_components_torsion.py').read().split('for m in (2, 3):')[0])
def nullspace_mod(Mx, p=7):
    Mx = [[v % p for v in r] for r in Mx]; n, m = len(Mx), len(Mx[0]); r = 0; piv = []
    for c in range(m):
        pr = next((i for i in range(r, n) if Mx[i][c]), None)
        if pr is None: continue
        Mx[r], Mx[pr] = Mx[pr], Mx[r]; inv = pow(Mx[r][c], p - 2, p); Mx[r] = [(v * inv) % p for v in Mx[r]]
        for i in range(n):
            if i != r and Mx[i][c]:
                f = Mx[i][c]; Mx[i] = [(a - f * b) % p for a, b in zip(Mx[i], Mx[r])]
        piv.append(c); r += 1
    free = [c for c in range(m) if c not in piv]; basis = []
    for fc in free:
        v = [0] * m; v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = (-Mx[i][fc]) % p
        basis.append(v)
    return basis
labels = list(range(6)); mate = {i: i ^ 1 for i in labels}
M = list(all_matchings(labels))
res = Counter(); tested = 0
for tu in M:
    for tb in M:
        for perm in itertools.permutations(labels):
            s = dict(zip(labels, perm))
            G = nx.Graph()
            for v in labels:
                G.add_edge(('x', v), ('x', mate[v])); G.add_edge(('u', v), ('u', tu[v])); G.add_edge(('b', v), ('b', tb[v]))
                G.add_edge(('x', v), ('u', v)); G.add_edge(('x', v), ('b', v)); G.add_edge(('u', v), ('b', s[v]))
            if G.number_of_edges() != 27 or not nx.is_connected(G) or not ok_local(G): continue
            if sum(nx.triangles(G).values()) > 0: continue                 # P = 0
            nodes = sorted(G); idx = {v: i for i, v in enumerate(nodes)}; n = len(nodes)
            layer = [ {'x': 0, 'u': 1, 'b': 2}[v[0]] for v in nodes ]
            L = nx.laplacian_matrix(G, nodelist=nodes).toarray().tolist()
            rows = [r[:] for r in L] + [[1 if layer[j] == p else 0 for j in range(n)] for p in range(3)]
            E = nullspace_mod(rows)
            if not E: continue
            tested += 1
            A = [[1 if G.has_edge(nodes[i], nodes[j]) else 0 for j in range(n)] for i in range(n)]
            nb = [set(j for j in range(n) if A[i][j]) for i in range(n)]
            def K(a, b):
                if layer[a] == layer[b]: return 0 if A[a][b] else 1
                return (1 if A[a][b] else 2) - len(nb[a] & nb[b])
            triples = [t for t in itertools.combinations(range(n), 3)
                       if len({layer[i] for i in t}) > 1 and all(K(a, b) > 0 for a, b in itertools.combinations(t, 2))
                       and sum(A[a][b] for a, b in itertools.combinations(t, 2)) <= 1]
            passing = 0
            for coeffs in itertools.product(range(7), repeat=len(E)):
                if not any(coeffs) or next(c for c in coeffs if c) != 1: continue
                phi = [sum(c * e[i] for c, e in zip(coeffs, E)) % 7 for i in range(n)]
                cov = Counter()
                for t in triples:
                    if (phi[t[0]] + phi[t[1]] + phi[t[2]]) % 7 == 0:
                        for a, b in itertools.combinations(t, 2): cov[(a, b)] += 1
                if all(cov[(a, b)] >= K(a, b) for a, b in itertools.combinations(range(n), 2)): passing += 1
            res[(len(E), passing > 0)] += 1
print('triangle-free 6-label components with torsion tested:', tested)
for k, v in sorted(res.items()): print(f'  dim E_C = {k[0]}, some phi passes the pair-coverage test: {k[1]}  -> {v}')
