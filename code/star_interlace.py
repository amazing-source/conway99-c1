"""Attack F3 x transitions: the induced subgraph S_a = {x} U N(x) U star(a) (27 vertices) of a putative
srg(99,14,1,2) is determined by the matching tau_a relative to the mate matching on L minus {a, abar}.
Isomorphism type of (mate, tau_a) = partition of 6 (cycle half-lengths of mate U tau_a).
Interlacing: lambda_2(S) <= 3 and lambda_min(S) >= -4 in any SRG with eigenvalues 14, 3, -4.
Equality eigenvectors with zero sum extend by zero to eigenvectors of Gamma (star complement lemma).
Also computed for the analogues in srg(9,4,1,2) / srg(243,22,1,2) families (t = 1, 10) as sanity checks.
"""
import itertools, sys
import numpy as np


def partitions(n, maxp=None):
    if maxp is None:
        maxp = n
    if n == 0:
        yield ()
        return
    for p in range(min(n, maxp), 0, -1):
        for rest in partitions(n - p, p):
            yield (p,) + rest


def build_S(t, part):
    """classes 0..t (class 0 contains a = (0,+), abar = (0,-)); other classes 1..t.
    tau_a on labels of classes 1..t built from the partition `part` of t: a part m means m classes
    c_1..c_m arranged in a cycle of mate U tau of length 2m: tau(c_i,+) = (c_{i+1},-)... for m = 1: tau(c,+) = (c,-)."""
    assert sum(part) == t
    labels = [(c, s) for c in range(t + 1) for s in (0, 1)]
    a, ab = (0, 0), (0, 1)
    others = [l for l in labels if l[0] != 0]
    tau = {}
    c0 = 1
    for m in part:
        cl = list(range(c0, c0 + m))
        c0 += m
        # cycle: (c1,0) -tau- (c2,1)? build alternating cycle of length 2m: v0=(c1,0) mate (c1,1) tau (c2,0) mate (c2,1) ... tau back to (c1,0)
        seq = []
        for c in cl:
            seq += [(c, 0), (c, 1)]
        # mate edges: seq[2i]-seq[2i+1]; tau edges: seq[2i+1]-seq[2i+2 mod 2m]
        for i in range(m):
            u, v = seq[2 * i + 1], seq[(2 * i + 2) % (2 * m)]
            tau[u], tau[v] = v, u
    assert all(tau[tau[l]] == l and tau[l] != l for l in others)
    V = ['x'] + labels + [('X', l) for l in others]
    ix = {v: i for i, v in enumerate(V)}
    n = len(V)
    A = np.zeros((n, n), dtype=np.int64)

    def e(u, v):
        A[ix[u], ix[v]] = A[ix[v], ix[u]] = 1
    for l in labels:
        e('x', l)
    for c in range(t + 1):
        e((c, 0), (c, 1))
    for b in others:
        e(a, ('X', b))
        e(b, ('X', b))
    for b in others:
        if tau[b] > b:
            e(('X', b), ('X', tau[b]))
    return A, tau


def main():
    for t, (r, s) in [(6, (3, -4)), (10, (4, -5)), (1, (1, -2))]:
        print(f'--- t = {t}: SRG eigenvalues r = {r}, s = {s}; S_a has {1 + 2*(t+1) + 2*t} vertices')
        for part in partitions(t):
            A, tau = build_S(t, part)
            ev = np.linalg.eigvalsh(A.astype(float))
            l2, lmin = ev[-2], ev[0]
            flag = []
            if l2 > r + 1e-9:
                flag.append('VIOLATES lambda_2 <= r')
            if lmin < s - 1e-9:
                flag.append('VIOLATES lambda_min >= s')
            # eigenvalue r / s with zero-sum eigenvectors
            def zero_sum_mult(theta):
                M = A - theta * np.eye(len(A))
                # null space of [M; 1^T]
                K = np.vstack([M, np.ones((1, len(A)))])
                return len(A) - np.linalg.matrix_rank(K, tol=1e-8)
            print(f'  tau type {part}: lambda_2 = {l2:.4f}, lambda_min = {lmin:.4f}, '
                  f'mult0sum(r)={zero_sum_mult(r)}, mult0sum(s)={zero_sum_mult(s)} {" ".join(flag)}')


if __name__ == '__main__':
    main()
