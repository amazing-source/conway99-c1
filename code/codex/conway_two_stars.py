"""Repair a global star while constructing a second complete star.

Only rows incident with the selected stars are assigned on all84 labels.
All their root counts and mutual common-neighbour equations are exact.
No other row is declared complete, and no full SRG is claimed.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_attachment_probe import build_probe, GLOBAL_LABELS, LABELS, STAR4
from conway_star_extension import read_frame
from conway_star_trades import verify_partial


def run(source, output, root=0, seconds=45, extra_labels=None):
    started = time.monotonic()
    model, _, metadata, _, base = build_probe(global_star=True)
    labels = GLOBAL_LABELS
    index = {p:i for i,p in enumerate(labels)}
    assigned = {index[LABELS[s]]:row for s,row in zip(STAR4,base)}
    added = ([index[tuple(p)] for p in extra_labels] if extra_labels is not None else
             [i for i,p in enumerate(labels) if root in p and i not in assigned])
    edges = {}
    for z in added:
        if z in assigned:
            continue
        row = []
        for q in range(84):
            if q == z:
                value = 0
            elif q in assigned:
                value = assigned[q][z]
            else:
                key = tuple(sorted((z,q)))
                if key not in edges:
                    edges[key] = model.NewBoolVar('extra_%d_%d' % key)
                value = edges[key]
            row.append(value)
        assigned[z] = row
    products = {}
    def conjunction(a,b):
        if isinstance(a,int):
            return b if a else 0
        if isinstance(b,int):
            return a if b else 0
        if a.Index() == b.Index():
            return a
        key = tuple(sorted((a.Index(),b.Index())))
        if key not in products:
            value = model.NewBoolVar('extra_and_%d_%d' % key)
            model.AddMultiplicationEquality(value,[a,b])
            products[key] = value
        return products[key]
    for z in added:
        row = assigned[z]
        model.Add(sum(row)==12)
        for r in range(14):
            model.Add(sum(row[q] for q,p in enumerate(labels) if r in p)
                      ==2-int(r in labels[z])-int((r^1) in labels[z]))
    for z,q in combinations(sorted(assigned),2):
        if z not in added and q not in added:
            continue
        model.Add(assigned[z][q]+sum(conjunction(a,b) for a,b in zip(assigned[z],assigned[q]))
                  ==2-len(set(labels[z]) & set(labels[q])))
    if added:
        for q,w in combinations(range(84),2):
            if q in assigned and w in assigned:
                continue
            edge=assigned[q][w] if q in assigned else assigned[w][q] if w in assigned else 0
            model.Add(edge+sum(conjunction(row[q],row[w]) for row in assigned.values())
                      <=2-len(set(labels[q])&set(labels[w])))
    # Exact columns whenever the second star is complete.
    selected_star=[i for i,p in enumerate(labels) if root in p]
    if all(i in assigned for i in selected_star):
        for q,p in enumerate(labels):
            model.Add(sum(assigned[z][q] for z in selected_star)==2-int(root in p)-int((root^1) in p))
    old_labels, previous = read_frame(source)
    assert old_labels == labels
    hinted = set()
    distance = []
    for z,old in previous.items():
        if z not in assigned:
            continue
        for q,bit in enumerate(old):
            var = assigned[z][q]
            if isinstance(var,int) or var.Index() in hinted:
                continue
            hinted.add(var.Index())
            model.AddHint(var,bit)
            distance.append(1-var if bit else var)
    model.Minimize(sum(distance))
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=seconds
    status=solver.Solve(model)
    result=dict(source_file=str(source),status=solver.StatusName(status),
                solver_seconds=solver.WallTime(),seconds=time.monotonic()-started,
                root=root,added_labels=[labels[z] for z in added],defect_cuts=metadata,
                scope='Complete assigned rows on84 labels only. Remaining rows unknown. No full SRG claimed.')
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        values={z:[solver.Value(v) for v in row] for z,row in assigned.items()}
        for z,row in values.items():
            assert row[z]==0 and sum(row)==12
            for r in range(14):
                assert sum(row[q] for q,p in enumerate(labels) if r in p)==2-int(r in labels[z])-int((r^1) in labels[z])
        for z,q in combinations(values,2):
            assert values[z][q]==values[q][z]
            assert sum(a*b for a,b in zip(values[z],values[q]))+values[z][q]==2-len(set(labels[z]) & set(labels[q]))
        for r in (4,root):
            star=[i for i,p in enumerate(labels) if r in p]
            if all(i in values for i in star):
                for q,p in enumerate(labels):
                    assert sum(values[z][q] for z in star)==2-int(r in p)-int((r^1) in p)
        verify_partial(labels,values)
        result.update(changed_old_star_edges=int(solver.ObjectiveValue()),best_lower_bound=solver.BestObjectiveBound(),
                      global_new_rows=dict(labels=labels,row_labels=[labels[z] for z in sorted(values)],
                                           rows=[values[z] for z in sorted(values)],exact_root_and_pair_counts=True,
                                           exact_assigned_row_check=True,all_partial_c2_caps=True))
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('global_new_rows','defect_cuts')}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--root',type=int,default=0)
    parser.add_argument('--seconds',type=float,default=45)
    parser.add_argument('--extra-labels',help='JSON list; use only these additional rows instead of a complete second star.')
    args=parser.parse_args()
    run(args.source,args.output,args.root,args.seconds,json.loads(args.extra_labels) if args.extra_labels else None)
