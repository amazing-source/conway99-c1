"""SDP on line-triple counts (notes/99), general t (line_triples_gen.Model): optimise P (or Q2 at fixed P) subject to
exact identities (marginals, idempotence of the four projections of the line space), nonnegativity of all counts,
positivity of the aggregated rooted Gram matrices, and optionally the Cauchy-Schwarz bound 231 Q2 >= 4 P^2.
Variables are scaled by 1/SC for numerical stability.
Usage: line_triples_sdp.py t [--cs] [--scanQ]
"""
import sys
import numpy as np
import sympy as sp
import cvxpy as cp
from line_triples_gen import Model, R

SC = 1000.0


def kernels(M, maxdeg):
    """Hadamard products (degree 1..maxdeg) of the four projections: PSD kernels depending only on the relation."""
    import itertools
    keys = list(M.pi)
    out = []
    for deg in range(1, maxdeg + 1):
        for combo in itertools.combinations_with_replacement(keys, deg):
            k = {r: sp.Integer(1) for r in R}
            for key in combo:
                k = {r: k[r] * M.pi[key][r] for r in R}
            if any(v != 0 for v in k.values()):
                out.append(k)
    return out


def build(M, use_cs, maxdeg=1):
    eqs = [e[3] for e in M.equations() if e[3] != 0]
    syms = [M.P, M.Q2] + list(M.na) + list(M.X9.values())
    var = cp.Variable(len(syms))
    idx = {s: i for i, s in enumerate(syms)}

    def lin(expr, scale=1.0):
        expr = sp.expand(sp.sympify(expr))
        coeffs = np.zeros(len(syms))
        const = 0.0
        for term, c in expr.as_coefficients_dict().items():
            if term == 1:
                const += float(c)
            else:
                coeffs[idx[term]] += float(c)
        # var holds value / SC
        return (coeffs * SC) @ var / scale + const / scale

    cons = []
    for e in eqs:
        ex = sp.expand(e)
        mx = max(abs(float(c)) for c in ex.as_coefficients_dict().values())
        cons.append(lin(ex, mx) == 0)
    cons += [var >= 0]
    P, Q2 = var[idx[M.P]], var[idx[M.Q2]]
    lines = float(M.Lam)
    pmax = float(M.t * M.Lam)          # P_max = t E / 3 = t * #lines
    cons += [Q2 <= 2 * (2 * M.t) * P, Q2 >= 2 * P, P <= pmax / SC]
    if use_cs:
        cons += [lines * Q2 >= 4 * SC * cp.square(P)]
    for kern in kernels(M, maxdeg):
        G = [[lin(sum(kern[r3] * M.X(r1, r2, r3) for r3 in R), SC * max(abs(float(v)) for v in kern.values()))
              for r2 in R] for r1 in R]
        Gm = cp.bmat(G)
        cons.append((Gm + Gm.T) / 2 >> 0)
    for r1 in R:
        for r2 in R:
            for r3 in R:
                ex = sp.sympify(M.X(r1, r2, r3))
                if ex.free_symbols:
                    cons.append(lin(ex, SC) >= 0)
    return var, idx, cons


def solve(prob):
    for solver, kw in (('CLARABEL', {}), ('SCS', {'eps': 1e-9, 'max_iters': 200000})):
        try:
            prob.solve(solver=solver, **kw)
            if prob.status in ('optimal', 'optimal_inaccurate', 'infeasible', 'unbounded'):
                return solver
        except Exception as ex:
            print('  ', solver, 'failed:', str(ex)[:80])
    return None


def main():
    t = int(sys.argv[1])
    M = Model(t)
    use_cs = '--cs' in sys.argv
    maxdeg = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--deg=')), 1))
    var, idx, cons = build(M, use_cs, maxdeg)
    print(f'kernels up to degree {maxdeg}: {len(kernels(M, maxdeg))}', flush=True)
    P, Q2 = var[idx[M.P]], var[idx[M.Q2]]
    for sense in ('min', 'max'):
        prob = cp.Problem(cp.Minimize(P) if sense == 'min' else cp.Maximize(P), cons)
        sv = solve(prob)
        print(f't={t} cs={use_cs} {sense} P: {prob.status} via {sv}: {None if prob.value is None else prob.value * SC:.4f}', flush=True)
    if '--scanQ' in sys.argv:
        pmax = float(M.t * M.Lam)
        for frac in (0.0, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0):
            Pv = frac * pmax
            c2 = cons + [P == Pv / SC]
            lo = cp.Problem(cp.Minimize(Q2), c2); solve(lo)
            hi = cp.Problem(cp.Maximize(Q2), c2); solve(hi)
            f = lambda pr: None if pr.value is None else pr.value * SC
            print(f'  P = {Pv:8.1f}: Q2 in [{f(lo)}, {f(hi)}]  ({lo.status}/{hi.status});  CS needs Q2 >= {4 * Pv * Pv / float(M.Lam):.1f}', flush=True)


if __name__ == '__main__':
    main()
