"""Exact SRG completion around a dominating square grid, with free fibres.

For Conway, every induced 3x3 grid D is a (4,1) intriguing set: its 90
exterior vertices have exactly one neighbour in D. Each of the nine fibres
has size10, induces a matching, and has degree1/2 to a fibre whose grid
point is adjacent/nonadjacent. Fibre matchings along any spanning tree of
the grid may all be renamed to identity; a common residual permutation
then makes one internal matching canonical. This assumes no automorphism.

Every graph with global minimum c(line)>=4 contains such a grid. Adding
that minimum on the six grid lines therefore gives a necessary model for
the whole global c>=4 branch, without selecting a root template or Gram.
The analogous 2x2-grid model reconstructs Clebsch(16,5,0,2) as a control.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortools.sat.python import cp_model
from root_component_resources import atomic_json_write, limit_research_process


def grid_adjacent(i,j,q):
    return i != j and (i//q == j//q or i%q == j%q)


def grid_tree(q):
    # Every row is rooted at its first point; the first column joins rows.
    return {(r*q,r*q+c) for r in range(q) for c in range(1,q)} | {(0,r*q) for r in range(1,q)}


def add_exterior_line_partitions(model,graph,lines,minimum_components,balanced):
    """Keep the known six-vertex grid component separate, partition the other30.

The other grid points already form one isolated component of N(L). If
N(L) has at least m components, its remaining components can be merged
into m-1 nonempty bins. Hence this restricts only auxiliary bin labels.
"""
    m=minimum_components-1; products={}; equalities=0
    def product(a,b):
        if isinstance(a,int):return b if a else 0
        key=(a.index,b.index)
        if key not in products:
            p=model.new_bool_var(f'grid_balance_{len(products)}')
            model.add_bool_or([p.Not(),a]);model.add_bool_or([p.Not(),b])
            model.add_bool_or([a.Not(),b.Not(),p]);products[key]=p
        return products[key]
    for li,line in enumerate(lines):
        colours=[[9+10*i+a for a in range(10)] for i in line]
        members=sum(colours,[]); outside=sorted(set(range(9,99))-set(members))
        flags={w:[model.new_bool_var(f'grid_bin_{li}_{w}_{j}') for j in range(m)] for w in members}
        bins={w:model.new_int_var(1,m,f'grid_bin_id_{li}_{w}') for w in members}
        for w in members:
            model.add_exactly_one(flags[w])
            model.add(bins[w]==sum((j+1)*flag for j,flag in enumerate(flags[w])))
        model.add(bins[colours[0][0]]==1); previous=1
        for i,w in enumerate(colours[0][1:],1):
            model.add(bins[w]<=previous+1)
            maximum=model.new_int_var(1,m,f'grid_bin_prefix_{li}_{i}')
            model.add_max_equality(maximum,[previous,bins[w]]);previous=maximum
        for j in range(m):
            half=model.new_int_var(1,6-m,f'grid_bin_half_{li}_{j}')
            for colour in colours:model.add(sum(flags[w][j] for w in colour)==2*half)
            if balanced:
                for x in outside:
                    model.add(sum(product(graph[x][y],flags[y][j]) for y in members)==half)
                    equalities+=1
        for u,v in combinations(members,2):
            edge=graph[u][v]
            if isinstance(edge,int):
                if edge:model.add(bins[u]==bins[v])
            else:model.add(bins[u]==bins[v]).only_enforce_if(edge)
    return {'global_minimum_components':minimum_components,'lines':lines,
            'fixed_grid_component_separated':True,'exterior_bins_per_line':m,
            'bin_half_size_range':[1,6-m],'component_degree_balance':balanced,
            'component_degree_equations':equalities,'component_degree_products':len(products),
            'scope':add_exterior_line_partitions.__doc__}


def build(q=3, minimum_components=0, upper_only=False, balanced=True,separate_grid_component=False):
    assert q in (2,3)
    k,lam,mu=(5,0,2) if q==2 else (14,1,2)
    assert minimum_components==0 or (q==3 and minimum_components in (3,4))
    grid_size=q*q; fibre_size=k-2*(q-1); exterior=grid_size*fibre_size
    n=grid_size+exterior; tree=grid_tree(q)
    assert len(tree)==grid_size-1
    model=cp_model.CpModel()
    graph=[[0]*n for _ in range(n)]
    for i,j in combinations(range(grid_size),2):
        graph[i][j]=graph[j][i]=int(grid_adjacent(i,j,q))
    def vertex(i,a):return grid_size+i*fibre_size+a
    for i in range(grid_size):
        for a in range(fibre_size):
            graph[i][vertex(i,a)]=graph[vertex(i,a)][i]=1
    for u,v in combinations(range(exterior),2):
        i,a=divmod(u,fibre_size); j,b=divmod(v,fibre_size)
        if i==j and lam==0:
            edge=0
        elif i==j==0:
            assert lam==1
            edge=int(b==(a^1))
        elif (i,j) in tree:
            edge=int(a==b)
        else:
            edge=model.new_bool_var(f'g_{u}_{v}')
        graph[grid_size+u][grid_size+v]=graph[grid_size+v][grid_size+u]=edge
    gamma=[row[grid_size:] for row in graph[grid_size:]]
    block_equations=0
    for u in range(exterior):
        i=u//fibre_size
        for j in range(grid_size):
            target=lam if i==j else (1 if grid_adjacent(i,j,q) else 2)
            model.add(sum(gamma[u][j*fibre_size+b] for b in range(fibre_size))==target)
            block_equations+=1
    products={}
    def product(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        if a.index==b.index:return a
        key=tuple(sorted((a.index,b.index)))
        if key not in products:
            p=model.new_bool_var(f'common_{len(products)}')
            model.add_bool_or([a.Not(),b.Not(),p])
            if not upper_only:
                model.add_bool_or([p.Not(),a])
                model.add_bool_or([p.Not(),b])
            products[key]=p
        return products[key]
    for u,v in combinations(range(exterior),2):
        target=2-int(u//fibre_size==v//fibre_size)
        expression=sum(product(gamma[u][w],gamma[v][w]) for w in range(exterior))+(4-q)*gamma[u][v]
        model.add(expression<=target if upper_only else expression==target)
    lines=[[r*q+c for c in range(q)] for r in range(q)]+[[r*q+c for r in range(q)] for c in range(q)]
    partitions=None
    if minimum_components:
        if separate_grid_component:
            partitions=add_exterior_line_partitions(model,graph,lines,minimum_components,balanced)
        else:
            from root_component_minimum_partition import add_partitions_for_lines
            partitions=add_partitions_for_lines(model,graph,lines,balance=balanced,
                minimum_components=minimum_components,tag_prefix='grid_line')
    info={'parameters':[n,k,lam,mu],'grid_order':q,'fibre_size':fibre_size,
          'grid_vertex_count':grid_size,'exterior_vertex_count':exterior,
          'identity_matching_tree':[list(e) for e in sorted(tree)],
          'first_internal_matching_canonical':lam==1,
          'graph_automorphism_assumption':False,'fixed_subgraph':f'{q}x{q} grid',
          'additional_arbitrary_local_seed':False,
          'full_common_neighbour_constraints':True,'upper_only':upper_only,
          'upper_bound_equivalence':'All pair upper bounds saturate when summed, by the exact block degrees.',
          'block_degree_equations':block_equations,'C2_products':len(products),
          'global_minimum_components':minimum_components or None,
          'separate_grid_component':separate_grid_component,
          'grid_line_partitions':partitions,
          'covers_global_minimum_four_branch':minimum_components==4,
          'all_Conway_graphs_covered':False,
          'scope':'Any graph containing this dominating grid; global c>=4 guarantees a grid exists.'}
    return model,graph,info


def check_adjacency(adjacency,parameters):
    n,k,lam,mu=parameters
    assert len(adjacency)==n and all(len(row)==n for row in adjacency)
    assert all(adjacency[i][i]==0 and sum(adjacency[i])==k for i in range(n))
    assert all(x in (0,1) for row in adjacency for x in row)
    for i,j in combinations(range(n),2):
        assert adjacency[i][j]==adjacency[j][i]
        assert sum(a*b for a,b in zip(adjacency[i],adjacency[j]))==(lam if adjacency[i][j] else mu)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--grid-order',type=int,choices=(2,3),default=3)
    p.add_argument('--minimum-components',type=int,choices=(0,3,4),default=0)
    p.add_argument('--upper-only',action='store_true')
    p.add_argument('--no-balance',action='store_true')
    p.add_argument('--separate-grid-component',action='store_true',help='Leave the known grid prism as its own auxiliary bin.')
    p.add_argument('--seconds',type=float,default=120)
    p.add_argument('--linearization',type=int,choices=(0,1,2),default=0)
    p.add_argument('--build-only',action='store_true')
    p.add_argument('--log-search',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(); resources=limit_research_process(1)
    assert not a.output.exists()
    start=time.process_time()
    model,graph,info=build(a.grid_order,a.minimum_components,a.upper_only,not a.no_balance,a.separate_grid_component)
    assert not model.validate(),model.validate()
    info.update(scope=__doc__,status='MODEL_BUILT',resources=resources,
                build_cpu_seconds=time.process_time()-start,
                variables=len(model.proto.variables),constraints=len(model.proto.constraints),
                seconds_budget=a.seconds,linearization=a.linearization,
                portable_unsat_proof=False,global_conway_exclusion=False)
    atomic_json_write(a.output,info)
    print(json.dumps({k:info[k] for k in ('status','parameters','variables','constraints','build_cpu_seconds')}),flush=True)
    if a.build_only:return
    # Keep the solver in this wrapper so a SAT model can be reconstructed
    # in the new grid labelling rather than the old84-label root labelling.
    import threading
    solver=cp_model.CpSolver(); solver.parameters.num_search_workers=1
    solver.parameters.cp_model_probing_level=0;solver.parameters.symmetry_level=0
    solver.parameters.max_presolve_iterations=1;solver.parameters.linearization_level=a.linearization
    solver.parameters.log_search_progress=a.log_search
    solver.parameters.max_time_in_seconds=max(600,100*a.seconds)
    start=time.process_time();done=threading.Event()
    def stop():
        while not done.wait(.05):
            if time.process_time()-start>=a.seconds:solver.stop_search()
    timer=threading.Thread(target=stop,daemon=True);timer.start()
    try:status=solver.solve(model)
    finally:done.set();timer.join()
    info.update(status=solver.status_name(status),cpu_seconds=time.process_time()-start,
                branches=solver.num_branches,conflicts=solver.num_conflicts)
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        adjacency=[[solver.value(x) for x in row] for row in graph]
        check_adjacency(adjacency,info['parameters'])
        info.update(adjacency=adjacency,exact_all_pair_check=True,
                    status='CONWAY_GRAPH_FOUND' if a.grid_order==3 else 'CONTROL_GRAPH_FOUND')
    atomic_json_write(a.output,info)
    print(json.dumps({k:info[k] for k in ('status','cpu_seconds','branches','conflicts')}),flush=True)


if __name__=='__main__':main()
