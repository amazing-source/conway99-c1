"""A complete abstract Green star extending the three shadows of note 218.

The ten resulting integer vectors have the prescribed mod-7 Gram, the
exact star sum, exact layer sums two, and central coordinate one. Seven
vectors are NOT binary incidence vectors. This is a witness for a weak
algebraic relaxation, not an SRG star or a completion of the input graph.
"""
import argparse
import copy
from itertools import product
import json
from pathlib import Path

import numpy as np

from joint_generic_stars import prepare


SUPPORTS = [[0, 1, 12, 13, 26, 35], [0, 2, 18, 21, 24, 25], [0, 7, 22, 23, 29, 32]]


def rref(matrix):
    a = np.asarray(matrix, dtype=np.int64).copy() % 7
    pivots, row = [], 0
    for col in range(a.shape[1]):
        found = next((i for i in range(row, a.shape[0]) if a[i, col]), None)
        if found is None:
            continue
        a[[row, found]] = a[[found, row]]
        a[row] = a[row]*pow(int(a[row, col]), -1, 7) % 7
        for i in range(a.shape[0]):
            if i != row:
                a[i] = (a[i]-a[i, col]*a[row]) % 7
        pivots.append(col)
        row += 1
        if row == a.shape[0]:
            break
    return a, pivots


def inverse(matrix):
    n = len(matrix)
    reduced, _ = rref(np.column_stack((matrix, np.eye(n, dtype=np.int64))))
    assert np.array_equal(reduced[:, :n], np.eye(n, dtype=np.int64))
    return reduced[:, n:]


def nullspace(matrix):
    a, pivots = rref(matrix)
    free = [i for i in range(a.shape[1]) if i not in pivots]
    basis = np.zeros((a.shape[1], len(free)), dtype=np.int64)
    for j, col in enumerate(free):
        basis[col, j] = 1
        for row, pivot in enumerate(pivots):
            basis[pivot, j] = -a[row, col] % 7
    assert not np.any(np.asarray(matrix)@basis % 7)
    return basis


def diagonalize(matrix):
    a = np.asarray(matrix, dtype=np.int64) % 7
    n = len(a)
    basis = np.eye(n, dtype=np.int64)
    assert np.array_equal(a, a.T)
    for pos in range(n):
        gram = basis.T@a@basis % 7
        pivot = next((i for i in range(pos, n) if gram[i, i]), None)
        if pivot is None:
            pair = next((i, j) for i in range(pos, n) for j in range(i+1, n) if gram[i, j])
            i, j = pair
            basis[:, i] = (basis[:, i]+basis[:, j]) % 7
            pivot = i
        basis[:, [pos, pivot]] = basis[:, [pivot, pos]]
        gram = basis.T@a@basis % 7
        assert gram[pos, pos]
        scale = pow(int(gram[pos, pos]), -1, 7)
        for j in range(pos+1, n):
            basis[:, j] = (basis[:, j]-int(gram[pos, j])*scale*basis[:, pos]) % 7
    gram = basis.T@a@basis % 7
    diag = np.diag(gram)
    assert np.all(diag) and np.array_equal(gram, np.diag(diag))
    inverse(basis)
    return basis, diag


def star_gram():
    adjacency = np.zeros((10, 10), dtype=np.int64)
    for i, j in ((2, 3), (4, 5), (6, 7), (8, 9)):
        adjacency[i, j] = adjacency[j, i] = 1
    return (3*np.eye(10, dtype=np.int64)+3-adjacency) % 7


def lift_exact(residues, target, center=0):
    """Correct row/layer sums by multiples of seven, preserving columns 0:3."""
    lifted = residues.copy()
    for p in range(36):
        delta = int(target[p]-lifted[p].sum())
        assert delta % 7 == 0
        lifted[p, 9] += delta
    for layer in range(3):
        rows = list(range(12*layer, 12*layer+12))
        anchor = next(p for p in rows if p != center)
        for col in range(3, 9):
            delta = 2-int(lifted[rows, col].sum())
            assert delta % 7 == 0
            lifted[anchor, col] += delta
            lifted[anchor, 9] -= delta
        assert np.all(lifted[rows].sum(axis=0) == 2)
    assert np.array_equal(lifted.sum(axis=1), target)
    assert np.all(lifted[center] == 1)
    return lifted


def build(g):
    prepared = prepare(g, 0, 12)
    g, green, k = prepared[:3]
    gram = star_gram()
    # Augment the target star by h, the Green-dual of the central coordinate.
    augmented = np.zeros((11, 11), dtype=np.int64)
    augmented[:10, :10] = gram
    augmented[:10, 10] = augmented[10, :10] = 2
    augmented[10, 10] = 4
    eye = np.eye(11, dtype=np.int64)
    sum_vector = np.r_[np.ones(10, dtype=np.int64), 0]
    change = np.column_stack([sum_vector, eye[:, 0], eye[:, 1], eye[:, 2], eye[:, 10]]+
                             [eye[:, i] for i in range(3, 9)])
    target_gram = change.T@augmented@change % 7
    fixed_gram = target_gram[:5, :5]
    cross = target_gram[:5, 5:]
    complement = (target_gram[5:, 5:]-cross.T@inverse(fixed_gram)@cross) % 7

    # V consists of vectors with zero sum in each layer: dimension 33.
    v_basis = np.zeros((36, 33), dtype=np.int64)
    for layer in range(3):
        for pos in range(11):
            v_basis[12*layer+pos, 11*layer+pos] = 1
            v_basis[12*layer+11, 11*layer+pos] = 6
    blocks = np.array([[int(i//12 == j//12) for j in range(36)] for i in range(36)], dtype=np.int64)
    projection = (np.eye(36, dtype=np.int64)-3*blocks) % 7
    h = projection@(3*np.eye(36, dtype=np.int64)-g)[:, 0] % 7
    fixed_shadows = np.array([[int(p in support) for support in SUPPORTS] for p in range(36)], dtype=np.int64)
    fixed = np.column_stack([k[:, 0]-60]+[fixed_shadows[:, i]-6 for i in range(3)]+[h]) % 7
    assert np.array_equal(fixed.T@green@fixed % 7, fixed_gram)
    assert np.array_equal(projection@fixed % 7, fixed)
    orthogonal = v_basis@nullspace(fixed.T@green@v_basis % 7) % 7
    assert orthogonal.shape == (36, 28)
    ambient_change, ambient_norms = diagonalize(orthogonal.T@green@orthogonal % 7)
    target_change, target_norms = diagonalize(complement)
    orthogonal_diagonal = orthogonal@ambient_change % 7
    diagonal_vectors = np.zeros((36, 6), dtype=np.int64)
    for j, norm in enumerate(target_norms):
        a, b = next((a, b) for a, b in product(range(7), repeat=2)
                    if (ambient_norms[2*j]*a*a+ambient_norms[2*j+1]*b*b-int(norm)) % 7 == 0)
        diagonal_vectors[:, j] = (a*orthogonal_diagonal[:, 2*j]+b*orthogonal_diagonal[:, 2*j+1]) % 7
    realized_complement = diagonal_vectors@inverse(target_change) % 7
    remaining = (fixed@inverse(fixed_gram)@cross+realized_complement) % 7
    all_vectors = np.column_stack((fixed, remaining))@inverse(change) % 7
    assert np.array_equal(all_vectors.T@green@all_vectors % 7, augmented)
    assert np.array_equal(all_vectors[:, 10], h)
    residues = (all_vectors[:, :10]+6) % 7
    lifted = lift_exact(residues, k[:, 0])
    report = {'adjacency': g.tolist(), 'center': 0, 'fixed_supports': SUPPORTS,
              'prescribed_green_gram': gram.tolist(), 'fixed_five_vector_gram': fixed_gram.tolist(),
              'complement_gram': complement.tolist(), 'residue_columns': residues.tolist(),
              'integer_columns': lifted.tolist(),
              'scope': 'integer algebraic relaxation; nonbinary signed vectors, not a C1 star'}
    report['checks'] = verify(report)
    return report


def verify(report):
    assert report['center'] == 0 and report['fixed_supports'] == SUPPORTS
    prepared = prepare(report['adjacency'], 0, 12)
    _, green, k = prepared[:3]
    residues = np.asarray(report['residue_columns'], dtype=np.int64)
    lifted = np.asarray(report['integer_columns'], dtype=np.int64)
    assert residues.shape == lifted.shape == (36, 10)
    assert np.all((residues >= 0) & (residues <= 6))
    assert np.array_equal(lifted % 7, residues)
    gram = star_gram()
    assert report['prescribed_green_gram'] == gram.tolist()
    assert np.array_equal(lifted.T@green@lifted % 7, gram)
    assert np.array_equal(lifted.sum(axis=1), k[:, 0])
    assert np.all(lifted[0] == 1)
    for layer in range(3):
        assert np.all(lifted[12*layer:12*layer+12].sum(axis=0) == 2)
    for i, support in enumerate(SUPPORTS):
        assert lifted[:, i].tolist() == [int(p in support) for p in range(36)]
    nonbinary = np.count_nonzero((lifted != 0) & (lifted != 1), axis=0).tolist()
    assert nonbinary[:3] == [0, 0, 0] and all(nonbinary[3:])
    return {'mod7_norms_and_all_pair_products': 'passed', 'integer_star_sum': 'passed',
            'integer_layer_sums': 'passed', 'central_coordinate_one': 'passed',
            'three_original_binary_shadows': 'preserved', 'nonbinary_entries_per_column': nonbinary,
            'minimum_entry': int(lifted.min()), 'maximum_entry': int(lifted.max())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ball', type=Path, default=Path('data/codex_single_choice_ball12.json'))
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--negative-control', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        report = json.loads(args.out.read_text(encoding='utf-8'))
        assert verify(report) == report['checks']
    else:
        report = build(json.loads(args.ball.read_text(encoding='utf-8'))['adjacency'])
        args.out.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    if args.negative_control:
        invalid = copy.deepcopy(report)
        invalid['integer_columns'][1][4] += 7  # Same mod-7 Gram, broken exact sums.
        try:
            verify(invalid)
        except AssertionError:
            pass
        else:
            raise AssertionError('corrupted integer sum was accepted')
    print(json.dumps(report['checks']))


if __name__ == '__main__':
    main()
