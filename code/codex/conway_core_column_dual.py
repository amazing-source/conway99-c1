"""Extract an integer separating inequality for the global column design.

For every missing label p choose one feature vector f_p(d) from its
complete domain. A certificate y satisfies
    sum_p min_d <y,f_p(d)> > <y,target>.
Thus even fractional mixtures of columns are impossible. GLOP proposes
y; the separating margin and every domain minimum are computed in Z.
"""
import argparse
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import time

import numpy as np
from ortools.linear_solver import pywraplp


def features(record):
    core,missing = record['core_labels'],record['missing_labels']
    root_count=record.get('root_count',14)
    gamma = np.array(record['core_adjacency'],dtype=np.int64)
    size = len(core)
    labels={p for p in combinations(range(root_count),2) if p[1] != (p[0]^1)}
    assert set(map(tuple,core+missing)) == labels and len(core)+len(missing) == len(labels)
    assert len(record['columns']) == len(missing)
    assert all(c['complete'] and c['domains'] for c in record['columns'])
    metadata,targets = [],[]
    degree,root,pair = {},{},{}
    def add(key,table,target,**description):
        table[key] = len(targets)
        targets.append(int(target))
        metadata.append(description)
    for i,p in enumerate(core):
        add(i,degree,root_count-2-int(gamma[i].sum()),kind='DEGREE',vertex=p)
        for r in range(root_count):
            target=2-int(r in p)-int((r^1) in p)-sum(int(gamma[i,j]) for j,q in enumerate(core) if r in q)
            add((i,r),root,target,kind='ROOT_COUNT',vertex=p,root=r)
    for i,j in combinations(range(size),2):
        target=2-len(set(core[i])&set(core[j]))-int(gamma[i,j])-int(gamma[i]@gamma[j])
        add((i,j),pair,target,kind='PAIR_COUNT',vertices=[core[i],core[j]])
    vectors=[]
    for p,column in zip(missing,record['columns']):
        group=[]
        for d in column['domains']:
            neighbours=sorted(d['neighbours'])
            indices=[degree[i] for i in neighbours]
            indices += [root[i,r] for i in neighbours for r in p]
            indices += [pair[i,j] for i,j in combinations(neighbours,2)]
            group.append(indices)
        vectors.append(group)
    return metadata,targets,vectors


class ColumnPropagation:
    """Exact bounds propagation on the multiple-choice feature equations."""
    def __init__(self,targets,vectors,forbidden=()):
        self.targets=targets
        self.full=[(1<<len(group))-1 for group in vectors]
        self.ones=[{} for _ in targets]
        self.forbidden=list(forbidden)
        for p,group in enumerate(vectors):
            for d,indices in enumerate(group):
                for i in indices:
                    self.ones[i][p]=self.ones[i].get(p,0)|(1<<d)

    def run(self,fixed,initial=None):
        live=self.full.copy() if initial is None else initial.copy()
        for p,d in fixed.items(): live[p]=1<<d
        trace=[]
        changed=True
        while changed:
            changed=False
            for certificate,assignment in enumerate(self.forbidden):
                if any(not (live[p]>>d&1) for p,d in assignment):
                    continue
                free=[(p,d) for p,d in assignment if live[p] != 1<<d]
                if not free:
                    return live,trace,dict(kind='INTEGER_SEPARATOR',certificate=certificate)
                if len(free)==1:
                    p,d=free[0]
                    live[p] ^= 1<<d
                    assert live[p]
                    trace.append(dict(certificate=certificate,column=p,removed_mask=str(1<<d),bound='FORBIDDEN_ASSIGNMENT'))
                    changed=True
            for i,(target,row) in enumerate(zip(self.targets,self.ones)):
                bounds=[(p,int(live[p]&mask==live[p]),int(bool(live[p]&mask)),mask) for p,mask in row.items()]
                lower=sum(b[1] for b in bounds); upper=sum(b[2] for b in bounds)
                if target < lower or target > upper:
                    return live,trace,dict(equation=i,target=target,lower=lower,upper=upper)
                if target not in (lower,upper): continue
                tight_lower=target==lower
                for p,lo,hi,mask in bounds:
                    if lo==hi: continue
                    new=live[p]&(~mask if tight_lower else mask)
                    assert new
                    trace.append(dict(equation=i,column=p,removed_mask=str(live[p]^new),
                                      bound='LOWER' if tight_lower else 'UPPER'))
                    live[p]=new
                    changed=True
        return live,trace,None


def run(domain_file,output,seconds=30,fixed=None):
    started=time.monotonic()
    record=json.loads(Path(domain_file).read_text(encoding='utf-8'))
    metadata,targets,vectors=features(record)
    fixed = fixed or {}
    for p,choice in fixed.items():
        vectors[p] = [vectors[p][choice]]
    solver=pywraplp.Solver.CreateSolver('GLOP')
    solver.SetTimeLimit(int(seconds*1000))
    y=[solver.NumVar(-1,1,'y%d'%i) for i in range(len(targets))]
    z=[solver.NumVar(-solver.infinity(),solver.infinity(),'minimum%d'%p) for p in range(len(vectors))]
    for p,group in enumerate(vectors):
        for indices in group:
            constraint=solver.Constraint(-solver.infinity(),0)
            constraint.SetCoefficient(z[p],1)
            for i in indices:
                constraint.SetCoefficient(y[i],-1)
    objective=solver.Objective()
    for variable,target in zip(y,targets): objective.SetCoefficient(variable,-target)
    for variable in z: objective.SetCoefficient(variable,1)
    objective.SetMaximization()
    status=solver.Solve()
    result=dict(domain_file=str(domain_file),solver_status=int(status),seconds=time.monotonic()-started,
                status='NO_INTEGER_SEPARATOR_OBTAINED',complete=False,
                fixed_columns=[dict(label=record['missing_labels'][p],domain_index=d) for p,d in fixed.items()])
    if status in (pywraplp.Solver.OPTIMAL,pywraplp.Solver.FEASIBLE):
        result['proposed_margin']=objective.Value()
        raw=[v.solution_value() for v in y]
        for scale in (1,2,3,4,6,10,12,24,60,120,1000,10000,1000000):
            weights=[round(scale*v) for v in raw]
            divisor=gcd(*weights)
            if not divisor: continue
            weights=[w//divisor for w in weights]
            minima=[min(sum(weights[i] for i in indices) for indices in group) for group in vectors]
            target_value=sum(w*t for w,t in zip(weights,targets))
            margin=sum(minima)-target_value
            if margin > 0:
                result.update(status='EXACT_GLOBAL_COLUMN_SEPARATOR',complete=True,margin=margin,
                              sum_domain_minima=sum(minima),target_value=target_value,
                              inequality='sum_p min_d <y,f_p(d)> > <y,target>',
                              weights=[dict(equation_index=i,weight=w,target=targets[i],**metadata[i])
                                       for i,w in enumerate(weights) if w],
                              domain_minima=[dict(label=p,minimum=m,domain_size=len(group))
                                             for p,m,group in zip(record['missing_labels'],minima,vectors)])
                break
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('weights','domain_minima')}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--domains',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--seconds',type=float,default=30)
    parser.add_argument('--branch-label',action='append',help='Split on this label; repeat for deeper levels. Existing matching child certificates are reused.')
    args=parser.parse_args()
    if args.branch_label:
        record=json.loads(Path(args.domains).read_text(encoding='utf-8'))
        branch_labels=[list(map(int,p.split(','))) for p in args.branch_label]
        def split(level,fixed,suffix):
            label=branch_labels[level]
            p=record['missing_labels'].index(label)
            results=[]
            for choice in range(len(record['columns'][p]['domains'])):
                child_suffix=suffix+'_choice%d'%choice
                child=Path(args.output).with_name(Path(args.output).stem+child_suffix+'.json')
                current={**fixed,p:choice}
                expected=[dict(label=record['missing_labels'][v],domain_index=d) for v,d in current.items()]
                result=json.loads(child.read_text(encoding='utf-8')) if child.exists() else None
                if not result or result.get('domain_file') != args.domains or result.get('fixed_columns') != expected:
                    result=run(args.domains,child,args.seconds,current)
                entry=dict(domain_index=choice,status=result['status'],certificate_file=str(child),complete=result['complete'])
                if not entry['complete'] and level+1 < len(branch_labels):
                    entry['subtree']=split(level+1,current,child_suffix)
                    entry['complete']=entry['subtree']['complete']
                results.append(entry)
            return dict(branch_label=label,complete=all(r['complete'] for r in results),branches=results)
        tree=dict(domain_file=args.domains,**split(0,{},''))
        Path(args.output).write_text(json.dumps(tree,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(dict(status='EXACT_SPLIT_REFUTATION' if tree['complete'] else 'SPLIT_INCOMPLETE',tree_file=args.output)),flush=True)
    else:
        run(args.domains,args.output,args.seconds)
