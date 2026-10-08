"""Local collision counts for F0: six positive vertices, seven edges,
and an anticomplete negative triangle. All counts include both signs.

Only binary differences of masses six and seven are treated here.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement
from math import comb
import argparse
import gzip
import json
import time

import numpy as np

from higher_census_minima import ROOT
from six_three_small_mass_bounds import admissible, extend, colour_key


class F0Representatives:
    def __init__(self, graph, profiles, m, p=6, triangle_free=False, positive_type=None):
        # The other family has (p,p-3) positive/negative vertices.
        # When p=6 it is also restricted to F0.
        self.m, self.p, self.r = m, p, p+3-m
        self.graph, self.profiles = graph, profiles
        self.triangle_free = triangle_free
        self.positive_type = positive_type
        assert positive_type is None or triangle_free
        r = self.r
        matrix = np.array([[(row >> i) & 1 for i in range(2*m)] for row in graph], dtype=np.int16)
        triangles = [(i,j,k) for i,j,k in combinations(range(2*m),3)
                     if graph[i] >> j & 1 and graph[i] >> k & 1 and graph[j] >> k & 1]
        core, common = [], []
        for c in range(r+1):
            a, b = m-6+c, 3-r+c
            if not 0 <= a <= m or not 0 <= b <= m:
                continue
            for B in combinations(range(m), a):
                for Bp in combinations(range(m), b):
                    v = np.array([int(i not in B) for i in range(m)]+[-int(i in Bp) for i in range(m)], dtype=np.int16)
                    w = v-np.array([1]*m+[-1]*m, dtype=np.int16)
                    valid = True
                    for x in [v, w] if p == 6 else [v]:
                        pos, neg = (x == 1).astype(np.int16), (x == -1).astype(np.int16)
                        # Every subset of the negative triangle must be complete.
                        if pos @ matrix @ pos > 14 or neg @ matrix @ neg != int(sum(neg))*(int(sum(neg))-1) or pos @ matrix @ neg:
                            valid = False; break
                        if triangle_free and any(pos[i] and pos[j] and pos[k] for i,j,k in triangles):
                            valid = False; break
                    if valid:
                        for C in combinations(range(r), c):
                            core.append(v)
                            common.append([1 if i in C else -1 for i in range(r)])
        self.vectors = np.array(core, dtype=np.int16).reshape((-1, 2*m))
        self.partners = self.vectors-np.array([1]*m+[-1]*m, dtype=np.int16)
        self.common = np.array(common, dtype=np.int16).reshape((len(core), r))
        neighbours = np.array([[(mask >> i) & 1 for i in range(2*m)] for mask, _ in profiles], dtype=np.int16)
        self.components = []
        self.triangle_components = []
        for x in [self.vectors, self.partners] if p == 6 else [self.vectors]:
            pos, neg = (x == 1).astype(np.int16), (x == -1).astype(np.int16)
            self.components.append((np.sum((pos @ matrix)*pos, axis=1)//2,
                                    np.sum((neg @ matrix)*neg, axis=1)//2,
                                    np.sum((pos @ matrix)*neg, axis=1),
                                    pos @ neighbours.T, neg @ neighbours.T))
            if triangle_free:
                # All remaining triangles meet the outside: one, two, or three vertices.
                single = np.zeros((len(core),len(profiles)),dtype=np.int16)
                for k,(mask,_) in enumerate(profiles):
                    for i,j in combinations(range(2*m),2):
                        if mask >> i & 1 and mask >> j & 1 and graph[i] >> j & 1:
                            single[:,k] += pos[:,i]*pos[:,j]
                overlaps = np.array([[((a & b) >> i) & 1 for i in range(2*m)]
                                     for a,_ in profiles for b,_ in profiles],dtype=np.int16)
                pair = pos @ overlaps.T
                self.triangle_components.append((single,pair))
        self.cp = (self.common == 1).astype(np.int16)
        self.cn = (self.common == -1).astype(np.int16)
        masks = {mask: i for i, (mask, _) in enumerate(profiles)}
        self.reverse = [masks[(mask >> m) | ((mask & ((1 << m)-1)) << m)] for mask, _ in profiles]

    def one_orientation(self, indices, edges):
        keep = np.ones(len(self.vectors), dtype=bool)
        for component,(p0, n0, x0, pdot, ndot) in enumerate(self.components):
            ep, en, cross = p0.copy(), n0.copy(), x0.copy()
            for j, index in enumerate(indices):
                ep += self.cp[:, j]*pdot[:, index]
                en += self.cn[:, j]*ndot[:, index]
                cross += self.cp[:, j]*ndot[:, index]+self.cn[:, j]*pdot[:, index]
            for bit, (i, j) in enumerate(combinations(range(self.r), 2)):
                if edges >> bit & 1:
                    ep += self.cp[:, i]*self.cp[:, j]
                    en += self.cn[:, i]*self.cn[:, j]
                    cross += self.cp[:, i]*self.cn[:, j]+self.cn[:, i]*self.cp[:, j]
            keep &= (ep == 7) & (en == 3) & (cross == 0)
            if self.triangle_free:
                single,pair = self.triangle_components[component]
                tri = np.zeros(len(self.vectors),dtype=np.int16)
                for j,index in enumerate(indices): tri += self.cp[:,j]*single[:,index]
                for bit,(i,j) in enumerate(combinations(range(self.r),2)):
                    if edges >> bit & 1:
                        tri += self.cp[:,i]*self.cp[:,j]*pair[:,indices[i]*len(self.profiles)+indices[j]]
                if self.r == 3 and edges == 7: tri += np.prod(self.cp,axis=1,dtype=np.int16)
                keep &= tri == 0
        if self.positive_type is not None and np.any(keep):
            from higher_vertex_census import ir_orders
            graph = extend(self.graph,[self.profiles[i][0] for i in indices],edges)
            for a in np.flatnonzero(keep):
                for x in [self.vectors[a],self.partners[a]] if self.p == 6 else [self.vectors[a]]:
                    full = list(x)+list(self.common[a])
                    W = [i for i,value in enumerate(full) if value == 1]
                    induced = tuple(sum(((graph[i] >> j) & 1) << b for b,j in enumerate(W)) for i in W)
                    if ir_orders(induced)[0] != self.positive_type:
                        keep[a] = False; break
        return int(np.count_nonzero(keep))

    def count(self, indices, edges):
        count = self.one_orientation(indices, edges)
        if self.p != 6:
            count += self.one_orientation([self.reverse[i] for i in indices], edges)
        return 2*count

    def direct_check(self, indices, edges):
        total = 0
        for ids in [indices] if self.p == 6 else [indices, [self.reverse[i] for i in indices]]:
            graph = extend(self.graph, [self.profiles[i][0] for i in ids], edges)
            matrix = np.array([[(row >> i) & 1 for i in range(len(graph))] for row in graph], dtype=np.int16)
            vectors = np.column_stack((self.vectors, self.common))
            partners = np.column_stack((self.partners, self.common))
            assert np.all(vectors.sum(axis=1) == 3) and np.all(partners.sum(axis=1) == 3)
            assert np.all(np.sum(vectors*vectors, axis=1) == 9)
            assert np.all(np.sum(partners*partners, axis=1) == 2*self.p-3)
            q = 28-np.sum((vectors @ matrix)*vectors, axis=1)
            other_q = 3*(2*self.p-3)+1-np.sum((partners @ matrix)*partners, axis=1)
            assert np.array_equal(q, other_q)
            keep = q == 8
            for x in [vectors, partners] if self.p == 6 else [vectors]:
                pos, neg = (x == 1).astype(np.int16), (x == -1).astype(np.int16)
                keep &= (np.sum((pos @ matrix)*pos, axis=1) == 14)
                keep &= (np.sum((neg @ matrix)*neg, axis=1) == 6)
                keep &= (np.sum((pos @ matrix)*neg, axis=1) == 0)
                if self.triangle_free:
                    for i,j,k in combinations(range(len(graph)),3):
                        if graph[i] >> j & 1 and graph[i] >> k & 1 and graph[j] >> k & 1:
                            keep &= (pos[:,i]*pos[:,j]*pos[:,k] == 0)
                if self.positive_type is not None:
                    # The two triangle-free types are distinguished by bipartiteness.
                    for a in np.flatnonzero(keep):
                        W = {i for i,value in enumerate(x[a]) if value == 1}
                        colours = {}; bipartite = True
                        for start in W:
                            if start in colours: continue
                            colours[start] = 0; queue = [start]
                            while queue:
                                v = queue.pop()
                                for u in W:
                                    if not (graph[v] >> u & 1): continue
                                    if u in colours:
                                        if colours[u] == colours[v]: bipartite = False
                                    else: colours[u] = 1-colours[v]; queue.append(u)
                        keep[a] &= bipartite == (self.positive_type == 21812)
            total += int(np.count_nonzero(keep))
        assert 2*total == self.count(indices, edges)


def generate(m, p, triangle_free=False, verify_only=False, positive_type=None):
    start = time.monotonic()
    with gzip.open(ROOT/f'data/codex_six_three_mass{m}_patterns.json.gz', 'rt') as stream:
        source = json.load(stream)
    graph, profiles = source['core_adjacency'], source['profiles']
    reps = F0Representatives(graph, profiles, m, p, triangle_free,positive_type)
    print('Mass', m, 'other family', (p,p-3), ':', len(reps.vectors), 'core templates', flush=True)
    if p == 6:
        patterns = source['patterns']
    else:
        patterns = []
        for ids in combinations_with_replacement(range(len(profiles)), reps.r):
            if any(n > profiles[i][1] for i, n in Counter(ids).items()): continue
            masks = [profiles[i][0] for i in ids]
            if m == 7:
                doubles = [a for a in masks if (a & 127).bit_count() == 2]
                if len({a & 127 for a in doubles}) < len(doubles) or len({a >> 7 for a in doubles}) < len(doubles): continue
            for edges in range(1 << comb(reps.r, 2)):
                if admissible(extend(graph, masks, edges)):
                    patterns.append({'profiles': ids, 'edges': edges})
    checked = set()
    out = []
    for row in patterns:
        ids, edges = row['profiles'], row['edges']
        count = reps.count(ids, edges)
        # Check full quadratic form on every local degree/edge/count class.
        degrees = [(profiles[i][0] & ((1 << m)-1)).bit_count() for i in ids]
        key = (colour_key(degrees, edges), count)
        if key not in checked:
            reps.direct_check(ids, edges); checked.add(key)
        out.append({'profiles': ids, 'edges': edges, 'counts': {'F0': count}})
    record = {'core_adjacency': graph, 'profiles': profiles, 'patterns': out,
              'mass': m, 'other_positive_size': p, 'outside_size': reps.r,
              'core_templates': len(reps.vectors), 'direct_check_classes': len(checked), 'triangle_free':triangle_free,
              'scope': 'Both signs, internal F0 if p=6; F0 against all norm-eight (p,p-3) representatives otherwise.'}
    suffix = '_tf' if triangle_free else ''
    if positive_type is not None:
        suffix += f'_{positive_type}'
        record['positive_type'] = positive_type
    path = ROOT/f'data/codex_f0_mass{m}_p{p}{suffix}_patterns.json.gz'
    if verify_only:
        with gzip.open(path,'rt') as stream:
            assert json.load(stream) == json.loads(json.dumps(record))
    else:
        with gzip.GzipFile(filename=path, mode='wb', mtime=0) as stream:
            stream.write(json.dumps(record).encode())
    print('Saved', len(out), 'patterns;', sum(bool(row['counts']['F0']) for row in out), 'nonzero;',
          'max local count', max((row['counts']['F0'] for row in out), default=0),
          '; seconds', round(time.monotonic()-start,1), flush=True)
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mass', type=int, choices=(6,7), required=True)
    parser.add_argument('--p', type=int, choices=(3,4,5,6), required=True)
    parser.add_argument('--triangle-free',action='store_true')
    parser.add_argument('--verify-only',action='store_true')
    parser.add_argument('--positive-type',type=int,choices=(7064,21812))
    args = parser.parse_args()
    assert args.p+3 >= args.mass
    generate(args.mass, args.p,args.triangle_free,args.verify_only,args.positive_type)
