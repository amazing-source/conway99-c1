"""Positive controls for the Gram-free intrarectangle C2 encoder."""

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
    from root_component_corner_c2 import add_corner_c2
    from root_component_z_joint import build_joint,solve_joint
    info={}
    model,labels,graph=build_joint(4,[{'rectangle':[0,1],'states':[[2]]}],
                                  corner_c2=True,mate_normalize=True,diagnostics=info)
    result=solve_joint(model,labels,graph,4,5)
    assert result.get('exact_srg_verified')
    records=[{'graph':'rook9','free_adjacency':True,'solver_status':result['status'],
              'exact_srg_verified':True,**info}]
    edges=[tuple(map(int,line.split())) for line in path.read_text().splitlines() if line.strip()]
    A=np.zeros((243,243),dtype=np.int64)
    for u,v in edges:A[u,v]=A[v,u]=1
    assert np.all(A.sum(axis=1)==22)
    assert np.array_equal(A@A+A,20*np.eye(243,dtype=np.int64)+2*np.ones_like(A))
    labels,gamma=extract_root(A.tolist(),0)
    model=cp_model.CpModel();graph=[[0]*len(labels) for _ in labels]
    for u,v in combinations(range(len(labels)),2):
        graph[u][v]=graph[v][u]=model.new_bool_var(f'e_{u}_{v}')
        model.add(graph[u][v]==gamma[u][v])
    info=add_corner_c2(model,graph,labels)
    assert not model.validate(),model.validate()
    result=solve_joint(model,labels,graph,22,10)
    assert result.get('exact_srg_verified')
    records.append({'graph':str(path),'fixed_edges_as_boolean_variables':True,
                    'solver_status':result['status'],'cpu_seconds':result['cpu_seconds'],
                    'exact_srg_verified':True,**info})
    return {'status':'CORNER_C2_ENCODER_CONTROLS_PASSED','controls':records}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--graph',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    resources=limit_research_process(1)
    result=run(a.graph);result['resources']=resources
    atomic_json_write(a.output,result);print(json.dumps(result),flush=True)
