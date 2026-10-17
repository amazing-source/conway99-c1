"""Classify all two-mate-star kernel relations by six-vertex connectivity.

For Conway parameters, the two-star adjacency has one internal and one
cross-star neighbour per vertex. The theorem gives rank23-c from the
component count c, without computing or auditing a matrix rank.
"""
import argparse
from pathlib import Path
import json

import sympy as sp


LABELS = tuple((c, x) for c in (0, 1) for x in range(2, 14))


def classify(gamma):
    if any(sum(gamma[i][j] for j in range(24) if LABELS[j][0] == c) != 1
           for i in range(24) for c in (0, 1)):
        raise ValueError('The two-star internal and cross matchings are required.')
    parent = list(range(7))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    auxiliary_edges = set()
    for i in range(24):
        for j in range(i+1, 24):
            if gamma[i][j]:
                a, b = LABELS[i][1]//2, LABELS[j][1]//2
                parent[root(a)] = root(b)
                if a != b:
                    auxiliary_edges.add(tuple(sorted((a, b))))
    components = {}
    for i in range(1, 7):
        components.setdefault(root(i), []).append(i)
    components = sorted(components.values())
    sets = [[p for p in LABELS if p[1]//2 in component] for component in components]
    return dict(
        status='STRUCTURAL_KERNEL_CLASSIFICATION_NO_RANK_RECOMPUTATION',
        auxiliary_edges=sorted(auxiliary_edges), outer_pair_components=components,
        component_count=len(components), closed_sets=sets,
        two_star_nullity_by_theorem=len(components)+1,
        two_star_rank_by_theorem=23-len(components),
        three_star_rank_upper_bound_if_PSD=32-len(components),
        kernel_generators='The two star indicators and the closed-set indicators; their only dependence is sum(closed sets)=sum(two stars).',
        scope='All relations supported on the two mate stars are classified. A relation with new coefficients on the third star is not classified.'
    )


def own_identity_check():
    K = sp.Matrix(24, 24, lambda i, j: sp.Rational(
        3*len(set(LABELS[i]).intersection(LABELS[j]))
        +sum((c ^ 1) in LABELS[j] for c in LABELS[i])-2, 8))
    mate = sp.Matrix(12, 12, lambda i, j: int(j == (i ^ 1)))
    identity = sp.eye(12)
    R = sp.BlockMatrix([[identity, -identity], [-identity, identity]]).as_explicit()/2
    R += sp.BlockMatrix([[identity-mate, identity-mate],
                         [identity-mate, identity-mate]]).as_explicit()/8
    Z = sp.zeros(24, 22)
    for half in (0, 1):
        for i in range(11):
            Z[12*half+i, 11*half+i] = 1
            Z[12*half+11, 11*half+i] = -1
    assert Z.T*(sp.eye(24)-K-R)*Z == sp.zeros(22)
    # Own two-star matchings, with outer pair components {1,6},{2,3,4,5}.
    permutation = {1:6, 6:1, 2:3, 3:4, 4:5, 5:2}
    gamma = [[0]*24 for _ in range(24)]
    index = {p:i for i, p in enumerate(LABELS)}
    for i, (c, x) in enumerate(LABELS):
        j = index[(c, x ^ 1)]
        gamma[i][j] = gamma[j][i] = 1
        if c == 0:
            j = index[(1, 2*permutation[x//2]+x%2)]
            gamma[i][j] = gamma[j][i] = 1
    result = classify(gamma)
    assert result['outer_pair_components'] == [[1, 6], [2, 3, 4, 5]]
    T = 3*sp.eye(24)-sp.Matrix(gamma)-K
    for closed in result['closed_sets']:
        assert T*sp.Matrix([int(p in closed) for p in LABELS]) == sp.zeros(24, 1)
    return dict(status='EXACT_SUM_OF_SQUARES_IDENTITY_PASS',
                own_matching_example_components=result['outer_pair_components'],
                no_peer_rank_recomputed=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gamma')
    parser.add_argument('--output', required=True)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        result = own_identity_check()
    else:
        data = json.loads(Path(args.gamma).read_text(encoding='utf-8-sig'))
        index = {tuple(p):i for i, p in enumerate(data['labels'])}
        gamma = [[data['gamma'][index[p]][index[q]] for q in LABELS] for p in LABELS]
        result = classify(gamma)
        result['input'] = args.gamma
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status', 'outer_pair_components',
                                         'two_star_rank_by_theorem', 'three_star_rank_upper_bound_if_PSD')
                      if k in result}))


if __name__ == '__main__':
    main()
