"""PSD trivial-quotient reduction for G1, c_left=c_right=5.

The non-grid-overlap case has one quotient up to exterior-pair relabelling.
The optional bounded CP-SAT search tests its binary local lifts, not the
producer's samples and not global Conway existence.
"""
import argparse
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_g1_sectors import action, character_bases
from four_star_profile_join import LABELS, upper_entry, boundary, residual
from three_star_ambient_upper import psd_or_witness
from three_star_column_domains import k8

GROUP = tuple(product((0, 1), repeat=2))
INDEX = {p:i for i, p in enumerate(LABELS)}
ROOTS = [(0, 2)]+[(0, 4+2*i) for i in range(5)]+[(2, 4+2*i) for i in range(5)]
ORBITS = [[INDEX[action(p, a, b)] for a, b in GROUP] for p in ROOTS]


def correction(i, j):
    """The trivial block of 3I-K, in orbit-indicator bases /2."""
    if i == j:
        return 2
    if 1 <= i <= 5 and 6 <= j <= 10:
        return int(i-1 != j-6)
    if 1 <= j <= 5 and 6 <= i <= 10:
        return int(j-1 != i-6)
    return 0


def canonical_quotient():
    # Positive overlap forces t=1 and distinct active exterior pairs.
    # Normalize the left active pair to0 and the right active pair to1.
    w = [0]*11
    w[0], w[1], w[7] = 1, -1, -1
    H = [[x*y for y in w] for x in w]
    D = [[correction(i, j)-H[i][j] for j in range(11)] for i in range(11)]
    return H, D


def character_diagnosis(labels, edges):
    """New sector information for an explicitly supplied boundary."""
    old = {tuple(p):i for i, p in enumerate(labels)}
    source = [[0]*44 for _ in range(44)]
    for i, j in edges:
        source[i][j] = source[j][i] = 1
    gamma = [[source[old[p]][old[q]] for q in LABELS] for p in LABELS]
    M = sp.Matrix(44, 44, lambda i,j: 24*int(i==j)-8*gamma[i][j]-k8(LABELS[i],LABELS[j]))
    N = sp.Matrix(44, 44, lambda i,j: upper_entry(LABELS[i],LABELS[j],gamma[i][j],i==j))
    _, bases = character_bases()
    out = {}
    for chi in ('00','10','01','11'):
        B = sp.Matrix(bases[chi])
        tblock = B.T*M*B/4
        ublock = B.T*N*B/4
        out[chi] = dict(T_nullity=11-tblock.rank(),
                        T_positivity=psd_or_witness(tblock),
                        U_positivity=psd_or_witness(ublock))
    return dict(character_order=['00','10','01','11'], sectors=out,
                scope='Character information on this local boundary. No global graph or full-completion assertion.')


def check_own_local_lift(labels, edges):
    old = {tuple(p):i for i,p in enumerate(labels)}
    source = [[0]*44 for _ in range(44)]
    for i,j in edges:
        source[i][j] = source[j][i] = 1
    gamma = [[source[old[p]][old[q]] for q in LABELS] for p in LABELS]
    R = residual(boundary(gamma, LABELS))
    assert min(x for row in R for x in row) >= 0
    assert all(x == 0 for row in R[:5] for x in row)
    _, D = canonical_quotient()
    assert all(sum(gamma[u][v] for v in oj) == D[i][j]
               for i,oi in enumerate(ORBITS) for u in oi for j,oj in enumerate(ORBITS))
    return dict(status='PASS_OWN_LIFT', boundary_vertices=59,
                all_common_neighbour_capacities_nonnegative=True,
                root_and_four_complete_star_residual_rows_zero=True,
                forced_orbit_quotient_satisfied=True)


def reduction_report():
    assert sorted(i for orbit in ORBITS for i in orbit) == list(range(44))
    for i, oi in enumerate(ORBITS):
        for j, oj in enumerate(ORBITS):
            entry = 3*int(i == j)-sp.Rational(sum(k8(LABELS[u], LABELS[v]) for u in oi for v in oj), 32)
            assert entry == correction(i, j)
    t, e = sp.symbols('t e')
    core = sp.Matrix([[t, -t, -t], [-t, t, e], [-t, e, t]])
    assert sp.expand(core.det()+t*(e-t)**2) == 0
    possibilities = []
    for left, right, weight, degree in product(range(5), range(5), (1, 2), range(5)):
        cross = int(left != right)-degree
        if cross == weight:
            possibilities.append([left, right, weight, degree])
    assert len(possibilities) == 20
    assert all(left != right and weight == 1 and degree == 0
               for left, right, weight, degree in possibilities)
    H, D = canonical_quotient()
    assert all(x >= 0 for row in D for x in row)
    for row in range(11):
        assert H[row][0]+sum(H[row][j] for j in range(1, 6)) == 0
        assert H[row][0]+sum(H[row][j] for j in range(6, 11)) == 0
    return dict(status='EXACT_C55_NON_GRID_TRIVIAL_QUOTIENT_REDUCTION',
                labels=LABELS, orbit_roots=ROOTS, orbits=ORBITS,
                trivial_block=H, orbit_adjacency_degrees=D,
                labelled_active_pair_choices=20, quotient_types_up_to_exterior_relabelling=1,
                trivial_rank=1, trivial_nullity=10, nontrivial_nullity_required_for_rank30=4,
                proof=[
                    'Write H=B_00^t T B_00/4 and D_ij as the adjacency degree from one vertex of orbit i to orbit j. H_ii=2-D_ii. Its off-diagonal entries are -D_ij on each mate line and involving the overlap, and 1-[i=j]-D_LiRj between exterior left/right orbits.',
                    'Each two-star quotient is a graph Laplacian on six orbits. Five components mean one component of size2 and four singleton components. Positive overlap means its component contains exactly one exterior orbit. Both sides have the same edge weight t=2-D_00 in {1,2}.',
                    'All other diagonal entries of H vanish. PSD forces their entire rows to vanish. The remaining core is [[t,-t,-t],[-t,t,e],[-t,e,t]], of determinant -t(e-t)^2. Hence e=t.',
                    'But e=1-[left=right]-D_left,right <=1. Therefore t=1, left!=right, and D_left,right=0. All other quotient entries are forced. The20 ordered distinct active pairs are equivalent under permutation of the five exterior pairs.'
                ],
                scope='Requires local G1 invariance, both two-star component counts5, and non-grid overlap (D_00<2). It does not exclude the grid-overlap case or general four-star boundaries.',
                validation='Own orbit correction identity and core determinant checked exactly. No peer sample audited.')


def local_lifts(seconds, workers, psd_rounds=1, upper_table=None):
    """Complete finite model; a timeout leaves the lift family unresolved."""
    started = time.monotonic()
    _, D = canonical_quotient()
    model = cp_model.CpModel()
    gamma = [[0]*44 for _ in range(44)]
    choices = []
    for i, oi in enumerate(ORBITS):
        for j in range(i, 11):
            degree = D[i][j]
            if not degree:
                continue
            oj = ORBITS[j]
            offsets = (1, 2, 3) if i == j else (0, 1, 2, 3)
            options = list(combinations(offsets, degree))
            selected = [model.NewBoolVar('o_%d_%d_%d'%(i,j,k)) for k in range(len(options))]
            model.AddExactlyOne(selected)
            choices.append(dict(orbits=[i,j], options=options, selected=selected))
            for a, u in enumerate(oi):
                for b, v in enumerate(oj):
                    if u == v or (i == j and a > b):
                        continue
                    support = [selected[k] for k, option in enumerate(options) if a^b in option]
                    if not support:
                        continue
                    edge = model.NewBoolVar('e_%d_%d'%(min(u,v), max(u,v)))
                    model.Add(edge == sum(support))
                    gamma[u][v] = gamma[v][u] = edge
    upper_table_info = None
    if upper_table is not None:
        from four_star_g1_c55_upper import add_upper_tables
        upper_table_info = add_upper_tables(model, choices, upper_table)
    def variable(x):
        return not isinstance(x, int)
    # Exact star rows for the four complete stars, and capacity rows for
    # each of the other ten root neighbours in this induced boundary.
    for i, p in enumerate(LABELS):
        for c in range(14):
            row = [gamma[i][j] for j, q in enumerate(LABELS) if c in q and variable(gamma[i][j])]
            bound = 2-int(c in p)-int((c^1) in p)
            if c < 4:
                model.Add(sum(row) == bound)
            else:
                model.Add(sum(row) <= bound)
    products = 0
    for i, j in combinations(range(44), 2):
        common = []
        for k in range(44):
            a, b = gamma[i][k], gamma[j][k]
            if not variable(a) or not variable(b):
                continue
            both = model.NewBoolVar('p_%d_%d_%d'%(i,j,k))
            model.AddMultiplicationEquality(both, [a, b])
            common.append(both)
            products += 1
        bound = 2-len(set(LABELS[i]) & set(LABELS[j]))
        model.Add(sum(common)+gamma[i][j] <= bound)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = 756
    rounds, cuts = [], []
    all_psd = False
    _, raw_bases = character_bases()
    for iteration in range(psd_rounds):
        remaining = seconds-(time.monotonic()-started)
        if remaining <= 0:
            result = cp_model.UNKNOWN
            break
        solver.parameters.max_time_in_seconds = remaining
        result = solver.Solve(model)
        if result not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break
        edges = [[i,j] for i,j in combinations(range(44),2)
                 if variable(gamma[i][j]) and solver.Value(gamma[i][j])]
        if psd_rounds == 1:
            break
        diagnosis = character_diagnosis(LABELS, edges)
        failures = []
        for chi, sector in diagnosis['sectors'].items():
            for form in ('T','U'):
                answer = sector[form+'_positivity']
                if answer['psd']:
                    continue
                vector = sp.Matrix(raw_bases[chi])*sp.Matrix(answer['integer_witness'])
                v = list(map(int, vector))
                if form == 'T':
                    constant = 24*sum(x*x for x in v)-sum(v[i]*v[j]*k8(LABELS[i],LABELS[j]) for i in range(44) for j in range(44))
                    factor = -16
                else:
                    constant = sum(v[i]*v[j]*upper_entry(LABELS[i],LABELS[j],0,i==j) for i in range(44) for j in range(44))
                    factor = 30
                source_value = constant+factor*sum(v[i]*v[j] for i,j in edges)
                assert source_value == 4*answer['quadratic_value'] and source_value < 0
                expression = sum(factor*v[i]*v[j]*gamma[i][j] for i,j in combinations(range(44),2)
                                 if v[i] and v[j] and variable(gamma[i][j]))
                model.Add(constant+expression >= 0)
                cuts.append(dict(form=form, character=chi, vector=v, constant=constant,
                                 edge_factor=factor, source_quadratic_value=source_value))
                failures.append(form+chi)
        rounds.append(dict(iteration=iteration, failed_sectors=failures,
                           T_nullities={chi:r['T_nullity'] for chi,r in diagnosis['sectors'].items()}))
        print(json.dumps(dict(iteration=iteration, failed_sectors=failures, cuts=len(cuts))), flush=True)
        if not failures:
            all_psd = True
            break
    else:
        result = cp_model.UNKNOWN
    status = solver.StatusName(result)
    record = dict(status=status, seconds=time.monotonic()-started,
                  solve_wall_seconds=solver.WallTime(), branches=solver.NumBranches(),
                  conflicts=solver.NumConflicts(), orbit_choice_groups=len(choices),
                  product_variables=products, psd_cut_rounds=rounds, exact_psd_cuts=cuts,
                  exact_upper_character_tables=upper_table_info,
                  full_T_U_psd_certified=all_psd,
                  meaning=('No binary locally admissible lift satisfies the necessary exact PSD cuts; excludes the stated G1 c55 non-grid-overlap family.'
                           if result == cp_model.INFEASIBLE else
                           ('Local lift with T/U PSD certified by exact character congruences; total T nullity must still be read separately.' if all_psd else
                            'Local lift found; full T/U positivity and rank have NOT been imposed.')
                           if result in (cp_model.OPTIMAL, cp_model.FEASIBLE) else
                           'Bounded search unresolved; no family excluded.'))
    if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        record['labels'] = LABELS
        record['edges'] = [[i,j] for i,j in combinations(range(44),2)
                           if variable(gamma[i][j]) and solver.Value(gamma[i][j])]
        record['orbit_choices'] = [dict(orbits=row['orbits'], offsets=next(option for option,var in zip(row['options'],row['selected']) if solver.Value(var))) for row in choices]
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--seconds', type=float, default=0)
    parser.add_argument('--workers', type=int, default=1)
    parser.add_argument('--psd-rounds', type=int, default=1)
    parser.add_argument('--upper-table', help='Exact catalogue from four_star_g1_c55_upper.py')
    args = parser.parse_args()
    report = reduction_report()
    if args.seconds > 0:
        upper_table = json.loads(Path(args.upper_table).read_text(encoding='utf-8')) if args.upper_table else None
        report['local_lifts'] = local_lifts(args.seconds, args.workers, args.psd_rounds, upper_table)
        if 'edges' in report['local_lifts']:
            report['own_local_lift_check'] = check_own_local_lift(
                report['local_lifts']['labels'], report['local_lifts']['edges'])
            report['own_local_lift_sectors'] = character_diagnosis(
                report['local_lifts']['labels'], report['local_lifts']['edges'])
            if upper_table is not None:
                assert all(report['own_local_lift_sectors']['sectors'][chi]['U_positivity']['psd'] for chi in ('10','01'))
                if 'joint_allowed_states' in upper_table:
                    assert all(report['own_local_lift_sectors']['sectors'][chi]['T_positivity']['psd']
                               and report['own_local_lift_sectors']['sectors'][chi]['T_nullity']==1 for chi in ('10','01'))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=report['status'], quotient_types=1,
                         local_lifts={k:v for k,v in report.get('local_lifts',{}).items() if k not in ('labels','edges','orbit_choices','exact_psd_cuts','psd_cut_rounds')})))
