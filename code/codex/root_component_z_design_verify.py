"""Check a row-count Farkas certificate with Python integers only.

No numerical optimizer, SAT solver, NumPy or SymPy is imported. The checker
also establishes completeness of the finite row catalogue: an affine kernel
is checked exactly, its dimension is certified by rank modulo 3, and all
bounded integral assignments of the free coordinates are enumerated.
"""

import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

# Also support isolated Python (-I) when the optional integer histogram
# proof helper is needed. That helper imports only the standard library.
sys.path.insert(0, str(Path(__file__).resolve().parent))


RECTANGLES = list(combinations(range(7), 2))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rank_modulo_three(matrix):
    rows = [[v % 3 for v in row] for row in matrix]
    rank = 0
    for col in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][col], -1, 3)
        rows[rank] = [v * inverse % 3 for v in rows[rank]]
        for i in range(rank + 1, len(rows)):
            factor = rows[i][col]
            rows[i] = [(a - factor * b) % 3 for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def check_catalogue(template, catalogue):
    require(catalogue['status'] == 'ROW_CATALOGUE_COMPLETE', 'Incomplete catalogue.')
    groups = template['nontrivial_component_groups']
    require(len(groups) == 7, 'Seven line partitions required.')
    matrix, right = [], []
    for i, parts0 in enumerate(groups):
        require(parts0 is not None, 'Partial templates are not supported.')
        used = [j for part in parts0 for j in part]
        require(len(set(used)) == len(used) and all(0 <= j < 7 and j != i for j in used),
                'Invalid component partition.')
        parts = [list(part) for part in parts0] + [[j] for j in range(7) if j != i and j not in used]
        for part in parts:
            require(part, 'Empty component.')
            support = {tuple(sorted((i, j))) for j in part}
            matrix.append([int(q in support) for q in RECTANGLES])
            right.append([3 * int(q in support) + len(part) * (1 - int(i in q))
                          - len(set(q) & set(part)) for q in RECTANGLES])
    require(matrix == catalogue['component_matrix'] and right == catalogue['right_sides'],
            'Component system does not match the template.')
    free = catalogue['free_coordinates']
    f, den = len(free), catalogue['denominator']
    require(den > 0 and len(set(free)) == f and all(0 <= j < 21 for j in free), 'Invalid affine coordinates.')
    linear, offset = catalogue['affine_linear_numerator'], catalogue['affine_offset_numerator']
    require(len(linear) == len(offset) == 21 and all(len(r) == f for r in linear)
            and all(len(r) == 21 for r in offset), 'Invalid affine dimensions.')
    require(all(type(v) is int for row in linear + offset for v in row), 'Noninteger affine data.')
    for index, coordinate in enumerate(free):
        require(linear[coordinate] == [den * int(j == index) for j in range(f)]
                and not any(offset[coordinate]), 'Free-coordinate normalization failed.')
    for row, rhs in zip(matrix, right):
        require(all(sum(a * linear[j][k] for j, a in enumerate(row)) == 0 for k in range(f)), 'Invalid kernel.')
        require(all(sum(a * offset[j][q] for j, a in enumerate(row)) == den * rhs[q] for q in range(21)),
                'Invalid affine offset.')
    require(rank_modulo_three(matrix) == 21 - f, 'Kernel completeness rank check failed.')
    require(len(catalogue['row_types']) == 21, 'Missing row types.')
    columns = []
    for qi, (q, item) in enumerate(zip(RECTANGLES, catalogue['row_types'])):
        require(item['rectangle'] == list(q), 'Unexpected row-type order.')
        upper = [2 if set(q) & set(r) else 4 for r in RECTANGLES]
        expected = []
        for assignment in product(*(range(upper[j] + 1) for j in free)):
            numerator = [offset[j][qi] + sum(a * b for a, b in zip(linear[j], assignment)) for j in range(21)]
            if all(v % den == 0 and 0 <= v <= den * bound for v, bound in zip(numerator, upper)):
                expected.append([v // den for v in numerator])
        require(expected == item['states'], 'The row catalogue is not exhaustive in the specified order.')
        columns += [(qi, si, row) for si, row in enumerate(expected)]
    return columns


def verify(certificate_path, catalogue_path):
    cert = json.loads(certificate_path.read_text(encoding='utf-8-sig'))
    document = json.loads(catalogue_path.read_text(encoding='utf-8-sig'))
    require(cert['status'] == 'EXCLUDED_BY_INTEGER_CERTIFICATE', 'No claimed certificate.')
    require(hashlib.sha256(catalogue_path.read_bytes()).hexdigest() == cert['source_catalogue_sha256'], 'Catalogue hash mismatch.')
    template = cert['template']
    columns = check_catalogue(template, document['catalogue'])
    require(cert['column_order'] == [{'rectangle': list(RECTANGLES[q]), 'state_index': s} for q, s, z in columns],
            'Unexpected certificate column order.')
    nongrid = {tuple(q) for q in template['nongrid_edges']}
    vector, constant = [0] * len(columns), 0
    seen = set()
    for is_bound, terms in ((False, cert['equation_multipliers']), (True, cert['upper_bound_multipliers'])):
        for term in terms:
            kind, indices, weight = term['kind'], term['indices'], term['multiplier']
            require(type(weight) is int and (not is_bound or weight >= 0), 'Invalid multiplier.')
            require(all(type(i) is int and 0 <= i < 21 for i in indices), 'Invalid rectangle index.')
            key = kind, tuple(indices), tuple(term.get('normal', []))
            require(key not in seen, 'Duplicate certificate term.')
            seen.add(key)
            if kind == 'four_rows' and len(indices) == 1 and not is_bound:
                i, = indices
                coefficients, target = [int(q == i) for q, s, z in columns], 4
            elif kind == 'block_symmetry' and len(indices) == 2 and not is_bound:
                i, j = indices
                coefficients = [int(q == i) * z[j] - int(q == j) * z[i] for q, s, z in columns]
                target = 0
            elif kind == 'neighbor_moment' and len(indices) == 2 and not is_bound:
                i, j = indices
                coefficients = [z[i] * z[j] + int(q == i) * z[j] for q, s, z in columns]
                target = 64 if i == j else 24 if set(RECTANGLES[i]) & set(RECTANGLES[j]) else 32
            elif kind == 'no_three_edge_rectangle' and len(indices) == 1 and is_bound:
                i, = indices
                require(RECTANGLES[i] in nongrid, 'E3 bound used on a grid rectangle.')
                coefficients, target = [z[i] if q == i else 0 for q, s, z in columns], 4
            elif kind == 'degree_histogram' and len(indices) == 1 and is_bound:
                i, = indices
                require(RECTANGLES[i] in nongrid, 'Degree histogram bound used on a grid rectangle.')
                coefficients = [(2 * int(z[i] == 2) - int(z[i] == 1)) if q == i else 0 for q, s, z in columns]
                target = 0
            elif kind == 'short_column_histogram' and len(indices) == 1 and is_bound:
                # This module uses Python integers only. The admissible planes
                # are regenerated from the finite necessary histogram table.
                from root_component_short_column_histograms import histogram_facets, h_value
                i, = indices
                require(RECTANGLES[i] in nongrid, 'Short-column bound used on a grid rectangle.')
                plane = tuple(term.get('normal', [])) + (term.get('half_upper'),)
                require(plane in histogram_facets(), 'Unproved short-column supporting plane.')
                a, b, c, d = plane
                coefficients = [a*z[i]*int(q == i)
                                + 2*b*int(h_value(RECTANGLES[q], RECTANGLES[i], z[i]) == -3)
                                + 2*c*int(h_value(RECTANGLES[q], RECTANGLES[i], z[i]) == -2)
                                for q, s, z in columns]
                target = 2*d
            else:
                raise ValueError('Unknown certificate term.')
            require(term['upper' if is_bound else 'target'] == target, 'Wrong right-hand side.')
            vector = [a + weight * b for a, b in zip(vector, coefficients)]
            constant += weight * target
    require(vector == cert['nonnegative_variable_coefficients'], 'Incorrect combined coefficient vector.')
    require(constant == cert['constant_upper_bound'] < 0 and min(vector, default=0) >= 0, 'No exact contradiction.')
    return {'status': 'EXACT_CERTIFICATE_VALID', 'row_types': 21, 'row_states': len(columns),
            'free_dimension': len(document['catalogue']['free_coordinates']),
            'equation_terms': len(cert['equation_multipliers']), 'bound_terms': len(cert['upper_bound_multipliers']),
            'coefficient_histogram': dict(sorted(Counter(vector).items())),
            'constant_upper_bound': constant, 'catalogue_exhaustiveness_checked': True,
            'uses_Gram_cover': False, 'uses_prism_budget': False, 'global_conway_exclusion': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate', type=Path, required=True)
    p.add_argument('--catalogue', type=Path, required=True)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    result = verify(a.certificate, a.catalogue)
    if a.output:
        require(not a.output.exists(), 'Output already exists.')
        a.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
