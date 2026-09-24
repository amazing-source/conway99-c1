"""Pursuing the Sigma nu^3 route (L15 / F21): in every local-axiom graph (locally (t+1)K2, lambda = 1, mu = 2 at
distance 2) the 1-Hodge Laplacian of the triangle+quadrangle complex is L1 = (k+1)I + Q, Q = signed adjacency of the
opposite-edge graph O ((k-2)-regular). Q = -I - A on the gradient part; the CURL part (spectrum nu) is unknown.
tr(Q^3) = -6 P (P = prisms). This script computes, for every available geometry, the full spectrum of Q split into
gradient / curl parts, and reports curl statistics: min, max, moments, integrality, multiplicities, P, twist.
"""
import json, sys, itertools
import numpy as np
import graphs, rooted, triincidence as ti
import complex_homology as ch


def hodge(A):
    adj = rooted.adjacency_lists(A)
    n = len(A)
    edges = sorted((u, v) for u in range(n) for v in adj[u] if u < v)
    eix = {e: i for i, e in enumerate(edges)}
    tris = rooted.lines(A)
    quads = ch.four_cycles(adj)

    def o(u, v):
        return (eix[(u, v)], 1) if u < v else (eix[(v, u)], -1)
    E = len(edges)
    d1 = np.zeros((n, E))
    for i, (u, v) in enumerate(edges):
        d1[u, i] -= 1; d1[v, i] += 1
    d2 = np.zeros((E, len(tris) + len(quads)))
    for j, c in enumerate([tuple(t) for t in tris] + quads):
        for i in range(len(c)):
            e, s = o(c[i], c[(i + 1) % len(c)]); d2[e, j] += s
    L1 = d1.T @ d1 + d2 @ d2.T
    k = int(A[0].sum())
    Q = L1 - (k + 1) * np.eye(E)
    # projector on the gradient space im(d1^T)
    G = d1.T
    U, s, _ = np.linalg.svd(G, full_matrices=False)
    r = int((s > 1e-9).sum())
    Pg = U[:, :r] @ U[:, :r].T
    Pc = np.eye(E) - Pg
    # curl eigenvalues: eigenvalues of Pc Q Pc restricted (Q commutes with Pg)
    evQ = np.linalg.eigvalsh(Q)
    evG = np.linalg.eigvalsh(Pg @ Q @ Pg)
    # remove the E - r zeros coming from the complement in evG, keep r gradient eigenvalues
    evC = np.linalg.eigvalsh(Pc @ Q @ Pc)
    # the curl part has E - r eigenvalues; Pc Q Pc has r extra zeros
    evC = np.sort(evC)
    # identify: multiset(evQ) = multiset(grad) U multiset(curl); compute curl = evQ minus grad eigenvalues
    grad = np.sort(np.linalg.eigvalsh(U[:, :r].T @ Q @ U[:, :r]))
    Vc = np.linalg.svd(Pc)[0][:, :E - r]
    curl = np.sort(np.linalg.eigvalsh(Vc.T @ Q @ Vc))
    Ob = (np.abs(Q) > 0.5).astype(int)
    P = int(round(np.trace(Ob @ Ob @ Ob) / 6))
    return E, k, grad, curl, P, np.trace(Q @ Q @ Q)


def describe(name, A):
    E, k, grad, curl, P, tr3 = hodge(A)
    vals, cnt = np.unique(np.round(curl, 4), return_counts=True)
    integral = np.allclose(curl, np.round(curl), atol=1e-6)
    top = ', '.join(f'{v:g}^{c}' for v, c in zip(vals[::-1][:8], cnt[::-1][:8]))
    print(f'{name}: k={k} E={E} curl dim={len(curl)} | curl min {curl.min():.3f} max {curl.max():.3f} '
          f'sum {curl.sum():.1f} sum2 {np.sum(curl**2):.1f} sum3 {np.sum(curl**3):.1f} | P={P} tr(Q^3)={tr3:.0f} '
          f'| integral: {integral} | largest: {top}', flush=True)
    return curl


if __name__ == '__main__':
    cases = [('srg9', graphs.srg9()),
             ('H(3,3)', np.array(json.load(open('../data/t2_untwisted.json')))),
             ('twist t=2 (20)', np.array(json.load(open('../data/t2_twisted.json')))),
             ('twist t=3 (39)', np.array(json.load(open('../data/t3_twisted.json')))),
             ('twist t=3 (42)', np.array(json.load(open('../data/t3_twisted_42.json'))))]
    q = 5; N = q * q + q + 1; D = ti.singer(q)
    cases.append(('tri-inc t=5 (93)', ti.build(N, D, sorted(D), sorted((12 * d + 26) % N for d in D))))
    if '--big' in sys.argv:
        cases.append(('bvls', graphs.bvls()))
    for name, A in cases:
        describe(name, A)
