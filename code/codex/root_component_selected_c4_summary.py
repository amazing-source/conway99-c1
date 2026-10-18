"""Assemble the finite global-c>=4 exclusion, keeping chosen-root scope.

This records CP-SAT conclusions and their exact covering steps. It is not
a portable UNSAT proof, and does not exclude Conway graphs with c_min<=3.
"""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_low_budget_transport import digest
from root_component_resources import atomic_json_write
from root_component_root_order import root_choice_requirements
from root_component_rotated_gram import unsafe_product_reports


def assemble(directory, frontier):
    paths={
        'arbitrary_root_frontier':frontier,
        'weighted_root_certificate':directory/'weighted_root_certificate.json',
        'family9':directory/'c4_9_all_variable_base.json',
        'family19':directory/'c4_19_matching_summary_closed.json',
    }
    records={k:json.loads(p.read_text(encoding='utf-8-sig')) for k,p in paths.items()}
    f,w,nine,nineteen=(records[k] for k in paths)
    assert f['budget']==51 and len(f['budget_cover_template_indices'])==79
    assert len(f['excluded_template_indices'])==76 and f['allowed_template_indices']==[7,9,19]
    assert w['universal_inequality']=='3P+4G<=2772'
    assert w['integer_identity_scale']==9504 and w['all_affine_columns_checked_exactly']==58
    seven=next(r for r in w['survivor_cover'] if r['template_index']==7)
    assert seven['minimum_weighted_score']==528>seven['selected_root_score_upper']==504
    assert nine['template_index']==9 and nine['status']=='INFEASIBLE'
    assert nine['global_minimum_components']==4 and nine['all_matching_branches_processed']
    assert nine['matching_cover']==[None] and nine['options']['all_matchings_variable']
    assert all(b['status']=='INFEASIBLE' for b in nine['matching_branches'])
    assert nineteen['template_index']==19 and nineteen['template_excluded']
    assert nineteen['matching_cover']==list(range(9)) and not nineteen['open_matching_indices']
    assert set(map(int,nineteen['excluded_matching_sources']))==set(range(9))
    assert nineteen['gram_cover_equivalence']['all_base_fields_identical']
    for r in (nine,nineteen):
        assert root_choice_requirements(r)=={'weighted_prisms_grids'}
        assert not list(unsafe_product_reports(r))
    for source in nineteen['report_sources']:
        assert digest(source['path'])==source['sha256_lf']
    return {
        'scope':__doc__, 'status':'GLOBAL_MINIMUM_COMPONENTS_FOUR_EXCLUDED_BY_CP_SAT',
        'parameters':[99,14,1,2], 'excluded_hypothesis':'c(L)>=4 for every triangle L',
        'necessary_consequence':'Any srg(99,14,1,2) has a triangle L with c(L)<=3.',
        'chosen_root':'A vertex minimizing 9s(x)+8g(x)',
        'chosen_root_budget_derivation':'Score<=504 and g>=7 imply s<=49<=51.',
        'selected_root_template_count':79,'selected_root_excluded_count':79,
        'selected_root_open_template_indices':[],
        'arbitrary_low_budget_root_excluded_count':76,
        'arbitrary_low_budget_root_open_template_indices':[7,9,19],
        'usable_in_arbitrary_low_budget_root_frontier':False,
        'root_order':'weighted_prisms_grids',
        'seven_exclusion':seven,
        'nineteen_direct_matchings':[0,1,2,3,4],
        'nineteen_matching_orbits':[[0],[1,2],[3,6],[4,5,7,8]],
        'sources':{k:{'path':str(p),'sha256_lf':digest(p)} for k,p in paths.items()},
        'portable_unsat_proof':False,'global_conway_exclusion':False,
        'solver_consequence':'May anchor an arbitrary line with c<=3; this does not also grant prism budget51 at that line or its vertices.',
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory',type=Path,required=True)
    p.add_argument('--frontier',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    result=assemble(a.directory,a.frontier);atomic_json_write(a.output,result)
    print(json.dumps({k:result[k] for k in ('status','selected_root_excluded_count','necessary_consequence')}))


if __name__=='__main__':main()
