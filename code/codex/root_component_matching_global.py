"""A whole-template model with variable Gram and transported complete stars.

The Gram ranges over an exhaustive earlier cover; none is chosen as a seed.
A known six-prism line needs no matching split. Otherwise the canonical
first-component codes are partitioned only by their first matching index.
Every branch must be INFEASIBLE before the whole template can be excluded.
"""
import argparse
import gc
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('--index',type=int,required=True)
    p.add_argument('--gram-cover',type=Path,required=True)
    p.add_argument('--seconds',type=float,default=120)
    p.add_argument('--matching-indices',type=int,nargs='+')
    p.add_argument('--low-budget-cover',type=Path,required=True)
    p.add_argument('--residual-gram-profiles',type=Path,required=True)
    p.add_argument('--residual-eigen',type=int,default=2)
    p.add_argument('--log-search',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();resources=limit_research_process(1)
    assert not args.output.exists()
    from root_component_global import build
    from root_component_local_tables import add_local_component_tables
    from root_component_minimum_partition import add_minimum_partitions
    from root_component_exact_triangles import add_exact_triangle_structure
    from root_component_matching_rotation import add_matching_rotation
    from root_component_rotated_rectangles import add_rotated_rectangles
    from root_component_rotated_residual import add_rotated_residual_cuts
    from root_component_rotated_gram import add_gram_cuts,add_eigen_cuts
    from root_component_rotated_templates import add_rotated_template_cover
    from root_component_rotated_gram_profiles import add_profile_cuts
    from root_component_low_budget_transport import digest
    from root_component_matching_residual import solve
    directory=args.directory
    templates=json.loads((directory/'root_component_templates.json').read_text())['survivors']
    template=templates[args.index]
    records=json.loads((directory/'root_component_gram_budget51.json').read_text())['records']
    gram_record=next(r for r in records if r['template_index']==args.index)
    cover=next(r for r in json.loads(args.gram_cover.read_text())['records'] if r['template_index']==args.index)
    assert cover['gram_count']>0 and cover['exhaustive'] and cover['usable_as_gram_cover']
    tables=json.loads((directory/'line_component_pattern_tables_e3_all_colours.json').read_text())
    frontier=json.loads(args.low_budget_cover.read_text());profiles=json.loads(args.residual_gram_profiles.read_text())
    assert profiles['template_frontier_sha256_lf']==digest(args.low_budget_cover)
    start=time.process_time();component={}
    base,graph,info=build(template,gram_record,gram_cover=cover)
    assert base is not None
    info['component_tables']=add_local_component_tables(base,graph,template,tables,
        normalize_first=True,branch_context=component)
    info['nonroot_partitions']=add_minimum_partitions(base,graph,2,balance=True)
    info['triangle_structure']=add_exact_triangle_structure(base,graph,template)
    prism_roots=[i for i,parts in enumerate(template['nontrivial_component_groups']) if not parts]
    use_prism=bool(prism_roots)
    matchings=[None] if use_prism else sorted({code[1] for code in component['codes']})
    selected=args.matching_indices if args.matching_indices is not None else matchings
    assert set(selected)<=set(matchings)
    result={'scope':__doc__,'template_index':args.index,'status':'UNKNOWN',
        'root_prism_budget':51,'global_minimum_components':4,
        'complete_gram_cover':info['complete_gram_cover'],'gram_cover':str(args.gram_cover),
        'gram_cover_sha256_lf':digest(args.gram_cover),'fixed_gram_witness':False,
        'resources':resources,'model':info,'build_cpu_seconds':time.process_time()-start,
        'options':{'seconds_per_matching':args.seconds,'residual_eigen':args.residual_eigen,
            'low_budget_cover':str(args.low_budget_cover),'low_budget_cover_sha256_lf':digest(args.low_budget_cover),
            'residual_gram_profiles':str(args.residual_gram_profiles),'residual_gram_profiles_sha256_lf':digest(args.residual_gram_profiles)},
        'known_six_prism_root':prism_roots[0] if use_prism else None,
        'component_codes':component.get('codes',[]),'matching_cover':matchings,
        'matching_branches':[],'all_matching_branches_processed':False,
        'portable_unsat_proof':False,'global_conway_exclusion':False}
    atomic_json_write(args.output,result)
    print(json.dumps({'template_index':args.index,'gram_count':cover['gram_count'],
                      'matching_cover':matchings,'build_cpu_seconds':result['build_cpu_seconds']}),flush=True)
    for mi in selected:
        model=base.clone();rectangles=[];start=time.process_time()
        if use_prism:
            fixed=graph
            rotation=add_rotated_rectangles(model,graph,template,tables,prism_roots[0],[],[],30,rectangles)
        else:
            fixed,rectangles,rotation=add_matching_rotation(model,graph,template,tables,component,mi)
        if len(rectangles) in (15,30):
            rotation['residuals']=add_rotated_residual_cuts(model,fixed,rectangles,tight_bounds=True)
            rotation['gram']=add_gram_cuts(model,rectangles,'all')
            if args.residual_eigen:rotation['eigen']=add_eigen_cuts(model,fixed,rectangles,args.residual_eigen)
            rotation['templates']=add_rotated_template_cover(model,rectangles,template,templates,low_budget_snapshot=frontier)
            rotation['profiles']=add_profile_cuts(model,rectangles,profiles)
        else:
            assert rotation.get('empty_corner_domain')
            model.add(False)
        branch={'matching_index':mi,'rotation':rotation,'variables':len(model.proto.variables),
                'constraints':len(model.proto.constraints),'build_cpu_seconds':time.process_time()-start}
        print(json.dumps({k:branch[k] for k in ('matching_index','variables','constraints','build_cpu_seconds')}|{'phase':'model_ready'}),flush=True)
        branch.update(solve(model,args.seconds,args.log_search))
        result['matching_branches'].append(branch)
        result['all_matching_branches_processed']={b['matching_index'] for b in result['matching_branches']}==set(matchings)
        if result['all_matching_branches_processed'] and all(b['status']=='INFEASIBLE' for b in result['matching_branches']):result['status']='INFEASIBLE'
        atomic_json_write(args.output,result)
        print(json.dumps({k:branch[k] for k in ('matching_index','status','cpu_seconds','branches','conflicts')}|
                         {'complete_template_status':result['status']}),flush=True)
        del model;gc.collect()


if __name__=='__main__':main()
