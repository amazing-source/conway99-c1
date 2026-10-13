"""Exact completion by integer linear cuts obtained from spectral witnesses.

Under the complete-neighbourhood hypotheses of coclique_global_completion,
an integral symmetric linear completion is an SRG precisely when
E0 + r P - E >= 0 and E - E0 - s P >= 0 (Loewner order).
No projector equation, quadratic edge products, or floating eigenvalue
tolerance is used here. The implemented separator requires rational r,s.
"""
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import argparse
import json
import time

import sympy as sp
from ortools.sat.python import cp_model

from coclique_affine_completion import frame, polynomial_defect
from coclique_global_completion import encode


def primitive_vector(vector):
    denominator = lcm(*(int(x.q) for x in vector))
    integers = [int(x*denominator) for x in vector]
    divisor = gcd(*integers)
    return sp.Matrix([x//divisor for x in integers])


def negative_witness(matrix, short=True):
    """Return rational w with w^t M w<0, or None iff M is PSD.

    Exact symmetric Schur elimination, including zero pivots. Short sign
    vectors are tried only in dimension <=6 to make certificates readable.
    """
    M = sp.Matrix(matrix)
    assert M == M.T and all(x.is_Rational for x in M)
    n = M.rows
    for i in range(n):
        if M[i, i] < 0:
            return sp.eye(n)[:, i]
    if short and 0 < n <= 6:
        for signs in product((-1, 1), repeat=n-1):
            w = sp.Matrix((1,)+signs)
            if (w.T*M*w)[0] < 0:
                return w
    for i in range(n):
        if M[i, i] != 0:
            continue
        for j in range(n):
            if M[i, j]:
                w = sp.eye(n)[:, i]
                w[j] = -M[i, j]/(M[j, j]+1)
                assert (w.T*M*w)[0] < 0
                return primitive_vector(w)
    pivots = [i for i in range(n) if M[i, i] > 0]
    if not pivots:
        assert M == sp.zeros(n)
        return None
    p = pivots[0]
    rest = [i for i in range(n) if i != p]
    b = M[rest, p]
    S = M[rest, rest] - b*b.T/M[p, p]
    v = negative_witness(S, short=False)
    if v is None:
        return None
    w = sp.zeros(n, 1)
    w[p] = -(b.T*v)[0]/M[p, p]
    for i, value in zip(rest, v):
        w[i] = value
    w = primitive_vector(w)
    assert (w.T*M*w)[0] < 0
    return w


def rounded_cut(constant, coefficients):
    """c+a.x>=0, strengthened using the integer lattice a.x lies in."""
    denominator = lcm(*(int(v.q) for v in [constant]+coefficients))
    c = int(constant*denominator)
    weights = [int(v*denominator) for v in coefficients]
    divisor = gcd(*weights) if weights else 0
    if not divisor:
        return dict(weights=weights, rhs=int(c < 0), raw_constant=c,
                    raw_weights=weights, scale=denominator, gcd=0)
    return dict(weights=[v//divisor for v in weights], rhs=-(c//divisor),
                raw_constant=c, raw_weights=weights, scale=denominator, gcd=divisor)


def separate(data, E, r, s):
    N = sp.Matrix(data['kernel'])
    if not N.cols:
        return None
    base, basis, E0, P = (data[key] for key in ('base', 'basis', 'E0', 'P'))
    for side, M in [('upper', E0+r*P-E), ('lower', E-E0-s*P)]:
        v = negative_witness(N.T*M*N)
        if v is None:
            continue
        z = primitive_vector(N*v)
        norm = (z.T*z)[0]
        if side == 'upper':
            constant = r*norm-(z.T*base*z)[0]
            coefficients = [-(z.T*T*z)[0] for T in basis]
        else:
            constant = (z.T*base*z)[0]-s*norm
            coefficients = [(z.T*T*z)[0] for T in basis]
        witness_value = (z.T*M*z)[0]
        assert witness_value < 0
        return dict(side=side, vector=[str(v) for v in z],
                    witness_value=str(witness_value), **rounded_cut(constant, coefficients))
    return None


def global_separate(A, k=14, mu=2):
    """A cut valid for every SRG with these parameters, with no fixed B,D.

    For C1 the two PSD matrices are 3I-A+J/9 and A+4I-2J/11.
    The certificate records a rational negative direction and an integer
    inequality on all graph edges. A numerical eigenvalue is never proof.
    """
    A = sp.Matrix(A)
    n = A.rows
    assert A == A.T and all(x in (0, 1) for x in A)
    assert all(A[i, i] == 0 for i in range(n))
    assert A*sp.ones(n, 1) == k*sp.ones(n, 1)
    assert k*(k+1) == k-mu+mu*n
    root = sp.sqrt(1+4*(k-mu))
    r, s = (-1+root)/2, (-1-root)/2
    if not r.is_Rational:
        raise ValueError('The implemented rational certificate needs rational endpoints')
    edges = list(combinations(range(n), 2))
    matrices = [('upper', r*sp.eye(n)-A+(k-r)*sp.ones(n)/n),
                ('lower', A-s*sp.eye(n)-(k-s)*sp.ones(n)/n)]
    for side, M in matrices:
        z = negative_witness(M)
        if z is None:
            continue
        z = primitive_vector(z)
        norm, total = (z.T*z)[0], sum(z)
        if side == 'upper':
            c = r*norm+(k-r)*total**2/n
            coefficients = [-2*z[u]*z[v] for u, v in edges]
        else:
            c = -s*norm-(k-s)*total**2/n
            coefficients = [2*z[u]*z[v] for u, v in edges]
        cut = rounded_cut(c, coefficients)
        assert sum(a*A[u, v] for a, (u, v) in zip(cut['weights'], edges)) < cut['rhs']
        active = [i for i, a in enumerate(cut['weights']) if a]
        cut['weights'] = [cut['weights'][i] for i in active]
        cut['raw_weights'] = [cut['raw_weights'][i] for i in active]
        return dict(side=side, vector=[str(v) for v in z],
                    witness_value=str((z.T*M*z)[0]), pairs=[edges[i] for i in active], **cut)
    assert A*A+A == (k-mu)*sp.eye(n)+mu*sp.ones(n)
    return None


def completions(B, D, k=14, mu=2, seconds=60, enumerate_all=False):
    start = time.monotonic()
    B, D = sp.Matrix(B), sp.Matrix(D)
    root = sp.sqrt(1+4*(k-mu))
    r, s = (-1+root)/2, (-1-root)/2
    if not r.is_Rational:
        return dict(status='UNSUPPORTED_IRRATIONAL_ENDPOINTS', complete=False, completions=[])
    data = frame(B, D, k, mu)
    if data['status'] != 'AFFINE_FRAME':
        return dict(status=data['status'], complete=True, completions=[])
    base, basis, chosen = (data[key] for key in ('base', 'basis', 'selected_pairs'))
    m, delta = D.cols, len(basis)
    model = cp_model.CpModel()
    free = [model.NewBoolVar(f'x{i}') for i in range(delta)]
    for u, v in combinations(range(m), 2):
        values = [base[u, v]]+[T[u, v] for T in basis]
        denominator = lcm(*(int(a.q) for a in values))
        c, *weights = [int(a*denominator) for a in values]
        if denominator+abs(c)+sum(map(abs, weights)) >= 2**50:
            return dict(status='UNSUPPORTED_COEFFICIENT_RANGE', complete=False, completions=[])
        e = model.NewBoolVar(f'e{u}_{v}')
        model.Add(denominator*e == c+sum(a*x for a, x in zip(weights, free)))
    cuts, answers, trials = [], [], []
    complete, status = False, 'UNKNOWN'
    while time.monotonic()-start < seconds:
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = max(.001, seconds-(time.monotonic()-start))
        result = solver.Solve(model)
        status = solver.StatusName(result)
        if result == cp_model.INFEASIBLE:
            complete = True
            break
        if result not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break
        bits = [solver.Value(x) for x in free]
        E = base+sum((a*T for a, T in zip(bits, basis)), sp.zeros(m))
        cut = separate(data, E, r, s)
        trial = dict(free=bits, is_completion=cut is None)
        trials.append(trial)
        if cut is None:
            assert polynomial_defect(B, D, E, k, mu) == sp.zeros(m)
            answers.append(encode(E))
            if not enumerate_all:
                break
            model.AddBoolOr([x.Not() if bit else x for x, bit in zip(free, bits)])
        else:
            assert sum(a*x for a, x in zip(cut['weights'], bits)) < cut['rhs']
            if abs(cut['rhs'])+sum(map(abs, cut['weights'])) >= 2**50:
                status = 'UNSUPPORTED_CUT_RANGE'
                break
            trial['cut_index'] = len(cuts)
            cut['rejected_free'] = bits
            cuts.append(cut)
            model.Add(sum(a*x for a, x in zip(cut['weights'], free)) >= cut['rhs'])
    final_solver_status = status
    if complete and answers:
        status = 'ENUMERATED_ALL'
    elif answers and not enumerate_all:
        status = 'SAT'
    elif not complete and not status.startswith('UNSUPPORTED'):
        status = 'UNKNOWN'
    return dict(status=status, final_solver_status=final_solver_status, complete=complete,
                rank=data['rank'], nullity=data['nullity'],
                dimension=delta, selected_pairs=chosen, r=str(r), s=str(s),
                cuts=cuts, trials=trials, completions=answers, quadratic_products=0,
                seconds=time.monotonic()-start)


def controls(source, folder):
    folder.mkdir(parents=True, exist_ok=True)
    reports = []
    fixtures = []
    for name in ('rook', 'petersen'):
        old = json.loads((source/(name+'.json')).read_text(encoding='utf-8'))
        fixtures.append((name, old))
    # Additional small fixtures exercise different affine dimensions; this
    # checks the new reduction, not a new graph-existence claim.
    for p, nonsquare in ((5, 2), (7, 3)):
        vertices = list(product(range(p), repeat=2))
        squares = {((a*a+nonsquare*b*b) % p, 2*a*b % p)
                   for a, b in vertices if a or b}
        A = sp.Matrix(p*p, p*p, lambda i, j: int(
            ((vertices[i][0]-vertices[j][0]) % p,
             (vertices[i][1]-vertices[j][1]) % p) in squares))
        k, mu = (p*p-1)//2, (p*p-1)//4
        assert A*A+A == (k-mu)*sp.eye(p*p)+mu*sp.ones(p*p)
        border = [0]+[i for i in range(1, p*p) if A[0, i]]
        missing = [i for i in range(p*p) if i not in border]
        B, D = A[border, border], A[border, missing]
        data = frame(B, D, k, mu)
        assert data['dimension'] <= 5
        expected = []
        for bits in product((0, 1), repeat=data['dimension']):
            E = data['base']+sum((a*T for a, T in zip(bits, data['basis'])), sp.zeros(D.cols))
            if all(x in (0, 1) for x in E) and polynomial_defect(B, D, E, k, mu) == sp.zeros(D.cols):
                expected.append(encode(E))
        assert encode(A[missing, missing]) in expected
        fixtures.append((f'paley{p*p}', dict(B=encode(B), D=encode(D), k=k, mu=mu, completions=expected)))
    for name, old in fixtures:
        result = completions(old['B'], old['D'], old['k'], old['mu'], enumerate_all=True)
        expected = {json.dumps(E) for E in old['completions']}
        assert result['complete'] and {json.dumps(E) for E in result['completions']} == expected
        result.update(B=old['B'], D=old['D'], k=old['k'], mu=old['mu'])
        (folder/(name+'.json')).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        reports.append(dict(name=name, dimension=result['dimension'], completions=len(expected), cuts=len(result['cuts']),
                            quadratic_products=0, seconds=result['seconds']))
    (folder/'summary.json').write_text(json.dumps(dict(status='PASS', controls=reports,
        scope='New spectral-cut procedure on existing examples; no C1 exclusion'), indent=2)+'\n', encoding='utf-8')
    print(json.dumps(reports), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    parser.add_argument('--source', type=Path, default=Path('data/codex_coclique_defects/affine_completion_v7'))
    args = parser.parse_args()
    controls(args.source, args.folder)
