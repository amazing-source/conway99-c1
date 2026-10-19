"""Schoenberg positivity for the vertices and the 231 lines of srg(99,14,1,2) together (LAB 19/10/2026).
Vectors (exact, from lambda = 1, mu = 2):
  E_-4 (dim 44, scaled Gram 27I - 9A + J): vertex norm 28; line chi_l norm 36;
     vertex-vertex: adjacent -8, else 1;  vertex-line: on l 12, adjacent to one point -6, far 3;
     line-line: meeting 0, disjoint with m edges between them 9(1 - m).
  E_3 (dim 54, scaled Gram 44I + 11A - 2J): vertex norm 42; line norm 180;
     vertex-vertex: adjacent 9, else -2;  vertex-line: on 60, adjacent 5, far -6;
     line-line: meeting 70, disjoint with m edges 11m - 18.
Pair counts: vertices 693 adjacent / 4158 not; vertex-line 693 on / 8316 adjacent / 13860 far; line pairs 2079 meeting,
N0 = 3696 - P, N1 = 16632 + 3P, N2 = 4158 - 3P, N3 = P (P = induced prisms; redrived from the per-line counts
e0 = 32 - c3, e1 = 144 + 3 c3, e2 = 36 - 3 c3, e3 = c3, sum_l c3(l) = 2P).
Kernels: Gegenbauer G_k^(44)(t), G_l^(54)(s) and products G_k^(44)(t) G_l^(54)(s) (positive definite on S^43 x S^53).
For each kernel the 2 x 2 matrix (vertex, line) of kernel sums is PSD; also the 1 x 1 line-only sum.
Prints the interval of P in [0, 1386] allowed by all kernels with k, l <= K.
usage: python gegen_lines.py [K=30]"""
import sys

import mpmath as mp

mp.mp.dps = 40
K = int(sys.argv[1]) if len(sys.argv) > 1 else 30


def gegen(d, t, K):
    g = [mp.mpf(1), t]
    for k in range(1, K):
        g.append(((2 * k + d - 2) * t * g[k] - k * g[k - 1]) / (k + d - 2))
    return g


def nz(x, n1, n2):
    return mp.mpf(x) / mp.sqrt(mp.mpf(n1) * n2)


# (inner product in E-4 scaled, inner product in E3 scaled) per relation, with norms
VV = {'self': (28, 42, 99), 'adj': (-8, 9, 2 * 693), 'non': (1, -2, 2 * 4158)}               # ordered pairs
VL = {'on': (12, 60, 693), 'adj': (-6, 5, 8316), 'far': (3, -6, 13860)}
LL_fixed = {'self': (36, 180, 231), 'meet': (0, 70, 2 * 2079)}
LL_P = {0: (9, -18, 2 * 3696, -2), 1: (0, -7, 2 * 16632, 6), 2: (-9, 4, 2 * 4158, -6), 3: (-18, 15, 0, 2)}
NV = (28, 42); NL = (36, 180)


def kernel_vals(kind, k, l):
    """returns function (a, b, na, nb) -> kernel value; a, b scaled inner products in E-4 and E3."""
    def f(a, b, na, nb):
        t = nz(a, na[0], nb[0]); s = nz(b, na[1], nb[1])
        if kind == 'E-4':
            return gegen(44, t, k)[k]
        if kind == 'E3':
            return gegen(54, s, l)[l]
        return gegen(44, t, k)[k] * gegen(54, s, l)[l]
    return f


def sums(kind, k, l):
    f = kernel_vals(kind, k, l)
    vv = sum(c * f(a, b, NV, NV) for a, b, c in VV.values())
    vl = sum(c * f(a, b, NV, NL) for a, b, c in VL.values())
    ll0 = sum(c * f(a, b, NL, NL) for a, b, c in LL_fixed.values())
    ll1 = mp.mpf(0)
    for m, (a, b, c0, c1) in LL_P.items():
        v = f(a, b, NL, NL)
        ll0 += c0 * v; ll1 += c1 * v
    return vv, vl, ll0, ll1


def allowed(vv, vl, ll0, ll1, P):
    ll = ll0 + ll1 * P
    tol = mp.mpf(10) ** (-25) * (abs(vv) + abs(ll) + abs(vl) + 1)
    return ll >= -tol and vv * ll - vl * vl >= -tol * (abs(vv) + abs(ll) + 1)


lo, hi = mp.mpf(0), mp.mpf(1386)
binding = []
kernels = [('E-4', k, 0) for k in range(1, K + 1)] + [('E3', 0, l) for l in range(1, K + 1)] + \
          [('prod', k, l) for k in range(1, K + 1) for l in range(1, K + 1)]
for kind, k, l in kernels:
    vv, vl, ll0, ll1 = sums(kind, k, l)
    # vv >= 0 is a pure parameter condition
    if vv < -mp.mpf(10) ** (-20) * (1 + abs(vv)):
        print('VERTEX-ONLY NEGATIVE', kind, k, l, vv)
    # allowed set in P is an interval (ll affine, det concave? ll*vv - vl^2 is affine in P since vv, vl fixed)
    # conditions: ll0 + ll1 P >= 0 and vv (ll0 + ll1 P) - vl^2 >= 0  -> both affine in P
    big = abs(vv) * (abs(ll0) + 1386 * abs(ll1)) + vl * vl + abs(ll0) + 1386 * abs(ll1) + 1
    eps = mp.mpf(10) ** (-25) * big
    conds = [(ll0, ll1)]
    if vv > eps:
        conds.append((vv * ll0 - vl * vl, vv * ll1))
    for c0, c1 in conds:
        c0 = c0 if abs(c0) > eps else mp.mpf(0)
        c1 = c1 if abs(c1) * 1386 > eps else mp.mpf(0)
        if c1 > 0:
            b = -c0 / c1
            if b > lo:
                lo = b; binding.append((kind, k, l, 'lo', mp.nstr(b, 10)))
        elif c1 < 0:
            b = -c0 / c1
            if b < hi:
                hi = b; binding.append((kind, k, l, 'hi', mp.nstr(b, 10)))
        elif c0 < 0:
            print('P-independent violation', kind, k, l, mp.nstr(c0, 8))
print('allowed P interval: [%s, %s]' % (mp.nstr(lo, 12), mp.nstr(hi, 12)))
for b in binding[-8:]:
    print('  binding', b)
