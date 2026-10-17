"""Binary mass-six pair counts for signed norm-eight families, support <=9.

Counts include both signs; balanced families already contain their negatives.
Only (6,3) is restricted, by requiring at most eight positive-support edges.
The (9,0) channel is separately labelled: it requires positive supports that
contain a prism and must not be charged to a family excluding those supports.
"""
from collections import Counter
from itertools import combinations
from math import comb
import argparse
import gzip
import json

import numpy as np

from higher_census_minima import ROOT
from six_three_small_mass_bounds import extend, colour_key


FAMILIES = ((9,0), (7,1), (6,3), (6,0), (5,2), (4,4),
            (4,1), (3,3), (3,0), (2,2), (1,1))


def name(shape):
    return ''.join(map(str, shape))


def channels(r):
    return [(a,b) for i,a in enumerate(FAMILIES) for b in FAMILIES[i:]
            if a[0]-a[1] == b[0]-b[1] and sum(a)+sum(b) == 12+2*r]


def four_four_formula(profiles, ids, edge):
    """Independent local formula checked exhaustively in note 185."""
    left,right = [profiles[i][0] for i in ids]
    d1,d2 = (left&63).bit_count(),(right&63).bit_count()
    if sorted((d1,d2)) == [0,2]: return 2*edge
    if sorted((d1,d2)) == [1,2] and not edge:
        single,double = (left,right) if d1 == 1 else (right,left)
        return 2*int(single&double == single)
    if d1 == d2 == 2: return 8*int(not edge)
    if d1 == d2 == 1:
        u,v = [(mask&63).bit_length()-1 for mask in (left,right)]
        x,y = [(mask>>6).bit_length()-1 for mask in (left,right)]
        adjacent = lambda a,b: a != b and (a//3 == b//3 or a%3 == b%3)
        if not edge: return 2*int(u//3 != v//3 and x//3 != y//3)
        if u == v: return 6*int(adjacent(x,y))
        if x == y: return 6*int(adjacent(u,v))
        return 2*int(adjacent(u,v) and adjacent(x,y))
    return 0


class PairCounts:
    def __init__(self, graph, profiles, a, b):
        p,q = a; pp,qq = b
        assert p-q == pp-qq
        r = (p+q+pp+qq-12)//2
        self.a, self.b, self.r = a, b, r
        self.graph, self.profiles = graph, profiles
        vectors, common = [], []
        for c in range(r+1):
            nl, nr = 6-p+c, q-r+c
            if not (0 <= nl <= 6 and 0 <= nr <= 6): continue
            for left in combinations(range(6), nl):
                for right in combinations(range(6), nr):
                    for positive in combinations(range(r), c):
                        vectors.append([int(i not in left) for i in range(6)]
                                       +[-int(i in right) for i in range(6)])
                        common.append([1 if i in positive else -1 for i in range(r)])
        self.vectors = np.array(vectors, dtype=np.int16).reshape((-1,12))
        self.other = self.vectors-np.array([1]*6+[-1]*6, dtype=np.int16)
        self.common = np.array(common, dtype=np.int16).reshape((len(vectors),r))
        self.cp = (self.common == 1).astype(np.int16)
        matrix = np.array([[(row >> i)&1 for i in range(12)] for row in graph], dtype=np.int16)
        neighbours = np.array([[(mask >> i)&1 for i in range(12)]
                               for mask,_ in profiles], dtype=np.int16)
        self.base = np.sum((self.vectors @ matrix)*self.vectors,axis=1)//2
        self.dots = self.vectors @ neighbours.T
        self.positive = []
        for shape, x in ((a,self.vectors),(b,self.other)):
            if shape == (6,3):
                pos = (x == 1).astype(np.int16)
                self.positive.append((np.sum((pos @ matrix)*pos,axis=1)//2,
                                      pos @ neighbours.T))
        masks = {mask:i for i,(mask,_) in enumerate(profiles)}
        self.reverse = [masks[(mask >> 6)|((mask&63)<<6)] for mask,_ in profiles]
        assert (p-q)%3 == 0
        self.target = (3*(p+q)+((p-q)//3)**2-8)//2
        self.factor = 1 if p == q else 2

    def one(self, ids, edges):
        signed = self.base.copy()
        for j,i in enumerate(ids): signed += self.common[:,j]*self.dots[:,i]
        for bit,(i,j) in enumerate(combinations(range(self.r),2)):
            if edges >> bit&1: signed += self.common[:,i]*self.common[:,j]
        keep = signed == self.target
        for base,dots in self.positive:
            ep = base.copy()
            for j,i in enumerate(ids): ep += self.cp[:,j]*dots[:,i]
            for bit,(i,j) in enumerate(combinations(range(self.r),2)):
                if edges >> bit&1: ep += self.cp[:,i]*self.cp[:,j]
            keep &= ep <= 8
        return int(np.count_nonzero(keep))

    def count(self, ids, edges):
        count = self.one(ids,edges)
        if self.a != self.b: count += self.one([self.reverse[i] for i in ids],edges)
        return self.factor*count

    def check(self, ids, edges):
        # Independent full-matrix norm/size evaluation, on all template vectors.
        total = 0
        for indices in [ids] if self.a == self.b else [ids,[self.reverse[i] for i in ids]]:
            graph = extend(self.graph,[self.profiles[i][0] for i in indices],edges)
            matrix = np.array([[(row >> i)&1 for i in range(len(graph))]
                               for row in graph], dtype=np.int16)
            keep = np.ones(len(self.vectors), dtype=bool)
            for shape,core in ((self.a,self.vectors),(self.b,self.other)):
                full = np.column_stack((core,self.common))
                assert np.all(np.sum(full == 1,axis=1) == shape[0])
                assert np.all(np.sum(full == -1,axis=1) == shape[1])
                norm = (3*np.sum(full*full,axis=1)+(full.sum(axis=1)//3)**2
                        -np.sum((full @ matrix)*full,axis=1))
                keep &= norm == 8
                if shape == (6,3):
                    pos = (full == 1).astype(np.int16)
                    keep &= np.sum((pos @ matrix)*pos,axis=1) <= 16
            total += int(np.count_nonzero(keep))
        assert self.factor*total == self.count(ids,edges)


def generate(verify_only=False):
    report = {'scope': __doc__, 'by_outside_size': {}}
    for r in range(4):
        path = ROOT / (f'data/codex_f0_mass6_p{r+3}_patterns.json.gz' if r < 3
                       else 'data/codex_six_three_mass6_patterns.json.gz')
        with gzip.open(path,'rt') as stream: data = json.load(stream)
        reps = {f'{name(a)}_{name(b)}':PairCounts(data['core_adjacency'],data['profiles'],a,b)
                for a,b in channels(r) if (a,b) != ((6,3),(6,3))}
        checked = set(); patterns = []
        for row in data['patterns']:
            ids,edges = row['profiles'],row['edges']
            costs = {label:rep.count(ids,edges) for label,rep in reps.items()}
            degrees = tuple((data['profiles'][i][0]&63).bit_count() for i in ids)
            if r == 2:
                assert costs['44_44'] == four_four_formula(data['profiles'],ids,edges)
            if r == 3:
                costs['63_63'] = row['counts']['Q8_no_prism']
                assert costs['90_90'] == 2*int(sum(degrees)+edges.bit_count() == 5)
            key = (colour_key(degrees,edges),tuple(costs.values()))
            if key not in checked:
                for rep in reps.values(): rep.check(ids,edges)
                checked.add(key)
            patterns.append({'profiles':ids,'edges':edges,'counts':costs})
        block = dict(data,patterns=patterns)
        block['direct_check_classes'] = len(checked)
        report['by_outside_size'][str(r)] = block
        print('Outside size',r,'patterns',len(patterns),'channels',list(patterns[0]['counts']),
              'direct checks',len(checked),flush=True)
    # Match previously derived exact channels (note 181/185).
    totals = Counter()
    for r in ('0','1'):
        data = report['by_outside_size'][r]
        for row in data['patterns']:
            cap = 1
            for i,n in Counter(row['profiles']).items(): cap *= comb(data['profiles'][i][1],n)
            for label,c in row['counts'].items(): totals[label] += cap*c
    assert totals['52_52'] == totals['52_41'] == 216
    assert totals['44_33'] == 792 and totals['44_22'] == 162
    report['exact_small_channels'] = dict(totals)
    path = ROOT / 'data/codex_mass6_family_patterns.json.gz'
    if verify_only:
        with gzip.open(path,'rt') as stream: assert json.load(stream) == report
    else:
        with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:
            stream.write(json.dumps(report).encode())
    print('Exact small channels:',dict(totals),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only',action='store_true')
    generate(parser.parse_args().verify_only)
