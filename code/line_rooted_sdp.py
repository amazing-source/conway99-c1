"""Rooted-at-a-line SDP (notes/99): can a line L with pi(L) = j prisms exist?
For a fixed line L, y[r1,r2,r3] = #{(M,N) : rel(L,M)=r1, rel(L,N)=r2, rel(M,N)=r3} (symmetric in r1, r2).
Exact per-line data: n_r(L) (depends on j), the concurrent / edge-through structure of lines meeting L
(mu_L = sum over the 3 edges of L of the number of prisms having that edge as a rung, free in [0, 3t]),
y[m,e,m] = e n_e, y[m,3,e'] = 3(t-1) j [e'=1], per-line idempotence
  sum_{r1,r3} pi(r1) pi(r3) y[r1,r2,r3] = n_{r2} pi(r2)   (from (Pi^2)_{LN} = Pi_{LN}),
and positivity of G_kappa[r1,r2] = sum_r3 y[r1,r2,r3] kappa(r3) for Hadamard products kappa of the 4 projections.
Usage: line_rooted_sdp.py t maxdeg [--validate]
"""
import sys, itertools
import numpy as np
import sympy as sp
import cvxpy as cp
from line_triples_gen import Model, R
from line_triples_sdp import kernels

SC = 100.0


def per_line(M, j):
    t = M.t
    n = {r: M.alpha[r] + M.beta[r] * j for r in R}
    return n


def build(M, j, maxdeg, fine=False):
    t = M.t
    n = per_line(M, j)
    keys = [(r1, r2, r3) for r1 in R for r2 in R for r3 in R if R.index(r1) <= R.index(r2)]
    y = {k: cp.Variable(nonneg=True) for k in keys}
    muL = cp.Variable(nonneg=True)

    def Y(r1, r2, r3):
        return y[(r1, r2, r3)] if R.index(r1) <= R.index(r2) else y[(r2, r1, r3)]
    cons = [muL <= 3 * t]      # mu_L = sum over the 3 edges e of L of m(e) (prisms with rung e); m(e) <= t
    # coincidences
    for r1 in R:
        for r2 in R:
            for r3 in R:
                if R.index(r1) > R.index(r2):
                    continue
                v = None
                if r1 == 's':
                    v = n[r2] if r3 == r2 else 0
                elif r3 == 's':
                    v = n[r1] if r1 == r2 else 0
                elif (r1, r2) == ('m', 'm'):
                    v = {'m': 3 * t * (t - 1), 0: 0}.get(r3)
                    if r3 == 3: cons.append(Y(r1, r2, r3) == 2 * muL); continue
                    if r3 == 2: cons.append(Y(r1, r2, r3) == 12 * t - 4 * muL); continue
                    if r3 == 1: cons.append(Y(r1, r2, r3) == 6 * (t * t - 2 * t) + 2 * muL); continue
                elif r1 == 'm' and r3 == 'm':
                    v = r2 * n[r2]
                elif r1 == 'm' and r2 == 3:
                    v = 3 * (t - 1) * j if r3 == 1 else 0
                if v is not None:
                    cons.append(Y(r1, r2, r3) == v)
    if fine:
        # exact local structure of lines M through a point of L relative to a line N disjoint from L (notes/99 §4 bis)
        A2 = cp.Variable(nonneg=True); al1 = cp.Variable(nonneg=True); B1 = cp.Variable(nonneg=True); C0 = cp.Variable(nonneg=True)
        n0, n1, n2 = n[0], n[1], n[2]
        cons += [A2 <= 2 * n2, al1 <= n1, B1 <= 4 * n1, C0 <= 3 * 3 * n0]
        cons += [Y('m', 2, 3) == 0, Y('m', 2, 2) == 2 * n2 + A2, Y('m', 2, 1) == (2 * t) * n2 - 2 * A2,
                 Y('m', 2, 0) == (t - 4) * n2 + A2,
                 Y('m', 1, 3) == al1, Y('m', 1, 2) == 2 * (n1 - al1) + B1,
                 Y('m', 1, 1) == (t + 7) * n1 + al1 - 2 * B1, Y('m', 1, 0) == (2 * t - 10) * n1 + B1,
                 Y('m', 0, 3) == 0, Y('m', 0, 2) == C0, Y('m', 0, 1) == 18 * n0 - 2 * C0,
                 Y('m', 0, 0) == (3 * t - 18) * n0 + C0]
    # marginals
    for r1 in R:
        for r2 in R:
            if R.index(r1) <= R.index(r2):
                cons.append(sum(Y(r1, r2, r3) for r3 in R) == n[r1] * n[r2])
    # per-line idempotence
    for key in ('r', 's', 'ker'):
        pk = {r: float(M.pi[key][r]) for r in R}
        for r2 in R:
            cons.append(sum(pk[r1] * pk[r3] * Y(r1, r2, r3) for r1 in R for r3 in R) == n[r2] * pk[r2])
    # rooted Gram positivity
    for kern in kernels(M, maxdeg):
        kk = {r: float(kern[r]) for r in R}
        sc = max(abs(v) for v in kk.values())
        G = cp.bmat([[sum(kk[r3] * Y(r1, r2, r3) for r3 in R) / sc for r2 in R] for r1 in R])
        cons.append((G + G.T) / 2 >> 0)
    return y, muL, cons, n


def validate_bvls():
    import graphs, rooted
    A = graphs.bvls(); nV = len(A)
    Ls = rooted.lines(A); Lam = len(Ls)
    NL = np.zeros((nV, Lam), dtype=np.int64)
    for jj, l in enumerate(Ls):
        for p in l: NL[p, jj] = 1
    meet = NL.T @ NL; E = NL.T @ A @ NL; Id = np.eye(Lam, dtype=bool)
    rel = np.empty((Lam, Lam), dtype=object)
    code = np.where(Id, 0, np.where(meet == 1, 1, 2 + E))     # 0 s, 1 m, 2+e disjoint
    names = ['s', 'm', 0, 1, 2, 3]
    L = 0
    M10 = Model(10)
    yv = {}
    for r1 in range(6):
        S1 = np.nonzero(code[L] == r1)[0]
        for r2 in range(6):
            S2 = np.nonzero(code[L] == r2)[0]
            sub = code[np.ix_(S1, S2)]
            for r3 in range(6):
                yv[(names[r1], names[r2], names[r3])] = int((sub == r3).sum())
    j = yv[('s', 3, 3)]
    y, muL, cons, n = build(M10, j, 3, fine=False)
    cons_f = build(M10, j, 3, fine=True)
    # evaluate constraints at the true point
    for k, var in y.items():
        var.value = float(yv[k])
    muL.value = yv[('m', 'm', 3)] / 2
    viol = [c for c in cons if not (c.value() if hasattr(c, 'value') else True)]
    worst = max((float(np.max(np.abs(c.violation()))) for c in cons), default=0.0)
    print(f'BvLS line: pi = {j}, mu_L = {muL.value}; max constraint violation at the true point: {worst:.3g}')
    # fine model: set its y and the auxiliary variables from the true counts
    yf, muf, consf, nf = cons_f
    for k, var in yf.items():
        var.value = float(yv[k])
    muf.value = yv[('m', 'm', 3)] / 2
    aux = [v for v in consf[0].variables()] if False else None
    import itertools as _it
    # recover A2, al1, B1, C0 from the definitions (true values)
    vals = {'A2': yv[('m', 2, 2)] - 2 * nf[2], 'al1': yv[('m', 1, 3)], 'B1': yv[('m', 1, 2)] - 2 * (nf[1] - yv[('m', 1, 3)]),
            'C0': yv[('m', 0, 2)]}
    fv = set()
    for c in consf:
        for v in c.variables():
            fv.add(v)
    extra = [v for v in fv if v not in set(yf.values()) and v is not muf]
    extra.sort(key=lambda v: v.id)
    for v, key in zip(extra, ['A2', 'al1', 'B1', 'C0']):
        v.value = float(vals[key])
    worstf = max((float(np.max(np.abs(c.violation()))) for c in consf), default=0.0)
    print(f'fine model at the true BvLS point: max violation {worstf:.3g}  (A2, al1, B1, C0 = {vals})')


def main():
    t = int(sys.argv[1]); maxdeg = int(sys.argv[2])
    if '--validate' in sys.argv:
        validate_bvls(); return
    M = Model(t)
    fine = '--fine' in sys.argv
    js = [int(a.split('=')[1]) for a in sys.argv if a.startswith('--j=')] or list(range(0, 2 * t + 1))
    for j in js:
        y, muL, cons, n = build(M, j, maxdeg, fine)
        prob = cp.Problem(cp.Minimize(0), cons)
        status = None
        for solver, kw in (('CLARABEL', {}), ('SCS', {'eps': 1e-8, 'max_iters': 50000})):
            try:
                prob.solve(solver=solver, **kw)
                status = f'{prob.status} ({solver})'
                if prob.status in ('optimal', 'infeasible'):
                    break
            except Exception as ex:
                status = f'{solver} error: {str(ex)[:60]}'
        rng_mu = ''
        if prob.status == 'optimal' and '--mu' in sys.argv:
            lo = cp.Problem(cp.Minimize(muL), cons); lo.solve(solver='CLARABEL')
            hi = cp.Problem(cp.Maximize(muL), cons); hi.solve(solver='CLARABEL')
            rng_mu = f'  mu_L in [{lo.value:.2f}, {hi.value:.2f}]'
        print(f't={t} fine={fine} pi(L)={j:2d}: {status}{rng_mu}', flush=True)


if __name__ == '__main__':
    main()
