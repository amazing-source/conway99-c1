"""Necessary integer -4 eigenvector constraints with an UNFIXED norm.

Every integer combination h=H d is integral and satisfies A h=-4h,
sum(h)=0, and vanishes on the closed root star. Its norm is the variable
sum h_w^2, not the value in the witness that suggested d. Thus a cut
found at one aggregate witness applies to every Gram of the template.

For each sign use its largest two magnitudes r,s and excess
E=sum binom(|h_w|,2). If two entries exist, N>=2E+8(r+s)-4.
The largest magnitude M also gives N>=M^2+7M.
For N=14, the seven vertices of each sign use each root label exactly
once (the established norm-two support lemma). Each of the seven root
lines therefore occurs twice in each sign. This is necessary, not a
claim that any feasible count solution is a graph.
"""

from itertools import combinations, product
from root_component_short_column_histograms import h_value


def scalar_violations(values, row_rectangles=None):
    norm = sum(v*v for v in values)
    violations = []
    assert sum(values) == 0
    for sign in (-1, 1):
        magnitudes = sorted((sign*v for v in values if sign*v > 0), reverse=True)
        if not magnitudes:
            continue
        required = magnitudes[0]**2+7*magnitudes[0]
        if required > norm:
            violations.append({'kind': 'one_coordinate', 'sign': sign, 'norm': norm, 'required': required})
        if len(magnitudes) >= 2:
            excess = sum(r*(r-1)//2 for r in magnitudes)
            required = 2*excess+8*sum(magnitudes[:2])-4
            if required > norm:
                violations.append({'kind': 'same_sign_overlap', 'sign': sign, 'norm': norm,
                                   'largest_two': magnitudes[:2], 'excess': excess, 'required': required})
        if norm == 14 and row_rectangles is not None:
            for line in range(7):
                count = sum(v == sign and line in q for v, q in zip(values, row_rectangles))
                if count != 2:
                    violations.append({'kind': 'norm14_root_line', 'sign': sign, 'norm': norm,
                                       'line': line, 'count': count, 'required_count': 2})
    return violations


def add_scalar_cuts(model, terms, rectangles, name):
    """terms: (row_rectangle_index, integer_value, multiplicity) triples."""
    assert terms
    max_by_rectangle = [max((v*v for qi, v, x in terms if qi == q), default=0)
                        for q in range(len(rectangles))]
    norm = model.new_int_var(0, 4*sum(max_by_rectangle), f'{name}_norm')
    model.add(norm == sum(v*v*x for qi, v, x in terms if v))
    model.add(sum(v*x for qi, v, x in terms if v) == 0)
    flags = constraints = 0
    for sign in (-1, 1):
        maximum = max((sign*v for qi, v, x in terms), default=0)
        if maximum <= 0:
            continue
        exists, repeated = [], []
        for threshold in range(1, maximum+1):
            above = sum(x for qi, v, x in terms if sign*v >= threshold)
            some = model.new_bool_var(f'{name}_{sign}_some_{threshold}')
            twice = model.new_bool_var(f'{name}_{sign}_twice_{threshold}')
            model.add(above >= 1).only_enforce_if(some)
            model.add(above == 0).only_enforce_if(some.Not())
            model.add(above >= 2).only_enforce_if(twice)
            model.add(above <= 1).only_enforce_if(twice.Not())
            exists.append(some); repeated.append(twice)
            flags += 2
        largest = model.new_int_var(0, maximum, f'{name}_{sign}_largest')
        second = model.new_int_var(0, maximum, f'{name}_{sign}_second')
        model.add(largest == sum(exists)); model.add(second == sum(repeated))
        lower = model.new_int_var(0, maximum**2+7*maximum, f'{name}_{sign}_one_bound')
        model.add_element(largest, [r*r+7*r for r in range(maximum+1)], lower)
        model.add(norm >= lower)
        excess = sum(v*(v-sign)//2*x for qi, v, x in terms if sign*v > 0)
        model.add(norm >= 2*excess+8*(largest+second)-4).only_enforce_if(repeated[0])
        constraints += 2
    root = model.new_bool_var(f'{name}_norm14')
    model.add(norm == 14).only_enforce_if(root)
    model.add(norm != 14).only_enforce_if(root.Not())
    for sign in (-1, 1):
        for line in range(7):
            count = sum(x for qi, v, x in terms if v == sign and line in rectangles[qi])
            model.add(count == 2).only_enforce_if(root)
    return {'threshold_flags': flags, 'norm_bounds': constraints, 'norm14_root_line_equations': 14}


def add_direction_cuts(model, rectangles, row_terms, directions):
    info = {'directions': len(directions), 'threshold_flags': 0,
            'norm_bounds': 0, 'norm14_root_line_equations': 0,
            'norm_is_variable': True, 'uses_Gram_cover': False}
    for di, direction in enumerate(directions):
        assert direction and all(type(j) is int and 0 <= j < len(rectangles)
                                 and type(c) is int for j, c in direction)
        assert len({j for j, c in direction}) == len(direction)
        terms = [(qi, sum(c*h_value(rectangles[qi], rectangles[j], z[j]) for j, c in direction), x)
                 for qi, z, x in row_terms]
        record = add_scalar_cuts(model, terms, rectangles, f'variable_norm_{di}')
        for key, value in record.items():
            info[key] += value
    return info


def candidate_directions(catalogue, support):
    """Sparse integer directions, deduplicated modulo known component relations."""
    assert 1 <= support <= 3
    linear = catalogue.get('affine_linear_numerator')
    seen = set()
    for size in range(1, support+1):
        for indices in combinations(range(21), size):
            for signs in product((-1, 1), repeat=size-1):
                direction = list(zip(indices, (1,)+signs))
                key = tuple(sum(c*linear[j][f] for j, c in direction) for f in range(len(linear[0]))) if linear else tuple(direction)
                if linear:
                    first = next((x for x in key if x), 0)
                    if not first:
                        continue
                    if first < 0:
                        key = tuple(-x for x in key)
                        direction = [(j, -c) for j, c in direction]
                if key not in seen:
                    seen.add(key)
                    yield direction


def separate(catalogue, row_multisets, support=3, maximum_norm=56):
    rectangles = [tuple(item['rectangle']) for item in row_multisets]
    h = [[h_value(q, f, z[j]) for j, f in enumerate(rectangles)]
         for q, item in zip(rectangles, row_multisets) for z in item['states']]
    row_rectangles = [q for q in rectangles for _ in range(4)]
    assert len(h) == 84
    gram = [[sum(row[i]*row[j] for row in h) for j in range(21)] for i in range(21)]
    records = []
    tested = short = 0
    for direction in candidate_directions(catalogue, support):
        tested += 1
        norm = sum(a*b*gram[i][j] for i, a in direction for j, b in direction)
        if not 0 < norm <= maximum_norm:
            continue
        short += 1
        values = [sum(c*row[j] for j, c in direction) for row in h]
        violations = scalar_violations(values, row_rectangles)
        if violations:
            records.append({'direction': direction, 'witness_norm': norm, 'violations': violations,
                            'total_violation': sum(max(1, v.get('required',norm)-norm) for v in violations)})
    records.sort(key=lambda r: (-r['total_violation'], r['witness_norm'], r['direction']))
    return {'directions_tested': tested, 'short_at_witness': short, 'violating_directions': records,
            'search_support': support, 'searched_witness_norm_at_most': maximum_norm}
