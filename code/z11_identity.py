"""Combinatorial meaning of Reimbayev's second free variable z11 (arXiv:2608.19410), checked by direct counting.

Definitions (any graph with lambda = 1 and mu = 2 at distance 2, i.e. our rooted axioms):
  sigma_x = point reflection at x: fixes x, swaps mates in N(x), and sends E in Gamma_2(x) with label {b, c}
            to the vertex with label {mate(b), mate(c)}.
  S       = #{(x, E) : E in Gamma_2(x), E ~ sigma_x(E)}                     ("sigma-adjacent pairs")
  S'      = sum_E #{non-mate pairs {a, c} in N(E) : tau_a(c) = tau_c(a)}     ("tau-coincidences", rooted at E)
  Wsum    = sum_x |W(x)|  (twisted (label, class) pairs; Reimbayev's n3 = Wsum / 2 in an SRG)
Claims (hand derivations in notes/90):
  S = S'  ;  z2 = S/2  ;  z3 = Wsum - 2S  ;  z11 = 2 Wsum - 2S   (z_i = number of induced copies of Z_i)
so in an SRG  z11 = 4 n3 - 2S  and Reimbayev's polygon 2 n3 <= z11 <= 4 n3 is exactly 0 <= S <= n3.
The three identities are local (derived without mu = 2 beyond distance 2), so they must hold on the twisted
non-SRG geometries too; that is the test.  Patterns Z2, Z3, Z11 transcribed from Figure 1 of the paper.
"""
import json
import itertools
import networkx as nx
from networkx.algorithms import isomorphism as iso
import numpy as np
import graphs
import rooted

Z = {
    2: [('C', 'TL'), ('C', 'TR'), ('TL', 'TR'), ('C', 'BL'), ('C', 'BR'), ('BL', 'BR'),
        ('L', 'TL'), ('L', 'BL'), ('R', 'TR'), ('R', 'BR'), ('L', 'R')],
    3: [('LT', 'LB'), ('LT', 'mid'), ('LB', 'mid'), ('LT', 'top'), ('LB', 'bot'), ('mid', 'rm'),
        ('top', 'rm'), ('bot', 'rm'), ('top', 'fr'), ('bot', 'fr')],
    11: [('T', 'A'), ('T', 'B'), ('A', 'B'), ('A', 'C'), ('A', 'D'), ('C', 'D'), ('C', 'E'), ('B', 'E'),
         ('D', 'F'), ('F', 'E')],
}


def induced_count(G, pat_edges):
    P = nx.Graph(pat_edges)
    aut = sum(1 for _ in iso.GraphMatcher(P, P).isomorphisms_iter())
    m = sum(1 for _ in iso.GraphMatcher(G, P).subgraph_isomorphisms_iter())
    assert m % aut == 0
    return m // aut


def stats(A):
    A = np.asarray(A)
    n = len(A)
    Wsum = S = Sp = 0
    for x in range(n):
        R = rooted.Rooted(A, x)
        adj = R.adj
        # twisting: label a twists class {c, mate c} iff tau_a(c) != mate(c)
        for a in R.L:
            classes = {frozenset((c, R.mate[c])) for c in R.tau[a]}
            Wsum += sum(1 for cl in classes if R.tau[a][next(iter(cl))] not in cl)
        for E in R.X:
            b, c = tuple(R.label[E])
            sE = R.vertex_of[frozenset((R.mate[b], R.mate[c]))]
            if sE in adj[E]:
                S += 1
        # tau-coincidences at root x
        for a, c in itertools.combinations(R.L, 2):
            if R.mate[a] == c:
                continue
            if R.tau[a][c] == R.tau[c][a]:
                Sp += 1
    return Wsum, S, Sp


def main():
    cases = [('twist t=2 (20)', json.load(open('../data/t2_twisted.json'))),
             ('twist t=3 (39)', json.load(open('../data/t3_twisted.json'))),
             ('twist t=3 (42)', json.load(open('../data/t3_twisted_42.json'))),
             ('zoo t=2 (20)', json.load(open('../data/zoo_t2_20_34.json'))) if False else None,
             ('srg(9,4,1,2)', graphs.srg9())]
    for item in cases:
        if item is None:
            continue
        name, A = item
        A = np.asarray(A)
        lam, mu = rooted.check_local_axioms(A)
        G = nx.from_numpy_array(A)
        Wsum, S, Sp = stats(A)
        z = {i: induced_count(G, e) for i, e in Z.items()}
        pred = {2: S / 2, 3: Wsum - 2 * S, 11: 2 * Wsum - 2 * S}
        ok = all(z[i] == pred[i] for i in z) and S == Sp
        print(f'{name}: lambda {lam}, mu {mu} | Wsum {Wsum}, S {S}, S\' {Sp} | '
              f'z2 {z[2]} (pred {pred[2]}), z3 {z[3]} (pred {pred[3]}), z11 {z[11]} (pred {pred[11]}) -> '
              f'{"OK" if ok else "MISMATCH"}')


if __name__ == '__main__':
    main()
