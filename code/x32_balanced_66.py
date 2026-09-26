# Hand-derived necessary condition for a balanced 7-torsion vector on a (6,6) component C (P = S = 0, girth >= 5):
#   each far vertex meets C in a triple {a,b,c} (layer type (1,1,1) or a perm of (2,1,0); two points in one layer are
#   non-partners; at most one G-edge, which is then a cross edge); pair multiplicities lambda(n,n') = number of far
#   common neighbours = 0 (partners), 1 (same layer non-partners, adjacent, distance 2), 2 (cross-layer distance >= 3).
#   A balanced phi (L_G phi = 0, layer sums 0) needs phi(a)+phi(b)+phi(c) = 0 on every such triple.
#   Test: for every nonzero phi in E_C, count pairs {n,n'} with lambda >= 1 having fewer than lambda admissible zero-sum
#   triples through them.  If some pair fails for every phi, balanced torsion is impossible for that type.
import itertools, sys
import networkx as nx
exec(open('x30e_comp66_tau.py').read().split('from collections import Counter')[0])
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
seen = {}
for tu, tb, s in good:
    L = lap(tu, tb, s)
    n = 18
    layer = [i // 6 for i in range(n)]
    rows = [r[:] for r in L] + [[1 if layer[j] == p else 0 for j in range(n)] for p in range(3)]
    E = nullspace_mod(rows)
    if not E: continue
    G = nx.Graph(); G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if L[i][j] % 7 == 6: G.add_edge(i, j)
    dist = dict(nx.all_pairs_shortest_path_length(G))
    partner = {i: next(j for j in G[i] if layer[j] == layer[i]) for i in range(n)}
    def lam(a, b):
        if layer[a] == layer[b]: return 0 if partner[a] == b else 1
        return 1 if dist[a][b] <= 2 else 2
    triples = []
    for a, b, c in itertools.combinations(range(n), 3):
        ls = sorted((layer[a], layer[b], layer[c]))
        if ls[0] == ls[1] == ls[2]: continue
        if any(lam(x, y) == 0 for x, y in ((a, b), (a, c), (b, c))): continue
        ne = sum(1 for x, y in ((a, b), (a, c), (b, c)) if G.has_edge(x, y))
        if ne > 1: continue
        triples.append((a, b, c))
    # all nonzero phi in span(E) up to scalar
    dimE = len(E); worst = None; ok_phis = 0
    for coeffs in itertools.product(range(7), repeat=dimE):
        if not any(coeffs): continue
        first = next(c for c in coeffs if c)
        if first != 1: continue                       # projective representatives
        phi = [sum(c * e[i] for c, e in zip(coeffs, E)) % 7 for i in range(n)]
        zs = [t for t in triples if (phi[t[0]] + phi[t[1]] + phi[t[2]]) % 7 == 0]
        cov = {}
        for t in zs:
            for x, y in ((t[0], t[1]), (t[0], t[2]), (t[1], t[2])):
                cov[(x, y)] = cov.get((x, y), 0) + 1
        bad = sum(1 for x, y in itertools.combinations(range(n), 2) if lam(x, y) > cov.get((x, y), 0))
        if bad == 0: ok_phis += 1
        worst = bad if worst is None else min(worst, bad)
    k = (dimE, len(triples))
    seen.setdefault(k, []).append((worst, ok_phis))
for k, v in seen.items():
    print(f'dim E_C = {k[0]}, admissible triples = {k[1]}: {len(v)} labeled components; '
          f'min #failing pairs over phi = {min(w for w, _ in v)}, components with some phi passing = {sum(1 for _, o in v if o)}')
