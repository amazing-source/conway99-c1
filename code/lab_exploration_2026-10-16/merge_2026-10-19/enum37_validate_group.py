"""Independent checks of the group-action formulas used by enum37 (LAB 20/10/2026, NOTE_ENUM37.md section 1).

A structure on V = {0,1,2} x [n] is a graph: three within-class perfect matchings M0, M1, M2 and three cross matchings
(s01: C0 -> C1, s12: C1 -> C2, s20: C2 -> C0).  An element phi = (tau; pi0, pi1, pi2) of W = S_n wr S3 acts by
phi(c, i) = (tau(c), pi_c(i)) on the GRAPH; here everything is recomputed from the image edge set (no formula used), and
compared with:
  (a) the bijection formulas: forward pair (a,b) -> if (tau a, tau b) is forward: s'_{tau a, tau b} = pi_b s_ab pi_a^-1,
      else s'_{tau b, tau a} = pi_a s_ab^-1 pi_b^-1;
  (b) the stabiliser A_lambda of F_lambda = (id, id, sigma) (six cosets, see enum37_burnside.py) and the six images
      of the matching triple;
  (c) the invariant: sigma' = s20' s12' s01' is conjugate to sigma (tau even) or sigma^-1 (tau odd);
  (d) the K >= 0 criterion: K = n I - G - G^2 + 2J - J_cl >= 0  <=>  no sigma-edge {i, sigma(i)} (sigma(i) != i) lies in
      M0 n M1, in M1 n M2 or in sigma(M2) n M0  (for the canonical cross structure F_lambda);
  (e) the conversion of (lambda; M0, M1, M2) to the 36-integer standard form and back (same graph up to relabelling).
usage: python enum37_validate_group.py [trials=2000] [seed=1]
"""
import random
import sys

import numpy as np

TAUS = [(0, 1, 2), (1, 2, 0), (2, 0, 1), (0, 2, 1), (1, 0, 2), (2, 1, 0)]   # tau as the image list tau[c]
FWD = [(0, 1), (1, 2), (2, 0)]


def inv(p):
    r = [0] * len(p)
    for i, j in enumerate(p):
        r[j] = i
    return r


def comp(a, b):  # a o b
    return [a[b[i]] for i in range(len(b))]


def rand_pm(n, rng):
    pts = list(range(n))
    rng.shuffle(pts)
    p = [0] * n
    for j in range(0, n, 2):
        p[pts[j]] = pts[j + 1]
        p[pts[j + 1]] = pts[j]
    return p                      # partner function


def std_pm(n):
    return [i ^ 1 for i in range(n)]


def graph_edges(n, M, s):
    """M = [M0, M1, M2] partner functions, s = {(0,1): s01, (1,2): s12, (2,0): s20}"""
    E = set()
    for c in range(3):
        for i in range(n):
            E.add(frozenset({(c, i), (c, M[c][i])}))
    for (a, b), sab in s.items():
        for i in range(n):
            E.add(frozenset({(a, i), (b, sab[i])}))
    return E


def read_structure(n, E):
    M = [[None] * n for _ in range(3)]
    s = {ab: [None] * n for ab in FWD}
    for e in E:
        (c1, i1), (c2, i2) = tuple(e)
        if c1 == c2:
            M[c1][i1] = i2
            M[c1][i2] = i1
        else:
            if (c1, c2) in s:
                s[(c1, c2)][i1] = i2
            else:
                s[(c2, c1)][i2] = i1
    return M, s


def act_graph(n, tau, pis, E):
    return {frozenset({(tau[c], pis[c][i]) for (c, i) in e}) for e in E}


def act_formula(n, tau, pis, s):
    out = {}
    for (a, b) in FWD:
        ta, tb = tau[a], tau[b]
        if (ta, tb) in FWD:
            out[(ta, tb)] = comp(pis[b], comp(s[(a, b)], inv(pis[a])))
        else:
            out[(tb, ta)] = comp(pis[a], comp(inv(s[(a, b)]), inv(pis[b])))
    return out


def ctype(p):
    n = len(p)
    seen = [False] * n
    t = []
    for i in range(n):
        if not seen[i]:
            L, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                L += 1
            t.append(L)
    return tuple(sorted(t, reverse=True))


def canonical_sigma(lam):
    n = sum(lam)
    p = list(range(n))
    pos = 0
    starts = []
    for L in lam:
        starts.append(pos)
        for j in range(L):
            p[pos + j] = pos + (j + 1) % L
        pos += L
    return p, starts


def rand_centralizer(lam, rng, reverser=False):
    """random element of C(sigma) (or of the reverser coset R(sigma)) via the wreath product structure"""
    sig, starts = canonical_sigma(lam)
    n = len(sig)
    g = [None] * n
    by_len = {}
    for j, L in enumerate(lam):
        by_len.setdefault(L, []).append(j)
    for L, cycles in by_len.items():
        perm = cycles[:]
        rng.shuffle(perm)
        for j, jj in zip(cycles, perm):
            b = rng.randrange(L)
            for x in range(L):
                y = (b - x) % L if reverser else (x + b) % L
                g[starts[j] + x] = starts[jj] + y
    return g, sig


def apply_pm(g, M):
    r = [0] * len(M)
    for i in range(len(M)):
        r[g[i]] = g[M[i]]
    return r


def k_ok(n, M, s):
    N = 3 * n
    G = np.zeros((N, N), dtype=np.int64)
    for c in range(3):
        for i in range(n):
            G[c * n + i, c * n + M[c][i]] = 1
    for (a, b), sab in s.items():
        for i in range(n):
            G[a * n + i, b * n + sab[i]] = G[b * n + sab[i], a * n + i] = 1
    assert (G.sum(axis=1) == 3).all()
    Jcl = np.zeros((N, N), dtype=np.int64)
    for c in range(3):
        Jcl[c * n:(c + 1) * n, c * n:(c + 1) * n] = 1
    K = n * np.eye(N, dtype=np.int64) - G - G @ G + 2 * np.ones((N, N), dtype=np.int64) - Jcl
    return bool((K >= 0).all())


def k_ok_sigma_edges(n, sig, M):
    sedges = {frozenset({i, sig[i]}) for i in range(n) if sig[i] != i}
    e = lambda P: {frozenset({i, P[i]}) for i in range(n)}
    E0, E1, E2 = e(M[0]), e(M[1]), e(M[2])
    E2s = {frozenset({sig[a] for a in ed}) for ed in E2}
    return not ((E0 & E1 & sedges) or (E1 & E2 & sedges) or (E2s & E0 & sedges))


def to_standard(n, sig, M):
    """relabel each class so that M_c becomes i <-> i^1; returns (s01, s12, s20) of F = (id, id, sigma)"""
    psi = []
    for c in range(3):
        p = [None] * n
        k = 0
        for i in range(n):
            if p[i] is None:
                p[i], p[M[c][i]] = 2 * k, 2 * k + 1
                k += 1
        psi.append(p)
    s01 = comp(psi[1], inv(psi[0]))
    s12 = comp(psi[2], inv(psi[1]))
    s20 = comp(psi[0], comp(sig, inv(psi[2])))
    return s01, s12, s20, psi


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    n = 12
    lams = [(12,), (11, 1), (6, 6), (4, 4, 4), (3, 3, 3, 3), (5, 4, 2, 1), (2, 2, 2, 2, 2, 2), (3, 2, 1, 1, 1, 1, 1, 1, 1),
            (1,) * 12, (6, 3, 2, 1), (7, 5), (2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), (10, 2), (10, 1, 1)]
    bad = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0}
    kstat = [0, 0]
    for t in range(T):
        # (a) + (c): arbitrary structure, arbitrary phi
        M = [rand_pm(n, rng) for _ in range(3)]
        s = {ab: rng.sample(range(n), n) for ab in FWD}
        tau = TAUS[rng.randrange(6)]
        pis = [rng.sample(range(n), n) for _ in range(3)]
        E2 = act_graph(n, tau, pis, graph_edges(n, M, s))
        M2_, s2_ = read_structure(n, E2)
        sf = act_formula(n, tau, pis, s)
        if sf != s2_:
            bad["a"] += 1
        sig = comp(s[(2, 0)], comp(s[(1, 2)], s[(0, 1)]))
        sig2 = comp(s2_[(2, 0)], comp(s2_[(1, 2)], s2_[(0, 1)]))
        if ctype(sig) != ctype(sig2):
            bad["c"] += 1
        # (b): stabiliser of F_lambda and the six images
        lam = lams[t % len(lams)]
        g, sig = rand_centralizer(lam, rng)
        h, _ = rand_centralizer(lam, rng, reverser=True)
        assert comp(g, sig) == comp(sig, g)
        assert comp(h, sig) == comp(inv(sig), h)
        ident = list(range(n))
        F = {(0, 1): ident, (1, 2): ident, (2, 0): sig}
        gs, hs = comp(g, sig), comp(h, sig)
        cases = [  # tau, (pi0, pi1, pi2), claimed image triple of (M0, M1, M2)
            (TAUS[0], (g, g, g), lambda M: (apply_pm(g, M[0]), apply_pm(g, M[1]), apply_pm(g, M[2]))),
            (TAUS[1], (g, g, gs), lambda M: (apply_pm(gs, M[2]), apply_pm(g, M[0]), apply_pm(g, M[1]))),
            (TAUS[2], (g, gs, gs), lambda M: (apply_pm(gs, M[1]), apply_pm(gs, M[2]), apply_pm(g, M[0]))),
            (TAUS[3], (h, hs, hs), lambda M: (apply_pm(h, M[0]), apply_pm(hs, M[2]), apply_pm(hs, M[1]))),
            (TAUS[4], (h, h, hs), lambda M: (apply_pm(h, M[1]), apply_pm(h, M[0]), apply_pm(hs, M[2]))),
            (TAUS[5], (h, h, h), lambda M: (apply_pm(h, M[2]), apply_pm(h, M[1]), apply_pm(h, M[0]))),
        ]
        for tau, pis, img in cases:
            E2 = act_graph(n, tau, list(pis), graph_edges(n, M, F))
            Mi, si = read_structure(n, E2)
            if si != F or tuple(map(tuple, Mi)) != tuple(map(tuple, img(M))):
                bad["b"] += 1
        # (d): K >= 0 criterion on F_lambda
        ok1 = k_ok(n, M, F)
        ok2 = k_ok_sigma_edges(n, sig, M)
        kstat[ok1] += 1
        if ok1 != ok2:
            bad["d"] += 1
        # (e): conversion to the standard form gives the same graph up to the class-wise relabelling psi
        s01, s12, s20, psi = to_standard(n, sig, M)
        Es = graph_edges(n, [std_pm(n)] * 3, {(0, 1): s01, (1, 2): s12, (2, 0): s20})
        if act_graph(n, TAUS[0], psi, graph_edges(n, M, F)) != Es:
            bad["e"] += 1
    print("trials %d, failures %s, K>=0 on F_lambda structures: %d of %d" % (T, bad, kstat[1], T))
    assert all(v == 0 for v in bad.values())


if __name__ == "__main__":
    main()
