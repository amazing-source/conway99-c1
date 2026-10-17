"""Cover every canonical first-component code of one fixed Gram.

Only a COMPLETE set of INFEASIBLE branches excludes the Gram. A single
fixed component, a time limit, or a satisfiable relaxation never does.
The code cover is computed from the exact filtered invariant component set.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process, atomic_json_write
from root_component_signature_joint import build
from root_component_signature_moments import gram_matrix
from ortools.sat.python import cp_model


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--index',type=int,required=True)
    parser.add_argument('--gram-index',type=int,required=True)
    parser.add_argument('--seconds',type=float,default=20,help='Actual CPU seconds per component branch.')
    parser.add_argument('--limit-new',type=int)
    parser.add_argument('--minc-lines',type=int,default=1)
    parser.add_argument('--line-profiles',type=int,default=1)
    parser.add_argument('--layer',type=int,default=0,choices=range(5))
    parser.add_argument('--local-tables',type=Path,required=True)
    parser.add_argument('--upper-projector',action='store_true')
    parser.add_argument('--rotated-boundary',action='store_true')
    parser.add_argument('--stabilizer-normalize',action='store_true')
    parser.add_argument('--boundary-projectors',action='store_true',help='Exact T and U Schur cuts after fixing the whole first line neighbourhood.')
    parser.add_argument('--reuse-proven',type=Path,help='Copy only excluded branches from an identical code cover.')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    resources=limit_research_process(4)
    cover=next(r for r in json.loads((args.directory/'root_component_gram_orbits20.json').read_text())['records'] if r['template_index']==args.index)
    assert cover['exhaustive'] and cover['usable_as_gram_cover']
    values=cover['gram_anchor_values'][args.gram_index]
    template=json.loads((args.directory/'root_component_templates.json').read_text())['survivors'][args.index]
    tables=json.loads(args.local_tables.read_text())
    context={}
    model,graph,info=build(template,gram_matrix(cover,values),layer=args.layer,eigen=True,
        four_corners=True,local_tables=tables,minc_lines=args.minc_lines,
        line_profiles=args.line_profiles,profile_triples=True,exact_triangles=True,
        short_vectors=True,normalize_component=True,component_branch_context=context,
        upper_projector=args.upper_projector,rotated_boundary=args.rotated_boundary,
        stabilizer_normalize=args.stabilizer_normalize)
    assert not model.validate(), model.validate()
    assert context, 'A component cover is required; solve an empty base domain directly instead.'
    codes=[list(c) for c in context['codes']]
    options={'layer':args.layer,'minc_lines':args.minc_lines,'line_profiles':args.line_profiles,
             'local_tables':str(args.local_tables),'seconds':args.seconds}
    for name in ('upper_projector','rotated_boundary','stabilizer_normalize','boundary_projectors'):
        if getattr(args,name):options[name]=True
    branches=[]
    if args.output.exists():
        old=json.loads(args.output.read_text())
        assert old['options']==options
        previous=old['records'][0]['cases'][0]
        assert previous['gram_anchor_values']==values and previous['component_codes']==codes
        branches.extend(previous['branches'])
    elif args.reuse_proven:
        old=json.loads(args.reuse_proven.read_text())
        assert old['records'][0]['template_index']==args.index
        previous=old['records'][0]['cases'][0]
        assert previous['gram_index']==args.gram_index
        assert previous['gram_anchor_values']==values and previous['component_codes']==codes
        branches.extend(dict(r,source=str(args.reuse_proven)) for r in previous['branches'] if r['status']=='INFEASIBLE')
    completed={r['component_index'] for r in branches}
    case=dict(info,gram_index=args.gram_index,gram_anchor_values=values,status='RUNNING',
              component_codes=codes,component_root=context['root'],component_part=context['part'],branches=branches)
    record={'template_index':args.index,'complete_source_gram_count':cover['gram_count'],'cases':[case]}
    def checkpoint():
        case['component_branch_counts']=dict(Counter(r['status'] for r in branches))
        case['all_component_branches_processed']=len(branches)==len(codes)
        case['status']='INFEASIBLE' if len(branches)==len(codes) and all(r['status']=='INFEASIBLE' for r in branches) else 'UNKNOWN'
        atomic_json_write(args.output,{'scope':__doc__,'options':options,'resources':resources,'records':[record]})
    checkpoint()
    case['branch_encoding']='Hard-fixed component selectors in a cloned model; constants available to presolve.'
    processed=0
    print(json.dumps({'template':args.index,'gram':args.gram_index,'component_codes':len(codes),'already_done':len(completed)}),flush=True)
    for i,code in enumerate(codes):
        if i in completed:continue
        if args.limit_new is not None and processed>=args.limit_new:break
        branch_model=model.clone()
        for selector,value in zip(context['selectors'],code):branch_model.add(selector==value)
        boundary_info=None
        if args.boundary_projectors:
            from root_component_boundary_psd import add_profile_cuts
            boundary_info=add_profile_cuts(branch_model,graph,template,tables,context['root'],context['part'],code,complementary=True)
            print(json.dumps({'component_index':i,'boundary_projectors':{k:v for k,v in boundary_info.items() if k!='per_vertex'}}),flush=True)
        assert not branch_model.validate(),branch_model.validate()
        solver=cp_model.CpSolver()
        solver.parameters.num_search_workers=1
        solver.parameters.max_time_in_seconds=max(600,100*args.seconds)
        solver.parameters.cp_model_probing_level=0
        solver.parameters.symmetry_level=0
        solver.parameters.linearization_level=0
        started=time.process_time();done=threading.Event()
        def interrupt():
            while not done.wait(.05):
                if time.process_time()-started>=args.seconds:solver.stop_search();return
        timer=threading.Thread(target=interrupt,daemon=True);timer.start()
        try:status=solver.solve(branch_model)
        finally:done.set();timer.join()
        result={'component_index':i,'code':code,'status':solver.status_name(status),
                'cpu_seconds':time.process_time()-started,'branches':solver.num_branches,'conflicts':solver.num_conflicts}
        if boundary_info is not None:result['boundary_projectors']=boundary_info
        branches.append(result);processed+=1;checkpoint()
        print(json.dumps(dict(result,complete_gram_status=case['status'])),flush=True)


if __name__=='__main__':main()
