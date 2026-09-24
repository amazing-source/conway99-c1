"""Exact local counting equations for induced subgraphs of a strongly regular graph, and the LP they define.

For an srg(n, k, lam, mu), every induced subgraph F on m vertices and every set U of at most 2 of its vertices,
the number of outside vertices adjacent to all of U is fixed:
    U = {}      : n - m
    U = {u}     : k - deg_F(u)
    U = {u, u'} : (lam if u ~ u' else mu) - |N_F(u) & N_F(u')|
Summing over all copies of F gives linear equations between the numbers z_G of induced copies of the
(m+1)-vertex graphs G and z_F:
    sum_G a(F, U, G) z_G = |Aut F| * b(F, U) * z_F,
    a(F, U, G) = #{(v, phi) : v in V(G), phi: F -> G - v isomorphism, phi(U) subset N_G(v)}.
Together with z_{K1} = n and z >= 0 this is a linear programme ("order-m local LP"); Reimbayev's hand
computations (orders 6, 7) are its equality part.  Only graphs in which adjacent pairs have <= lam and
non-adjacent pairs <= mu common neighbours can occur; we enumerate exactly those.
"""
import itertools
import sys
from collections import defaultdict
import networkx as nx
from networkx.algorithms import isomorphism as iso


def admissible(m, edges, lam, mu, k):
    adj = [set() for _ in range(m)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    if any(len(a) > k for a in adj):
        return False
    for u in range(m):
        for v in range(u + 1, m):
            c = len(adj[u] & adj[v])
            if (v in adj[u] and c > lam) or (v not in adj[u] and c > mu):
                return False
    return True


class Types:
    """Isomorphism types of admissible graphs, by order."""

    def __init__(self, lam, mu, k, maxm):
        self.lam, self.mu, self.k = lam, mu, k
        self.reps = {1: [nx.empty_graph(1)]}
        self.buckets = {1: {self._h(nx.empty_graph(1)): [0]}}
        for m in range(1, maxm):
            self._extend(m)

    @staticmethod
    def _h(G):
        return (G.number_of_edges(), tuple(sorted(d for _, d in G.degree())),
                nx.weisfeiler_lehman_graph_hash(G, iterations=3))

    def find(self, G):
        m = G.number_of_nodes()
        for i in self.buckets[m].get(self._h(G), []):
            if nx.is_isomorphic(self.reps[m][i], G):
                return i
        return None

    def _extend(self, m):
        reps, buckets = [], {}
        for F in self.reps[m]:
            fe = list(F.edges())
            for r in range(m + 1):
                for S in itertools.combinations(range(m), r):
                    edges = fe + [(s, m) for s in S]
                    if not admissible(m + 1, edges, self.lam, self.mu, self.k):
                        continue
                    G = nx.Graph()
                    G.add_nodes_from(range(m + 1))
                    G.add_edges_from(edges)
                    h = self._h(G)
                    if any(nx.is_isomorphic(reps[i], G) for i in buckets.get(h, [])):
                        continue
                    buckets.setdefault(h, []).append(len(reps))
                    reps.append(G)
        self.reps[m + 1] = reps
        self.buckets[m + 1] = buckets


def build_equations(T, n, maxm):
    """Return (variables, rows) with rows = list of (dict var -> coeff) meaning sum = 0.
    Variables are (m, i). The constant z_{K1} = n is a separate row with rhs."""
    lam, mu, k = T.lam, T.mu, T.k
    rows = []
    aut = {}
    for m in range(1, maxm):
        for i, F in enumerate(T.reps[m]):
            aut[(m, i)] = sum(1 for _ in iso.GraphMatcher(F, F).isomorphisms_iter())
    # a[(m, i, U)][(m+1, j)]
    a = defaultdict(lambda: defaultdict(int))
    for m1 in range(2, maxm + 1):
        m = m1 - 1
        for j, G in enumerate(T.reps[m1]):
            for v in range(m1):
                rest = [u for u in range(m1) if u != v]
                Gv = nx.relabel_nodes(G.subgraph(rest).copy(), {u: t for t, u in enumerate(rest)})
                i = T.find(Gv)
                assert i is not None, 'deleted-vertex subgraph not admissible?'
                F = T.reps[m][i]
                Nv = {rest.index(u) for u in G[v]}
                for phi in iso.GraphMatcher(Gv, F).isomorphisms_iter():   # phi: Gv -> F
                    inv = {fv: gv for gv, fv in phi.items()}               # F -> Gv
                    img = {fv for fv in range(m) if inv[fv] in Nv}         # F-vertices mapped into N(v)
                    a[(m, i, ())][(m1, j)] += 1
                    for u in img:
                        a[(m, i, (u,))][(m1, j)] += 1
                    for u, w in itertools.combinations(sorted(img), 2):
                        a[(m, i, (u, w))][(m1, j)] += 1
    for m in range(1, maxm):
        for i, F in enumerate(T.reps[m]):
            Us = [()] + [(u,) for u in range(m)] + list(itertools.combinations(range(m), 2))
            for U in Us:
                if len(U) == 0:
                    b = n - m
                elif len(U) == 1:
                    b = k - F.degree(U[0])
                else:
                    u, w = U
                    c = len(set(F[u]) & set(F[w]))
                    b = (lam if F.has_edge(u, w) else mu) - c
                row = dict(a[(m, i, U)])
                row[(m, i)] = row.get((m, i), 0) - aut[(m, i)] * b
                rows.append(row)
    return rows, aut


def brute_counts(A, maxm, T):
    """Exact induced-subgraph counts of a small graph (for testing)."""
    N = len(A)
    cnt = defaultdict(int)
    for m in range(1, maxm + 1):
        for S in itertools.combinations(range(N), m):
            G = nx.Graph()
            G.add_nodes_from(range(m))
            G.add_edges_from((p, q) for p in range(m) for q in range(p + 1, m) if A[S[p]][S[q]])
            i = T.find(G)
            assert i is not None
            cnt[(m, i)] += 1
    return cnt


if __name__ == '__main__':
    print('module; see order8 driver')
