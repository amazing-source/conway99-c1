"""Exact projection of the continuous common-neighbour auxiliaries.

For a pair i,j with s shared letters, the extended C2 formulation is
 y_t>=0, y_t>=x_it+x_jt-1, sum_t y_t<=2-s-x_ij.
For 0<=x<=1 its projection is exactly
 x_ij+sum_t max(0,x_it+x_jt-1)<=2-s.
For every subset W this yields the integer row
 x_ij+sum_{t in W}(x_it+x_jt)<=2-s+|W|.
Selecting the positive terms separates the whole family in linear time.
Repeated linear forms are grouped with positive integer multiplicities.

No solver, graph sample, or third-party package is used here.  This is an
equivalent formulation, not a claim that a cut loop will be faster.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import argparse
import json


def exact_number(value):
    if isinstance(value, float):
        raise ValueError('Use an integer or an exact rational string.')
    return Fraction(str(value))


def validate_model(model):
    n = model['n_variables']
    if not isinstance(n, int) or not 0 <= model['pair_variable'] < n:
        raise ValueError('Invalid pair-variable index.')
    if model['shared_letters'] not in (0, 1):
        raise ValueError('Expected zero or one shared letter.')
    if any(not 0 <= a < n or not 0 <= b < n or not isinstance(weight, int) or weight <= 0
           for a, b, weight in model['terms']):
        raise ValueError('Invalid common-neighbour variable or multiplicity.')


def subset_cut(model, selected_terms):
    """Any subset gives a valid integer <= row, even if chosen numerically."""
    validate_model(model)
    n = model['n_variables']
    selected = sorted(set(selected_terms))
    terms = model['terms']
    if any(not isinstance(j, int) or not 0 <= j < len(terms) for j in selected):
        raise ValueError('Unknown common-neighbour term.')
    coefficients = [0]*n
    coefficients[model['pair_variable']] = 1
    rhs = 2-model['shared_letters']
    for j in selected:
        left, right, weight = terms[j]
        coefficients[left] += weight
        coefficients[right] += weight
        rhs += weight
    selected_set = set(selected)
    return dict(coefficients=coefficients, rhs=rhs,
                kind='projected_C2_subset', selected_terms=selected,
                derivation=dict(sum_cap_multiplier=1,
                    product_lower_bound_multipliers=[weight if j in selected_set else 0
                        for j, (_, _, weight) in enumerate(terms)],
                    nonnegativity_multipliers=[0 if j in selected_set else weight
                        for j, (_, _, weight) in enumerate(terms)]))


def separate_pair(model, assignment):
    """Return the maximally violated subset row, or certify this C2 pair.

    The exact input may be fractional.  No subset enumeration is performed.
    Choosing terms approximately still gives a valid row via subset_cut,
    but would no longer certify that no violated subset exists.
    """
    values = [exact_number(x) for x in assignment]
    if len(values) != model['n_variables'] or any(x < 0 or x > 1 for x in values):
        raise ValueError('Expected one exact value in [0,1] per edge variable.')
    return _separate_pair(model, values)


def _separate_pair(model, values):
    validate_model(model)
    selected = [j for j, (a, b, _) in enumerate(model['terms']) if values[a]+values[b] > 1]
    projected_lhs = values[model['pair_variable']]+sum(
        weight*max(Fraction(0), values[a]+values[b]-1)
        for a, b, weight in model['terms'])
    slack = 2-model['shared_letters']-projected_lhs
    return dict(feasible=slack >= 0, exact_slack=str(slack),
                projected_lhs=str(projected_lhs), cut=subset_cut(model, selected) if slack < 0 else None)


def separate_all(models, assignment):
    """Parse one fractional point once; return all violated pair cuts."""
    values = [exact_number(x) for x in assignment]
    if any(x < 0 or x > 1 for x in values) or any(model['n_variables'] != len(values) for model in models):
        raise ValueError('Expected a consistent exact point in the unit cube.')
    violations = []
    for index, model in enumerate(models):
        result = _separate_pair(model, values)
        if not result['feasible']:
            violations.append(dict(model_index=index, **result))
    return violations


def models_from_edge_orbits(labels, edge_orbits):
    """Build exact pair models in the producer's variable/label order.

    Each edge orbit is a list of pairs of vertex indices assigned one bit.
    All unordered pairs must be covered exactly once.  Identical pair
    constraints are merged by their ACTUAL linear forms, not by assuming
    an unverified group action.  Different models may share edge variables.
    """
    labels = [frozenset(p) for p in labels]
    n = len(labels)
    if len(set(labels)) != n:
        raise ValueError('Labels must be distinct.')
    variable = {}
    for index, orbit in enumerate(edge_orbits):
        for i, j in orbit:
            i, j = sorted((i, j))
            if not 0 <= i < j < n or (i, j) in variable:
                raise ValueError('Invalid or repeated pair in the variable partition.')
            variable[i, j] = index
    if len(variable) != n*(n-1)//2:
        raise ValueError('Every unordered pair must have an edge variable.')

    def edge(i, j):
        return variable[tuple(sorted((i, j)))]

    models = {}
    for i, j in combinations(range(n), 2):
        shared = len(labels[i] & labels[j])
        if shared not in (0, 1):
            raise ValueError('The lambda=1, mu=2 formula expects shared-letter count0 or1.')
        counts = Counter(tuple(sorted((edge(i, t), edge(j, t))))
                         for t in range(n) if t not in (i, j))
        terms = tuple((a, b, count) for (a, b), count in sorted(counts.items()))
        key = shared, edge(i, j), terms
        if key in models:
            models[key]['pair_count'] += 1
        else:
            models[key] = dict(n_variables=len(edge_orbits), representative=[i, j],
                pair_variable=edge(i, j), shared_letters=shared,
                terms=terms, pair_count=1)
    return list(models.values())


def report():
    # Both shared-letter cases, including repeated forms with multiplicity.
    fractional_cases = 0
    for shared in (0, 1):
        model = dict(n_variables=5, pair_variable=0, shared_letters=shared,
                     terms=[(1, 2, 1), (3, 4, 1)])
        for assignment in product(('0', '1/2', '1'), repeat=5):
            separated = separate_pair(model, assignment)
            values = list(map(Fraction, assignment))
            slacks = []
            for mask in range(4):
                cut = subset_cut(model, [j for j in range(2) if mask >> j & 1])
                proof = cut['derivation']
                for j, (_, _, weight) in enumerate(model['terms']):
                    assert weight-proof['product_lower_bound_multipliers'][j]-proof['nonnegativity_multipliers'][j] == 0
                assert cut['rhs'] == 2-shared+sum(proof['product_lower_bound_multipliers'])
                slacks.append(cut['rhs']-sum(a*x for a, x in zip(cut['coefficients'], values)))
            assert Fraction(separated['exact_slack']) == min(slacks)
            fractional_cases += 1
    model = dict(n_variables=2, pair_variable=0, shared_letters=1, terms=[(1, 1, 3)])
    weighted = separate_pair(model, ['1/4', '3/4'])
    assert weighted['cut']['coefficients'] == [1, 6]
    assert weighted['cut']['rhs'] == 4 and weighted['exact_slack'] == '-3/4'
    fractional = separate_pair(dict(n_variables=5, pair_variable=0, shared_letters=1,
        terms=[(1, 2, 1), (3, 4, 1)]), ['1/2', '3/4', '3/4', '3/4', '3/4'])
    assert fractional['cut']['coefficients'] == [1]*5
    assert fractional['cut']['rhs'] == 3 and fractional['exact_slack'] == '-1/2'
    labels = [(0, 2), (0, 3), (1, 2), (1, 3)]
    pairs = list(combinations(range(4), 2))
    partitions = ([[pair] for pair in pairs],
                  [[(0, 1), (2, 3)], [(0, 2), (1, 3)], [(0, 3), (1, 2)]])
    binary_cases = 0
    for orbits in partitions:
        models = models_from_edge_orbits(labels, orbits)
        assert sum(model['pair_count'] for model in models) == 6
        for assignment in product((0, 1), repeat=len(orbits)):
            gamma = [[0]*4 for _ in range(4)]
            for value, orbit in zip(assignment, orbits):
                for i, j in orbit:
                    gamma[i][j] = gamma[j][i] = value
            literal = all(len(set(labels[i]) & set(labels[j]))
                          +sum(gamma[i][t]*gamma[j][t] for t in range(4))
                          <= 2-gamma[i][j] for i, j in pairs)
            projected = all(separate_pair(model, assignment)['feasible'] for model in models)
            assert projected == literal
            assert bool(separate_all(models, assignment)) == (not literal)
            binary_cases += 1
    return dict(status='EXACT_C2_PROJECTION_AND_LINEAR_TIME_SEPARATION',
                fractional_subset_comparisons=fractional_cases,
                literal_binary_C2_comparisons=binary_cases,
                fractional_violation_example=fractional,
                repeated_form_example=weighted,
                scope='Eliminates the nonnegative continuous y variables with these lower bounds and C2 sum caps; no graph search or peer computation repeated.',
                limitation='Equivalent relaxation, not a bound on the number of cut-loop iterations or a speedup guarantee.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in (
        'status', 'fractional_subset_comparisons', 'literal_binary_C2_comparisons')}))
