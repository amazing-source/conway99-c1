"""Finite local patterns and certified mass-6/7 collision bounds for (6,3).

Every count includes both signs of sum three. These are internal pair losses,
not a complete distinct-vector bound for the family.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb
import json
import gzip
import time

import numpy as np

from higher_census_minima import ROOT, certify
from seven_vertex_census import decode


def admissible(adj):
    return all((adj[i] & adj[j]).bit_count() <= (1 if adj[i] >> j & 1 else 2)
               for i, j in combinations(range(len(adj)), 2))


def join(core, centre=None):
    m = len(core)
    graph = list(core)+[row << m for row in core]
    if centre is not None:
        graph[centre] |= 1 << (centre+m)
        graph[centre+m] |= 1 << centre
    return graph


def extend(graph, profiles, edges):
    n = len(graph)
    out = list(graph)+list(profiles)
    for j, mask in enumerate(profiles):
        for i in range(n):
            if mask >> i & 1:
                out[i] |= 1 << (n+j)
    for bit, (i, j) in enumerate(combinations(range(len(profiles)), 2)):
        if edges >> bit & 1:
            out[n+i] |= 1 << (n+j)
            out[n+j] |= 1 << (n+i)
    return out


def colour_key(degrees, edges):
    pairs = list(combinations(range(len(degrees)), 2))
    adj = [[0]*len(degrees) for _ in degrees]
    for bit, (i, j) in enumerate(pairs):
        adj[i][j] = adj[j][i] = (edges >> bit) & 1
    codes = []
    for p in permutations(range(len(degrees))):
        if tuple(degrees[i] for i in p) == tuple(degrees):
            codes.append(sum(adj[p[i]][p[j]] << bit for bit, (i, j) in enumerate(pairs)))
    return tuple(degrees), min(codes)


class Representatives:
    def __init__(self, graph, m, r, profiles):
        core_vectors, common, left_positive, right_positive = [], [], [], []
        for c in range(r+1):
            bsize = m-6+c
            for B in combinations(range(m), bsize):
                for Bp in combinations(range(m), bsize):
                    v = [int(i not in B) for i in range(m)]+[-int(i in Bp) for i in range(m)]
                    partner = [v[i]-(1 if i < m else -1) for i in range(2*m)]
                    for C in combinations(range(r), c):
                        core_vectors.append(v)
                        common.append([1 if i in C else -1 for i in range(r)])
                        left_positive.append([int(x == 1) for x in v])
                        right_positive.append([int(x == 1) for x in partner])
        self.common = np.array(common, dtype=np.int16)
        self.cp = (self.common == 1).astype(np.int16)
        vectors = np.array(core_vectors, dtype=np.int16)
        self.vectors = vectors
        self.partners = vectors-np.array([1]*m+[-1]*m, dtype=np.int16)
        left, right = np.array(left_positive, dtype=np.int16), np.array(right_positive, dtype=np.int16)
        matrix = np.array([[(row >> i) & 1 for i in range(2*m)] for row in graph], dtype=np.int16)
        self.base = np.sum((vectors @ matrix)*vectors, axis=1)//2
        self.lp = np.sum((left @ matrix)*left, axis=1)//2
        self.rp = np.sum((right @ matrix)*right, axis=1)//2
        neighbour_matrix = np.array([[(mask >> i) & 1 for i in range(2*m)] for mask, _ in profiles], dtype=np.int16)
        self.dots = vectors @ neighbour_matrix.T
        self.ldots = left @ neighbour_matrix.T
        self.rdots = right @ neighbour_matrix.T

    def direct_check(self, graph, expected):
        """Check against the complete quadratic form, including both partners."""
        vectors = np.column_stack((self.vectors, self.common))
        partners = np.column_stack((self.partners, self.common))
        assert np.all(np.sum(vectors, axis=1) == 3)
        assert np.all(np.sum(vectors*vectors, axis=1) == 9)
        assert np.all(np.sum(partners, axis=1) == 3)
        assert np.all(np.sum(partners*partners, axis=1) == 9)
        n = len(graph)
        matrix = np.array([[(row >> i) & 1 for i in range(n)] for row in graph], dtype=np.int16)
        q = 28-np.sum((vectors @ matrix)*vectors, axis=1)
        other_q = 28-np.sum((partners @ matrix)*partners, axis=1)
        assert np.array_equal(q, other_q)
        positive = (vectors == 1).astype(np.int16)
        other_positive = (partners == 1).astype(np.int16)
        ew = np.sum((positive @ matrix)*positive, axis=1)//2
        ep = np.sum((other_positive @ matrix)*other_positive, axis=1)//2
        restricted = (ew <= 8) & (ep <= 8)
        actual = {f'Q{norm}_{kind}': 2*int(np.count_nonzero((q == norm) & keep))
                  for norm in (6, 8) for kind, keep in [('all', True), ('no_prism', restricted)]}
        assert actual == expected

    def counts(self, indices, edges):
        signed = self.base.copy(); left = self.lp.copy(); right = self.rp.copy()
        for j, index in enumerate(indices):
            signed += self.common[:, j]*self.dots[:, index]
            left += self.cp[:, j]*self.ldots[:, index]
            right += self.cp[:, j]*self.rdots[:, index]
        for bit, (i, j) in enumerate(combinations(range(len(indices)), 2)):
            if edges >> bit & 1:
                signed += self.common[:, i]*self.common[:, j]
                left += self.cp[:, i]*self.cp[:, j]
                right += self.cp[:, i]*self.cp[:, j]
        restricted = (left <= 8) & (right <= 8)
        return {f'Q{q}_{kind}': 2*int(np.count_nonzero((signed == (28-q)//2) & keep))
                for q in (6, 8) for kind, keep in [('all', True), ('no_prism', restricted)]}


def local_patterns(m):
    r = 9-m
    if m == 6:
        core = tuple(sum(1 << j for j in range(6) if i != j and (i//3 == j//3 or i%3 == j%3)) for i in range(6))
        graph = join(core)
        profiles = [(0, 24)]
        profiles += [((1 << i)+(1 << (6+j)), 1 if i%3 == j%3 else 2) for i in range(6) for j in range(6)]
        profiles += [(sum(1 << j for j in [i, i+3, i+6, i+9]), 1) for i in range(3)]
    else:
        source = json.loads((ROOT/'data/codex_seven_vertex_census.json').read_text())
        core = decode(7, source['families']['minimum_degree_three_types'][0]['code'])
        centre = next(i for i, row in enumerate(core) if row.bit_count() == 4)
        graph = join(core, centre)
        masks = [mask for mask in range(128) if admissible(extend(list(core), [mask], 0))]
        assert max(mask.bit_count() for mask in masks) == 2
        assert sum(mask.bit_count() == 2 for mask in masks) == 7
        assert all(not (mask >> centre & 1) for mask in masks if mask.bit_count() == 2)
        profiles = [(0, 17)]
        for a in masks:
            for b in masks:
                if not a or a.bit_count() != b.bit_count():
                    continue
                mask = a | (b << 7)
                if not admissible(extend(graph, [mask], 0)):
                    continue
                if a.bit_count() == 1:
                    i, j = a.bit_length()-1, 7+b.bit_length()-1
                    capacity = (1 if graph[i] >> j & 1 else 2)-(graph[i] & graph[j]).bit_count()
                else:
                    capacity = 1
                if capacity:
                    profiles.append((mask, capacity))
    profiles.sort(key=lambda item: ((item[0] & ((1 << m)-1)).bit_count(), item[0]))
    representatives = Representatives(graph, m, r, profiles)
    maxima, cases, detailed = {}, 0, {}
    for indices in combinations_with_replacement(range(len(profiles)), r):
        if any(count > profiles[i][1] for i, count in Counter(indices).items()):
            continue
        masks = [profiles[i][0] for i in indices]
        if m == 7:
            doubles = [mask for mask in masks if (mask & 127).bit_count() == 2]
            if len({mask & 127 for mask in doubles}) < len(doubles) or len({mask >> 7 for mask in doubles}) < len(doubles):
                continue
        degrees = tuple((mask & ((1 << m)-1)).bit_count() for mask in masks)
        for edges in range(1 << comb(r, 2)):
            if not admissible(extend(graph, masks, edges)):
                continue
            key = colour_key(degrees, edges)
            counts = representatives.counts(indices, edges)
            profile_key = colour_key(indices, edges)
            if profile_key in detailed:
                assert detailed[profile_key] == counts
            detailed[profile_key] = counts
            if key not in maxima:
                representatives.direct_check(extend(graph, masks, edges), counts)
                maxima[key] = counts
            else:
                maxima[key] = {name: max(maxima[key][name], value) for name, value in counts.items()}
            cases += 1
    print('Mass', m, ':', cases, 'local patterns;', len(maxima), 'colour/edge types', flush=True)
    record = {'core_adjacency': graph, 'profiles': profiles,
              'patterns': [{'profiles': indices, 'edges': edges, 'counts': counts}
                           for (indices, edges), counts in sorted(detailed.items())]}
    with gzip.GzipFile(filename=ROOT/f'data/codex_six_three_mass{m}_patterns.json.gz', mode='wb', mtime=0) as stream:
        stream.write(json.dumps(record).encode('utf-8'))
    return maxima, cases


def collision_bounds(m, maxima):
    """Aggregate exterior sets using exact group, edge, wedge, triangle counts."""
    r = 9-m
    sizes = [24, 60, 3] if m == 6 else [17, 61, 7]
    # E_ab = constant + coefficient*t, t = E_22.
    edges = {(0, 0): (33, 1), (0, 1): (252, -4), (0, 2): (18, 2),
             (1, 1): (228, 4), (1, 2): (12, -4), (2, 2): (0, 1)} if m == 6 else {
             (0, 0): (14, 1), (0, 1): (182, -4), (0, 2): (28, 2),
             (1, 1): (254, 4), (1, 2): (42, -4), (2, 2): (0, 1)}
    keys = sorted(maxima)
    width = len(keys)+2  # constant, t, one variable per colour/edge type
    rows = [('t>=0', [F(0), F(1)]+[F(0)]*len(keys)),
            ('t_upper', [F(3 if m == 6 else 10), F(-1)]+[F(0)]*len(keys))]
    for i, key in enumerate(keys):
        row = [F(0)]*width; row[2+i] = 1
        rows.append((f'pattern_{key}_nonnegative', row))
    def equality(name, c, t, coefficients):
        row = [F(c), F(t)]+list(map(F, coefficients))
        rows.append((name+'_positive', row))
        rows.append((name+'_negative', [-x for x in row]))
    for degrees in combinations_with_replacement(range(3), r):
        total = 1
        for degree, multiplicity in Counter(degrees).items():
            total *= comb(sizes[degree], multiplicity)
        equality(f'group_total_{degrees}', -total, 0, [int(key[0] == degrees) for key in keys])
        for pair in set(tuple(sorted(p)) for p in combinations(degrees, 2)):
            rest = list(degrees)
            for degree in pair:
                rest.remove(degree)
            factor = 1 if not rest else sizes[rest[0]]-sum(x == rest[0] for x in pair)
            c, t = edges[pair]
            coeff = []
            for ds, mask in keys:
                coeff.append(sum(1 for bit, (i, j) in enumerate(combinations(range(r), 2))
                                 if ds == degrees and (ds[i], ds[j]) == pair and mask >> bit & 1))
            equality(f'edge_marginal_{degrees}_{pair}', -factor*c, -factor*t, coeff)
    if r == 3:
        equality('outer_triangles', -161, 0, [int(mask == 7) for _, mask in keys])
        # An induced path has one wedge, a triangle has three.
        equality('outer_wedges', -6279, 0, [3 if mask == 7 else int(mask.bit_count() == 2) for _, mask in keys])
    results = {}
    for name in ['Q6_all', 'Q6_no_prism', 'Q8_all', 'Q8_no_prism']:
        objective = [F(0), F(0)]+[F(-maxima[key][name]) for key in keys]
        result = certify(rows, objective)
        result['objective'] = list(map(str, objective))
        result['collision_pair_upper_bound'] = str(-F(result['lower_bound']))
        results[name] = result
        print('Mass', m, name, '<=', result['collision_pair_upper_bound'], flush=True)
    return {'exterior_group_sizes': sizes, 'edge_counts_affine_in_t': {str(k): v for k, v in edges.items()},
            'pattern_order': [str(key) for key in keys], 'rows': [(name, list(map(str, row))) for name, row in rows],
            'results': results}


def main():
    start = time.monotonic(); report = {}
    for m in (6, 7):
        maxima, cases = local_patterns(m)
        report[str(m)] = {'local_patterns_checked': cases,
                          'pattern_maxima': {str(key): value for key, value in sorted(maxima.items())},
                          'bound': collision_bounds(m, maxima)}
        report['scope'] = 'Upper bounds on internal unordered collision pairs, both signs. Masses 8/9 and collisions with previous families remain unaudited.'
        (ROOT/'data/codex_six_three_small_mass_bounds.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Completed in', round(time.monotonic()-start, 2), 'seconds', flush=True)


if __name__ == '__main__':
    main()
