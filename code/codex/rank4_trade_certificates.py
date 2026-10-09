"""Exact certificates for the four bounded difference cores.

The LP supplies multipliers only. Every resulting bound is checked with
rational arithmetic; no solver infeasibility status is used as a proof.
"""
import itertools as it
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[2]
source = json.loads((ROOT/'data/codex_rank4_grid_trade_probe.json').read_text())
certificates = []
for rec in source['pilot_representatives']:
    d = sp.Matrix(rec['D'])
    n = d.rows
    a0 = d.applyfunc(lambda z: int(z == -1))
    pairs = [(i, j) for i in range(n) for j in range(i+1, n) if d[i, j] == 0]
    es = []
    for i, j in pairs:
        e = sp.zeros(n)
        e[i, j] = e[j, i] = 1
        es.append(e)
    eq = sp.Matrix.hstack(*[(e*d+d*e).reshape(n*n, 1) for e in es])
    rhs = -(a0*d+d*a0+d*d+d).reshape(n*n, 1)
    sol, parameters = eq.gauss_jordan_solve(rhs)
    assert eq*sol == rhs
    # gauss_jordan_solve parameters are actual free edge coordinates.
    free_indices = {p: next(i for i, x in enumerate(sol) if x == p) for p in parameters}
    cert = {'n': n, 'D': [[int(v) for v in row] for row in d.tolist()], 'common_edge_variables': pairs,
            'free_variable_indices': {str(p): i for p, i in free_indices.items()},
            'affine_solution': [str(x) for x in sol]}
    if n != 15:
        witnesses = []
        for i, x in enumerate(sol):
            constant = x.subs({p: 0 for p in parameters})
            coefficients = [x.coeff(p) for p in parameters]
            if constant.q != 1 and all(c.q == 1 for c in coefficients):
                witnesses.append({'variable': i, 'expression': str(x)})
        assert witnesses
        cert['integer_contradiction'] = witnesses[0]
    else:
        w = sp.Matrix.hstack(*d.columnspace())
        rows = list(w.T.rref()[1])
        left = w[rows, :].inv()
        h0 = left*(a0*w)[rows, :]
        hs = [left*(e*w)[rows, :] for e in es]
        h = h0 + sum((x*z for x, z in zip(sol, hs)), sp.zeros(4))
        coords = [(0, 0), (0, 1), (1, 0), (2, 0)]
        abc_expr = [sp.expand(h[i, j]) for i, j in coords]
        bounds = []
        for expr in abc_expr:
            constant = expr.subs({p: 0 for p in parameters})
            coeffs = [expr.coeff(p) for p in parameters]
            assert constant.q == 1 and all(c.q == 1 for c in coeffs)
            bounds.append((int(constant+sum(min(0, c) for c in coeffs)),
                           int(constant+sum(max(0, c) for c in coeffs))))
        a, b, c, t = sp.symbols('a b c t')
        e = (3*t-4*b+4*c-4*a+22)/4
        z = 2*b+a-2*c-6
        general = sp.Matrix([[a,b,e,-3], [c,z,3,e-3],
                             [t,4,1-z,b-4], [-4,t+4,c+4,-a-3]])
        assert (general.subs(dict(zip((a,b,c,t),abc_expr)))-h).applyfunc(sp.expand) == sp.zeros(4)
        # c is -2 plus twice a difference of binary free coordinates.
        assert abc_expr[2] == -2*parameters[16]+2*parameters[21]-2
        admissible = []
        for aa, bb, cc, tt in it.product(range(bounds[0][0], bounds[0][1]+1),
                                         range(bounds[1][0], bounds[1][1]+1),
                                         (-4,-2,0), range(bounds[3][0], bounds[3][1]+1)):
            ee = 3*tt-4*bb+4*cc-4*aa+22
            zz = 2*bb+aa-2*cc-6
            h4 = np.array([[4*aa,4*bb,ee,-12],[4*cc,4*zz,12,ee-12],
                           [4*tt,16,4-4*zz,4*bb-16],[-16,4*tt+16,4*cc+16,-4*aa-12]], dtype=np.int64)
            if np.all(h4@h4+4*h4-192*np.eye(4,dtype=np.int64)==0):
                admissible.append([aa,bb,cc,tt])
        assert admissible == [[-4,2,-2,-2],[1,2,-2,-2]]
        cert['restriction_formula'] = [[str(x) for x in row] for row in general.tolist()]
        cert['coordinate_bounds'] = bounds
        cert['spectral_integer_tuples'] = admissible
        ex = eq.copy()
        bx = rhs.copy()
        for i, j, value in [(0,1,2),(1,0,-2),(2,0,-2)]:
            ex = ex.col_join(sp.Matrix([[z[i,j] for z in hs]]))
            bx = bx.col_join(sp.Matrix([value-h0[i,j]]))
        objective = sp.Matrix([z[0,0] for z in hs])
        dual_certificates = []
        for sign in (1,-1):
            result = linprog(np.array(sign*objective,dtype=float).ravel(),
                             A_eq=np.array(ex,dtype=float), b_eq=np.array(bx,dtype=float).ravel(),
                             bounds=(0,1), method='highs')
            assert result.success
            y = sp.Matrix([sp.Rational(float(v)).limit_denominator(10000) for v in result.eqlin.marginals])
            remainder = sign*objective-ex.T*y
            lower = (y.T*bx)[0]+sum(min(0, r) for r in remainder)
            a_bound = h0[0,0]+sign*lower
            assert a_bound == (-3 if sign == 1 else 0)
            dual_certificates.append({'sign': sign, 'bound_on_a': str(a_bound),
                                      'equality_multipliers': [[i,str(v)] for i,v in enumerate(y) if v],
                                      'remainder': [[i,str(v)] for i,v in enumerate(remainder) if v]})
        cert['exact_box_dual_certificates'] = dual_certificates
    certificates.append(cert)
    print(json.dumps({'n': n, 'exact_certificate': 'nonintegral edge' if n != 15 else 'spectral tuples violate -3 <= a <= 0'}))

dest = ROOT/'data/codex_rank4_trade_certificates.json'
dest.write_text(json.dumps({'certificates': certificates, 'all_exact_checks_pass': True},
                           indent=2), encoding='utf-8')
print(str(dest))
