r"""X19b -- exact Farkas certificates for the infeasible block-level systems of X19.
{x in [0,1]^n : A x = b} is empty iff there is y with  b^T y > sum_j max(0, (A^T y)_j).
y is taken from the duals of the phase-1 LP  min sum(s+ + s-)  s.t.  A x + s+ - s- = b,  0 <= x <= 1,
rationalised, and the inequality is checked in exact arithmetic (A, b integral)."""
import sys, random, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import hstack, identity
sys.path.insert(0, 'scripts')
from x19_block_lp_generic import build_lp
from x14_triangle_supports import LAB, random_tau, random_sigma, build, admissible

def certify(tau, sigma):
    built, msg = build_lp(tau, sigma, True)
    A, b, nv, T = built
    m = A.shape[0]
    I = identity(m, format='csr')
    Abig = hstack([A, I, -I]).tocsr()
    c = np.concatenate([np.zeros(nv), np.ones(2 * m)])
    bounds = [(0, 1)] * nv + [(0, None)] * (2 * m)
    res = linprog(c, A_eq=Abig, b_eq=b, bounds=bounds, method='highs')
    delta = res.fun
    y = res.eqlin.marginals
    best = None
    Acoo = A.tocoo()
    for sgn in (1, -1):
        for den in (10 ** 6, 10 ** 8, 10 ** 10):
            yq = [Fr(sgn * y[i]).limit_denominator(den) for i in range(m)]
            col = [Fr(0)] * nv
            for i, j, v in zip(Acoo.row, Acoo.col, Acoo.data):
                if yq[i]:
                    col[j] += yq[i] * int(round(v))
            val = sum(yq[i] * int(round(b[i])) for i in range(m) if yq[i]) - sum(x for x in col if x > 0)
            if val > 0:
                return delta, val, den
            if best is None or val > best:
                best = val
    return delta, best, None

if __name__ == '__main__':
    seed, n = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    done = 0
    while done < n:
        tau = {u: random_tau(u, rng) for u in LAB}
        sigma = {c: random_sigma(c, rng) for c in range(7)}
        ok = all(admissible(build([frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2)
                                   for s in (0, 1) for t in (0, 1)], tau, sigma))
                 for tri in itertools.combinations(range(7), 3))
        if not ok:
            continue
        done += 1
        delta, val, den = certify(tau, sigma)
        print(f'config {done}: phase-1 optimum {delta:.4f}; exact Farkas value {float(val):.6f} '
              f'({"CERTIFIED INFEASIBLE" if den else "no certificate (feasible or not rationalised)"}, denominators <= {den})', flush=True)
