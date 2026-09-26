# Hand-derived claim (C1, 26/09): in any graph with lambda = 1 and mu = 2 at distance 2 and no prism (P = 0),
# every 4-cycle of G(L) (cubic graph on N_1(L), L a line) is a Z2 copy centred at a vertex of L, and
#   sum_L c4(G(L)) = S,   S = #{(x,E): E in Gamma_2(x), E ~ sigma_x(E)}  (L18).
# Exact check on the twisted geometries of data/ (independent code: plain adjacency sets, no rooted.py).
import json, itertools, sys, os
from math import comb
def check(name, A):
    n = len(A); adj = [set(j for j in range(n) if A[i][j]) for i in range(n)]
    lines = set()
    for i in range(n):
        for j in adj[i]:
            for k in adj[i] & adj[j]:
                lines.add(frozenset((i, j, k)))
    lines = list(lines)
    # prisms: disjoint lines with a perfect matching of 3 edges
    P = 0
    for L, M in itertools.combinations(lines, 2):
        if L & M: continue
        E = [(a, b) for a in L for b in M if b in adj[a]]
        if len(E) == 3 and len({a for a, b in E}) == 3 and len({b for a, b in E}) == 3: P += 1
    # S from the definition
    S = 0
    for x in range(n):
        Nx = adj[x]
        mate = {}
        for a in Nx:
            (b,) = [c for c in Nx if c in adj[a]]
            mate[a] = b
        for E in range(n):
            if E == x or E in Nx: continue
            lab = [a for a in Nx if a in adj[E]]
            if not lab: continue          # distance >= 3 (these geometries are not diameter 2)
            assert len(lab) == 2
            b, c = lab
            sE = [w for w in adj[mate[b]] & adj[mate[c]] if w != x]
            assert len(sE) == 1
            if sE[0] in adj[E]: S += 1
    # 4-cycles of G(L)
    tot = 0; girth5 = 0; cubic = True
    for L in lines:
        N1 = [v for v in range(n) if v not in L and len(adj[v] & L) == 1]
        s = set(N1)
        for v in N1:
            if len(adj[v] & s) != 3: cubic = False
        c4 = 0
        for a, c in itertools.combinations(N1, 2):
            m = len(adj[a] & adj[c] & s)
            c4 += comb(m, 2)
        c4 //= 2
        c3 = sum(1 for a, b in itertools.combinations(N1, 2) if b in adj[a] for c in (adj[a] & adj[b] & s)) // 3
        tot3 = globals().setdefault('_t3', {}); tot3[name] = tot3.get(name, 0) + c3
        tot += c4; girth5 += (c4 == 0)
    print(f'   sum_L c3(G(L)) = {globals()["_t3"].get(name, 0)}  (claim: 2P = {2*P})')
    print(f'{name}: n={n} lines={len(lines)} P={P} S={S} sum_L c4(G(L))={tot}  G(L) cubic={cubic}  lines with c4=0: {girth5}')
    return P, S, tot
for f, name in [('t2_twisted.json', 't=2 (20)'), ('t3_twisted.json', 't=3 (39)'), ('t3_twisted_42.json', 't=3 (42)')]:
    A = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f)))
    check(name, A)
