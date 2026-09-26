"""Canonical components of G(L_c) at a FULL-PIVOT block (tau_c = eta_c): a D-cycle of length l at c gives labels
b_0..b_{2l-1} on an alternating cycle pi/mu (pi = block flip, mu = tau_c = eta_c), and the component has 6l vertices:
interiors b, roots (c+,b), (c-,b).  Edges: b - pi(b); b - (c+,b); b - (c-,b); (c+,b) - (c+,mu b);
(c-,b) - (c-, pi mu pi b); (c+,b) - (c-, pi mu b)  [h(b) = pi eta(b) = pi mu(b)].
sigma: b -> pi b, (c+,b) <-> (c-, pi b).  Reports: Laplacian spectrum over Q, 7-rank of L, of its sigma-even and sigma-odd
parts (d+, d-), for l = 1..6."""
import numpy as np
from fractions import Fraction


def comp(l):
    n = 2 * l
    # labels 0..n-1 on a cycle: pi pairs (0,1),(2,3),...; mu pairs (1,2),(3,4),...,(n-1,0)
    pi = [i ^ 1 for i in range(n)]
    mu = [(i + 1) % n if i % 2 == 1 else (i - 1) % n for i in range(n)]
    if l == 1:
        mu = [1, 0]            # sib: mu = pi on the single block
    assert all(mu[mu[i]] == i for i in range(n))
    V = [('i', b) for b in range(n)] + [('p', b) for b in range(n)] + [('m', b) for b in range(n)]
    idx = {v: k for k, v in enumerate(V)}
    E = set()

    def add(u, v):
        if u != v:
            E.add(frozenset((idx[u], idx[v])))
    for b in range(n):
        add(('i', b), ('i', pi[b]))
        add(('i', b), ('p', b))
        add(('i', b), ('m', b))
        add(('p', b), ('p', mu[b]))
        add(('m', b), ('m', pi[mu[pi[b]]]))
        add(('p', b), ('m', pi[mu[b]]))
    N = len(V)
    A = np.zeros((N, N), int)
    for e in E:
        a, b = tuple(e)
        A[a, b] = A[b, a] = 1
    deg = A.sum(1)
    sig = [idx[('i', pi[b])] for b in range(n)] + [idx[('m', pi[b])] for b in range(n)] + [idx[('p', pi[b])] for b in range(n)]
    return A, deg, sig


def rank_mod(M, p=7):
    M = [[int(x) % p for x in r] for r in M]
    n, m = len(M), len(M[0])
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r


for l in range(1, 7):
    A, deg, sig = comp(l)
    N = len(A)
    assert all(d == 3 for d in deg), deg
    L = np.diag(deg) - A
    ev = sorted(np.round(np.linalg.eigvalsh(L), 6))
    P = np.zeros((N, N), int)
    for i, j in enumerate(sig):
        P[j, i] = 1
    assert (P @ A @ P.T == A).all()
    # even / odd parts: bases (e_v + e_sv), (e_v - e_sv) over orbit representatives
    reps = [v for v in range(N) if v < sig[v]]
    Be = np.array([[1 if (w == v or w == sig[v]) else 0 for w in range(N)] for v in reps])
    Bo = np.array([[1 if w == v else (-1 if w == sig[v] else 0) for w in range(N)] for v in reps])
    Le = Be @ L @ Be.T
    Lo = Bo @ L @ Bo.T
    d_all = N - rank_mod(L)
    d_even = len(reps) - rank_mod(Le)
    d_odd = len(reps) - rank_mod(Lo)
    ncomp = sum(1 for x in ev if abs(x) < 1e-9)
    print('l=%d  vertices %d  components %d  7-kernel dim of L: %d (even %d, odd %d)' % (l, N, ncomp, d_all, d_even, d_odd))
    print('     spectrum', ev)
