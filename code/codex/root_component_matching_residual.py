"""Cover a fixed Gram by first internal matchings, leaving P and M1 free.

Each first-component canonical code belongs to exactly one M0 group.
Only an INFEASIBLE verdict on every group closes the Gram. The projected
root budget is applied conditionally, using an immutable earlier frontier.
"""
import argparse
import gc
import json
from pathlib import Path
import re
import sys
import threading
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def solve(model,seconds,log_search=False,linearization=0,solution_graph=None):
    from ortools.sat.python import cp_model
    assert not model.validate(),model.validate()
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.cp_model_probing_level=0;solver.parameters.symmetry_level=0
    assert linearization in (0,1,2)
    solver.parameters.linearization_level=linearization;solver.parameters.max_presolve_iterations=1
    solver.parameters.log_search_progress=log_search
    conflict_indices=[]
    if log_search:
        def log(message):
            match=re.search(r'Unsat after presolving constraint #(\d+)',message)
            if match:conflict_indices.append(int(match.group(1)))
        solver.log_callback=log
    solver.parameters.max_time_in_seconds=max(600,100*seconds)
    start=time.process_time();done=threading.Event()
    def stop():
        while not done.wait(.05):
            if time.process_time()-start>=seconds:solver.stop_search()
    timer=threading.Thread(target=stop,daemon=True);timer.start()
    try:status=solver.solve(model)
    finally:done.set();timer.join()
    result={'status':solver.status_name(status),'cpu_seconds':time.process_time()-start,
            'branches':solver.num_branches,'conflicts':solver.num_conflicts}
    if solution_graph is not None and status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        from conway_global_cover import reconstruct_and_check
        from root_component_propagation import LABELS
        gamma=[[solver.value(x) for x in row] for row in solution_graph]
        result['adjacency']=reconstruct_and_check(14,LABELS,gamma)
        result['exact_all_pair_check']=True
    if conflict_indices:
        index=conflict_indices[-1]
        result['presolve_conflict_hint']={'index':index,'not_a_portable_certificate':True}
        if index<len(model.proto.constraints):
            constraint=model.proto.constraints[index]
            result['presolve_conflict_hint']['original_constraint']=str(constraint)
            result['presolve_conflict_hint']['original_linear_variables']={str(i):
                {'name':model.proto.variables[i].name,'domain':list(model.proto.variables[i].domain)}
                for i in constraint.linear.vars}
            result['presolve_conflict_hint']['original_bool_variables']={str(i):
                {'name':model.proto.variables[i].name,'domain':list(model.proto.variables[i].domain)}
                for literal in constraint.bool_or.literals for i in [literal if literal>=0 else -literal-1]}
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('--index',type=int,required=True)
    p.add_argument('--gram-index',type=int,required=True);p.add_argument('--seconds',type=float,default=180)
    p.add_argument('--matching-indices',type=int,nargs='+')
    p.add_argument('--layer',type=int,choices=(1,2,3,4),default=2,
                   help='C2 pair layers; 4 imposes every common-neighbour equation.')
    p.add_argument('--low-budget-cover',type=Path,required=True)
    p.add_argument('--residual-gram-profiles',type=Path,required=True)
    p.add_argument('--residual-eigen',type=int,default=2)
    p.add_argument('--log-search',action='store_true')
    p.add_argument('--linearization',type=int,choices=(0,1,2),default=0)
    p.add_argument('--minimum-prism-root',action='store_true',help='Require the chosen root to minimize prism incidence globally; changes the scope of an exclusion.')
    p.add_argument('--weighted-prism-grid-root',action='store_true',help='Choose a global minimum of9s+8g, with score<=504. Alternative to minimizing s alone.')
    p.add_argument('--grid-intersections',action='store_true',help='Expose exact intersections of transported grids with fixed root grids.')
    p.add_argument('--grid-corner-tables',action='store_true',help='Enumerate all perfect matchings on the eight remaining labels when a transported rectangle is a grid.')
    p.add_argument('--no-rotations',action='store_true',help='Study the weaker base model split only by M0; no new star or residual is added.')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();resources=limit_research_process(1)
    assert not (args.minimum_prism_root and args.weighted_prism_grid_root)
    assert not args.output.exists(), 'Use a fresh report; never overwrite another proof.'
    from root_component_signature_joint import build
    from root_component_signature_moments import gram_matrix
    from root_component_low_budget_transport import digest
    from root_component_matching_rotation import add_matching_rotation
    from root_component_rotated_residual import add_rotated_residual_cuts
    from root_component_rotated_gram import add_gram_cuts,add_eigen_cuts,add_gram_kernel_cuts
    from root_component_rotated_templates import add_rotated_template_cover
    from root_component_rotated_gram_profiles import add_profile_cuts
    from root_component_short_vectors import add_rotated_signature_cuts
    directory=args.directory
    covers=json.loads((directory/'root_component_gram_orbits20.json').read_text())['records']
    cover=next(r for r in covers if r['template_index']==args.index)
    assert cover['exhaustive'] and cover['usable_as_gram_cover']
    templates=json.loads((directory/'root_component_templates.json').read_text())['survivors']
    template=templates[args.index];values=cover['gram_anchor_values'][args.gram_index]
    tables=json.loads((directory/'line_component_pattern_tables_e3_all_colours.json').read_text())
    frontier=json.loads(args.low_budget_cover.read_text());profiles=json.loads(args.residual_gram_profiles.read_text())
    assert profiles['template_frontier_sha256_lf']==digest(args.low_budget_cover)
    component={};eigen_context={};started=time.process_time()
    base,graph,info=build(template,gram_matrix(cover,values),layer=args.layer,eigen=True,
        four_corners=True,local_tables=tables,minc_lines=2,line_profiles=2,
        profile_triples=True,exact_triangles=True,short_vectors=True,
        normalize_component=True,component_branch_context=component,
        upper_projector=True,rotated_boundary=True,stabilizer_normalize=True,
        short_norm=8,minc_balance=True,rotated_signature_context=eigen_context)
    if args.weighted_prism_grid_root:
        from root_component_root_order import add_weighted_root_budget
        info['root_choice']=add_weighted_root_budget(base,graph,template)
    codes=component.get('codes',[])
    matchings=sorted({code[1] for code in codes}) if component else [None]
    selected=args.matching_indices if args.matching_indices is not None else matchings
    assert set(selected)<=set(matchings)
    case={'gram_index':args.gram_index,'gram_anchor_values':values,'status':'UNKNOWN',
          'component_codes':codes,'matching_cover':matchings,'matching_branches':[],
          'build_cpu_seconds':time.process_time()-started,'base_model':info,
          'component_root':component.get('root'),'component_part':component.get('part'),
          'all_matching_branches_processed':False}
    result={'scope':__doc__,'resources':resources,'options':{
        'seconds_per_matching':args.seconds,'residual_eigen':args.residual_eigen,'no_rotations':args.no_rotations,
        'linearization':args.linearization,'layer':args.layer,
        'minimum_prism_root':args.minimum_prism_root,
        'weighted_prism_grid_root':args.weighted_prism_grid_root,
        'grid_intersections':args.grid_intersections,
        'grid_corner_tables':args.grid_corner_tables,
        'low_budget_cover':str(args.low_budget_cover),'low_budget_cover_sha256_lf':digest(args.low_budget_cover),
        'residual_gram_profiles':str(args.residual_gram_profiles),'residual_gram_profiles_sha256_lf':digest(args.residual_gram_profiles)},
        'records':[{'template_index':args.index,'complete_source_gram_count':cover['gram_count'],'cases':[case]}]}
    atomic_json_write(args.output,result)
    print(json.dumps({'gram_index':args.gram_index,'component_codes':len(codes),'matching_cover':matchings,
                      'build_cpu_seconds':case['build_cpu_seconds']}),flush=True)
    for mi in selected:
        start=time.process_time();model=base.clone();rotation=None;boundaries=[('base',len(model.proto.constraints))]
        if mi is not None and args.no_rotations:
            model.add(component['selectors'][1]==mi)
        elif mi is not None:
            fixed,rectangles,rotation=add_matching_rotation(model,graph,template,tables,component,mi)
            boundaries.append(('matching_rotation',len(model.proto.constraints)))
            if len(rectangles)==15:
                if args.grid_intersections or args.grid_corner_tables:
                    from root_component_grid_intersections import add_grid_intersection_cuts
                    rotation['grid_intersections']=add_grid_intersection_cuts(model,template,rectangles,args.grid_corner_tables)
                if args.minimum_prism_root:
                    from root_component_root_order import add_minimum_root_cuts
                    rotation['root_choice']=add_minimum_root_cuts(model,graph,rectangles)
                if args.weighted_prism_grid_root:
                    from root_component_root_order import add_weighted_root_comparisons
                    rotation['root_choice']=add_weighted_root_comparisons(model,graph,template,rectangles)
                rotation['integer_residuals']=add_rotated_residual_cuts(model,fixed,rectangles,tight_bounds=True)
                boundaries.append(('residuals',len(model.proto.constraints)))
                rotation['integer_gram']=add_gram_cuts(model,rectangles,'all')
                rotation['gram_kernel']=add_gram_kernel_cuts(model,rectangles)
                boundaries.append(('gram',len(model.proto.constraints)))
                if args.residual_eigen:rotation['full_eigen']=add_eigen_cuts(model,fixed,rectangles,args.residual_eigen)
                boundaries.append(('eigen',len(model.proto.constraints)))
                rotation['short_signatures']=add_rotated_signature_cuts(model,rectangles,eigen_context)
                boundaries.append(('short_signatures',len(model.proto.constraints)))
                # Old-line corners are variable. Omit the optional projection
                # energy cuts, whose old implementation assumes fixed corners.
                rotation['templates']=add_rotated_template_cover(model,rectangles,template,templates,low_budget_snapshot=frontier)
                boundaries.append(('templates',len(model.proto.constraints)))
                rotation['profiles']=add_profile_cuts(model,rectangles,profiles)
                boundaries.append(('profiles',len(model.proto.constraints)))
        branch={'matching_index':mi,'component_code_count':sum(code[1]==mi for code in codes),
                'variables':len(model.proto.variables),'constraints':len(model.proto.constraints),
                'constraint_stage_endpoints':boundaries,
                'build_cpu_seconds':time.process_time()-start}
        print(json.dumps(dict(branch,phase='model_ready')),flush=True)
        branch.update(solve(model,args.seconds,args.log_search,args.linearization))
        if rotation is not None:branch['rotation']=rotation
        case['matching_branches'].append(branch)
        processed={r['matching_index'] for r in case['matching_branches']}
        case['all_matching_branches_processed']=processed==set(matchings)
        if case['all_matching_branches_processed'] and all(r['status']=='INFEASIBLE' for r in case['matching_branches']):
            case['status']='INFEASIBLE'
        atomic_json_write(args.output,result)
        print(json.dumps({k:branch[k] for k in ('matching_index','status','cpu_seconds','branches','conflicts')}|
                         {'complete_gram_status':case['status']}),flush=True)
        del model;gc.collect()


if __name__=='__main__':main()
