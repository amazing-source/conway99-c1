"""Enumerate complete single-row domains and expose pair incompatibilities.

For rows in one star, compatibility requires symmetric adjacency and
the exact common-neighbour count (1-edge). Individual partial C2 caps
then remain valid together: two rows of the same star cannot share two
neighbours, so cannot both consume capacity at any other vertex pair.
The final combined matrix is still checked directly. Enumeration is
marked complete only on OPTIMAL/INFEASIBLE, never on a time/size limit.
"""
import argparse
from collections import Counter
from itertools import combinations,product
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

sys.path.insert(0,str(Path(__file__).resolve().parent))
from conway_star_extension import read_frame,build_extension
from conway_star_trades import verify_partial


def enumerate_row(labels,fixed,z,seconds=5,limit=1000):
    model,rows,_=build_extension(labels,fixed,[z])
    domain=[]
    class Collector(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            domain.append([self.Value(v) for v in rows[z]])
            if len(domain)>=limit:
                self.StopSearch()
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=seconds
    solver.parameters.enumerate_all_solutions=True
    status=solver.Solve(model,Collector())
    assert len({tuple(r) for r in domain})==len(domain)
    for row in domain:
        combined=dict(fixed)
        combined[z]=row
        verify_partial(labels,combined)
    return dict(label=labels[z],status=solver.StatusName(status),seconds=solver.WallTime(),
                complete=status in (cp_model.OPTIMAL,cp_model.INFEASIBLE),rows=domain,count=len(domain))


def run(source,output,targets,seconds=5,limit=1000):
    labels,fixed=read_frame(source)
    ids=[labels.index(tuple(p)) for p in targets]
    assert all(i not in fixed for i in ids)
    assert set.intersection(*(set(labels[z]) for z in ids)), 'Targets must lie in one star.'
    domains=[enumerate_row(labels,fixed,z,seconds,limit) for z in ids]
    for item in domains:
        print(json.dumps({k:v for k,v in item.items() if k!='rows'}),flush=True)
    pairs=[]
    for i,j in combinations(range(len(ids)),2):
        z,q=ids[i],ids[j]
        histogram=Counter()
        compatible=[]
        for a,b in product(range(len(domains[i]['rows'])),range(len(domains[j]['rows']))):
            x,y=domains[i]['rows'][a],domains[j]['rows'][b]
            if x[q]!=y[z]:
                histogram['asymmetric_edge']+=1
                continue
            common=sum(u*v for u,v in zip(x,y))
            if common+x[q]!=1:
                histogram['common_%d_edge_%d'%(common,x[q])]+=1
                continue
            combined=dict(fixed)
            combined.update({z:x,q:y})
            verify_partial(labels,combined)
            compatible.append([a,b])
        item=dict(labels=[labels[z],labels[q]],complete=domains[i]['complete'] and domains[j]['complete'],
                  domain_sizes=[domains[i]['count'],domains[j]['count']],
                  incompatible_reasons=dict(histogram),compatible_choices=compatible)
        pairs.append(item)
        print(json.dumps(item),flush=True)
    result=dict(source_file=str(source),labels=labels,domains=domains,pairs=pairs,
                scope='Exact domains conditional on the fixed frame. Completeness flags are part of each verdict.')
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--targets',required=True,help='JSON array of row labels.')
    parser.add_argument('--seconds',type=float,default=5)
    parser.add_argument('--limit',type=int,default=1000)
    args=parser.parse_args()
    run(args.source,args.output,json.loads(args.targets),args.seconds,args.limit)
