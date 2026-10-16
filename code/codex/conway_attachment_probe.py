"""Build symmetry-breaking attachments and their new-star matching.

This is a construction stage, NOT a complete52-vertex graph. The44 old
vertices are not given a seed graph. We choose the eight new rows and
the perfect matching of star4, then attempt to complete each old row.
Missing old-old edges are unknown, even though zero placeholders are
used to compute necessary partial common-neighbour bounds.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

from ortools.sat.python import cp_model

sys.path.insert(0,str(Path(__file__).resolve().parent))
from conway_five_star_defect import (add_defect_cuts, measure_defects,
                                     add_attachment_demand_cuts, measure_attachment_demand,
                                     add_outside_support_cuts, measure_outside_support)
from conway_linear_explanation import explain_linear

LABELS = [p for p in combinations(range(14),2) if p[0]<5 and p[1]!=(p[0]^1)]
OLD = [i for i,p in enumerate(LABELS) if p[0]<4]
NEW = [i for i,p in enumerate(LABELS) if p[0]==4]
STAR4 = [i for i,p in enumerate(LABELS) if 4 in p]
GLOBAL_LABELS = [p for p in combinations(range(14),2) if p[1]!=(p[0]^1)]


def build_probe(global_new_rows=False,global_star=False):
    model = cp_model.CpModel()
    graph = [[0]*len(LABELS) for _ in LABELS]
    for i,j in combinations(range(len(LABELS)),2):
        selected=(i in STAR4 or j in STAR4) if global_star else (i in NEW or j in NEW or (i in STAR4 and j in STAR4))
        if selected:
            graph[i][j] = graph[j][i] = model.NewBoolVar('e_%d_%d'%(i,j))
    products = {}
    def conjunction(x,y):
        if isinstance(x,int):
            return y if x else 0
        if isinstance(y,int):
            return x if y else 0
        key = tuple(sorted((x.Index(),y.Index())))
        if key not in products:
            z = model.NewBoolVar('and_%d_%d'%key)
            model.AddMultiplicationEquality(z,[x,y])
            products[key] = z
        return products[key]
    for x in NEW:
        for r in range(14):
            target = 2-int(r in LABELS[x])-int((r^1) in LABELS[x])
            total = sum(graph[x][v] for v,p in enumerate(LABELS) if r in p)
            model.Add(total==target) if r<5 else model.Add(total<=target)
    for v in OLD:
        target = 2-int(4 in LABELS[v])-int(5 in LABELS[v])
        model.Add(sum(graph[v][x] for x in STAR4)<=target)
    for v in STAR4:
        model.Add(sum(graph[v][w] for w in STAR4)==1)
    # Common-neighbour caps for every pair involving a new vertex.
    # For old-new pairs this uses only known edges, hence is necessary.
    for i,j in combinations(range(len(LABELS)),2):
        if i not in NEW and j not in NEW:
            continue
        model.Add(graph[i][j]+sum(conjunction(graph[i][z],graph[j][z]) for z in range(len(LABELS)))
                  <=2-len(set(LABELS[i])&set(LABELS[j])))
    metadata,expressions = add_defect_cuts(model,LABELS,graph,conjunction=conjunction)
    add_attachment_demand_cuts(model,LABELS,graph,conjunction=conjunction)
    add_outside_support_cuts(model,LABELS,graph,conjunction=conjunction)
    global_rows=None
    if global_new_rows or global_star:
        local_index={p:i for i,p in enumerate(LABELS)}
        global_rows=[]
        global_indices=STAR4 if global_star else NEW
        for x in global_indices:
            row=[]
            for z,p in enumerate(GLOBAL_LABELS):
                row.append(graph[x][local_index[p]] if p in local_index else model.NewBoolVar('global_%d_%d'%(x,z)))
            global_rows.append(row)
            model.Add(sum(row)==12)
            for r in range(14):
                target=2-int(r in LABELS[x])-int((r^1) in LABELS[x])
                model.Add(sum(row[z] for z,p in enumerate(GLOBAL_LABELS) if r in p)==target)
        for z,p in enumerate(GLOBAL_LABELS):
            if 4 not in p:
                total=sum(row[z] for row in global_rows)
                model.Add(total==2-int(5 in p)) if global_star else model.Add(total<=2-int(5 in p))
        for i,j in combinations(range(len(global_indices)),2):
            model.Add(graph[global_indices[i]][global_indices[j]]+sum(conjunction(a,b) for a,b in zip(global_rows[i],global_rows[j]))==1)
    return model,graph,metadata,expressions,global_rows


def inspect_old_rows(adjacency,seconds=30,per_row=1):
    """Try necessary completions of the old rows; return an exact CP core.

    No unknown old-old edge is fixed to its placeholder value, except
    edges of the already chosen matching inside star4. INFEASIBLE for
    one row excludes this attachment pattern, irrespective of old seeds.
    """
    started = time.monotonic()
    results = []
    for vertex in OLD:
        remaining = started+seconds-time.monotonic()
        if remaining<=0:
            return dict(status='TIME_LIMIT',complete=False,rows=results)
        model = cp_model.CpModel()
        row = {}
        conditions = {}
        def condition(expression,name):
            active = model.NewBoolVar('assume_%d'%len(conditions))
            model.Add(expression).OnlyEnforceIf(active)
            model.AddAssumption(active)
            conditions[active.Index()] = name
        for q in OLD:
            if q==vertex:
                row[q]=0
            elif vertex in STAR4 and q in STAR4:
                row[q]=adjacency[vertex][q]
            else:
                row[q]=model.NewBoolVar('row_%d'%q)
            if q!=vertex:
                common = sum(adjacency[x][vertex]*adjacency[x][q] for x in NEW)
                capacity = 2-len(set(LABELS[vertex])&set(LABELS[q]))-common
                condition(row[q]<=capacity,dict(kind='old_pair_capacity',other=LABELS[q],capacity=capacity))
        for r in range(14):
            used = sum(adjacency[vertex][x] for x in NEW if r in LABELS[x])
            target = 2-int(r in LABELS[vertex])-int((r^1) in LABELS[vertex])-used
            count = sum(row[q] for q in OLD if r in LABELS[q])
            condition(count==target if r<5 else count<=target,
                      dict(kind='root_count',root=r,target=target,exact=r<5))
        degree_budget = 12-sum(adjacency[vertex][x] for x in NEW)
        condition(sum(row.values())<=degree_budget,dict(kind='degree',budget=degree_budget))
        for x in NEW:
            used = adjacency[x][vertex]+sum(adjacency[x][y]*adjacency[vertex][y] for y in NEW)
            capacity = 2-len(set(LABELS[vertex])&set(LABELS[x]))-used
            condition(sum(adjacency[x][q]*row[q] for q in OLD)<=capacity,
                      dict(kind='new_pair_capacity',new_vertex=LABELS[x],capacity=capacity))
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = min(remaining,per_row)
        status = solver.Solve(model)
        item = dict(vertex=LABELS[vertex],status=solver.StatusName(status),seconds=solver.WallTime())
        if status==cp_model.INFEASIBLE:
            core = solver.SufficientAssumptionsForInfeasibility()
            item['sufficient_core'] = [conditions[i] for i in core]
            results.append(item)
            return dict(status='NO_OLD_ROW_COMPLETION',complete=True,blocked_vertex=LABELS[vertex],rows=results)
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            item['possible_neighbours'] = [LABELS[q] for q,v in row.items() if solver.Value(v)]
        results.append(item)
    return dict(status='INDIVIDUAL_ROWS_POSSIBLE' if all(r['status'] in ('OPTIMAL','FEASIBLE') for r in results)
                else 'ROW_SEARCH_INCOMPLETE',complete=False,rows=results)


def complete_old_block(adjacency,seconds=30):
    """Join all old rows, first linearly, then with their C2 constraints."""
    started = time.monotonic()
    model = cp_model.CpModel()
    graph = [list(row) for row in adjacency]
    capacities = {}
    for i,j in combinations(OLD,2):
        common_new = sum(adjacency[i][x]*adjacency[j][x] for x in NEW)
        cap = 2-len(set(LABELS[i])&set(LABELS[j]))-common_new
        assert cap >= 0
        capacities[i,j] = cap
        if i in STAR4 and j in STAR4:
            continue
        graph[i][j] = graph[j][i] = model.NewBoolVar('old_%d_%d'%(i,j)) if cap else 0
    assumptions = {}
    def guard(name):
        variable = model.NewBoolVar('assume_%d'%len(assumptions))
        model.AddAssumption(variable)
        assumptions[variable.Index()] = name
        return variable
    for i in OLD:
        active = guard(dict(kind='old_root_counts',vertex=LABELS[i]))
        for r in range(14):
            target=2-int(r in LABELS[i])-int((r^1) in LABELS[i])
            total=sum(graph[i][v] for v,p in enumerate(LABELS) if r in p)
            (model.Add(total==target) if r<5 else model.Add(total<=target)).OnlyEnforceIf(active)
        model.Add(sum(graph[i])<=12).OnlyEnforceIf(active)
        active=guard(dict(kind='old_new_common_counts',vertex=LABELS[i]))
        for x in NEW:
            common=sum(adjacency[x][q]*graph[i][q] for q in OLD)
            common+=sum(adjacency[x][y]*adjacency[i][y] for y in NEW)
            model.Add(adjacency[x][i]+common<=2-len(set(LABELS[x])&set(LABELS[i]))).OnlyEnforceIf(active)
    stages=[]
    for stage in ('SHARED_OLD_ROWS','FULL_LOCAL_C2'):
        if stage=='FULL_LOCAL_C2':
            products={}
            def conjunction(x,y):
                if isinstance(x,int):
                    return y if x else 0
                if isinstance(y,int):
                    return x if y else 0
                key=tuple(sorted((x.Index(),y.Index())))
                if key not in products:
                    z=model.NewBoolVar('and_%d_%d'%key)
                    model.AddMultiplicationEquality(z,[x,y])
                    products[key]=z
                return products[key]
            for (i,j),cap in capacities.items():
                active=guard(dict(kind='old_old_common_counts',pair=[LABELS[i],LABELS[j]],capacity=cap))
                model.Add(graph[i][j]+sum(conjunction(graph[i][q],graph[j][q]) for q in OLD)<=cap).OnlyEnforceIf(active)
        remaining=started+seconds-time.monotonic()
        if remaining<=0:
            return dict(status='TIME_LIMIT',complete=False,stages=stages)
        solver=cp_model.CpSolver()
        solver.parameters.num_search_workers=1
        solver.parameters.max_time_in_seconds=remaining
        status=solver.Solve(model)
        item=dict(stage=stage,status=solver.StatusName(status),seconds=solver.WallTime())
        if status==cp_model.INFEASIBLE:
            core=solver.SufficientAssumptionsForInfeasibility()
            item['sufficient_core']=[assumptions[i] for i in core]
            item['integer_explanation']=explain_linear(model,assumptions,core)
            stages.append(item)
            return dict(status='ATTACHMENT_PATTERN_EXCLUDED',complete=True,stages=stages,
                        scope='This full attachment pattern and star4 matching, with every other old-old edge free.')
        stages.append(item)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            return dict(status='INCOMPLETE',complete=False,stages=stages)
    result=[[solver.Value(v) for v in row] for row in graph]
    for i,p in enumerate(LABELS):
        assert sum(result[i])<=12
        for r in range(14):
            count=sum(result[i][v] for v,q in enumerate(LABELS) if r in q)
            target=2-int(r in p)-int((r^1) in p)
            assert count<=target and (r>=5 or count==target)
    for i,j in combinations(range(len(LABELS)),2):
        common=sum(result[i][q]*result[j][q] for q in range(len(LABELS)))
        assert common+result[i][j]+len(set(LABELS[i])&set(LABELS[j]))<=2
    return dict(status='COMBINATORIAL52_CONSTRUCTED',complete=True,stages=stages,
                adjacency=result,scope='C1/C1-prime/C2 only; Gram PSD and rank conditions still required.')


def run(output,seconds=20,row_seconds=30,objective='broken',join_seconds=30,global_new_rows=False,global_star=False):
    model,graph,metadata,expressions,global_rows = build_probe(global_new_rows,global_star)
    model.Minimize(sum(expressions[0]['joint_broken']) if objective=='broken'
                   else sum(e['total'] for e in expressions))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = seconds
    status = solver.Solve(model)
    scope=('Twelve complete star4 rows on84 labels; the partial52 matrix contains all edges incident with star4. Edges among the other72 vertices remain unknown. Not a complete52 or84 graph.'
           if global_star else 'Attachments plus star4 matching; old-old edges outside that matching still unknown. Not a local52 certificate.')
    result = dict(scope=scope,
                  status=solver.StatusName(status),seconds=solver.WallTime(),objective_kind=objective,defect_cuts=metadata,
                  global_new_rows_enabled=global_new_rows,global_star_enabled=global_star)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        adjacency = [[solver.Value(v) for v in row] for row in graph]
        assert all(sum(adjacency[v][w] for w in STAR4)==1 for v in STAR4)
        # Check only our newly constructed partial incidence data.
        for i,j in combinations(range(len(LABELS)),2):
            common = sum(adjacency[i][z]*adjacency[j][z] for z in range(len(LABELS)))
            assert common+adjacency[i][j]+len(set(LABELS[i])&set(LABELS[j]))<=2
        for x in NEW:
            for r in range(14):
                count = sum(adjacency[x][v] for v,p in enumerate(LABELS) if r in p)
                target = 2-int(r in LABELS[x])-int((r^1) in LABELS[x])
                assert count<=target and (r>=5 or count==target)
        result.update(objective=int(solver.ObjectiveValue()),bound=solver.BestObjectiveBound(),
                      labels=LABELS,partial_adjacency=adjacency,
                      star4_matching=[[LABELS[i],LABELS[j]] for i,j in combinations(STAR4,2) if adjacency[i][j]],
                      defect=measure_defects(LABELS,adjacency),
                      attachment_demand=measure_attachment_demand(LABELS,adjacency))
        assert all(item['satisfied'] for item in result['attachment_demand'])
        result['outside_common_support']=measure_outside_support(LABELS,adjacency)
        assert all(item['satisfied'] for item in result['outside_common_support'])
        if global_rows is not None:
            full_rows=[[solver.Value(v) for v in row] for row in global_rows]
            global_indices=STAR4 if global_star else NEW
            for i,x in enumerate(global_indices):
                assert sum(full_rows[i])==12
                for r in range(14):
                    assert sum(full_rows[i][z] for z,p in enumerate(GLOBAL_LABELS) if r in p)==2-int(r in LABELS[x])-int((r^1) in LABELS[x])
            for i,j in combinations(range(len(global_indices)),2):
                assert adjacency[global_indices[i]][global_indices[j]]+sum(a*b for a,b in zip(full_rows[i],full_rows[j]))==1
            if global_star:
                for z,p in enumerate(GLOBAL_LABELS):
                    assert sum(row[z] for row in full_rows)==(1 if 4 in p or 5 in p else 2)
            result['global_new_rows']=dict(labels=GLOBAL_LABELS,row_labels=[LABELS[x] for x in global_indices],rows=full_rows,
                                           exact_root_and_pair_counts=True,
                                           exact_column_counts=global_star,
                                           scope='Complete rows for the listed vertices on84 labels, not a completed graph84.')
        if row_seconds:
            result['old_row_completion'] = inspect_old_rows(adjacency,row_seconds)
        if join_seconds and result.get('old_row_completion',{}).get('status')!='NO_OLD_ROW_COMPLETION':
            result['old_block_completion'] = complete_old_block(adjacency,join_seconds)
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('labels','partial_adjacency','old_row_completion','old_block_completion','defect_cuts','outside_common_support','global_new_rows')}
                     | ({'old_row_completion':{k:v for k,v in result['old_row_completion'].items() if k!='rows'}} if 'old_row_completion' in result else {})
                     | ({'old_block_completion':{k:v for k,v in result['old_block_completion'].items() if k not in ('stages','adjacency')}} if 'old_block_completion' in result else {})))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    parser.add_argument('--seconds',type=float,default=20)
    parser.add_argument('--row-seconds',type=float,default=30)
    parser.add_argument('--objective',choices=('broken','defect'),default='broken')
    parser.add_argument('--join-seconds',type=float,default=30)
    parser.add_argument('--global-new-rows',action='store_true',help='Construct the eight new rows on all84 labels, with exact root and mutual common-neighbour counts.')
    parser.add_argument('--global-star',action='store_true',help='Construct all twelve rows of L4 on84 labels, including exact column degrees and mutual common counts.')
    args=parser.parse_args()
    run(args.output,args.seconds,args.row_seconds,args.objective,args.join_seconds,args.global_new_rows,args.global_star)
