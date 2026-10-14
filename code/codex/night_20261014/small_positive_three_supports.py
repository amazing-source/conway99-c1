"""Exact support graphs for integral eigenvalue-three vectors of norm <=16.

The mass bound excludes entries of magnitude two at these norms. For each
sign on at most eight vertices, the induced graph has minimum
degree three, maximum degree four, and the SRG common-neighbor upper bounds.
This script enumerates these necessary induced graphs and the cross edges.
It does not claim that any surviving support extends to an SRG.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
from math import factorial
from pathlib import Path
import argparse
import json


def edge(ns, x, y):
    ns[x] |= 1 << y
    ns[y] |= 1 << x


def valid(ns):
    return all((ns[x] & ns[y]).bit_count() <= (1 if ns[x] >> y & 1 else 2)
               for x, y in combinations(range(len(ns)), 2))


def pairs(n):
    return list(combinations(range(n), 2))


def encode(ns):
    return sum(1 << k for k, (x, y) in enumerate(pairs(len(ns))) if ns[x] >> y & 1)


def decode(code, n):
    ns = [0]*n
    for k, (x, y) in enumerate(pairs(n)):
        if code >> k & 1:
            edge(ns, x, y)
    return ns


def cubic_graphs(n):
    result = set()
    def walk(ns):
        v = next((v for v, row in enumerate(ns) if row.bit_count() < 3), None)
        if v is None:
            result.add(encode(ns))
            return
        need = 3-ns[v].bit_count()
        candidates = [x for x in range(v+1, n) if ns[x].bit_count() < 3 and not ns[v] >> x & 1]
        for chosen in combinations(candidates, need):
            nn = ns.copy()
            for x in chosen:
                edge(nn, v, x)
            if valid(nn):
                walk(nn)
    walk([0]*n)
    return result


def degree_four_graphs(n):
    """Fix vertex zero of degree four; enumerate its matching and all else."""
    result = set()
    for matching_size in range(3):
        ns = [0]*n
        for x in range(1, 5):
            edge(ns, 0, x)
        for x, y in [(1, 2), (3, 4)][:matching_size]:
            edge(ns, x, y)
        remaining = [(x, y) for x, y in pairs(n) if y >= 5 and x != 0]
        for selected in range(1 << len(remaining)):
            nn = ns.copy()
            for k, (x, y) in enumerate(remaining):
                if selected >> k & 1:
                    edge(nn, x, y)
            if all(3 <= row.bit_count() <= 4 for row in nn) and valid(nn):
                result.add(encode(nn))
    return result


def isomorphism_orbits(codes, n):
    unseen = set(codes)
    pair_indices = {p: k for k, p in enumerate(pairs(n))}
    reps = []
    while unseen:
        code = min(unseen)
        ns = decode(code, n)
        edges = [(x, y) for x, y in pairs(n) if ns[x] >> y & 1]
        orbit = set()
        for perm in permutations(range(n)):
            transformed = 0
            for x, y in edges:
                transformed |= 1 << pair_indices[tuple(sorted((perm[x], perm[y])))]
            orbit.add(transformed)
        removed = unseen & orbit
        unseen -= orbit
        reps.append(dict(code=code, degrees=sorted(row.bit_count() for row in ns),
                         orbit_size_full=len(orbit), enumerated_labels=len(removed),
                         edges=edges))
    return reps


def support_couplings(first, second):
    n = len(first)
    left = [x for x, row in enumerate(first) if row.bit_count() == 4]
    right = [x for x, row in enumerate(second) if row.bit_count() == 4]
    if len(left) != len(right):
        return []
    survivors = []
    for order in permutations(right):
        ns = first.copy() + [row << n for row in second]
        for x, y in zip(left, order):
            edge(ns, x, n+y)
        if valid(ns):
            signs = [1]*n + [-1]*n
            assert all(sum(signs[y] for y in range(2*n) if ns[x] >> y & 1) == 3*signs[x]
                       for x in range(2*n))
            survivors.append(order)
    return survivors


def embedding_bound(ns):
    """Induced labeled embedding bound from degrees and lambda/mu alone."""
    n = len(ns)
    @lru_cache(None)
    def best(assigned):
        if assigned == (1 << n)-1:
            return 1, []
        answer = None
        for v in range(n):
            if assigned >> v & 1:
                continue
            known_neighbors = [x for x in range(n) if assigned >> x & 1 and ns[v] >> x & 1]
            if len(known_neighbors) >= 2:
                choices = min((1 if ns[x] >> y & 1 else 2) - (ns[x] & ns[y] & assigned).bit_count()
                              for x,y in combinations(known_neighbors,2))
            elif known_neighbors:
                choices = 14-(ns[known_neighbors[0]] & assigned).bit_count()
            elif assigned:
                choices = 85-assigned.bit_count()+min((ns[x] & assigned).bit_count()
                                                      for x in range(n) if assigned >> x & 1)
            else:
                choices = 99
            assert choices >= 1
            remaining, order = best(assigned | 1 << v)
            candidate = (choices*remaining, [(v,choices)] + order)
            if answer is None or candidate[0] < answer[0]:
                answer = candidate
        return answer
    count, order = best(0)
    return dict(labeled_embeddings=count, order_and_choice_bounds=order)


def outside_patterns(ns, signs=None):
    n = len(ns)
    residual = {(x,y): (1 if ns[x] >> y & 1 else 2) - (ns[x] & ns[y]).bit_count()
                for x, y in pairs(n)}
    assert min(residual.values()) >= 0
    compatible = [0]*n
    for (x,y), count in residual.items():
        if count:
            compatible[x] |= 1 << y
            compatible[y] |= 1 << x
    result = []
    if signs is None:
        signs = [1]*(n//2) + [-1]*(n//2)
    def walk(selected, available, balance):
        if selected.bit_count() > 14:
            return
        if any((row & selected).bit_count() > (1 if selected >> x & 1 else 2)
               for x, row in enumerate(ns)):
            return
        if balance == 0:
            result.append(selected)
        while available:
            b = available & -available
            available ^= b
            x = b.bit_length()-1
            walk(selected | b, available & compatible[x], balance + signs[x])
    walk(0, (1 << n)-1, 0)
    assert len(set(result)) == len(result)
    return result, residual


def extension_linear_test(ns, signs=None):
    import numpy as np
    from scipy.optimize import linprog
    patterns, residual = outside_patterns(ns, signs)
    n = len(ns)
    row_labels = [()] + [(x,) for x in range(n)] + pairs(n)
    rhs = [99-n] + [14-row.bit_count() for row in ns] + list(residual.values())
    matrix = np.array([[all(pattern >> x & 1 for x in label) for pattern in patterns]
                       for label in row_labels], dtype=float)
    primal = linprog(np.zeros(len(patterns)), A_eq=matrix, b_eq=rhs,
                     bounds=(0, None), method='highs')
    if primal.success:
        for denominator in [100, 10000, 1000000]:
            counts = [(pattern, Fraction(float(x)).limit_denominator(denominator))
                      for pattern, x in zip(patterns, primal.x) if abs(x) > 1e-9]
            if all(count >= 0 for _, count in counts) and all(
                sum(count for pattern, count in counts if all(pattern >> x & 1 for x in label)) == b
                for label, b in zip(row_labels, rhs)):
                return dict(pattern_count=len(patterns), verdict='exact_fractionally_feasible',
                            integral=all(count.denominator == 1 for _, count in counts),
                            incidence_counts=[(pattern, str(count)) for pattern, count in counts])
        return dict(pattern_count=len(patterns), verdict='numerically_feasible')
    if primal.status != 2:
        return dict(pattern_count=len(patterns), verdict='unresolved', solver_message=primal.message)
    dual = linprog(np.array(rhs, dtype=float), A_ub=-matrix.T,
                   b_ub=np.zeros(len(patterns)), bounds=(-1, 1), method='highs')
    assert dual.success and dual.fun < 0
    for denominator in [100, 10000, 1000000]:
        certificate = [Fraction(float(x)).limit_denominator(denominator) for x in dual.x]
        value = sum(a*b for a, b in zip(certificate, rhs))
        columns = [sum(certificate[k] for k, label in enumerate(row_labels)
                       if all(pattern >> x & 1 for x in label)) for pattern in patterns]
        if value < 0 and min(columns) >= 0:
            return dict(pattern_count=len(patterns), verdict='excluded_exact_farkas',
                        certificate=[str(x) for x in certificate],
                        certificate_rhs=str(value), min_column=str(min(columns)))
    return dict(pattern_count=len(patterns), verdict='infeasible_without_exact_certificate')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outside-lp', action='store_true')
    args = parser.parse_args()
    report = {}
    for n in [6, 7, 8]:
        codes = cubic_graphs(n) | degree_four_graphs(n)
        reps = isomorphism_orbits(codes, n)
        couplings = []
        for i in range(len(reps)):
            for j in range(i, len(reps)):
                good = support_couplings(decode(reps[i]['code'], n), decode(reps[j]['code'], n))
                if good:
                    item = dict(first=i, second=j, matchings=good)
                    if args.outside_lp:
                        outcomes = []
                        for order in good:
                            left = decode(reps[i]['code'], n)
                            right = decode(reps[j]['code'], n)
                            ns = left + [row << n for row in right]
                            fours = [x for x, row in enumerate(left) if row.bit_count() == 4]
                            for x, y in zip(fours, order):
                                edge(ns, x, n+y)
                            outcomes.append(extension_linear_test(ns))
                        item['outside_lp'] = outcomes
                    couplings.append(item)
        report[n] = dict(enumerated_graphs=len(codes), induced_graph_types=len(reps),
                         representatives=reps, support_couplings=couplings)
        print(json.dumps(dict(sign_size=n, enumerated_graphs=len(codes),
                              induced_graph_types=len(reps),
                              degrees=Counter(tuple(r['degrees']) for r in reps).__str__(),
                              coupling_counts=[(c['first'], c['second'], len(c['matchings'])) for c in couplings],
                              lp=Counter(x['verdict'] for c in couplings for x in c.get('outside_lp', [])).__str__())), flush=True)
    assert [report[n]['induced_graph_types'] for n in [6,7,8]] == [1,1,7]
    assert sum(len(c['matchings']) for c in report[8]['support_couplings']) == 42
    prism_bound = 1150
    prism_quotient, prism_remainder = divmod(prism_bound, 6)
    twin_pairs = prism_quotient*15 + prism_remainder*(prism_remainder-1)//2
    assert twin_pairs == 2871
    report['global_bounds'] = dict(prism_count_assumption=prism_bound,
                                   prism_boundary_class_size=6,
                                   twin_prism_pairs=twin_pairs,
                                   signed_norm12_vectors=2*twin_pairs,
                                   seven_vertex_graphs=99*21*2,
                                   seven_vertex_boundary_class_size=3,
                                   signed_norm14_vectors=2*99*21*2,
                                   norm16_count='not bounded here')
    windmill = [0]*7
    for x in range(1,7):
        edge(windmill,0,x)
    for x,y in [(1,2),(3,4),(5,6)]:
        edge(windmill,x,y)
    weighted = []
    other_parts = [('windmill',windmill,[2]+[1]*6)]
    other_parts += [(f'cubic8_type_{i}',decode(rep['code'],8),[1]*8)
                    for i,rep in enumerate(report[8]['representatives']) if max(rep['degrees']) == 3]
    for name, second, second_weights in other_parts:
        ns = windmill + [row << 7 for row in second]
        signs = [2]+[1]*6+[-x for x in second_weights]
        assert sum(signs)==0 and sum(abs(x) for x in signs)==16
        assert all(sum(signs[y] for y in range(len(ns)) if ns[x] >> y & 1)==3*signs[x]
                   for x in range(len(ns)))
        item = dict(second_part=name, support=len(ns), squared_norm=sum(x*x for x in signs),
                    signs=signs, edges=[(x,y) for x,y in pairs(len(ns)) if ns[x]>>y&1])
        if args.outside_lp:
            item['outside_lp']=extension_linear_test(ns, signs)
        weighted.append(item)
    report['weighted_l1_at_most_16'] = weighted
    report['l1_at_most_16_total_templates'] = 48
    bounds_by_fours = Counter()
    for rep in report[8]['representatives']:
        ns = decode(rep['code'],8)
        rep['embedding_bound'] = embedding_bound(ns)
        automorphisms = factorial(8)//rep['orbit_size_full']
        rep['automorphisms'] = automorphisms
        rep['induced_copy_bound'] = rep['embedding_bound']['labeled_embeddings']//automorphisms
        fours = rep['degrees'].count(4)
        bounds_by_fours[fours] += rep['induced_copy_bound']
        proper = [bits for bits in range(1,255)
                  if all((ns[x] & bits).bit_count() >= 3 for x in range(8) if bits >> x & 1)]
        rep['proper_minimum_degree_three_subsets'] = proper
        if fours in [0,2]:
            assert not proper
        else:
            assert len(proper)==2 and all(bits.bit_count()==6 for bits in proper)
            for bits in proper:
                missing = 255 ^ bits
                x,y = [x for x in range(8) if missing >> x & 1]
                assert ns[x] >> y & 1 and ns[x].bit_count()==ns[y].bit_count()==3
    assert dict(bounds_by_fours)=={0:79002,2:24948,4:2079}
    assert (6-1)**2 > 4*6-2  # A two-lift on >=12 high vertices is impossible.
    norm16_parts = {0:2*bounds_by_fours[0], 2:4*bounds_by_fours[2], 4:10*bounds_by_fours[4]}
    norm16_bound = sum(norm16_parts.values())
    weighted_bound = 2*3*(99*35)
    total_bound = 2*twin_pairs + 2*99*21*2 + norm16_bound + weighted_bound
    assert norm16_bound==278586 and weighted_bound==20790 and total_bound==313434
    report['global_bounds'].update(dict(norm16_count=norm16_bound,
                                        norm16_by_number_of_degree_four_vertices=norm16_parts,
                                        weighted_l1_16_norm18_or_20=weighted_bound,
                                        all_nonzero_integer_eigenvalue3_l1_at_most_16=total_bound))
    print(json.dumps(dict(weighted_templates=len(weighted),
                          lp=[x.get('outside_lp',{}).get('verdict') for x in weighted],
                          signed_kernel_l1_16_bound=total_bound)), flush=True)
    out = Path(__file__).resolve().parents[3] / 'data' / 'codex_night_20261014'
    (out / 'small_positive_three_supports.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
