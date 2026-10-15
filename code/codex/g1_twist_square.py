"""A forced square and a 96-to-one interface normalization for G1''.

G1'' = <a,b>, a=(01)(45)(67)(89)(10 11)(12 13),
b=(23)(67)(89)(10 11)(12 13).  This is a local symmetry assumption.
The square reduction uses C1/C2 and T>=0.  It does not construct a graph,
test producer samples, or assert that all admissible structures have it.
Only SymPy is needed.  Labels may be supplied in the producer's order.
"""
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json

import sympy as sp


LABELS = tuple(p for p in combinations(range(14), 2)
               if p[1] != (p[0] ^ 1) and p[0] < 4)
CHARS = ('00', '10', '01', '11')
F_LABELS = ((0, 4), (0, 5), (1, 4), (1, 5))


def letter_action(x, a=0, b=0):
    flip = ((x < 2 and a) or (2 <= x < 4 and b)
            or (4 <= x < 6 and a) or (x >= 6 and a != b))
    return x ^ 1 if flip else x


def act_label(label, a=0, b=0):
    return tuple(sorted(letter_action(x, a, b) for x in label))


def ordered_labels(labels):
    out = tuple(tuple(sorted(p)) for p in labels)
    if len(out) != 44 or set(out) != set(LABELS):
        raise ValueError('Expected the 44 non-mate labels meeting 0,1,2,3.')
    return out


def square_template(labels=LABELS):
    """Return fixed square rows, C2 zeros and four PSD degree cuts.

    Every PSD admissible G1'' structure has a frame relabelling satisfying
    these assignments.  The template alone need not have a completion.
    """
    labels = ordered_labels(labels)
    index = {p: i for i, p in enumerate(labels)}
    square = [index[p] for p in F_LABELS]
    ones = set()

    def add(p, q):
        ones.add(tuple(sorted((index[p], index[q]))))

    for i, j in ((0, 1), (0, 2), (1, 3), (2, 3)):
        add(F_LABELS[i], F_LABELS[j])
    for y in (6, 8, 10, 12):
        positive, negative = ((0, 4), (1, 5)) if y < 10 else ((0, 5), (1, 4))
        add((2, y), positive)
        add((2, y + 1), negative)
        add((3, y), negative)
        add((3, y + 1), positive)
    zeros = {tuple(sorted((i, j))) for i in square for j in range(44)
             if i != j} - ones
    known = sp.zeros(44)
    for i, j in ones:
        known[i, j] = known[j, i] = 1
    forced_extra = set()
    for i, j in combinations(range(44), 2):
        common = len(set(labels[i]) & set(labels[j])) + sum(
            known[i, k] * known[j, k] for k in range(44))
        assert common <= (1 if (i, j) in ones else 2)
        if common == 2 and (i, j) not in zeros:
            assert (i, j) not in ones
            forced_extra.add((i, j))
    degree_cuts = []
    for y in (6, 8, 10, 12):
        root = index[(2, y)]
        others = [index[(2, y+1)], index[(3, y)], index[(3, y+1)]]
        degree_cuts.append(dict(outer_pair=[y, y+1],
            edges=[sorted((root, other)) for other in others], upper_bound=1,
            proof='T minor on q_F and 1_Rpair has determinant 5*(2-d)-1>=0, hence integer d<=1.'))
    return dict(labels=labels, square=square, ones=sorted(ones),
                zeros=sorted(zeros), c2_extra_zeros=sorted(forced_extra),
                internal_degree_cuts=degree_cuts,
                known_adjacency=known)


def geometry_reduction(labels=LABELS):
    """Four affine 10x10 tests after eliminating the normalized square.

    For Gamma on the remaining 40 labels, put Gamma_chi=V_chi^t Gamma
    V_chi/4.  The exact tests are T_offsets[chi]-Gamma_chi>=0 and
    U_offsets[chi]+Gamma_chi>=0.  The full lower rank is three plus the
    sum of the four lower ranks.  No eigensolver or graph search is used.
    """
    template = square_template(labels)
    labels = template['labels']
    index = {p: i for i, p in enumerate(labels)}
    square = template['square']
    remaining = [i for i in range(44) if i not in square]
    unused, orbits = set(remaining), []
    elements = ((0, 0), (1, 0), (0, 1), (1, 1))
    while unused:
        root = min(unused)
        orbit = [index[act_label(labels[root], a, b)] for a, b in elements]
        assert len(set(orbit)) == 4
        unused.difference_update(orbit)
        orbits.append(orbit)
    assert len(orbits) == 10
    bases = {}
    for chi in CHARS:
        a, b = map(int, chi)
        basis = sp.zeros(44, 10)
        for col, orbit in enumerate(orbits):
            for row, (x, y) in zip(orbit, elements):
                basis[row, col] = (-1) ** (a*x+b*y)
        bases[chi] = basis
    grid_modes = {}
    for name, values in [('kappa', (1, 1, 1, 1)),
                         ('q', (1, -1, -1, 1)),
                         ('r', (1, 1, -1, -1)),
                         ('t', (1, -1, 1, -1))]:
        vec = sp.zeros(44, 1)
        for row, value in zip(square, values):
            vec[row, 0] = value
        grid_modes[name] = vec
    grid_by_char = {'00': ['kappa', 'q'], '10': ['r', 't'], '01': [], '11': []}
    gamma = template['known_adjacency']
    k8 = sp.Matrix(44, 44, lambda i, j:
        3*len(set(labels[i]) & set(labels[j]))
        + sum((x ^ 1) in labels[j] for x in labels[i])-2)
    l15 = sp.Matrix(44, 44, lambda i, j:
        4*len(set(labels[i]) & set(labels[j]))
        - sum((x ^ 1) in labels[j] for x in labels[i])+2)
    lower = 3*sp.eye(44)-gamma-k8/8
    upper = 4*sp.eye(44)+gamma-l15/15
    assert lower*grid_modes['kappa'] == sp.zeros(44, 1)
    tdiag = dict(kappa=sp.Rational(0), q=sp.Rational(5),
                 r=sp.Rational(5, 2), t=sp.Rational(5, 2))
    udiag = dict(kappa=sp.Rational(14, 3), q=sp.Rational(2),
                 r=sp.Rational(10, 3), t=sp.Rational(10, 3))
    offsets, couplings = {}, {}
    for chi in CHARS:
        v = bases[chi]
        assert v.T*v == 4*sp.eye(10)
        t = v.T*lower*v/4
        u = v.T*upper*v/4
        couplings[chi] = {}
        for name in grid_by_char[chi]:
            w = grid_modes[name]
            assert (w.T*lower*w)[0]/4 == tdiag[name]
            assert (w.T*upper*w)[0]/4 == udiag[name]
            ct, cu = w.T*lower*v/4, w.T*upper*v/4
            couplings[chi][name] = dict(T=ct, U=cu)
            if tdiag[name]:
                t -= ct.T*ct/tdiag[name]
            else:
                assert ct == sp.zeros(1, 10)
            u -= cu.T*cu/udiag[name]
        offsets[chi] = dict(T=t, U=u)
    # Check only the new geometry decomposition, not any producer graph.
    full_bases = {}
    for chi in CHARS:
        full_bases[chi] = sp.Matrix.hstack(
            *(grid_modes[n] for n in grid_by_char[chi]), bases[chi])
    for chi, other in combinations(CHARS, 2):
        x, y = full_bases[chi], full_bases[other]
        assert x.T*y == sp.zeros(x.cols, y.cols)
        assert x.T*lower*y == sp.zeros(x.cols, y.cols)
        assert x.T*upper*y == sp.zeros(x.cols, y.cols)
    return dict(template=template, remaining=remaining, regular_orbits=orbits,
                character_bases=bases, grid_modes=grid_modes,
                grid_by_character=grid_by_char, T_grid_diagonal=tdiag,
                U_grid_diagonal=udiag, offsets=offsets, couplings=couplings)


def compressed_adjacency(gamma, reduction):
    """Four integer 10x10 adjacency blocks from a supplied invariant Gamma.

    The producer supplies G1'' invariance and the normalized square.  Only
    four entries per reduced entry are needed; there is no full matrix
    multiplication and no recheck of the producer's certification.
    """
    def entry(i, j):
        return gamma[i, j] if isinstance(gamma, sp.MatrixBase) else gamma[i][j]

    elements = ((0, 0), (1, 0), (0, 1), (1, 1))
    orbits = reduction['regular_orbits']
    out = {}
    for chi in CHARS:
        a, b = map(int, chi)
        signs = [(-1)**(a*x+b*y) for x, y in elements]
        out[chi] = sp.Matrix(10, 10, lambda i, j: sum(
            sign*entry(orbits[i][0], vertex)
            for sign, vertex in zip(signs, orbits[j])))
    return out


def matchings(points):
    if not points:
        yield ()
        return
    first = points[0]
    for j in range(1, len(points)):
        for rest in matchings(points[1:j]+points[j+1:]):
            yield tuple(sorted(((first, points[j]),)+rest))


def invariant_matching_list(points, permutation):
    return [m for m in matchings(tuple(points)) if m == tuple(sorted(
        tuple(sorted((permutation[x], permutation[y]))) for x, y in m))]


def projected_matching_counts():
    """Count abstract matching choices after the NEW square constraints.

    This does not enumerate SAT cubes or assert C1/C2 extendability.
    """
    m0 = invariant_matching_list([2, 3]+list(range(6, 14)),
                                 [letter_action(x, b=1) for x in range(14)])
    m2 = invariant_matching_list([0, 1]+list(range(4, 14)),
                                 [letter_action(x, a=1) for x in range(14)])
    forbidden = {(6, 8), (7, 9), (10, 12), (11, 13)}
    allowed = [m for m in m2 if not forbidden.intersection(m)]
    return dict(M0_after_fixed_45=len(m0), M2_before_square_colors=len(m2),
                M2_after_square_colors=len(allowed),
                M2_broken_45_before=sum((4, 5) not in m for m in m2),
                M2_broken_45_after=sum((4, 5) not in m for m in allowed),
                labelled_cube_bound=len(m0)*len(allowed),
                broken_labelled_cube_bound=len(m0)*sum((4, 5) not in m for m in allowed),
                scope='Only invariant matchings and the four new forbidden pairs; no SAT feasibility claimed.')


def interface_orbit_size(template):
    labels = template['labels']
    square = set(template['square'])
    attachments = tuple((labels[i], labels[j]) for i, j in template['ones']
                        if (i in square) != (j in square))
    orbit = set()
    for perm in permutations(range(4)):
        for flips in product((0, 1), repeat=4):
            p = list(range(14))
            for j in range(4):
                for sign in (0, 1):
                    p[6+2*j+sign] = 6+2*perm[j]+(sign ^ flips[j])
            image = tuple(sorted(tuple(sorted((tuple(sorted(p[x] for x in u)),
                                               tuple(sorted(p[x] for x in v)))))
                                 for u, v in attachments))
            orbit.add(image)
    return len(orbit)


def serial(value):
    if isinstance(value, sp.MatrixBase):
        return [[str(v) for v in value.row(i)] for i in range(value.rows)]
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, dict):
        return {key: serial(v) for key, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(v) for v in value]
    return value


def report():
    result = geometry_reduction()
    template = result['template']
    known = template['known_adjacency']
    for i in template['square']:
        for y in range(4):
            count = sum(known[i, j] for j, p in enumerate(LABELS) if y in p)
            assert count == (1 if y in LABELS[i] or (y ^ 1) in LABELS[i] else 2)
    for a, b in ((1, 0), (0, 1)):
        lookup = {p: i for i, p in enumerate(LABELS)}
        p = [lookup[act_label(label, a, b)] for label in LABELS]
        assert all(known[i, j] == known[p[i], p[j]] for i in range(44) for j in range(44))
    # A new weighted invariant matrix tests the fast character projection;
    # it is deliberately only algebraic, not an admissible graph fixture.
    weighted = sp.zeros(44)
    lookup = {p: i for i, p in enumerate(LABELS)}
    for root, orbit in enumerate(result['regular_orbits']):
        for other in result['regular_orbits'][root:]:
            i, j = orbit[0], other[(root+1) % 4]
            if i == j:
                continue
            for a, b in ((0, 0), (1, 0), (0, 1), (1, 1)):
                u = lookup[act_label(LABELS[i], a, b)]
                v = lookup[act_label(LABELS[j], a, b)]
                weighted[u, v] = weighted[v, u] = root+1
    compressed = compressed_adjacency(weighted, result)
    for chi in CHARS:
        v = result['character_bases'][chi]
        assert compressed[chi] == v.T*weighted*v/4
    orbit_size = interface_orbit_size(template)
    assert orbit_size == 96
    counts = projected_matching_counts()
    assert counts['M0_after_fixed_45'] == 81
    assert counts['M2_before_square_colors'] == 331
    assert len(template['ones']) == 20 and len(template['zeros']) == 146
    assert len(template['c2_extra_zeros']) == 8
    for j, orbit in enumerate(result['regular_orbits']):
        if LABELS[orbit[0]][0] == 2 and LABELS[orbit[0]][1] >= 6:
            assert abs(result['couplings']['00']['q']['T'][j]) == 1
            assert result['offsets']['00']['T'][j, j] == sp.Rational(9, 5)
    denominator = sp.ilcm(*(entry.q for chi in CHARS for entry in result['offsets'][chi]['T']))
    return dict(status='EXACT_G1_DOUBLE_PRIME_SQUARE_NORMALIZATION',
                interface_orbit_size=orbit_size,
                full_character_dimensions={'00': 12, '10': 12, '01': 10, '11': 10},
                reduced_character_dimensions={chi: 10 for chi in CHARS},
                T_offset_common_denominator=int(denominator),
                matching_counts=counts, reduction=serial(result),
                component_bounds=dict(
                    grids_on_m_at_most=2,
                    components_on_m_at_most=4,
                    if_M2_does_not_contain_45=dict(grids_on_m_at_most=1,
                                                 components_on_m_at_most=3),
                    proof='The four other exterior pair-orbits have internal degree<=1, so cannot be grids. Non-singleton H_m components use at least two of its six pair-nodes.'),
                formulas={
                    'T_test': 'T_offsets[chi]-V_chi^t Gamma_remaining V_chi/4 >= 0, for every chi',
                    'U_test': 'U_offsets[chi]+V_chi^t Gamma_remaining V_chi/4 >= 0, for every chi',
                    'T_rank': 'rank(T)=3+sum_chi rank(T_reduced[chi])',
                    'T_nullity': 'nullity(T)=1+sum_chi nullity(T_reduced[chi])',
                    'rank30_target': 'sum reduced ranks <=27',
                    'F7_rank28_target': 'If the additional global rank_F7(8T)<=28 bound is imposed, sum reduced ranks over F7 <=25; all T denominators are units mod7'},
                scope='Local G1 double-prime, C1/C2 and T PSD. A necessary normalization and exact spectral reduction, not an exclusion or a graph construction.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = report()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps({key: output[key] for key in (
        'status', 'interface_orbit_size', 'T_offset_common_denominator', 'matching_counts')}))
