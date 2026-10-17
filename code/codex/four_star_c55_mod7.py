"""Finite-field coupling of the exact G1 c55 non-grid character tables.

The input is our accepted 126-state table, not a producer's seed graph.
All ranks below are exact Gaussian elimination over F7.
"""
import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_g1_c55 import canonical_quotient
from four_star_g1_c55_upper import balanced_rows, schur_t


def rank_mod(matrix, prime=7):
    rows = [[int(x) % prime for x in row] for row in matrix]
    rank = 0
    for col in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][col], -1, prime)
        rows[rank] = [(inverse*x) % prime for x in rows[rank]]
        for i in range(rank+1, len(rows)):
            multiple = rows[i][col]
            if multiple:
                rows[i] = [(x-multiple*y) % prime
                           for x, y in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def signed_adjacency(state, character, row_signs=(1, 1, 1, 1, 1)):
    """Canonical independent row signs, in O,L0..L4,R0..R4 order."""
    s, d = [2*b-1 for b in state[:2]]
    if character == '10':
        left, right = list(range(6)), list(range(6, 11))
    else:
        assert character == '01'
        swap = lambda i: 1-i if i < 2 else i
        left = [0]+[6+swap(i) for i in range(5)]
        right = [1+swap(i) for i in range(5)]
    gamma = [[0]*11 for _ in range(11)]
    gamma[left[0]][left[0]] = gamma[left[1]][left[1]] = s
    gamma[left[0]][left[1]] = gamma[left[1]][left[0]] = -s
    for j in range(5):
        gamma[right[j]][right[j]] = d if j == 1 else -2
        row = balanced_rows(j)[state[2+j]]
        for i, value in enumerate(row):
            gamma[left[i]][right[j]] = gamma[right[j]][left[i]] = value*row_signs[j]
    return gamma


def doubled_t11(gamma10, gamma01, mate_signs=(1, 1, 1, 1, 1)):
    """Return a diagonal congruence of 2*T11.

    Ten independent row signs reduce to five products on the fixed mate
    correction entries. They cannot all be discarded: the correction
    entries are geometric and do not belong to the signed adjacency.
    None means an impossible nonzero internal offset.
    """
    _, degree = canonical_quotient()
    for i in (0, 1, 7):
        if gamma10[i][i] == gamma01[i][i] == 1:
            return None
    matrix = [[0]*11 for _ in range(11)]
    for i in range(11):
        matrix[i][i] = 6 if i == 0 else 5
    for i in range(5):
        matrix[1+i][6+i] = matrix[6+i][1+i] = -mate_signs[i]
    for i, j in product(range(11), repeat=2):
        if degree[i][j] == 1:
            matrix[i][j] -= 2*gamma10[i][j]*gamma01[i][j]
    return matrix


def check_reduction(examples):
    """Check our Fourier/gauge formula against explicit own 44-label lifts.

    These are fixtures of the relaxation; no local SRG admissibility claim.
    In particular no producer's candidate is read or retested.
    """
    import numpy as np
    from sympy.polys.domains import GF
    from sympy.polys.matrices import DomainMatrix
    from four_star_g1_c55 import ORBITS
    from four_star_g1_sectors import character_bases
    from four_star_profile_join import LABELS
    from three_star_column_domains import k8
    _, degree = canonical_quotient()
    _, bases = character_bases()
    bases = {chi: np.array(b, dtype=np.int64) for chi, b in bases.items()}
    k_matrix = np.array([[k8(p, q) for q in LABELS] for p in LABELS], dtype=np.int64)
    fixtures = 0
    for expected, sample in sorted(examples.items()):
        a, b = sample['states']
        signs = sample['mate_signs']
        for r10 in ((1,)*5, (-1, 1, -1, 1, -1), (-1,)*5):
            # These five simultaneous sign changes preserve the five products.
            r01_by_pair = [signs[i]*r10[i] for i in range(5)]
            r01 = [r01_by_pair[1], r01_by_pair[0], *r01_by_pair[2:]]
            ga = signed_adjacency(a, '10', r10)
            gb = signed_adjacency(b, '01', r01)
            gamma = np.zeros((44, 44), dtype=np.int64)
            for i in range(11):
                for j in range(i, 11):
                    if degree[i][j] == 0:
                        continue
                    if degree[i][j] == 1:
                        offset = 2*int(ga[i][j] < 0)+int(gb[i][j] < 0)
                        assert i != j or offset != 0
                        offsets = [offset]
                    else:
                        assert i == j and degree[i][j] == 2
                        offsets = [1, 3] if i < 6 else [2, 3]
                    for u, x in enumerate(ORBITS[i]):
                        for v, y in enumerate(ORBITS[j]):
                            gamma[x, y] = gamma[y, x] = int(u ^ v in offsets)
            assert not np.diag(gamma).any()
            assert np.array_equal(gamma, gamma.T)
            for chi, signed in [('10', ga), ('01', gb)]:
                assert np.array_equal(bases[chi].T@gamma@bases[chi], 4*np.array(signed))
            m8 = 24*np.eye(44, dtype=np.int64)-8*gamma-k_matrix
            diagonal_gauge = np.diag([1]+r01_by_pair+list(r10))
            transformed = diagonal_gauge@(bases['11'].T@m8@bases['11'])@diagonal_gauge
            assert np.array_equal(transformed, 16*np.array(sample['T11_times2']))
            # All cross-character blocks must vanish, not just their diagonals.
            for chi, psi in product(bases, repeat=2):
                if chi != psi:
                    assert not (bases[chi].T@m8@bases[psi]).any()
            assert rank_mod(m8.tolist()) == int(expected)
            fixtures += 1
        reference_rank = DomainMatrix.from_Matrix(sp.Matrix(sample['T11_times2'])).convert_to(GF(7)).rank()
        assert reference_rank == rank_mod(sample['T11_times2'])
    return dict(status='PASS', own_lift_fixtures=fixtures,
                checks=['Fourier normalization against 44-label geometry',
                        'three distinct choices of the five removable row gauges per example',
                        'vanishing cross-character blocks and direct whole-matrix rank',
                        'F7 rank of representative T11 blocks agrees with exact DomainMatrix'],
                no_peer_seed_read=True)


def interpretation():
    return dict(
        theorem='Every canonical G1 c55 non-grid four-star border with T/U PSD has rank_F7(8T_S)>=29.',
        global_consequence='Together with the previously established global bound rank_F7(8T_far)<=28, this excludes a Conway completion of the entire stated local family.',
        global_bound_source='Previously established L4/L23/L22, recalled by Claude in message774; accepted as an existing result, not recomputed here.',
        conditional_scope='G1 invariance of the local 44-label border, both two-star component counts5, non-grid overlap, and T/U PSD. No global G1 action is assumed.',
        does_not_exclude=['the grid-overlap case', 'other component counts',
                          'general four-star borders', 'all Conway graphs or C1'],
        proof=[
            'In the normalized non-grid c55 quotient, T00=w*w^t, w=e_O-e_L0-e_R1, has rank1 over F7. The group has order4, invertible modulo7, so the four character ranks add.',
            'The previously exact joint T/U table has126 states in each of characters10 and01. Elimination of the five right diagonal entries and the forced all-ones kernel gives rank=5+rank(schur_t). All elimination/scaling factors are units modulo7.',
            'Of these126 states,114 have F7 rank10 and12 have rank9. Every rank9 state has s=d=+1. The internal offset in orbit O is nonzero, so its two character signs cannot both be+1; hence both sectors cannot lose rank simultaneously.',
            'For a degree1 orbit block, its character11 adjacency entry is the product of its character10 and01 signs. For ordinary internal degree2 grids its character11 entry is zero. The only invalid internal offsets are the pairs of+1 signs at O,L0,R1.',
            'The126^2 state pairs reduce to4536 after these three internal-offset conditions. Each state has five independent row signs. In character11 a diagonal congruence removes their ten individual values but leaves five products t_i on the fixed L_i,R_i geometric entries. All32 choices must be kept.',
            'Explicitly 2*T11 has initial diagonal(6,5,...,5), mate entries -t_i, and subtracts twice the product of the two canonical signed adjacency entries wherever the quotient degree is1. This formula covers every possible coupled block up to congruence.',
            'Exact elimination of the145152 resulting11x11 integer matrices modulo7 gives T11 ranks only9,10,11. Combined ranks are29:24 cases,30:2334,31:29358,32:113436. Thus rank_F7(8T_S)>=29, already without imposing positivity in character11, the rational rank<=30, or the remaining common-neighbour capacity conditions.',
            'Multiplication by2,8 and the character change of basis uses only units modulo7. A principal submatrix cannot have greater rank than the full far matrix. The accepted global upper bound28 therefore contradicts every case of this local family.'
        ],
        solver_consequence='A global completion branch satisfying all stated local-family conditions may be rejected immediately; the local PSD-only model can still have witnesses. No runtime speedup is claimed.',
        gauge_correction='The preliminary direction message775 omitted five residual sign products. They are included here:4536*32 cases, not just4536.')


def report(catalogue_path):
    data = json.loads(Path(catalogue_path).read_text(encoding='utf-8'))
    states = data['joint_allowed_states']
    assert len(states) == 126
    ranks = [5+rank_mod(schur_t(2*a[0]-1, 2*a[1]-1, a[2:]).tolist())
             for a in states]
    counts, examples = Counter(), {}
    valid = 0
    for i, a in enumerate(states):
        ga = signed_adjacency(a, '10')
        for j, b in enumerate(states):
            gb = signed_adjacency(b, '01')
            if doubled_t11(ga, gb) is None:
                continue
            valid += 1
            for signs in product((-1, 1), repeat=5):
                matrix = doubled_t11(ga, gb, signs)
                rc = rank_mod(matrix)
                key = (ranks[i], ranks[j], rc)
                counts[key] += 1
                total = 1+sum(key)
                examples.setdefault(total, dict(states=[a, b], mate_signs=signs,
                                                T11_times2=matrix))
    output = dict(status='EXACT_F7_COUPLED_CHARACTER_TABLE',
                input_catalogue=str(catalogue_path),
                input_sha256=hashlib.sha256(Path(catalogue_path).read_bytes()).hexdigest(),
                state_count=len(states), single_ranks=dict(Counter(ranks)),
                total_pairs=len(states)**2, valid_internal_offset_pairs=valid,
                residual_sign_states=32, coupled_cases=valid*32,
                rank_counts=[dict(T10=a, T01=b, T11=c, total=1+a+b+c, count=n)
                             for (a, b, c), n in sorted(counts.items())],
                exact_minimum= min(examples),
                examples_by_total=examples)
    output['own_reduction_checks'] = check_reduction(examples)
    output.update(interpretation())
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalogue', default='data/codex_three_star_completion_20261014/four_star_g1_c55_756/upper_character_catalogue.json')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report(args.catalogue)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'examples_by_total'}))
