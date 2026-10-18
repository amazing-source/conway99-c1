"""Exercise the new signed-component encoder on a genuine SRG243."""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process


def run(path):
    import numpy as np
    from ortools.sat.python import cp_model
    from root_component_neighbor_moment_controls import extract_root
    from root_component_signed_components import blocks, template_from_gamma, add_signed_components
    from root_component_z_joint import solve_joint
    edges = [tuple(map(int,line.split())) for line in path.read_text().splitlines() if line.strip()]
    n = max(max(e) for e in edges)+1
    A = np.zeros((n,n),dtype=np.int64)
    for u,v in edges:
        A[u,v] = A[v,u] = 1
    assert n == 243 and np.all(A.sum(axis=1) == 22)
    assert np.array_equal(A@A+A,20*np.eye(n,dtype=np.int64)+2*np.ones_like(A))
    labels, gamma = extract_root(A.tolist(),0)
    template = template_from_gamma(labels,gamma)
    candidates = [(len(blocks(template,a,11)),a) for a in range(11)]
    nontrivial = sorted((count,a) for count,a in candidates if count >= 3)
    assert nontrivial, 'Need at least two independent signed components to exercise their cross Gram.'
    count,a = nontrivial[0]
    model = cp_model.CpModel()
    graph = [[0]*len(labels) for _ in labels]
    for u,v in combinations(range(len(labels)),2):
        graph[u][v] = graph[v][u] = model.new_bool_var(f'e_{u}_{v}')
        model.add(graph[u][v] == gamma[u][v])
    info = add_signed_components(model,graph,labels,template,[a],mode='boundary')
    assert not model.validate(),model.validate()
    assert info['lines'][0]['gram_products'] > 0
    assert info['lines'][0]['signed_equations']['boolean_integer_products'] > 0
    result = solve_joint(model,labels,graph,22,15)
    assert result.get('exact_srg_verified'),result['status']
    return {'status':'SIGNED_COMPONENT_ENCODER_POSITIVE_CONTROL_PASSED', 'source_graph':str(path),
            'root_line':a,'component_count':count,'fixed_edges_kept_as_boolean_variables':True,
            'conway_uniform_component_counts_used':False,'signed_components':info,
            'solver_status':result['status'],'cpu_seconds':result['cpu_seconds'],
            'variables':result['model_variables'],'constraints':result['model_constraints'],
            'exact_srg_verified':True}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--graph',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    resources=limit_research_process(1)
    result=run(a.graph);result['resources']=resources
    atomic_json_write(a.output,result)
    print(json.dumps(result),flush=True)
