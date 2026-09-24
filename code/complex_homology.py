"""F2-mutation (universal cover): the 2-complex K(G) with 2-cells = triangles (lines) + all 4-cycles.
Computes dim H_1(K; F_p) for p = 2, 3, 5, 7 and over Q (via a large prime), and pi_1 hints.
For a local-axiom graph (lambda = 1, mu in {0,2}), a covering of K preserves the local axioms, so
pi_1(K) != 1 means a strictly larger graph with the same local structure covers G.
"""
import itertools, json, sys
import numpy as np
import rooted, graphs


def four_cycles(adj):
    n = len(adj)
    C = set()
    for u in range(n):
        for v in range(u + 1, n):
            if v in adj[u]:
                continue
            com = sorted(adj[u] & adj[v])
            for p, q in itertools.combinations(com, 2):
                C.add(tuple(sorted([(u, p), (p, v), (v, q), (q, u)], key=lambda e: e)))
    # canonical: store as vertex cycle u,p,v,q
    out = set()
    for u in range(n):
        for v in range(u + 1, n):
            if v in adj[u]:
                continue
            com = sorted(adj[u] & adj[v])
            for p, q in itertools.combinations(com, 2):
                out.add(frozenset([u, p, v, q]) | frozenset())
                # keep orientation info separately
    cyc = []
    seen = set()
    for u in range(n):
        for v in range(u + 1, n):
            if v in adj[u]:
                continue
            com = sorted(adj[u] & adj[v])
            for p, q in itertools.combinations(com, 2):
                key = frozenset([u, v, p, q])
                if key in seen:
                    continue
                seen.add(key)
                cyc.append((u, p, v, q))
    return cyc


def rank_mod(M, p):
    M = M.copy() % p
    r = 0
    rows, cols = M.shape
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i, c]:
                piv = i
                break
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), -1, p)
        M[r] = (M[r] * inv) % p
        nz = np.nonzero(M[:, c])[0]
        for i in nz:
            if i != r:
                M[i] = (M[i] - M[i, c] * M[r]) % p
        r += 1
        if r == rows:
            break
    return r


def homology(A, primes=(2, 3, 5, 7, 1000003)):
    adj = rooted.adjacency_lists(A)
    n = len(adj)
    edges = sorted((u, v) for u in range(n) for v in adj[u] if u < v)
    eix = {e: i for i, e in enumerate(edges)}
    tris = rooted.lines(A)
    quads = four_cycles(adj)

    def oriented(u, v):
        return (eix[(u, v)], 1) if u < v else (eix[(v, u)], -1)
    d2 = np.zeros((len(edges), len(tris) + len(quads)), dtype=np.int64)
    for j, cyc in enumerate([tuple(t) for t in tris] + quads):
        L = len(cyc)
        for i in range(L):
            e, s = oriented(cyc[i], cyc[(i + 1) % L])
            d2[e, j] += s
    d1 = np.zeros((n, len(edges)), dtype=np.int64)
    for i, (u, v) in enumerate(edges):
        d1[u, i] -= 1
        d1[v, i] += 1
    res = {'V': n, 'E': len(edges), 'T': len(tris), 'Q': len(quads)}
    for p in primes:
        r1 = rank_mod(d1.T.copy(), p)   # rank of d1
        r2 = rank_mod(d2.T.copy(), p)
        res[f'b1_F{p}' if p < 1000 else 'b1_Q'] = len(edges) - r1 - r2
    return res


if __name__ == '__main__':
    cases = [('srg9', graphs.srg9()),
             ('H(3,3)', np.array(json.load(open('../data/t2_untwisted.json')))),
             ('twist t=2 (20)', np.array(json.load(open('../data/t2_twisted.json')))),
             ('twist t=3 (39)', np.array(json.load(open('../data/t3_twisted.json'))))]
    if '--bvls' in sys.argv:
        cases.append(('bvls', graphs.bvls()))
    for name, A in cases:
        print(name, homology(A), flush=True)
