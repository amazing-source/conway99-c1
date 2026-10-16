"""Use all84 labels to complete a principal core's exact common-neighbour counts.

Only adjacencies from new vertices to the retained core are chosen here.
This is a necessary global projection, not a constructed graph: edges
between the missing vertices remain undecided. UNSAT excludes the core;
SAT supplies complete columns for the next Schur assembly stage.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import time

import numpy as np
from ortools.sat.python import cp_model


def run(domain_file,output,seconds=60,explain=False):
    started = time.monotonic()
    record = json.loads(Path(domain_file).read_text(encoding='utf-8'))
    root_count = record.get('root_count',14)
    second_degree = root_count-2
    core = [tuple(p) for p in record['core_labels']]
    missing = [tuple(p) for p in record['missing_labels']]
    all_labels = [p for p in combinations(range(root_count),2) if p[1] != (p[0]^1)]
    assert root_count % 2 == 0 and len(core)+len(missing) == len(all_labels)
    assert set(core).isdisjoint(missing) and set(core+missing) == set(all_labels)
    assert len(record['columns']) == len(missing)
    assert all(c['complete'] and c['domains'] for c in record['columns'])
    gamma = np.array(record['core_adjacency'],dtype=np.int64)
    domains = [entry['domains'] for entry in record['columns']]
    masks = [[sum(1 << i for i in d['neighbours']) for d in domain] for domain in domains]
    size,count = len(core),len(missing)
    model = cp_model.CpModel()
    choices = [model.NewIntVar(0,len(d)-1,'column_%d'%v) for v,d in enumerate(domains)]
    statistics = Counter()
    assumptions = {}
    def equation(terms,target,metadata):
        constraint = model.Add(sum(terms) == int(target))
        statistics[metadata['kind']] += 1
        if explain:
            gate = model.NewBoolVar('equation_%d'%len(assumptions))
            constraint.OnlyEnforceIf(gate)
            model.AddAssumption(gate)
            assumptions[gate.Index()] = dict(target=int(target),**metadata)
    def indicator(v,flags,name):
        if min(flags) == max(flags):
            return flags[0]
        variable = model.NewBoolVar(name)
        model.AddElement(choices[v],flags,variable)
        return variable
    columns = [[indicator(v,[(mask >> i)&1 for mask in masks[v]],'edge_%d_%d'%(i,v))
                for i in range(size)] for v in range(count)]
    for i,p in enumerate(core):
        equation([columns[v][i] for v in range(count)],second_degree-int(gamma[i].sum()),dict(kind='DEGREE',vertex=p))
        for r in range(root_count):
            target = 2-int(r in p)-int((r^1) in p)-sum(int(gamma[i,j]) for j,q in enumerate(core) if r in q)
            equation([columns[v][i] for v,q in enumerate(missing) if r in q],target,
                     dict(kind='ROOT_COUNT',vertex=p,root=r))
    pair_targets = {}
    for i,j in combinations(range(size),2):
        target = 2-len(set(core[i])&set(core[j]))-int(gamma[i,j])-int(gamma[i]@gamma[j])
        pair_targets[i,j] = target
        terms = [indicator(v,[int((mask >> i)&1 and (mask >> j)&1) for mask in masks[v]],
                           'common_%d_%d_col_%d'%(i,j,v)) for v in range(count)]
        equation(terms,target,dict(kind='PAIR_COUNT',vertices=[core[i],core[j]]))
    print(json.dumps(dict(stage='GLOBAL_COLUMN_MODEL',core=size,missing=count,
                          domain_sizes=[len(d) for d in domains],equations=dict(statistics),
                          build_seconds=time.monotonic()-started)),flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = max(.01,started+seconds-time.monotonic())
    status = solver.Solve(model)
    result = dict(domain_file=str(domain_file),status=solver.StatusName(status),
                  complete=status in (cp_model.OPTIMAL,cp_model.INFEASIBLE),
                  scope='Necessary complete second-neighbourhood column design on the specified principal core. New-new edges not constructed.',
                  root_count=root_count,
                  core_labels=core,missing_labels=missing,equations=dict(statistics),
                  solver_seconds=solver.WallTime(),seconds=time.monotonic()-started)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        assignment = [solver.Value(v) for v in choices]
        attachment = np.zeros((count,size),dtype=np.int64)
        for v,a in enumerate(assignment):
            attachment[v,domains[v][a]['neighbours']] = 1
        assert np.all(gamma.sum(axis=1)+attachment.sum(axis=0) == second_degree)
        for i,p in enumerate(core):
            for r in range(root_count):
                total = sum(int(gamma[i,j]) for j,q in enumerate(core) if r in q)
                total += sum(int(attachment[v,i]) for v,q in enumerate(missing) if r in q)
                assert total == 2-int(r in p)-int((r^1) in p)
        for (i,j),target in pair_targets.items():
            assert int(attachment[:,i]@attachment[:,j]) == target
        result.update(column_indices=assignment,attachment=attachment.tolist())
    elif status == cp_model.INFEASIBLE and explain:
        result['sufficient_equation_core'] = [assumptions[v] for v in solver.SufficientAssumptionsForInfeasibility()]
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('core_labels','missing_labels','attachment','column_indices','sufficient_equation_core')}),flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domains',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--seconds',type=float,default=60)
    parser.add_argument('--explain',action='store_true')
    args = parser.parse_args()
    run(args.domains,args.output,args.seconds,args.explain)
