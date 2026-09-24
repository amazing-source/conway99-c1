"""Lower bound for the global 7-adic invariant k = rank_7(A - 3I) - 15 (L19) from the star of a label.

At a vertex x, the principal submatrix of A - 3I on B1(x) U star(a) (star(a) = the 12 vertices of Gamma_2(x) having
label a) is determined by tau_a alone: B1(x) is the windmill, labels are known, and inside star(a) the adjacency is the
tau_a matching.  Since the windmill block (F - 3I) is invertible mod 7 (det 2^23), rank_7(A - 3I) >= 15 + rank_7(S)
with S the Schur complement, hence k >= rank_7(S).  This script tabulates rank_7(S) over all 10395 matchings tau_a,
by 'class type' (2-regular multigraph induced on the 6 other classes; a loop = untwisted class).
"""
import itertools, numpy as np
from collections import Counter, defaultdict
import networkx as nx

p = 7
labels = [(c, s) for c in range(7) for s in (0, 1)]
B1 = ['x'] + labels
idx = {v: i for i, v in enumerate(B1)}
mate = lambda l: (l[0], 1 - l[1])


def inv_mod(M, p):
    n = len(M); A = np.concatenate([M % p, np.eye(n, dtype=np.int64)], axis=1)
    for c in range(n):
        piv = next(r for r in range(c, n) if A[r, c] % p)
        A[[c, piv]] = A[[piv, c]]; A[c] = (A[c] * pow(int(A[c, c]), -1, p)) % p
        for r in range(n):
            if r != c and A[r, c]:
                A[r] = (A[r] - A[r, c] * A[c]) % p
    return A[:, n:]


def rank_mod(M, p):
    A = M.copy() % p; r = 0; n, m = A.shape
    for c in range(m):
        piv = next((i for i in range(r, n) if A[i, c] % p), None)
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]; A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        for i in range(n):
            if i != r and A[i, c]:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
    return r


def matchings(lst):
    if not lst:
        yield []; return
    f = lst[0]
    for i in range(1, len(lst)):
        for rest in matchings(lst[1:i] + lst[i + 1:]):
            yield [(f, lst[i])] + rest


def class_type(m):
    """(number of untwisted classes, sorted cycle lengths of the class multigraph on the twisted classes)."""
    loops = sum(1 for b, c in m if b[0] == c[0])
    G = nx.MultiGraph()
    for b, c in m:
        if b[0] != c[0]:
            G.add_edge(b[0], c[0])
    comps = sorted(len(C) for C in nx.connected_components(G))
    return loops, tuple(comps)


def main():
    F = np.zeros((15, 15), dtype=np.int64)
    for l in labels:
        F[0, idx[l]] = F[idx[l], 0] = 1
        F[idx[l], idx[mate(l)]] = 1
    Finv = inv_mod((F - 3 * np.eye(15, dtype=np.int64)) % p, p)
    assert round(np.linalg.det(F - 3 * np.eye(15))) == -2 ** 23 or round(abs(np.linalg.det(F - 3 * np.eye(15)))) == 2 ** 23
    a = (0, 0); others = [l for l in labels if l[0] != 0]
    Mp = np.zeros((15, 12), dtype=np.int64)
    for j, b in enumerate(others):
        Mp[idx[a], j] = 1; Mp[idx[b], j] = 1
    C0 = (Mp.T @ Finv @ Mp) % p
    single = rank_mod((np.array([[-3]]) - Mp[:, :1].T @ Finv @ Mp[:, :1]) % p, p)
    print('single vertex of Gamma_2(x): rank_7 of Schur complement =', single, '(=> k >= 1, so k >= 2 by parity)')
    tab = defaultdict(Counter)
    for m in matchings(others):
        H = np.zeros((12, 12), dtype=np.int64)
        for b, c in m:
            i, j = others.index(b), others.index(c); H[i, j] = H[j, i] = 1
        r = rank_mod((H - 3 * np.eye(12, dtype=np.int64) - C0) % p, p)
        tab[class_type(m)][r] += 1
    print('class type (untwisted classes, cycle lengths of the class graph) -> rank_7 distribution:')
    for t in sorted(tab):
        print('  ', t, dict(tab[t]))


if __name__ == '__main__':
    main()
