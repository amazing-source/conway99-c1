"""A four-column defect square forces even degrees on the complementary triangle.

For Conway, if H_ab=H_cd=-H_ac=-H_bd is nonzero, its support is exactly
the four square rectangles and the three rectangles on the remaining
root lines. All 28 entries have absolute value one. The restriction to
the last 12 vertices is killed by their induced adjacency matrix.

In particular, if two complementary rectangles are grids, the third
must be empty. If its H column equals a disjoint column, this is
impossible. Detection uses component equations only, not row catalogues,
Gram covers, symmetry assumptions or a prism budget. E3 is required.
See notes/CARRE_DE_DEFAUT_ET_PARITE_2026_10_18.txt for the proof.
"""

from fractions import Fraction
from itertools import combinations
from math import lcm


RECTANGLES = list(combinations(range(7), 2))
INDEX = {q: i for i, q in enumerate(RECTANGLES)}


def component_rows(template):
    groups = template['nontrivial_component_groups']
    nongrid = {tuple(q) for q in template['nongrid_edges']}
    assert nongrid <= set(INDEX)
    assert len(groups) == 7
    rows, descriptions = [], []
    for a, blocks in enumerate(groups):
        used = set()
        for block in blocks:
            assert len(block) >= 2 and len(set(block)) == len(block)
            assert a not in block and set(block) <= set(range(7))
            assert not used.intersection(block)
            used.update(block)
        assert used == {b for b in range(7) if tuple(sorted((a, b))) in nongrid}
        for block in list(blocks) + [[b] for b in range(7) if b != a and b not in used]:
            support = {tuple(sorted((a, b))) for b in block}
            rows.append([int(q in support) for q in RECTANGLES])
            descriptions.append({'root_line': a, 'block': sorted(block)})
    return rows, descriptions


def squares(template):
    """Direct four-cycles of pair components; no rational elimination needed."""
    parts = template['nontrivial_component_groups']
    result = []
    for vertices in combinations(range(7), 4):
        a = vertices[0]
        for b, c in combinations(vertices[1:], 2):
            d = next(v for v in vertices if v not in (a, b, c))
            required = {a: {b, c}, b: {a, d}, c: {a, d}, d: {b, c}}
            if all(any(set(block) == target for block in parts[v]) for v, target in required.items()):
                result.append([a, b, c, d])
    return result


def _basis(rows):
    basis = {}
    for i, values in enumerate(rows):
        row = list(map(Fraction, values))
        combination = [Fraction(int(i == j)) for j in range(len(rows))]
        for pivot, (old, coeff) in sorted(basis.items()):
            if row[pivot]:
                factor = row[pivot]
                row = [x-factor*y for x, y in zip(row, old)]
                combination = [x-factor*y for x, y in zip(combination, coeff)]
        pivot = next((j for j, x in enumerate(row) if x), None)
        if pivot is not None:
            factor = row[pivot]
            basis[pivot] = ([x/factor for x in row], [x/factor for x in combination])
    return basis


def _identity(basis, row_count, f, other):
    row = [Fraction(int(q == f)-int(q == other)) for q in RECTANGLES]
    combination = [Fraction(0)]*row_count
    for pivot, (old, coeff) in sorted(basis.items()):
        factor = row[pivot]
        if factor:
            row = [x-factor*y for x, y in zip(row, old)]
            combination = [x+factor*y for x, y in zip(combination, coeff)]
    if any(row):
        return None
    denominator = lcm(*(x.denominator for x in combination))
    return {'denominator': denominator,
            'component_coefficients': [[i, int(denominator*x)] for i, x in enumerate(combination) if x]}


def find_obstruction(template):
    found = squares(template)
    if not found:
        return None
    rows, descriptions = component_rows(template)
    nongrid = {tuple(q) for q in template['nongrid_edges']}
    basis = None
    for square in found:
        remaining = sorted(set(range(7))-set(square))
        triangle = list(combinations(remaining, 2))
        bad = [q for q in triangle if q in nongrid]
        if len(bad) != 1:
            continue
        f = bad[0]
        if basis is None:
            basis = _basis(rows)
        for other in RECTANGLES:
            if set(f).intersection(other):
                continue
            identity = _identity(basis, len(rows), f, other)
            if identity is not None:
                certificate = {'square': square, 'remaining_root_lines': remaining,
                    'forced_empty_rectangle': list(f), 'equal_disjoint_column': list(other),
                    'column_identity': identity, 'component_row_order': descriptions,
                    'uses_universal_E3_exclusion': True, 'uses_Gram_cover': False,
                    'uses_row_catalogue': False, 'uses_prism_budget': False}
                verify_certificate(template, certificate)
                return certificate
    return None


def verify_certificate(template, certificate):
    """Integer-only verification of the finite hypotheses of the written lemma."""
    rows, descriptions = component_rows(template)
    assert certificate['component_row_order'] == descriptions
    square = certificate['square']
    assert square in squares(template)
    remaining = sorted(set(range(7))-set(square))
    assert certificate['remaining_root_lines'] == remaining
    f = tuple(certificate['forced_empty_rectangle'])
    other = tuple(certificate['equal_disjoint_column'])
    assert f in list(combinations(remaining, 2)) and other in INDEX
    assert not set(f).intersection(other)
    nongrid = {tuple(q) for q in template['nongrid_edges']}
    assert [q for q in combinations(remaining, 2) if q in nongrid] == [f]
    identity = certificate['column_identity']
    denominator = identity['denominator']
    assert isinstance(denominator, int) and denominator > 0
    total = [0]*21
    for i, coefficient in identity['component_coefficients']:
        assert isinstance(i, int) and 0 <= i < len(rows)
        assert isinstance(coefficient, int)
        total = [x+coefficient*y for x, y in zip(total, rows[i])]
    assert total == [denominator*(int(q == f)-int(q == other)) for q in RECTANGLES]
    return {'status': 'SQUARE_DEFECT_OBSTRUCTION_CHECKED', 'square': square,
            'forced_empty_rectangle': list(f), 'minimum_degree_from_equal_column': 1,
            'even_degree_forced': True, 'maximum_total_degree_from_E3': 4,
            'minimum_total_degree_after_evenness': 8, 'global_conway_exclusion': False}


def forbidden_states(template, row_types):
    """Necessary state cuts from saturation and even degrees, for every square."""
    assert [item['rectangle'] for item in row_types] == [list(q) for q in RECTANGLES]
    forbidden = set()
    found = squares(template)
    for a, b, c, d in found:
        positive = {tuple(sorted((a, b))), tuple(sorted((c, d)))}
        negative = {tuple(sorted((a, c))), tuple(sorted((b, d)))}
        remaining = set(range(7))-{a, b, c, d}
        triangle = [q for q in RECTANGLES if set(q) <= remaining]
        js = [INDEX[q] for q in triangle]
        f = tuple(sorted((a, b)))
        fi = INDEX[f]
        for qi, (q, item) in enumerate(zip(RECTANGLES, row_types)):
            base = 3*int(q == f)+1-len(set(q)&set(f))
            for si, state in enumerate(item['states']):
                h = base-state[fi]
                valid = h == 1 if q in positive else h == -1 if q in negative else abs(h) == 1 if q in triangle else h == 0
                if not valid or (q in triangle and sum(state[j] for j in js) % 2):
                    forbidden.add((qi, si))
    return forbidden, found
