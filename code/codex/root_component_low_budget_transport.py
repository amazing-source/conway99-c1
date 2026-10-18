"""Transport a FROZEN earlier exclusion frontier to other complete stars.

At any new root with prism sum <=51, the earlier necessary root cover and
its exclusions apply. Above51 the new root retains all200 pre-budget
templates. No new-root budget or symmetry is assumed. The frozen snapshot
must precede these new computations, preventing circular use of results.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def digest(path):
    return hashlib.sha256(Path(path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def freeze(directory,output):
    directory=Path(directory)
    assert not output.exists(), 'A proof frontier snapshot is immutable.'
    cover_path=directory/'root_component_cover79.json'
    all_path=directory/'root_component_templates.json'
    cover=json.loads(cover_path.read_text());templates=json.loads(all_path.read_text())['survivors']
    assert len(templates)==200 and cover['template_count']==79
    assert all(r['exclusion_status'] in ('EXCLUDED','OPEN') for r in cover['templates'])
    allowed=sorted(r['template_index'] for r in cover['templates'] if r['exclusion_status']=='OPEN')
    assert allowed==sorted(cover['open_template_indices'])
    sources={cover_path.name: digest(cover_path),all_path.name:digest(all_path)}
    excluded=[]
    for r in cover['templates']:
        if r['exclusion_status']!='EXCLUDED':continue
        excluded.append(r['template_index'])
        paths=r['exclusion_source']
        if isinstance(paths,str):paths=[paths]
        for name in paths:
            path=directory/name
            data=json.loads(path.read_text())
            assert not data.get('options',{}).get('low_budget_cover'), 'Do not create a circular frontier.'
            sources[name]=digest(path)
    for name in ('root_component_gram_budget51.json','root_component_gram_realization.json'):
        sources[name]=digest(directory/name)
    result={'scope':__doc__,'source_scope':cover['scope'],
            'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            'all_template_count':200,'budget':51,
            'budget_cover_template_indices':sorted(r['template_index'] for r in cover['templates']),
            'excluded_template_indices':sorted(excluded),'allowed_template_indices':allowed,
            'allowed_nongrid_masks':sorted({templates[i]['graph_mask'] for i in allowed}),
            'source_sha256_lf':sources,'portable_unsat_proof':False}
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


def add_conditional_cover(model,root,items,nongrid,low_rows,snapshot):
    assert len(items)==15 and len(items[0]['old_root_rectangles'])==6
    assert snapshot['budget']==51
    old_cost=sum(row['shared_label_edges'] for row in items[0]['old_root_rectangles'])
    cost=old_cost+sum(item['edges'][i] for item in items for i in (0,1,4,5))
    low=model.new_bool_var(f'rotated_root_low_budget_{root}')
    model.add(cost<=51).only_enforce_if(low)
    model.add(cost>=52).only_enforce_if(low.Not())
    if low_rows:model.add_allowed_assignments(nongrid,low_rows).only_enforce_if(low)
    else:model.add(low==0)
    return {'old_line_prism_contribution':old_cost,'budget_threshold':51,
            'unconditional_new_root_budget':None,'allowed_low_budget_nongrid_rows':len(low_rows),
            'frozen_survivors':snapshot['allowed_template_indices'],
            'frozen_source_commit':snapshot['source_commit']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('--freeze',type=Path,required=True)
    args=p.parse_args();result=freeze(args.directory,args.freeze)
    print(json.dumps({'frozen_survivors':result['allowed_template_indices'],
                     'earlier_excluded_templates':len(result['excluded_template_indices']),
                     'source_files':len(result['source_sha256_lf'])}))


if __name__=='__main__':main()
