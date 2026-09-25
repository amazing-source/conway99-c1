r"""X11 -- real strongly regular graphs with the SAME eigenvalues as Conway 99: r = 3, s = -4 (r - s = 7).

Feasible parameter sets with {r, s} = {3, -4}: (49,24,11,12) [conference: Paley(49), Latin-square graphs LS_4(7)],
(50,21,8,9) [regular two-graphs on 50 points], (99,14,1,2) [open], and complements.  The corpus never used them.
They carry exactly the 7-adic algebra of C1: N = A - 3I, (A - 3I)(A + 4I) = mu J, so N^2 = mu J (mod 7).

For each real graph: eigenlattices Lambda_3, Lambda_{-4} (integer kernels), determinants, Smith / Jordan data at 7,
rank_7(A - 3I), the glue rank alpha (7-part of disc Lambda_{-4}), 7-adic signs, parity (even/odd), oddity check.
Purpose: (i) soundness of the L22-type genus reasoning on graphs that exist; (ii) observe where real graphs sit
(maximal glue rank or not); (iii) look for a law.
"""
import sys, os, itertools
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'c1_recherche', 'code'))
import graphs, genus_tools as gt
from eigenlattice_check import int_kernel, rank_mod


def paley49():
    # F_49 = F_7[x]/(x^2 - 3), 3 is a non-square mod 7
    els = [(a, b) for a in range(7) for b in range(7)]
    ix = {e: i for i, e in enumerate(els)}
    def mul(u, v):
        return ((u[0] * v[0] + 3 * u[1] * v[1]) % 7, (u[0] * v[1] + u[1] * v[0]) % 7)
    sq = set()
    for u in els:
        if u != (0, 0):
            sq.add(mul(u, u))
    A = np.zeros((49, 49), dtype=np.int64)
    for u in els:
        for v in els:
            d = ((u[0] - v[0]) % 7, (u[1] - v[1]) % 7)
            if d in sq:
                A[ix[u], ix[v]] = 1
    assert graphs.srg_params(A) == (49, 24, 11, 12), graphs.srg_params(A)
    return A


def net_graph(slopes):
    """Net graph of AG(2,7) with the parallel classes of the given slopes (None = vertical)."""
    pts = [(x, y) for x in range(7) for y in range(7)]
    A = np.zeros((49, 49), dtype=np.int64)
    for i, (x1, y1) in enumerate(pts):
        for j, (x2, y2) in enumerate(pts):
            if i == j:
                continue
            for m in slopes:
                if (m is None and x1 == x2) or (m is not None and (y2 - y1) % 7 == (m * (x2 - x1)) % 7):
                    A[i, j] = 1
    return A


def lattice_data(A, theta):
    n = len(A)
    B = int_kernel((A - theta * np.eye(n, dtype=np.int64)).tolist())
    Bm = np.array(B, dtype=object)
    G = (Bm @ Bm.T).tolist()
    d = gt.det_frac(G)
    even = all(G[i][i] % 2 == 0 for i in range(len(G)))
    return len(B), G, int(d), even


def fmt_det(d):
    out = []
    for q in (2, 3, 5, 7, 11, 13):
        v = gt.vp(d, q)
        if v:
            out.append(f'{q}^{v}')
    return '*'.join(out) or '1'


def analyse(name, A):
    n = len(A); k = int(A[0].sum())
    print(f'== {name}: {graphs.srg_params(A)}')
    r7 = rank_mod((A - 3 * np.eye(n, dtype=np.int64)).tolist(), 7)
    print(f'   rank_7(A - 3I) = {r7}')
    for theta in (3, -4):
        rk, G, d, even = lattice_data(A, theta)
        js = gt.jordan_symbol(G, 7)
        other = {q: gt.jordan_symbol(G, q) for q in (3, 5) if gt.vp(d, q)}
        print(f'   Lambda_{theta}: rank {rk}, det {fmt_det(d)}, {"even" if even else "odd"}; '
              f'7-adic Jordan (j, dim, sign) {js}; other {other}')
        if even and gt.vp(d, 2) == 0:
            print(f'      oddity check (sum of excesses + signature = 0 mod 8): {gt.oddity_check(G)}')


def srg50_from_net(slopes, extra_slope, Dset):
    """Switch the regular two-graph {inf} + net(slopes) to a regular representative of degree 21.
    Hand derivation: x = +1 on P, -1 on M with (A + 4I) 1_M = 12*1 (M a (-4)-tight 21-set).  M = three parallel
    lines {y - m x in Dset} of a slope m outside the net meets every net line in 3 points, hence works."""
    A = net_graph(slopes)
    pts = [(x, y) for x in range(7) for y in range(7)]
    S = np.zeros((50, 50), dtype=np.int64)
    S[0, 1:] = S[1:, 0] = 1                                   # inf non-adjacent to all: Seidel +1
    S[1:, 1:] = np.ones((49, 49), dtype=np.int64) - np.eye(49, dtype=np.int64) - 2 * A
    d = np.array([1] + [(-1 if (y - extra_slope * x) % 7 in Dset else 1) for x, y in pts], dtype=np.int64)
    S2 = S * np.outer(d, d)
    A2 = (np.ones((50, 50), dtype=np.int64) - np.eye(50, dtype=np.int64) - S2) // 2
    return A2


if __name__ == '__main__':
    for sl, m, D in (([None, 0, 1, 2], 3, {0, 1, 3}), ([None, 0, 1, 2], 4, {0, 1, 2}), ([None, 0, 1, 3], 5, {0, 2, 3})):
        A = srg50_from_net(sl, m, D)
        prm = graphs.srg_params(A)
        print(f'switching of net {sl} by slope {m}, D = {sorted(D)}: {prm}')
        if prm == (50, 21, 8, 9):
            analyse(f'srg(50,21,8,9) from net {sl}, slope {m}, D {sorted(D)}', A)
        elif prm == (50, 28, 15, 16):
            analyse(f'srg(50,28,15,16) from net {sl}, slope {m}, D {sorted(D)}', A)
    analyse('Paley(49)', paley49())
    for sl in ([None, 0, 1, 2], [None, 0, 1, 3], [None, 0, 1, 5], [None, 0, 2, 4]):
        A = net_graph(sl)
        if graphs.srg_params(A) == (49, 24, 11, 12):
            analyse(f'net AG(2,7) slopes {sl}', A)
