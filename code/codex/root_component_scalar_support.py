"""Necessary 45-vertex support for an e(Q)=1 diagonal with a four-neighbour.

This is a universal necessary model, with no minimum-component assumption.
It is NOT an arbitrary support-size truncation: the integer -4 eigenvector
h=T 1_Q has norm 42. If h(w)=-3, its entire nonzero support is forced into
28 vertices. Adding N[o] and the two zero-valued partners gives 45 vertices.
Only INFEASIBLE excludes the configuration; a solution is not a Conway graph.

Reduction: N(w) is a matching of seven edges. The Q endpoints have h=1,1,
the Q isolates h=2,2. Their two matching partners have h<=0, and the two
original labels have h=0. The remaining six values are <=1, hence Ah(w)=12
forces all six to be 1 and both partners to be 0. For the complement of
N[w], let p be the number of positive entries and n_i the number of -i.
All positives there are 1, and norm/sum give p+n_2+3n_3=4. Summing Ah=-4h
over the ten positives in N(w) forces at least 24 weighted incidences to
negative vertices outside N[w]. Each of those has two neighbours in N(w),
so 24<=2(9+p), hence p>=3. If p=3, a vertex of value -2 would need positive
neighbour-weight >=8 but has at most 4 inside N(w) and 3 outside. Thus
p=4, n_2=n_3=0: exactly thirteen -1 entries outside N[w].

Q's two endpoints require two negative neighbours each, its isolates five
each. Every -1 vertex sees one or two Q vertices. Exactly one sees two;
the existing common neighbour w and original labels force this pair to be
the two isolates. C1 fixes the original Q labels of the other twelve.
All remaining, unmodelled vertices have h=0; Ah=-4h is therefore exact on
the 45 known vertices. Common-neighbour counts are only upper bounds,
except at o and w, whose complete neighbourhoods are included.
"""

import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process, atomic_json_write
from ortools.sat.python import cp_model


def build():
    model = cp_model.CpModel()
    n, w = 45, 15
    h = [0]*n
    h[w] = -3
    for u in (16, 17, *range(22, 32)): h[u] = 1
    h[18] = h[19] = 2
    for u in range(32, 45): h[u] = -1
    assert sum(h) == 0 and sum(x*x for x in h) == 42
    fixed = {}
    def fix(u, v, value):
        if u == v:
            assert value == 0
            return
        p = tuple(sorted((u, v)))
        assert p not in fixed or fixed[p] == value, (p, fixed.get(p), value)
        fixed[p] = value
    for v in range(1, n): fix(0, v, int(v <= 14))
    for a, b in combinations(range(14), 2): fix(a+1, b+1, int((a^1) == b))
    labels = {15:(4,6), 16:(0,2), 17:(1,3), 18:(0,3), 19:(1,2)}
    for u, lab in labels.items():
        for a in range(14): fix(u, a+1, int(a in lab))
    single = [(33,16,0),(34,16,2),(35,17,1),(36,17,3)]
    single += [(37+a,18,a) for a in range(4)]
    single += [(41+a,19,a) for a in range(4)]
    q_neighbours = {15:{16,17,18,19}, 20:{18}, 21:{19}, 32:{18,19}}
    for u, q, a in single:
        q_neighbours[u] = {q}
        for b in range(4): fix(u, b+1, int(a == b))
    for u in range(20, 33):
        for a in range(4): fix(u, a+1, 0)
    for u in range(15, n):
        if u in range(16,20): continue
        for q in range(16,20): fix(u, q, int(q in q_neighbours.get(u,set())))
    for a,b in combinations(range(16,20),2): fix(a,b,int((a,b)==(16,17)))
    nw = [5,7,*range(16,28)]
    assert len(nw) == 14 and w not in nw
    for v in range(n):
        if v != w: fix(w,v,int(v in nw))
    matching = {(16,17),(18,20),(19,21),(5,22),(7,23),(24,25),(26,27)}
    assert Counter(v for e in matching for v in e) == Counter(nw)
    for u,v in combinations(sorted(nw),2): fix(u,v,int((u,v) in matching))
    a = [[0]*n for _ in range(n)]
    for u,v in combinations(range(n),2):
        a[u][v] = a[v][u] = fixed.get((u,v), model.new_bool_var(f'e_{u}_{v}') if (u,v) not in fixed else 0)
    for u in range(n):
        model.add(sum(a[u]) <= 14)
        model.add(sum(h[v]*a[u][v] for v in range(n) if h[v]) == -4*h[u])
    for u in range(15,n):
        model.add(sum(a[u][1:15]) == 2)
        for k in range(7): model.add(a[u][2*k+1]+a[u][2*k+2] <= 1)
    products = 0
    for u,v in combinations(range(n),2):
        terms = [a[u][v]]
        for z in range(n):
            x,y = a[u][z],a[v][z]
            if isinstance(x,int):
                if x: terms.append(y)
            elif isinstance(y,int):
                if y: terms.append(x)
            else:
                p = model.new_bool_var(f'p_{u}_{v}_{z}')
                model.add(p <= x); model.add(p <= y); model.add(p >= x+y-1)
                terms.append(p); products += 1
        if u in (0,w) or v in (0,w): model.add(sum(terms) == 2)
        else: model.add(sum(terms) <= 2)
    assert not model.validate(), model.validate()
    return model,a,h,{'vertices':n,'nonzero_support':sum(bool(x) for x in h),
                      'edge_variables':sum(not isinstance(a[u][v],int) for u,v in combinations(range(n),2)),
                      'products':products}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seconds',type=float,default=60)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--linearization',type=int,default=0,choices=(0,1,2))
    args=p.parse_args()
    resources=limit_research_process(3)
    model,a,h,info=build()
    report={'scope':__doc__,'resources':resources,'model':info,'status':'RUNNING'}
    atomic_json_write(args.output,report)
    print(info,flush=True)
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=max(600,100*args.seconds)
    solver.parameters.linearization_level=args.linearization
    solver.parameters.cp_model_probing_level=0
    started=time.process_time();done=threading.Event()
    def interrupt():
        while not done.wait(.05):
            if time.process_time()-started >= args.seconds: solver.stop_search();return
    timer=threading.Thread(target=interrupt,daemon=True);timer.start()
    try: status=solver.solve(model)
    finally: done.set();timer.join()
    report.update(status=solver.status_name(status),cpu_seconds=time.process_time()-started,
                  branches=solver.num_branches,conflicts=solver.num_conflicts)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        graph=[[solver.value(e) for e in row] for row in a]
        # Check the actual necessary properties, not just solver bookkeeping.
        assert all(sum(graph[u][v]*h[v] for v in range(45)) == -4*h[u] for u in range(45))
        assert all(graph[u][v]+sum(graph[u][z]*graph[v][z] for z in range(45)) <= 2 for u,v in combinations(range(45),2))
        report.update(h=h,adjacency=graph)
    atomic_json_write(args.output,report)
    print({k:v for k,v in report.items() if k not in ('scope','adjacency','h')},flush=True)


if __name__ == '__main__': main()
