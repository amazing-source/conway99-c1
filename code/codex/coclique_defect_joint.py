"""Joint population and reciprocal edge counts over zero-charge row types.

Every full completion induces this model. Multiplicities can merge vertices,
so feasibility is still a necessary relaxation, never a claimed SRG.
"""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import time

from ortools.sat.python import cp_model
from coclique_defect_gluing import gluing_data


def joint(core, order, csize, seconds, workers, logfile):
    data = gluing_data(core, order, csize)
    rows, q = data['rows'], data['charges']
    n, m = len(q), len(rows)
    k = core['parameters']['degree']
    bzero = 4 if k == 14 else 2
    assert k in (4, 14)
    model = cp_model.CpModel()
    upper, counts, ccounts, fcounts, used = [], [], [], [], []
    h = [[2-((r>>i)&1)-(r&data['neighbours'][i]).bit_count() for i in range(n)] for r in rows]
    forbidden = [sum(1<<i for i, v in enumerate(t) if v == 0) for t in h]
    for r, row in enumerate(rows):
        members = [i for i in range(n) if row>>i&1]
        u = min([order-n]+[data['outside_degrees'][i] for i in members]
                +[data['residual'][i,j] for i,j in combinations(members, 2)])
        if len(members) >= 3:
            u = min(u, 1)
        upper.append(u)
        x = model.NewIntVar(0, u, f'x{r}')
        c = model.NewIntVar(0, u, f'c{r}')
        f = model.NewIntVar(0, 0 if len(members)>k-bzero else u, f'f{r}')
        z = model.NewBoolVar(f'used{r}')
        model.Add(x == c+f)
        model.Add(x >= 1).OnlyEnforceIf(z)
        model.Add(x == 0).OnlyEnforceIf(z.Not())
        counts.append(x); ccounts.append(c); fcounts.append(f); used.append(z)
    model.Add(sum(counts) == order-n)
    model.Add(sum(ccounts) == csize)
    for i in range(n):
        rr = [r for r, row in enumerate(rows) if row>>i&1]
        model.Add(sum(counts[r] for r in rr) == data['outside_degrees'][i])
        model.Add(sum(ccounts[r] for r in rr) == core['boundary_degrees'][i])
    for (i,j), target in data['residual'].items():
        model.Add(sum(counts[r] for r,row in enumerate(rows) if row>>i&1 and row>>j&1) == target)
    for r,t in combinations(range(m), 2):
        if (rows[r]&rows[t]).bit_count()>2:
            model.AddBoolOr([used[r].Not(),used[t].Not()])

    # Types are (row, C) and (row, outside C). A single shared variable
    # counts the edges between each pair of types, enforcing reciprocity.
    pop = [v for r in range(m) for v in (ccounts[r], fcounts[r])]
    incident = [[] for _ in pop]
    incoming_c = [[] for _ in pop]
    common = [[[] for _ in range(n)] for _ in pop]
    all_edges = []
    large_products = 0

    def add_edge(r, rc, t, tc):
        nonlocal large_products
        a,b = 2*r+rc,2*t+tc
        if a>b:
            return
        if rc==tc==0:
            return
        u,v = upper[r],upper[t]
        loop = a==b
        if loop:
            # Identical singleton types induce a matching, as the shared
            # core neighbour already uses the edge's one common neighbour.
            edge = model.NewIntVar(0,u//2,f'g{a}_{b}')
            model.Add(2*edge<=pop[a])
        else:
            edge = model.NewIntVar(0,u*v,f'g{a}_{b}')
            model.Add(edge<=v*pop[a])
            model.Add(edge<=u*pop[b])
            if u>1 and v>1:
                product = model.NewIntVar(0,u*v,f'prod{a}_{b}')
                model.AddMultiplicationEquality(product,[pop[a],pop[b]])
                model.Add(edge<=product)
                large_products += 1
        for source,target,row_t in ((a,b,rows[t]),(b,a,rows[r])):
            incident[source].append(edge)
            if target%2==0:
                incoming_c[source].append(edge)
            for i in range(n):
                if row_t>>i&1:
                    common[source][i].append(edge)
        all_edges.append((a,b,edge))

    for r in range(m):
        for t in range(r,m):
            if (rows[r]&rows[t]).bit_count()>1 or rows[t]&forbidden[r] or rows[r]&forbidden[t]:
                continue
            for rc in (0,1):
                for tc in (0,1):
                    add_edge(r,rc,t,tc)
    for typ in range(2*m):
        r, colour = divmod(typ,2)
        model.Add(sum(incident[typ]) == (k-rows[r].bit_count())*pop[typ])
        if colour==1:
            model.Add(sum(incoming_c[typ]) == bzero*pop[typ])
        for i in range(n):
            model.Add(sum(common[typ][i]) == h[r][i]*pop[typ])
    stats = dict(row_types=m,typed_edge_variables=len(all_edges),large_products=large_products,
                 model=model.ModelStats(),enumeration_nodes=data['enumeration_nodes'])
    print(json.dumps(stats),flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=seconds
    solver.parameters.num_search_workers=workers
    solver.parameters.log_search_progress=True
    solver.parameters.log_to_stdout=False
    start=time.monotonic()
    with logfile.open('w',encoding='utf8') as log:
        def record(line):
            log.write(f'{time.monotonic()-start:.3f} {line}\n');log.flush()
        solver.log_callback=record
        status=solver.Solve(model)
    result=dict(status=solver.StatusName(status),seconds=time.monotonic()-start,
                stats=stats,limit_seconds=seconds,workers=workers,order=order,coclique_size=csize,
                scope='All row populations and reciprocal aggregate edges for this fixed core only; feasible does not prove an SRG',
                response_stats=solver.ResponseStats())
    if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
        result['selected_rows']=[dict(vertices=[i for i in range(n) if row>>i&1],
                                     count=solver.Value(counts[r]),coclique_count=solver.Value(ccounts[r]))
                                 for r,row in enumerate(rows) if solver.Value(counts[r])]
        result['typed_edges']=[dict(a=a,b=b,count=solver.Value(e)) for a,b,e in all_edges if solver.Value(e)]
        # Independently check the aggregated equations in integers.
        for typ in range(2*m):
            r=typ//2
            assert sum(solver.Value(e) for e in incident[typ]) == (k-rows[r].bit_count())*solver.Value(pop[typ])
            assert all(sum(solver.Value(e) for e in common[typ][i]) == h[r][i]*solver.Value(pop[typ]) for i in range(n))
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('core',type=Path)
    ap.add_argument('--order',type=int,default=99)
    ap.add_argument('--coclique',type=int,default=21)
    ap.add_argument('--seconds',type=float,default=120)
    ap.add_argument('--workers',type=int,default=4)
    args=ap.parse_args()
    raw=args.core.read_bytes();core=json.loads(raw)
    out=args.core.with_name(args.core.stem+'_joint.json')
    result=joint(core,args.order,args.coclique,args.seconds,args.workers,out.with_suffix('.log'))
    result['input_sha256']=hashlib.sha256(raw).hexdigest()
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:result[k] for k in ('status','seconds','stats')}),flush=True)


if __name__=='__main__':
    main()
