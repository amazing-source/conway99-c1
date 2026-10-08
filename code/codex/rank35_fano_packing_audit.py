"""Independent certificate excluding rank 35 after Fano seed packing.

Imports only Codex's eta expansion and rational-coordinate routines, no
LAB module and no optimisation solver. All assertions use exact integers
or Fraction. The combinatorial packing proof is in note 180.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json

from theta7_audit import basis
from theta7_certificates_audit import family

ROOT = Path(__file__).resolve().parents[2]


def packing_checks():
    # Seven disjoint edges in the neighbourhood of one vertex.
    def independent(S):
        return len({i//2 for i in S}) == len(S)
    triples = [S for S in combinations(range(14), 3) if independent(S)]
    seeds = [S for S in combinations(range(14), 4) if independent(S)]
    assert len(triples) == comb(7, 3)*2**3 == 280
    assert len(seeds) == comb(7, 4)*2**4 == 560
    multiplicities = Counter(T for S in seeds for T in combinations(S, 3))
    assert set(multiplicities) == set(triples)
    assert set(multiplicities.values()) == {8}
    assert sum(multiplicities.values()) == 4*len(seeds)
    # Complement of the Fano incidence matrix: seven positive versus
    # seven negative support vertices, with row size four and overlap two.
    incidence = [{j for j in range(1, 8) if (i & j).bit_count() % 2}
                 for i in range(1, 8)]
    assert all(len(row) == 4 for row in incidence)
    assert all(len(incidence[i] & incidence[j]) == 2 for i, j in combinations(range(7), 2))
    for p0, U in enumerate(incidence):
        pair_to_second = {}
        for pair in combinations(sorted(U), 2):
            candidates = [i for i in range(7) if i != p0 and set(pair) <= incidence[i]]
            assert len(candidates) == 1
            pair_to_second[pair] = candidates[0]
        assert len(set(pair_to_second.values())) == 6
        for T in combinations(sorted(U), 3):
            assert len({pair_to_second[pair] for pair in combinations(T, 2)}) == 3
            assert all(set(T) & incidence[i] for i in range(7) if i != p0)
    return {'independent_triples_per_vertex': 280, 'candidate_seeds_per_vertex': 560,
            'triples_per_seed': 4, 'extending_seeds_per_vertex_at_most': 70,
            'vertices': 99, 'seeds_per_signed_Fano_vector': 7,
            'a7_at_most': 99*70//7,
            'finite_Fano_core_checks': 28}


def certificate_checks():
    A, B = family(34, basis(84))
    rows = {f'a{n}>=0': A[n] for n in (9, 10, 11)}
    for n, lower in ((3, 24948), (4, 2729034)):
        row = list(B[n]); row[0] -= lower
        rows[f'b{n}>={lower}'] = row
    row = [-7*x-8*y for x, y in zip(A[7], A[8])]; row[0] += 55440
    rows['7a7+8a8<=55440'] = row
    row = [-x for x in A[7]]; row[0] += 990
    rows['a7<=990'] = row
    row = [-x for x in B[1]]; row[0] += 88
    rows['b1<=88'] = row
    weights = {'a9>=0': 3110, 'a10>=0': 5474, 'a11>=0': 1328,
               'b3>=24948': 68698, 'b4>=2729034': 3822,
               '7a7+8a8<=55440': 15559, 'a7<=990': 876897, 'b1<=88': 18880582}
    value = [sum(weights[n]*f[i] for n, f in rows.items()) for i in range(8)]
    assert all(w > 0 for w in weights.values())
    assert value == [F(-919306710)]+[F(0)]*7
    # The uniform dual bound keeps all grid and twin losses:
    # +90P -4572rho -48tau >= (90-4572/6-48*5/2)P = -792P.
    coefficient = 90-F(4572, 6)-48*F(5, 2)
    assert coefficient == -792
    b4_lower = 3826746+coefficient*1386
    assert b4_lower == 2729034
    # A deliberately perturbed multiplier must fail the zero-coefficient check.
    changed = [value[i]+rows['a9>=0'][i] for i in range(8)]
    assert any(changed[1:])
    return {'rank_excluded': 35, 'positive_integer_multipliers': weights,
            'affine_rows_in_c1_through_c7': {n: list(map(str, f)) for n, f in rows.items()},
            'weighted_sum': list(map(str, value)), 'negative_constant': -919306710,
            'uniform_b4_bound': int(b4_lower),
            'same_certificate_with_a7_cap1980_constant': -919306710+876897*(1980-990),
            'remaining_ranks': [37, 39, 41, 43]}


def main():
    report = {'packing': packing_checks(), 'certificate': certificate_checks(),
              'scope': 'Fano packing and exact rank-35 exclusion; no exclusion of ranks 37,39,41,43.'}
    path = ROOT/'data/codex_rank35_fano_packing_audit.json'
    path.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Verified: a7 <=', report['packing']['a7_at_most'])
    print('Verified: b4 >=', report['certificate']['uniform_b4_bound'])
    print('Exact contradiction:', report['certificate']['weighted_sum'])
    print('Remaining ranks:', report['certificate']['remaining_ranks'])


if __name__ == '__main__':
    main()
