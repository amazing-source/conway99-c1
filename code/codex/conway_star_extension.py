"""Complete further rows of a fixed global star, with exact explanations.

Only assigned rows are known. A successful relaxation is not a graph84.
For a new row z and an old star vertex p, the common-neighbour equation
is linear, since the entire row of p is already given. These equations
are recorded by guards so an obstruction can be turned into a small
integer argument. No old44 graph, PSD condition, or symmetry is assumed.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from conway_linear_explanation import explain_linear


def read_frame(source):
    record = json.loads(Path(source).read_text(encoding='utf-8'))
    frame = record.get('global_new_rows', record)
    labels = [tuple(p) for p in frame['labels']]
    index = {p: i for i, p in enumerate(labels)}
    row_labels = frame.get('row_labels', frame.get('star_labels'))
    rows = {index[tuple(p)]: list(row) for p, row in zip(row_labels, frame['rows'])}
    return labels, rows


def build_extension(labels, fixed, selected, pair_constraints=False):
    n = len(labels)
    selected = sorted(set(selected) - set(fixed))
    model = cp_model.CpModel()
    rows = {z: list(row) for z, row in fixed.items()}
    variables = {}
    for z in selected:
        row = []
        for q in range(n):
            if q == z:
                value = 0
            elif q in fixed:
                value = fixed[q][z]
            else:
                key = tuple(sorted((z, q)))
                if key not in variables:
                    variables[key] = model.NewBoolVar('e_%d_%d' % key)
                value = variables[key]
            row.append(value)
        rows[z] = row
    guards = {}
    def guarded(expr, description):
        active = model.NewBoolVar('assume_%d' % len(guards))
        model.Add(expr).OnlyEnforceIf(active)
        model.AddAssumption(active)
        guards[active.Index()] = description

    for z in selected:
        model.Add(sum(rows[z]) == 12)
        for r in range(14):
            target = 2 - int(r in labels[z]) - int((r ^ 1) in labels[z])
            guarded(sum(rows[z][q] for q, p in enumerate(labels) if r in p) == target,
                    dict(kind='root', row=labels[z], root=r, target=target))
        for p, prow in fixed.items():
            target = 2 - len(set(labels[z]) & set(labels[p])) - prow[z]
            guarded(sum(rows[z][q] for q in range(n) if prow[q]) == target,
                    dict(kind='common', row=labels[z], other=labels[p], target=target))
        for q in range(n):
            if q == z or q in fixed:
                continue
            common_fixed = sum(row[z] * row[q] for row in fixed.values())
            capacity = 2 - len(set(labels[z]) & set(labels[q])) - common_fixed
            if capacity < 1:
                guarded(rows[z][q] <= capacity,
                        dict(kind='known_common_cap', row=labels[z], other=labels[q],
                             common_fixed=common_fixed, capacity=capacity))
        # A new common neighbour cannot be added to a pair whose two
        # available common neighbours are already roots or fixed rows.
        # This includes pairs of still unassigned vertices, not only
        # pairs involving the new row itself.
        remaining = [q for q in range(n) if q != z]
        for q,w in combinations(remaining,2):
            known_edge = fixed[q][w] if q in fixed else fixed[w][q] if w in fixed else 0
            used = known_edge + len(set(labels[q]) & set(labels[w])) + sum(row[q]*row[w] for row in fixed.values())
            if used > 2:
                model.Add(0 == 1)
            elif used == 2:
                guarded(rows[z][q] + rows[z][w] <= 1,
                        dict(kind='saturated_pair', row=labels[z], pair=[labels[q],labels[w]], used=used))
    products = {}
    def conjunction(a, b):
        if isinstance(a, int):
            return b if a else 0
        if isinstance(b, int):
            return a if b else 0
        if a.Index() == b.Index():
            return a
        key = tuple(sorted((a.Index(), b.Index())))
        if key not in products:
            value = model.NewBoolVar('and_%d_%d' % key)
            model.AddMultiplicationEquality(value, [a, b])
            products[key] = value
        return products[key]
    if pair_constraints:
        for z, q in combinations(selected, 2):
            model.Add(rows[z][q] + sum(conjunction(a, b) for a, b in zip(rows[z], rows[q]))
                      == 2 - len(set(labels[z]) & set(labels[q])))
        # The complete partial matrix must also respect capacities at
        # every pair of vertices whose rows remain unassigned.
        for q,w in combinations(range(n),2):
            if q in rows and w in rows:
                continue
            used=sum(row[q]*row[w] for row in fixed.values())
            known_edge=rows[q][w] if q in rows else rows[w][q] if w in rows else 0
            model.Add(known_edge+sum(conjunction(rows[z][q],rows[z][w]) for z in selected)
                      <=2-len(set(labels[q])&set(labels[w]))-used)
    return model, rows, guards


def solve_selected(labels, fixed, selected, seconds=10, pair_constraints=False):
    model, rows, guards = build_extension(labels, fixed, selected, pair_constraints)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = seconds
    status = solver.Solve(model)
    result = dict(status=solver.StatusName(status), seconds=solver.WallTime(),
                  row_labels=[labels[z] for z in selected], mutual_c2=pair_constraints)
    if status == cp_model.INFEASIBLE:
        active = list(solver.SufficientAssumptionsForInfeasibility())
        result['sufficient_core'] = [guards[g] for g in active]
        result['linear_explanation'] = explain_linear(model, guards, active)
    elif status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = {z: [solver.Value(v) for v in rows[z]] for z in selected}
        for z, row in values.items():
            assert row[z] == 0 and sum(row) == 12
            for r in range(14):
                assert sum(row[q] for q, p in enumerate(labels) if r in p) == 2-int(r in labels[z])-int((r^1) in labels[z])
            for p, prow in fixed.items():
                assert row[p] == prow[z]
                assert sum(a*b for a, b in zip(row, prow)) + row[p] == 2-len(set(labels[z]) & set(labels[p]))
        for z, q in combinations(selected, 2):
            assert values[z][q] == values[q][z]
            if pair_constraints:
                assert sum(a*b for a,b in zip(values[z], values[q])) + values[z][q] == 2-len(set(labels[z]) & set(labels[q]))
        result.update(rows=[values[z] for z in selected], exact_row_check=True)
        if pair_constraints or len(selected)==1:
            combined=dict(fixed)
            combined.update(values)
            for q,w in combinations(range(len(labels)),2):
                common=sum(row[q]*row[w] for row in combined.values())
                edge=combined[q][w] if q in combined else combined[w][q] if w in combined else 0
                assert common+edge+len(set(labels[q])&set(labels[w]))<=2
            result['all_partial_c2_caps']=True
    return result


def run(source, output, root=0, seconds=20, mode='individual'):
    labels, fixed = read_frame(source)
    selected = [i for i, p in enumerate(labels) if i not in fixed and (root < 0 or root in p)]
    started = time.monotonic()
    results = []
    if mode == 'individual':
        for z in selected:
            result = solve_selected(labels, fixed, [z], seconds=seconds)
            results.append(result)
            print(json.dumps({k:v for k,v in result.items() if k not in ('rows','sufficient_core','linear_explanation')}), flush=True)
    else:
        results.append(solve_selected(labels, fixed, selected, seconds=seconds,
                                      pair_constraints=(mode == 'complete')))
        print(json.dumps({k:v for k,v in results[-1].items() if k not in ('rows','sufficient_core','linear_explanation')}), flush=True)
    result = dict(source_file=str(source), mode=mode, root=root, labels=labels,
                  fixed_row_labels=[labels[z] for z in fixed], results=results,
                  seconds=time.monotonic()-started,
                  scope='Only the listed rows are completed, if feasible; other rows remain unknown.')
    Path(output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result


def grow(source,output,root=0,seconds=5,max_subsets=64):
    """Find the largest compatible subset within one additional star.

    Optimality is only asserted for this fixed frame and this relaxation,
    after every larger subset has actually been excluded. UNKNOWN remains
    open; it never excludes a row or a subset.
    """
    labels,fixed=read_frame(source)
    selected=[i for i,p in enumerate(labels) if root in p and i not in fixed]
    individuals=[]
    candidates=[]
    for z in selected:
        item=solve_selected(labels,fixed,[z],seconds)
        individuals.append(item)
        if item['status']!='INFEASIBLE':
            candidates.append(z)
    attempts=[]
    all_larger_closed=True
    chosen=None
    for size in range(len(candidates),0,-1):
        for subset in combinations(candidates,size):
            if len(attempts)>=max_subsets:
                break
            item=solve_selected(labels,fixed,list(subset),seconds,pair_constraints=True)
            attempts.append(dict(row_labels=[labels[z] for z in subset],status=item['status'],seconds=item['seconds']))
            print(json.dumps(attempts[-1]),flush=True)
            if 'rows' in item:
                chosen=(subset,item)
                break
            if item['status']!='INFEASIBLE':
                all_larger_closed=False
        if chosen or len(attempts)>=max_subsets:
            break
    result=dict(source_file=str(source),root=root,individuals=individuals,attempts=attempts,
                scope='Additional rows within one star, with the given frame FIXED. Other unassigned edges remain unknown.')
    if chosen:
        subset,item=chosen
        rows=dict(fixed)
        rows.update(zip(subset,item['rows']))
        result.update(status='ADDITIONAL_ROWS_CONSTRUCTED',additional_row_count=len(subset),
                      maximum_for_fixed_frame_proved=all_larger_closed,
                      global_new_rows=dict(labels=labels,row_labels=[labels[z] for z in sorted(rows)],
                                           rows=[rows[z] for z in sorted(rows)],
                                           exact_root_and_pair_counts=True,all_partial_c2_caps=True))
    else:
        result['status']='NO_EXTENSION_IN_SEARCH' if all_larger_closed and len(attempts)<max_subsets else 'SUBSET_SEARCH_INCOMPLETE'
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('individuals','attempts','global_new_rows')}),flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--root', type=int, default=0)
    parser.add_argument('--seconds', type=float, default=10)
    parser.add_argument('--mode', choices=('individual','linear','complete','grow'), default='individual')
    args = parser.parse_args()
    if args.mode=='grow':
        grow(args.source,args.output,args.root,args.seconds)
    else:
        run(args.source, args.output, args.root, args.seconds, args.mode)
