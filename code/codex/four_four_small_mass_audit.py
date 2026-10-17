"""Finite collision counts for the (4,4), norm-eight family.

Kernel supports are hypothetical genuine twin supports in SRG(99,14,1,2).
Finite models count representation pairs, not ambient graph existence.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations
from math import isqrt
import json

from seven_vertex_census import ROOT, decode
from mass8_kernel_audit import four_sets
from seven_support_collisions import joined


def admissible(adj):
    return all((adj[i] & adj[j]).bit_count() <= (1 if adj[i] >> j & 1 else 2)
               for i, j in combinations(range(len(adj)), 2))


def extend(adj, masks, edge=0):
    out = list(adj)
    for mask in masks:
        n = len(out)
        for i in range(n):
            if mask >> i & 1:
                out[i] |= 1 << n
        out.append(mask)
    if edge:
        i, j = len(out)-2, len(out)-1
        out[i] |= 1 << j; out[j] |= 1 << i
    return out


def family(adj, p):
    n = len(adj)
    if p == 4:
        subsets = [(W, mask, 4) for W, mask in four_sets(adj)]
    else:
        subsets = []
        for W in combinations(range(n), p):
            mask = sum(1 << i for i in W)
            edges = sum((adj[i] & mask).bit_count() for i in W)//2
            subsets.append((W, mask, edges))
    answer = set()
    for W, wm, ew in subsets:
        for Y, ym, ey in subsets:
            if wm & ym or ew+ey < 3*p-4:
                continue
            cross = sum((adj[i] & ym).bit_count() for i in W)
            if ew+ey-cross == 3*p-4:
                answer.add(tuple(int(wm >> i & 1)-int(ym >> i & 1) for i in range(n)))
    return answer


def pairs(new, old, delta, same=False):
    directions = [delta] if same else [delta, [-x for x in delta]]
    return sum(tuple(x-y for x, y in zip(v, d)) in old for v in new for d in directions)


def probe_old(prism, D):
    out = {}
    graph = joined(prism)
    new = family(graph, 4)
    out['old_two_two_mass6'] = pairs(new, family(graph, 2), [1]*6+[-1]*6)
    assert out['old_two_two_mass6'] == 162
    for name, neighbours in [('single', [0, 6]), ('double', [0, 3, 6, 9])]:
        a = extend(graph, [sum(1 << i for i in neighbours)])
        count = pairs(family(a, 4), family(a, 3), [1]*6+[-1]*6+[0])
        out[f'old_three_three_mass6_{name}'] = count
    assert out['old_three_three_mass6_single'] == 12
    assert out['old_three_three_mass6_double'] == 24
    out['old_three_three_mass6_total'] = 60*12+3*24
    c = next(i for i, row in enumerate(D) if row.bit_count() == 4)
    a = joined(D)
    a[c] |= 1 << (c+7); a[c+7] |= 1 << c
    count = pairs(family(a, 4), family(a, 3), [1]*7+[-1]*7)
    out['old_three_three_mass7'] = count
    return out


def probe_prism_common_pair(prism):
    graph = joined(prism)
    patterns = [('Z', 0, 24)]
    patterns += [(f'A{i}', sum(1 << j for j in [i, i+3, i+6, i+9]), 1) for i in range(3)]
    patterns += [(f'B{i}_{j}', (1 << i)+(1 << (6+j)), 1 if i % 3 == j % 3 else 2)
                 for i in range(6) for j in range(6)]
    observed = Counter()
    cases = 0
    for left, right in combinations_with_replacement(patterns, 2):
        if left == right and left[2] < 2:
            continue
        for edge in (0, 1):
            a = extend(graph, [left[1], right[1]], edge)
            if not admissible(a):
                continue
            vectors = family(a, 4)
            count = pairs(vectors, vectors, [1]*6+[-1]*6+[0, 0], same=True)
            d1 = (left[1] & 63).bit_count(); d2 = (right[1] & 63).bit_count()
            key = (min(d1, d2), max(d1, d2), edge)
            observed[key] = max(observed[key], count)
            cases += 1
            expected = 0
            if key == (0, 2, 1): expected = 2
            if key == (1, 2, 0):
                single = left[1] if d1 == 1 else right[1]
                double = right[1] if d1 == 1 else left[1]
                expected = 2 if single & double == single else 0
            if d1 == d2 == 1:
                u, v = [(m & 63).bit_length()-1 for m in [left[1], right[1]]]
                x, y = [(m >> 6).bit_length()-1 for m in [left[1], right[1]]]
                if edge:
                    if u == v: expected = 6 if prism[x] >> y & 1 else 0
                    elif x == y: expected = 6 if prism[u] >> v & 1 else 0
                    else: expected = 2 if (prism[u] >> v & 1) and (prism[x] >> y & 1) else 0
                else:
                    expected = 2 if u//3 != v//3 and x//3 != y//3 else 0
            if key == (2, 2, 0): expected = 8
            assert count == expected, (left[0], right[0], edge, count, expected)
    return {'checked_local_patterns': cases,
            'maxima_by_degrees_and_edge': {str(k): v for k, v in sorted(observed.items())}}


def probe_D_common_point(D):
    c = next(i for i, row in enumerate(D) if row.bit_count() == 4)
    graph = joined(D)
    graph[c] |= 1 << (7+c); graph[7+c] |= 1 << c
    masks = [m for m in range(128) if admissible(extend(D, [m]))]
    assert max(m.bit_count() for m in masks) == 2
    counts = Counter(); distributions = Counter(); examples = {}
    for m in masks:
        for z in masks:
            if m.bit_count() != z.bit_count():
                continue
            a = extend(graph, [m | (z << 7)])
            if not admissible(a):
                continue
            vectors = family(a, 4)
            count = pairs(vectors, vectors, [1]*7+[-1]*7+[0], same=True)
            degree = m.bit_count()
            counts[degree] = max(counts[degree], count)
            distributions[(degree, count)] += 1
            examples.setdefault((degree, count), [m, z])
    doubles = [m for m in masks if m.bit_count() == 2]
    assert len(doubles) == 7
    r = [(m & D[c]).bit_count() for m in doubles]
    t = []
    for m in doubles:
        a = extend(graph, [m | (m << 7)])
        vectors = family(a, 4)
        number = pairs(vectors, vectors, [1]*7+[-1]*7+[0], same=True)
        t.append(isqrt(number//2))
        assert 2*t[-1]**2 == number
    maxima = []
    for permutation in permutations(range(7)):
        maxima.append(104+2*sum(t[i]*t[permutation[i]]-r[i]*r[permutation[i]] for i in range(7)))
    assert max(maxima) == 184
    return {'maxima_by_degree': dict(counts), 'degree_two_masks': doubles,
            'r_weights': r, 't_weights': t, 'permutations_checked': len(maxima),
            'total_new_new_per_D_pair_at_most': max(maxima),
            'pattern_counts': {str(k): v for k, v in sorted(distributions.items())},
            'examples': {str(k): v for k, v in sorted(examples.items())}}


def main():
    prism = tuple(sum(1 << j for j in range(6) if i != j and
                      (i//3 == j//3 or i % 3 == j % 3)) for i in range(6))
    data = json.loads((ROOT/'data/codex_seven_vertex_census.json').read_text())
    dense = data['families']['minimum_degree_three_types']
    assert len(dense) == 1
    D = decode(7, dense[0]['code'])
    G14 = decode(8, 127242964)
    contained_prisms = 0
    for vertices in combinations(range(8), 6):
        mask = sum(1 << i for i in vertices)
        if all((G14[i] & mask).bit_count() == 3 for i in vertices):
            contained_prisms += 1
    assert contained_prisms == 2
    report = {'old_families': probe_old(prism, D)}
    print('Old families:', report['old_families'], flush=True)
    report['mass6_common_pair'] = probe_prism_common_pair(prism)
    print('Mass6:', report['mass6_common_pair'], flush=True)
    report['mass7_common_point'] = probe_D_common_point(D)
    print('Mass7:', report['mass7_common_point'], flush=True)
    assert report['old_families']['old_three_three_mass7'] == 88
    report['proved_bounds'] = {
        'mass6_new_new': '1680*tau+20*C8_127242964',
        'mass6_including_old': '2634*tau+20*C8_127242964',
        'mass7_including_old': '272*Omega',
        'all_losses_for_four_four': ('997920+2794*tau+272*Omega+(668/3)*C8_127242964'
                                    '+72*C8_2022000+32*C8_5683824+128*C8_5691760'
                                    '+100*C8_127305925+144*C8_128354469+64*C8_245715219')}
    (ROOT/'data/codex_four_four_small_mass_audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
