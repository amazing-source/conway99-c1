"""Add direct local E3 contradictions to a recorded component-code cover.

The source report is preserved. A Gram closes only if every code in its
complete listed cover has a proof, either from the source or from E3.
Missing codes are kept UNKNOWN unless an explicit E3 rectangle refutes them.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_e3_colours import obstruction,matching_maps
from root_component_resources import atomic_json_write,limit_research_process


def augment(data,tables,source):
    library={r['vertices']:r for r in tables['records']}
    maps={n:matching_maps(record) for n,record in library.items()}
    added=0
    for record in data['records']:
        for case in record['cases']:
            if case.get('base_model_only'):continue
            if not case.get('component_codes'):continue
            codes=case['component_codes'];size=6*len(case['component_part'])
            assert len({tuple(code) for code in codes})==len(codes)
            previous={r['component_index']:r for r in case['branches']}
            assert len(previous)==len(case['branches'])
            assert all(0<=i<len(codes) for i in previous)
            branches=[];processed={i for i,r in previous.items() if not r.get('not_processed')}
            for ci,code in enumerate(codes):
                prior=previous.get(ci)
                if prior is not None:assert prior['code']==code
                witness=obstruction(library[size],code,maps[size])
                if prior is not None and prior['status']=='INFEASIBLE':
                    branches.append(dict(prior,source_report=source));continue
                if witness is not None:
                    branches.append({'component_index':ci,'code':code,'status':'INFEASIBLE',
                        'method':'LOCAL_E3_RECTANGLE','local_vertices':size,'witness':witness})
                    processed.add(ci);added+=1
                elif prior is not None:branches.append(dict(prior,source_report=source))
                else:branches.append({'component_index':ci,'code':code,'status':'UNKNOWN','not_processed':True})
            case['branches']=branches
            case['component_branch_counts']=dict(Counter(r['status'] for r in branches))
            case['all_component_branches_processed']=len(processed)==len(codes)
            case['status']='INFEASIBLE' if all(r['status']=='INFEASIBLE' for r in branches) else 'UNKNOWN'
            case['added_local_E3_proofs']=sum(r.get('method')=='LOCAL_E3_RECTANGLE' for r in branches)
            case['proof_augmentation_source']=source
        record['counts']=dict(Counter(c['status'] for c in record['cases']))
        record['all_source_grams_processed']=len(record['cases'])==record['complete_source_gram_count']
        record['excluded']=record['all_source_grams_processed'] and all(c['status']=='INFEASIBLE' for c in record['cases'])
    return added


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report',type=Path);parser.add_argument('--tables',type=Path,required=True)
    parser.add_argument('--glob',help='Read matching reports from the report directory; retain only cases with newly added proofs.')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();limit_research_process(1)
    assert args.output.resolve()!=args.report.resolve()
    table_raw=args.tables.read_bytes()
    tables=json.loads(table_raw)
    if args.glob:
        sources=[];records=[];added=0;new_grams=Counter();branch_counts=Counter();input_counts=Counter()
        for path in sorted(args.report.glob(args.glob)):
            assert path.resolve()!=args.output.resolve()
            raw=path.read_bytes();data=json.loads(raw)
            prior={(r['template_index'],c['gram_index']):c['status'] for r in data['records'] for c in r['cases']}
            count=augment(data,tables,path.as_posix());added+=count
            sources.append({'path':path.as_posix(),'sha256_lf':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),
                            'new_local_proofs':count})
            for r in data['records']:
                ti=r['template_index'];kept=[]
                for c in r['cases']:
                    input_counts[(ti,prior[ti,c['gram_index']])]+=1
                    if c.get('added_local_E3_proofs',0):
                        kept.append(c)
                        branch_counts.update((ti,b['status']) for b in c['branches'])
                        if c['status']=='INFEASIBLE' and prior[ti,c['gram_index']]!='INFEASIBLE':new_grams[ti]+=1
                if kept:
                    item=dict(r,cases=kept)
                    item['counts']=dict(Counter(c['status'] for c in kept))
                    item['all_source_grams_processed']=len(kept)==item['complete_source_gram_count']
                    item['excluded']=item['all_source_grams_processed'] and all(c['status']=='INFEASIBLE' for c in kept)
                    records.append(item)
        result={'scope':__doc__,'records':records,'local_E3_augmentation':{'scope':__doc__,'sources':sources,
            'tables':args.tables.as_posix(),'tables_sha256_lf':hashlib.sha256(table_raw.replace(b'\r\n',b'\n')).hexdigest(),
            'new_proofs':added,'newly_excluded_grams':dict(new_grams)}}
        atomic_json_write(args.output,result)
        print(json.dumps({'source_reports':len(sources),'new_local_proofs':added,'newly_excluded_grams':dict(new_grams),
            'augmented_cases':sum(len(r['cases']) for r in records),
            'input_counts':{str(k):v for k,v in input_counts.items()},
            'augmented_branch_counts':{str(k):v for k,v in branch_counts.items()}}))
        return
    raw=args.report.read_bytes();data=json.loads(raw)
    added=augment(data,tables,args.report.as_posix())
    data['local_E3_augmentation']={'scope':__doc__,'source':args.report.as_posix(),
        'source_sha256_lf':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),
        'tables':args.tables.as_posix(),'tables_sha256_lf':hashlib.sha256(table_raw.replace(b'\r\n',b'\n')).hexdigest(),
        'new_proofs':added}
    atomic_json_write(args.output,data)
    print(json.dumps({'new_local_proofs':added,'cases':[{'template':r['template_index'],
        'gram':c['gram_index'],'status':c['status'],'counts':c.get('component_branch_counts')}
        for r in data['records'] for c in r['cases']]}))


if __name__=='__main__':main()
