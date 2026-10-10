"""Joint D-Z and simple-vertex incidence model for the tight 4+4 cut.

By default this forgets the core cells; --core-cells restores those labels
and their exact common-neighbour equations. B-B edges are always omitted.
The model uses a fixed forest Z and the tight-cut lemma.
FEASIBLE is only a relaxation witness; UNKNOWN is never an exclusion.
"""
from itertools import combinations
from collections import defaultdict
import argparse
import json
import time
import networkx as nx
import numpy as np
from ortools.sat.python import cp_model
from norm16_schur_data import ROOT, source_data
from norm16_even_margins_probe import instance


def solve(fid,seconds=30, triple_caps=False, core_cells=False, orbit=0):
    started = time.monotonic()
    cores,cases,forests=source_data()
    shadows=[set(r[:2])|{8+q for q in r[2:]} for r in cases[3]['orbits'][orbit]['representative']]
    c=[[len(s&t) if i!=j else 0 for j,t in enumerate(shadows)] for i,s in enumerate(shadows)]
    record=next(r for r in json.loads((ROOT/'data/codex_norm16_shadow_connectivity.json').read_text())['records'] if r['case']==3 and r['orbit']==orbit)
    u,v=record['tight_subsets']
    f=next(f for f in forests if f['id']==fid)
    az=f['adjacency_Z'];deg=list(map(sum,az))
    az2=[[sum(az[i][k]*az[k][j] for k in range(11)) for j in range(11)] for i in range(11)]
    m=cp_model.CpModel()
    x=[[m.new_bool_var(f'x_{d}_{z}') for z in range(11)] for d in range(8)]
    for d in range(8):
        m.add(sum(x[d])==4)
        m.add(sum(deg[z]*x[d][z] for z in range(11))<=6)
        for z in range(11):
            m.add(sum(x[d][j] for j in range(11) if az[z][j])<=2-x[d][z])
    for z in range(11):
        m.add(sum(x[d][z] for d in range(8))==2+deg[z])
        for part in (u,v):
            m.add_linear_constraint(sum(x[d][z] for d in part),1,2)
    # Quotient only the first D row by automorphisms of the fixed Z forest.
    graph=nx.from_numpy_array(np.array(az))
    autos=list(nx.algorithms.isomorphism.GraphMatcher(graph,graph).isomorphisms_iter())
    canonical=set()
    for zs in combinations(range(11),4):
        if sum(deg[z] for z in zs)>6:continue
        mask=sum(1<<z for z in zs)
        if any(sum(az[z][j] for j in zs)>2-int(z in zs) for z in range(11)):continue
        if mask==min(sum(1<<a[z] for z in zs) for a in autos):canonical.add(mask)
    m.add_allowed_assignments(x[0],[[(mask>>z)&1 for z in range(11)] for mask in sorted(canonical)])
    dd={};zz={}
    for d,e in combinations(range(8),2):
        terms=[]
        for z in range(11):
            t=m.new_bool_var(f'dd_{d}_{e}_{z}');m.add_multiplication_equality(t,[x[d][z],x[e][z]]);terms.append(t)
        dd[d,e]=terms
    for z,w in combinations(range(11),2):
        terms=[]
        for d in range(8):
            t=m.new_bool_var(f'zz_{z}_{w}_{d}');m.add_multiplication_equality(t,[x[d][z],x[d][w]]);terms.append(t)
        zz[z,w]=terms
    bd=defaultdict(list);bz=defaultdict(list);bdd=defaultdict(list);bzz=defaultdict(list);bdz=defaultdict(list)
    cell_terms=defaultdict(list);core_d=defaultdict(list);core_z=defaultdict(list)
    cell_copies={}
    if core_cells:
        core=cores[3]['representatives'][0]
        for p in range(8):
            for q in range(8):
                cell_copies[p,q]=2-core[p][q]-sum(p in s and 8+q in s for s in shadows)
        labels=instance(3,orbit,fid)[2]
        prototypes=[]
        for label in labels:
            if label[0]!='B':continue
            _,p,q,dm=label
            ds=tuple(d for d in range(8) if dm>>d&1)
            if len(set(ds)&set(u))<=1 and len(set(ds)&set(v))<=1:prototypes.append(((p,8+q),ds))
    else:
        prototypes=[((),tuple(sorted(d for d in (ud,vd) if d is not None))) for ud in [None]+u for vd in [None]+v]
    variables=[];types=[]
    for cs,ds in prototypes:
            for zs in combinations(range(11),1+len(ds)):
                if any(az[z][w]+az2[z][w]>=2 for z,w in combinations(zs,2)):continue
                internal=[sum(az[z][w] for w in zs) for z in range(11)]
                if any(internal[z]>2-int(z in zs) for z in range(11)):continue
                var=m.new_int_var(0,12,f'b0_{zs[0]}') if not ds and not core_cells else m.new_bool_var(f'b_{len(variables)}')
                variables.append(var);types.append([list(ds),list(zs),list(cs)])
                for d in ds:bd[d].append(var)
                for z in zs:bz[z].append(var)
                for pair in combinations(ds,2):bdd[pair].append(var)
                for pair in combinations(zs,2):bzz[pair].append(var)
                for d in ds:
                    for z in zs:bdz[d,z].append(var)
                if core_cells:
                    cell_terms[cs[0],cs[1]-8].append(var)
                    for p in cs:
                        for d in ds:core_d[p,d].append(var)
                        for z in zs:core_z[p,z].append(var)
                if not ds and not core_cells:continue
                for d in range(8):
                    m.add(sum(x[d][z] for z in zs)<=2-int(d in ds)-sum(p in shadows[d] for p in cs)).only_enforce_if(var)
                for z in range(11):
                    m.add(sum(x[d][z] for d in ds)<=2-int(z in zs)-internal[z]).only_enforce_if(var)
    m.add(sum(variables)==64)
    if triple_caps:
        triple_columns=defaultdict(list)
        for t,var in zip(types,variables):
            for triple in combinations(sorted(t[2]+[16+d for d in t[0]]+[24+z for z in t[1]]),3):
                triple_columns[triple].append(var)
        for vs in triple_columns.values():
            if len(vs)>1:m.add(sum(vs)<=1)
    for d in range(8):m.add(sum(bd[d])==6)
    for z in range(11):m.add(sum(bz[z])==12-2*deg[z])
    for d,e in combinations(range(8),2):m.add(sum(bdd[d,e])+sum(dd[d,e])==2-c[d][e])
    for z,w in combinations(range(11),2):m.add(sum(bzz[z,w])+sum(zz[z,w])==2-az[z][w]-az2[z][w])
    for d in range(8):
        for z in range(11):m.add(sum(bdz[d,z])+x[d][z]+sum(x[d][w] for w in range(11) if az[z][w])==2)
    if core_cells:
        for cell,n in cell_copies.items():m.add(sum(cell_terms[cell])==n)
        for p in range(16):
            for d in range(8):
                common_core=sum(core[p][q-8] if p<8 else core[q][p-8] for q in shadows[d] if (p<8)!=(q<8))
                m.add(sum(core_d[p,d])==2-int(p in shadows[d])-common_core)
            for z in range(11):m.add(sum(core_z[p,z])+sum(x[d][z] for d in range(8) if p in shadows[d])==2)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=seconds;solver.parameters.num_search_workers=1
    print(json.dumps({'forest':fid,'B_types':len(types),'first_D_row_orbits':len(canonical),'build_seconds':time.monotonic()-started}),flush=True)
    status=solver.solve(m)
    out={'scope':__doc__,'forest':fid,'case_representative':3,'orbit_representative':orbit,'C':c,
         'status':solver.status_name(status),'seconds':solver.wall_time,'branches':solver.num_branches,'B_types':len(types),
         'B_pair_common_neighbours_through_triples':triple_caps,'core_cells_included':core_cells}
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        out['D_Z_row_masks']=[sum((1<<z)*int(solver.value(x[d][z])) for z in range(11)) for d in range(8)]
        out['B_types_used']=[{'D':t[0],'Z':t[1],'core':t[2],'multiplicity':int(solver.value(v))} for t,v in zip(types,variables) if solver.value(v)]
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--forest',type=int,default=7);p.add_argument('--seconds',type=float,default=30)
    p.add_argument('--triple-caps',action='store_true')
    p.add_argument('--core-cells',action='store_true');p.add_argument('--orbit',type=int,default=0)
    args=p.parse_args();r=solve(args.forest,args.seconds,args.triple_caps,args.core_cells,args.orbit)
    suffix='_triples' if args.triple_caps else ''
    if args.core_cells:suffix+=f'_core{args.orbit}'
    (ROOT/f'data/codex_norm16_tight_block_f{args.forest}{suffix}.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('B_types_used','scope','C')}),flush=True)
