"""Apply the analytic per-positive matching bound, note246, to saved supports.

No optimization and no spectral recomputation. Original IDs stay unchanged.
"""
from collections import Counter
from itertools import combinations
import json

from p3_n25_saturated import ROOT, adjacency


def local_rows(row):
    a = adjacency(row)
    rows = []
    for p in range(3):
        q = [v for v in range(3, 28) if a[p][v]]
        assert len(q) == 8
        t = sum(a[v][w] for v, w in combinations(q, 2))
        c = [sum(a[p][v] * a[other][v] for v in range(3, 28))
             for other in range(3) if other != p]
        x = sum(v * (v - 1) // 2 for v in c)
        w = 0
        for v in range(3, 28):
            d = sum(a[v][u] for u in q)
            w += d * (d - 1) // 2
        upper = 5 + 2 * sum(c) - x - w
        rows.append({'positive': p, 't': t, 'common_counts': c,
                     'X': x, 'W': w, 'upper_for_3t': upper,
                     'ell': upper - 3 * t})
    return rows


def main():
    source = json.loads((ROOT / 'data/codex_p3_n25_open_triangles.json').read_text())
    retained, excluded = [], []
    counts = Counter()
    for row in source['supports']:
        if row['status'] == 'excluded_exact_spectral' or row['outside_N_triangles'] < 3:
            continue
        local = local_rows(row)
        bad = [r for r in local if r['t'] < 1 or r['ell'] < 0]
        entry = {'id': row['id'], 'delta': row['outside_N_triangles'], 'local': local}
        if bad:
            entry['first_obstruction'] = bad[0]['positive']
            excluded.append(entry)
            counts[(entry['delta'], 'excluded')] += 1
        else:
            retained.append(entry)
            counts[(entry['delta'], 'retained')] += 1
    report = {'scope': 'Exact combinatorial local matching inequalities, note246; S0 remains open',
              'source': 'codex_p3_n25_open_triangles.json',
              'previous_survivors': len(retained) + len(excluded),
              'new_exclusions': len(excluded), 'retained_count': len(retained),
              'by_delta': {str(d): {s: counts[(d, s)] for s in ('excluded', 'retained')}
                           for d in sorted({d for d, _ in counts})},
              'excluded': excluded, 'retained': retained}
    (ROOT / 'data/codex_p3_n25_local_matching.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('previous_survivors', 'new_exclusions', 'retained_count', 'by_delta')}))


if __name__ == '__main__':
    main()
