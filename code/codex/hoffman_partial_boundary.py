"""Find coexistence obstructions that survive forgetting coclique incidences.

Retained points specify their incidence to every outside vertex. All points
of the selected root blocks are retained, so these blocks remain fully fixed.
Other point incidences are forgotten, as are conflicts invisible on retained
points. The row model is therefore a relaxation for EVERY boundary extension.
Only INFEASIBLE establishes an obstruction; a feasible row model is no SRG.
"""
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from ortools.sat.python import cp_model

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'data/codex_hoffman_trades/proof_bundle.json'
OUT = ROOT / 'data/codex_hoffman_partial'


def solve_rows(blocks, roots, retained, seconds=3):
    retained = set(retained)
    sets = [set(b) for b in blocks]
    assert all(sets[r] <= retained for r in roots)
    projected = [s & retained for s in sets]
    forbidden = [(a, b) for a, b in combinations(range(77), 2)
                 if len(projected[a] & projected[b]) >= 2]
    m = cp_model.CpModel()
    rows = {r: [m.new_bool_var(f'r{r}_{j}') for j in range(77)] for r in roots}
    for r, row in rows.items():
        m.add(row[r] == 0)
        m.add(sum(row) == 10)
        for p in sorted(retained):
            m.add(sum(row[j] for j in range(77) if p in sets[j]) == 2-int(p in sets[r]))
        for a, b in forbidden:
            m.add(row[a] + row[b] <= 1)
        for j in range(77):
            if len(projected[r] & projected[j]) >= 2:
                m.add(row[j] == 0)
    for i, j in combinations(roots, 2):
        m.add(rows[i][j] == rows[j][i])
        common = [m.new_bool_var(f'z{i}_{j}_{k}') for k in range(77)]
        for k, z in enumerate(common):
            m.add(z <= rows[i][k])
            m.add(z <= rows[j][k])
            m.add(z >= rows[i][k] + rows[j][k] - 1)
        m.add(sum(common) + rows[i][j] == 2-len(sets[i] & sets[j]))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 20261012
    status = solver.solve(m)
    result = dict(status=solver.status_name(status), seconds=solver.wall_time,
                  conflicts=solver.num_conflicts, branches=solver.num_branches,
                  retained=sorted(retained), roots=roots)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result['witness_rows'] = {str(r): [j for j in range(77) if solver.value(row[j])]
                                  for r, row in rows.items()}
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=3)
    ap.add_argument('--limit', type=int, default=9)
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    items = json.loads(SOURCE.read_text())['items']
    eligible = [x for x in items if x['compact_certificate']['smallest_incompatible_pair']]
    eligible.sort(key=lambda x: x['compact_certificate']['smallest_incompatible_pair']['total_candidates'])
    start = time.monotonic()
    output = []
    for item in eligible[:args.limit]:
        blocks = item['design']['blocks']
        roots = item['compact_certificate']['smallest_incompatible_pair']['rows']
        mandatory = set().union(*(set(blocks[r]) for r in roots))
        retained = set(range(22))
        trials = []
        # One pass is enough: feasibility is monotone when forgetting more points.
        # UNKNOWN is recorded and may prevent minimization; no minimality claim.
        for p in sorted(retained-mandatory):
            result = solve_rows(blocks, roots, retained-{p}, args.seconds)
            result['removed_trial'] = p
            trials.append(result)
            if result['status'] == 'INFEASIBLE':
                retained.remove(p)
            print(item['design']['key'][:12], 'erase', p, result['status'],
                  'retained',len(retained), 'seconds',round(result['seconds'],3), flush=True)
        record = dict(design_key=item['design']['key'], blocks=blocks, roots=roots,
                      mandatory=sorted(mandatory), retained=sorted(retained),
                      erased=sorted(set(range(22))-retained), trials=trials,
                      scope='All design extensions of retained incidence rows; full root blocks fixed')
        output.append(record)
        (OUT/'partial_boundaries.json').write_text(json.dumps(dict(results=output,
                 elapsed_seconds=time.monotonic()-start, arguments=vars(args)),indent=2))
        print('RESULT',item['design']['key'][:12], 'erased',record['erased'],flush=True)


if __name__ == '__main__':
    main()
