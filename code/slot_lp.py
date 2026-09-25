"""notes/109: LP relaxation of the slot calculus (stronger than interval propagation).
Infeasibility is certified by an exact rational Farkas vector: y (equalities), z >= 0 (upper bounds) with
A^T y - z <= 0 componentwise and b.y - ub.z > 0.  Feasibility (float) proves nothing."""
import numpy as np
from fractions import Fraction
from scipy.optimize import linprog
from slot_calculus import build, propagate

def lp_check(cfg):
    var, lo, hi, eqs, inc = build(cfg)
    ok, lo, hi, log = propagate(lo, hi, eqs)
    if not ok:
        return 'refuted by propagation', None
    n = len(lo)
    A = np.zeros((len(eqs), n)); b = np.zeros(len(eqs))
    for i, (coef, rhs, lab) in enumerate(eqs):
        for j, a in coef.items():
            A[i, j] = a
        b[i] = rhs
    res = linprog(np.zeros(n), A_eq=A, b_eq=b, bounds=list(zip(lo, hi)), method='highs')
    if res.status == 0:
        return 'LP feasible', res.x
    # Farkas: maximize b.y - ub.z - lb.w  s.t. A^T y - z + w <= 0, z, w >= 0, b.y - ub.z + lb.w <= 1
    m = len(eqs)
    lb = np.array(lo, float); ub = np.array(hi, float)
    # variables [y (m, free), z (n, >=0), w (n, >=0)] ; constraint A^T y - z + w <= 0
    c = -np.concatenate([b, -ub, lb])
    A_ub = np.hstack([A.T, -np.eye(n), np.eye(n)])
    b_ub = np.zeros(n)
    A_ub = np.vstack([A_ub, np.concatenate([b, -ub, lb])[None, :]])
    b_ub = np.concatenate([b_ub, [1.0]])
    bounds = [(None, None)] * m + [(0, None)] * (2 * n)
    r2 = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    if r2.status != 0 or -r2.fun < 0.5:
        return 'LP status unclear', None
    yv = [Fraction(v).limit_denominator(1000) for v in r2.x[:m]]
    zv = [Fraction(v).limit_denominator(1000) for v in r2.x[m:m + n]]
    wv = [Fraction(v).limit_denominator(1000) for v in r2.x[m + n:]]
    # exact verification
    for j in range(n):
        s = sum(yv[i] * int(A[i, j]) for i in range(m) if A[i, j] != 0) - zv[j] + wv[j]
        if s > 0:
            return 'certificate failed exact check', None
    if any(v < 0 for v in zv + wv):
        return 'certificate failed sign check', None
    val = sum(yv[i] * int(b[i]) for i in range(m)) - sum(zv[j] * hi[j] for j in range(n)) + sum(wv[j] * lo[j] for j in range(n))
    if val <= 0:
        return 'certificate failed value check', None
    return 'LP infeasible (exact Farkas certificate)', (yv, zv, wv, eqs)

if __name__ == '__main__':
    from slot_tests import configs
    for name, twist in [('L14 |C|=2', {(0, 0): {2, 3}, (1, 0): {2, 3}}),
                        ('L14 |C|=3', {(0, 0): {2, 3, 4}, (1, 0): {2, 3, 4}})]:
        from collections import Counter
        cnt = Counter()
        for cfg in configs(twist):
            st, _ = lp_check(cfg)
            cnt[st] += 1
        print(name, dict(cnt), flush=True)
