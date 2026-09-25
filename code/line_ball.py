r"""Line ball reduction for the 7-adic invariant k (notes/99).

For a line L = {x, a, abar}, the 36 points adjacent to exactly one point of L split as X0 = N(x)\L (the 12 labels),
X1 = star(a), X2 = star(abar).  The induced graph G(L) on these 36 points is cubic: one matching inside each part
(lines through x, a, abar: mate involution m, tau_a, tau_abar) and the Lou-Murin 2-factor C(L) between the parts
(b -- {a,b} -- {abar, sigma(b)} -- sigma(b)).  Claim (proved by hand in notes/99):
    rank_7(two-star block S24 of M_x) = rank_7(A_G - 3I) - 13,
so  k >= 23 - d(L),  d(L) = dim ker_7(A_{G(L)} - 3I)  (>= number of components of G(L)).
This script checks the identity on random configurations and reports d(L) statistics.
Coordinates: labels (c, s), c = 1..6 class, s = 0/1; X0 = label b, X1 = {a,b}, X2 = {abar,b}.
"""
import sys, itertools, random
import numpy as np
import kbound_star as ks

p = 7
others = ks.others                    # 12 labels
oi = ks.oi
mate = ks.mate


def rank_mod(M, q=p):
    M = np.array(M, dtype=np.int64) % q
    r = 0; rows, cols = M.shape
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if nz.size == 0:
            continue
        i = r + nz[0]
        M[[r, i]] = M[[i, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, q)) % q
        col = M[:, c].copy(); col[r] = 0
        nzr = np.nonzero(col)[0]
        if nzr.size:
            M[nzr] = (M[nzr] - np.outer(col[nzr], M[r])) % q
        r += 1
        if r == rows:
            break
    return r


def random_matching(rng):
    L = others[:]; rng.shuffle(L)
    t = {}
    for i in range(0, 12, 2):
        t[L[i]], t[L[i + 1]] = L[i + 1], L[i]
    return t


def cubic_graph(tau_a, tau_ab, sigma):
    """adjacency of G(L) on 36 vertices: index 12*part + oi[label]; X2 vertex b means {abar, b}."""
    A = np.zeros((36, 36), dtype=np.int64)
    def e(u, v):
        A[u, v] = A[v, u] = 1
    for b in others:
        e(oi[b], oi[mate(b)])                        # lines through x
        e(12 + oi[b], 12 + oi[tau_a[b]])             # lines through a
        e(24 + oi[b], 24 + oi[tau_ab[b]])            # lines through abar
        e(oi[b], 12 + oi[b])                         # b ~ {a,b}
        e(oi[b], 24 + oi[b])                         # b ~ {abar,b}
        e(12 + oi[b], 24 + oi[sigma[b]])             # {a,b} ~ {abar, sigma(b)}
    assert (A.sum(1) == 3).all()
    return A


def two_star_block(tau_a, tau_ab, sigma):
    """S24 = [[H_tau_a + P' + J, Pi + 3I + P' - J], [.., H_tau_abar + P' + J]] mod 7 (notes/97)."""
    n = 12
    Pm = np.zeros((n, n), dtype=np.int64); Ta = Pm.copy(); Tb = Pm.copy(); Pi = Pm.copy()
    for b in others:
        Pm[oi[b], oi[mate(b)]] = 1; Ta[oi[b], oi[tau_a[b]]] = 1; Tb[oi[b], oi[tau_ab[b]]] = 1
        Pi[oi[b], oi[sigma[b]]] = 1
    I = np.eye(n, dtype=np.int64); J = np.ones((n, n), dtype=np.int64)
    top = np.concatenate([Ta + Pm + J, Pi + 3 * I + Pm - J], axis=1)
    bot = np.concatenate([(Pi + 3 * I + Pm - J).T, Tb + Pm + J], axis=1)
    return np.concatenate([top, bot], axis=0) % p


def full_ball(tau_a, tau_ab, sigma):
    """A - 3I on the 39-vertex ball L + N(L): vertices x, a, abar, then the 36 of G(L)."""
    G = cubic_graph(tau_a, tau_ab, sigma)
    A = np.zeros((39, 39), dtype=np.int64)
    A[3:, 3:] = G
    for i in range(3):
        for j in range(3):
            if i != j:
                A[i, j] = 1
        A[i, 3 + 12 * i: 3 + 12 * (i + 1)] = 1
        A[3 + 12 * i: 3 + 12 * (i + 1), i] = 1
    return A - 3 * np.eye(39, dtype=np.int64)


def local_ok(tau_a, tau_ab, sigma):
    """lambda <= 1 on edges and mu <= 2 on non-edges, triangles only on lines, inside the 39-vertex ball."""
    A = full_ball(tau_a, tau_ab, sigma) + 3 * np.eye(39, dtype=np.int64)
    A2 = A @ A
    off = ~np.eye(39, dtype=bool)
    if (A2[(A == 1) & off] > 1).any():
        return False
    if (A2[(A == 0) & off] > 2).any():
        return False
    return True


def ncomp(A):
    n = len(A); seen = [False] * n; c = 0
    for s in range(n):
        if seen[s]:
            continue
        c += 1; st = [s]; seen[s] = True
        while st:
            u = st.pop()
            for v in np.nonzero(A[u])[0]:
                if not seen[v]:
                    seen[v] = True; st.append(v)
    return c


def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    from collections import Counter
    stats = Counter(); bad = 0; okc = 0
    for _ in range(trials):
        ta, tb = random_matching(rng), random_matching(rng)
        perm = others[:]; rng.shuffle(perm)
        sigma = {b: perm[i] for i, b in enumerate(others)}
        r24 = rank_mod(two_star_block(ta, tb, sigma))
        G = cubic_graph(ta, tb, sigma)
        rG = rank_mod(G - 3 * np.eye(36, dtype=np.int64))
        rB = rank_mod(full_ball(ta, tb, sigma))
        if not (r24 == rG - 13 and rB == 15 + r24 and rB == 2 + rG):
            bad += 1
        ok = local_ok(ta, tb, sigma); okc += ok
        stats[(36 - rG, ncomp(G), ok)] += 1
    print(f'identity failures: {bad} / {trials};  locally admissible: {okc}')
    for (d, c, ok), m in sorted(stats.items()):
        print(f'  d={d:2d} components={c:2d} admissible={ok}: {m}')


if __name__ == '__main__':
    main()


def climb(seed, iters, restarts):
    """local search maximising d(L) over locally admissible (tau_a, tau_abar, sigma)."""
    rng = random.Random(seed)
    best_global = (0, None)
    def dval(ta, tb, sg):
        return 36 - rank_mod(cubic_graph(ta, tb, sg) - 3 * np.eye(36, dtype=np.int64))
    def mutate(ta, tb, sg):
        ta, tb, sg = dict(ta), dict(tb), dict(sg)
        w = rng.randrange(3)
        if w < 2:
            t = ta if w == 0 else tb
            u, v = rng.sample(others, 2)
            if t[u] == v:
                return ta, tb, sg
            pu, pv = t[u], t[v]
            t[u], t[v], t[pu], t[pv] = pv, pu, v, u      # 2-switch
        else:
            u, v = rng.sample(others, 2)
            sg[u], sg[v] = sg[v], sg[u]
        return ta, tb, sg
    for r in range(restarts):
        ta, tb = random_matching(rng), random_matching(rng)
        perm = others[:]; rng.shuffle(perm); sg = {b: perm[i] for i, b in enumerate(others)}
        while not local_ok(ta, tb, sg):
            ta, tb, sg = mutate(ta, tb, sg)
        cur = dval(ta, tb, sg)
        for it in range(iters):
            na, nb, ns = mutate(ta, tb, sg)
            if not local_ok(na, nb, ns):
                continue
            dv = dval(na, nb, ns)
            if dv >= cur or rng.random() < 0.02:
                ta, tb, sg, cur = na, nb, ns, dv
                if cur > best_global[0]:
                    best_global = (cur, (dict(ta), dict(tb), dict(sg)))
    return best_global
