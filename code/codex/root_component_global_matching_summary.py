"""Merge matching branches of an identical whole-template Gram model.

Only an INFEASIBLE record closes a matching. Root choice, Gram cover,
the labelled full-star matching cover and every transported frontier
must agree. No isomorphism between different matching frames is assumed.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_low_budget_transport import digest
from root_component_resources import atomic_json_write
from root_component_root_order import root_choice_requirements
from root_component_rotated_gram import unsafe_product_reports


def compare_base_gram_covers(reports, base_path):
    """Allow additional necessary tables only when every base field agrees.

    In particular, the ordered Gram values, source indices, anchors, lift,
    budget and root-choice scope are compared exactly, not just the count.
    The original report hashes must still match the actual cover files.
    """
    base=json.loads(base_path.read_text(encoding='utf-8-sig'))
    index=reports[0]['template_index']
    base_record=next(r for r in base['records'] if r['template_index']==index)
    assert base_record['exhaustive'] and base_record['usable_as_gram_cover']
    allowed_extra={'corner_orientation_factorization','corner_signature_tables',
                   'coupled_corner_eliminated_indices','coupled_corner_scope',
                   'row_signature_tables'}
    compared=[]
    for report in reports:
        path=Path(report['gram_cover'])
        assert digest(path)==report['gram_cover_sha256_lf'],f'Cover changed: {path}'
        cover=json.loads(path.read_text(encoding='utf-8-sig'))
        record=next(r for r in cover['records'] if r['template_index']==index)
        for key,value in base_record.items():
            assert record.get(key)==value,f'Different base Gram field {key}: {path}'
        for key,value in base.items():
            if key!='records':assert cover.get(key)==value,f'Different cover scope {key}: {path}'
        extra=set(record)-set(base_record)
        assert extra<=allowed_extra,f'Unrecognised additional cover fields: {extra-allowed_extra}'
        assert not record.get('coupled_corner_eliminated_indices'), 'Gram selection changed.'
        compared.append({'path':str(path),'sha256_lf':digest(path),
                         'additional_fields':sorted(extra)})
    return {'base_cover':str(base_path),'base_cover_sha256_lf':digest(base_path),
            'template_index':index,'gram_count':base_record['gram_count'],
            'all_base_fields_identical':True,'source_covers':compared,
            'scope':compare_base_gram_covers.__doc__}


def merge(paths, residual_mate_flips=False, same_base_gram_cover=None):
    texts=[p.read_text(encoding='utf-8-sig') for p in paths]
    reports=[json.loads(t) for t in texts]
    first=reports[0];order=root_choice_requirements(first)
    assert len(order)<=1
    keys=('template_index','global_minimum_components',
          'complete_matching_root','complete_star_matching_cover','matching_cover','component_codes')
    equivalence=None
    if same_base_gram_cover is None:keys+=('gram_cover_sha256_lf',)
    else:equivalence=compare_base_gram_covers(reports,same_base_gram_cover)
    required=set(first['matching_cover']);closed={};attempts=[]
    for path,report in zip(paths,reports):
        assert not list(unsafe_product_reports(report)),f'Withdrawn product encoding: {path}'
        assert root_choice_requirements(report)==order,'Different root-choice scopes.'
        for key in keys:assert report[key]==first[key],f'Different {key}: {path}'
        for key in ('low_budget_cover_sha256_lf','residual_gram_profiles_sha256_lf'):
            assert report['options'][key]==first['options'][key],f'Different transported frontier: {path}'
        for branch in report['matching_branches']:
            mi=branch['matching_index'];assert mi in required
            attempts.append({'matching_index':mi,'status':branch['status'],
                             'cpu_seconds':branch['cpu_seconds'],'source':str(path)})
            if branch['status']=='INFEASIBLE':closed.setdefault(mi,str(path))
    orbit_cover=None;relabelled=[]
    if residual_mate_flips:
        from root_component_complete_star import mate_flip_orbits
        root=first['complete_matching_root'];assert root is not None
        norm=first['model']['component_tables']['first_component_normalization']
        assert norm and 'root_stabilizer' not in norm
        assert norm['action']=='Global independent mate flips only; no graph automorphism assumed.'
        for report in reports:
            assert report['model']['component_tables']['first_component_normalization']==norm
            assert not report['model']['independent_matching_normalization']
            assert not report['model']['grid_matching_mate_normalization']
        # Keep every letter of the normalised component fixed. The remaining
        # mate flips preserve its complete code, not merely its orbit. They
        # also leave every rectangle Gram entry unchanged. The selected star
        # root pair stays fixed so M0 is not exchanged with the free M1.
        protected={norm['root_line'],*norm['part'],root}
        orbit_cover=mate_flip_orbits(root,first['complete_star_matching_cover'],
                                    sorted(set(range(7))-protected))
        orbit_cover['pointwise_fixed_normalized_component_lines']=sorted(protected)
        original=dict(closed)
        for orbit in orbit_cover['orbits']:
            witnesses=sorted(set(orbit['members']) & set(original))
            if not witnesses:continue
            source=witnesses[0]
            for target in orbit['members']:
                if target in closed:continue
                mask=(orbit['flip_mask_by_member'][str(source)] ^
                      orbit['flip_mask_by_member'][str(target)])
                closed[target]=original[source]
                relabelled.append({'matching_index':target,'source_matching_index':source,
                                   'source':original[source],'flip_mask':mask})
    return {'scope':__doc__,'template_index':first['template_index'],
            'root_order':next(iter(order),None),
            'usable_in_arbitrary_low_budget_root_frontier':not order,
            'complete_matching_root':first['complete_matching_root'],
            'gram_cover':first['gram_cover'],'gram_cover_sha256_lf':first['gram_cover_sha256_lf'],
            'gram_cover_equivalence':equivalence,
            'matching_cover':first['matching_cover'],'excluded_matching_sources':closed,
            'residual_mate_flip_cover':orbit_cover,'relabelled_exclusions':relabelled,
            'open_matching_indices':sorted(required-set(closed)),
            'template_excluded':set(closed)==required,'attempts':attempts,
            'attempt_status_counts':dict(Counter(r['status'] for r in attempts)),
            'report_sources':[{'path':str(p),'sha256_lf':hashlib.sha256(t.replace('\r\n','\n').encode()).hexdigest()}
                              for p,t in zip(paths,texts)],
            'portable_unsat_proof':False,'global_conway_exclusion':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reports',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--residual-mate-flips',action='store_true',
                   help='Use only mate flips fixing the already normalised component pointwise.')
    p.add_argument('--same-base-gram-cover',type=Path,
                   help='Require exact equality with every field of this base cover, allowing only added corner tables.')
    a=p.parse_args()
    if a.output.exists():raise FileExistsError(a.output)
    result=merge(a.reports,a.residual_mate_flips,a.same_base_gram_cover);atomic_json_write(a.output,result)
    print(json.dumps({k:result[k] for k in ('template_index','root_order','open_matching_indices','template_excluded')}))


if __name__=='__main__':main()
