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


def solve_cpu(model,seconds):
    assert seconds>0
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.max_time_in_seconds=max(600,100*seconds)
    solver.parameters.cp_model_probing_level=0
    solver.parameters.symmetry_level=0
    solver.parameters.linearization_level=0
    started=time.process_time();done=threading.Event()
    def interrupt():
        while not done.wait(.05):
            if time.process_time()-started>=seconds:solver.stop_search();return
    timer=threading.Thread(target=interrupt,daemon=True);timer.start()
    try:status=solver.solve(model)
    finally:done.set();timer.join()
    return {'status':solver.status_name(status),'cpu_seconds':time.process_time()-started,
            'branches':solver.num_branches,'conflicts':solver.num_conflicts}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--index',type=int,required=True)
    parser.add_argument('--gram-index',type=int,required=True)
    parser.add_argument('--seconds',type=float,default=20,help='Actual CPU seconds per component branch.')
    parser.add_argument('--total-cpu-seconds',type=float,help='Maximum summed solver CPU time in this invocation; model construction is separate.')
    parser.add_argument('--limit-new',type=int)
    parser.add_argument('--component-range',type=int,nargs=2,metavar=('START','STOP'),help='Process this half-open range of current canonical codes; retain the full cover in the report.')
    parser.add_argument('--prefilter-seconds',type=float,default=0,help='First try the fixed-code base model, then add rotated constraints only if needed; included in the per-code CPU budget.')
    parser.add_argument('--minc-lines',type=int,default=1)
    parser.add_argument('--minc-balance',action='store_true')
    parser.add_argument('--line-profiles',type=int,default=1)
    parser.add_argument('--layer',type=int,default=0,choices=range(5))
    parser.add_argument('--local-tables',type=Path,required=True)
    parser.add_argument('--upper-projector',action='store_true')
    parser.add_argument('--rotated-boundary',action='store_true')
    parser.add_argument('--stabilizer-normalize',action='store_true')
    parser.add_argument('--short-norm',type=int,default=4)
    parser.add_argument('--boundary-projectors',action='store_true',help='Exact T and U Schur cuts after fixing the whole first line neighbourhood.')
    parser.add_argument('--rotated-rectangles',type=int,default=0,help='Number of additional E3 rectangles in the two fixed stars; corners remain variable.')
    parser.add_argument('--rotated-signatures',action='store_true',help='Project short integer eigenvectors onto each variable rotated rectangle.')
    parser.add_argument('--rotated-templates',action='store_true',help='Transport all pre-budget component graph templates to each complete neighbouring star.')
    parser.add_argument('--rotated-residuals',action='store_true',help='Exact99-coordinate integer residual norm and old-star eigen-equations for each rotated nine-set.')
    parser.add_argument('--fixed-cross-triangles',type=int,default=0,help='Apply the global minimum-component bound at newly fixed cross-colour triangles of the first component.')
    parser.add_argument('--fixed-star-triangles',type=int,default=0,help='Apply that bound also at newly fixed matched pairs within the two stars.')
    parser.add_argument('--reuse-proven',type=Path,help='Copy excluded codes with the same Gram, frame and matching catalogue; filtered code covers may differ.')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    assert args.prefilter_seconds>=0
    if args.component_range:assert 0<=args.component_range[0]<args.component_range[1]
    resources=limit_research_process(4)
    cover=next(r for r in json.loads((args.directory/'root_component_gram_orbits20.json').read_text())['records'] if r['template_index']==args.index)
    assert cover['exhaustive'] and cover['usable_as_gram_cover']
    values=cover['gram_anchor_values'][args.gram_index]
    all_templates=json.loads((args.directory/'root_component_templates.json').read_text())['survivors']
    template=all_templates[args.index]
    tables=json.loads(args.local_tables.read_text())
    context={};rotation_values={} if args.rotated_signatures else None
    model,graph,info=build(template,gram_matrix(cover,values),layer=args.layer,eigen=True,
        four_corners=True,local_tables=tables,minc_lines=args.minc_lines,
        line_profiles=args.line_profiles,profile_triples=True,exact_triangles=True,
        short_vectors=True,normalize_component=True,component_branch_context=context,
        upper_projector=args.upper_projector,rotated_boundary=args.rotated_boundary,
        stabilizer_normalize=args.stabilizer_normalize,short_norm=args.short_norm,minc_balance=args.minc_balance,
        rotated_signature_context=rotation_values)
    assert not model.validate(), model.validate()
    base_model_only=not context
    if base_model_only:
        # An empty signature/component domain can refute the unrestricted
        # Gram before selectors exist. Keep one unrestricted solver branch,
        # never regard an empty list of branches as a proof.
        context={'codes':[[]],'selectors':[],'root':None,'part':[]}
    codes=[list(c) for c in context['codes']]
    options={'layer':args.layer,'minc_lines':args.minc_lines,'line_profiles':args.line_profiles,
             'local_tables':str(args.local_tables),'seconds':args.seconds}
    for name in ('upper_projector','rotated_boundary','stabilizer_normalize','boundary_projectors','minc_balance','rotated_signatures','rotated_templates','rotated_residuals'):
        if getattr(args,name):options[name]=True
    if args.rotated_rectangles:options['rotated_rectangles']=args.rotated_rectangles
    if args.short_norm!=4:options['short_norm']=args.short_norm
    if args.prefilter_seconds:options['prefilter_seconds']=args.prefilter_seconds
    if args.fixed_cross_triangles:options['fixed_cross_triangles']=args.fixed_cross_triangles
    if args.fixed_star_triangles:options['fixed_star_triangles']=args.fixed_star_triangles
    if args.component_range:options['component_range']=args.component_range
    if args.total_cpu_seconds is not None:
        assert args.total_cpu_seconds>0
        options['total_cpu_seconds']=args.total_cpu_seconds
    branches=[]
    if args.output.exists():
        old=json.loads(args.output.read_text())
        assert old['options']==options
        previous=old['records'][0]['cases'][0]
        assert previous['gram_anchor_values']==values and previous['component_codes']==codes
        branches.extend(previous['branches'])
    elif args.reuse_proven:
        old=json.loads(args.reuse_proven.read_text())
        matches=[c for r in old['records'] if r['template_index']==args.index
                 for c in r['cases'] if c['gram_index']==args.gram_index]
        assert len(matches)==1
        previous=matches[0]
        assert previous['gram_anchor_values']==values
        if not base_model_only:
            assert previous['component_root']==context['root'] and previous['component_part']==context['part']
            prior_table_path=old.get('options',{}).get('local_tables') or old.get('local_E3_augmentation',{}).get('tables')
            assert prior_table_path, 'Code numbers need the original matching catalogue.'
            previous_tables=json.loads(Path(prior_table_path).read_text())
            size=6*len(context['part'])
            before=next(r for r in previous_tables['records'] if r['vertices']==size)
            after=next(r for r in tables['records'] if r['vertices']==size)
            for field in ('cross_permutations','internal_matchings'):assert before[field]==after[field]
            positions={tuple(code):i for i,code in enumerate(codes)}
            for r in previous['branches']:
                if r['status']!='INFEASIBLE' or tuple(r['code']) not in positions:continue
                assert previous['component_codes'][r['component_index']]==r['code']
                branches.append(dict(r,component_index=positions[tuple(r['code'])],
                    source_component_index=r['component_index'],source=str(args.reuse_proven)))
        elif previous.get('base_model_only') and previous['status']=='INFEASIBLE':
            branches.extend(dict(r,source=str(args.reuse_proven)) for r in previous['branches'] if r['status']=='INFEASIBLE')
    completed={r['component_index'] for r in branches}
    case=dict(info,gram_index=args.gram_index,gram_anchor_values=values,status='RUNNING',
              component_codes=codes,component_root=context['root'],component_part=context['part'],branches=branches,
              base_model_only=base_model_only)
    record={'template_index':args.index,'complete_source_gram_count':cover['gram_count'],'cases':[case]}
    def checkpoint():
        case['component_branch_counts']=dict(Counter(r['status'] for r in branches))
        case['all_component_branches_processed']=len(branches)==len(codes)
        case['status']='INFEASIBLE' if len(branches)==len(codes) and all(r['status']=='INFEASIBLE' for r in branches) else 'UNKNOWN'
        atomic_json_write(args.output,{'scope':__doc__,'options':options,'resources':resources,'records':[record]})
    checkpoint()
    case['branch_encoding']='Unrestricted base model with no component selectors.' if base_model_only else 'Hard-fixed component selectors in a cloned model; constants available to presolve.'
    processed=0;solver_cpu_used=0.0
    print(json.dumps({'template':args.index,'gram':args.gram_index,'component_codes':len(codes),'already_done':len(completed)}),flush=True)
    for i,code in enumerate(codes):
        if i in completed:continue
        if args.component_range and not args.component_range[0]<=i<args.component_range[1]:continue
        if args.limit_new is not None and processed>=args.limit_new:break
        branch_seconds=args.seconds
        if args.total_cpu_seconds is not None:
            remaining=args.total_cpu_seconds-solver_cpu_used
            if remaining<=0:break
            branch_seconds=min(branch_seconds,remaining)
        branch_model=model.clone()
        for selector,value in zip(context['selectors'],code):branch_model.add(selector==value)
        prefilter=solve_cpu(branch_model,min(args.prefilter_seconds,branch_seconds)) if args.prefilter_seconds else None
        if prefilter is not None and prefilter['status']=='INFEASIBLE':
            result=dict(prefilter,component_index=i,code=code,method='FIXED_CODE_BASE_MODEL',prefilter=prefilter)
            solver_cpu_used+=result['cpu_seconds']
            case['solver_cpu_seconds_this_invocation']=solver_cpu_used
            branches.append(result);processed+=1;checkpoint()
            print(json.dumps(dict(result,complete_gram_status=case['status'])),flush=True)
            continue
        remaining=branch_seconds-(prefilter['cpu_seconds'] if prefilter else 0)
        if remaining<=0:
            result={'component_index':i,'code':code,'status':'UNKNOWN','cpu_seconds':prefilter['cpu_seconds'],
                    'prefilter':prefilter,'method':'PREFILTER_BUDGET_EXHAUSTED'}
            solver_cpu_used+=result['cpu_seconds'];case['solver_cpu_seconds_this_invocation']=solver_cpu_used
            branches.append(result);processed+=1;checkpoint()
            print(json.dumps(dict(result,complete_gram_status=case['status'])),flush=True)
            continue
        boundary_info=None;cross_triangle_info=None
        rotated_info=None
        if (args.fixed_cross_triangles or args.fixed_star_triangles) and not base_model_only:
            from root_component_fixed_triangle_partitions import add_fixed_cross_triangle_partitions
            from root_component_boundary_psd import fixed_line_graph
            fixed=fixed_line_graph(graph,template,tables,context['root'],context['part'],code)
            cross_triangle_info=add_fixed_cross_triangle_partitions(branch_model,graph,fixed,context['root'],args.fixed_cross_triangles,
                eigen_context=rotation_values if args.rotated_signatures else None,star_count=args.fixed_star_triangles)
        if args.boundary_projectors and not base_model_only:
            from root_component_boundary_psd import add_profile_cuts
            boundary_info=add_profile_cuts(branch_model,graph,template,tables,context['root'],context['part'],code,complementary=True)
            print(json.dumps({'component_index':i,'boundary_projectors':{k:v for k,v in boundary_info.items() if k!='per_vertex'}}),flush=True)
        if args.rotated_rectangles and not base_model_only:
            from root_component_rotated_rectangles import add_rotated_rectangles
            rectangle_context=[]
            rotated_info=add_rotated_rectangles(branch_model,graph,template,tables,context['root'],context['part'],code,args.rotated_rectangles,rectangle_context)
            if args.rotated_residuals:
                from root_component_rotated_residual import add_rotated_residual_cuts
                from root_component_boundary_psd import fixed_line_graph
                fixed=fixed_line_graph(graph,template,tables,context['root'],context['part'],code)
                rotated_info['integer_residuals']=add_rotated_residual_cuts(branch_model,fixed,rectangle_context)
            if args.rotated_signatures:
                from root_component_short_vectors import add_rotated_signature_cuts
                rotated_info['short_signature_cuts']=add_rotated_signature_cuts(branch_model,rectangle_context,rotation_values)
            if args.rotated_templates:
                from root_component_rotated_templates import add_rotated_template_cover
                rotated_info['component_template_cover']=add_rotated_template_cover(branch_model,rectangle_context,template,all_templates,
                    eigen_context=rotation_values if args.rotated_signatures else None)
            print(json.dumps({'component_index':i,'phase':'model_ready',
                'rotated_rectangles':len(rotated_info['rectangles']),
                'variables':len(branch_model.proto.variables),
                'constraints':len(branch_model.proto.constraints)}),flush=True)
        assert not branch_model.validate(),branch_model.validate()
        result=dict(solve_cpu(branch_model,remaining),component_index=i,code=code)
        if prefilter is not None:
            result['prefilter']=prefilter
            result['strong_solver_cpu_seconds']=result['cpu_seconds']
            result['cpu_seconds']+=prefilter['cpu_seconds']
        solver_cpu_used+=result['cpu_seconds']
        case['solver_cpu_seconds_this_invocation']=solver_cpu_used
        if boundary_info is not None:result['boundary_projectors']=boundary_info
        if cross_triangle_info is not None:result['fixed_cross_triangle_partitions']=cross_triangle_info
        if rotated_info is not None:result['rotated_rectangles']=rotated_info
        branches.append(result);processed+=1;checkpoint()
        print(json.dumps({k:result[k] for k in ('component_index','code','status','cpu_seconds','branches','conflicts')} |
                         {'complete_gram_status':case['status'],'counts':case['component_branch_counts']}),flush=True)


if __name__=='__main__':main()
