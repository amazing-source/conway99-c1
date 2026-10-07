"""C1, lab session, 2026-10-07. Exact version of theta_lp.py: rational simplex, standard library only.

  python theta_lp_exact.py <N> <mode> [d ...]      (one process; series from theta_lp.py, which it imports)

Unknowns beta = (b_1..b_7). Every constraint is an affine form  const + coef . beta >= 0.
The primal  min g . beta  s.t. constraints  is solved through its dual
    max  - sum_i lambda_i const_i   s.t.  sum_i lambda_i coef_i = g,  lambda >= 0
by a two-phase tableau simplex in Fractions (Bland's rule). Returned objects are re-verified from scratch:
  infeasible : lambda >= 0, sum lambda_i coef_i = 0, sum lambda_i const_i < 0                       (Farkas)
  optimal    : lambda >= 0 with sum lambda_i coef_i = g (lower bound), and a beta satisfying every constraint with
               g . beta equal to that bound.
Modes (constraint sets), all containing: a_n >= 0 (7 <= n <= N), b_n >= 0 (1 <= n <= N), a_7k >= b_k:
  base : b_2 >= 462, b_3 >= 8316, b_4 >= 1386
  ext  : b_2 >= 462, b_3 >= 24948, b_4 >= 388080, b_5 >= 196812     (see NOTE.md for the configurations counted)
  ext2 : b_2 >= 462, b_3 >= 24948, b_4 >= 1431738, b_5 >= 3415104, b_6 >= 10844064   (NOTE.md section 9)
  suffix "+a7" adds a_7 <= 0;  suffix "+min:m" adds a_n <= 0 for 7 <= n < m (what-if: min L1 >= 2m);  suffix "+cap:b1=X,b2=Y,b3=Z" adds upper bounds b_k <= value (what-if runs, NOT facts)."""
import sys
from fractions import Fraction as Fr
import theta_lp as T
N = T.N


def simplex(cols, c, g):
    """max c.lam s.t. sum lam_i cols_i = g, lam >= 0.  ('optimal', value, lam, y) | ('unbounded', ray) | ('infeasible',)"""
    n = len(cols); k = len(g); sg = [-1 if x < 0 else 1 for x in g]
    tab = [[sg[r] * cols[i][r] for i in range(n)] + [Fr(int(r == q)) for q in range(k)] + [sg[r] * g[r]] for r in range(k)]
    basis = [n + r for r in range(k)]

    def pivot(r, j):
        q = tab[r][j]; tab[r] = [x / q for x in tab[r]]
        for i in range(k):
            if i != r and tab[i][j] != 0:
                f = tab[i][j]; row = tab[r]; tab[i] = [x - f * y for x, y in zip(tab[i], row)]
        basis[r] = j

    def run(cost, allowed):
        while True:
            cb = [cost[b] for b in basis]; ent = None
            for j in range(allowed):
                if j in basis: continue
                rc = cost[j] - sum(cb[r] * tab[r][j] for r in range(k) if cb[r] != 0 and tab[r][j] != 0)
                if rc > 0: ent = j; break
            if ent is None: return None
            best = None
            for r in range(k):
                if tab[r][ent] > 0:
                    ratio = tab[r][-1] / tab[r][ent]
                    if best is None or ratio < best[0] or (ratio == best[0] and basis[r] < basis[best[1]]): best = (ratio, r)
            if best is None: return ent
            pivot(best[1], ent)

    run([Fr(0)] * n + [Fr(-1)] * k, n + k)
    if any(basis[r] >= n and tab[r][-1] != 0 for r in range(k)): return ("infeasible",)
    for r in range(k):                                                   # drive the artificial variables out of the basis
        if basis[r] >= n:
            j = next((j for j in range(n) if tab[r][j] != 0), None)
            if j is not None: pivot(r, j)
    cost = list(c) + [Fr(0)] * k; ent = run(cost, n)
    if ent is not None:
        ray = [Fr(0)] * n; ray[ent] = Fr(1)
        for r in range(k):
            if basis[r] < n: ray[basis[r]] = -tab[r][ent]
        return ("unbounded", ray)
    lam = [Fr(0)] * n
    for r in range(k):
        if basis[r] < n: lam[basis[r]] = tab[r][-1]
    cb = [cost[b] for b in basis]; y = [sg[q] * sum(cb[r] * tab[r][n + q] for r in range(k)) for q in range(k)]
    return ("optimal", sum(x * z for x, z in zip(c, lam)), lam, y)


def build(d, mode):
    A, B = T.family(d); C = []
    for n in range(7, N + 1): C.append(("a_%d >= 0" % n, A[n]))
    for n in range(1, N + 1): C.append(("b_%d >= 0" % n, B[n]))
    low = {"base": ((2, 462), (3, 8316), (4, 1386)), "ext": ((2, 462), (3, 24948), (4, 388080), (5, 196812)),
           "ext2": ((2, 462), (3, 24948), (4, 1431738), (5, 3415104), (6, 10844064)),
           "ext3": ((2, 462), (3, 24948), (4, 1431738), (5, 17668728), (6, 23272326), (7, 5987520))}[mode.split("+")[0]]
    for n, lo in low: C.append(("b_%d >= %d" % (n, lo), T.add(B[n], T.aff(lo), -1)))
    for k in range(1, N // 7 + 1): C.append(("a_%d >= b_%d" % (7 * k, k), T.add(A[7 * k], B[k], -1)))
    for part in mode.split("+")[1:]:
        if part == "a7": C.append(("a_7 <= 0", T.sc(A[7], -1)))
        elif part == "caps": C.append(("a_7 <= 7920", T.add(T.aff(7920), A[7], -1))); C.append(("b_1 <= 3784", T.add(T.aff(3784), B[1], -1))); C.append(("a_8 <= 27720", T.add(T.aff(27720), A[8], -1)))
        elif part.startswith("min:"):                                     # what-if: no vector of L1 of norm < 2m
            for n in range(7, int(part[4:])): C.append(("a_%d <= 0" % n, T.sc(A[n], -1)))
        elif part.startswith("cap:"):
            for item in part[4:].split(","):
                nm, val = item.split("="); n = int(nm[1:]); C.append(("%s <= %s" % (nm, val), T.add(T.aff(int(val)), B[n], -1)))
    return A, B, C


def feasible(C):
    """('feasible', beta) or ('infeasible', certificate), both re-verified."""
    res = simplex([f[1:] for _, f in C], [-f[0] for _, f in C], [Fr(0)] * 7)
    if res[0] == "unbounded":
        lam = res[1]; assert all(x >= 0 for x in lam)
        assert all(sum(l * f[k] for l, (_, f) in zip(lam, C)) == 0 for k in range(1, 8)) and sum(l * f[0] for l, (_, f) in zip(lam, C)) < 0
        return ("infeasible", [(C[i][0], lam[i]) for i in range(len(C)) if lam[i]])
    assert res[0] == "optimal" and res[1] == 0
    return ("feasible", None)


def minimise(C, form):
    """exact minimum of the affine form over the polytope: ('min', value, beta) | ('unbounded',) | ('infeasible',)"""
    res = simplex([f[1:] for _, f in C], [-f[0] for _, f in C], form[1:])
    if res[0] == "infeasible": return ("unbounded",)                     # only called on a non-empty polytope
    if res[0] == "unbounded": return ("infeasible",)
    _, val, lam, y = res
    assert all(x >= 0 for x in lam) and all(sum(l * f[k] for l, (_, f) in zip(lam, C)) == form[k] for k in range(1, 8))
    assert all(f[0] + sum(f[k] * y[k - 1] for k in range(1, 8)) >= 0 for _, f in C), "primal point not feasible"
    assert sum(form[k] * y[k - 1] for k in range(1, 8)) == val
    return ("min", form[0] + val, y)


def show(x):
    if x.denominator == 1 and abs(x) < 10 ** 15: return str(x.numerator)
    return "%.9g" % float(x)


if __name__ == "__main__":
    mode = sys.argv[2]; ds = [int(x) for x in sys.argv[3:]] or list(range(2, 44, 2))
    T.selfcheck(); print("mode %s, N = %d" % (mode, N), flush=True)
    for d in ds:
        A, B, C = build(d, mode); st = feasible(C)
        if st[0] == "infeasible":
            print("d = %2d (r = %2d): INFEASIBLE, exact Farkas certificate on %d constraints: %s" % (d, d + 1, len(st[1]), ", ".join(nm for nm, _ in st[1])), flush=True); continue
        parts = []
        for nm, f in (("a_7", A[7]), ("a_8", A[8]), ("b_1", B[1]), ("b_2", B[2]), ("b_3", B[3])):
            lo = minimise(C, f); hi = minimise(C, T.sc(f, -1))
            parts.append("%s in [%s, %s]" % (nm, show(lo[1]) if lo[0] == "min" else "-inf", show(-hi[1]) if hi[0] == "min" else "+inf"))
        print("d = %2d (r = %2d): feasible; %s" % (d, d + 1, "; ".join(parts)), flush=True)
