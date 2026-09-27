r"""Rank-17 switch (handoff RANK17_HANDOFF.md, verified by structures 27/09 night): V is one of the 9 unimodular lattices of
rank 17 = (unit-free core) + Z^m. This module builds the 8 cores explicitly (generators in R^n, exact fractions) and checks
them: integral, determinant 1, root count, no unit vectors.
  core      rank  m   glue
  E8          8   9   -
  D12+       12   5   D12 + (1/2)^12
  E7^2+      14   3   E7 + E7 + ([1],[1])      (E7 = A7 + [4] in the standard 8-dim A7 coordinates, sum = 0 hyperplane... see below)
  A15+       15   2   A15 + [4]
  E8^2       16   1   -
  D16+       16   1   D16 + (1/2)^16
  D8^2+      16   1   D8 + D8 + (s, v), (v, s)
  A11E6+     17   0   A11 + E6 + ([2],[1])
Coordinates: every core lives in an explicit R^N with the standard inner product (A_n in the sum-zero hyperplane of R^(n+1),
E6 / E7 inside E8 coordinates). The lattice is given by generator rows (Fractions); the Gram matrix of an LLL-free integral
basis is obtained by HNF over a common denominator."""
import itertools, json, math, os, sys
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from envelope_trap import hnf_rows, lll, gram


def e8_roots():
    R = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (1, -1):
            for sj in (1, -1):
                v = [F(0)] * 8; v[i] = F(si); v[j] = F(sj); R.append(v)
    for signs in itertools.product((1, -1), repeat=8):
        if signs.count(-1) % 2 == 0:
            R.append([F(s, 2) for s in signs])
    return R


def dn_gens(n):
    """D_n in Z^n: e_i - e_{i+1}, e_{n-1} + e_n"""
    G = []
    for i in range(n - 1):
        v = [F(0)] * n; v[i] = F(1); v[i + 1] = F(-1); G.append(v)
    v = [F(0)] * n; v[n - 2] = F(1); v[n - 1] = F(1); G.append(v)
    return G


def an_gens(n):
    """A_n in the sum-zero hyperplane of R^(n+1)"""
    G = []
    for i in range(n):
        v = [F(0)] * (n + 1); v[i] = F(1); v[i + 1] = F(-1); G.append(v)
    return G


def an_glue(n, i):
    """glue vector [i] of A_n: (i/(n+1))^(n+1-i), (-(n+1-i)/(n+1))^i   (norm i(n+1-i)/(n+1))"""
    return [F(i, n + 1)] * (n + 1 - i) + [F(-(n + 1 - i), n + 1)] * i


def e7_in_e8():
    """E7 = vectors of E8 orthogonal to a fixed root r = (1,-1,0^6)... we use r = e_7 + e_8 style: take r = (0^6, 1, 1)."""
    r = [F(0)] * 6 + [F(1), F(1)]
    R = [v for v in e8_roots() if sum(a * b for a, b in zip(v, r)) == 0]
    return R, r


def e6_in_e8():
    """E6 = vectors of E8 orthogonal to an A2: roots r1 = (0^6,1,1), r2 = (0^5,1,-1,0)... pick r2 with (r1, r2) = -1."""
    r1 = [F(0)] * 6 + [F(1), F(1)]
    r2 = [F(0)] * 5 + [F(1), F(-1), F(0)]
    assert sum(a * b for a, b in zip(r1, r2)) == -1
    R = [v for v in e8_roots() if sum(a * b for a, b in zip(v, r1)) == 0 and sum(a * b for a, b in zip(v, r2)) == 0]
    return R, (r1, r2)


def dual_glue_e7(R7, r):
    """a minimal vector of E7* not in E7: projection of an E8 root with (v, r) = 1 onto r-perp: v - r/2 (norm 2 - 1/2 = 3/2)"""
    for v in e8_roots():
        if sum(a * b for a, b in zip(v, r)) == 1:
            return [a - b / 2 for a, b in zip(v, r)]


def dual_glue_e6(r1, r2):
    """a minimal vector of E6* (class [1], norm 4/3): projection of an E8 root onto the A2-perp"""
    G = [[2, -1], [-1, 2]]
    for v in e8_roots():
        a, b = sum(x * y for x, y in zip(v, r1)), sum(x * y for x, y in zip(v, r2))
        if (a, b) != (0, 0):
            # coefficients of the projection onto span(r1, r2): solve G c = (a, b)
            det = F(3)
            c1 = (2 * a + b) / det
            c2 = (a + 2 * b) / det
            p = [x - c1 * y - c2 * z for x, y, z in zip(v, r1, r2)]
            if sum(x * x for x in p) == F(4, 3):
                return p


def block(*parts):
    """direct sum of generator lists given as (gens, dim) -> generators in the concatenated coordinates"""
    tot = sum(d for _, d in parts)
    out, off = [], 0
    for gens, d in parts:
        for g in gens:
            v = [F(0)] * tot
            v[off:off + d] = g
            out.append(v)
        off += d
    return out


def concat(*vecs):
    out = []
    for v in vecs:
        out += list(v)
    return out


def cores():
    C = {}
    E8 = e8_roots()
    C['E8'] = (E8, 8)
    s12 = [F(1, 2)] * 12
    C['D12+'] = (dn_gens(12) + [s12], 12)
    R7, r = e7_in_e8()
    g7 = dual_glue_e7(R7, r)
    C['E7^2+'] = (block((R7, 8), (R7, 8)) + [concat(g7, g7)], 16)          # lives in a 14-dim subspace of R^16
    C['A15+'] = (an_gens(15) + [an_glue(15, 4)], 16)                        # 15-dim subspace of R^16
    C['E8^2'] = (block((E8, 8), (E8, 8)), 16)
    C['D16+'] = (dn_gens(16) + [[F(1, 2)] * 16], 16)
    s8 = [F(1, 2)] * 8
    v8 = [F(1)] + [F(0)] * 7
    D8 = dn_gens(8)
    C['D8^2+'] = (block((D8, 8), (D8, 8)) + [concat(s8, v8), concat(v8, s8)], 16)
    R6, (r1, r2) = e6_in_e8()
    g6 = dual_glue_e6(r1, r2)
    C['A11E6+'] = (block((an_gens(11), 12), (R6, 8)) + [concat(an_glue(11, 2), g6)], 20)   # 17-dim subspace of R^20
    return C


def int_basis(gens):
    """an integral basis (rows, exact) of the lattice generated by gens, via HNF on a common denominator"""
    den = 1
    for g in gens:
        for x in g:
            den = den * x.denominator // math.gcd(den, x.denominator)
    rows = [[int(x * den) for x in g] for g in gens]
    H = hnf_rows(rows)
    return [[F(x, den) for x in row] for row in H]


def check():
    res = {}
    for name, (gens, dim) in cores().items():
        B = int_basis(gens)
        Gm = [[sum(a * b for a, b in zip(u, v)) for v in B] for u in B]
        assert all(x.denominator == 1 for row in Gm for x in row), name + ' not integral'
        Gi = np.array([[int(x) for x in row] for row in Gm], dtype=np.int64)
        det = round(abs(np.linalg.det(Gi.astype(float))))
        from h_stage2 import short_vectors_fast
        X, nrm = short_vectors_fast(Gi.tolist(), 2)
        roots = 2 * int((nrm == 2).sum())
        units = 2 * int((nrm == 1).sum())
        odd = any(int(Gi[i, i]) % 2 for i in range(len(Gi)))
        res[name] = {'rank': len(B), 'det': det, 'roots': roots, 'units': units, 'odd': odd}
        print(name, res[name], flush=True)
    return res


if __name__ == '__main__':
    check()
