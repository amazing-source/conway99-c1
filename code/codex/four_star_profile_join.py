"""Join ten certified column domains into a fourth Conway star.

This consumes the producer's rank30/PSD seed and complete column domains.
It does not re-audit that seed. New edges are forced by exact Gram products;
only the new 44-label extension is tested for complementary positivity.
A finite rejection concerns this seed, never all three-star boundaries.
"""
import argparse
from collections import Counter, defaultdict
from itertools import combinations
from math import lcm
from pathlib import Path
import json
import sys
import time

import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_column_domains import S, INDEX, bits, k8
from three_star_ambient_upper import psd_or_witness


NEW = tuple((3, x) for x in range(4, 14))
LABELS = S + NEW
A, B = INDEX[(0, 3)], INDEX[(1, 3)]


def read_seed(path):
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    labels = tuple(tuple(sorted(p)) for p in data['labels'])
    if len(labels) != 34 or set(labels) != set(S):
        raise ValueError('The seed must contain the 34 labels meeting {0,1,2}.')
    structure = data['structures'][0] if 'structures' in data else data
    gamma = structure.get('gamma', structure.get('adjacency'))
    if gamma is None:
        gamma = [[0]*34 for _ in range(34)]
        for i, j in structure['edges']:
            gamma[i][j] = gamma[j][i] = 1
    old = {p: i for i, p in enumerate(labels)}
    return [[int(gamma[old[p]][old[q]]) for q in S] for p in S]


def boundary(gamma, labels):
    n = 15+len(labels)
    out = [[0]*n for _ in range(n)]
    for c in range(14):
        out[0][1+c] = out[1+c][0] = 1
        out[1+c][1+(c ^ 1)] = 1
    for i, p in enumerate(labels):
        for c in p:
            out[15+i][1+c] = out[1+c][15+i] = 1
        out[15+i][15:] = gamma[i][:]
    return out


def residual(matrix):
    masks = [sum(v << j for j, v in enumerate(row)) for row in matrix]
    return [[12*int(i == j)+2-matrix[i][j]-(masks[i] & masks[j]).bit_count()
             for j in range(len(matrix))] for i in range(len(matrix))]


def fourth_star_targets(gamma):
    return [2-int(3 in p)-int(2 in p)-gamma[i][A]-gamma[i][B]
            for i, p in enumerate(S)]


def upper_entry(p, q, edge, diagonal=False):
    return 60*int(diagonal)+15*edge-4*len(set(p) & set(q))+sum((c ^ 1) in q for c in p)-2


def upper_inverse_from_certification(gamma):
    """Consume rank(U_S)=31 and PSD, computing only the extension inverse."""
    stars = sp.Matrix([[int(c in p) for p in S] for c in (0, 1, 2)])
    anchors = stars.rref()[1]
    basis = [i for i in range(34) if i not in anchors]
    principal = sp.Matrix(31, 31, lambda i, j:
        upper_entry(S[basis[i]], S[basis[j]], gamma[basis[i]][basis[j]], i == j))
    inverse = principal.inv(method='DM')
    scale = lcm(*(int(x.q) for x in inverse))
    return basis, [[int(x*scale) for x in inverse.row(i)] for i in range(31)], scale


def forced_edge(left, right, scale, correction):
    """left=m_u[I], right=(scale*M_II^-1)m_v[I]."""
    value = -scale*correction-sum(x*y for x, y in zip(left, right))
    return 0 if value == 0 else 1 if value == 8*scale else None


def prepare_profiles(gamma, data, producer_upper_rank31=False):
    if data.get('spectral_rank') != 30:
        raise ValueError('Supply a producer-certified rank30 domain bundle.')
    if tuple(map(tuple, data.get('input_labels', S))) != S:
        raise ValueError('Domain masks/basis must use the standard S order.')
    basis = data['spectral_basis']
    inverse = data['inverse_numerator']
    scale = data['inverse_denominator']
    if len(basis) != 30 or len(set(basis)) != 30 or scale <= 0:
        raise ValueError('Invalid principal-basis contract.')
    old_boundary = boundary(gamma, S)
    old_masks = [sum(v << j for j, v in enumerate(row)) for row in old_boundary]
    by_label = {tuple(c['label']): c for c in data['columns']}
    upper_data = upper_inverse_from_certification(gamma) if producer_upper_rank31 else None
    domains = []
    upper_rejections = []
    for label in NEW:
        source = by_label.get(label)
        if source is None or not source.get('complete') or 'profiles' not in source:
            raise ValueError('All ten complete (3,x) domains, with profile masks, are required.')
        column = []
        removed = 0
        for h in sorted(set(map(int, source['profiles']))):
            if h < 0 or h >> 34:
                raise ValueError('Profile masks must contain 34 bits.')
            d = (h << 15) | sum(1 << (1+c) for c in label)
            m = [-8*((h >> i) & 1)-k8(S[i], label) for i in basis]
            hm = [sum(x*y for x, y in zip(row, m)) for row in inverse]
            # A domain is trusted as complete, but incomplete-norm profiles
            # cannot be fed into the rank-preserving pair formula.
            if sum(x*y for x, y in zip(m, hm)) != 20*scale:
                raise ValueError('A supplied profile fails its declared exact norm contract.')
            slack = [2-((d >> r) & 1)-(old_masks[r] & d).bit_count() for r in range(49)]
            if any(v < 0 for v in slack):
                raise ValueError('A supplied profile exceeds a declared individual C2 cap.')
            profile = dict(h=h, d=d, m=m, hm=hm, slack=slack)
            if upper_data is not None:
                ubasis, uinverse, uscale = upper_data
                f = [upper_entry(S[i], label, (h >> i) & 1) for i in ubasis]
                hf = [sum(x*y for x, y in zip(row, f)) for row in uinverse]
                diagonal = 50*uscale-sum(x*y for x, y in zip(f, hf))
                if diagonal < 0:
                    removed += 1
                    continue
                profile.update(f=f, hf=hf, udiagonal=diagonal, uscale=uscale)
            column.append(profile)
        domains.append(column)
        upper_rejections.append(removed)
    return domains, scale, residual(old_boundary), upper_rejections


def pair_option(left, right, label_left, label_right, scale):
    edge = forced_edge(left['m'], right['hm'], scale, k8(label_left, label_right))
    if edge is None:
        return None, 'nonbinary_Gram_entry'
    if (left['d'] & right['d']).bit_count() > 2-edge:
        return None, 'new_pair_common_neighbours'
    if edge:
        # A vertex in L3 has at most one neighbour among the ten new
        # vertices. These are the complete additional old/new C2 terms.
        if any(left['slack'][r] == 0 for r in bits(right['d'])):
            return None, 'left_old_new_common_neighbours'
        if any(right['slack'][r] == 0 for r in bits(left['d'])):
            return None, 'right_old_new_common_neighbours'
    if 'udiagonal' in left:
        off = upper_entry(label_left, label_right, edge)*left['uscale']
        off -= sum(x*y for x, y in zip(left['f'], right['hf']))
        if off*off > left['udiagonal']*right['udiagonal']:
            return None, 'complementary_Gram_Schur_minor'
    return edge, None


def compatibility_tables(domains, scale, deadline, pair_limit):
    tables, rejected = {}, Counter()
    expected = sum(len(domains[u])*len(domains[v]) for u, v in combinations(range(10), 2))
    if expected > pair_limit:
        return None, dict(status='PAIR_LIMIT_NO_EXCLUSION', pair_count=expected, pair_limit=pair_limit)
    tested = 0
    for u, v in combinations(range(10), 2):
        allowed = []
        for a, left in enumerate(domains[u]):
            for b, right in enumerate(domains[v]):
                tested += 1
                if tested % 1024 == 0 and time.monotonic() >= deadline:
                    return None, dict(status='TIME_LIMIT_NO_EXCLUSION', tested_pairs=tested)
                edge, reason = pair_option(left, right, NEW[u], NEW[v], scale)
                if reason:
                    rejected[reason] += 1
                else:
                    allowed.append((a, b, edge))
        tables[u, v] = allowed
        if not allowed:
            return None, dict(status='NO_FOURTH_STAR_EXTENSION', empty_pair=[NEW[u], NEW[v]],
                              tested_pairs=tested, rejection_counts=dict(rejected))
    return tables, dict(tested_pairs=tested, rejection_counts=dict(rejected),
                        compatible_pairs=sum(map(len, tables.values())))


def upper15(gamma):
    return sp.Matrix(44, 44, lambda i, j:
        upper_entry(LABELS[i], LABELS[j], gamma[i][j], i == j))


def upper_schur(gamma, profiles):
    """Integer multiple of the new 10x10 Schur complement; old PSD is trusted."""
    scale = profiles[0]['uscale']
    schur = sp.Matrix(10, 10, lambda i, j:
        upper_entry(NEW[i], NEW[j], gamma[34+i][34+j], i == j)*scale
        -sum(x*y for x, y in zip(profiles[i]['f'], profiles[j]['hf'])))
    # The completed fourth star forces this relation. Check our assembly.
    assert schur*sp.ones(10, 1) == sp.zeros(10, 1)
    result = psd_or_witness(schur[:9, :9])
    result.update(schur_dimension=10, tested_principal_dimension=9,
                  forced_relation=[1]*10, denominator=scale)
    return result


def build_model(gamma, domains, tables, capacities, connected_second_line):
    model = cp_model.CpModel()
    choices, selectors = [], []
    for u, domain in enumerate(domains):
        row = [model.NewBoolVar('choose_%d_%d' % (u, a)) for a in range(len(domain))]
        model.AddExactlyOne(row)
        selector = model.NewIntVar(0, len(row)-1, 'profile_%d' % u)
        model.Add(selector == sum(a*x for a, x in enumerate(row)))
        choices.append(row)
        selectors.append(selector)
    new_edges = {}
    for (u, v), rows in tables.items():
        e = model.NewBoolVar('edge_%d_%d' % (u, v))
        model.AddAllowedAssignments([selectors[u], selectors[v], e], rows)
        new_edges[u, v] = e
    cross = [[sum(choices[u][a] for a, p in enumerate(domains[u]) if (p['h'] >> i) & 1)
              for u in range(10)] for i in range(34)]
    for i, target in enumerate(fourth_star_targets(gamma)):
        model.Add(sum(cross[i]) == target)
    for u in range(10):
        model.Add(cross[A][u]+cross[B][u] +
                  sum(e for (v, w), e in new_edges.items() if u in (v, w)) == 1)
    # Entire old boundary: degree budgets on the diagonal, C2 elsewhere.
    consumed = defaultdict(list)
    for u, domain in enumerate(domains):
        for a, p in enumerate(domain):
            active = tuple(bits(p['d']))
            for r in active:
                consumed[r, r].append(choices[u][a])
            for r, s in combinations(active, 2):
                consumed[r, s].append(choices[u][a])
    for (r, s), terms in consumed.items():
        model.Add(sum(terms) <= capacities[r][s])
    def edge_expr(i, j):
        if i > j:
            i, j = j, i
        if j < 34:
            return gamma[i][j]
        if i < 34:
            return cross[i][j-34]
        return new_edges[i-34, j-34]
    if connected_second_line:
        # Contract the six outside mate pairs in L2 union L3. The 31
        # complementary cut representatives characterize connected Q.
        outer_pairs = (0, 2, 3, 4, 5, 6)
        two = [i for i, p in enumerate(LABELS) if set(p) & {2, 3}]
        pair_of = {i: next(c//2 for c in LABELS[i] if c not in (2, 3)) for i in two}
        for mask in range(1, 63, 2):
            part = {outer_pairs[j] for j in range(6) if (mask >> j) & 1}
            model.Add(sum(edge_expr(i, j) for i, j in combinations(two, 2)
                          if (pair_of[i] in part) != (pair_of[j] in part)) >= 1)
    return model, choices, selectors, new_edges, edge_expr


def join(gamma, data, seconds, pair_limit, candidate_limit, connected_second_line,
         producer_upper_rank31=False):
    start = time.monotonic()
    report = dict(status='TIME_LIMIT_NO_EXCLUSION', seed_properties_source='producer certification',
                  seed_reaudited=False, full_srg_constructed=False,
                  connected_second_line_required=connected_second_line, iterations=[],
                  producer_upper_rank31=producer_upper_rank31,
                  exclusion_scope='Only extensions of the input seed satisfying the requested second-line type.')
    domains, scale, capacities, removed = prepare_profiles(gamma, data, producer_upper_rank31)
    report['domain_sizes'] = [len(row) for row in domains]
    report['negative_upper_Schur_diagonal_rejections'] = removed
    if any(not row for row in domains):
        report.update(status='NO_FOURTH_STAR_EXTENSION', reason='A complete domain is empty after exact necessary filters.')
        report['seconds'] = time.monotonic()-start
        return report
    tables, statistics = compatibility_tables(domains, scale, start+seconds, pair_limit)
    report['compatibility'] = statistics
    if tables is None:
        report['status'] = statistics['status']
        report['seconds'] = time.monotonic()-start
        return report
    model, choices, selectors, new_edges, edge_expr = build_model(
        gamma, domains, tables, capacities, connected_second_line)
    for iteration in range(candidate_limit):
        remaining = start+seconds-time.monotonic()
        if remaining <= 0:
            break
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = remaining
        status = solver.Solve(model)
        record = dict(status=solver.StatusName(status), solver_seconds=solver.WallTime(),
                      branches=solver.NumBranches())
        report['iterations'].append(record)
        if status == cp_model.INFEASIBLE:
            report.update(status='NO_FOURTH_STAR_EXTENSION', proof_kind='finite CP-SAT UNSAT; no portable proof trace')
            break
        if status == cp_model.MODEL_INVALID:
            report.update(status='MODEL_INVALID_NO_EXCLUSION', reason=solver.ResponseStats())
            break
        if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            break
        selection = [solver.Value(v) for v in selectors]
        extension = [row[:] + [0]*10 for row in gamma]+[[0]*44 for _ in range(10)]
        for u, a in enumerate(selection):
            for i in bits(domains[u][a]['h']):
                extension[i][34+u] = extension[34+u][i] = 1
        for (u, v), e in new_edges.items():
            extension[34+u][34+v] = extension[34+v][34+u] = solver.Value(e)
        # These are checks of our newly assembled object, not of the seed.
        R = residual(boundary(extension, LABELS))
        assert all(x >= 0 for row in R for x in row), 'Joint C2 encoding mismatch.'
        assert all(not x for r in range(5) for x in R[r]), 'A completed neighbourhood is inconsistent.'
        selected_profiles = [domains[u][a] for u, a in enumerate(selection)]
        if producer_upper_rank31:
            record['upper_Schur'] = upper_schur(extension, selected_profiles)
        certificate = (dict(psd=True, method='producer PSD block and exact 9x9 Schur quotient')
                       if producer_upper_rank31 and record['upper_Schur']['psd']
                       else psd_or_witness(upper15(extension)))
        record['upper_Gram'] = certificate
        if certificate['psd']:
            report.update(status='FOUR_STAR_RANK30_PSD_EXTENSION', labels=LABELS, gamma=extension,
                          selected_profiles=[domains[u][a]['h'] for u, a in enumerate(selection)],
                          scope='One local 44-label boundary; no full Conway graph or automorphism conclusion.')
            break
        q = certificate['integer_witness']
        constant = sum(q[i]*q[j]*(60*int(i == j)-4*len(set(LABELS[i]) & set(LABELS[j]))
                       +sum((c ^ 1) in LABELS[j] for c in LABELS[i])-2)
                       for i in range(44) for j in range(44))
        coefficients = [(i, j, 30*q[i]*q[j]) for i, j in combinations(range(44), 2) if q[i] and q[j]]
        if abs(constant)+sum(abs(c) for i, j, c in coefficients) >= 2**60:
            # A rational witness may be very large. Avoid int64 overflow in
            # CP-SAT while retaining a valid exact exclusion of this tuple.
            model.AddForbiddenAssignments(selectors, [selection])
            record['cut_kind'] = 'exact_rejected_tuple; PSD witness too large for int64'
        else:
            model.Add(constant+sum(c*edge_expr(i, j) for i, j, c in coefficients) >= 0)
            record['cut_kind'] = 'integer complementary PSD inequality'
    else:
        report['status'] = 'CANDIDATE_LIMIT_NO_EXCLUSION'
    report['seconds'] = time.monotonic()-start
    return report


def self_test():
    # Exact edge recovery can reject a rational near-edge without tolerances.
    assert forced_edge([1], [-2], 1, 2) == 0
    assert forced_edge([1], [-10], 1, 2) == 1
    assert forced_edge([1], [-9], 1, 2) is None
    # Pair compatibility catches capacity consumed only when the two new
    # vertices are joined. Individually each profile has nonnegative slack.
    left = dict(m=[1], d=1 << 4, slack=[1]*49)
    right = dict(hm=[-10], d=1 << 7, slack=[1]*49)
    assert pair_option(left, right, (3, 4), (3, 5), 1) == (1, None)
    left['slack'][7] = 0
    assert pair_option(left, right, (3, 4), (3, 5), 1)[1] == 'left_old_new_common_neighbours'
    # The same forced non-edge does not consume that old/new capacity.
    right['hm'] = [-2]
    assert pair_option(left, right, (3, 4), (3, 5), 1) == (0, None)
    # Positive diagonal Schur entries do not guarantee a positive 2x2 minor.
    left.update(f=[0], udiagonal=1, uscale=1)
    right.update(hf=[0], udiagonal=1)
    assert pair_option(left, right, (3, 4), (3, 5), 1)[1] == 'complementary_Gram_Schur_minor'
    assert len(LABELS) == 44 and len(set(LABELS)) == 44
    return dict(status='PASS', scope='Own exact Gram and joint-capacity primitives only; no peer audit.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed')
    parser.add_argument('--domains')
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--pair-limit', type=int, default=2000000)
    parser.add_argument('--candidate-limit', type=int, default=20)
    parser.add_argument('--allow-special-second-line', action='store_true')
    parser.add_argument('--producer-upper-rank31', action='store_true',
                        help='Consume the producer certification rank(U_S)=31 and PSD; enable exact Schur pair filters.')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        if not args.seed or not args.domains or args.seconds <= 0:
            parser.error('--seed, --domains and positive --seconds are required.')
        data = json.loads(Path(args.domains).read_text(encoding='utf-8-sig'))
        result = join(read_seed(args.seed), data, args.seconds, args.pair_limit,
                      args.candidate_limit, not args.allow_special_second_line, args.producer_upper_rank31)
        result.update(seed_path=args.seed, domains_path=args.domains)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'domain_sizes', 'seconds', 'scope') if k in result}))


if __name__ == '__main__':
    main()
