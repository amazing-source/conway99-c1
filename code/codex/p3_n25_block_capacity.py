"""Count boundary blocks violating the seven-pair neighborhood capacity.

Exploration of a new column filter only. No LP or support exclusion is run.
Uses the existing support register; IDs are not regenerated.
"""
import argparse
from collections import Counter
from itertools import combinations
import json

from p3_n25_saturated import ROOT, adjacency


def measure(row):
    a = adjacency(row)
    neighbors = [sum(a[i][j] << j for j in range(28)) for i in range(28)]
    forbidden = [sum(1 << j for j in range(28) if i != j and
                     2 - a[i][j] - (neighbors[i] & neighbors[j]).bit_count() == 0)
                 for i in range(28)]
    counts = Counter()
    examples = {}
    for k in range(4):
        for pp in combinations(range(3), k):
            pbits = sum(1 << p for p in pp)
            if any(forbidden[p] & pbits for p in pp):
                continue
            available = [q for q in range(3, 28) if not forbidden[q] & pbits]
            for nn in combinations(available, 4 + k):
                bits = pbits
                for q in nn:
                    if forbidden[q] & bits:
                        break
                    bits |= 1 << q
                else:
                    degrees = [(neighbors[s] & bits).bit_count() for s in range(28)]
                    if any(degrees[s] > 2 - ((bits >> s) & 1) for s in range(28)):
                        continue
                    vertices = pp + nn
                    t = sum(degrees[s] for s in vertices) // 2
                    rejected = t < len(vertices) - 7
                    counts[k, 'before'] += 1
                    counts[k, 'removed'] += rejected
                    if rejected and k not in examples:
                        examples[k] = {'vertices': vertices, 'internal_edges': t,
                                       'unmatched': len(vertices) - 2 * t,
                                       'remaining_neighbors': 14 - len(vertices)}
    return {'id': row['id'], 'delta': row['outside_N_triangles'],
            'before': sum(counts[k, 'before'] for k in range(4)),
            'removed': sum(counts[k, 'removed'] for k in range(4)),
            'by_k': {str(k): {s: counts[k, s] for s in ('before', 'removed')}
                     for k in range(4)}, 'examples': examples}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', default='4,443')
    parser.add_argument('--out', default='data/codex_p3_n25_block_capacity.json')
    args = parser.parse_args()
    wanted = set(map(int, args.ids.split(',')))
    source = json.loads((ROOT / 'data/codex_p3_n25_open_triangles.json').read_text())
    results = []
    for row in source['supports']:
        if row['id'] in wanted:
            result = measure(row)
            results.append(result)
            print(json.dumps(result), flush=True)
    assert {row['id'] for row in results} == wanted
    (ROOT / args.out).write_text(json.dumps({'scope': 'Column capacity only; no support exclusion',
                                          'results': results}, indent=2) + '\n')


if __name__ == '__main__':
    main()
