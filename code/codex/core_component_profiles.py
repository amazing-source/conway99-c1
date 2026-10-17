"""New component/grid reductions from the 174 surviving defect cores.

Uses the real component-balance identity, with no modular rank hypothesis.
Profiles listed here are necessary possibilities, not completion witnesses.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from twisted_prism_core import ROOT, matrix


def coarsenings(weights):
    profiles = set()
    def add(i, sums):
        if i == len(weights):
            profiles.add(tuple(sorted(sums, reverse=True)))
            return
        add(i+1, sums+[weights[i]])
        for j in range(len(sums)):
            merged = sums.copy()
            merged[j] += weights[i]
            add(i+1, merged)
    add(0, [])
    return sorted(profiles, reverse=True)


def anchor_profile(a, triangle, far):
    near = {v for v in range(14) if v not in triangle and int(a[v, triangle].sum()) == 1}
    shadow = {v for v in near if a[v, far]}
    assert len(near) == 10 and len(shadow) == 6
    unseen = set(near)
    components = []
    while unseen:
        start = min(unseen)
        reached, pending = {start}, [start]
        unseen.remove(start)
        while pending:
            u = pending.pop()
            for v in sorted(unseen):
                if a[u, v]:
                    unseen.remove(v)
                    reached.add(v)
                    pending.append(v)
        hit = reached & shadow
        assert hit
        components.append({'vertices': sorted(reached), 'shadow_vertices': sorted(hit),
                           'weight': len(hit)})
    weights = tuple(sorted((c['weight'] for c in components), reverse=True))
    profiles = coarsenings(weights)
    bound = weights.count(1)
    return {'triangle': triangle, 'far_apex': far, 'partial_components': components,
            'shadow_component_weights': weights,
            'necessary_full_component_sizes': [tuple(6*q for q in p) for p in profiles],
            'grid_count_upper_bound': bound,
            'forces_connected': profiles == [(6,)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    cores = json.loads((ROOT/'data/codex_twisted_prism_core.json').read_text())
    extension = json.loads((ROOT/'data/codex_twisted_prism_extension.json').read_text())
    ids = [r['bits'] for r in extension['results'] if r['status'] == 'lp_feasible_unresolved']
    edges = [tuple(e) for e in cores['optional_edges']]
    rows = []
    bounds_hist = Counter()
    for bits in ids:
        a = matrix(bits, edges)
        anchors = [anchor_profile(a, [0, 1, 2], 5), anchor_profile(a, [3, 4, 5], 2)]
        bounds = tuple(sorted(p['grid_count_upper_bound'] for p in anchors))
        bounds_hist[bounds] += 1
        rows.append({'bits': bits, 'anchors': anchors, 'unordered_grid_upper_bounds': bounds})
    grid_rich = {str(q): [r['bits'] for r in rows if min(r['unordered_grid_upper_bounds']) >= q]
                 for q in range(7)}
    summary = {
        'core_count': len(rows),
        'both_triangles_forced_gridfree': sum(r['unordered_grid_upper_bounds'] == (0, 0) for r in rows),
        'at_least_one_triangle_forced_gridfree': sum(min(r['unordered_grid_upper_bounds']) == 0 for r in rows),
        'at_least_one_connected_near_graph': sum(any(p['forces_connected'] for p in r['anchors']) for r in rows),
        'both_connected_near_graphs': sum(all(p['forces_connected'] for p in r['anchors']) for r in rows),
        'remaining_if_every_triangle_in_at_least_q_grids': {q: len(v) for q, v in grid_rich.items()},
        'grid_upper_bound_pairs': [{'bounds': list(k), 'core_count': n} for k, n in sorted(bounds_hist.items())]}
    report = {'scope': 'rank-independent necessary component profiles; no new unconditional core exclusions',
              'summary': summary, 'grid_rich_core_ids': grid_rich, 'cores': rows}
    args.out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(summary))
    print('For q=4:', grid_rich['4'])


if __name__ == '__main__':
    main()
