"""Isolate the rectangle coordinates sufficient for a Gram-free CP contradiction.

The shared-edge count products remain exact even when an equation guard
is off. Guards activate only the final row equations. UNKNOWN never
removes a coordinate from the sufficient set.
"""

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process
from root_component_row_neighbor_moments import coordinates_for_catalogue,add_row_moments
from root_component_z_joint import build_joint,solve_joint


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('catalogue',type=Path);p.add_argument('--seconds',type=float,default=5)
    p.add_argument('--fresh-models',action='store_true',help='Rebuild unguarded models to keep CP presolve active.')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    resources=limit_research_process(1)
    doc=json.loads(a.catalogue.read_text(encoding='utf-8-sig'))
    template,catalogue=doc['template'],doc['catalogue']
    coordinates=coordinates_for_catalogue(catalogue,template)
    if a.fresh_models:
        result={'scope':__doc__,'source':str(a.catalogue),'resources':resources,
                'strategy':'Fresh unguarded models; UNKNOWN retains the coordinate.',
                'trials':[],'uses_Gram_cover':False,'uses_prism_budget':False,'portable_unsat_proof':False}
        def fresh(active):
            diagnostic={}
            model,labels,graph=build_joint(14,catalogue['row_types'],template['nongrid_edges'],
                mate_normalize=True,row_moment_coordinates=active,diagnostics=diagnostic)
            record=solve_joint(model,labels,graph,14,a.seconds)
            record['coordinates']=list(active)
            result['trials'].append(record);atomic_json_write(a.output,result)
            print(json.dumps({k:v for k,v in record.items() if k not in ('Gamma','C2_violations','srg')}),flush=True)
            return record
        first=fresh(coordinates)
        if first['status']!='INFEASIBLE':
            result['status']='NO_CORE_WITHIN_BUDGET'
        else:
            current=list(coordinates)
            for j in list(current):
                trial=fresh([i for i in current if i!=j])
                if trial['status']=='INFEASIBLE':current.remove(j)
            result.update(status='SUFFICIENT_COORDINATE_CORE',sufficient_coordinates=current,
                minimality_proved=all(t['status']!='UNKNOWN' for t in result['trials']))
        atomic_json_write(a.output,result)
        return
    model,labels,graph=build_joint(14,catalogue['row_types'],template['nongrid_edges'],mate_normalize=True)
    guards={j:model.new_bool_var(f'coordinate_{j}') for j in coordinates}
    reverse={g.index:j for j,g in guards.items()}
    info=add_row_moments(model,graph,labels,catalogue['row_types'],coordinates,guards=guards)
    result={'scope':__doc__,'source':str(a.catalogue),'resources':resources,'model':info,
            'trials':[],'uses_Gram_cover':False,'uses_prism_budget':False,'portable_unsat_proof':False}
    def solve(active):
        model.clear_assumptions();model.add_assumptions([guards[j] for j in active])
        record=solve_joint(model,labels,graph,14,a.seconds)
        record['coordinates']=list(active)
        if 'sufficient_assumptions' in record:
            record['sufficient_coordinates']=[reverse[g] for g in record['sufficient_assumptions']]
        result['trials'].append(record);atomic_json_write(a.output,result)
        print(json.dumps({k:v for k,v in record.items() if k not in ('Gamma','C2_violations','srg')}),flush=True)
        return record
    first=solve(coordinates)
    if first['status']!='INFEASIBLE':
        result['status']='NO_CORE_WITHIN_BUDGET'
    else:
        current=first['sufficient_coordinates']
        for j in list(current):
            if j not in current:continue
            trial=solve([i for i in current if i!=j])
            if trial['status']=='INFEASIBLE':
                current=trial['sufficient_coordinates']
        result.update(status='SUFFICIENT_COORDINATE_CORE',sufficient_coordinates=current,
                      minimality_proved=all(t['status']!='UNKNOWN' for t in result['trials']))
    atomic_json_write(a.output,result)


if __name__=='__main__':main()
