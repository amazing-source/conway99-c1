"""Positive/negative controls for selector-dependent vertex kernel cuts.

The two PSD Gram fixtures have different kernels. Their binary graph
relaxations are satisfiable separately, even when the other Gram's kernel
is violated. Violating the selected Gram's kernel must be infeasible.
These fixtures are not asserted to be SRGs.
"""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ortools.sat.python import cp_model
from root_component_finite_gram_kernel import prepare
from root_component_gram_table import add_gram_table
from root_component_propagation import RECTANGLES
from root_component_resources import atomic_json_write,limit_research_process


def fixture():
    template={'nongrid_edges':[[0,1],[2,3]],'nontrivial_component_groups':[[] for _ in range(7)]}
    record={'anchors':[0,1],'anchor_pairs':[[0,0],[0,1],[1,1]],
            'lift_matrix':[[[1,1],[0,1]],[[0,1],[1,1]]],
            'gram_anchor_values':[[4,4,4],[4,-4,4]],'gram_count':2,
            'exhaustive':True,'usable_as_gram_cover':True,'root_prism_budget':51,
            'requires_separate_corner_realization':False}
    return template,record


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists();resources=limit_research_process(1)
    template,record=fixture();profile=prepare(template,record)
    assert sorted(c['gram_selectors'] for c in profile['extra_vectors'])==[[0],[1]]
    results=[]
    for gi in (0,1):
        for violate_selected in (False,True):
            model=cp_model.CpModel();graph=[[0]*84 for _ in range(84)]
            for i in range(84):
                for j in range(i):graph[i][j]=graph[j][i]=model.new_bool_var(f'g_{i}_{j}')
            info=add_gram_table(model,graph,template,record,kernel_lifting=True)
            assert info['finite_gram_vertex_kernels']['vertex_kernel_equations']==168
            assert info['finite_gram_vertex_kernels']['conditional_selector_groups']==2
            selector_index=next(i for i,v in enumerate(model.proto.variables) if v.name=='gram_selector')
            model.add(model.get_int_var_from_proto_index(selector_index)==gi)
            q0,q1=RECTANGLES[(0,1)],RECTANGLES[(2,3)];w=q0[0]
            h0=2-sum(graph[w][q] for q in q0)
            h1=1-sum(graph[w][q] for q in q1)
            tested_gram=gi if violate_selected else 1-gi
            model.add(h0+(-1 if tested_gram==0 else 1)*h1!=0)
            assert not model.validate(),model.validate()
            solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
            solver.parameters.max_time_in_seconds=10
            status=solver.solve(model)
            expected=cp_model.INFEASIBLE if violate_selected else cp_model.OPTIMAL
            assert status==expected,(gi,violate_selected,solver.status_name(status))
            results.append({'gram_selector':gi,'violate_selected_kernel':violate_selected,
                            'status':solver.status_name(status)})
    atomic_json_write(a.output,{'status':'PASSED','scope':__doc__,'resources':resources,
                               'kernel_profile':profile,'controls':results})
    print(json.dumps({'status':'PASSED','controls':results}))


if __name__=='__main__':main()
