"""Build a Gram cover ONLY for a root minimizing 9s+8g globally.

The supplied integer certificate removes template 7 at that chosen root.
Projection reports may remove Gram selectors only after an exhaustive
INFEASIBLE terminal call on all selectors not previously retained.
The arbitrary-root frontier and its Gram rows are never overwritten.
"""
import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_low_budget_transport import digest
from root_component_resources import atomic_json_write


def make_cover(source,certificate,projections):
    data=json.loads(source.read_text());proof=json.loads(certificate.read_text())
    assert proof['universal_inequality']=='3P+4G<=2772'
    assert proof['all_affine_columns_checked_exactly']==58
    assert proof['root_order']=='weighted_prisms_grids'
    selected=proof['remaining_selected_root_templates']
    assert selected==[9,19]
    omissions={};sources=[]
    for path in projections:
        report=json.loads(path.read_text())
        assert report['source_gram_cover_sha256_lf']==digest(source)
        assert report['root_order']=='weighted_prisms_grids'
        index=report['template_index'];assert index in selected
        if report['excluded_gram_indices']:
            assert report['exhaustive'] and report['status']=='INFEASIBLE'
            assert not report['unprocessed_gram_indices']
            assert not set(report['excluded_gram_indices']) & set(report['feasible_gram_indices'])
        omissions.setdefault(index,set()).update(report['excluded_gram_indices'])
        sources.append({'path':str(path),'sha256_lf':digest(path)})
    records=[]
    for index in selected:
        old=next(r for r in data['records'] if r['template_index']==index)
        assert old['exhaustive'] and old['usable_as_gram_cover']
        excluded=omissions.get(index,set());assert excluded<=set(old['source_gram_indices'])
        keep=[i for i,gi in enumerate(old['source_gram_indices']) if gi not in excluded]
        record=copy.deepcopy(old)
        record.update(root_order='weighted_prisms_grids',requires_selected_root=True,
                      usable_in_arbitrary_low_budget_root_frontier=False,
                      previous_gram_count=old['gram_count'],gram_count=len(keep),
                      selected_root_excluded_gram_indices=sorted(excluded),
                      source_gram_indices=[old['source_gram_indices'][i] for i in keep],
                      gram_anchor_values=[old['gram_anchor_values'][i] for i in keep])
        if 'gram_orbit_sizes' in old:
            record['gram_orbit_sizes']=[old['gram_orbit_sizes'][i] for i in keep]
            record['orbit_size_histogram']=dict(Counter(record['gram_orbit_sizes']))
        records.append(record)
    return {'scope':__doc__,'root_order':'weighted_prisms_grids',
            'usable_in_arbitrary_low_budget_root_frontier':False,
            'source_gram_cover':str(source),'source_gram_cover_sha256_lf':digest(source),
            'root_certificate':str(certificate),'root_certificate_sha256_lf':digest(certificate),
            'projection_sources':sources,'records':records,'global_conway_exclusion':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--root-certificate',type=Path,required=True)
    p.add_argument('--projections',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists():raise FileExistsError(a.output)
    result=make_cover(a.source,a.root_certificate,a.projections);atomic_json_write(a.output,result)
    print(json.dumps({'root_order':result['root_order'],'remaining':[
        [r['template_index'],r['gram_count']] for r in result['records']]}))


if __name__=='__main__':main()
