"""Filter Gram candidates at a selected root with9s+8g<=504.

Only binary C1/component equations and the complete prescribed Gram are
imposed. A feasible projection is not a Conway graph. After blocking
each feasible Gram selector, INFEASIBLE excludes exactly the unobserved
selectors. UNKNOWN leaves every unobserved selector open.
"""
import argparse
from fractions import Fraction as F
import json
from math import lcm
from pathlib import Path
import sys
import threading
import time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from root_component_propagation import LABELS,PAIRS,RECTANGLES,constraints,propagate
from root_component_low_budget_transport import digest
from root_component_root_order import add_weighted_root_budget


def build(template,cover):
    from ortools.sat.python import cp_model
    propagation=propagate(template)
    assert not propagation['conflict']
    fixed={i:value for i,value,_ in propagation['assignments']}
    model=cp_model.CpModel()
    variables=[fixed[i] if i in fixed else model.new_bool_var(f'e{i}') for i in range(len(PAIRS))]
    graph=[[0]*84 for _ in range(84)]
    for (u,v),value in zip(PAIRS,variables):graph[u][v]=graph[v][u]=value
    equations,bounds,_=constraints(template)
    for positions,target,_ in equations:model.add(sum(variables[i] for i in positions)==target)
    for positions,upper,_ in bounds:model.add(sum(variables[i] for i in positions)<=upper)
    choice=add_weighted_root_budget(model,graph,template)
    pairs=[tuple(p) for p in cover['anchor_pairs']]
    anchors={pair:model.new_int_var(-8,8,f'anchor_{pair}') for pair in pairs}
    selector=model.new_int_var(0,cover['gram_count']-1,'gram_selector')
    model.add_allowed_assignments([selector]+[anchors[pair] for pair in pairs],
        [[i]+values for i,values in enumerate(cover['gram_anchor_values'])])
    lift=[[F(*x) for x in row] for row in cover['lift_matrix']]
    edges=[tuple(e) for e in template['nongrid_edges']]
    assert len(lift)==len(edges)
    for i,e in enumerate(edges):
        for j in range(i+1):
            f=edges[j]
            if i==j:
                corners=RECTANGLES[e]
                expression=8-2*sum(graph[corners[a]][corners[b]] for a in range(4) for b in range(a+1,4))
            else:
                expression=(0 if set(e)&set(f) else 4)-sum(graph[u][v] for u in RECTANGLES[e] for v in RECTANGLES[f])
            weights={pair:lift[i][pair[0]]*lift[j][pair[1]]+
                     (lift[i][pair[1]]*lift[j][pair[0]] if pair[0]!=pair[1] else 0)
                     for pair in pairs}
            scale=lcm(*(x.denominator for x in weights.values()))
            model.add(scale*expression==sum(int(scale*w)*anchors[pair] for pair,w in weights.items() if w))
    assert not model.validate(),model.validate()
    return model,selector,choice


def run(directory,index,cover_path,seconds,output,resume=None):
    from ortools.sat.python import cp_model
    resources=limit_research_process(1)
    template=json.loads((directory/'root_component_templates.json').read_text())['survivors'][index]
    cover=next(r for r in json.loads(cover_path.read_text())['records'] if r['template_index']==index)
    assert cover['exhaustive'] and cover['usable_as_gram_cover']
    started=time.process_time();model,selector,choice=build(template,cover)
    result={'scope':__doc__,'template_index':index,'root_order':'weighted_prisms_grids',
        'source_gram_cover':str(cover_path),'source_gram_cover_sha256_lf':digest(cover_path),
        'input_gram_count':cover['gram_count'],'root_choice':choice,'resources':resources,
        'build_cpu_seconds':time.process_time()-started,'feasible_gram_indices':[],
        'excluded_gram_indices':[],'unprocessed_gram_indices':list(cover['source_gram_indices']),
        'status':'RUNNING','exhaustive':False,'portable_unsat_proof':False}
    found=set()
    if resume is not None:
        old=json.loads(resume.read_text(encoding='utf-8-sig'))
        assert old['template_index']==index and old['root_order']=='weighted_prisms_grids'
        assert old['source_gram_cover_sha256_lf']==digest(cover_path)
        # Skipping these previously feasible selectors is conservative: no
        # exclusion is inferred for them, even if an old witness was lost.
        previous=set(old['feasible_gram_indices'])
        assert previous<=set(cover['source_gram_indices'])
        found={i for i,gi in enumerate(cover['source_gram_indices']) if gi in previous}
        for i in found:model.add(selector!=i)
        result['reused_feasible_projections_from']=str(resume)
        result['feasible_gram_indices']=sorted(previous)
        result['unprocessed_gram_indices']=[gi for gi in cover['source_gram_indices'] if gi not in previous]
    atomic_json_write(output,result);start=time.process_time();step=0
    while time.process_time()-start<seconds:
        remaining=seconds-(time.process_time()-start)
        solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
        solver.parameters.linearization_level=0;solver.parameters.cp_model_probing_level=0
        solver.parameters.symmetry_level=0;solver.parameters.max_presolve_iterations=1
        solver.parameters.max_time_in_seconds=max(600,100*remaining)
        done=threading.Event();before=time.process_time()
        def interrupt():
            while not done.wait(.05):
                if time.process_time()-before>=remaining:solver.stop_search()
        timer=threading.Thread(target=interrupt,daemon=True);timer.start()
        try:status=solver.solve(model)
        finally:done.set();timer.join()
        step+=1
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            selected=solver.value(selector);assert selected not in found
            found.add(selected);model.add(selector!=selected)
        elif status==cp_model.INFEASIBLE:
            result['exhaustive']=True
            result['excluded_gram_indices']=[gi for i,gi in enumerate(cover['source_gram_indices']) if i not in found]
        else:assert status==cp_model.UNKNOWN,solver.status_name(status)
        result['status']=solver.status_name(status)
        result['feasible_gram_indices']=sorted(cover['source_gram_indices'][i] for i in found)
        result['unprocessed_gram_indices']=[] if result['exhaustive'] else [gi for i,gi in enumerate(cover['source_gram_indices']) if i not in found]
        result['solver_cpu_seconds']=time.process_time()-start
        atomic_json_write(output,result)
        if step%10==0 or status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            print(json.dumps({'template':index,'feasible':len(found),'excluded':len(result['excluded_gram_indices']),
                              'unprocessed':len(result['unprocessed_gram_indices']),'cpu':result['solver_cpu_seconds']}),flush=True)
        if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):break
        if len(found)==cover['gram_count']:
            result['exhaustive']=True;result['status']='ALL_GRAMS_HAVE_RELAXATION_WITNESS'
            atomic_json_write(output,result);break
    if not result['exhaustive'] and result['status'] in ('OPTIMAL','FEASIBLE','RUNNING'):
        result['status']='UNKNOWN_CPU_LIMIT'
        atomic_json_write(output,result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('--index',type=int,required=True)
    p.add_argument('--gram-cover',type=Path,required=True);p.add_argument('--seconds',type=float,default=60)
    p.add_argument('--resume',type=Path,help='Skip selectors with a previous relaxation witness from this exact cover.')
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise FileExistsError(a.output)
    r=run(a.directory,a.index,a.gram_cover,a.seconds,a.output,a.resume)
    print(json.dumps({'template':a.index,'status':r['status'],'exhaustive':r['exhaustive'],
        'feasible':len(r['feasible_gram_indices']),'excluded':len(r['excluded_gram_indices']),
        'unprocessed':len(r['unprocessed_gram_indices'])}))


if __name__=='__main__':main()
