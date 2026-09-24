"""Hodge route, second pass (2026-09-24 evening): test of the 'confinement' claim and of the triangle-block identities.

Local-axiom graph (locally (t+1)K2, lambda = 1, mu in {0,2}), triangle+quadrangle 2-complex, L1 = (k+1)I + Q,
Q = signed adjacency of the opposite-edge graph O (2t-regular).  g(x) = x^2 + x - 2t: its roots r', s' are the values
-1-theta of Q on gradients of an SRG (t = 6: 3 and -4).  n_SRG = 2t^2 + 4t + 3.
Claims tested here (all proved by hand in notes/60_HODGE.md):
  (1) Sum_curl g(nu) = -2 (n - n_SRG)                        (= 0 for an SRG)
  (2) C_T = span of the triangle circulations (dim = #lines, inside the curl space), curl_0 = curl ∩ C_T^perp,
      B = P_T Q (1 - P_T):   ||B||^2 = (4/3)(P_max - P),  ||[Q, B_T]||^2 = 24 (P_max - P),  P_max = tE/3,
      Sum_{C_T} g(alpha) = -||B||^2,   Sum_{curl_0} g(kappa) = -||B||^2 - 2 (n - n_SRG)
      (alpha, kappa = spectra of Q compressed to C_T and to curl_0).
  (3) BvLS (H(11,3)/Golay): curl = {-20^11, -5^660, -2^660, 4^880, 7^220}, C_T part {-20, -2, 7}, curl_0 part {-5, 4}:
      the curl spectrum of an existing SRG of the family is NOT confined to [s', r'].
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '2')
os.environ.setdefault('OMP_NUM_THREADS', '2')
os.environ.setdefault('MKL_NUM_THREADS', '2')
import json, sys, time
import numpy as np
import graphs, rooted, triincidence as ti
import complex_homology as ch


def build(A):
    A = np.asarray(A)
    n = len(A)
    adj = rooted.adjacency_lists(A)
    k = int(A[0].sum())
    t = (k - 2) // 2
    edges = sorted((u, v) for u in range(n) for v in adj[u] if u < v)
    eix = {e: i for i, e in enumerate(edges)}
    E = len(edges)

    def o(p, q):
        return (eix[(p, q)], 1) if p < q else (eix[(q, p)], -1)
    quads = ch.four_cycles(adj)
    Q = np.zeros((E, E))
    for cyc in quads:
        d = [o(cyc[i], cyc[(i + 1) % 4]) for i in range(4)]
        for i in range(2):
            (e1, s1), (e2, s2) = d[i], d[i + 2]
            Q[e1, e2] += s1 * s2
            Q[e2, e1] += s1 * s2
    tris = rooted.lines(A)
    UT = np.zeros((E, len(tris)))
    for j, (a, b, c) in enumerate(tris):
        for p, q in ((a, b), (b, c), (c, a)):
            e, s = o(p, q)
            UT[e, j] = s / np.sqrt(3)
    d1 = np.zeros((n, E))
    for i, (u, v) in enumerate(edges):
        d1[u, i] = -1
        d1[v, i] = 1
    lap_err = None
    if E <= 700:   # direct check Q = L1 - (k+1) I on small complexes
        faces = [tuple(x) for x in tris] + [tuple(c) for c in quads]
        d2 = np.zeros((E, len(faces)))
        for j, c in enumerate(faces):
            for i in range(len(c)):
                e, s = o(c[i], c[(i + 1) % len(c)])
                d2[e, j] += s
        lap_err = np.abs(d1.T @ d1 + d2 @ d2.T - (k + 1) * np.eye(E) - Q).max()
    return A, n, k, t, E, Q, UT, d1, lap_err


def multiset(x, nd=6):
    v, c = np.unique(np.round(x, nd), return_counts=True)
    if len(v) <= 12:
        return '{' + ', '.join(f'{a:g}^{b}' for a, b in zip(v, c)) + '}'
    return f'[{len(v)} distinct values, min {x.min():.4f}, max {x.max():.4f}]'


def analyse(name, A):
    t0 = time.time()
    A, n, k, t, E, Q, UT, d1, lap_err = build(A)
    nS = 2 * t * t + 4 * t + 3
    g = lambda x: x * x + x - 2 * t
    rp, sp = (-1 + np.sqrt(1 + 8 * t)) / 2, (-1 - np.sqrt(1 + 8 * t)) / 2
    absQ = np.abs(Q)
    degs = set(np.round(absQ.sum(1)).astype(int).tolist())
    P = int(round(np.trace(absQ @ absQ @ absQ) / 6))
    Pmax = t * E / 3
    grad_err = np.abs(Q @ d1.T - d1.T @ (-np.eye(n) - A)).max()
    _, s, Vt = np.linalg.svd(d1, full_matrices=True)
    r = int((s > 1e-9).sum())
    Vc = Vt[r:].T
    nu = np.linalg.eigvalsh(Vc.T @ Q @ Vc)
    alpha = np.linalg.eigvalsh(UT.T @ Q @ UT)
    W0 = Vc - UT @ (UT.T @ Vc)
    Uw, sw, _ = np.linalg.svd(W0, full_matrices=False)
    W = Uw[:, sw > 1e-8]
    kappa = np.linalg.eigvalsh(W.T @ Q @ W)
    Bn = np.linalg.norm(UT.T @ Q @ W) ** 2
    BT = 3 * UT @ UT.T
    comm = np.linalg.norm(Q @ BT - BT @ Q) ** 2
    out = [f'== {name}: n={n} k={k} t={t} E={E} O-degrees={sorted(degs)} n_SRG={nS} '
           f'| lapl check {lap_err} | grad identity err {grad_err:.1e}',
           f'   P={P} P_max={Pmax:g}  ||[Q,B_T]||^2={comm:.4f} vs 24(Pmax-P)={24*(Pmax-P):g}'
           f'  ||B||^2={Bn:.4f} vs (4/3)(Pmax-P)={4*(Pmax-P)/3:.4f}',
           f'   curl  (dim {len(nu)}): sum g = {g(nu).sum():.4f} vs -2(n-n_SRG) = {-2*(n-nS)}'
           f' | outside [{sp:.3f},{rp:.3f}]: {(g(nu) > 1e-7).sum()} | {multiset(nu)}',
           f'   C_T   (dim {len(alpha)}): sum g = {g(alpha).sum():.4f} vs -||B||^2 = {-Bn:.4f} | {multiset(alpha)}',
           f'   curl0 (dim {len(kappa)}): sum g = {g(kappa).sum():.4f} vs -||B||^2-2(n-nS) = {-Bn-2*(n-nS):.4f}'
           f' | strictly inside: {(g(kappa) < -1e-7).sum()} | {multiset(kappa)}',
           f'   ({time.time()-t0:.1f}s)']
    print('\n'.join(out), flush=True)


if __name__ == '__main__':
    cases = [('srg9', graphs.srg9()),
             ('H(3,3)', json.load(open('../data/t2_untwisted.json'))),
             ('twist t=2 (20)', json.load(open('../data/t2_twisted.json'))),
             ('twist t=3 (39)', json.load(open('../data/t3_twisted.json'))),
             ('twist t=3 (42)', json.load(open('../data/t3_twisted_42.json')))]
    q = 5
    N = q * q + q + 1
    D = ti.singer(q)
    cases.append(('tri-inc t=5 (93)', ti.build(N, D, sorted(D), sorted((12 * d + 26) % N for d in D))))
    if '--big' in sys.argv:
        cases.append(('BvLS', graphs.bvls()))
    for name, A in cases:
        analyse(name, A)
