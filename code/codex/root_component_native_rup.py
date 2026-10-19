"""Check an own generated RUP proof with the repository's native checker.

The '-U' flag forbids RAT additions; '-p' ignores deletion information,
matching the existing Python RUP checker. Verification must explicitly
finish with 's VERIFIED'. The checked input is retained as compressed
DIMACS/proof artifacts, and the checker executable is hashed.
"""

import gzip
import hashlib
import os
from pathlib import Path
import subprocess
import time


CHECKER=Path(__file__).resolve().parents[2]/'tools/win64/drat-trim.exe'


def check_native_rup(clauses,proof,prefix,timeout=600):
    prefix=Path(prefix);cnf=prefix.with_suffix('.native.cnf');rup=prefix.with_suffix('.native.input.rup')
    trimmed=prefix.with_suffix('.native.trimmed.rup');log=prefix.with_suffix('.native.log')
    assert CHECKER.exists()
    variables=max((abs(v) for c in clauses for v in c),default=0)
    with cnf.open('w',encoding='ascii',newline='\n') as f:
        f.write('p cnf %d %d\n'%(variables,len(clauses)))
        for c in clauses:f.write(' '.join(map(str,c))+' 0\n')
    count=0
    with rup.open('w',encoding='ascii',newline='\n') as f:
        for line in proof:
            if not line.strip() or line.startswith('d '):continue
            f.write(line.rstrip()+'\n');count+=1
    command=[str(CHECKER),str(cnf),str(rup),'-U','-p','-l',str(trimmed),'-t',str(timeout)]
    started=time.monotonic()
    with log.open('wb') as f:
        result=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,timeout=timeout+10,
                              creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
    contents=log.read_text(encoding='utf-8',errors='replace')
    assert result.returncode==0 and 's VERIFIED' in contents.splitlines(), ('RUP verification failed',result.returncode,str(log))
    paths={}
    for path in (cnf,rup,trimmed):
        if not path.exists():continue
        target=path.with_suffix(path.suffix+'.gz');h=hashlib.sha256()
        with path.open('rb') as source,target.open('wb') as raw:
            with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as zipped:
                for chunk in iter(lambda:source.read(1024*1024),b''):
                    h.update(chunk);zipped.write(chunk)
        paths[target.name]={'uncompressed_sha256':h.hexdigest(),'compressed_bytes':target.stat().st_size}
        # These are our own temporary ASCII copies; the compressed data remain.
        path.unlink()
    return {'empty_clause_verified':True,'checker':'drat-trim -U -p','rup_only':True,
            'input_additions':count,'checker_sha256':hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
            'wall_seconds':time.monotonic()-started,'log':str(log),'artifacts':paths}
