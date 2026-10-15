"""General c55 non-grid borders as 18 cores and 19 S4 matchings.

No G1 symmetry is imposed. The old G1 family is the diagonal-mode subcase.
The global no-nine-vertices-with-17-edges theorem and the existing two-star
component theorem are inputs. This is NOT LAB's later conjecture named N9
(an upper bound on four-star nullity), which has been refuted.
"""
import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_c55_general_overlap import CORE, TWO_LABELS, two_star_catalogue
from four_star_g1_c55 import ORBITS, canonical_quotient
from four_star_profile_join import LABELS, upper_entry
from three_star_column_domains import k8

PAIRS12 = tuple(combinations(range(12), 2))
PERMUTATIONS = tuple(permutations(range(4)))
WALSH = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], dtype=np.int64)


def decode(code):
    gamma = [[0]*12 for _ in range(12)]
    for bit, (i, j) in enumerate(PAIRS12):
        gamma[i][j] = gamma[j][i] = (int(code) >> bit) & 1
    return gamma


def core_types(source):
    data = json.loads(Path(source).read_text(encoding='utf-8'))
    catalogue = [r for r in two_star_catalogue() if r['overlap_edges'] == 2]
    ix = {p: i for i, p in enumerate(TWO_LABELS)}
    mirror = {0: 2, 1: 3, 2: 0, 3: 1, 4: 6, 5: 7, 6: 4, 7: 5,
              **{i: i for i in range(8, 14)}}
    ri = {tuple(sorted(mirror[x] for x in p)): i for i, p in enumerate(TWO_LABELS)}
    ci = {p: i for i, p in enumerate(CORE)}
    group = []
    for flips, swap in product(product((0, 1), repeat=4), (0, 1)):
        def letter(x):
            y = x ^ flips[x//2]
            return mirror[y] if swap else y
        group.append([ci[tuple(sorted(letter(x) for x in p))] for p in CORE])
    counts = Counter()
    signatures = set()
    for record in data['certificates']:
        assert record['T']['psd'] and record['U']['psd'] and record['rank_T'] == 10
        left = catalogue[record['left_index']]['gamma']
        right = catalogue[record['right_index']]['gamma']
        gamma = [[0]*12 for _ in range(12)]
        for i, p in enumerate(CORE):
            for j, q in enumerate(CORE):
                if p in ix and q in ix:
                    gamma[i][j] = left[ix[p]][ix[q]]
                if p in ri and q in ri:
                    gamma[i][j] = right[ri[p]][ri[q]]
        assert not record['cross_edges']
        for cell in (range(4), range(4, 8), range(8, 12)):
            assert all(sum(gamma[i][j] for j in cell) == 1 for i in cell)
        raw = sum(gamma[i][j] << bit for bit, (i, j) in enumerate(PAIRS12))
        signatures.add(raw)
        canonical = min(sum(gamma[p[i]][p[j]] << bit for bit, (i, j) in enumerate(PAIRS12))
                        for p in group)
        counts[canonical] += 1
    assert len(signatures) == 128 and len(counts) == 18
    return [dict(code=str(code), labelled_core_count=count, gamma=decode(code))
            for code, count in sorted(counts.items())]


def make_gamma(core, choices):
    """Make a quotient lift; C1/C2 and PSD are still required separately."""
    _, degree = canonical_quotient()
    index = {p: i for i, p in enumerate(LABELS)}
    gamma = np.zeros((44, 44), dtype=np.int64)
    for i, p in enumerate(CORE):
        for j, q in enumerate(CORE):
            gamma[index[p], index[q]] = core[i][j]
    # The eight singleton components are genuine grids.
    for orbit_index, orbit in enumerate(ORBITS):
        if orbit_index in (0, 1, 7):
            continue
        for i, j in combinations(orbit, 2):
            gamma[i, j] = gamma[j, i] = int(len(set(LABELS[i]) & set(LABELS[j])) == 1)
    unknown = [(i, j) for i in range(1, 6) for j in range(6, 11) if degree[i][j]]
    assert len(unknown) == len(choices) == 19
    for (i, j), choice in zip(unknown, choices):
        for u, v in enumerate(PERMUTATIONS[choice]):
            gamma[ORBITS[i][u], ORBITS[j][v]] = gamma[ORBITS[j][v], ORBITS[i][u]] = 1
    return gamma


def add_completion_counts(model, rows_by_label):
    """Necessary completion counts for this canonical family, without G1.

    Establish the c55 non-grid quotient and PSD hypotheses before use.
    The older bound on profiles breaking h is deliberately not part of this
    adapter: its proof requires G1, whereas these counts do not.
    """
    missing = [p for p in combinations(range(4, 14), 2) if p[1] != (p[0] ^ 1)]
    if set(rows_by_label) != set(missing) or any(len(row) != 44 for row in rows_by_label.values()):
        raise ValueError('Exactly the40 canonical missing labels and44 entries per row are required.')
    counts = [[] for _ in range(3)]
    for u in missing:
        row = rows_by_label[u]
        used_pairs = {x//2-2 for x in u}
        nO = model.NewIntVar(0, 1 if used_pairs & {0, 1} else 2, 'c55_general_nO_%d_%d' % u)
        model.Add(nO == sum(row[i] for i in ORBITS[0]))
        for side in range(2):
            active = side  # L0 and R1
            for pair in range(5):
                total = sum(row[i] for i in ORBITS[1+5*side+pair])
                if pair == active:
                    model.Add(total+nO == 2-int(pair in used_pairs))
                else:
                    model.Add(total == 1-int(pair in used_pairs))
        for value in range(3):
            flag = model.NewBoolVar('c55_general_nOeq%d_%d_%d' % (value, *u))
            model.Add(nO == value).OnlyEnforceIf(flag)
            model.Add(nO != value).OnlyEnforceIf(flag.Not())
            counts[value].append(flag)
    for indicators, total in zip(counts, (10, 24, 6)):
        model.Add(sum(indicators) == total)
    return dict(overlap_histogram=[10, 24, 6], component_count_equations=400,
                symmetry_assumption=None, symmetry_breaking_bound_imposed=False)


def report(source):
    cores = core_types(source)
    _, degree = canonical_quotient()
    b0 = np.zeros((44, 11), dtype=np.int64)
    bs = np.zeros((44, 33), dtype=np.int64)
    for j, orbit in enumerate(ORBITS):
        b0[orbit, j] = 1
        bs[orbit, 3*j:3*j+3] = WALSH
    assert np.array_equal(bs.T@bs, 4*np.eye(33, dtype=np.int64))
    assert not (b0.T@bs).any()
    m0 = np.array([[24*int(i == j)-k8(p, q) for j, q in enumerate(LABELS)]
                   for i, p in enumerate(LABELS)], dtype=np.int64)
    n0 = np.array([[upper_entry(p, q, 0, i == j) for j, q in enumerate(LABELS)]
                   for i, p in enumerate(LABELS)], dtype=np.int64)
    raw_t, raw_u = bs.T@m0@bs, bs.T@n0@bs
    assert not (raw_t % 16).any() and not (raw_u % 20).any()
    correction_t, correction_u = raw_t//16, raw_u//20
    tables = []
    for permutation in PERMUTATIONS:
        p = np.zeros((4, 4), dtype=np.int64)
        p[range(4), permutation] = 1
        raw = WALSH.T@p@WALSH
        assert not (raw % 4).any()
        signed = raw//4
        assert np.array_equal(signed.T@signed, np.eye(3, dtype=np.int64))
        assert all(np.count_nonzero(row) == 1 for row in signed)
        assert np.prod(signed[signed != 0]) == 1
        tables.append(dict(permutation=permutation, standard_action=signed.tolist(),
                           diagonal_mode_action=bool(np.array_equal(signed, np.diag(np.diag(signed))))))
    assert sum(r['diagonal_mode_action'] for r in tables) == 4
    # Geometric quotient and Fourier formula checked on new algebraic lifts.
    for number, core in enumerate(cores):
        gamma = make_gamma(core['gamma'], [(number+7*i) % 24 for i in range(19)])
        assert np.array_equal(gamma, gamma.T) and not np.diag(gamma).any()
        for i, orbit in enumerate(ORBITS):
            for j, other in enumerate(ORBITS):
                assert all(sum(gamma[u, v] for v in other) == degree[i][j] for u in orbit)
        m8 = m0-8*gamma
        assert not (b0.T@m8@bs).any()
        assert np.array_equal(b0.T@m8@b0, 32*np.array(canonical_quotient()[0]))
        adjacency_standard = (bs.T@gamma@bs)//4
        assert not ((bs.T@gamma@bs) % 4).any()
        assert np.array_equal(bs.T@m8@bs//16, correction_t-2*adjacency_standard)
    drop = [0, 1]  # O coordinates10 and01 of the two forced star differences.
    retained = [i for i in range(33) if i not in drop]
    return dict(status='EXACT_C55_NON_GRID_S4_LIFT_WITHOUT_G1',
                labels=LABELS, fibres=ORBITS, core_labels=CORE,
                quotient_adjacency_degrees=degree, core_types=cores,
                number_core_types=18, labelled_cores=128,
                unknown_matching_blocks=[[i, j] for i in range(1, 6) for j in range(6, 11) if degree[i][j]],
                permutation_table=tables, standard_basis=bs.tolist(),
                T_standard_times2_geometric_correction=correction_t.tolist(),
                U_standard_times3_geometric_correction=correction_u.tolist(),
                forced_star_coordinates_to_remove=drop, quotient_coordinates=retained,
                own_checks='PASS:128 distinct cores,18 canonical types,24 exact S4 actions,18 new quotient-lift/Fourier fixtures; no peer seed read.',
                proof=[
                    'For c=5 the six mate pairs split into one component of size2 and four singleton components. A singleton is a genuine grid by the existing C1/C2 component result. A non-grid overlap belongs to the size2 component on each side.',
                    'Let O be the overlap and LA,RB the active exterior fibres. Their indicator vectors satisfy T(1_O+1_LA)=T(1_O+1_RB)=0. The eight ordinary grid indicators are also in the kernel. The compression on the eleven fibre indicators is therefore t*w*w^t, w=e_O-e_LA-e_RB, t=2-e(O)/2.',
                    'The LA,RB entry is 1-[A=B]-e(LA,RB)/4=t. Thus A!=B and0<t<=1, so e(O)=2 or3. The case e(O)=3 makes the root, its four selected neighbours and O a nine-vertex set with17 edges, forbidden by the established global no-nine-vertices-with17-edges theorem (LAB635). This input is distinct from the later refuted nullity conjecture also called N9.',
                    'For e(O)=2, enumerate the3*3*24 active two-star matching/permutation choices. Of122 locally admissible connected patterns,36 have e(O)=2. Pairing two such patterns with common O, the required kernel equations and C2 leave128 distinct12-label cores. All have O,LA,RB internally perfect matched and all have T/U PSD on the core; these are necessary tests, not full borders.',
                    'Independent flips of the four mate pairs and exchange of the two central lines together with A/B form32 label symmetries. Canonicalization leaves18 core types. The kernel equations of the eight ordinary grids force every remaining nonzero cross block to be a4x4 permutation matrix: exactly19 such blocks. The whole11-fibre quotient equals the former c55 quotient, without assuming G1.',
                    'Each4x4 permutation fixes the constant vector and acts on the other three Walsh directions as a signed3x3 permutation with sign product+1. There are24 possibilities: four sign choices for each of six permutations of the modes. The old G1 action restricts to the four diagonal possibilities and also imposes its core invariance; that restriction is not made here.',
                    'The constant11-dimensional sector has T rank1. The remaining33-dimensional sector has2T=C_T-2*Gamma_standard and3U=C_U+3*Gamma_standard. Complete central-star equations give two known kernel vectors, with unit pivots in the O coordinates10/01. Removing these yields principal31x31 tests equivalent to positivity and preserving the nontrivial rank.',
                    'For an admissible c55 non-grid border, rank(T44)=1+rank(T31), and its mixed-relation count is31-rank(T31). A Conway completion requires rational rank(T31)<=29 and rank_F7(2T31)<=27. Four mixed relations mean rational rank(T31)<=27.',
                    'The forced core perfect matchings and quotient give z=T_far*1_O, extended by0 on the root ball, with values+1 on O,-1 on LA and RB,0 on the other32 labels, and1-n_O(u) on the40 missing labels. Kernel counts imply n_O<=1 when u uses A or B, otherwise n_O<=2. Thus z is an integral -4 eigenvector of squared norm28 with14 plus and14 minus signs. The40 missing counts n_O=0,1,2 occur exactly10,24,6 times, as in the earlier G1 result.'],
                global_consequences=dict(signed_eigenvector=dict(eigenvalue=-4, positive_entries=14, negative_entries=14, squared_norm=28),
                                         overlap_neighbour_histogram={'0': 10, '1': 24, '2': 6}),
                remaining_conditions='The19 permutations must jointly satisfy the full central-star equations, all common-neighbour capacities, both Gram positivity tests and global completion constraints.',
                limitations=['No full44-label PSD border constructed in this report.',
                             '18*24^19 is only a finite parameterization, not an affordable exhaustive computation claim.',
                             'The earlier F7 exclusion applies when the full G1 symmetry holds. A core with that symmetry alone is not enough.',
                             'The29 exterior symmetry-breaking bound still requires G1 and is not extended by this argument.',
                             'The general c55 non-grid family and Conway remain open.'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--core-source', default='data/codex_local_global_20261015/c55_general_overlap2.json')
    p.add_argument('--output', required=True)
    a = p.parse_args()
    result = report(a.core_source)
    path = Path(a.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'number_core_types', 'labelled_cores', 'own_checks', 'global_consequences', 'limitations')}))
