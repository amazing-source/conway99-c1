"""Bounded necessary extension test for a mate hexagon in the co-Heawood branch."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np
from ortools.sat.python import cp_model
from coheawood_probe import core_with_rows


def run(chord):
    a, _, b, _ = core_with_rows()
    ss = [0,1,3]
    tt = [next(t for t in range(7) if not b[ss[i]][t] and not b[ss[(i+1)%3]][t])
          for i in range(3)]
    labs = [(ss[0],tt[0]),(ss[1],tt[0]),(ss[1],tt[1]),
            (ss[2],tt[1]),(ss[2],tt[2]),(ss[0],tt[2])]
    h = np.zeros((20,20), dtype=int)
    h[:14,:14] = a[:14,:14]
    for k,(s,t) in enumerate(labs):
        h[14+k,s] = h[s,14+k] = 1
        h[14+k,7+t] = h[7+t,14+k] = 1
        j = 14+(k+1)%6
        h[14+k,j] = h[j,14+k] = 1
    if chord:
        h[14,17] = h[17,14] = 1
    deficit = 2-h-h@h
    types = []
    groups = {}
    sizes = {}
    for cell in [(s,t) for s in range(7) for t in range(7)] + [('z',)]:
        count = 15 if cell == ('z',) else 2-b[cell[0]][cell[1]]-labs.count(cell)
        sizes[cell] = count
        if count == 0:
            continue
        groups[cell] = []
        for mask in range(64):
            x = np.zeros(20, dtype=int)
            if cell != ('z',):
                x[cell[0]] = x[7+cell[1]] = 1
            for k in range(6):
                x[14+k] = (mask>>k)&1
            support = list(np.flatnonzero(x))
            if any(deficit[u,v] <= 0 for u,v in combinations(support,2)):
                continue
            if np.any(h@x > 2-x):
                continue
            groups[cell].append(len(types))
            types.append((cell,mask,x))
    model = cp_model.CpModel()
    ns = [model.NewIntVar(0, sizes[cell], f'n_{i}') for i,(cell,mask,x) in enumerate(types)]
    for cell, ids in groups.items():
        model.Add(sum(ns[i] for i in ids) == sizes[cell])
        if cell != ('z',) and sizes[cell] == 2:
            for k in range(6):
                model.Add(sum(ns[i] for i in ids if types[i][1]>>k&1) <= 1)
        if cell == ('z',):
            for i in ids:
                if types[i][1].bit_count() >= 3:
                    model.Add(ns[i] <= 1)
    for u in range(20):
        model.Add(sum(ns[i] for i,(_,_,x) in enumerate(types) if x[u]) == 14-int(h[u].sum()))
    for u,v in combinations(range(20),2):
        model.Add(sum(ns[i] for i,(_,_,x) in enumerate(types) if x[u] and x[v]) == int(deficit[u,v]))
    for k in range(6):
        model.Add(sum(ns[i] for i,(cell,mask,x) in enumerate(types)
                      if cell==('z',) and x[14+k]) == 3)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    solver.parameters.num_search_workers = 4
    status = solver.Solve(model)
    report = dict(chord=chord, status=solver.StatusName(status), mask_types=len(types),
                  seconds=solver.WallTime(), scope='necessary extension moments, not full completion')
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        report['selected'] = [dict(cell=cell,mask=mask,count=solver.Value(ns[i]))
                              for i,(cell,mask,x) in enumerate(types) if solver.Value(ns[i])]
    print(json.dumps({k:v for k,v in report.items() if k!='selected'}), flush=True)
    return report


if __name__ == '__main__':
    out = Path(__file__).resolve().parents[2]/'data/codex_coheawood/hexagon_masks.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps([run(False),run(True)],indent=2)+'\n',encoding='utf-8')
