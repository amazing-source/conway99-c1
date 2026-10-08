"""Finite checks for mass-eight +3 kernel differences (note 183).

This classifies possible supports and audits the cubic/windmill component.
It is not a complete collision bound for the (4,4) family: masses six
and seven and overlaps with previous families still need handling.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations
import json

from seven_vertex_census import ROOT, decode


def four_sets(adj):
    out = []
    for vertices in combinations(range(len(adj)), 4):
        mask = sum(1 << i for i in vertices)
        if sum((adj[i] & mask).bit_count() for i in vertices) == 8:
            out.append((vertices, mask))
    return out


def pair_audit(a, wa, b, wb, cross=()):
    n = len(a)
    graph = list(a)+[row << n for row in b]
    for i, j in cross:
        graph[i] |= 1 << (n+j)
        graph[n+j] |= 1 << i
    sets = four_sets(graph)
    vectors = []
    for W, wm in sets:
        for Y, ym in sets:
            if wm & ym or any(graph[i] & ym for i in W):
                continue
            vectors.append(tuple(int(wm >> i & 1)-int(ym >> i & 1) for i in range(len(graph))))
    kernel = list(wa)+[-w for w in wb]
    pivot = next(i for i, w in enumerate(kernel) if w == 1)
    counts = Counter(tuple(x-v[pivot]*w for x, w in zip(v, kernel)) for v in vectors)
    return sum(c*(c-1)//2 for c in counts.values())


def main():
    source = json.loads((ROOT/'data/codex_order8_census.json').read_text())
    dense = source['families']['minimum_degree_three_types']
    assert len(dense) == 7
    records, cubic = [], []
    for record in dense:
        a = decode(8, record['code'])
        e = sum(row.bit_count() for row in a)//2
        partitions = sum(1 for W, mask in four_sets(a)
                         if sum((a[i] & (255 ^ mask)).bit_count() for i in range(8)
                                if not (mask >> i & 1)) == 8)
        records.append({'code': record['code'], 'edges': e,
                        'degrees': record['degrees'], 'four_four_partitions': partitions})
        if e == 12:
            assert record['degrees'] == [3]*8
            cubic.append((str(record['code']), a, [1]*8, partitions))
    assert sorted(r['edges'] for r in records) == [12, 12, 12, 13, 13, 13, 14]
    windmill = [sum(1 << i for i in range(1, 7))]
    for i in range(1, 7):
        mate = i+1 if i % 2 else i-1
        windmill.append(1 | (1 << mate))
    weighted = [2]+[1]*6
    assert all(sum(weighted[j] for j in range(7) if windmill[i] >> j & 1) == 3*weighted[i]
               for i in range(7))
    assert sum(1 for W, mask in four_sets(windmill) if mask & 1) == 12
    supports = cubic+[('weighted_windmill', windmill, weighted, 12)]
    pairs = []
    for left, right in combinations_with_replacement(supports, 2):
        name, a, wa, ta = left
        other, b, wb, tb = right
        collisions = pair_audit(a, wa, b, wb)
        assert collisions == ta*tb
        pairs.append({'supports': [name, other], 'collision_pairs': collisions})
    assert 88**2/128 == 60.5
    assert 99-61 == 38
    possible_13 = [m for m in range(1, 13)
                   if (88-2*m)**2 <= (99-8*m)*(114-2*m)]
    assert max(possible_13) == 5
    thirteen = [r for r in records if r['edges'] == 13]
    thirteen_pairs = []
    for left, right in combinations_with_replacement(thirteen, 2):
        a, b = decode(8, left['code']), decode(8, right['code'])
        ha = [i for i, row in enumerate(a) if row.bit_count() == 4]
        hb = [i for i, row in enumerate(b) if row.bit_count() == 4]
        counts = [pair_audit(a, [1]*8, b, [1]*8, zip(ha, order)) for order in permutations(hb)]
        expected = left['four_four_partitions']*right['four_four_partitions']//2
        assert set(counts) == {expected}
        thirteen_pairs.append({'supports': [left['code'], right['code']], 'collision_pairs': expected})
    fourteen = next(r for r in records if r['edges'] == 14)
    a = decode(8, fourteen['code'])
    hot = [i for i, row in enumerate(a) if row.bit_count() == 4]
    counts = [pair_audit(a, [1]*8, a, [1]*8, zip(hot, order)) for order in permutations(hot)]
    assert max(counts) == 64
    result = {'binary_support_types': records, 'weighted_support': 'three triangles with centre weight two',
              'number_of_weighted_windmills': 99*35,
              'cubic_windmill_pairs': pairs,
              'thirteen_edge_pairs': thirteen_pairs,
              'fourteen_edge_pair_maximum': max(counts),
              'maximum_class_size': {'cubic_only': 4, 'cubic_and_windmill': 5, 'thirteen_edges': 5},
              'cubic_windmill_collision_bound': '72*C2022000+32*C5683824+128*C5691760+997920',
              'thirteen_edge_collision_bound': '100*C127305925+144*C128354469+64*C245715219',
              'fourteen_edge_collision_bound': '(608/3)*C127242964+160*tau',
              'scope': 'Mass-eight component only; other masses and previous families still need handling.'}
    (ROOT/'data/codex_mass8_kernel_audit.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
