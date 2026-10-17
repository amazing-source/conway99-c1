"""Intersections of orthogonal co-Heawood vectors and a four-root edge.

Exact finite part of the proof in the 14 October night journal. A common
edge in four orthogonal roots forces a 39-vertex graph, up to isomorphism.
This is a necessary induced graph, not a completion to an SRG.
"""
from itertools import combinations, permutations, product
from fractions import Fraction
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import json


ARCS = [(i, j) for i in range(4) for j in range(4) if i != j]
N = {e: 3+k for k, e in enumerate(ARCS)}
P = {e: 15+k for k, e in enumerate(ARCS)}
Q = {e: 27+k for k, e in enumerate(ARCS)}


def cycles_at(i):
    labels = [j for j in range(4) if j != i]
    return [{j: perm[k] for k, j in enumerate(labels)}
            for perm in permutations(labels)
            if all(j != perm[k] for k, j in enumerate(labels))]


def four_root_graph(bits):
    cycles = [cycles_at(i)[bits[i]] for i in range(4)]
    ns = [0]*39
    def edge(x, y):
        assert x != y
        ns[x] |= 1 << y
        ns[y] |= 1 << x
    # 0 and 1 are the common edge. 2 is its unique common neighbor.
    edge(0, 1)
    edge(0, 2)
    edge(1, 2)
    for i, j in ARCS:
        edge(0, N[i, j])
        edge(1, P[i, j])
        edge(N[i, j], N[j, i])
        edge(P[i, j], P[j, i])
        edge(Q[i, j], Q[j, i])
        for k in range(4):
            if k != i and k != j:
                edge(Q[i, j], N[i, k])
                edge(Q[i, j], P[j, k])
        edge(Q[i, j], Q[cycles[i][j], i])
        # The co-Heawood common-neighbor equations force the inverse cycle.
        edge(N[i, j], P[i, cycles[i][cycles[i][j]]])

    forced_disjoint_arcs = set()
    for i, j in ARCS:
        k = cycles[i][j]
        ell = cycles[j][cycles[j][i]]
        if k != ell:
            forced_disjoint_arcs.add(tuple(sorted((Q[i, j], Q[ell, k]))))
    for x, y in forced_disjoint_arcs:
        edge(x, y)

    roots = []
    for i in range(4):
        f = [0]*39
        f[0], f[1] = 1, -1
        for j in range(4):
            if j != i:
                f[P[i, j]] = f[Q[i, j]] = 1
                f[N[i, j]] = f[Q[j, i]] = -1
        roots.append(f)
    assert all(sum(f) == 0 and sum(x*x for x in f) == 14 for f in roots)
    assert all(sum(x*y for x, y in zip(roots[i], roots[j])) == 0
               for i, j in combinations(range(4), 2))
    linear_witness = next((dict(root=i, vertex=x, observed=observed,
                                required=-4*f[x])
                           for i, f in enumerate(roots) for x in range(39)
                           if (observed := sum(f[y] for y in range(39)
                                               if ns[x] >> y & 1)) != -4*f[x]), None)
    common_witness = next((dict(pair=[x, y], adjacent=bool(ns[x] >> y & 1),
                                common=[z for z in range(39)
                                        if (ns[x] & ns[y]) >> z & 1])
                           for x, y in combinations(range(39), 2)
                           if (ns[x] & ns[y]).bit_count()
                           > (1 if ns[x] >> y & 1 else 2)), None)
    return ns, dict(bits=bits, added_disjoint_arc_edges=len(forced_disjoint_arcs),
                    linear_witness=linear_witness, common_witness=common_witness)


def find_label_isomorphism(first, second):
    for perm in permutations(range(4)):
        mapping = list(range(39))
        for table in (N, P, Q):
            for (i, j), vertex in table.items():
                mapping[vertex] = table[perm[i], perm[j]]
        if all(bool(first[x] >> y & 1) == bool(second[mapping[x]] >> mapping[y] & 1)
               for x, y in combinations(range(39), 2)):
            return dict(root_permutation=perm, vertex_permutation=mapping)
    return None


def norm28_checks():
    # Mass of either sign M is at least 4a. A coefficient of absolute
    # value a contributes a^2-a beyond the l1 norm, so norm>=a^2+7a.
    assert 3*3 + 7*3 > 28
    # Two coefficients +2 force M>=16-4=12, hence the total number
    # of coefficients of absolute value 2 is <=2. Both are positive;
    # the negative common-neighbor mass is then <=2, forcing M>=14,
    # inconsistent with M=12. The same applies to the negative sign.
    types = []
    for plus_twos, minus_twos in product(range(2), repeat=2):
        twos = plus_twos + minus_twos
        mass = 14 - twos
        types.append(dict(plus_two=plus_twos, minus_two=minus_twos,
                          plus_one=mass-2*plus_twos,
                          minus_one=mass-2*minus_twos))
    for t in types:
        assert 4*(t['plus_two']+t['minus_two']) + t['plus_one']+t['minus_one'] == 28
        assert 2*t['plus_two']+t['plus_one'] == 2*t['minus_two']+t['minus_one']
    return types


def integer_kernel(matrix):
    """A rational nullspace basis, rescaled to primitive integer vectors."""
    width = len(matrix[0])
    rows = [[Fraction(x) for x in row] for row in matrix]
    pivots = []
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][col]
        rows[rank] = [x/value for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                value = rows[i][col]
                rows[i] = [x-value*y for x, y in zip(rows[i], rows[rank])]
        pivots.append(col)
        rank += 1
    basis = []
    for free in range(width):
        if free in pivots:
            continue
        vector = [Fraction(0)]*width
        vector[free] = Fraction(1)
        for i, pivot in enumerate(pivots):
            vector[pivot] = -rows[i][free]
        multiple = lcm(*(x.denominator for x in vector))
        vector = [int(x*multiple) for x in vector]
        divisor = reduce(gcd, vector)
        vector = [x//divisor for x in vector]
        assert all(sum(x*y for x, y in zip(row, vector)) == 0 for row in matrix)
        basis.append(vector)
    return basis


def exclude_neighbor_of_third_point(ns):
    """No outside vertex can be adjacent to vertex 2, whose degree is only 2.

    Such a vertex must meet N and P once each, plus a subset of the 12 Qs.
    Every co-Heawood permits at most one neighbor of each sign outside it.
    Q therefore is a partial directed permutation on four indices. We
    enumerate all 108 such subsets and all 12*12 N/P choices. Kernel
    equations of the principal (-4) projector refute every remaining row.
    """
    matrix = [[27*(i == j)-9*((ns[i] >> j) & 1)+1 for j in range(39)]
              for i in range(39)]
    basis = integer_kernel(matrix)
    assert len(basis) == 5
    assert all(sum(v) % 9 == 0 for v in basis)
    rhs = [sum(v)//9 for v in basis]
    q_subsets = []
    for mask in range(1 << 12):
        incoming, outgoing = [0]*4, [0]*4
        for k, (i, j) in enumerate(ARCS):
            if mask >> k & 1:
                outgoing[i] += 1
                incoming[j] += 1
        if max(incoming+outgoing) <= 1:
            q_subsets.append(([27+k for k in range(12) if mask >> k & 1],
                              incoming, outgoing))
    assert len(q_subsets) == 108
    counts = dict(enumerated=0, root_balance=0, root_balance_and_cap=0,
                  all_projector_kernel_equations=0)
    for (i, j), n in N.items():
        for (k, ell), p in P.items():
            for qs, incoming, outgoing in q_subsets:
                counts['enumerated'] += 1
                positive = [outgoing[h]+(h == k) for h in range(4)]
                negative = [incoming[h]+(h == i) for h in range(4)]
                if positive != negative:
                    continue
                counts['root_balance'] += 1
                if max(positive) > 1:
                    continue
                counts['root_balance_and_cap'] += 1
                selected = [2, n, p]+qs
                if all(sum(v[x] for x in selected) == target
                       for v, target in zip(basis, rhs)):
                    counts['all_projector_kernel_equations'] += 1
    assert counts['enumerated'] == 12*12*108
    assert counts['all_projector_kernel_equations'] == 0
    return dict(status='excluded', tested_rows=counts,
                principal_projector_kernel=basis, required_rhs=rhs,
                contradiction='The third point of the common edge has only two neighbors in the 39-vertex graph and requires twelve outside neighbors; not even one has a feasible incidence row.')


def check():
    cases, survivors = [], []
    for bits in product(range(2), repeat=4):
        ns, case = four_root_graph(bits)
        case['status'] = ('inconsistent eigenvector equations' if case['linear_witness']
                          else 'excess common neighbors' if case['common_witness']
                          else 'survives these necessary tests')
        cases.append(case)
        if case['status'] == 'survives these necessary tests':
            survivors.append((ns, case))
    counts = {status: sum(c['status'] == status for c in cases) for status in (
        'inconsistent eigenvector equations', 'excess common neighbors',
        'survives these necessary tests')}
    assert list(counts.values()) == [6, 8, 2]
    iso = find_label_isomorphism(survivors[0][0], survivors[1][0])
    assert iso is not None
    ns = survivors[0][0]
    edges = [(x, y) for x, y in combinations(range(39), 2) if ns[x] >> y & 1]
    assert len(edges) == 117
    degree_counts = {d: sum(x.bit_count() == d for x in ns)
                     for d in sorted({x.bit_count() for x in ns})}
    assert degree_counts == {2: 1, 5: 24, 7: 12, 14: 2}
    extension = exclude_neighbor_of_third_point(ns)
    return dict(
        status='exact checks pass', norm28_coefficient_types=norm28_checks(),
        orthogonal_root_intersections=dict(possible_sizes=[0, 2, 4],
            each_joint_sign_pattern_at_most_once=True,
            size_four_induces='two disjoint edges joining opposite joint signs'),
        four_roots_on_one_edge=dict(cases=cases, counts=counts,
            survivors_isomorphism=iso, induced_vertices=39, induced_edges=117,
            degree_counts=degree_counts, edges=edges, extension=extension),
        consequence='No edge lies in three members of a pairwise orthogonal family of co-Heawood sign vectors: a third would force a fourth, and that family is excluded.',
        scope='Four orthogonal co-Heawoods on a common edge excluded; C1 and an isolated co-Heawood remain open')


if __name__ == '__main__':
    report = check()
    out = Path('data/codex_night_20261014/orthogonal_root_intersections.json')
    out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    graph = report['four_roots_on_one_edge']
    Path('data/codex_night_20261014/four_root_edge_graph.txt').write_text(
        '39 117\n' + ''.join(f'{x} {y}\n' for x, y in graph['edges']), encoding='ascii')
    print(json.dumps(dict(status=report['status'], cases=graph['counts'],
                         induced_isomorphism_classes=1,
                         vertices=39, edges=117,
                         extension=graph['extension']['tested_rows'],
                         verdict=graph['extension']['status']), indent=2))
