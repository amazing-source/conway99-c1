"""Projected Gegenbauer positivity with a small reference subgraph H (LAB 19/10/2026), after Liao-Wang-Yu-Cai
(arXiv:2610.20259) and Bondarenko-Prymak-Radchenko (LAA 2017).  Pure parameter test for srg(99,14,1,2).

Facts used (all from lambda = 1, mu = 2):
  * spherical representation: in E_-4 (dim 44) the unit vertex vectors have inner products -2/7 (adjacent), 1/28 (not);
    in E_3 (dim 54) they are 3/14 and -1/21  (Gram = 63 P_-4 / 28 and 77 P_3 / 42);
  * for a reference copy of H (m vertices, independent vectors), every other vertex u is projected onto span(H)^perp
    (dimension d = n - m) and normalised; the normalised inner product depends only on the adjacency patterns of u and v
    to H and on A_uv;
  * Schoenberg: for each k the Gegenbauer kernel G_k^(d) is positive definite on S^(d-1), so the matrix
    M_k[i, j] = sum_{u in class i, v in class j} G_k^(d)(t_uv) (diagonal u = v included) is PSD for every copy of H;
  * the class sizes and the numbers of adjacent / non-adjacent ordered pairs between classes are FIXED for every copy
    of H in {vertex, edge, non-edge, triangle} (derived in NOTE_ENONCE_RENFORCE_2026-10-19.md, section 2).
A negative eigenvalue of some M_k would exclude srg(99,14,1,2) outright.
usage: python gegen_ref_test.py [K=80]"""
import sys
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 60
K = int(sys.argv[1]) if len(sys.argv) > 1 else 80
REPS = {'E-4': (44, Fr(-2, 7), Fr(1, 28)), 'E3': (54, Fr(3, 14), Fr(-1, 21))}


def gegen(d, t, K):
    """G_0..G_K for S^(d-1), normalised G_k(1) = 1."""
    g = [mp.mpf(1), t]
    for k in range(1, K):
        g.append(((2 * k + d - 2) * t * g[k] - k * g[k - 1]) / (k + d - 2))
    return g


def solve(Gm, b):
    """exact solve Gm x = b (Fractions, Gauss)."""
    n = len(Gm)
    M = [list(Gm[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [M[r][i] - f * M[c][i] for i in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]


def run(name, H_adj, classes, pairs, rep):
    n, a, b = REPS[rep]
    m = len(H_adj)
    ip = lambda adj: a if adj else b
    Gm = [[Fr(1) if i == j else ip(H_adj[i][j]) for j in range(m)] for i in range(m)]
    g = {c: [ip(x) for x in pat] for c, (size, pat) in classes.items()}
    Ginv_g = {c: solve(Gm, g[c]) for c in classes}
    proj = lambda c1, c2, base: base - sum(g[c1][i] * Ginv_g[c2][i] for i in range(m))
    norm = {c: proj(c, c, Fr(1)) for c in classes}
    d = n - m
    names = list(classes)
    worst = (mp.inf, None)
    zero_k = []
    for k in range(1, K + 1):
        M = mp.matrix(len(names), len(names))
        for i, c1 in enumerate(names):
            for j, c2 in enumerate(names):
                s = mp.mpf(classes[c1][0]) if i == j else mp.mpf(0)
                adj, non = pairs.get((c1, c2), pairs.get((c2, c1), (0, 0)))
                for cnt, base in ((adj, a), (non, b)):
                    if cnt:
                        t = mp.mpf(proj(c1, c2, base).numerator) / proj(c1, c2, base).denominator
                        t = t / mp.sqrt(mp.mpf(norm[c1].numerator) / norm[c1].denominator *
                                        mp.mpf(norm[c2].numerator) / norm[c2].denominator)
                        s += cnt * gegen(d, t, k)[k]
                M[i, j] = s
        ev = min(mp.eigsy(M)[0])
        scale = max(abs(M[i, j]) for i in range(len(names)) for j in range(len(names)))
        if scale < mp.mpf(10) ** (-40):          # M_k = 0 identically (k = 1: sum of a vertex's neighbours = theta x)
            zero_k.append(k)
            continue
        if ev / scale < worst[0]:
            worst = (ev / scale, k)
        if ev < -mp.mpf(10) ** (-30) * scale:
            print('  NEGATIVE', name, rep, 'k =', k, 'min eig', mp.nstr(ev, 12))
    print('%-9s %-4s d=%d  M_k = 0 for k in %s; worst relative min eigenvalue %s at k=%s' % (
        name, rep, d, zero_k, mp.nstr(worst[0], 8), worst[1]))


# ---- reference graphs with per-copy fixed counts (ordered pairs u != v; (c1,c2) and (c2,c1) symmetric) ----
CASES = {
    'vertex': ([[0]], {'N': (14, [1]), 'F': (84, [0])},
               {('N', 'N'): (14, 168), ('N', 'F'): (168, 1008), ('F', 'F'): (1008, 5964)}),
    'edge': ([[0, 1], [1, 0]], {'Z': (1, [1, 1]), 'X': (12, [1, 0]), 'Y': (12, [0, 1]), 'O': (72, [0, 0])},
             {('Z', 'Z'): (0, 0), ('Z', 'X'): (0, 12), ('Z', 'Y'): (0, 12), ('Z', 'O'): (12, 60), ('X', 'X'): (12, 120),
              ('Y', 'Y'): (12, 120), ('X', 'Y'): (12, 132), ('X', 'O'): (132, 732), ('Y', 'O'): (132, 732),
              ('O', 'O'): (732, 4380)}),
    'nonedge': ([[0, 0], [0, 0]], {'C': (2, [1, 1]), 'U': (12, [1, 0]), 'V': (12, [0, 1]), 'O': (71, [0, 0])},
                {('C', 'C'): (0, 2), ('C', 'U'): (2, 22), ('C', 'V'): (2, 22), ('C', 'O'): (20, 122),
                 ('U', 'U'): (10, 122), ('V', 'V'): (10, 122), ('U', 'V'): (22, 122), ('U', 'O'): (122, 730),
                 ('V', 'O'): (122, 730), ('O', 'O'): (730, 4240)}),
    'triangle': ([[0, 1, 1], [1, 0, 1], [1, 1, 0]],
                 {'P': (12, [1, 0, 0]), 'Q': (12, [0, 1, 0]), 'S': (12, [0, 0, 1]), 'R': (60, [0, 0, 0])},
                 {('P', 'P'): (12, 120), ('Q', 'Q'): (12, 120), ('S', 'S'): (12, 120), ('P', 'Q'): (12, 132),
                  ('P', 'S'): (12, 132), ('Q', 'S'): (12, 132), ('P', 'R'): (120, 600), ('Q', 'R'): (120, 600),
                  ('S', 'R'): (120, 600), ('R', 'R'): (480, 3060)}),
}


def sanity(H_adj, classes, pairs):
    """degree and size checks: every vertex outside H has 14 neighbours, sizes add up to 99 - m."""
    m = len(H_adj)
    assert sum(s for s, _ in classes.values()) == 99 - m
    for c, (size, pat) in classes.items():
        deg = size * sum(pat)
        for c2 in classes:
            adj, non = pairs[(c, c2)] if (c, c2) in pairs else pairs[(c2, c)]
            deg += adj
            assert adj + non == size * (classes[c2][0] - (1 if c == c2 else 0)), (c, c2)
        assert deg == 14 * size, (c, deg, 14 * size)


for nm, (H, cl, pr) in CASES.items():
    sanity(H, cl, pr)
    for rep in REPS:
        run(nm, H, cl, pr, rep)
