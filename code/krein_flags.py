"""Delsarte / Krein LP over FLAG families for srg(99,14,1,2), as a function of P (number of prisms).
Pure mathematics: every number below comes from the local structure; no graph is needed.

Objects: flags f = (x, L), x in L, vector z_f = alpha e_x + beta 1_L projected on an eigenspace (E_{-4}, E_3, or the
weighted sum of both). Pair types of ordered flag pairs and their counts (notes/70):
  A same flag (1), B same line other point (2), C same point other line (6), D lines meet at m, x = m, x' != m (12),
  E lines meet at m, x != m, x' = m (12), F lines meet at m, x, x' != m (24),
  G_e disjoint lines with e edges: ordered line pairs N_e(P) = 7392-2P, 33264+6P, 8316-6P, 2P (e = 0..3),
      9 flag pairs each: e matched pairs, e(e-1) both matched elsewhere, e(3-e) + e(3-e) one matched, (3-e)^2 none.
Primitive data per type: delta=[x=x'], a=A_xx', (in1, nb1) = (x in L', #nbrs of x in L'), (in2, nb2), (m=|L cap L'|, eLL).
For each Gegenbauer degree j and each set of families, the matrix S_ab = sum over pairs G_j(<z_a, z'_b>) must be PSD.
"""
import itertools
import numpy as np

T0 = [  # (count_per_flag, delta, a, in1, nb1, in2, nb2, m, eLL)
    (1, 1, 0, 1, 2, 1, 2, 3, 6),
    (2, 0, 1, 1, 2, 1, 2, 3, 6),
    (6, 1, 0, 1, 2, 1, 2, 1, 4),
    (12, 0, 1, 1, 2, 0, 1, 1, 4),
    (12, 0, 1, 0, 1, 1, 2, 1, 4),
    (24, 0, 0, 0, 1, 0, 1, 1, 4),
]


def types(P):
    out = [(693 * c, d, a, i1, n1, i2, n2, m, ell) for c, d, a, i1, n1, i2, n2, m, ell in T0]
    Ne = {0: 7392 - 2 * P, 1: 33264 + 6 * P, 2: 8316 - 6 * P, 3: 2 * P}
    for e, N in Ne.items():
        sub = [(e, 1, 1, 1), (e * (e - 1), 0, 1, 1), (e * (3 - e), 0, 1, 0), (e * (3 - e), 0, 0, 1), ((3 - e) ** 2, 0, 0, 0)]
        for mult, a, n1, n2 in sub:
            if mult:
                out.append((N * mult, 0, a, 0, n1, 0, n2, 0, e))
    return out


def prim(space):
    if space == -4:
        X = lambda d, a: (3 * d - a + 1 / 9) / 7
        Y = lambda i, nb: (3 * i - nb + 1 / 3) / 7
        Z = lambda m, e: (3 * m - e + 1) / 7
    else:
        X = lambda d, a: (a + 4 * d - 2 / 11) / 7
        Y = lambda i, nb: (nb + 4 * i - 6 / 11) / 7
        Z = lambda m, e: (e + 4 * m - 18 / 11) / 7
    return X, Y, Z


def inner(fam1, fam2, ty):
    """fam = (alpha, beta, w3, w4): vector = w3 * E_3(alpha e_x + beta 1_L) + w4 * E_-4(...)."""
    _, d, a, i1, n1, i2, n2, m, ell = ty
    tot = 0.0
    for space, w1, w2 in ((3, fam1[2], fam2[2]), (-4, fam1[3], fam2[3])):
        if w1 == 0 or w2 == 0:
            continue
        X, Y, Z = prim(space)
        al1, be1, al2, be2 = fam1[0], fam1[1], fam2[0], fam2[1]
        tot += w1 * w2 * (al1 * al2 * X(d, a) + al1 * be2 * Y(i1, n1) + be1 * al2 * Y(i2, n2) + be1 * be2 * Z(m, ell))
    return tot


def geg(j, t, dim):
    p0, p1 = np.ones_like(t), t
    if j == 0:
        return p0
    for i in range(1, j):
        p0, p1 = p1, ((2 * i + dim - 2) * t * p1 - i * p0) / (i + dim - 2)
    return p1


def S_affine(fams, j, dim):
    """S(P) = S0 + P * S1 (counts are affine in P, inner products do not depend on P)."""
    t0, t1 = types(0), types(1)
    selfn = [inner(f, f, t0[0]) for f in fams]
    c0 = np.array([tt[0] for tt in t0], dtype=float)
    c1 = np.array([tt[0] for tt in t1], dtype=float) - c0
    S0 = np.zeros((len(fams), len(fams)))
    S1 = np.zeros_like(S0)
    for x, y in itertools.combinations_with_replacement(range(len(fams)), 2):
        t = np.array([inner(fams[x], fams[y], tt) / np.sqrt(selfn[x] * selfn[y]) for tt in t0])
        g = geg(j, t, dim)
        S0[x, y] = S0[y, x] = (c0 * g).sum()
        S1[x, y] = S1[y, x] = (c1 * g).sum()
    return S0, S1


def report(name, fams, dim, jmax=8):
    Ps = np.arange(0, 1387)
    ok = np.ones(len(Ps), dtype=bool)
    for j in range(1, jmax + 1):
        S0, S1 = S_affine(fams, j, dim)
        for i, P in enumerate(Ps):
            if ok[i]:
                ev = np.linalg.eigvalsh(S0 + P * S1)
                if ev.min() < -1e-7 * max(1.0, abs(ev).max()):
                    ok[i] = False
    if ok.any():
        print(f'{name}: feasible P in [{Ps[ok].min()}, {Ps[ok].max()}]  ({ok.sum()} values)', flush=True)
    else:
        print(f'{name}: NO feasible P  <-- contradiction', flush=True)


if __name__ == '__main__':
    lines4 = [(0, 1, 0, 1)]
    report('lines, E_-4 (check: P <= 1155)', lines4, 44)
    report('points+lines, E_-4 (check: P <= 1151)', [(1, 0, 0, 1), (0, 1, 0, 1)], 44)
    angles = np.linspace(0, np.pi, 25, endpoint=False)
    fl4 = [(np.cos(a), np.sin(a), 0, 1) for a in angles]
    report('flags, 25 directions, E_-4', fl4, 44)
    fl3 = [(np.cos(a), np.sin(a), 1, 0) for a in angles]
    report('flags, 25 directions, E_3', fl3, 54)
    mix = [(np.cos(a), np.sin(a), np.cos(b), np.sin(b)) for a in angles[::3] for b in np.linspace(0.05, 1.52, 6)]
    report('flags x eigenspace mixes (dim 98)', mix, 98)
