"""Run one-core continuation searches on explicit residual attachments.

The input is a materialized residual catalogue, not an inferred complete
family cover. Statuses are per attachment. The wrapper's CPU interrupt
limits search; a separate wall-time limit bounds proof processing too.
"""

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import limit_research_process,atomic_json_write


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def run(directory,indices,cpu_seconds,wall_seconds):
    resources=limit_research_process(1)
    data=json.loads((directory/'cases.json').read_text(encoding='utf-8'))
    family=data.get('family','2K2')
    assert family in ('2K2','2K2N')
    source=directory/'lab_source.py'
    raw=gzip.decompress((directory/'lab_source.py.gz').read_bytes())
    if source.exists():assert source.read_bytes()==raw
    else:source.write_bytes(raw)
    assert hashlib.sha256(raw).hexdigest()==data['source_sha256']
    report={'scope':'Per-attachment continuation only; completeness comes from the separate LAB census.',
            'resources':resources,'cpu_search_limit_per_case':cpu_seconds,
            'wall_limit_per_case_including_proof':wall_seconds,'cases':[]}
    report_path=directory/'continuation_batch.json'
    assert not report_path.exists(),'Use a new directory or an explicit continuation of the recorded batch.'
    wrapper=Path(__file__).with_name('root_component_lab_profile_export.py')
    for index in indices:
        case=data['cases'][index];prefix=directory/('case%03d.json'%index)
        assert not prefix.with_suffix('.lab_result.json.gz').exists()
        cover=directory/('core_%03d.json.gz'%case['core_index'])
        command=[sys.executable,'-I','-u','-X','utf8',str(wrapper),str(source),str(cover),
                 '--index',str(case['boundary_index']),'--family',family]
        for attachment in case['attachment']:
            command+=['--attachment',*map(str,attachment)]
        command+=['--sigma',*map(str,case['sigma']),'--row-cut-rounds','128',
                  '--row-cut-cpu-seconds',str(cpu_seconds),'--continuation-cuts','--output',str(prefix)]
        record={'case_index':index,'core_index':case['core_index'],'boundary_index':case['boundary_index'],
                'attachment':case['attachment'],'sigma':case['sigma'],'status':'RUNNING'}
        report['cases'].append(record);atomic_json_write(report_path,report)
        print(json.dumps({'start':record}),flush=True)
        started=time.monotonic();timed_out=False
        with prefix.with_suffix('.log').open('wb') as log:
            process=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,
                                     creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            record['pid']=process.pid;atomic_json_write(report_path,report)
            while process.poll() is None:
                if time.monotonic()-started>=wall_seconds:
                    timed_out=True
                    # A Windows venv python.exe can be a launcher with a real
                    # interpreter child. Terminate this OWN process tree.
                    if os.name=='nt':
                        subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],
                                       stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                                       creationflags=subprocess.CREATE_NO_WINDOW,timeout=10)
                    else:process.terminate()
                    try:process.wait(timeout=10)
                    except subprocess.TimeoutExpired:process.kill();process.wait(timeout=10)
                    break
                time.sleep(.25)
        record['returncode']=process.returncode;record['wall_seconds']=time.monotonic()-started
        result_path=prefix.with_suffix('.lab_result.json.gz')
        learning_path=prefix.with_suffix('.row_cut_learning.json')
        if timed_out:record['status']='UNKNOWN_WALL_TIMEOUT'
        elif process.returncode!=0:record['status']='ERROR'
        elif result_path.exists():
            result=json.loads(gzip.decompress(result_path.read_bytes()))
            if 'attachments' not in result:
                record['status']='ERROR_NOT_A_TARGETED_ATTACHMENT_RESULT'
                record['detail']='The wrapper returned a whole-boundary driver result; no exclusion is counted.'
                atomic_json_write(report_path,report)
                print(json.dumps({'finished':record}),flush=True)
                continue
            assert result['attachments']==case['attachment'] and result['sigma']==case['sigma']
            assert result['boundary_hex']==case['boundary_hex']
            frontier=result['frontier'];status=frontier['status'];record['raw_status']=status
            if status=='EXCLUDED_PROFILE_SELECTION_UNSAT':
                assert frontier['proof_check']['empty_clause_verified'] is True
                learning=json.loads(learning_path.read_text(encoding='utf-8'))
                assert learning['terminal_status']=='UNSAT_WITH_NECESSARY_ROW_CUTS'
                assert learning['rounds'][-1]['answer'] is False
                record['status']='EXCLUDED_ATTACHMENT_WITH_CHECKED_RUP'
                record['proof_check']=frontier['proof_check']
                record['clauses_added']=learning['clauses_added']
                record['sat_selections_refuted']=sum(r['answer'] is True for r in learning['rounds'])
                record['solve_learning_cpu_seconds']=learning['rounds'][-1]['cpu_seconds']
                record['total_frontier_cpu_seconds']=frontier['cpu_seconds']
            elif status.startswith('EXCLUDED_'):record['status']=status
            elif status=='SAT_KNOWN_ROWS_COMPLETE':record['status']='OPEN_KNOWN_ROWS_SAT'
            else:record['status']='UNKNOWN'
            record['files']={p.name:digest(p) for p in directory.glob(prefix.stem+'.*') if p.suffix!='.log'}
        else:record['status']='ERROR_MISSING_RESULT'
        atomic_json_write(report_path,report)
        print(json.dumps({'finished':{k:v for k,v in record.items() if k!='files'}}),flush=True)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path);p.add_argument('--cases',nargs='+',type=int,required=True)
    p.add_argument('--cpu-seconds',type=float,default=120);p.add_argument('--wall-seconds',type=float,default=900)
    a=p.parse_args();run(a.directory,a.cases,a.cpu_seconds,a.wall_seconds)
