"""Twisted local-axiom geometries from planar difference sets ('tri-incidence').
Vertices (i, a), i in Z_3 (part), a in Z_N, N = q^2+q+1. Edges between parts i and i+1: (i,a) ~ (i+1, a + d), d in D_i.
D_0 = D (a Singer/planar difference set), D_1 = u*D (normalised shift, by relabelling part 2), D_2 = v*D + c.
Checks the local axioms (lambda = 1, mu in {0,2}); reports twisted / untwisted and distance profile.
The 39-vertex twisted t=3 graph found by SAT is D_0 = {0,1,4,6}, D_1 = {0,1,5,11}, D_2 = {0,1,4,6} over Z_13.
"""
import sys, itertools
import numpy as np


def singer(q):
    """planar difference set of order q (q prime power) by brute force over small N."""
    N = q * q + q + 1
    for D in itertools.combinations(range(1, N), q):
        D = (0,) + D
        diffs = sorted((a - b) % N for a in D for b in D if a != b)
        if diffs == list(range(1, N)):
            return list(D)
    return None


def build(N, D0, D1, D2):
    n = 3 * N
    A = np.zeros((n, n), dtype=np.int64)
    Ds = [D0, D1, D2]
    for i in range(3):
        j = (i + 1) % 3
        for a in range(N):
            for d in Ds[i]:
                u, v = i * N + a, j * N + (a + d) % N
                A[u, v] = A[v, u] = 1
    return A


def axioms(A):
    A2 = A @ A
    n = len(A)
    off = ~np.eye(n, dtype=bool)
    return set(A2[(A == 1) & off].tolist()), set(A2[(A == 0) & off].tolist())


def main():
    import rooted, networkx as nx
    from collections import Counter
    for q in map(int, sys.argv[1:] or ['2', '3', '4', '5', '7']):
        N = q * q + q + 1
        D = singer(q)
        units = [u for u in range(1, N) if np.gcd(u, N) == 1]
        found = {}
        for u in units:
            D1 = sorted((u * d) % N for d in D)
            for v in units:
                for c in range(N):
                    D2 = sorted((v * d + c) % N for d in D)
                    A = build(N, D, D1, D2)
                    lam, mu = axioms(A)
                    if lam == {1} and mu <= {0, 2}:
                        R = rooted.Rooted(A, 0)
                        tw = not R.is_mate_system()
                        G = nx.from_numpy_array(A)
                        dd = tuple(sorted(Counter(nx.single_source_shortest_path_length(G, 0).values()).items()))
                        key = (tw, dd)
                        found.setdefault(key, (u, v, c))
        print(f'q={q} N={N} D={D}: {len(found)} classes of valid tri-incidences', flush=True)
        for (tw, dd), ex in found.items():
            print('   ', 'TWISTED' if tw else 'untwisted', 'distance profile', dd, 'example (u,v,c) =', ex)


if __name__ == '__main__':
    main()
