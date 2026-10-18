"""A necessary boundary cover with the external labels temporarily erased.

At four pairwise-grid root lines, a Gamma vertex with one internal letter
has one neighbour in each of the three disjoint internal rectangles. A
vertex with two external letters has one in all six rectangles. Enumerate
these columns, then impose the exact D D^t demands by LINEAR equations on
their multiplicities. Columns cannot repeat: they would have at least
three common neighbours. Retain the eight internal-letter classes, each
of size six, and one external class of size twelve.

Pair-intersection packing inequalities are necessary even after external
labels are erased. This is a relaxation, not a full graph construction.
Only all59 INFEASIBLE cases can exclude the four-grid-line configuration.
"""
import argparse
from collections import Counter,defaultdict
from itertools import combinations,product
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from root_component_grid4_cover import gamma_ball,PAIRS


def column_catalogues(code):
    labels,c=gamma_ball(code)
    demands={(u,v):2-len(set(labels[u])&set(labels[v]))-c[u][v]-sum(c[u][w]*c[v][w] for w in range(24))
             for u,v in combinations(range(24),2)}
    assert min(demands.values())>=0
    catalogues={}
    for axis in list(range(4))+[None]:
        groups=[i for i,pair in enumerate(PAIRS) if axis not in pair]
        rows=[]
        for values in product(range(4),repeat=len(groups)):
            support=tuple(4*i+j for i,j in zip(groups,values))
            if all(demands[tuple(sorted((u,v)))]>0 for u,v in combinations(support,2)):
                rows.append(support)
        catalogues[axis]=rows
    return labels,c,demands,catalogues


def build(code):
    from ortools.sat.python import cp_model
    labels,c,demands,catalogues=column_catalogues(code)
    model=cp_model.CpModel();columns=[];groups={};by_row=defaultdict(list);by_pair=defaultdict(list)
    for colour in list(range(8))+[None]:
        axis=None if colour is None else colour//2
        entries=[]
        for j,support in enumerate(catalogues[axis]):
            flag=model.new_bool_var(f'column_{colour}_{j}')
            entries.append((support,flag));columns.append((colour,support,flag))
            for u in support:by_row[u].append(flag)
            for pair in combinations(support,2):by_pair[pair].append(flag)
        model.add(sum(flag for _,flag in entries)==(12 if colour is None else 6))
        groups[colour]=entries
    for u in range(24):model.add(sum(by_row[u])==9)
    for pair,target in demands.items():model.add(sum(by_pair[pair])==target)
    for colour in range(8):
        for u in range(24):
            target=2-int(colour in labels[u])-int((colour^1) in labels[u])-sum(c[u][v] for v in range(24) if colour in labels[v])
            model.add(sum(flag for support,flag in groups[colour] if u in support)==target)
    packing=0
    # Equal internal letters give one common neighbour already in the old
    # root neighbourhood: their boundary columns may intersect at most once.
    for colour in range(8):
        cells=defaultdict(list)
        for support,flag in groups[colour]:
            for pair in combinations(support,2):cells[pair].append(flag)
        for flags in cells.values():model.add(sum(flags)<=1);packing+=1
    # Every pair of external columns intersects at most twice. A shared
    # triple is forbidden across all classes, including the mate classes.
    cells=defaultdict(list)
    for _,support,flag in columns:
        for triple in combinations(support,3):cells[triple].append(flag)
    for flags in cells.values():
        if len(flags)>1:model.add(sum(flags)<=1);packing+=1
    assert not model.validate(),model.validate()
    info={'column_counts':{str(k):len(v) for k,v in groups.items()},
          'variables':len(model.proto.variables),'constraints':len(model.proto.constraints),
          'packing_inequalities':packing,'external_labels_erased':True,
          'scope':__doc__}
    return model,columns,info


def check_witness(code,witness):
    labels,c,demands,_=column_catalogues(code)
    assert Counter(row['colour'] for row in witness)==dict([(a,6) for a in range(8)]+[(None,12)])
    supports=[set(row['support']) for row in witness]
    assert all(sum(u in s for s in supports)==9 for u in range(24))
    assert all(sum(u in s and v in s for s in supports)==target for (u,v),target in demands.items())
    for i,j in combinations(range(60),2):
        cap=1 if witness[i]['colour'] is not None and witness[i]['colour']==witness[j]['colour'] else 2
        assert len(supports[i]&supports[j])<=cap
    for a in range(8):
        for u in range(24):
            assert sum(u in s for s,r in zip(supports,witness) if r['colour']==a)==2-int(a in labels[u])-int((a^1) in labels[u])-sum(c[u][v] for v in range(24) if a in labels[v])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cover',type=Path);parser.add_argument('--indices',type=int,nargs='+')
    parser.add_argument('--seconds',type=float,default=30)
    parser.add_argument('--linearization',type=int,choices=(0,1,2),default=2)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();resources=limit_research_process(1)
    from ortools.sat.python import cp_model
    import threading
    cover=json.loads(args.cover.read_text());assert cover['exhaustive'] and cover['orbit_count']==59
    options={'seconds':args.seconds,'linearization':args.linearization}
    report={'scope':__doc__,'options':options,'complete_ball_count':59,'resources':resources,'records':[]}
    if args.output.exists():
        report=json.loads(args.output.read_text());assert report['options']==options
    seen={r['index'] for r in report['records']}
    for item in cover['records']:
        index=item['index']
        if index in seen or args.indices is not None and index not in args.indices:continue
        start=time.process_time();model,columns,info=build(item['representative'])
        info['build_cpu_seconds']=time.process_time()-start
        solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
        solver.parameters.cp_model_probing_level=0;solver.parameters.symmetry_level=0
        solver.parameters.linearization_level=args.linearization
        solver.parameters.max_time_in_seconds=max(600,100*args.seconds)
        start=time.process_time();done=threading.Event()
        def interrupt():
            while not done.wait(.05):
                if time.process_time()-start>=args.seconds:solver.stop_search();return
        timer=threading.Thread(target=interrupt,daemon=True);timer.start()
        try:status=solver.solve(model)
        finally:done.set();timer.join()
        row=dict(info,index=index,representative=item['representative'],status=solver.status_name(status),
                 cpu_seconds=time.process_time()-start,branches=solver.num_branches,conflicts=solver.num_conflicts)
        if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
            row['columns']=[{'colour':colour,'support':list(support)} for colour,support,flag in columns if solver.value(flag)]
            check_witness(item['representative'],row['columns'])
        report['records'].append(row)
        report['counts']=dict(Counter(r['status'] for r in report['records']))
        report['complete_cover_excluded']=len(report['records'])==59 and all(r['status']=='INFEASIBLE' for r in report['records'])
        atomic_json_write(args.output,report)
        print(json.dumps({k:row[k] for k in ('index','status','variables','build_cpu_seconds','cpu_seconds','branches','conflicts')}),flush=True)


if __name__=='__main__':main()
