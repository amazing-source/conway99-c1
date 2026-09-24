"""Combinatorial flag positivity (Razborov-style, exact finite counts) for SRG subgraph counts.

For a labelled type sigma (admissible graph on s vertices) and each labelled induced copy phi of sigma, let
x_T(phi) = number of vertices w outside phi(sigma) with N(w) & phi(sigma) = phi(T), for the admissible
patterns T.  Then  M_sigma = sum_phi x(phi) x(phi)^T  is PSD.  Entries:
  M[T,T'] = [T = T'] * sum_phi x_T(phi)  +  #{(phi, w, w') : w != w', patterns T, T'},
which are linear in the counts of order s+1 and s+2.  With s <= 6 everything lives at order <= 8.
"""
import itertools
from collections import defaultdict
import numpy as np
import networkx as nx
from networkx.algorithms import isomorphism as iso


def patterns(sigma, lam, mu, k):
    from subgraph_lp import admissible
    s = sigma.number_of_nodes()
    out = []
    for r in range(s + 1):
        for T in itertools.combinations(range(s), r):
            edges = list(sigma.edges()) + [(t, s) for t in T]
            if admissible(s + 1, edges, lam, mu, k):
                out.append(frozenset(T))
    return out


def flag_coefficients(T, s, lam, mu, k):
    """For each type index i of order s: (patterns list, coef dict (a, b) -> {(order, idx): value}) with a <= b."""
    res = {}
    for i, sig in enumerate(T.reps[s]):
        pats = patterns(sig, lam, mu, k)
        pidx = {p: q for q, p in enumerate(pats)}
        coef = defaultdict(lambda: defaultdict(float))
        # diagonal term: order s+1
        for j, G in enumerate(T.reps[s + 1]):
            for v in G.nodes():
                rest = [u for u in G.nodes() if u != v]
                H = G.subgraph(rest)
                GM = iso.GraphMatcher(H, sig)
                for phi in GM.isomorphisms_iter():          # H-vertex -> sigma-vertex
                    Tv = frozenset(phi[u] for u in G[v])
                    q = pidx[Tv]
                    coef[(q, q)][(s + 1, j)] += 1
        # off-diagonal (w != w'): order s+2
        if s + 2 in T.reps:
            for j, G in enumerate(T.reps[s + 2]):
                for v, v2 in itertools.permutations(G.nodes(), 2):
                    rest = [u for u in G.nodes() if u not in (v, v2)]
                    H = G.subgraph(rest)
                    GM = iso.GraphMatcher(H, sig)
                    for phi in GM.isomorphisms_iter():
                        q1 = pidx[frozenset(phi[u] for u in G[v] if u in phi)]
                        q2 = pidx[frozenset(phi[u] for u in G[v2] if u in phi)]
                        if q1 <= q2:
                            coef[(q1, q2)][(s + 2, j)] += 1 if q1 != q2 else 1
                        # (q2, q1) with q2 > q1 is the same symmetric entry, counted when the pair is (v2, v)
        res[i] = (pats, {key: dict(d) for key, d in coef.items()})
    return res


def flag_matrix(pats, coef, z):
    P = len(pats)
    M = np.zeros((P, P))
    for (a, b), d in coef.items():
        v = sum(c * z.get(u, 0) for u, c in d.items())
        M[a, b] += v
        if a != b:
            M[b, a] += v
    return M
