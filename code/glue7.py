"""F5 x C: 7-adic gluing at a root x.
Over Z_7: Z^99 = K (+) K^perp orthogonally, K = ker(B) cap Z^84 (the 70-space, 7 does not divide det),
K^perp = span{e_x, e_a (a in N(x)), B^T e_a} (saturated at 7). A - 3I preserves both, so
  rank_7(A - 3I) = k(x) + k',  k(x) = rank_7((H - 3I)|_K),  k' = rank_7((A - 3I)|_{K^perp}).
The action of A on K^perp is forced by the rooted combinatorics (no dependence on tau or H):
  A e_x = sum_a e_a ;  A e_a = e_x + e_abar + B^T e_a ;
  A B^T e_a = (k-2) e_a + sum_{b != a, abar} e_b + sum_{b != a, abar} B^T e_b.
This script computes k' for the (lambda, mu) = (1, 2) family and checks the formula on srg(9,4,1,2) and
srg(243,22,1,2) by computing the full ranks directly (primes p dividing r - s).
"""
import numpy as np
import graphs, rooted


def rank_mod(M, p):
    M = np.array(M, dtype=np.int64) % p
    r = 0
    rows, cols = M.shape
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i, c]), None)
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        for i in np.nonzero(M[:, c])[0]:
            if i != r:
                M[i] = (M[i] - M[i, c] * M[r]) % p
        r += 1
        if r == rows:
            break
    return r


def kperp_matrix(t, theta):
    """matrix of (A - theta I) on the basis e_x, e_a (a = 0..2t+1), f_a = B^T e_a; mate(a) = a ^ 1.
    column j = image of basis vector j."""
    m = 2 * (t + 1)
    k = 2 * (t + 1)
    N = 1 + 2 * m
    X, E, F = 0, lambda a: 1 + a, lambda a: 1 + m + a
    M = np.zeros((N, N), dtype=np.int64)
    for a in range(m):
        M[E(a), X] += 1
    for a in range(m):
        M[X, E(a)] += 1
        M[E(a ^ 1), E(a)] += 1
        M[F(a), E(a)] += 1
    for a in range(m):
        M[E(a), F(a)] += k - 2
        for b in range(m):
            if b not in (a, a ^ 1):
                M[E(b), F(a)] += 1
                M[F(b), F(a)] += 1
    M -= theta * np.eye(N, dtype=np.int64)
    return M


def main():
    # consistency check of the K^perp action on the controls (exact over Z): compare with the real A
    for name, t in [('srg9', 1), ('bvls', 10)]:
        A = graphs.ALL[name]()
        R = rooted.Rooted(A, 0)
        n = len(A)
        L = R.L
        # relabel labels so that mate(a) = a ^ 1
        order = []
        for a, ab in R.classes():
            order += [a, ab]
        basis = [np.eye(n, dtype=np.int64)[R.x]]
        basis += [np.eye(n, dtype=np.int64)[a] for a in order]
        for a in order:
            v = np.zeros(n, dtype=np.int64)
            for u in R.X:
                if a in R.label[u]:
                    v[u] = 1
            basis.append(v)
        Bm = np.array(basis).T  # n x N
        Mk = kperp_matrix(t, 0)
        ok = np.array_equal(A @ Bm, Bm @ Mk)
        print(f'{name}: forced K^perp action matches the real graph: {ok}')
    # k' for 99 and the parity consequence
    t, theta, p = 6, 3, 7
    Mk = kperp_matrix(t, theta)
    kp = rank_mod(Mk, p)
    print(f'srg(99,14,1,2): k\' = rank_7((A-3I)|K^perp) = {kp} (dimension {len(Mk)})')
    print('  => rank_7(A-3I) = k(x) + k\'; with rank_7(A-3I) odd (lemma F5): k(x) parity =', (1 - kp) % 2)
    # sanity on controls: full rank vs k' + k, p | r - s
    for name, t, theta, p in [('srg9', 1, 1, 3), ('bvls', 10, 4, 3)]:
        A = graphs.ALL[name]()
        full = rank_mod(A - theta * np.eye(len(A), dtype=np.int64), p)
        kp = rank_mod(kperp_matrix(t, theta), p)
        print(f'{name}: rank_{p}(A - {theta}I) = {full}, k\' = {kp} (the split K+K^perp needs p prime to det, check separately)')


if __name__ == '__main__':
    main()
