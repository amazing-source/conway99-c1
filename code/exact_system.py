"""Exact rational solution of the local counting equations (subgraph_lp.py) for srg(n,k,lam,mu) up to order M.
Returns the affine parametrisation z = z0 + sum_t t_j v_j (free variables = pivots-free columns)."""
import sys
from fractions import Fraction
from subgraph_lp import Types, build_equations


def solve_exact(n, k, lam, mu, M):
    T = Types(lam, mu, k, M)
    rows, aut = build_equations(T, n, M)
    var = [(m, i) for m in range(1, M + 1) for i in range(len(T.reps[m]))]
    # order variables so that high-order ones are eliminated last (free vars = high order)
    col = {v: j for j, v in enumerate(var)}
    N = len(var)
    R = []
    for row in rows:
        r = [Fraction(0)] * (N + 1)
        for v, c in row.items():
            r[col[v]] += c
        R.append(r)
    r = [Fraction(0)] * (N + 1); r[col[(1, 0)]] = Fraction(1); r[N] = Fraction(n); R.append(r)
    # Gauss-Jordan
    piv = []
    rr = 0
    for c in range(N):
        p = next((i for i in range(rr, len(R)) if R[i][c] != 0), None)
        if p is None:
            continue
        R[rr], R[p] = R[p], R[rr]
        inv = 1 / R[rr][c]
        R[rr] = [x * inv for x in R[rr]]
        for i in range(len(R)):
            if i != rr and R[i][c] != 0:
                f = R[i][c]
                R[i] = [a - f * b for a, b in zip(R[i], R[rr])]
        piv.append(c)
        rr += 1
    incons = [i for i in range(rr, len(R)) if R[i][N] != 0]
    free = [c for c in range(N) if c not in piv]
    return T, var, R[:rr], piv, free, incons


if __name__ == '__main__':
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    n, k, lam, mu = (int(a) for a in sys.argv[2:6]) if len(sys.argv) > 5 else (99, 14, 1, 2)
    T, var, R, piv, free, incons = solve_exact(n, k, lam, mu, M)
    print(f'srg({n},{k},{lam},{mu}) order {M}: {len(var)} variables, rank {len(piv)}, '
          f'free variables {[var[c] for c in free]}, inconsistent rows: {len(incons)}')
    # print the parametrisation of low orders
    N = len(var)
    for r, c in zip(R, piv):
        m, i = var[c]
        if m <= 3:
            terms = ' '.join(f'{-r[f]:+}*{var[f]}' for f in free if r[f] != 0)
            print(f'  z{var[c]} = {r[N]} {terms}')
