"""Bounded exploration of the forced triangle matchings above the core.

The 64 simple vertices are labelled by their two core neighbours. In each
nonedge cell, the triangle partner at either core neighbour may be a D or
a B vertex. D-incidences and local common-neighbour upper bounds are
coupled to these partial matchings. Z vertices,
and B-B edges outside those matchings, are omitted by default. --forest
adds Z incidences; --full-b introduces all B-B edges with exact core/B
moments and necessary D/B bounds. SAT is still only a relaxation.
"""
import argparse
from collections import defaultdict
from itertools import combinations
import json
import time
import numpy as np
from ortools.sat.python import cp_model
from norm16_schur_data import ROOT, source_data
from norm16_even_margins_probe import instance


def add_far_vertices(m, bd, bs, transport, vv, u, v, fid):
    _, _, forests = source_data()
    az = np.array(next(f for f in forests if f['id']==fid)['adjacency_Z'],dtype=int)
    az2 = az@az
    kz = az.sum(axis=1)
    x = [[m.new_bool_var(f'x_{d}_{z}') for z in range(11)] for d in range(8)]
    y = [[m.new_bool_var(f'z_{b}_{z}') for z in range(11)] for b in range(64)]
    def both(a,b,name):
        t=m.new_bool_var(name);m.add_multiplication_equality(t,[a,b]);return t
    for d in range(8):
        m.add(sum(x[d])==4)
        m.add(sum(int(kz[z])*x[d][z] for z in range(11))<=6)
    for z in range(11):
        m.add(sum(x[d][z] for d in range(8))==2+int(kz[z]))
        m.add_linear_constraint(sum(x[d][z] for d in u),1,2)
        m.add_linear_constraint(sum(x[d][z] for d in v),1,2)
        m.add(sum(y[b][z] for b in range(64))==12-2*int(kz[z]))
        for c in range(16):
            m.add(sum(y[b][z] for b,(p,q,k) in enumerate(bs) if c in (p,8+q))
                  +sum(x[d][z] for d in range(8) if vv[c,d])==2)
        for d in range(8):
            bcommon=[both(bd[b][d],y[b][z],f'dz_{d}_{z}_{b}') for b in range(64)]
            m.add(sum(bcommon)+x[d][z]+sum(x[d][w] for w in range(11) if az[z,w])==2)
    for d,e in combinations(range(8),2):
        zcommon=[both(x[d][z],x[e][z],f'xdd_{d}_{e}_{z}') for z in range(11)]
        bcommon=[both(bd[b][d],bd[b][e],f'bdd_{d}_{e}_{b}') for b in range(64)]
        m.add(sum(zcommon)+sum(bcommon)==2-int(vv[:,d]@vv[:,e]))
    for z,w in combinations(range(11),2):
        dcommon=[both(x[d][z],x[d][w],f'xzz_{z}_{w}_{d}') for d in range(8)]
        bcommon=[both(y[b][z],y[b][w],f'bzz_{z}_{w}_{b}') for b in range(64)]
        m.add(sum(dcommon)+sum(bcommon)==2-int(az[z,w]+az2[z,w]))
    neighbors=defaultdict(list)
    for (a,b),e in transport.items():
        neighbors[a].append((b,e));neighbors[b].append((a,e))
    for b,(p,q,k) in enumerate(bs):
        m.add(sum(y[b])==1+sum(bd[b]))
        for d in range(8):
            common=[both(y[b][z],x[d][z],f'bdz_{b}_{d}_{z}') for z in range(11)]
            common += [both(e,bd[t][d],f'bdt_{b}_{d}_{t}') for t,e in neighbors[b]]
            m.add(sum(common)+int(vv[p,d]+vv[8+q,d])<=2-bd[b][d])
        for z in range(11):
            common=[both(bd[b][d],x[d][z],f'bzd_{b}_{z}_{d}') for d in range(8)]
            common += [both(e,y[t][z],f'bzt_{b}_{z}_{t}') for t,e in neighbors[b]]
            m.add(sum(common)+sum(y[b][w] for w in range(11) if az[z,w])<=2-y[b][z])
    for i,j in combinations(range(64),2):
        p,q,_=bs[i];r,s,_=bs[j]
        common=[both(bd[i][d],bd[j][d],f'bbd_{i}_{j}_{d}') for d in range(8)]
        common += [both(y[i][z],y[j][z],f'bbz_{i}_{j}_{z}') for z in range(11)]
        m.add(sum(common)<=2-int(p==r)-int(q==s)-transport.get((i,j),0))
    # Only quotient relabellings which preserve the fixed forest.
    import networkx as nx
    graph=nx.from_numpy_array(az)
    autos=list(nx.algorithms.isomorphism.GraphMatcher(graph,graph).isomorphisms_iter())
    canonical=[]
    for zs in combinations(range(11),4):
        if sum(kz[z] for z in zs)>6:continue
        mask=sum(1<<z for z in zs)
        if any(sum(az[z,j] for j in zs)>2-int(z in zs) for z in range(11)):continue
        if mask==min(sum(1<<a[z] for z in zs) for a in autos):
            canonical.append([int(z in zs) for z in range(11)])
    m.add_allowed_assignments(x[0],canonical)
    return x,y


def add_full_simple_edges(m, bd, bs, transport, vv, ac):
    """Exact core/B moments, with all B edges and necessary D/B bounds.

    Z is still absent. The residual D/B counts must be nonnegative and
    sum to between 2(1+r_b) and 4(1+r_b), since every Z has 2..4 D neighbours.
    """
    edges=dict(transport)
    for i,j in combinations(range(64),2):
        p,q,_=bs[i];r,s,_=bs[j]
        if p!=r and q!=s:
            edges[i,j]=m.new_bool_var(f'full_edge_{i}_{j}')
    neighbors=defaultdict(list)
    for (i,j),edge in edges.items():
        neighbors[i].append((j,edge));neighbors[j].append((i,edge))
    def both(a,b,name):
        t=m.new_bool_var(name);m.add_multiplication_equality(t,[a,b]);return t
    for b,(p,q,k) in enumerate(bs):
        for c in range(16):
            m.add(sum(e for j,e in neighbors[b] if c in (bs[j][0],8+bs[j][1]))
                  +sum(bd[b][d] for d in range(8) if vv[c,d])
                  ==2-int(c in (p,8+q))-int(ac[c,p]+ac[c,8+q]))
        residual=[]
        for d in range(8):
            common=[both(e,bd[j][d],f'full_bd_{b}_{d}_{j}') for j,e in neighbors[b]]
            missing=m.new_int_var(0,2,f'missing_z_{b}_{d}')
            m.add(missing==2-bd[b][d]-int(vv[p,d]+vv[8+q,d])-sum(common))
            residual.append(missing)
        m.add(sum(residual)>=2+2*sum(bd[b]))
        m.add(sum(residual)<=4+4*sum(bd[b]))
    for (i,j),edge in edges.items():
        p,q,_=bs[i];r,s,_=bs[j]
        common=[both(bd[i][d],bd[j][d],f'full_common_{i}_{j}_{d}') for d in range(8)]
        m.add(sum(common)<=2-int(p==r)-int(q==s)-edge)
    return edges


def solve(orbit=0, seconds=30, forest=None, full_b=False):
    started = time.monotonic()
    cores, cases, _ = source_data()
    core = np.array(cores[3]['representatives'][0], dtype=int)
    shadows = [set(r[:2]) | {8+q for q in r[2:]}
               for r in cases[3]['orbits'][orbit]['representative']]
    record = next(r for r in json.loads((ROOT/'data/codex_norm16_shadow_connectivity.json').read_text())['records']
                  if r['case'] == 3 and r['orbit'] == orbit)
    u, v = map(set, record['tight_subsets'])
    ac = np.block([[np.zeros((8,8), dtype=int), core], [core.T, np.zeros((8,8), dtype=int)]])
    vv = np.array([[int(c in s) for s in shadows] for c in range(16)])
    domains = defaultdict(list)
    for kind, p, q, dm in (r for r in instance(3, orbit, 7)[2] if r[0] == 'B'):
        ds = {d for d in range(8) if dm >> d & 1}
        if len(ds & u) <= 1 and len(ds & v) <= 1:
            domains[p,q].append(dm)
    bs = []
    for p in range(8):
        for q in range(8):
            n = 2-int(core[p,q])-sum(p in s and 8+q in s for s in shadows)
            bs.extend((p,q,k) for k in range(n))
    assert len(bs) == 64
    m = cp_model.CpModel()
    gates = {name:m.new_bool_var(name) for name in ('moments','two_count','shared_cap','matchings','core_B_cap')}
    m.add_assumptions(list(gates.values()))
    bd = [[m.new_bool_var(f'd_{b}_{d}') for d in range(8)] for b in range(64)]
    masks = []
    twos = []
    for b, (p,q,k) in enumerate(bs):
        mask = m.new_int_var(0,255,f'mask_{b}'); masks.append(mask)
        m.add(mask == sum((1<<d)*bd[b][d] for d in range(8)))
        m.add_allowed_assignments([mask], [(x,) for x in domains[p,q]])
        two = m.new_bool_var(f'two_{b}'); twos.append(two)
        m.add(sum(bd[b]) == 2).only_enforce_if(two)
        m.add(sum(bd[b]) <= 1).only_enforce_if(two.Not())
        if k:
            m.add(masks[b-1] <= mask)
    m.add_linear_constraint(sum(twos),6,9).only_enforce_if(gates['two_count'])
    for d in range(8):
        m.add(sum(bd[b][d] for b in range(64)) == 6).only_enforce_if(gates['moments'])
    for c in range(16):
        for d in range(8):
            rhs = 2-vv[c,d]-int((ac@vv)[c,d])
            m.add(sum(bd[b][d] for b,(p,q,k) in enumerate(bs) if c in (p,8+q)) == rhs).only_enforce_if(gates['moments'])
    # The nonedge cells need a D or B partner at each core neighbour.
    transport = {}
    incident = defaultdict(list)
    for i,j in combinations(range(64),2):
        p,q,_ = bs[i]; r,s,_ = bs[j]
        shared = int(p == r)+int(q == s)
        if shared == 1 and not core[p,q] and not core[r,s]:
            edge = m.new_bool_var(f'e_{i}_{j}')
            transport[i,j] = edge
            c = p if p == r else 8+q
            incident[i,c].append(edge); incident[j,c].append(edge)
            for d in range(8):
                m.add(bd[i][d]+bd[j][d] <= 1).only_enforce_if(edge)
        if shared:
            common_d = []
            for d in range(8):
                both = m.new_bool_var(f'common_{i}_{j}_{d}')
                m.add_multiplication_equality(both,[bd[i][d],bd[j][d]])
                common_d.append(both)
            m.add(sum(common_d) <= 2-shared).only_enforce_if(gates['shared_cap'])
    for i,(p,q,k) in enumerate(bs):
        if not core[p,q]:
            for c in (p,8+q):
                m.add(sum(incident[i,c])+sum(bd[i][d] for d in range(8) if vv[c,d]) == 1).only_enforce_if(gates['matchings'])
    # Mandatory transport edges already consume some core/B pair capacity.
    for i,(p,q,k) in enumerate(bs):
        for c in range(16):
            terms = [edge for (a,b),edge in transport.items()
                     if (a == i and c in (bs[b][0],8+bs[b][1]))
                     or (b == i and c in (bs[a][0],8+bs[a][1]))]
            common_core = int(ac[c,p]+ac[c,8+q])
            m.add(sum(terms)+sum(bd[i][d] for d in range(8) if vv[c,d])
                  <= 2-int(c in (p,8+q))-common_core).only_enforce_if(gates['core_B_cap'])
    if forest is not None:
        x,y=add_far_vertices(m,bd,bs,transport,vv,u,v,forest)
    if full_b:
        full_edges=add_full_simple_edges(m,bd,bs,transport,vv,ac)
    print(json.dumps({'orbit':orbit,'vertices':64,'transport_edges':len(transport),
                      'build_seconds':time.monotonic()-started}),flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    status = solver.solve(m)
    result = {'scope':__doc__,'case':3,'orbit':orbit,'forest':forest,'full_B_edges':full_b,'status':solver.status_name(status),
              'seconds':solver.wall_time,'branches':solver.num_branches}
    if status == cp_model.INFEASIBLE:
        indices = set(solver.sufficient_assumptions_for_infeasibility())
        result['unsat_groups'] = [name for name,g in gates.items() if g.index in indices]
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        result['B_vertices'] = [{'cell':list(cell),'D_mask':int(solver.value(mask))}
                                for cell,mask in zip(bs,masks)]
        result['transport_edges'] = [list(pair) for pair,edge in transport.items() if solver.value(edge)]
        result['B_with_two_D'] = sum(solver.value(t) for t in twos)
        if forest is not None:
            result['D_Z_row_masks']=[sum((1<<z)*int(solver.value(x[d][z])) for z in range(11)) for d in range(8)]
            result['B_Z_row_masks']=[sum((1<<z)*int(solver.value(y[b][z])) for z in range(11)) for b in range(64)]
        if full_b:
            result['full_B_edges_present']=[list(pair) for pair,e in full_edges.items() if solver.value(e)]
    return result


if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--orbit',type=int,default=0); p.add_argument('--seconds',type=float,default=30)
    p.add_argument('--forest',type=int)
    p.add_argument('--full-b',action='store_true')
    args=p.parse_args(); result=solve(args.orbit,args.seconds,args.forest,args.full_b)
    suffix='' if args.forest is None else f'_forest{args.forest}'
    if args.full_b:suffix+='_full_b'
    (ROOT/f'data/codex_norm16_tight_transport_{args.orbit}{suffix}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('scope','B_vertices','transport_edges')}),flush=True)
