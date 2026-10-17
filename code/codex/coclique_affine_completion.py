"""Exact binary completion using only the residual affine degrees of freedom.

Given a valid binary boundary factor and one complete neighbourhood, let
V={T: T=T.T, diag(T)=0, D*T=0}. Both differences of linear completions
and the polynomial defect of a binary linear completion belong to V.
Consequently dim(V) selected edge equations suffice for the entire graph.
With regularity=True, append 1.T to D and use V={T: T=T.T,
diag(T)=0, D*T=0, T*1=0}; no complete neighbourhood is then required.
This implements the singular case without searching continuous projectors.
"""
from itertools import combinations
from pathlib import Path
from math import gcd, lcm
import argparse
import json
import time
import sympy as sp
from ortools.sat.python import cp_model
from coclique_global_completion import eliminate, encode
from coclique_regular_completion import eliminate_regular


def frame(B, D, k=14, mu=2, regularity=False):
    B, D = sp.Matrix(B), sp.Matrix(D)
    data = (eliminate_regular if regularity else eliminate)(B, D, k=k, mu=mu)
    constraints = data['constraint_matrix'] if regularity else D
    rhs = data['constraint_rhs'] if regularity else data['F']
    E0 = data['E0']; m = D.cols
    columns = constraints.nullspace()
    N = sp.Matrix.hstack(*columns) if columns else sp.zeros(m, 0)
    h = N.cols
    pairs = [(a, b) for a in range(h) for b in range(a, h)]
    diagonal = sp.Matrix(m, len(pairs), lambda i, j:
        N[i, pairs[j][0]] * N[i, pairs[j][1]] * (1 if pairs[j][0] == pairs[j][1] else 2))
    target = -sp.Matrix([E0[i, i] for i in range(m)])
    report = dict(rank=data['rank'], nullity=h, diagonal_rank=diagonal.rank(),
                  dimension=len(pairs)-diagonal.rank(), kernel=encode(N))
    if regularity:
        report.update(regularity=True, boundary_rank=data['boundary_rank'],
                      regularity_rank_gain=data['regularity_rank_gain'])
    try:
        solution, parameters = diagonal.gauss_jordan_solve(target)
    except ValueError:
        return dict(**report, status='NO_REAL_ZERO_DIAGONAL_COMPLETION')
    solution = solution.subs({p: 0 for p in parameters})

    def lift(coefficients):
        S = sp.zeros(h)
        for value, (a, b) in zip(coefficients, pairs):
            S[a, b] = S[b, a] = value
        return N*S*N.T

    particular = E0 + lift(solution)
    basis = [lift(v) for v in diagonal.nullspace()]
    edges = list(combinations(range(m), 2))
    delta = len(basis)
    W = sp.Matrix(len(edges), delta, lambda i, j: basis[j][edges[i]])
    positions = W.T.rref()[1] if delta else ()
    assert len(positions) == delta
    chosen = [edges[i] for i in positions]
    if delta:
        inverse = W[list(positions), :].inv()
        basis = [sum((basis[i]*inverse[i, j] for i in range(delta)), sp.zeros(m))
                 for j in range(delta)]
    base = particular - sum((particular[u, v]*T for (u, v), T in zip(chosen, basis)), sp.zeros(m))
    assert constraints*base == rhs and base == base.T
    assert all(base[i, i] == 0 for i in range(m))
    for a, T in enumerate(basis):
        assert T == T.T and constraints*T == sp.zeros(constraints.rows, m)
        assert all(T[i, i] == 0 for i in range(m))
        assert [T[u, v] for u, v in chosen] == [int(a == b) for b in range(delta)]
    return dict(**report, status='AFFINE_FRAME', base=base, basis=basis,
                selected_pairs=chosen, E0=E0, P=data['P'])


def polynomial_defect(B, D, E, k, mu):
    return D.T*D + E*E + E - (k-mu)*sp.eye(E.rows) - mu*sp.ones(E.rows)


def parity_cuts(data, D, mu):
    """Primitive integer residual polynomials whose quadratic part is even.

    These are necessary XOR laws. They replace no quadratic equation unless
    a separate argument proves sufficiency, as in the Petersen certificate.
    """
    base, basis = data['base'], data['basis']
    gram = D.T*D; cuts = []
    for u, v in data['selected_pairs']:
        dot = lambda X, Y: (X.row(u)*Y[:, v])[0]
        constant = gram[u, v]+dot(base, base)+base[u, v]-mu
        linear = [dot(base, T)+dot(T, base)+dot(T, T)+T[u, v] for T in basis]
        quadratic = [(i, j, dot(basis[i], basis[j])+dot(basis[j], basis[i]))
                     for i, j in combinations(range(len(basis)), 2)]
        values = [constant]+linear+[q for i, j, q in quadratic]
        denominator = lcm(*(int(x.q) for x in values))
        integers = [int(x*denominator) for x in values]
        divisor = gcd(*integers)
        if not divisor: continue
        integers = [x//divisor for x in integers]
        if any(q % 2 for q in integers[1+len(basis):]): continue
        indices = [i for i, value in enumerate(integers[1:1+len(basis)]) if value % 2]
        cuts.append(dict(pair=[u, v], indices=indices, rhs=integers[0] % 2,
                         primitive_polynomial=dict(constant=integers[0], linear=integers[1:1+len(basis)],
                            quadratic=[[i, j, q] for (i, j, _), q in zip(quadratic, integers[1+len(basis):]) if q])))
    return cuts


def binary_completions(B, D, k=14, mu=2, seconds=60, enumerate_all=False, regularity=False,
                      rank_one_first=False):
    start = time.monotonic()
    B, D = sp.Matrix(B), sp.Matrix(D)
    if rank_one_first:
        if not regularity:
            raise ValueError('rank_one_first requires the augmented regularity boundary')
        from coclique_rank_one_completion import complete_rank_one
        reduced = complete_rank_one(B, D, k, mu)
        if reduced['status'] != 'NOT_APPLICABLE':
            return dict(reduced, complete=True, seconds=time.monotonic()-start,
                        quadratic_pairs=0, completion_method='rank_one_signs',
                        verdict=reduced['status'])
    data = frame(B, D, k=k, mu=mu, regularity=regularity)
    summary = {key: value for key, value in data.items() if key not in ('base', 'basis', 'E0', 'P')}
    if data['status'] != 'AFFINE_FRAME':
        return dict(**summary, completions=[], complete=True, seconds=time.monotonic()-start)
    base, basis, chosen = data['base'], data['basis'], data['selected_pairs']
    m = D.cols; delta = len(basis); gram = D.T*D
    summary.update(base=encode(base), basis=[encode(T) for T in basis])
    if not delta:
        binary = all(x in (0, 1) for x in base)
        if binary:
            assert polynomial_defect(B, D, base, k, mu) == sp.zeros(m)
        return dict(**summary, completions=[encode(base)] if binary else [], complete=True,
                    verdict='UNIQUE_BINARY' if binary else 'UNIQUE_NONBINARY',
                    seconds=time.monotonic()-start, quadratic_pairs=0)
    model = cp_model.CpModel()
    free = [model.NewBoolVar(f'free_{u}_{v}') for u, v in chosen]
    cuts = parity_cuts(data, D, mu) if delta <= 24 else []
    summary.update(parity_cuts=cuts, parity_extraction='performed' if delta <= 24 else 'skipped_large_dimension')
    unique = set()
    for cut in cuts:
        key = (tuple(cut['indices']), cut['rhs'])
        if key in unique: continue
        unique.add(key)
        literals = [free[i] for i in cut['indices']]
        if not cut['rhs']: literals.append(True)
        model.AddBoolXOr(literals)
    variables = {}
    for u, v in combinations(range(m), 2):
        coefficients = [T[u, v] for T in basis]
        if (u, v) in chosen:
            variables[u, v] = free[chosen.index((u, v))]
            continue
        denominator = lcm(*(int(x.q) for x in [base[u, v]] + coefficients))
        constant = int(base[u, v]*denominator)
        weights = [int(x*denominator) for x in coefficients]
        if not any(weights):
            if constant not in (0, denominator):
                return dict(**summary, completions=[], complete=True, verdict='FORCED_NONBINARY',
                            seconds=time.monotonic()-start, quadratic_pairs=delta)
            variables[u, v] = constant//denominator
        else:
            if max([abs(constant), denominator] + [abs(x) for x in weights]) >= 2**50:
                return dict(**summary, completions=[], complete=False,
                            verdict='INTEGER_COEFFICIENTS_EXCEED_IMPLEMENTED_SOLVER_RANGE',
                            seconds=time.monotonic()-start)
            e = model.NewBoolVar(f'e_{u}_{v}')
            variables[u, v] = e
            model.Add(denominator*e == constant + sum(w*x for w, x in zip(weights, free)))
    edge = lambda u, v: 0 if u == v else variables[tuple(sorted((u, v)))]
    for u, v in combinations(range(m), 2):
        model.Add(edge(u, v) + int(gram[u, v]) <= mu)
    for u in range(m):
        model.Add(sum(edge(u, v) for v in range(m)) == k-int(gram[u, u]))
    products = {}
    def multiply(a, b):
        if isinstance(a, int): return b if a else 0
        if isinstance(b, int): return a if b else 0
        key = tuple(sorted((a.Index(), b.Index())))
        if key not in products:
            z = model.NewBoolVar(f'p{len(products)}')
            model.Add(z <= a); model.Add(z <= b); model.Add(z >= a+b-1)
            products[key] = z
        return products[key]
    for u, v in chosen:
        model.Add(sum(multiply(edge(u, w), edge(v, w)) for w in range(m)) + edge(u, v)
                  == mu-int(gram[u, v]))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.enumerate_all_solutions = enumerate_all
    answers = []
    class Collect(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            value = lambda x: x if isinstance(x, int) else self.Value(x)
            E = sp.Matrix(m, m, lambda u, v: value(edge(u, v)))
            assert polynomial_defect(B, D, E, k, mu) == sp.zeros(m)
            answers.append(encode(E))
    status = solver.Solve(model, Collect())
    return dict(**summary, verdict=solver.StatusName(status), completions=answers,
                complete=status == cp_model.INFEASIBLE or (enumerate_all and status == cp_model.OPTIMAL),
                seconds=time.monotonic()-start, quadratic_pairs=delta,
                product_variables=len(products), branches=solver.NumBranches(), conflicts=solver.NumConflicts())


def controls(folder):
    folder.mkdir(parents=True, exist_ok=True)
    graphs = []
    rook = sp.Matrix(9, 9, lambda i, j: int(i != j and (i//3 == j//3 or i%3 == j%3)))
    graphs.append(('rook', rook, 4, 2))
    vertices = list(combinations(range(5), 2))
    petersen = sp.Matrix(10, 10, lambda i, j: int(set(vertices[i]).isdisjoint(vertices[j])))
    graphs.append(('petersen', petersen, 3, 1))
    for p in (13, 17):
        squares = {i*i % p for i in range(1, p)}
        A = sp.Matrix(p, p, lambda i, j: int((i-j) % p in squares))
        graphs.append((f'paley{p}', A, (p-1)//2, (p-1)//4))
    summaries = []
    for name, A, k, mu in graphs:
        border = [0] + [i for i in range(1, A.rows) if A[0, i]]
        outside = [i for i in range(A.rows) if i not in border]
        B, D = A[border, border], A[border, outside]
        result = binary_completions(B, D, k, mu, seconds=60, enumerate_all=True)
        result.update(name=name, k=k, mu=mu, B=encode(B), D=encode(D), actual=encode(A[outside, outside]))
        assert result['actual'] in result['completions']
        (folder/(name+'.json')).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        summary = {key: result.get(key) for key in ('name', 'rank', 'nullity', 'dimension', 'diagonal_rank',
            'verdict', 'complete', 'quadratic_pairs', 'seconds')}
        summary['completions'] = len(result['completions'])
        summaries.append(summary)
        print(json.dumps(summary), flush=True)
    (folder/'summary.json').write_text(json.dumps(dict(status='PASS', controls=summaries,
        scope='New exact reduction on known graphs; no Conway exclusion'), indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    controls(args.folder)
