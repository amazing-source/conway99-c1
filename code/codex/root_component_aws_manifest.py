"""Prepare independent tasks for the remaining Gram cover; launch nothing.

The bounded tasks can close Gram branches, but do not guarantee that all
will close. Incomplete code covers and every UNKNOWN stay open.
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


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('filtered',type=Path)
    p.add_argument('--prefix',type=Path,required=True)
    p.add_argument('--seconds',type=float,default=120)
    p.add_argument('--total-cpu-seconds',type=float,default=900)
    args=p.parse_args()
    repo=Path(__file__).resolve().parents[2]
    directory=args.filtered.parent
    data=json.loads(args.filtered.read_text())
    original=directory/'root_component_gram_orbits20.json'
    covers={r['template_index']:r for r in json.loads(original.read_text())['records']}
    tasks=[]
    for record in data['records']:
        index=record['template_index']
        if index not in (7,9,19):continue
        assert record['exhaustive'] and record['usable_as_gram_cover']
        ids=record['source_gram_indices']
        assert len(ids)==len(record['gram_anchor_values'])==record['gram_count']
        for gi,values in zip(ids,record['gram_anchor_values']):
            assert values==covers[index]['gram_anchor_values'][gi]
            output=directory/f'root_component_signature_aws_v1_{index}_{gi}_branches.json'
            argv=['python','-I','-u','-X','utf8','code/codex/root_component_local_branch.py',
                  directory.as_posix(),'--index',str(index),'--gram-index',str(gi),
                  '--seconds',str(args.seconds),'--total-cpu-seconds',str(args.total_cpu_seconds),
                  '--minc-lines','2','--minc-balance','--line-profiles','2','--layer','2',
                  '--local-tables',(directory/'line_component_pattern_tables_rotated.json').as_posix(),
                  '--upper-projector','--rotated-boundary','--stabilizer-normalize',
                  '--short-norm','8','--rotated-rectangles','6','--output',output.as_posix()]
            tasks.append({'task_id':f't{index}_g{gi}','template_index':index,'gram_index':gi,
                'gram_anchor_values':values,'argv':argv,'command':shlex.join(argv),
                'cwd':'repository root','output':output.as_posix(),
                'log':output.with_suffix('.log').as_posix(),
                'workers':1,'cpu_seconds_per_component':args.seconds,
                'solver_cpu_seconds_per_invocation':args.total_cpu_seconds,
                'model_construction_excluded_from_cpu_budget':True})
    assert len({t['task_id'] for t in tasks})==len(tasks)
    assert len({t['output'] for t in tasks})==len(tasks)
    # Try the small type9 cover first; each task is otherwise independent.
    tasks.sort(key=lambda t:((9,7,19).index(t['template_index']),t['gram_index']))
    inputs=[args.filtered,original,directory/'root_component_templates.json',
            directory/'line_component_pattern_tables_rotated.json']
    requirements={name:importlib.metadata.version(name) for name in ('ortools','sympy','numpy')}
    code_dir=repo/'code/codex'
    dependencies=set();pending=[code_dir/'root_component_local_branch.py']
    while pending:
        path=pending.pop()
        if path in dependencies:continue
        dependencies.add(path)
        tree=ast.parse(path.read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            modules=([node.module] if isinstance(node,ast.ImportFrom) and node.module else
                     [alias.name for alias in node.names] if isinstance(node,ast.Import) else [])
            for module in modules:
                candidate=code_dir/(module.split('.')[0]+'.py')
                if candidate.exists() and candidate not in dependencies:pending.append(candidate)
    dependency_names=[p.relative_to(repo).as_posix() for p in sorted(dependencies)]
    assert subprocess.call(['git','diff','--quiet','HEAD','--',*dependency_names],cwd=repo)==0
    tracked=set(subprocess.check_output(['git','ls-files','--',*dependency_names],cwd=repo,text=True).splitlines())
    assert set(dependency_names)<=tracked, 'Every runtime source must be in the pinned commit.'
    meta={'scope':__doc__,'task_count':len(tasks),'counts':dict(Counter(t['template_index'] for t in tasks)),
          'code_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),
          'tested_python':sys.version,'tested_packages':requirements,
          'input_sha256':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
          'code_sha256':{p.relative_to(repo).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(dependencies)},
          'solver_cpu_budget_sum_seconds':len(tasks)*args.total_cpu_seconds,
          'completion_time_bound_proved':False,
          'exclusion_rule':'Only case.status=INFEASIBLE with all canonical component branches processed and all branch statuses INFEASIBLE closes a Gram. UNKNOWN, missing or malformed outputs remain open. An unrestricted base-model INFEASIBLE is also valid.',
          'linux_cpu_binding':'Bind each concurrent task to a different allowed CPU with taskset -c CPU. The existing affinity limiter preserves that singleton; without taskset many tasks would share the first four CPUs.',
          'local_runtime_files':'Do not copy cpu_guard.budget.json, cpu_guard.stop, or guard logs to AWS.',
          'merge_commands':[
              'python -I code/codex/root_component_campaign.py '+directory.as_posix()+' --refresh-only',
              'python -I code/codex/root_component_filtered_cover.py '+directory.as_posix()+' --output '+(directory/'root_component_gram_filtered_after_aws_v1.json').as_posix()],
          'retry_rule':'Use a NEW output filename and --reuse-proven OLD_FILE. This carries only proved INFEASIBLE component codes; UNKNOWN codes are tried again. Do not overwrite the first report.'}
    args.prefix.parent.mkdir(parents=True,exist_ok=True)
    args.prefix.with_suffix('.jsonl').write_text(''.join(json.dumps(t,separators=(',',':'))+'\n' for t in tasks),encoding='utf-8')
    args.prefix.with_suffix('.metadata.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    args.prefix.with_suffix('.requirements.txt').write_text(''.join(f'{k}=={v}\n' for k,v in requirements.items()),encoding='utf-8')
    print(json.dumps({k:meta[k] for k in ('task_count','counts','code_commit','solver_cpu_budget_sum_seconds')}))


if __name__=='__main__':main()
