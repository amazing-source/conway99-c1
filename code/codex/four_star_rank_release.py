"""Locate small vertex sets whose reconstruction can release one T rank.

For PSD T, deleting D lowers its rank iff a nonzero vector supported on
D lies in im T, equivalently K_T^t v=0. This is a repair design tool,
not a claim that any such repair can be completed to a Conway graph.
"""
import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np
import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_completion_columns import prepare
from hmatch_cycle_reflections import LABELS


def run(source, output, coefficient_bound=1, seconds=15, count=8):
    started = time.monotonic()
    gamma, t8, u15, kt, ku = prepare(json.loads(Path(source).read_text(encoding='utf-8')))
    model = cp_model.CpModel()
    v = [model.NewIntVar(-coefficient_bound, coefficient_bound, 'v_%d'%i) for i in range(44)]
    support = [model.NewBoolVar('support_%d'%i) for i in range(44)]
    for x, present in zip(v, support):
        model.Add(x == 0).OnlyEnforceIf(present.Not())
        model.Add(x != 0).OnlyEnforceIf(present)
    for q in kt.T:
        model.Add(sum(int(c)*x for c, x in zip(q, v)) == 0)
    model.Add(sum(support) >= 1)
    model.Minimize(sum(support))
    entries = []
    for attempt in range(count):
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = max(.01, started+seconds-time.monotonic())
        status = solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break
        vector = np.array([solver.Value(x) for x in v], dtype=object)
        removed = np.flatnonzero(vector).tolist()
        core = [i for i in range(44) if i not in removed]
        assert not np.any(kt.T@vector)
        # For PSD A, rank(A_CC)=rank(A)-|D|+rank(K_A[D,:]).
        # Only the tiny deleted-row kernel profile needs elimination.
        t_rank = 44-kt.shape[1]-len(removed)+len(sp.Matrix(kt[removed].tolist()).rref()[1])
        u_rank = 44-ku.shape[1]-len(removed)+len(sp.Matrix(ku[removed].tolist()).rref()[1])
        entry = dict(removed_indices=removed, removed_labels=[LABELS[i] for i in removed],
                     core_indices=core, range_vector=list(map(int, vector)),
                     core_T_rank=t_rank, core_U_rank=u_rank,
                     T_rank_budget=30-t_rank, U_rank_budget=40-u_rank,
                     minimum_support_proved_in_coefficient_box=status == cp_model.OPTIMAL,
                     solver_status=solver.StatusName(status), solver_seconds=solver.WallTime())
        entries.append(entry)
        print(json.dumps({k: val for k, val in entry.items() if k not in ('range_vector', 'core_indices')}), flush=True)
        # Ask for genuinely different repair vertices, not just a new sign.
        model.AddBoolOr([x.Not() if i in removed else x for i, x in enumerate(support)])
        if time.monotonic() >= started+seconds:
            break
    result = dict(source_file=str(source), coefficient_bound=coefficient_bound,
                  repairs=entries, seconds=time.monotonic()-started,
                  scope='Small bounded-integer dependencies choose repair supports. No minimum over arbitrary rational coefficients is asserted.')
    Path(output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result


def follow_obstruction(source, obstruction_file, output):
    """Release neighbours of forced old vertices named by a Schur cut."""
    gamma, _, _, kt, ku = prepare(json.loads(Path(source).read_text(encoding='utf-8')))
    previous = json.loads(Path(obstruction_file).read_text(encoding='utf-8'))
    removed_before = set(range(44))-set(previous['core_indices'])
    assembly = previous['assembly']
    witness = assembly['rank_cuts'][0]['labels'] if assembly.get('rank_cuts') else assembly['empty_pair']
    entries = []
    for p in witness:
        label = tuple(p)
        if label not in LABELS:
            continue
        vertex = LABELS.index(label)
        extra = set(map(int,np.flatnonzero(gamma[vertex])))-removed_before
        if not extra:
            continue
        removed = sorted(removed_before|extra)
        rt = 44-kt.shape[1]-len(removed)+len(sp.Matrix(kt[removed].tolist()).rref()[1])
        ru = 44-ku.shape[1]-len(removed)+len(sp.Matrix(ku[removed].tolist()).rref()[1])
        entry = dict(removed_indices=removed,removed_labels=[LABELS[i] for i in removed],
                     core_indices=[i for i in range(44) if i not in removed],
                     core_T_rank=rt,core_U_rank=ru,T_rank_budget=30-rt,U_rank_budget=40-ru,
                     obstructing_vertex=label,newly_released_labels=[LABELS[i] for i in sorted(extra)])
        entries.append(entry)
        print(json.dumps({k:v for k,v in entry.items() if k not in ('core_indices',)}),flush=True)
    result = dict(source_file=str(source),obstruction_file=str(obstruction_file),repairs=entries,
                  scope='Targeted neighbourhood release following an exact Schur obstruction, without a minimum claim.')
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--bound', type=int, default=1)
    parser.add_argument('--seconds', type=float, default=15)
    parser.add_argument('--count', type=int, default=8)
    parser.add_argument('--follow-obstruction')
    args = parser.parse_args()
    if args.follow_obstruction:
        follow_obstruction(args.source,args.follow_obstruction,args.output)
    else:
        run(args.source, args.output, args.bound, args.seconds, args.count)
