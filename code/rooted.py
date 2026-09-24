"""Rooted structure of a graph with lambda = 1 (locally (t+1)K2) and mu = 2 at distance 2.

For a root x:
  labels  = N(x) (vertex ids), mate[a] = the other point of the line {x, a, mate[a]}
  X       = vertices at distance 2 from x, label(u) = frozenset of its two neighbours in N(x)
  tau[a]  = dict b -> c : the X-vertex ab is adjacent to ac (the unique line through a and ab)
Works for any graph satisfying the local axioms (not only SRGs): X = Gamma_2(x).
"""
from collections import defaultdict
import itertools
import numpy as np


def adjacency_lists(A):
    A = np.asarray(A)
    return [set(np.nonzero(A[i])[0].tolist()) for i in range(A.shape[0])]


def lines(A):
    """All triangles (as sorted tuples). For lambda = 1 graphs these are the lines."""
    adj = adjacency_lists(A)
    T = set()
    for u in range(len(adj)):
        for v in adj[u]:
            if v > u:
                for w in adj[u] & adj[v]:
                    if w > v:
                        T.add((u, v, w))
    return sorted(T)


def check_local_axioms(A):
    """lambda = 1 on edges; mu in {0, 2} on non-edges (mu = 2 at distance 2)."""
    A = np.asarray(A, dtype=np.int64)
    A2 = A @ A
    n = A.shape[0]
    off = ~np.eye(n, dtype=bool)
    lam = set(A2[(A == 1) & off].tolist())
    mu = set(A2[(A == 0) & off].tolist())
    return lam, mu


class Rooted:
    def __init__(self, A, x):
        A = np.asarray(A, dtype=np.int64)
        self.A = A
        self.adj = adj = adjacency_lists(A)
        self.x = x
        self.L = sorted(adj[x])
        self.mate = {}
        for a in self.L:
            m = adj[a] & adj[x]
            assert len(m) == 1, "N(x) is not a perfect matching (lambda != 1?)"
            self.mate[a] = next(iter(m))
        Lset = set(self.L)
        self.X = sorted(v for v in range(A.shape[0]) if v != x and v not in Lset and adj[v] & Lset)
        self.label = {}
        for u in self.X:
            lab = frozenset(adj[u] & Lset)
            assert len(lab) == 2, "distance-2 vertex without exactly 2 neighbours in N(x)"
            a, b = tuple(lab)
            assert self.mate[a] != b
            self.label[u] = lab
        self.vertex_of = {lab: u for u, lab in self.label.items()}
        self.tau = {a: {} for a in self.L}
        for a in self.L:
            for u in self.X:
                if a in self.label[u]:
                    (b,) = self.label[u] - {a}
                    nb = [w for w in adj[u] & adj[a] if w in self.label]
                    assert len(nb) == 1
                    (c,) = self.label[nb[0]] - {a}
                    self.tau[a][b] = c
        Xset = set(self.X)
        self.lab_edges, self.dis_edges = [], []
        for u in self.X:
            for w in adj[u] & Xset:
                if w > u:
                    (self.lab_edges if self.label[u] & self.label[w] else self.dis_edges).append((u, w))

    def classes(self):
        seen, cl = set(), []
        for a in self.L:
            if a not in seen:
                cl.append((a, self.mate[a]))
                seen |= {a, self.mate[a]}
        return cl

    def is_mate_system(self):
        return all(self.tau[a][b] == self.mate[b] for a in self.L for b in self.tau[a])

    def mate_fixed(self, a):
        """number of mate pairs {b, b-bar} fixed by tau_a (= prisms through the edge x-a with that rung)."""
        return sum(1 for b in self.tau[a] if self.tau[a][b] == self.mate[b]) // 2

    def trail_cycles(self):
        """cycles of the labelled 2-factor on X (lengths)."""
        Xset = set(self.X)
        nbr = defaultdict(list)
        for u, w in self.lab_edges:
            nbr[u].append(w)
            nbr[w].append(u)
        seen, lengths = set(), []
        for u in self.X:
            if u in seen:
                continue
            L, prev, cur = 0, None, u
            while True:
                seen.add(cur)
                L += 1
                nxt = [w for w in nbr[cur] if w != prev]
                if prev is None:
                    nxt = nbr[cur][:1]
                prev, cur = cur, nxt[0]
                if cur == u:
                    break
            lengths.append(L)
        return sorted(lengths)


def shadow(adj, p, a, x):
    """unique common neighbour of p and a other than x (p, a non-adjacent, both adjacent to x)."""
    c = (adj[p] & adj[a]) - {x}
    assert len(c) == 1
    return next(iter(c))


def line_holonomy(A, line, adj=None):
    """rho_l for l = (x, a, abar) based at x: permutation of N(x) minus l, as dict p -> rho(p)."""
    if adj is None:
        adj = adjacency_lists(A)
    x, a, ab = line
    P0 = sorted(adj[x] - {a, ab})
    rho = {}
    for p in P0:
        pa = shadow(adj, p, a, x)          # in N(a)
        pab = shadow(adj, pa, ab, a)       # in N(abar), common nbr of pa and abar other than a
        q = shadow(adj, pab, x, ab)        # in N(x), common nbr of pab and x other than abar
        rho[p] = q
    return rho


def cycle_type(perm):
    seen, ct = set(), []
    for p in perm:
        if p in seen:
            continue
        L, q = 0, p
        while q not in seen:
            seen.add(q)
            q = perm[q]
            L += 1
        ct.append(L)
    return tuple(sorted(ct, reverse=True))


if __name__ == '__main__':
    import graphs
    for name in ['srg9', 'bvls']:
        A = graphs.ALL[name]()
        print(name, 'local axioms (lam, mu):', check_local_axioms(A))
        R = Rooted(A, 0)
        print('  |L| =', len(R.L), '|X| =', len(R.X), 'labelled edges', len(R.lab_edges), 'disjoint', len(R.dis_edges))
        print('  mate system:', R.is_mate_system(), ' trail cycles:', R.trail_cycles()[:8], '...')
        T = lines(A)
        print('  lines:', len(T))
        hol = [cycle_type(line_holonomy(A, (l[0], l[1], l[2]))) for l in T[:20]]
        print('  holonomy cycle types (first 20 lines):', set(hol))
