"""Exact anti-neighborhood edge identities from A^2 and A^3 for four motifs.

For S, X its external neighborhood, Y the vertices outside S with no
neighbor in S, put j(x)=|N(x) cap S| and R={x in X:j(x)>=2}.
The identity has the form e(Y)=constant+sum_{xy in E(R)}(j(x)-1)(j(y)-1).
It uses A^3=13A-12I+26J and no extension or solver assumption.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json

from small_positive_three_supports import edge, valid, pairs


MOTIFS = {
    'C4': (4, [(0,1), (1,2), (2,3), (3,0)]),
    'paw': (4, [(0,1), (1,2), (2,0), (0,3)]),
    'bowtie': (5, [(0,1), (1,2), (2,0), (0,3), (3,4), (4,0)]),
    'house': (5, [(0,1), (1,2), (2,3), (3,0), (0,4), (1,4)]),
}


def examine(n, edges):
    rows = [0]*n
    for x,y in edges:
        edge(rows, x, y)
    degrees = [row.bit_count() for row in rows]
    pair_list = pairs(n)
    residual = [(1 if rows[x] >> y & 1 else 2)-(rows[x] & rows[y]).bit_count()
                for x,y in pair_list]
    assert max(residual) == 1  # Hence all multiple profiles occur at most once.
    multiple_profiles = []
    for mask in range(1, 1 << n):
        if mask.bit_count() < 2:
            continue
        extended = rows+[0]
        for x in range(n):
            if mask >> x & 1:
                edge(extended, x, n)
        if valid(extended):
            multiple_profiles.append(mask)
    weighted_X_edges = (26*len(edges)-12*n+26*n*n
        -2*sum(degrees[x]*degrees[y] for x,y in edges)
        -2*sum(degrees[x]*(12+2*n-degrees[x]
                          -sum(degrees[y] for y in range(n) if rows[x] >> y & 1)) for x in range(n)))//2
    cases = []
    for selection in range(1 << len(multiple_profiles)):
        profiles = [mask for i,mask in enumerate(multiple_profiles) if selection >> i & 1]
        if any(sum(bool(mask >> x & 1 and mask >> y & 1) for mask in profiles) != target
               for (x,y),target in zip(pair_list, residual)):
            continue
        single_counts = [14-degrees[x]-sum(bool(mask >> x & 1) for mask in profiles) for x in range(n)]
        assert min(single_counts) >= 0
        count_X = sum(single_counts)+len(profiles)
        D = sum((mask.bit_count()-1)*(2*n-mask.bit_count()
                 -sum(degrees[x] for x in range(n) if mask >> x & 1)) for mask in profiles)
        constant = 693-len(edges)-14*count_X+weighted_X_edges-D
        fixed = rows+[0]*len(profiles)
        for i,mask in enumerate(profiles):
            for x in range(n):
                if mask >> x & 1:
                    edge(fixed, x, n+i)
        corrections = Counter()
        variable_edges = pairs(len(profiles))
        for selected in range(1 << len(variable_edges)):
            extended = fixed.copy()
            correction = 0
            for bit,(i,j) in enumerate(variable_edges):
                if selected >> bit & 1:
                    edge(extended, n+i, n+j)
                    correction += (profiles[i].bit_count()-1)*(profiles[j].bit_count()-1)
            if valid(extended):
                corrections[correction] += 1
        assert corrections
        cases.append(dict(multiple_profiles=profiles, weights=[m.bit_count()-1 for m in profiles],
                          singleton_profile_counts=single_counts, X_size=count_X, Y_size=99-n-count_X,
                          Y_degree_constant=14-2*n, Y_edge_constant=constant,
                          correction_histogram=dict(sorted(corrections.items())),
                          minimum_Y_edges=constant+min(corrections), maximum_Y_edges=constant+max(corrections)))
    return dict(order=n, edges=edges, weighted_X_edges=weighted_X_edges, cases=cases)


def main():
    report = {name: examine(n, edges) for name,(n,edges) in MOTIFS.items()}
    for name, item in report.items():
        print(json.dumps(dict(motif=name, cases=[{key: case[key] for key in
              ['Y_size','Y_edge_constant','correction_histogram']} for case in item['cases']])), flush=True)
    # Each prism contains six houses, each with a unique three-neighbor vertex.
    raw_norm8_support7 = 2*(2079*96+8316*103-24*1150)
    assert raw_norm8_support7 == 2057064
    report['norm8_support7_raw_vector_lower_bound'] = raw_norm8_support7
    report['warning'] = 'Raw vectors only; projection collisions have not been subtracted.'
    data = Path(__file__).resolve().parents[3] / 'data' / 'codex_night_20261014'
    (data / 'small_antineighborhoods.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
