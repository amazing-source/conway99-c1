"""Construct three-star boundaries using nonnegative integer relations.

The coefficient normalization covers every integer extra relation after
adding/subtracting the three star relations, but there is NO universal
bound on the required height. A height-limited timeout proves nothing.
Peer733's binary classification and congruences are inputs, not audited.
"""
import argparse
from itertools import combinations, product
from pathlib import Path
import json
import sys
import time

import numpy as np
import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_prescribed_kernel import (LABELS, EDGES, N, K8, S, U0,
    linear_constraints, spectral_witnesses)
from three_star_rank_repairs import boundary_masks, GROUPS
from three_star_ambient_upper import psd_or_witness


def coefficients(model, height, weight_limit=None, fixed_weight=None):
    """Necessary constraints; they do not assert existence of any graph."""
    index = {p:i for i, p in enumerate(LABELS)}
    q = [model.NewIntVar(0, height, 'q%d'%i) for i in range(N)]
    w = model.NewIntVar(0, N*height, 'weight')
    model.Add(w == sum(q))
    # T_ii=20/8 and T_ij>=-10/8 for distinct labels. Nonnegative
    # q in ker(T) gives20*q_i<=10*(w-q_i), hence3*q_i<=w.
    for value in q:
        model.Add(3*value <= w)
    quarter = model.NewIntVar(0, N*height//4, 'quarter_weight')
    model.Add(w == 4*quarter)
    if weight_limit is not None:
        model.Add(w <= weight_limit)
    if fixed_weight is not None:
        model.Add(w == fixed_weight)
    maximum = model.NewIntVar(0, height, 'maximum')
    model.AddMaxEquality(maximum, q)
    # Peer733 excludes every binary extra relation when Q is connected.
    model.Add(maximum >= 2)
    for c in (0, 1, 2):
        model.AddMinEquality(0, [q[i] for i, p in enumerate(LABELS) if c in p])
    tail = [q[i] for i, p in enumerate(LABELS) if p[0] == 2]
    tail_min = model.NewIntVar(0, height, 'tail_min')
    tail_max = model.NewIntVar(0, height, 'tail_max')
    model.AddMinEquality(tail_min, tail)
    model.AddMaxEquality(tail_max, tail)
    model.Add(tail_max > tail_min)
    d = []
    for c in range(14):
        rows = [q[i] for i, p in enumerate(LABELS) if c in p]
        value = model.NewIntVar(0, len(rows)*height, 'd%d'%c)
        model.Add(value == sum(rows))
        d.append(value)
    residue_bit = model.NewBoolVar('common_t_residue_div4')
    t = [3*d[c]+d[c ^ 1] for c in range(14)]
    for c in range(14):
        quotient = model.NewIntVar(0, 6*height, 't_quotient%d'%c)
        model.Add(t[c] == 4*residue_bit+8*quotient)
    rhs = []
    for i, (a, b) in enumerate(LABELS):
        value = model.NewIntVar(0, N*height, 'required_neighbour_weight%d'%i)
        model.Add(8*value == 24*q[i]+2*w-t[a]-t[b])
        model.Add(value <= w-q[i])
        rhs.append(value)
    # The centre swap0<->1, outside mate flips, and permutations of the
    # five outside mate pairs preserve all the mathematical conditions.
    a, b = q[index[0, 2]], q[index[1, 2]]
    model.Add(a <= b)
    equal = model.NewBoolVar('overlap_equal')
    model.Add(a == b).OnlyEnforceIf(equal)
    model.Add(a < b).OnlyEnforceIf(equal.Not())
    model.Add(q[index[0, 3]] <= q[index[1, 3]]).OnlyEnforceIf(equal)
    base = height+1
    triple_code = {x:sum(base**c*q[index[c, x]] for c in (0, 1, 2))
                   for x in range(4, 14)}
    pair_code = {}
    for p in range(2, 7):
        model.Add(triple_code[2*p] <= triple_code[2*p+1])
        pair_code[p] = base**3*triple_code[2*p]+triple_code[2*p+1]
    for p in range(2, 6):
        model.Add(pair_code[p] <= pair_code[p+1])
    return q, w, d, t, rhs


def coefficient_probe(height, seconds, weight_limit=None, fixed_weight=None):
    model = cp_model.CpModel()
    q, w, d, t, rhs = coefficients(model, height, weight_limit, fixed_weight)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = seconds
    status = solver.Solve(model)
    report = dict(mode='coefficient_necessary_conditions_only', height=height,
                  weight_limit=weight_limit, fixed_weight=fixed_weight,
                  status=solver.StatusName(status), elapsed_seconds=solver.WallTime(),
                  branches=solver.NumBranches(), labels=LABELS,
                  graph_not_constructed=True)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        report.update(q=[solver.Value(v) for v in q], weight=solver.Value(w),
                      d=[solver.Value(v) for v in d],
                      t=[solver.Value(v) for v in t],
                      required_row_sums=[solver.Value(v) for v in rhs])
    return report


def first_impossible_row(q):
    """Exact, independent row domains using the three star counts only."""
    q = np.array(q, dtype=np.int64)
    required = (24*q-K8@q)//8
    assert not np.any((24*q-K8@q) % 8)
    star_rhs = (24*S-K8@S)//8
    overlap = [i for i, p in enumerate(LABELS) if len(set(p)&{0, 1, 2}) == 2]
    for i in range(N):
        domains = []
        for group in GROUPS:
            values = [int(q[j]) for j in group if j != i]
            domains.append([{0}, set(values), {a+b for a, b in combinations(values, 2)}])
        possible = set()
        for bits in product((0, 1), repeat=2):
            chosen = [j for j, bit in zip(overlap, bits) if bit]
            if i in chosen:
                continue
            needed = star_rhs[i].copy()
            for j in chosen:
                needed -= S[j]
            if any(k < 0 or k > 2 for k in needed):
                continue
            values = {int(sum(q[j] for j in chosen))}
            for c, k in enumerate(needed):
                values = {a+b for a in values for b in domains[c][int(k)]}
            possible.update(values)
        if int(required[i]) not in possible:
            return dict(row=i, label=LABELS[i], required=int(required[i]),
                        possible_neighbour_weights=sorted(possible))
    return None


def enumerate_coefficients(height, seconds, limit, weight_limit=None, fixed_weight=None):
    model = cp_model.CpModel()
    q, w, d, t, rhs = coefficients(model, height, weight_limit, fixed_weight)
    class Collector(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
            self.rows = []
        def on_solution_callback(self):
            vector = [self.Value(v) for v in q]
            self.rows.append(dict(q=vector, weight=self.Value(w),
                                  impossible_row=first_impossible_row(vector)))
            if len(self.rows) >= limit:
                self.StopSearch()
    callback = Collector()
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(model, callback)
    return dict(mode='normalized_coefficient_enumeration', height=height,
                weight_limit=weight_limit, fixed_weight=fixed_weight,
                status=solver.StatusName(status), complete=status in
                (cp_model.OPTIMAL, cp_model.INFEASIBLE),
                normalized_profiles=len(callback.rows), profiles=callback.rows,
                row_domain_survivors=sum(row['impossible_row'] is None for row in callback.rows),
                elapsed_seconds=solver.WallTime(), branches=solver.NumBranches(),
                labels=LABELS, graph_not_constructed=True,
                isomorphism_class_count_not_claimed=True)


def direct_profiles(weight, seconds):
    """Exhaust weighted multisets of outside mate-pair triples directly.

    Every nonnegative relation has max(q)<=weight/3. On each outside
    letter, its three coefficients determine its degree. Sort the two
    triples within each mate pair, and sort the five pairs. Residues
    restrict the permitted pair types before any four-overlap choices.
    """
    start = time.monotonic()
    height = weight//3
    base = height+1
    index = {p:i for i, p in enumerate(LABELS)}
    triples = sorted(product(range(base), repeat=3),
                     key=lambda a: a[0]+base*a[1]+base*base*a[2])
    overlaps = {}
    for a, b, c, d in product(range(base), repeat=4):
        if a > b or (a == b and c > d):
            continue
        overlaps.setdefault(a+b+c+d, []).append((a, b, c, d))
    rows, counts = [], []
    cache = {}
    leaves = 0
    def overlap_choices(total, residue):
        key = total, residue
        if key not in cache:
            u0, u1, u2 = total
            answer = []
            for a, b, c, d in overlaps.get(weight-sum(total), []):
                d0, d1, d2, d3 = a+c+u0, b+d+u1, a+b+u2, c+d
                if all(v % 8 == residue for v in
                       (3*d0+d1, 3*d1+d0, 3*d2+d3, 3*d3+d2)):
                    answer.append((a, b, c, d))
            cache[key] = answer
        return cache[key]
    def consume(chosen, residue):
        nonlocal leaves
        leaves += 1
        if leaves % 1000 == 0 and time.monotonic()-start >= seconds:
            raise TimeoutError
        chosen = sorted(chosen, key=lambda pair:pair[2])
        outside = [triple for pair in chosen for triple in pair[1]]
        if len({triple[2] for triple in outside}) == 1:
            return
        total = tuple(sum(a[c] for a in outside) for c in (0, 1, 2))
        for a, b, c, d in overlap_choices(total, residue):
            vector = [0]*N
            for p, value in (((0, 2), a), ((1, 2), b), ((0, 3), c), ((1, 3), d)):
                vector[index[p]] = value
            for x, triple in zip(range(4, 14), outside):
                for centre in (0, 1, 2):
                    vector[index[centre, x]] = triple[centre]
            if max(vector) < 2:
                continue
            if any(min(vector[i] for i, p in enumerate(LABELS) if centre in p) != 0
                   for centre in (0, 1, 2)):
                continue
            q = np.array(vector, dtype=np.int64)
            assert int(sum(q)) == weight
            rhs8 = 24*q-K8@q
            assert not np.any(rhs8 % 8)
            rhs = rhs8//8
            if np.any(rhs < 0) or np.any(rhs > weight-q):
                continue
            rows.append(dict(q=vector, weight=weight,
                             impossible_row=first_impossible_row(vector)))
    complete = True
    try:
        for residue in (0, 4):
            minimum = 0 if residue == 0 else 2
            types = []
            for i, first in enumerate(triples):
                first_degree = sum(first)
                first_code = first[0]+base*first[1]+base*base*first[2]
                for second in triples[i:]:
                    second_degree = sum(second)
                    cost = first_degree+second_degree
                    if cost > weight-4*minimum:
                        continue
                    if (3*first_degree+second_degree) % 8 != residue or \
                       (3*second_degree+first_degree) % 8 != residue:
                        continue
                    second_code = second[0]+base*second[1]+base*base*second[2]
                    types.append((cost, (first, second), base**3*first_code+second_code))
            types.sort(key=lambda pair:(pair[0], pair[2]))
            before = leaves
            def visit(first_index, left, remaining, chosen):
                if not left:
                    consume(chosen, residue)
                    return
                for i in range(first_index, len(types)):
                    pair = types[i]
                    if pair[0]*left > remaining:
                        break
                    visit(i, left-1, remaining-pair[0], chosen+[pair])
            visit(0, 5, weight, [])
            counts.append(dict(residue=residue, pair_types=len(types),
                               five_pair_multisets=leaves-before))
    except TimeoutError:
        complete = False
    return dict(mode='direct_five_pair_multiset_enumeration', weight=weight,
                height=height, complete=complete, normalized_profiles=len(rows),
                profiles=rows, row_domain_survivors=sum(r['impossible_row'] is None for r in rows),
                elapsed_seconds=time.monotonic()-start, five_pair_multisets=leaves,
                residue_counts=counts, labels=LABELS, graph_not_constructed=True,
                isomorphism_class_count_not_claimed=True)


def search(height, seconds, max_candidates, seed, weight_limit=None, fixed_weight=None,
           profiles_path=None, cuts_path=None):
    start = time.monotonic()
    report = dict(mode='new_graph_construction', height=height,
                  weight_limit=weight_limit, fixed_weight=fixed_weight,
                  labels=LABELS, iterations=[], cuts=[], no_peer_graph_input=True,
                  scope='All normalized nonnegative extra relations of this bounded height; no universal height bound asserted.')
    model = cp_model.CpModel()
    edges = {e:model.NewBoolVar('e%d_%d'%e) for e in EDGES}
    def edge(i, j):
        return edges[tuple(sorted((i, j)))]
    for row, lo, hi, _ in linear_constraints(connected_Q=True):
        expr = sum(a*edges[e] for e, a in row.items())
        if lo is not None:
            model.Add(expr >= lo)
        if hi is not None:
            model.Add(expr <= hi)
    for i, j in EDGES:
        wedges = []
        for k in range(N):
            if k in (i, j):
                continue
            value = model.NewBoolVar('w%d_%d_%d'%(i, j, k))
            model.Add(value >= edge(i, k)+edge(j, k)-1)
            wedges.append(value)
        model.Add(sum(wedges)+edge(i, j) <= 2-len(set(LABELS[i]).intersection(LABELS[j])))
    q, w, d, t, rhs = coefficients(model, height, weight_limit, fixed_weight)
    if profiles_path is not None:
        profile_data = json.loads(Path(profiles_path).read_text(encoding='utf-8-sig'))
        assert profile_data['complete'] and profile_data['source_enumeration_complete']
        remaining_profiles = [row['q'] for row in profile_data['records'] if
            row.get('certificate', {}).get('status') != 'EXACT_NONNEGATIVE_LINEAR_COMBINATION_CONTRADICTION']
        model.AddAllowedAssignments(q, remaining_profiles)
        report['exact_preprocessing'] = dict(source=str(profiles_path),
            remaining_profiles=len(remaining_profiles),
            discarded_only_with_exact_row_or_Farkas_certificates=True)
    for i in range(N):
        products = []
        for j in range(N):
            if i == j:
                continue
            value = model.NewIntVar(0, height, 'eq%d_%d'%(i, j))
            model.Add(value == q[j]).OnlyEnforceIf(edge(i, j))
            model.Add(value == 0).OnlyEnforceIf(edge(i, j).Not())
            products.append(value)
        model.Add(sum(products) == rhs[i])
    signatures = set()
    if cuts_path is not None:
        prior = json.loads(Path(cuts_path).read_text(encoding='utf-8-sig'))
        for cut in prior['cuts']:
            name = cut['matrix']
            v = np.array(cut['vector'], dtype=np.int64)
            assert name in ('T', 'U') and len(v) == N
            signatures.add((name, tuple(map(int, v))))
            expr = sum(int(v[i]*v[j])*edges[i, j] for i, j in EDGES if v[i]*v[j])
            if name == 'T':
                model.Add(16*expr <= int(24*(v@v)-v@K8@v))
            else:
                model.Add(30*expr >= int(-v@U0@v))
            report['cuts'].append(dict(matrix=name, vector=list(map(int, v)), source=str(cuts_path)))
    for iteration in range(max_candidates):
        remaining = seconds-(time.monotonic()-start)
        if remaining <= 0:
            report['status'] = 'TIME_LIMIT_NO_EXCLUSION'
            break
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = remaining
        solver.parameters.random_seed = seed
        status = solver.Solve(model)
        record = dict(iteration=iteration, status=solver.StatusName(status),
                      solver_seconds=solver.WallTime(), branches=solver.NumBranches())
        report['iterations'].append(record)
        if status == cp_model.INFEASIBLE:
            report['status'] = 'BOUNDED_HEIGHT_FAMILY_UNSAT_BY_CP_SAT'
            break
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            report['status'] = 'TIME_LIMIT_NO_EXCLUSION'
            break
        gamma = np.zeros((N, N), dtype=np.int64)
        for i, j in EDGES:
            gamma[i, j] = gamma[j, i] = solver.Value(edges[i, j])
        q_value = np.array([solver.Value(x) for x in q], dtype=np.int64)
        M = 24*np.eye(N, dtype=np.int64)-8*gamma-K8
        U = U0+15*gamma
        assert not np.any(M@np.column_stack((S, q_value)))
        masks = boundary_masks(gamma.tolist())
        assert all((masks[i]&masks[j]).bit_count() <= 2-((masks[i]>>j)&1)
                   for i, j in combinations(range(49), 2))
        record['q'] = q_value.tolist()
        record['weight'] = int(sum(q_value))
        report['last_gamma'] = gamma.tolist()
        report['last_kernel'] = q_value.tolist()
        new_cuts = 0
        for name, matrix in (('T', M), ('U', U)):
            minimum, witnesses = spectral_witnesses(matrix)
            record[name+'_minimum_eigenvalue_approx'] = minimum
            if not witnesses:
                exact = psd_or_witness(sp.Matrix(matrix.tolist()))
                if not exact['psd']:
                    witnesses = [(np.array(exact['integer_witness'], dtype=object),
                                  exact['quadratic_value'])]
            for v, energy in witnesses:
                signature = (name, tuple(map(int, v)))
                if signature in signatures:
                    continue
                signatures.add(signature)
                assert int(v@matrix@v) == energy < 0
                expr = sum(int(v[i]*v[j])*edges[i, j] for i, j in EDGES if v[i]*v[j])
                if name == 'T':
                    model.Add(16*expr <= int(24*(v@v)-v@K8@v))
                else:
                    model.Add(30*expr >= int(-v@U0@v))
                report['cuts'].append(dict(matrix=name, vector=list(map(int, v)),
                                          negative_value=energy, candidate=iteration))
                new_cuts += 1
        record['new_exact_cuts'] = new_cuts
        print(json.dumps({k:v for k, v in record.items() if k != 'q'}), flush=True)
        if not new_cuts:
            rank = int(sp.Matrix(M.tolist()).rank())
            report.update(status='NEW_CONNECTED_Q_LOCAL_T_AND_U_PSD_BOUNDARY', rank=rank,
                          counterexample_to_A=True, exact_PSD=True)
            assert rank <= 30
            break
    else:
        report['status'] = 'CANDIDATE_LIMIT_NO_EXCLUSION'
    report['elapsed_seconds'] = time.monotonic()-start
    report['local_candidates'] = sum('q' in record for record in report['iterations'])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--height', type=int, default=2)
    parser.add_argument('--seconds', type=float, default=40)
    parser.add_argument('--weight-limit', type=int)
    parser.add_argument('--fixed-weight', type=int)
    parser.add_argument('--max-candidates', type=int, default=100)
    parser.add_argument('--seed', type=int, default=37)
    parser.add_argument('--coefficients-only', action='store_true')
    parser.add_argument('--enumerate-coefficients', action='store_true')
    parser.add_argument('--direct-profiles', action='store_true')
    parser.add_argument('--profile-limit', type=int, default=10000)
    parser.add_argument('--profiles-file')
    parser.add_argument('--cuts-file')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.direct_profiles:
        if args.fixed_weight is None:
            parser.error('--direct-profiles requires --fixed-weight')
        report = direct_profiles(args.fixed_weight, args.seconds)
    elif args.enumerate_coefficients:
        report = enumerate_coefficients(args.height, args.seconds, args.profile_limit,
                                        args.weight_limit, args.fixed_weight)
    elif args.coefficients_only:
        report = coefficient_probe(args.height, args.seconds, args.weight_limit, args.fixed_weight)
    else:
        report = search(args.height, args.seconds, args.max_candidates, args.seed,
                        args.weight_limit, args.fixed_weight, args.profiles_file, args.cuts_file)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k, v in report.items() if k in
                      ('mode', 'status', 'elapsed_seconds', 'local_candidates', 'weight', 'q', 'd', 't',
                       'complete', 'normalized_profiles', 'row_domain_survivors')}))


if __name__ == '__main__':
    main()
