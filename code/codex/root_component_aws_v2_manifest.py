"""Prepare bounded code ranges for the remaining cover; launch no resources.

The all-colour E3 filter is invariant under the same mate flips, colour
swap and Gram stabilizer as the old cover. Removing its invalid orbits
therefore filters, rather than renumbers within, the canonical code list.
Each task nevertheless checks a hash of the entire newly computed cover.
Known proofs are retained in compact seeds. A range is NEVER a Gram proof
on its own; complete pointwise unions are required after the tasks finish.
"""
import argparse
import ast
from collections import Counter
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shlex
import subprocess
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write,limit_research_process


def digest_bytes(raw):return hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()
def code_hash(codes):return hashlib.sha256(json.dumps(codes,separators=(',',':')).encode()).hexdigest()


def prepare(filtered,table_path,frontier,prefix,extra_paths,chunk_size,seconds,prefilter_seconds):
    directory=filtered.parent;repo=Path(__file__).resolve().parents[2]
    cover=json.loads(filtered.read_text());tables=json.loads(table_path.read_text())
    old_tables_path=directory/'line_component_pattern_tables_rotated.json'
    old_tables=json.loads(old_tables_path.read_text())
    valid={r['vertices']:{tuple(c) for c in r['component_code_triples']} for r in tables['records']}
    for before,after in zip(old_tables['records'],tables['records']):
        assert before['vertices']==after['vertices']
        assert before['cross_permutations']==after['cross_permutations']
        assert before['internal_matchings']==after['internal_matchings']
    extra={};input_hashes={p.as_posix():digest_bytes(p.read_bytes()) for p in [filtered,table_path,old_tables_path,frontier,
        directory/'root_component_templates.json',directory/'root_component_gram_orbits20.json']}
    for path in extra_paths:
        raw=path.read_bytes();data=json.loads(raw)
        assert data['options']['stabilizer_normalize']
        assert Path(data['options']['local_tables']).name in (table_path.name,old_tables_path.name)
        sha=digest_bytes(raw);input_hashes[path.as_posix()]=sha
        for record in data['records']:
            for case in record['cases']:extra.setdefault((record['template_index'],case['gram_index']),[]).append((path,sha,case))
    seeds=prefix.parent/(prefix.name+'_seeds');seeds.mkdir(parents=True,exist_ok=True)
    tasks=[];stats=Counter();sample_covers={};newly_closed=[]
    for record in cover['records']:
        ti=record['template_index']
        if ti not in (7,9,19):continue
        assert record['exhaustive'] and record['usable_as_gram_cover']
        for gi,values in zip(record['source_gram_indices'],record['gram_anchor_values']):
            source=directory/f'root_component_signature_aws_v1_{ti}_{gi}_branches.json'
            raw=source.read_bytes();data=json.loads(raw);source_sha=digest_bytes(raw)
            assert data['options']['stabilizer_normalize']
            assert Path(data['options']['local_tables']).name==old_tables_path.name
            case=data['records'][0]['cases'][0]
            assert data['records'][0]['template_index']==ti and case['gram_index']==gi and case['gram_anchor_values']==values
            assert not case.get('base_model_only')
            codes=[c for c in case['component_codes'] if tuple(c) in valid[6*len(case['component_part'])]]
            assert codes and len({tuple(c) for c in codes})==len(codes)
            positions={tuple(c):i for i,c in enumerate(codes)};proofs={};sources={source.as_posix():source_sha}
            for path,sha,other in [(source,source_sha,case)]+extra.get((ti,gi),[]):
                assert other['gram_anchor_values']==values
                assert other['component_root']==case['component_root'] and other['component_part']==case['component_part']
                sources[path.as_posix()]=sha
                for b in other['branches']:
                    if b['status']!='INFEASIBLE' or tuple(b['code']) not in positions:continue
                    assert other['component_codes'][b['component_index']]==b['code']
                    i=positions[tuple(b['code'])]
                    proofs[i]={'component_index':i,'code':b['code'],'status':'INFEASIBLE',
                               'source_report':path.as_posix(),'source_sha256_lf':sha,
                               'source_component_index':b['component_index'],'cpu_seconds':b.get('cpu_seconds',0)}
            missing=[i for i in range(len(codes)) if i not in proofs]
            seed_path=seeds/f't{ti}_g{gi}.json'
            seed_case={k:case[k] for k in ('gram_index','gram_anchor_values','component_root','component_part')}
            seed_case.update(component_codes=codes,branches=[proofs[i] for i in sorted(proofs)],
                status='UNKNOWN' if missing else 'INFEASIBLE',base_model_only=False,
                all_component_branches_processed=not missing,
                component_branch_counts={'INFEASIBLE':len(proofs)},
                ordered_component_code_cover_sha256=code_hash(codes))
            seed={'scope':__doc__,'options':{'local_tables':table_path.as_posix(),'stabilizer_normalize':True},
                  'records':[{'template_index':ti,'complete_source_gram_count':data['records'][0]['complete_source_gram_count'],'cases':[seed_case]}],
                  'canonical_cover_source':source.as_posix(),'proof_source_sha256_lf':sources,
                  'equivariant_filter':'All-colour E3; runtime rechecks the complete canonical code-cover hash.'}
            atomic_json_write(seed_path,seed)
            input_hashes[seed_path.as_posix()]=digest_bytes(seed_path.read_bytes())
            stats[f'{ti}_grams']+=1;stats[f'{ti}_code_cover']+=len(codes)
            stats[f'{ti}_reused_proofs']+=len(proofs);stats[f'{ti}_unproved_codes']+=len(missing)
            if not missing:newly_closed.append([ti,gi])
            for offset in range(0,len(missing),chunk_size):
                indices=missing[offset:offset+chunk_size];lo,hi=indices[0],indices[-1]+1
                output=directory/f'root_component_signature_aws_v2_{ti}_{gi}_r{lo}_{hi}.json'
                argv=['python','-I','-u','-X','utf8','code/codex/root_component_local_branch.py',directory.as_posix(),
                      '--index',str(ti),'--gram-index',str(gi),'--seconds',str(seconds),
                      '--component-range',str(lo),str(hi),'--expected-code-cover',code_hash(codes),
                      '--prefilter-seconds',str(prefilter_seconds),
                      '--minc-lines','2','--minc-balance','--line-profiles','2','--layer','2',
                      '--local-tables',table_path.as_posix(),'--upper-projector','--rotated-boundary',
                      '--stabilizer-normalize','--short-norm','8','--rotated-rectangles','30',
                      '--rotated-signatures','--rotated-templates','--rotated-residuals',
                      '--fixed-cross-triangles','6','--fixed-star-triangles','2',
                      '--low-budget-cover',frontier.as_posix(),'--reuse-proven',seed_path.as_posix(),
                      '--output',output.as_posix()]
                tasks.append({'task_id':f't{ti}_g{gi}_r{lo}_{hi}','template_index':ti,'gram_index':gi,
                              'range':[lo,hi],'new_code_indices':indices,'new_code_count':len(indices),
                              'full_code_count':len(codes),'full_code_cover_sha256':code_hash(codes),
                              'argv':argv,'command':shlex.join(argv),'output':output.as_posix(),
                              'log':output.with_suffix('.log').as_posix(),'workers':1,
                              'nominal_cpu_seconds_per_code':seconds,'external_wall_timeout_seconds':7200})
            sample_covers[ti,gi]=codes
    tasks.sort(key=lambda r:((9,19,7).index(r['template_index']),r['gram_index'],r['range'][0]))
    assert len({r['task_id'] for r in tasks})==len(tasks)
    assert sum(t['new_code_count'] for t in tasks)==sum(v for k,v in stats.items() if k.endswith('_unproved_codes'))
    dependencies=set();pending=[repo/'code/codex/root_component_local_branch.py']
    while pending:
        path=pending.pop()
        if path in dependencies:continue
        dependencies.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8-sig'))):
            modules=([node.module] if isinstance(node,ast.ImportFrom) and node.module else
                     [a.name for a in node.names] if isinstance(node,ast.Import) else [])
            for module in modules:
                candidate=path.parent/(module.split('.')[0]+'.py')
                if candidate.exists() and candidate not in dependencies:pending.append(candidate)
    names=[p.relative_to(repo).as_posix() for p in sorted(dependencies)]
    assert subprocess.call(['git','diff','--quiet','HEAD','--',*names],cwd=repo)==0,'Commit the runtime before freezing a manifest.'
    tracked=set(subprocess.check_output(['git','ls-files','--',*names],cwd=repo,text=True).splitlines())
    assert set(names)<=tracked
    metadata={'scope':__doc__,'task_count':len(tasks),'stats':dict(stats),'newly_closed_by_union':newly_closed,
              'code_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
              'code_sha256_lf':{p.relative_to(repo).as_posix():digest_bytes(p.read_bytes()) for p in sorted(dependencies)},
              'input_sha256_lf':input_hashes,'cpu_seconds_per_code':seconds,'chunk_size':chunk_size,
              'nominal_solver_cpu_seconds':sum(t['new_code_count'] for t in tasks)*seconds,
              'hard_cpu_bound_proved':False,'completion_time_bound_proved':False,
              'no_inner_total_budget':'Each new code in the range receives its own nominal budget; external watchdog remains necessary.',
              'exclusion_rule':'Merge only identical complete covers. Every code must be INFEASIBLE; missing or UNKNOWN stays open.',
              'cpu_binding':'One process per assigned CPU with taskset; do not copy local cpu_guard files.',
              'tested_packages':{n:importlib.metadata.version(n) for n in ('ortools','sympy','numpy')}}
    prefix.parent.mkdir(parents=True,exist_ok=True)
    prefix.with_suffix('.jsonl').write_text(''.join(json.dumps(t,separators=(',',':'))+'\n' for t in tasks),encoding='utf-8')
    prefix.with_suffix('.tsv').write_text(''.join('\t'.join([t['task_id'],'7200',t['command']+' > '+shlex.quote(t['log'])+' 2>&1',t['output']+','+t['log']])+'\n' for t in tasks),encoding='utf-8')
    atomic_json_write(prefix.with_suffix('.metadata.json'),metadata,indent=2)
    return metadata,sample_covers


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('filtered',type=Path);p.add_argument('--tables',type=Path,required=True)
    p.add_argument('--frontier',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True)
    p.add_argument('--extra-report',type=Path,nargs='*',default=[])
    p.add_argument('--chunk-size',type=int,default=8);p.add_argument('--seconds',type=float,default=180)
    p.add_argument('--prefilter-seconds',type=float,default=5)
    args=p.parse_args();assert args.chunk_size>0 and args.seconds>0
    limit_research_process(1)
    meta,_=prepare(args.filtered,args.tables,args.frontier,args.prefix,args.extra_report,args.chunk_size,args.seconds,args.prefilter_seconds)
    print(json.dumps({k:meta[k] for k in ('task_count','stats','code_commit','nominal_solver_cpu_seconds','newly_closed_by_union')}))


if __name__=='__main__':main()
