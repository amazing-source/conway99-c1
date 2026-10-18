"""Union pointwise branch proofs only within identical canonical code covers.

Missing branches remain UNKNOWN. One complete cover is excluded only when
every listed code has an INFEASIBLE proof. Different covers, frames or Gram
anchors are never spliced into an apparently complete cover.
"""
import argparse
from collections import Counter,defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def merge_reports(sources):
    groups={};provenance=[];catalogues=set();table_cache={};catalogue_cache={}
    for path,data,sha in sources:
        provenance.append({'path':path,'sha256_lf':sha})
        if data.get('options',{}).get('local_tables'):catalogues.add(data['options']['local_tables'])
        for record in data.get('records',[]):
            for case in record.get('cases',[]):
                codes=case.get('component_codes')
                if not codes:continue
                assert len({tuple(c) for c in codes})==len(codes)
                catalogue='UNRESTRICTED_BASE_MODEL'
                if not case.get('base_model_only'):
                    table_path=data.get('options',{}).get('local_tables') or data.get('local_E3_augmentation',{}).get('tables')
                    assert table_path, 'Matching catalogue is required to interpret code indices.'
                    size=6*len(case['component_part']);catalogue_key=(table_path,size)
                    if catalogue_key not in catalogue_cache:
                        if table_path not in table_cache:table_cache[table_path]=json.loads(Path(table_path).read_text())
                        table=next(r for r in table_cache[table_path]['records'] if r['vertices']==size)
                        content=[table['cross_permutations'],table['internal_matchings']]
                        catalogue_cache[catalogue_key]=hashlib.sha256(json.dumps(content,separators=(',',':')).encode()).hexdigest()
                    catalogue=catalogue_cache[catalogue_key]
                identity=[record['template_index'],case['gram_index'],case['gram_anchor_values'],
                          case['component_root'],case['component_part'],catalogue,codes]
                key=json.dumps(identity,separators=(',',':'))
                if key not in groups:
                    groups[key]={'record':deepcopy(record),'case':deepcopy(case),'branches':{},'sources':set()}
                group=groups[key]
                assert group['record']['complete_source_gram_count']==record['complete_source_gram_count']
                group['sources'].add(path)
                local=set()
                for branch in case['branches']:
                    i=branch['component_index'];assert i not in local;local.add(i)
                    assert 0<=i<len(codes) and branch['code']==codes[i]
                    old=group['branches'].get(i)
                    if old is None or branch['status']=='INFEASIBLE' and old['status']!='INFEASIBLE' or old['status']!='INFEASIBLE' and old.get('not_processed') and not branch.get('not_processed'):
                        group['branches'][i]=dict(branch,union_source=path)
    records={};closed=[]
    for key,group in sorted(groups.items()):
        case=group['case'];codes=case['component_codes'];proofs=group['branches']
        case['branches']=[proofs.get(i,{'component_index':i,'code':code,'status':'UNKNOWN','not_processed':True})
                          for i,code in enumerate(codes)]
        case['component_branch_counts']=dict(Counter(b['status'] for b in case['branches']))
        case['all_component_branches_processed']=all(not b.get('not_processed') for b in case['branches'])
        case['status']='INFEASIBLE' if all(b['status']=='INFEASIBLE' for b in case['branches']) else 'UNKNOWN'
        case['branch_union_sources']=sorted(group['sources'])
        case['code_cover_sha256']=hashlib.sha256(key.encode()).hexdigest()
        ti=group['record']['template_index']
        record=records.setdefault(ti,{'template_index':ti,'complete_source_gram_count':group['record']['complete_source_gram_count'],'cases':[]})
        assert record['complete_source_gram_count']==group['record']['complete_source_gram_count']
        record['cases'].append(case)
        if case['status']=='INFEASIBLE':closed.append([ti,case['gram_index']])
    result={'scope':__doc__,'records':list(records.values()),'sources':provenance,'closed_grams':closed}
    if len(catalogues)==1:result['options']={'local_tables':next(iter(catalogues))}
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path);parser.add_argument('--glob',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();limit_research_process(1)
    def sources():
        for path in sorted(args.directory.glob(args.glob)):
            assert path.resolve()!=args.output.resolve()
            raw=path.read_bytes()
            yield path.as_posix(),json.loads(raw),hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()
    result=merge_reports(sources());atomic_json_write(args.output,result)
    print(json.dumps({'source_files':len(result['sources']),'covers':sum(len(r['cases']) for r in result['records']),
                      'closed_grams':result['closed_grams']}))


if __name__=='__main__':main()
