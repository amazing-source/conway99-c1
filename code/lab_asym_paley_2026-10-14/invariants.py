"""Microscopic invariants of every graph of a Spence list (asymmetry campaign, 14/10/2026).

Per graph: |Aut|; local graph types G[N(v)] (canonical forms, multiset over v); lambda-graph types G[N(u) cap N(v)] over
edges; mu-graph types over non-edges; K4 count; all maximum cliques and maximum cocliques (sizes and numbers);
spreads (partitions of V into disjoint maximum cliques) and pairs of orthogonal spreads (nets); p-rank of A - sI for
the prime p dividing r - s when r - s is a prime power.
usage: python invariants.py <spence file> [max_graphs]       (exact; small graphs only)
"""
import itertools
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srglib as L


def induced(nb, S):
    S = list(S)
    idx = {v: i for i, v in enumerate(S)}
    return [set(idx[w] for w in nb[v] if w in idx) for v in S]


def shape(nb, S):
    """Canonical form of the induced subgraph on S, as a short string: n:edges-code-hash."""
    g = induced(nb, S)
    cf = L.canonical_form(g) if len(S) <= 14 else None
    deg = tuple(sorted(len(x) for x in g))
    return (len(S), sum(deg) // 2, deg, cf)


def cliques_of_size(nb, size):
    n = len(nb)
    out = []

    def rec(cl, cand):
        if len(cl) == size:
            out.append(tuple(cl))
            return
        for v in sorted(cand):
            if cl and v < cl[-1]:
                continue
            rec(cl + [v], cand & nb[v])
    rec([], set(range(n)))
    return out


def max_clique_size(nb):
    n = len(nb)
    best = [0]

    def rec(size, cand, last):
        if size + len(cand) <= best[0]:
            return
        if size > best[0]:
            best[0] = size
        for v in sorted(cand):
            if v <= last:
                continue
            rec(size + 1, cand & nb[v], v)
    rec(0, set(range(n)), -1)
    return best[0]


def spreads(nb, cl):
    """All partitions of V into disjoint cliques of the list cl (exact cover by DFS)."""
    n = len(nb)
    size = len(cl[0])
    if n % size:
        return []
    by_vertex = {v: [c for c in cl if v in c] for v in range(n)}
    out = []

    def rec(covered, chosen):
        if len(covered) == n:
            out.append(tuple(sorted(chosen)))
            return
        v = min(set(range(n)) - covered)
        for c in by_vertex[v]:
            if covered.isdisjoint(c):
                rec(covered | set(c), chosen + [c])
    rec(set(), [])
    return out


def p_rank(rows, p):
    M = [list(r) for r in rows]
    nr, nc = len(M), len(M[0])
    r = 0
    for c in range(nc):
        piv = next((i for i in range(r, nr) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(x * inv) % p for x in M[r]]
        for i in range(nr):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r


def eigen_rs(n, k, lam, mu):
    import math
    d = (lam - mu) ** 2 + 4 * (k - mu)
    sq = math.isqrt(d)
    if sq * sq != d:
        return None
    return ((lam - mu + sq) // 2, (lam - mu - sq) // 2)


if __name__ == "__main__":
    header, gs = L.read_spence(sys.argv[1])
    maxg = int(sys.argv[2]) if len(sys.argv) > 2 else len(gs)
    shape_names = {}

    def name(sh):
        if sh not in shape_names:
            shape_names[sh] = "T%d" % len(shape_names)
        return shape_names[sh]

    print(header, "|", len(gs), "graphs")
    for gi, nb in enumerate(gs[:maxg]):
        t0 = time.time()
        n = len(nb)
        n_, k, lam, mu = L.srg_params(nb)
        order, chain, base = L.group_order(nb)
        loc = {}
        for v in range(n):
            loc.setdefault(name(shape(nb, nb[v])), []).append(v)
        lamg, mug = {}, {}
        for u in range(n):
            for v in range(u + 1, n):
                sh = name(shape(nb, nb[u] & nb[v]))
                (lamg if v in nb[u] else mug)[sh] = (lamg if v in nb[u] else mug).get(sh, 0) + 1
        k4 = len(cliques_of_size(nb, 4))
        w = max_clique_size(nb)
        cl = cliques_of_size(nb, w)
        comp = [set(range(n)) - nb[v] - {v} for v in range(n)]
        a = max_clique_size(comp)
        co = cliques_of_size(comp, a)
        sp = spreads(nb, cl) if n % w == 0 else []
        rs = eigen_rs(n, k, lam, mu)
        prank = None
        if rs:
            r, s = rs
            d = r - s
            for p in (2, 3, 5, 7, 11, 13):
                if d % p == 0:
                    rows = [[(1 if j in nb[i] else 0) - (s if i == j else 0) for j in range(n)] for i in range(n)]
                    prank = (p, p_rank(rows, p))
                    break
        print("#%2d |Aut|=%-4d local types %s | lambda-graphs %s | mu-graphs %s | K4=%d | omega=%d (#%d) alpha=%d (#%d) | spreads %d | p-rank(A-sI) %s (%.1fs)"
              % (gi + 1, order, {t: len(vs) for t, vs in sorted(loc.items())}, dict(sorted(lamg.items())),
                 dict(sorted(mug.items())), k4, w, len(cl), a, len(co), len(sp), prank, time.time() - t0), flush=True)
    print("shape dictionary:")
    for sh, nm in sorted(shape_names.items(), key=lambda t: int(t[1][1:])):
        print("  %s: n=%d e=%d degrees=%s" % (nm, sh[0], sh[1], sh[2]))
