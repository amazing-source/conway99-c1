"""Controls for partial-block assumptions and conditional energy encoders.

The SRG243 control covers the affine count equation ONLY. The Conway
Schur constant 5/2 is not applied to SRG243. Synthetic Gram cases test
the implication encoding; they are not asserted to be graphs.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process,atomic_json_write


def run(directory,partial,graph_path):
    import numpy as np
    from ortools.sat.python import cp_model
    from root_component_partial_gram import test_block,filter_catalogue,add_graph_block
    from root_component_energy_implications import patterns,violations,add_energy_implications
    from root_component_z_design import solve_design
    from root_component_neighbor_moment_controls import extract_root
    from root_component_gram_enumeration import integer_psd
    template=json.loads((directory/'partition.json').read_text())['template']
    catalogue=json.loads((directory/'catalogue.json').read_text())['catalogue']
    certificate=json.loads(partial.read_text());block=certificate['best_block']
    checked=test_block(template,block['coordinate_rectangles'],block['principal_block'],catalogue=catalogue)
    assert checked['status']=='EXCLUDED_PARTIAL_BLOCK'
    small={'rectangles':block['coordinate_rectangles'][:2],
           'matrix':[row[:2] for row in block['principal_block'][:2]]}
    passes=test_block(template,small['rectangles'],small['matrix'],catalogue=catalogue)
    assert passes['status']=='PASSES'
    filtered,_=filter_catalogue(catalogue,block)
    rejected=False
    try:solve_design(template,filtered,0)
    except AssertionError:rejected=True
    assert rejected,'A conditional catalogue must never be usable without its branch assumptions.'
    rectangles,records=patterns(template)
    original=json.loads(Path(certificate['source_gram']).read_text())
    R=[[0]*21 for _ in range(21)]
    indices=[rectangles.index(tuple(e)) for e in original['edges']]
    for i,a in enumerate(indices):
        for j,b in enumerate(indices):R[a][b]=original['gram'][i][j]
    assert len(violations(R,records))==1
    target=violations(R,records)[0]
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=10
    high=[[0]*21 for _ in range(21)]
    for i in indices:high[i][i]=100
    high[target['C']][target['C']]=8
    a,c=target['A'],target['C'];high[a][c]=high[c][a]=-1
    matrices=[('saved_Gram_102',R,False),('zero_Gram_trigger_off',[[0]*21 for _ in range(21)],True),
              ('large_norm_trigger_on',high,True)]
    logic=[]
    for name,raw,expected_sat in matrices:
        assert (not violations(raw,records))==expected_sat
        model=cp_model.CpModel()
        K=[[None]*21 for _ in range(21)]
        for i,j in combinations_with_diagonal(21):
            value=4*(3*int(i==j)+1-len(set(rectangles[i])&set(rectangles[j])))-raw[i][j]
            K[i][j]=K[j][i]=model.new_int_var(value,value,f'K{i}_{j}')
        info=add_energy_implications(model,K,rectangles,template)
        assert not model.validate(),model.validate()
        status=solver.solve(model)
        assert (status in (cp_model.OPTIMAL,cp_model.FEASIBLE))==expected_sat
        logic.append({'name':name,'expected_sat':expected_sat,'status':solver.status_name(status),**info})
    A=np.zeros((243,243),dtype=np.int64)
    for line in graph_path.read_text().splitlines():
        if line.strip():
            u,v=map(int,line.split());A[u,v]=A[v,u]=1
    assert np.all(A.sum(axis=1)==22)
    assert np.array_equal(A@A+A,20*np.eye(243,dtype=np.int64)+2*np.ones_like(A))
    labels,gamma=extract_root(A.tolist(),0)
    qs=list(combinations(range(7),2))
    members=[[w for w,l in enumerate(labels) if tuple(a//2 for a in l)==q] for q in qs]
    gram=[[4*(3*int(i==j)+1-len(set(qs[i])&set(qs[j])))-sum(gamma[u][v] for u in members[i] for v in members[j])
           for j in range(21)] for i in range(21)]
    pair=next((i,j) for i,j in combinations(range(21),2)
              if gram[i][j]!=0 and integer_psd([[gram[i][i],gram[i][j]],[gram[j][i],gram[j][j]]]))
    b={'rectangles':[list(qs[i]) for i in pair],'matrix':[[gram[i][j] for j in pair] for i in pair]}
    model=cp_model.CpModel();g=[[0]*len(labels) for _ in labels]
    for u,v in combinations(range(len(labels)),2):
        if gamma[u][v]:
            e=model.new_bool_var(f'e{u}_{v}');model.add(e==1);g[u][v]=g[v][u]=e
    info=add_graph_block(model,g,labels,b)
    assert not model.validate(),model.validate()
    status=solver.solve(model)
    assert status in (cp_model.OPTIMAL,cp_model.FEASIBLE)
    return {'scope':__doc__,'partial4_filter':checked,'proper_block_passes':passes,
            'unguarded_conditional_catalogue_rejected':rejected,'implication_logic':logic,
            'srg243_affine_count_control':{'status':solver.status_name(status),**info},
            'status':'PARTIAL_GRAM_AND_ENERGY_CONTROLS_PASSED'}


def combinations_with_diagonal(n):
    return [(i,j) for i in range(n) for j in range(i,n)]


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--partial',type=Path,required=True)
    p.add_argument('--graph',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    resources=limit_research_process(1)
    r=run(a.directory,a.partial,a.graph);r['resources']=resources
    atomic_json_write(a.output,r)
    print(json.dumps({'status':r['status'],'implication_statuses':[x['status'] for x in r['implication_logic']],
                      'srg243':r['srg243_affine_count_control']}),flush=True)
