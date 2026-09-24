"""Search twisted local-axiom Cayley graphs on Frobenius groups F_{3p} = Z_p x| Z_3 (p = 1 mod 3).
Elements (a, i), product (a,i)(b,j) = (a + w^i b, i + j), w a primitive cube root of unity mod p.
Lines through e are taken to be subgroups of order 3: H_a = {e, (a,1), (a,1)^2}; S = union over a in A.
Local axioms: lambda = 1 (N(e) = (t+1)K2, no other triangles), mu in {0, 2}.
Reports whether the graph is twisted (tau != mate at e) and its distance distribution.
Usage: python cayley_frobenius.py p t [max_orbits]
"""
import itertools, sys, random
import numpy as np


def group(p):
    w = next(x for x in range(2, p) if pow(x, 3, p) == 1)
    els = [(a, i) for i in range(3) for a in range(p)]
    ix = {g: k for k, g in enumerate(els)}
    wp = [1, w, w * w % p]

    def mul(g, h):
        return ((g[0] + wp[g[1]] * h[0]) % p, (g[1] + h[1]) % 3)
    return els, ix, mul, w


def cayley(p, A):
    els, ix, mul, w = group(p)
    S = []
    for a in A:
        g = (a, 1)
        S += [g, mul(g, g)]
    n = len(els)
    M = np.zeros((n, n), dtype=np.int64)
    for g in els:
        for s in S:
            M[ix[g], ix[mul(g, s)]] = 1
    return M, S


def check(M):
    if not (M == M.T).all():
        return None
    A2 = M @ M
    n = len(M)
    off = ~np.eye(n, dtype=bool)
    lam = set(A2[(M == 1) & off].tolist())
    mu = set(A2[(M == 0) & off].tolist())
    return lam, mu


def canon_orbits(p, k):
    """representatives of k-subsets of Z_p up to the affine group x -> u x + v (acts on the subgroups H_a
    by automorphisms of F_{3p}: (a,i) -> (u a + v - w^i v, i) is an automorphism; H_a -> H_{ua + (1-w)v}...)."""
    seen = set()
    reps = []
    for A in itertools.combinations(range(p), k):
        if A in seen:
            continue
        orb = set()
        for u in range(1, p):
            for v in range(p):
                orb.add(tuple(sorted((u * a + v) % p for a in A)))
        seen |= orb
        reps.append(A)
    return reps


def main():
    p, t = int(sys.argv[1]), int(sys.argv[2])
    maxo = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
    k = t + 1
    import rooted
    found = 0
    if p <= 19:
        reps = canon_orbits(p, k)
    else:
        rng = random.Random(0)
        reps = [tuple(sorted([0, 1] + rng.sample(range(2, p), k - 2))) for _ in range(maxo)]
    for A in reps[:maxo]:
        M, S = cayley(p, A)
        c = check(M)
        if c is None:
            continue
        lam, mu = c
        if lam == {1} and mu <= {0, 2}:
            R = rooted.Rooted(M, 0)
            tw = not R.is_mate_system()
            import networkx as nx
            G = nx.from_numpy_array(M)
            from collections import Counter
            dd = Counter(nx.single_source_shortest_path_length(G, 0).values())
            print('A =', A, 'twisted' if tw else 'untwisted', 'distance distribution', dict(sorted(dd.items())), flush=True)
            found += 1
    print('checked', min(len(reps), maxo), 'found', found)


if __name__ == '__main__':
    main()
