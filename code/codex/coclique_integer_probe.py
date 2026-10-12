"""Locate an integer coexistence obstruction in a saved population.

No claim of global exclusion: each pilot records exactly the equations used.
The LP and Boolean model share the same sparse integer input matrix.
"""
from pathlib import Path
from itertools import combinations
import argparse
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from ortools.sat.python import cp_model
from coclique_completion_certificate import equations


def probe(core, pop, folder, seconds=60):
    folder.mkdir(parents=True, exist_ok=True)
    eq, edges, rows, colours = equations(core, pop, prune_incompatible=True)
    er, ec = [], []
    for i, e in enumerate(eq):
        for j in e['variables']: er.append(i); ec.append(j)
    A = coo_matrix((np.ones(len(er)), (er, ec)), shape=(len(eq), len(edges))).tocsr()
    b = np.array([e['rhs'] for e in eq], dtype=float)
    start = time.monotonic()
    print(json.dumps(dict(stage='fractional_start', equations=len(eq), edges=len(edges))), flush=True)
    lp = linprog(np.random.default_rng(0).random(len(edges)), A_eq=A, b_eq=b,
                 bounds=(0, 1), method='highs-ds', options={'time_limit':30})
    report = dict(lp_status=lp.message, edges=len(edges), equations=len(eq), stages=[])
    if lp.x is not None:
        fractions = [j for j, x in enumerate(lp.x) if 1e-7 < x < 1-1e-7]
        report['fractional_edges'] = len(fractions)
        report['lp_values'] = lp.x.tolist()
    print(json.dumps(dict(stage='fractional_end', status=lp.status,
                         fractional=report.get('fractional_edges'))), flush=True)
    # All core-star matchings plus selected upper bounds for the remaining
    # quotas; only edges with a core common neighbour are chosen here.
    intersecting = {j for j, (u, v) in enumerate(edges) if rows[u] & rows[v]}
    for mode in ('matchings', 'matchings_packing', 'matchings_capacity', 'full'):
        model = cp_model.CpModel()
        ids = set(range(len(edges))) if mode == 'full' else intersecting
        x = {j: model.NewBoolVar(f'd{j}') for j in sorted(ids)}
        for e in eq:
            reason = e['reason']
            selected = [j for j in e['variables'] if j in ids]
            star = reason[0] == 'common_with_core' and reason[2] in rows[reason[1]]
            if mode == 'full' or star:
                model.Add(sum(x[j] for j in selected) == e['rhs'])
            elif mode != 'matchings':
                model.Add(sum(x[j] for j in selected) <= e['rhs'])
                if mode == 'matchings_capacity':
                    model.Add(sum(x[j] for j in selected) >= e['rhs']-(len(e['variables'])-len(selected)))
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 6
        solver.parameters.max_time_in_seconds = seconds
        solver.parameters.log_search_progress = True
        solver.parameters.log_to_stdout = False
        with (folder/f'{mode}.log').open('w', encoding='utf8') as log:
            solver.log_callback = lambda line: (log.write(line+'\n'), log.flush())
            status = solver.Solve(model)
        stage = dict(mode=mode, status=solver.StatusName(status), seconds=solver.WallTime(),
                     conflicts=solver.NumConflicts(), branches=solver.NumBranches(), variables=len(ids))
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            stage['chosen_edges'] = [edges[j] for j in ids if solver.Value(x[j])]
        report['stages'].append(stage)
        report['seconds'] = time.monotonic()-start
        (folder/'result.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps({k:v for k,v in stage.items() if k!='chosen_edges'}), flush=True)
        if status == cp_model.INFEASIBLE: break
    return report


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('core', type=Path); ap.add_argument('population', type=Path)
    ap.add_argument('output', type=Path); ap.add_argument('--seconds', type=float, default=60)
    args=ap.parse_args()
    probe(json.loads(args.core.read_text()), json.loads(args.population.read_text()), args.output, args.seconds)
