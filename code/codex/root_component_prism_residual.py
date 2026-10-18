"""Use both complete stars of a six-prism line without fixing any code.

Every first-component code remains variable. Thus an INFEASIBLE result
closes the whole fixed Gram directly, without enumerating hundreds of
component codes. Rotated templates use the pre-budget cover, since the
new root need not have prism budget51.
"""
import argparse
import json
from pathlib import Path
import sys
import threading
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--index',type=int,default=7)
    parser.add_argument('--gram-index',type=int,required=True)
    parser.add_argument('--seconds',type=float,default=300)
    parser.add_argument('--linearization',type=int,choices=(0,1,2),default=0)
    parser.add_argument('--presolve-iterations',type=int,default=3)
    parser.add_argument('--low-budget-cover',type=Path)
    parser.add_argument('--residual-gram',choices=('incident','all'))
    parser.add_argument('--residual-eigen',type=int,default=0)
    parser.add_argument('--tight-residual-bounds',action='store_true')
    parser.add_argument('--residual-gram-profiles',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();resources=limit_research_process(1)
    from ortools.sat.python import cp_model
    from root_component_signature_joint import build
    from root_component_signature_moments import gram_matrix
    from root_component_rotated_rectangles import add_rotated_rectangles
    from root_component_rotated_residual import add_rotated_residual_cuts
    from root_component_rotated_templates import add_rotated_template_cover
    from root_component_short_vectors import add_rotated_signature_cuts
    directory=args.directory
    covers=json.loads((directory/'root_component_gram_orbits20.json').read_text())['records']
    cover=next(r for r in covers if r['template_index']==args.index)
    assert cover['exhaustive'] and cover['usable_as_gram_cover']
    values=cover['gram_anchor_values'][args.gram_index]
    templates=json.loads((directory/'root_component_templates.json').read_text())['survivors']
    template=templates[args.index]
    roots=[i for i,parts in enumerate(template['nontrivial_component_groups']) if not parts]
    assert roots, 'There must be a known six-prism line.'
    tables=json.loads((directory/'line_component_pattern_tables_e3_all_colours.json').read_text())
    low_snapshot=json.loads(args.low_budget_cover.read_text()) if args.low_budget_cover else None
    gram_profiles=json.loads(args.residual_gram_profiles.read_text()) if args.residual_gram_profiles else None
    assert gram_profiles is None or low_snapshot is not None and args.residual_gram=='all'
    if gram_profiles is not None:
        from root_component_low_budget_transport import digest
        assert gram_profiles['template_frontier_sha256_lf']==digest(args.low_budget_cover)
    eigen_context={};component_context={};started=time.process_time()
    model,graph,info=build(template,gram_matrix(cover,values),layer=2,eigen=True,
        four_corners=True,local_tables=tables,minc_lines=2,line_profiles=2,
        profile_triples=True,exact_triangles=True,short_vectors=True,
        normalize_component=True,component_branch_context=component_context,
        upper_projector=True,rotated_boundary=True,stabilizer_normalize=True,
        short_norm=8,minc_balance=True,rotated_signature_context=eigen_context)
    rotations=[]
    if component_context:
        for root in roots:
            context=[]
            rotation=add_rotated_rectangles(model,graph,template,tables,root,[],[],30,context)
            rotation['integer_residuals']=add_rotated_residual_cuts(model,graph,context,tight_bounds=args.tight_residual_bounds)
            if args.residual_gram:
                from root_component_rotated_gram import add_gram_cuts
                rotation['integer_gram']=add_gram_cuts(model,context,args.residual_gram)
            if args.residual_eigen:
                from root_component_rotated_gram import add_eigen_cuts
                rotation['full_residual_eigen']=add_eigen_cuts(model,graph,context,args.residual_eigen)
            rotation['short_signature_cuts']=add_rotated_signature_cuts(model,context,eigen_context)
            rotation['component_template_cover']=add_rotated_template_cover(model,context,template,templates,eigen_context=eigen_context,low_budget_snapshot=low_snapshot)
            if gram_profiles is not None:
                from root_component_rotated_gram_profiles import add_profile_cuts
                rotation['frozen_gram_profiles']=add_profile_cuts(model,context,gram_profiles)
            rotations.append(rotation)
    assert not model.validate(),model.validate()
    case=dict(info,gram_index=args.gram_index,gram_anchor_values=values,status='UNKNOWN',
        fixed_component_code=False,component_code_count=len(component_context.get('codes',[])),
        six_prism_rotations=rotations,build_cpu_seconds=time.process_time()-started,
        variables=len(model.proto.variables),constraints=len(model.proto.constraints))
    record={'template_index':args.index,'complete_source_gram_count':cover['gram_count'],'cases':[case]}
    result={'scope':__doc__,'resources':resources,'options':{'seconds':args.seconds,'linearization':args.linearization},'records':[record]}
    if args.low_budget_cover:
        from root_component_low_budget_transport import digest
        result['options'].update(low_budget_cover=str(args.low_budget_cover),low_budget_cover_sha256_lf=digest(args.low_budget_cover))
    if args.residual_gram:result['options']['residual_gram']=args.residual_gram
    if args.residual_eigen:result['options']['residual_eigen']=args.residual_eigen
    if args.presolve_iterations!=3:result['options']['presolve_iterations']=args.presolve_iterations
    if args.tight_residual_bounds:result['options']['tight_residual_bounds']=True
    if args.residual_gram_profiles:
        from root_component_low_budget_transport import digest
        result['options'].update(residual_gram_profiles=str(args.residual_gram_profiles),residual_gram_profiles_sha256_lf=digest(args.residual_gram_profiles))
    atomic_json_write(args.output,result)
    print(json.dumps({k:case[k] for k in ('gram_index','component_code_count','build_cpu_seconds','variables','constraints')}),flush=True)
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    solver.parameters.cp_model_probing_level=0;solver.parameters.symmetry_level=0
    solver.parameters.linearization_level=args.linearization
    solver.parameters.max_presolve_iterations=args.presolve_iterations
    solver.parameters.max_time_in_seconds=max(600,100*args.seconds)
    started=time.process_time();done=threading.Event()
    def interrupt():
        while not done.wait(.05):
            if time.process_time()-started>=args.seconds:solver.stop_search()
    timer=threading.Thread(target=interrupt,daemon=True);timer.start()
    try:status=solver.solve(model)
    finally:done.set();timer.join()
    case.update(status=solver.status_name(status),cpu_seconds=time.process_time()-started,
                branches=solver.num_branches,conflicts=solver.num_conflicts)
    atomic_json_write(args.output,result)
    print(json.dumps({k:case[k] for k in ('gram_index','status','cpu_seconds','branches','conflicts')}),flush=True)


if __name__=='__main__':main()
