"""Gram-free histograms of the integral -4 vectors H[:,F].

For a nongrid rectangle F with e internal edges, H=W-Gamma P has norm
N=56-14e, sum zero, and values in {-3,-2,-1,0,1,2}. Its positive twos
are exactly the isolated corners of F. Thus (e,n_2) is one of
(0,4),(1,2),(2,0),(2,1), using the universal exclusion of three edges.

Put S=sum(h_+)=sum(h_-), E_sign=sum binom(|h|,2) on that sign.
Then N/2=S+E_++E_-. For two same-sign entries of magnitudes r,s,
their opposite-sign neighbour weights total at least 4(r+s).
The union weighs at most S, and the intersection at most 2+E_opposite
because mu=2 and a-1<=binom(a,2). Consequently
    E_sign <= N/2+2-4(r+s).
It suffices to test the two largest magnitudes of each sign.
This does not assume a fixed Gram, rank, symmetry, or selected root.

The finite table below is a NECESSARY relaxation of realizable histograms.
All its points and supporting planes are computed using Python integers.
"""

from functools import lru_cache
from itertools import combinations
from math import gcd


def h_value(rectangle, target, z):
    return 3 * int(rectangle == target) + 1 - len(set(rectangle) & set(target)) - z


def sign_overlap_possible(counts, half_norm):
    """Counts maps positive magnitudes to multiplicities for one sign."""
    largest = []
    excess = sum(r * (r - 1) // 2 * n for r, n in counts.items())
    for r in sorted(counts, reverse=True):
        largest.extend([r] * min(counts[r], 2 - len(largest)))
        if len(largest) == 2:
            return excess <= half_norm + 2 - 4 * sum(largest)
    return True


@lru_cache(None)
def histogram_rows():
    """All necessary (e,n_positive2,n_negative3,n_negative2) tuples."""
    rows = []
    for e, p2 in ((0, 4), (1, 2), (2, 0), (2, 1)):
        half = 28 - 7 * e
        # N and integrality bound these loops, without any empirical cutoff.
        for m3 in range((2 * half) // 9 + 1):
            for m2 in range((2 * half) // 4 + 1):
                p1 = half - 3 * p2 - m2 - 3 * m3
                m1 = half - p2 - 3 * m2 - 6 * m3
                zero = 84 - p2 - p1 - m1 - m2 - m3
                if min(p1, m1, zero) < 0:
                    continue
                counts = {2: p2, 1: p1, -1: m1, -2: m2, -3: m3, 0: zero}
                if any(n and r*r + 7*abs(r) > 2*half for r, n in counts.items()):
                    continue
                if not sign_overlap_possible({2: p2, 1: p1}, half):
                    continue
                if not sign_overlap_possible({3: m3, 2: m2, 1: m1}, half):
                    continue
                assert sum(counts.values()) == 84
                assert sum(r*n for r, n in counts.items()) == 0
                assert sum(r*r*n for r, n in counts.items()) == 2*half
                rows.append((e, p2, m3, m2))
    return tuple(rows)


@lru_cache(None)
def histogram_facets():
    """Exact supporting planes a*e+b*n_negative3+c*n_negative2 <= d.

Only nonnegative normals are retained: lower bounds are already present.
Testing every enumerated histogram establishes validity of every plane;
facet completeness is not needed for the soundness of these cuts.
"""
    points = sorted({(e, m3, m2) for e, p2, m3, m2 in histogram_rows()})
    planes = set()
    for x, y, z in combinations(points, 3):
        u = [b-a for a, b in zip(x, y)]
        v = [b-a for a, b in zip(x, z)]
        normal = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
        divisor = gcd(*normal)
        if not divisor:
            continue
        normal = [n // divisor for n in normal]
        for sign in (1, -1):
            a = tuple(sign*n for n in normal)
            if min(a) < 0:
                continue
            d = sum(n*t for n, t in zip(a, x))
            if all(sum(n*t for n, t in zip(a, p)) <= d for p in points):
                planes.add(a + (d,))
    assert planes
    return tuple(sorted(planes))


def linear_bounds(columns, rectangles, nongrid):
    """Integer LP rows: use 2e=sum of the own-rectangle degrees."""
    nongrid = {tuple(q) for q in nongrid}
    output = []
    for j, target in enumerate(rectangles):
        if target not in nongrid:
            continue
        for a, b, c, d in histogram_facets():
            coefficients = []
            for qi, si, state in columns:
                h = h_value(rectangles[qi], target, state[j])
                coefficients.append(a * state[j] * int(qi == j)
                                    + 2*b*int(h == -3) + 2*c*int(h == -2))
            output.append({'coefficients': coefficients, 'upper': 2*d,
                           'kind': 'short_column_histogram', 'indices': [j],
                           'normal': [a, b, c], 'half_upper': d})
    return output


def add_histogram_tables(model, rectangles, nongrid, row_terms):
    """row_terms = (rectangle_index, state, multiplicity/Boolean) triples.

Works with aggregate design multiplicities and with individual vertex
state indicators in the joint adjacency model. No products are introduced.
"""
    nongrid = {tuple(q) for q in nongrid}
    tables = 0
    for j, target in enumerate(rectangles):
        if target not in nongrid:
            continue
        e = model.new_int_var(0, 2, f'short_column_edges_{j}')
        p2 = model.new_int_var(0, 4, f'short_column_p2_{j}')
        m3 = model.new_int_var(0, 2, f'short_column_m3_{j}')
        m2 = model.new_int_var(0, 14, f'short_column_m2_{j}')
        model.add(2*e == sum(z[j]*x for qi, z, x in row_terms if qi == j))
        for value, count in ((2, p2), (-3, m3), (-2, m2)):
            model.add(count == sum(x for qi, z, x in row_terms
                                  if h_value(rectangles[qi], target, z[j]) == value))
        model.add_allowed_assignments([e, p2, m3, m2], histogram_rows())
        tables += 1
    return {'tables': tables, 'histograms_per_table': len(histogram_rows()),
            'boolean_integer_products': 0, 'uses_fixed_Gram': False}


def witness_histograms(row_multisets, nongrid):
    rectangles = [tuple(item['rectangle']) for item in row_multisets]
    output = []
    for j, target in enumerate(rectangles):
        if target not in nongrid:
            continue
        twice_e = sum(z[j] for z in row_multisets[j]['states'])
        assert twice_e % 2 == 0
        values = [h_value(q, target, z[j]) for q, item in zip(rectangles, row_multisets) for z in item['states']]
        record = (twice_e // 2, values.count(2), values.count(-3), values.count(-2))
        output.append({'rectangle': list(target), 'histogram': list(record),
                       'admissible': record in histogram_rows(), 'sum': sum(values),
                       'squared_norm': sum(v*v for v in values)})
    return output


def check_witness(row_multisets, nongrid):
    records = witness_histograms(row_multisets, nongrid)
    assert all(r['admissible'] and r['sum'] == 0 and r['squared_norm'] == 56-14*r['histogram'][0]
               for r in records)
    return True


if __name__ == '__main__':
    import json
    print(json.dumps({'rows': histogram_rows(), 'facets': histogram_facets()}))
