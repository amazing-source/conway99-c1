r"""X14 -- Rayleigh bounds on the fully determined 'triangle' supports of a maximally twisted vertex.

At x: 7 classes, 14 labels (c, s), mate m(c,s) = (c, 1-s).  Delta_x = non-mate pairs {u, v}.
Local data (max twist, generic):  tau_u = perfect matching on the 12 labels outside class(u), never pairing b with m(b);
sigma_c (class c) = bijection on labels outside class c with {c0, b} ~ {c1, sigma_c(b)}, sigma_c(b) not in {b, m(b)}.
Two pairs whose class-pairs intersect have a determined adjacency:
  share one label u:        {u,v} ~ {u,w}  iff  w = tau_u(v);
  mate-related via class c: {c0, v} ~ {c1, w}  iff  w = sigma_c(v).
A family of pairs with pairwise intersecting class-pairs is a star (6 class-pairs: the line ball) or a triangle
{ab, bc, ca} of classes (12 pairs).  W = {x} + 14 labels + 12 triangle pairs is fully determined (27 vertices).
Necessary in any srg(99,14,1,2):  lambda_min(A_W) >= -4  and  lambda_max(A_W - (11/99) J) <= 3
(since -4 I <= A <= 3 I + (11/99) J).  Star supports (the line ball) are the control: they must always pass.
Admissibility filter: inside W, lambda <= 1 on edges, mu <= 2 on non-edges, every triangle is a line (<= 1 per edge).
"""
import sys, random, itertools
import numpy as np

LAB = [(c, s) for c in range(7) for s in (0, 1)]
LI = {l: i for i, l in enumerate(LAB)}
mate = lambda l: (l[0], 1 - l[1])


def random_tau(u, rng):
    others = [l for l in LAB if l[0] != u[0]]
    while True:
        rng.shuffle(others)
        t = {}
        ok = True
        for i in range(0, 12, 2):
            b, c = others[i], others[i + 1]
            if c == mate(b):
                ok = False; break
            t[b], t[c] = c, b
        if ok:
            return t


def random_sigma(c, rng):
    others = [l for l in LAB if l[0] != c]
    while True:
        perm = others[:]; rng.shuffle(perm)
        s = dict(zip(others, perm))
        if all(s[b] not in (b, mate(b)) for b in others):
            return s


def build(pairs, tau, sigma):
    """adjacency on x + 14 labels + given pairs (list of frozensets)"""
    n = 15 + len(pairs)
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(14):
        A[0, 1 + i] = A[1 + i, 0] = 1
        A[1 + i, 1 + LI[mate(LAB[i])]] = 1
    for j, P in enumerate(pairs):
        for u in P:
            A[1 + LI[u], 15 + j] = A[15 + j, 1 + LI[u]] = 1
    for j1, j2 in itertools.combinations(range(len(pairs)), 2):
        P, Q = pairs[j1], pairs[j2]
        common = P & Q
        adj = False
        if len(common) == 1:
            u = next(iter(common)); v = next(iter(P - common)); w = next(iter(Q - common))
            adj = (tau[u][v] == w)
        elif not common:
            for u in P:
                if mate(u) in Q:
                    c = u[0]; v = next(iter(P - {u})); w = next(iter(Q - {mate(u)}))
                    if u[1] == 0:
                        adj = adj or (sigma[c][v] == w)
                    else:
                        adj = adj or (sigma[c][w] == v)
        if adj:
            A[15 + j1, 15 + j2] = A[15 + j2, 15 + j1] = 1
    return A


def admissible(A):
    A2 = A @ A; n = len(A); off = ~np.eye(n, dtype=bool)
    return (A2[(A == 1) & off] <= 1).all() and (A2[(A == 0) & off] <= 2).all()


def bounds(A):
    n = len(A)
    lmin = np.linalg.eigvalsh(A.astype(float)).min()
    lmax = np.linalg.eigvalsh(A.astype(float) - (11 / 99) * np.ones((n, n))).max()
    return lmin, lmax


def main(seed=1, trials=300):
    rng = random.Random(seed)
    stats = dict(configs=0, tri_tested=0, tri_viol=0, star_tested=0, star_viol=0, inadm=0)
    worst = (0, None)
    for _ in range(trials):
        tau = {u: random_tau(u, rng) for u in LAB}
        sigma = {c: random_sigma(c, rng) for c in range(7)}
        stats['configs'] += 1
        for tri in itertools.combinations(range(7), 3):
            pairs = [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]
            A = build(pairs, tau, sigma)
            if not admissible(A):
                stats['inadm'] += 1; continue
            stats['tri_tested'] += 1
            lmin, lmax = bounds(A)
            if lmin < -4 - 1e-9 or lmax > 3 + 1e-9:
                stats['tri_viol'] += 1
                excess = max(-4 - lmin, lmax - 3)
                if excess > worst[0]:
                    worst = (excess, (tri, lmin, lmax))
        for c in range(7):
            pairs = [frozenset({(c, s), l}) for s in (0, 1) for l in LAB if l[0] != c]
            A = build(pairs, tau, sigma)
            if not admissible(A):
                continue
            stats['star_tested'] += 1
            lmin, lmax = bounds(A)
            stats['star_viol'] += (lmin < -4 - 1e-9 or lmax > 3 + 1e-9)
    print(stats)
    print('largest violation (excess, (triangle, lmin, lmax)):', worst)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1, int(sys.argv[2]) if len(sys.argv) > 2 else 300)
