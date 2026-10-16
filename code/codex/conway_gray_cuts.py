"""Portable forbidden positive-edge patterns from gray-block contradictions.

If m complete degree-12 rows imply a contradiction, the union P of their
positive edges cannot occur in any rooted Conway graph. Indeed all those
edges would saturate the m rows and force their entire neighbourhoods.
Thus sum(e for e in P) <= |P|-1 is a universally necessary inequality.
It forbids a specific labelled pattern, not every possible frame.
"""
from itertools import combinations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_gray_block import build_system, propagate

ALL_LABELS = [(a,b) for a,b in combinations(range(14),2) if b != (a ^ 1)]


def make_cut(labels, fixed, name):
    assert list(labels) == ALL_LABELS
    proof = propagate(*build_system(labels, fixed))
    assert proof['status'] == 'EXACT_PROPAGATION_CONTRADICTION'
    pattern = set()
    neighbourhoods = []
    for z,row in sorted(fixed.items()):
        assert len(row) == 84 and set(row) <= {0,1} and row[z] == 0 and sum(row) == 12
        neighbours = [labels[q] for q,value in enumerate(row) if value]
        neighbourhoods.append(dict(row=labels[z], neighbours=neighbours))
        for q,value in enumerate(row):
            if value:
                pattern.add(tuple(sorted((labels[z],labels[q]))))
    return dict(name=name, edges=sorted(pattern), upper_bound=len(pattern)-1,
                neighbourhoods=neighbourhoods,
                proof_method='Exact integer propagation, then degree-12 saturation of the positive pattern.',
                scope='Universal necessary inequality in rooted Conway labels. Only this positive-edge pattern is forbidden.')


def validate_cut(cut):
    index = {p:i for i,p in enumerate(ALL_LABELS)}
    fixed = {}
    for item in cut['neighbourhoods']:
        z = index[tuple(item['row'])]
        assert z not in fixed
        row = [0]*84
        for neighbour in item['neighbours']:
            row[index[tuple(neighbour)]] = 1
        fixed[z] = row
    derived = make_cut(ALL_LABELS, fixed, cut['name'])
    given = {tuple(sorted(tuple(p) for p in edge)) for edge in cut['edges']}
    expected = set(derived['edges'])
    assert given == expected and len(given) == len(cut['edges'])
    assert cut['upper_bound'] == derived['upper_bound']
    return True


def add_gray_cuts(model, labels, graph, cuts):
    index = {tuple(p):i for i,p in enumerate(labels)}
    applied = []
    seen = set()
    for cut in cuts:
        pattern = tuple(sorted(tuple(sorted(tuple(p) for p in edge)) for edge in cut['edges']))
        if pattern in seen or any(p not in index for edge in pattern for p in edge):
            continue
        validate_cut(cut)
        model.Add(sum(graph[index[p]][index[q]] for p,q in pattern) <= cut['upper_bound'])
        seen.add(pattern)
        applied.append(cut)
    return applied
