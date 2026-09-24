"""Tri-incidence ansatz (S, -2S, S) over Z_N, t = |S| - 1: parts P0,P1,P2 = Z_N, edges P_i -> P_{i+1} by
difference sets D_0 = S, D_1 = -2S, D_2 = S (as found for q = 3 by SAT). Enumerate Sidon sets S (all pairwise
differences distinct) up to affine equivalence, test the local axioms (lambda = 1, mu in {0,2}), twist.
Also tests the general 'rotated' variants (-2S, S, S) etc. implicitly (they are relabellings).
Usage: python sidon_tri.py k Nmin Nmax      (k = |S| = t + 1)
"""
import sys, math
import numpy as np


def sidon_sets(N, k):
    """backtracking: S contains 0 and 1, elements increasing, all differences distinct mod N (Sidon)."""
    out = []

    def rec(S, diffs, start):
        if len(S) == k:
            out.append(tuple(S))
            return
        for x in range(start, N):
            nd = []
            ok = True
            for s in S:
                for d in ((x - s) % N, (s - x) % N):
                    if d in diffs or d in nd:
                        ok = False
                        break
                    nd.append(d)
                if not ok:
                    break
            if ok:
                rec(S + [x], diffs | set(nd), x + 1)
    rec([0, 1], {1, N - 1}, 2)
    return out


def canon(S, N):
    best = None
    for u in range(1, N):
        if math.gcd(u, N) != 1:
            continue
        T = sorted((u * s) % N for s in S)
        for c in T:
            U = tuple(sorted((x - c) % N for x in T))
            if best is None or U < best:
                best = U
    return best


def build(N, Ds):
    n = 3 * N
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(3):
        j = (i + 1) % 3
        for a in range(N):
            for d in Ds[i]:
                u, v = i * N + a, j * N + (a + d) % N
                A[u, v] = A[v, u] = 1
    return A


def main():
    k, Nmin, Nmax = map(int, sys.argv[1:4])
    import rooted
    for N in range(Nmin, Nmax + 1):
        cands = sidon_sets(N, k)
        seen = set()
        good = 0
        for S in cands:
            c = canon(S, N)
            if c in seen:
                continue
            seen.add(c)
            S = list(c)
            D = [S, sorted((-2 * s) % N for s in S), S]
            if len(set(D[1])) < k:
                continue
            A = build(N, D)
            if (A.sum(1) != 2 * k).any():
                continue
            A2 = A @ A
            off = ~np.eye(len(A), dtype=bool)
            lam = set(A2[(A == 1) & off].tolist())
            mu = set(A2[(A == 0) & off].tolist())
            if lam == {1} and mu <= {0, 2}:
                good += 1
                R = rooted.Rooted(A, 0)
                print(f'  N={N} S={S}: VALID, {"TWISTED" if not R.is_mate_system() else "untwisted"}', flush=True)
        print(f'k={k} N={N}: {len(cands)} Sidon sets with 0,1; {len(seen)} affine classes; valid: {good}', flush=True)


if __name__ == '__main__':
    main()
