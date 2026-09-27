r"""Finish line (C), C1 27/09: y-energy criterion from ROOT DATA (proven, notes/140 s.2 + per-root trap).
Packing in the smaller neighbour nb_min: sum_u m(u) + m_min(y1) + m_min(y2) <= #new_min = 24 h_min - r, with m(u) >= 0 and
m_min(y) = 4 h_min + r/8 - E(y)  (lattice identity for norm-7 vectors whose new-root products are <= 3/2, which the frame forces).
Hence E(y1) + E(y2) >= 1.25 r - 16 h_min.
Each y has |(alpha,y)| <= 2 on every root (trap per root), so its projection on each root component R_i is a weight of level <= 2
(W-conjugate of a dominant weight lam with (lam, theta_i) <= 2), and E(y) = sum_i h_i |P_i y|^2 with sum |P_i y|^2 <= 7.
E_y_max = knapsack over components.  If 2 E_y_max < 1.25 r - 16 h_min: EXCLUDED."""
import itertools, json, re, sys, os
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from packing_criterion import COX, comps, cox


def cartan(t, n):
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        A[i, i] = 2
    if t == 'a':
        for i in range(n - 1):
            A[i, i + 1] = A[i + 1, i] = -1
    elif t == 'd':
        for i in range(n - 2):
            A[i, i + 1] = A[i + 1, i] = -1
        A[n - 3, n - 1] = A[n - 1, n - 3] = -1
    elif t == 'e':
        # Bourbaki: 1-3-4-5-6(-7-8), 2 attached to 4
        edges = [(0, 2), (2, 3), (3, 4), (1, 3)] + [(k, k + 1) for k in range(4, n - 1)]
        for a, b in edges:
            A[a, b] = A[b, a] = -1
    return A


def highest_root_marks(t, n):
    """coefficients of the highest root in simple roots."""
    if t == 'a':
        return [1] * n
    if t == 'd':
        return [1] + [2] * (n - 3) + [1, 1]
    return {6: [1, 2, 2, 3, 2, 1], 7: [2, 2, 3, 4, 3, 2, 1], 8: [2, 3, 4, 6, 5, 4, 3, 2]}[n]


def level2_norms(t, n):
    """norms of the dominant weights lam = sum c_j w_j with sum_j m_j c_j <= 2 (m = marks of theta), lam != 0."""
    A = cartan(t, n)
    Ainv = [[F(x).limit_denominator(1000) for x in row] for row in np.linalg.inv(A)]
    m = highest_root_marks(t, n)
    out = set()
    idx1 = [j for j in range(n) if m[j] <= 2]
    for j in idx1:
        for c in (1, 2):
            if m[j] * c <= 2:
                v = [0] * n; v[j] = c
                out.add(sum(v[a] * v[b] * Ainv[a][b] for a in range(n) for b in range(n)))
    for j, k in itertools.combinations(range(n), 2):
        if m[j] + m[k] <= 2:
            v = [0] * n; v[j] = 1; v[k] = 1
            out.add(sum(v[a] * v[b] * Ainv[a][b] for a in range(n) for b in range(n)))
    return sorted(out)


def E_y_max(cs, full_rank):
    best = {F(0): F(0)}
    for (t, n) in cs:
        h = cox(t, n)
        new = dict(best)
        for tot, e in best.items():
            for nm in level2_norms(t, n):
                s = tot + nm
                if s <= 7 and new.get(s, -1) < e + h * nm:
                    new[s] = e + h * nm
        best = new
    if full_rank:
        return best.get(F(7))
    return max(best.values())


if __name__ == '__main__':
    d = json.load(open('data/borcherds_odd24.json'))
    rows = []
    for L in d:
        if L['id'] == 0:
            continue
        cs = comps(L['roots'])
        r = L['nroots']
        h1, h2 = COX[L['nb1']], COX[L['nb2']]
        hmin = min(h1, h2)
        need = F(5, 4) * r - 16 * hmin
        Em = E_y_max(cs, L['rank'] == 24)
        excl = Em is None or 2 * Em < need
        rows.append((L['id'], L['roots'], r, hmin, float(need), float(Em) if Em is not None else None, excl))
    ex = [x for x in rows if x[-1]]
    print('excluded by y-energy:', [x[0] for x in ex])
    for x in rows:
        if x[4] > 0:
            print(x)
