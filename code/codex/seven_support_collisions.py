"""Finite audits of collision losses for house/bowtie minus a far edge.

The ambient kernel relations are assumed only for genuine twin supports;
these finite models count the representations attached to each such pair.
They do not assert existence of an SRG(99,14,1,2).
"""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from joint_theta_small_shells import decode

ROOT = Path(__file__).resolve().parents[2]


def edges(adj, S):
    mask = sum(1 << i for i in S)
    return sum((adj[i] & mask).bit_count() for i in S)//2


def joined(adj, extra=None):
    n = len(adj)
    out = list(adj)+[row << n for row in adj]
    if extra is not None:
        out.append(0)
        for v in extra:
            out[v] |= 1 << (2*n)
            out[-1] |= 1 << v
    return out


def representatives(adj, p, q, internal_edges, filter_vector=None):
    n = len(adj)
    answer = set()
    for W in combinations(range(n), p):
        if edges(adj, W) != internal_edges:
            continue
        mask = sum(1 << i for i in W)
        far = [i for i in range(n) if not (mask >> i & 1) and not (adj[i] & mask)]
        for Y in combinations(far, q):
            if edges(adj, Y) != int(q == 2):
                continue
            v = [0]*n
            for i in W:
                v[i] = 1
            for i in Y:
                v[i] = -1
            if filter_vector is not None and not filter_vector(v):
                continue
            answer.add(tuple(v)); answer.add(tuple(-x for x in v))
    return answer


def quotient(v, relation):
    pivot = next(i for i, x in enumerate(relation) if x == 1)
    return tuple(x-v[pivot]*w for x, w in zip(v, relation))


def loss(vectors, relation):
    counts = Counter(quotient(v, relation) for v in vectors)
    return {'representatives': len(vectors), 'images': len(counts),
            'loss': len(vectors)-len(counts),
            'unordered_collision_pairs': sum(c*(c-1)//2 for c in counts.values()),
            'multiplicity_histogram': dict(Counter(counts.values()))}


def main():
    prism = tuple(sum(1 << j for j in range(6) if i != j and
                      (i//3 == j//3 or i % 3 == j % 3)) for i in range(6))
    two = joined(prism)
    relation = [1]*6+[-1]*6
    new = representatives(two, 5, 2, 6)
    old = representatives(two, 4, 1, 4)
    new_images = set(quotient(v, relation) for v in new)
    old_images = set(quotient(v, relation) for v in old)
    assert len(new) == len(new_images) == len(old) == len(old_images) == 216
    assert len(new_images & old_images) == 216
    # One exterior vertex sees one rung of each twin prism.
    double = joined(prism, (0, 3, 6, 9))
    double_case = loss(representatives(double, 5, 2, 6, lambda v: v[-1] == 1), relation+[0])
    assert double_case['unordered_collision_pairs'] == 32
    # One exterior vertex sees one point of each twin prism.
    single = joined(prism, (0, 6))
    single_case = loss(representatives(single, 5, 2, 6, lambda v: v[-1] == -1), relation+[0])
    assert single_case['unordered_collision_pairs'] == 2
    total_twin_loss_bound = 216+3*32+60*2
    assert total_twin_loss_bound == 432
    # Unique seven-vertex support with minimum degree three, independently
    # found by the complete order-seven census.
    source = json.loads((ROOT/'data/codex_seven_vertex_census.json').read_text())
    dense = [r for r in source['counts'] if min(r['degrees']) >= 3]
    assert len(dense) == 1 and dense[0]['degrees'] == [3]*6+[4]
    H = decode(7, dense[0]['code'])
    center = next(i for i, row in enumerate(H) if row.bit_count() == 4)
    two_H = joined(H)
    two_H[center] |= 1 << (7+center)
    two_H[7+center] |= 1 << center
    H_case = loss(representatives(two_H, 5, 2, 6), [1]*7+[-1]*7)
    assert H_case['unordered_collision_pairs'] == 98
    # Five-sets with six edges in the grid and the complementary four fibres.
    grid = tuple(sum(1 << j for j in range(9) if i != j and
                     (i//3 == j//3 or i%3 == j%3)) for i in range(9))
    grid_types = Counter()
    for W in combinations(range(9), 5):
        if edges(grid, W) != 6:
            continue
        S = tuple(i for i in range(9) if i not in W)
        assert edges(grid, S) == 4
        far_fibre_edges = 4*5+10*edges(grid, S)+20*(6-edges(grid, S))
        assert far_fibre_edges == 100
        mask = sum(1 << i for i in W)
        kind = 'bowtie' if max((grid[i] & mask).bit_count() for i in W) == 4 else 'house'
        grid_types[kind] += 2*far_fibre_edges
    assert grid_types == {'bowtie': 1800, 'house': 7200}
    report = {'old_vs_new_per_twin_prism_pair': 216,
              'common_positive_vertex_degree_two': double_case,
              'common_negative_vertex_degree_one': single_case,
              'loss_bound_per_twin_prism_pair': total_twin_loss_bound,
              'seven_support_pair': H_case, 'signed_grid_collisions': dict(grid_types),
              'inequality': 'b4 >= 5939010+66P+14H-13572rho-480tau-98Omega',
              'scope': 'Safe collision-pair subtraction; not a claim that every subtraction is disjoint or sharp.'}
    (ROOT/'data/codex_seven_support_collisions.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
