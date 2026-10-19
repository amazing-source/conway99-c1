"""Four-colour factor obstruction for H01=-H02 and the grid Q12.

The 24 labels of D={3,4,5,6} each see exactly two core vertices and
exactly one Q12 vertex. Their core pairs form the deficit multigraph T.
The colour j subgraph is simple: repeating a pair would give two labels
three common neighbours (two in the core and one in Q12). Its degree at
v is 2 minus the number of upper letters shared by v and Q12 corner j.
All four simple factors must add to T. No D-grid hypothesis is needed.
"""

import argparse
from collections import defaultdict
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process

PAIRS = tuple(combinations(range(8), 2))
PAIR_ID = {p: i for i, p in enumerate(PAIRS)}


def colour_degrees(j):
    return tuple(2-int(v % 2 == (j//2 if v < 4 else j % 2)) for v in range(8))


def deficit(core):
    return tuple(core['T'][f'{u}-{v}'] for u, v in PAIRS)


def factors(T, degrees):
    """All simple spanning subgraphs of support(T) with given degrees."""
    d = list(degrees)
    result = []

    def visit(u, mask):
        if u == 8:
            result.append(mask)
            return
        neighbours = [v for v in range(u+1, 8) if d[v] and T[PAIR_ID[u, v]]]
        need = d[u]
        for chosen in combinations(neighbours, need):
            for v in chosen:
                d[v] -= 1
            d[u] = 0
            visit(u+1, mask | sum(1 << PAIR_ID[u, v] for v in chosen))
            d[u] = need
            for v in chosen:
                d[v] += 1

    visit(0, 0)
    return tuple(result)


def colourings(core):
    T = deficit(core)
    assert max(T) <= 2
    one = sum(1 << k for k, t in enumerate(T) if t == 1)
    two = sum(1 << k for k, t in enumerate(T) if t == 2)
    fs = [factors(T, colour_degrees(j)) for j in range(4)]
    right = defaultdict(list)
    for c in fs[2]:
        for d in fs[3]:
            if not (c & d & one):
                right[c | d, c & d].append((c, d))
    result = []
    for a in fs[0]:
        for b in fs[1]:
            union, inter = a | b, a & b
            if inter & one:
                continue
            wanted = ((one & ~union) | (two & ~inter), two & ~union)
            result.extend((a, b, c, d) for c, d in right.get(wanted, ()))
    return fs, result


def weighted_edge_bound(T, j, weights, remove=None):
    """Exact linear witness that a colour factor needs a forbidden edge."""
    support = [p for k, p in enumerate(PAIRS) if T[k] and p != remove]
    lhs = sum(w*d for w, d in zip(weights, colour_degrees(j)))
    rhs = sum(max(0, weights[u]+weights[v]) for u, v in support)
    return {'colour': j, 'weights': weights, 'degree_sum': lhs,
            'edge_capacity': rhs, 'removed_edge': remove,
            'impossible_without_removed_edge': lhs > rhs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pair-cores', type=Path, required=True)
    parser.add_argument('--core-orbits', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not args.output.exists()
    resources = limit_research_process(1)
    start = time.process_time()
    cores = json.loads(args.pair_cores.read_text(encoding='utf8'))
    orbit_data = json.loads(args.core_orbits.read_text(encoding='utf8'))
    results = []
    for ci in orbit_data['representatives']:
        fs, cs = colourings(cores[ci])
        record = {'core_index': ci, 'factor_counts': [len(f) for f in fs],
                  'colourings': cs, 'status': 'PASSES' if cs else 'EXCLUDED_COLOUR_FACTORS'}
        if ci == 20:
            certificate = weighted_edge_bound(deficit(cores[ci]), 0, [-1, 1]*4)
            assert certificate['impossible_without_removed_edge']
            record['linear_certificate'] = certificate
        if ci == 23:
            certificates = [
                weighted_edge_bound(deficit(cores[ci]), 2, [1,-1,1,-1,0,-1,-1,1], (4,7)),
                weighted_edge_bound(deficit(cores[ci]), 3, [1,-1,1,-1,1,-1,-1,0], (4,7)),
            ]
            assert all(c['impossible_without_removed_edge'] for c in certificates)
            assert deficit(cores[ci])[PAIR_ID[4,7]] == 1
            record['linear_certificate'] = {'forced_in_colours': certificates,
                                            'edge': [4,7], 'demand': 1, 'minimum': 2}
        results.append(record)
        print(json.dumps({'core': ci, 'factors': record['factor_counts'],
                          'colourings': len(cs), 'status': record['status']}), flush=True)
    out = {'scope': __doc__, 'resources': resources, 'uses_Q12_grid': True,
           'D_grids_required': False, 'uses_E3_in_core_catalogue': True,
           'sources': {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (args.pair_cores, args.core_orbits)},
           'core_pair_order': PAIRS, 'results': results,
           'cpu_seconds': time.process_time()-start, 'whole_family_excluded': False}
    atomic_json_write(args.output, out)


if __name__ == '__main__':
    main()
