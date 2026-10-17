"""An exact fractional feasible point, not a Conway graph or binary boundary.

This specializes the previously derived forced operator E0. It shows that
the natural star/cap/PSD relaxation has feasible points of forbidden rank31.
"""
import argparse
from itertools import combinations
from pathlib import Path
import json

import numpy as np
import sympy as sp


def construct():
    far = [p for p in combinations(range(14), 2) if (p[0] ^ 1) != p[1]]
    selected = [i for i, p in enumerate(far) if set(p).intersection((0, 1, 2))]
    labels = [far[i] for i in selected]
    intersection = np.array([[len(set(p).intersection(q)) for q in far] for p in far], dtype=np.int64)
    mates = np.array([[sum((c ^ 1) in q for c in p) for q in far] for p in far], dtype=np.int64)
    gamma10 = 2-intersection-mates
    K8 = 3*intersection+mates-2
    projector120 = 120*np.eye(84, dtype=np.int64)-11*intersection-mates+2
    incidence = np.array([[int(c in p) for p in far] for c in range(14)], dtype=np.int64)
    assert np.array_equal(projector120 @ projector120, 120*projector120)
    assert not np.any(incidence @ projector120)
    assert np.array_equal(120*np.eye(84, dtype=np.int64)-4*gamma10-5*K8, projector120)
    assert int(np.trace(projector120)) == 120*70
    block10 = gamma10[np.ix_(selected, selected)]
    B10 = np.zeros((49, 49), dtype=np.int64)
    for c in range(14):
        B10[0, 1+c] = B10[1+c, 0] = 10
        B10[1+c, 1+(c ^ 1)] = 10
    for i, pair in enumerate(labels):
        for c in pair:
            B10[15+i, 1+c] = B10[1+c, 15+i] = 10
    B10[15:, 15:] = block10
    cap_slack100 = 200-10*B10-B10@B10
    np.fill_diagonal(cap_slack100, 10000)
    assert cap_slack100.min() >= 0
    assert B10.sum(axis=1).max() <= 140
    for c in (0, 1, 2):
        column_set = [i for i, pair in enumerate(labels) if c in pair]
        for i, pair in enumerate(labels):
            assert block10[i, column_set].sum() == 10*(2-int(c in pair)-int((c ^ 1) in pair))
    T40 = projector120[np.ix_(selected, selected)]
    exact_rank = int(sp.Matrix(T40.tolist()).rank())
    assert exact_rank == 31
    # The factor120/40=3 gives T=3Pi, with 0<=T<=3I on the full84 labels.
    return {
        'status': 'EXACT_FRACTIONAL_WITNESS_NOT_A_GRAPH',
        'labels': labels,
        'gamma_numerator': block10.tolist(),
        'gamma_denominator': 10,
        'T_numerator': T40.tolist(),
        'T_denominator': 40,
        'spectral_rank': exact_rank,
        'required_rank_for_actual_Conway_boundary': 30,
        'exact_checks': {
            'three_star_counts': True,
            'all_local_caps_B_squared_le_2_minus_B': True,
            'minimum_cap_slack_numerator': int(cap_slack100.min()),
            'minimum_far_cap_slack_numerator': int(cap_slack100[15:, 15:].min()),
            'cap_slack_denominator': 100,
            'degrees_at_most_14': True,
            'Pi_squared_equals_Pi': True,
            'root_incidence_times_Pi_zero': True,
            'T_equals_3Pi': True,
            'spectral_bound': '0 <= T_SS <= 3I <= 7I',
            'full_Pi_rank': 70
        },
        'proof': [
            'For root incidence D, DD^t=11I+J-B_matching, with inverse(11I+B_matching)/120-J/240.',
            'Gamma0_yz=(2-intersection(y,z)-mate_incidence(y,z))/10 specializes E0.',
            'Pi=I-D^t(DD^t)^(-1)D and T0=3I-Gamma0-K=3Pi. An orthogonal projector is PSD and bounded by I.',
            'A kernel vector of Pi_SS extends by zero to an element D^t f supported on S.',
            'For every outside pair{c,d}, f_c+f_d=0. The outside-pair graph on the11 other letters is connected and contains an odd cycle, so all those11 f_c are zero.',
            'The three centre weights are unrestricted, giving nullity3 and rank34-3=31.'
        ],
        'scope': [
            'This is a concrete specialization of the existing forced spectral operator, not a new SRG.',
            'It satisfies the natural announced continuous star/common-neighbour-cap/PSD conditions, including the upper PSD bound.',
            'A PSD cutting-plane scheme cannot reject this point using PSD cuts alone. Additional constraints may define a smaller relaxation.',
            'The integrality requirement and the extra kernel relation needed for rank<=30 remain unresolved.',
            'This fractional matrix is deliberately not an input accepted by the binary column-domain preprocessor.'
        ]
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = construct()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status', 'spectral_rank', 'exact_checks')}))


if __name__ == '__main__':
    main()
