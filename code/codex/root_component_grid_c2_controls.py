"""Exercise grid-C2 on a real SRG243, including vertices with no grid neighbour."""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def run(path):
    import numpy as np
    from ortools.sat.python import cp_model
    from root_component_neighbor_moment_controls import extract_root
    from root_component_grid_c2 import add_grid_c2
    from root_component_z_joint import solve_joint
    edges=[tuple(map(int,line.split())) for line in path.read_text().splitlines() if line.strip()]
    A=np.zeros((243,243),dtype=np.int64)
    for u,v in edges:A[u,v]=A[v,u]=1
    assert np.all(A.sum(axis=1)==22)
    assert np.array_equal(A@A+A,20*np.eye(243,dtype=np.int64)+2*np.ones_like(A))
    labels,gamma=extract_root(A.tolist(),0)
    rectangles=list(combinations(range(11),2))
    groups=[[w for w,label in enumerate(labels) if tuple(a//2 for a in label)==q] for q in rectangles]
    grid_indices=[i for i,g in enumerate(groups) if all(gamma[u][v]==int(bool(set(labels[u])&set(labels[v])))
                  for u,v in combinations(g,2))]
    assert grid_indices,'Control graph must contain a root grid.'
    row_types=[{'rectangle':list(q),'states':[list(z) for z in sorted({tuple(sum(gamma[w][v] for v in target)
                for target in groups) for w in group})]} for q,group in zip(rectangles,groups)]
    model=cp_model.CpModel();graph=[[0]*len(labels) for _ in labels]
    for u,v in combinations(range(len(labels)),2):
        graph[u][v]=graph[v][u]=model.new_bool_var(f'e_{u}_{v}')
        model.add(graph[u][v]==gamma[u][v])
    qi=grid_indices[0];q=rectangles[qi]
    info=add_grid_c2(model,graph,labels,[q],row_types)
    assert info['boolean_products']>0
    assert not model.validate(),model.validate()
    result=solve_joint(model,labels,graph,22,10)
    assert result.get('exact_srg_verified')
    # Directly find the corresponding full nine-vertex grid to expose the
    # distinction between valid C2 and Conway-specific perfect domination.
    neighbours=np.flatnonzero(A[0]).tolist()
    pairs=[];unused=set(neighbours)
    while unused:
        x=min(unused);y=next(v for v in unused if A[x,v]);pairs.append((x,y));unused-={x,y}
    letters=[v for pair in pairs for v in pair]
    label_to_vertex={tuple(i for i,v in enumerate(letters) if A[w,v]):w
                     for w in range(243) if w!=0 and not A[0,w]}
    full={0,*pairs[q[0]],*pairs[q[1]],*(label_to_vertex[tuple(labels[w])] for w in groups[qi])}
    assert len(full)==9
    outside=[sum(int(A[w,v]) for v in full) for w in range(243) if w not in full]
    assert outside.count(0)==72 and outside.count(1)==162
    return {'status':'GRID_C2_ENCODER_CONTROL_PASSED','graph':str(path),'rectangle':list(q),
            'fixed_edges_as_boolean_variables':True,'solver_status':result['status'],
            'cpu_seconds':result['cpu_seconds'],'exact_srg_verified':True,
            'outside_grid_neighbour_counts':{'0':72,'1':162},**info}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--graph',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    resources=limit_research_process(1)
    result=run(a.graph);result['resources']=resources
    atomic_json_write(a.output,result);print(json.dumps(result),flush=True)
