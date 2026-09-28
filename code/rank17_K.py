r"""Rank-17 switch: for every (V, y-pair) of data/rank17/ypairs_*.json, the rank-15 lattice K = V cap {y1, y2}-perp.
Exact: V basis = (integral basis of the core, ambient coordinates) + (unit vectors of Z^m); y1, y2 in coefficients;
K = integer kernel of x -> (x G y1, x G y2) by HNF of [M | I]; LLL-reduced; det K must be 49 (handoff Prop. 4.1).
Output per V: data/rank17/K_<tag>.json with, per pair: K basis (ambient coordinates, fraction strings), Gram, and the
numbers of vectors of norm 1, 2, 3 in K.
Usage: python rank17_K.py <tag|all>"""
import json, math, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rank17_cores import cores, int_basis
from rank17_ypairs import UNITS
from envelope_trap import hnf_rows, lll
from h_stage2 import short_vectors_fast

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'rank17')


def v_basis(name):
    if name == 'Z17':                                                  # V = Z^17, standard basis (structures' Z17 pairs)
        return [[F(int(i == j)) for j in range(17)] for i in range(17)], 0, 17
    gens, dim = cores()[name]
    Bc = int_basis(gens)
    m = UNITS[name]
    B = [list(r) + [F(0)] * m for r in Bc]
    for j in range(m):
        e = [F(0)] * (dim + m); e[dim + j] = F(1); B.append(e)
    return B, dim, m


def solve_coeffs(B, y):
    """coefficients x with x B = y (exact; B square invertible)"""
    n = len(B)
    M = [[B[i][k] for i in range(n)] + [y[k]] for k in range(len(y))]      # columns of B as equations
    # least squares is not needed: B has full row rank n and len(y) = n (ambient dim = rank for Z^m part + core dim)
    # use the n x n system on the ambient coordinates: pick n independent columns
    rows = []
    for k in range(len(y)):
        rows.append([B[i][k] for i in range(n)] + [y[k]])
    # Gaussian elimination over Q on the (ambient x n) system
    A = [r[:] for r in rows]
    piv_cols, r = [], 0
    for c in range(n):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [v * inv for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv_cols.append(c); r += 1
    assert r == n
    for i in range(r, len(A)):
        assert A[i][n] == 0, 'y not in the span of V'
    x = [F(0)] * n
    for i, c in enumerate(piv_cols):
        x[c] = A[i][n]
    assert all(v.denominator == 1 for v in x), 'y not in V'
    return [int(v) for v in x]


def main(tag):
    t0 = time.time()
    src = json.load(open(os.path.join(DATA, 'ypairs_%s.json' % tag)))
    name = src['core']
    B, dim, m = v_basis(name)
    G = [[sum(a * b for a, b in zip(u, v)) for v in B] for u in B]
    assert all(x.denominator == 1 for row in G for x in row)
    Gi = [[int(x) for x in row] for row in G]
    n = len(B)
    out = []
    for p in src['pairs']:
        y1 = [F(x) for x in p['y1_core']] + [F(x) for x in p['y1_units']]
        y2 = [F(x) for x in p['y2_core']] + [F(x) for x in p['y2_units']]
        c1, c2 = solve_coeffs(B, y1), solve_coeffs(B, y2)
        Gy = [[sum(Gi[i][k] * c[k] for k in range(n)) for c in (c1, c2)] for i in range(n)]   # n x 2
        rows = [Gy[i] + [int(i == t) for t in range(n)] for i in range(n)]
        H = hnf_rows(rows)
        Kc = [row[2:] for row in H if row[0] == 0 and row[1] == 0]
        # rows of H with zero in the first two columns span the kernel (row HNF: pivots of the 2 columns come first)
        Kc = [row[2:] for row in H[2:]] if len(Kc) != n - 2 else Kc
        assert len(Kc) == n - 2, (len(Kc), n)
        Kamb = [[sum(F(r[i]) * B[i][k] for i in range(n)) for k in range(dim + m)] for r in Kc]
        Kred = lll(Kamb)
        GK = [[sum(a * b for a, b in zip(u, v)) for v in Kred] for u in Kred]
        GKi = [[int(x) for x in row] for row in GK]
        det = round(abs(np.linalg.det(np.array(GKi, dtype=float))))
        assert det == 49, ('det', det, p['id'])
        X, nrm = short_vectors_fast(GKi, 3)
        cnt = {k: 2 * int((nrm == k).sum()) for k in (1, 2, 3)}
        out.append({'id': p['id'], 'K_basis': [[str(x) for x in r] for r in Kred], 'K_gram': GKi, 'counts_norm_1_2_3': cnt,
                    'rootless_U_allowed': p['rootless_U_allowed']})
    res = {'V': src['V'], 'core': name, 'units': m, 'n': len(out), 'seconds': round(time.time() - t0, 1),
           'note': 'K = V cap {y1,y2}-perp, LLL-reduced, det 49 checked for every pair; ambient coordinates as rank17_ypairs',
           'K': out}
    json.dump(res, open(os.path.join(DATA, 'K_%s.json' % tag), 'w'))
    from collections import Counter
    print(json.dumps({'V': src['V'], 'n': len(out), 'seconds': res['seconds'],
                      'units_in_K': dict(Counter(o['counts_norm_1_2_3'][1] for o in out)),
                      'roots_in_K': dict(Counter(o['counts_norm_1_2_3'][2] for o in out))}), flush=True)


if __name__ == '__main__':
    tags = ['E8', 'D12p', 'E72p', 'A15p', 'E82', 'D16p', 'D82p', 'A11E6p'] if sys.argv[1] == 'all' else [sys.argv[1]]
    for t in tags:
        main(t)
