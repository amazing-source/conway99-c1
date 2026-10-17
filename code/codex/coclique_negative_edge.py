"""The common neighbour of an isolated negative edge forces a small f-factor.

For profile a=0,e=2 all its zero-charge neighbours have type {H_i} or
{L_j,L_k}. The latter types must form a simple graph with exact degrees.
"""
from pathlib import Path
from itertools import combinations
import argparse
import json
import time

from ortools.sat.python import cp_model
from coclique_defect_gluing import gluing_data


def probe(core):
    d=gluing_data(core);q=d['charges'];rows=d['rows'];n=len(q)
    assert sorted(q)==[-1]*2+[1]*12+[2]*4
    negative=sum(1<<i for i,v in enumerate(q) if v<0)
    targets=[[2-((r>>i)&1)-(r&d['neighbours'][i]).bit_count() for i in range(n)] for r in rows]
    zero=[sum(1<<i for i,v in enumerate(h) if v==0) for h in targets]
    lookup={r:t for t,r in enumerate(rows)}
    results=[];started=time.monotonic()
    for root,r in enumerate(rows):
        if r&negative!=negative:continue
        h=targets[root]
        allowed=[t for t,s in enumerate(rows) if (r&s).bit_count()<=1 and not(s&zero[root]) and not(r&zero[t])]
        assert all(not(rows[t]&negative) for t in allowed)
        singleton_fail=[i for i in range(n) if q[i]==2 and h[i] and lookup.get(1<<i) not in allowed]
        if singleton_fail:
            results.append(dict(root=[i for i in range(n) if r>>i&1],status='NO_SINGLETON_SUPPORT',vertices=singleton_fail));continue
        edges=[]
        for t in allowed:
            s=rows[t]
            if s.bit_count()==2:
                v=[i for i in range(n) if s>>i&1]
                assert all(q[i]==1 for i in v)
                edges.append((t,*v))
            else:
                assert s.bit_count()==1
        model=cp_model.CpModel();bits=[model.NewBoolVar(f'e{u}_{v}') for t,u,v in edges]
        for i in range(n):
            if q[i]==1:
                model.Add(sum(bits[j] for j,(_,u,v) in enumerate(edges) if i in (u,v))==h[i])
        solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
        status=solver.Solve(model)
        entry=dict(root=[i for i in range(n) if r>>i&1],status=solver.StatusName(status))
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            selected=[[i] for i in range(n) if q[i]==2 for _ in range(h[i])]
            selected += [[u,v] for j,(_,u,v) in enumerate(edges) if solver.Value(bits[j])]
            assert len(selected)==14-r.bit_count()
            assert all(sum(i in s for s in selected)==h[i] for i in range(n))
            entry['zero_neighbour_types']=selected
        results.append(entry)
    return dict(roots=len(results),feasible=sum(r['status']=='OPTIMAL' for r in results),
                complete=True,seconds=time.monotonic()-started,results=results,
                scope='Necessary common-neighbour f-factor of this fixed defect core')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('core',type=Path);args=ap.parse_args()
    report=probe(json.loads(args.core.read_text()))
    args.core.with_name(args.core.stem+'_negative_edge.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('roots','feasible','complete','seconds')}),flush=True)
