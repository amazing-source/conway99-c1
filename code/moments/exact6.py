"""Exact order-t analysis with ONE free parameter left by the exact identities (order 6 for lambda=1, mu=2).
Rational elimination gives q = q0 + P q1 (P = prism count); then the admissible interval of P from q >= 0 and from
each PSD block M0 + P M1 (assembled exactly, then diagonally scaled and tested in float64 / bisection).
Usage: python3 exact6.py n k lam mu t"""
import sys, math, time
from fractions import Fraction
import numpy as np
from srg_moments import Hierarchy, canon, pid


def nullspace_affine(rows, ncol):
    """solve rows.x = 0, sum x = 1 exactly: returns x0 and basis of the null directions (lists of Fractions)"""
    Mx = [list(r) + [Fraction(0)] for r in rows] + [[Fraction(1)] * ncol + [Fraction(1)]]
    piv, r = [], 0
    for c in range(ncol):
        p = next((i for i in range(r, len(Mx)) if Mx[i][c] != 0), None)
        if p is None: continue
        Mx[r], Mx[p] = Mx[p], Mx[r]
        inv = 1 / Mx[r][c]; Mx[r] = [v * inv for v in Mx[r]]
        for i in range(len(Mx)):
            if i != r and Mx[i][c] != 0:
                f = Mx[i][c]; Mx[i] = [a - f * b for a, b in zip(Mx[i], Mx[r])]
        piv.append(c); r += 1
    assert all(Mx[i][ncol] == 0 for i in range(r, len(Mx))), "inconsistent system"
    free = [c for c in range(ncol) if c not in piv]
    x0 = [Fraction(0)] * ncol
    for i, c in enumerate(piv): x0[c] = Mx[i][ncol]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncol; v[f] = Fraction(1)
        for i, c in enumerate(piv): v[c] = -Mx[i][f]
        basis.append(v)
    return x0, basis


def frac_dot(B_ij, v):
    return sum((b * x for b, x in zip(B_ij, v) if b and x), Fraction(0))


if __name__ == "__main__":
    n, k, lam, mu, t = map(int, sys.argv[1:6]); t0 = time.time()
    H = Hierarchy(n, k, lam, mu, t, exact=True)
    Aeq = H.equalities(); nq = len(H.top)
    x0, basis = nullspace_affine(Aeq.tolist(), nq)
    print(f"srg({n},{k},{lam},{mu}) order {t}: {nq} classes, free parameters {len(basis)}  ({time.time() - t0:.0f}s)", flush=True)
    assert len(basis) == 1
    bits = 0
    for (i, j) in [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4), (2, 5)]:
        bits |= 1 << pid(i, j)
    dens = list(H.dens[(6, canon(6, bits)[0])]); C6 = math.comb(n, 6)
    a0 = frac_dot(dens, x0) * C6; a1 = frac_dot(dens, basis[0]) * C6        # P = a0 + s*a1
    q0 = [x - b * a0 / a1 for x, b in zip(x0, basis[0])]                   # value at P = 0
    q1 = [b / a1 for b in basis[0]]                                         # d q / d P
    lo, hi = Fraction(-10 ** 12), Fraction(10 ** 12)
    for a, b in zip(q1, q0):
        if a > 0: lo = max(lo, -b / a)
        elif a < 0: hi = min(hi, -b / a)
        elif b < 0: lo, hi = Fraction(1), Fraction(0)
    print(f"  q >= 0:        P in [{float(lo):.6f}, {float(hi):.6f}]", flush=True)
    killer = None
    for name, s, a, F, coef in H.blocks():
        B = H.block_matrices(s, a, F, coef); d = B.shape[0]
        X0 = [[frac_dot(B[i, j], q0) for j in range(d)] for i in range(d)]
        X1 = [[frac_dot(B[i, j], q1) for j in range(d)] for i in range(d)]
        def ok(P):
            M = [[X0[i][j] + P * X1[i][j] for j in range(d)] for i in range(d)]
            keep = [i for i in range(d) if M[i][i] != 0]
            if any(M[i][i] < 0 for i in keep):
                return False
            for i in range(d):            # zero diagonal => zero row, exactly
                if M[i][i] == 0 and any(M[i][j] != 0 for j in range(d)):
                    return False
            if not keep:
                return True
            dg = np.array([math.sqrt(float(M[i][i])) for i in keep])
            N = np.array([[float(M[i][j]) for j in keep] for i in keep]) / dg[:, None] / dg[None, :]
            return np.linalg.eigvalsh(N).min() >= -1e-9
        if lo > hi: break
        grid = [lo + (hi - lo) * Fraction(i, 32) for i in range(33)]
        feas = [g for g in grid if ok(g)]
        if not feas:
            killer = name; lo, hi = Fraction(1), Fraction(0); break
        if not ok(lo):
            x, y = lo, feas[0]
            for _ in range(60):
                m_ = (x + y) / 2; x, y = (x, m_) if ok(m_) else (m_, y)
            lo = y
        if not ok(hi):
            x, y = feas[-1], hi
            for _ in range(60):
                m_ = (x + y) / 2; x, y = (m_, y) if ok(m_) else (x, m_)
            hi = x
    if killer:
        print(f"  EMPTY: killed by block {killer}", flush=True)
    else:
        print(f"  all PSD blocks: P in [{float(lo):.6f}, {float(hi):.6f}]  ({time.time() - t0:.0f}s)", flush=True)
