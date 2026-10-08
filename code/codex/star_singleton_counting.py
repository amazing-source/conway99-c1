"""Exact checks for the forced singleton pair in a hypothetical C1 star.

The general result is a counting lemma, proved in note 218. The artificial
incidence matrices below are boundary examples for counting ONLY: they are
not Green-compatible stars or SRG completions.
"""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np
import sympy as sp

from joint_generic_stars import prepare
from joint_star_propagation import propagate
from two_star_core_ablation import filtered_system
from two_star_single_choice import restrict, replay_original
from two_star_real_projector import exact_green


def boundary_example(singletons, a, edges):
    """24 outside coordinates: singletons, doubletons, then unused points."""
    matrix = np.zeros((10, 24), dtype=np.int64)
    assert sum(a) == singletons
    offset = 0
    for i, count in enumerate(a):
        matrix[i, offset:offset+count] = 1
        offset += count
    assert len(set(tuple(sorted(e)) for e in edges)) == len(edges)
    for col, (i, j) in enumerate(edges, singletons):
        assert i != j
        matrix[i, col] = matrix[j, col] = 1
    assert np.all(matrix.sum(axis=1) == 4)
    targets = matrix.sum(axis=0)
    assert np.array_equal(targets[:singletons], np.ones(singletons, dtype=np.int64))
    assert np.all(targets[singletons:singletons+len(edges)] == 2)
    assert a[0] >= 1 and a[1] >= 1  # Two distinguished apex rows.
    degrees = []
    for w in (0, 1):
        residual = targets-matrix[w]
        d = matrix[:, residual == 1].sum(axis=1)
        others = [j for j in range(10) if j != w]
        assert int(d[others].sum()) == singletons+4-2*a[w]
        assert all(d[j] >= a[j] for j in others)
        degrees.append([int(d[j]) for j in others])
    return {'outside_incidence': matrix.tolist(), 'column_sums': targets.tolist(),
            'original_singleton_counts': a, 'apex_rows': [0, 1],
            'residual_singleton_counts_for_other_rows': degrees,
            'scope': 'abstract incidence counting only; no G or Green compatibility asserted'}


def counting_checks():
    cases = []
    for a0, a1 in product(range(1, 5), repeat=2):
        if a0 == 1:
            reason = 'apex 0 leaves ten unit incidences for nine rows'
        elif a1 == 1:
            reason = 'apex 1 leaves ten unit incidences for nine rows'
        else:
            reason = 'the other apex itself uses at least two residual singleton coordinates'
        cases.append({'apex_singleton_counts': [a0, a1], 'forced_pair_reason': reason})
    # z=1: six singletons, seventeen doubletons, one unused coordinate.
    cycle8 = [(i, i+1) for i in range(2, 9)]+[(9, 2)]
    z1_edges = [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 9)]+cycle8+[(2, 4), (3, 8), (5, 9)]
    z1 = boundary_example(6, [1]*6+[0]*4, z1_edges)
    assert all(max(d) <= 1 for d in z1['residual_singleton_counts_for_other_rows'])
    # z=0, but only the FIRST apex satisfies d<=1. Both apices matter.
    cycle9 = [(i, i+1) for i in range(1, 9)]+[(9, 1)]
    z0_edges = [(0, 7), (0, 8)]+cycle9+[(9, 3), (9, 6), (1, 7), (2, 4), (5, 8)]
    z0 = boundary_example(8, [2]+[1]*6+[0]*3, z0_edges)
    assert max(z0['residual_singleton_counts_for_other_rows'][0]) <= 1
    assert max(z0['residual_singleton_counts_for_other_rows'][1]) >= 2
    return {'sixteen_apex_count_cases': cases, 'z1_boundary_example': z1,
            'z0_one_apex_boundary_example': z0}


def profiles(data_dir):
    result = []
    for name in ('ball5', 'ball9', 'ball12', 'cyclic241'):
        source = json.loads((data_dir/('codex_single_choice_'+name+'.json')).read_text(encoding='utf-8'))
        prepared = prepare(source['adjacency'], 0, 12)
        g, k, commons = prepared[0], prepared[2], prepared[6]
        g2 = g@g
        for center in (0, 12):
            outside = np.arange(36)//12 != center//12
            assert np.all(g2[outside, center] <= 2)
            z = int(np.count_nonzero(g2[outside, center] == 2))
            counts = Counter(map(int, k[outside, center]))
            assert (counts[0], counts[1], counts[2]) == (z, 8-2*z, 16+z)
            histogram = Counter()
            for support in commons:
                w = np.array([int(p in support) for p in range(36)], dtype=np.int64)
                a = int(w[outside & (k[:, center] == 1)].sum())
                assert a >= 1 and np.all(w <= k[:, center])
                t = k[:, center]-w
                assert int(np.count_nonzero(outside & (t == 1))) == 12-2*z-2*a
                histogram[a] += 1
            result.append({'ball': name, 'center': center, 'double_two_step_endpoints': z,
                           'outside_K_counts_0_1_2': [counts[0], counts[1], counts[2]],
                           'apex_original_singleton_count_histogram': dict(sorted(histogram.items()))})
    return result


def within_system(g):
    system = list(filtered_system(prepare(g, 0, 12), 0, 12, 187, 'green'))
    labels = system[1]
    system[-1] = {ij: a if labels[ij[0]][0] == labels[ij[1]][0] else np.ones_like(a)
                  for ij, a in system[-1].items()}
    return system


def verify_hard_leaf(path):
    rec = json.loads(path.read_text(encoding='utf-8'))
    assert rec['centers'] == [0, 12] and rec['apex_index'] == 187
    system = within_system(rec['adjacency'])
    assert rec['common_apex'] == list(system[0])
    arrays, labels = system[2], system[1]
    kept = replay_original(system, rec['base_propagation'], [list(range(len(a))) for a in arrays])
    assert rec['base_propagation']['contradiction'] is None
    pivot, c = rec['first_pivot'], rec['first_candidate']
    assert (pivot, c) == (0, 17) and c in kept[pivot]
    support = np.flatnonzero(arrays[pivot][c]).tolist()
    assert support == rec['first_support'] == [0, 1, 15, 18, 26, 29]
    t = system[4][0]
    points = [p for p in support if p//12 != 0 and t[p] == 1]
    assert points == rec['outside_target_one_points_used'] == [18, 29]
    trial = [d if i != pivot else [c] for i, d in enumerate(kept)]
    first = rec['first_propagation']
    alive = replay_original(system, first, trial)
    assert first['contradiction'] is None and all(alive)
    # A surviving trace alone need not be a propagation fixed point.
    stable = propagate(restrict(system, alive))
    assert stable['trace'] == [] and stable['contradiction'] is None
    second = rec['second_pivot']
    assert second == 3 and labels[second][0] == 0
    assert [x['candidate'] for x in rec['second_leaves']] == alive[second]
    assert len(alive[second]) == 6 and rec['second_survivors'] == []
    for leaf in rec['second_leaves']:
        trial2 = [d if i != second else [leaf['candidate']] for i, d in enumerate(alive)]
        result = leaf['propagation']
        replay_original(system, result, trial2)
        reason = result['contradiction']
        assert reason is not None
        assert all(labels[e['variable']][0] == 0 for e in result['trace'])
        if reason['kind'] == 'empty_domain':
            assert labels[reason['variable']][0] == 0
        else:
            assert reason['kind'] == 'sum_outside_bounds' and reason['side'] == 0
    return {'first_choice_uses_two_singleton_coordinates': True,
            'first_propagation_reaches_nonempty_fixed_point': True,
            'second_choice_leaves_all_contradictory': 6}


def exact_three_shadow_control(data_dir):
    """Audit one LAB triplet in rationals; no completion is asserted."""
    source = json.loads((data_dir/'codex_single_choice_ball12.json').read_text(encoding='utf-8'))
    prepared = prepare(source['adjacency'], 0, 12)
    g, green, k = prepared[:3]
    supports = [[0, 1, 12, 13, 26, 35], [0, 2, 18, 21, 24, 25], [0, 7, 22, 23, 29, 32]]
    n = np.array([[int(p in s) for p in range(36)] for s in supports], dtype=np.int64)
    assert all(tuple(s) in prepared[4][s[1]] for s in supports)
    assert np.array_equal(n@green@n.T % 7, 3*np.ones((3, 3), dtype=np.int64)+3*np.eye(3, dtype=np.int64))
    assert np.all(n.sum(axis=0) <= k[:, 0])
    assert np.all(n.T@n <= k)
    transverse = [p for p in range(12, 36) if g[0, p]]
    assert [int(n[i, transverse].sum()) for i in range(3)] == [1, 1, 0]
    assert not np.any(n[0, transverse] & n[1, transverse])
    counts = []
    for w in (0, 1):
        t = k[:, 0]-n[w]
        counts.append(int(n[2, (t == 1) & (np.arange(36)//12 != 0)].sum()))
    assert max(counts) >= 2
    numerator, denominator = exact_green(prepared)
    gram = sp.Matrix((n@numerator@n.T).tolist())/denominator
    q = 3*sp.eye(3)+sp.ones(3)/12-gram  # All three far adjacencies are zero.
    minors = []
    for size in (1, 2, 3):
        for indices in combinations(range(3), size):
            value = q.extract(indices, indices).det()
            assert value > 0
            minors.append({'indices': list(indices), 'determinant': str(value)})
    return {'supports': supports, 'third_shadow_residual_singleton_counts': counts,
            'projector_gram': [[str(q[i, j]) for j in range(3)] for i in range(3)],
            'positive_principal_minors': minors,
            'scope': 'three shadows pass the stated exact filters; no complete star asserted'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=Path('data'))
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    report = {**counting_checks(), 'input_ball_profiles': profiles(args.data_dir),
              'hard_leaf_check': verify_hard_leaf(args.data_dir/'codex_singleton_hard_leaf187.json'),
              'exact_three_shadow_control': exact_three_shadow_control(args.data_dir)}
    # Canonical JSON makes integer histogram keys comparable after reload.
    report = json.loads(json.dumps(report))
    if args.verify_only:
        assert report == json.loads(args.out.read_text(encoding='utf-8'))
    else:
        args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'profiles': report['input_ball_profiles'], 'hard_leaf': report['hard_leaf_check'],
                      'boundary_examples_verified': 2, 'apex_count_cases': 16,
                      'exact_three_shadow_minors': report['exact_three_shadow_control']['positive_principal_minors']}))


if __name__ == '__main__':
    main()
