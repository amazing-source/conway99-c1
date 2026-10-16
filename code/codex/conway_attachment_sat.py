"""Complete a fixed new-star attachment pattern by exact SAT.

The old44 is free except its four-vertex part of the star4 matching.
This searches our newly built attachments, not a peer's fixed seed.
"""
import argparse
from hashlib import sha256
from itertools import combinations
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from pysat.card import CardEnc,EncType
from pysat.formula import IDPool,CNF

sys.path.insert(0,str(Path(__file__).resolve().parent))
from conway_attachment_probe import LABELS,OLD,NEW,STAR4

CADICAL=Path('C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe')


class Encoder:
    def __init__(self):
        self.pool=IDPool()
        self.cnf=CNF()
        self.products={}
    def var(self):
        return self.pool.id()
    @staticmethod
    def neg(x):
        return not x if isinstance(x,bool) else -x
    def conjunction(self,a,b):
        if isinstance(a,bool):
            return b if a else False
        if isinstance(b,bool):
            return a if b else False
        if a==b:
            return a
        key=tuple(sorted((a,b)))
        if key not in self.products:
            c=self.var()
            self.cnf.extend([[-c,a],[-c,b],[c,-a,-b]])
            self.products[key]=c
        return self.products[key]
    def at_most(self,terms,bound):
        bound-=sum(v is True for v in terms)
        literals=[v for v in terms if not isinstance(v,bool)]
        if bound<0:
            self.cnf.append([])
        elif bound==0:
            self.cnf.extend([[-v] for v in literals])
        elif bound<len(literals):
            self.cnf.extend(CardEnc.atmost(lits=literals,bound=bound,vpool=self.pool,encoding=EncType.seqcounter).clauses)
    def exactly(self,terms,target):
        self.at_most(terms,target)
        self.at_most([self.neg(v) for v in terms],len(terms)-target)


def build(adjacency,linear_only=False):
    enc=Encoder()
    graph=[[bool(v) for v in row] for row in adjacency]
    for i,j in combinations(OLD,2):
        if i in STAR4 and j in STAR4:
            continue
        cap=2-len(set(LABELS[i])&set(LABELS[j]))-sum(adjacency[i][x]*adjacency[j][x] for x in NEW)
        assert cap>=0
        graph[i][j]=graph[j][i]=enc.var() if cap else False
    for i,p in enumerate(LABELS):
        enc.at_most(graph[i],12)
        for r in range(14):
            target=2-int(r in p)-int((r^1) in p)
            terms=[graph[i][j] for j,q in enumerate(LABELS) if r in q]
            (enc.exactly if r<5 else enc.at_most)(terms,target)
    for i,j in combinations(range(len(LABELS)),2):
        if linear_only and i in OLD and j in OLD:
            continue
        terms=[graph[i][j]]+[enc.conjunction(graph[i][z],graph[j][z]) for z in range(len(LABELS))]
        enc.at_most(terms,2-len(set(LABELS[i])&set(LABELS[j])))
    return enc,graph


def validate(graph,linear_only=False):
    for i,p in enumerate(LABELS):
        assert sum(graph[i])<=12
        for r in range(14):
            count=sum(graph[i][j] for j,q in enumerate(LABELS) if r in q)
            target=2-int(r in p)-int((r^1) in p)
            assert count<=target and (r>=5 or count==target)
    for i,j in combinations(range(len(LABELS)),2):
        if linear_only and i in OLD and j in OLD:
            continue
        assert graph[i][j]+sum(graph[i][z]*graph[j][z] for z in range(len(LABELS)))+len(set(LABELS[i])&set(LABELS[j]))<=2


def run(source,output,seconds=60,linear_only=False):
    started=time.monotonic()
    record=json.loads(Path(source).read_text(encoding='utf-8'))
    enc,graph=build(record['partial_adjacency'],linear_only)
    output=Path(output)
    cnf_path=output.with_suffix('.cnf')
    log_path=output.with_suffix('.sat.log')
    proof_path=output.with_suffix('.drat')
    enc.cnf.to_file(str(cnf_path))
    build_seconds=time.monotonic()-started
    print(json.dumps(dict(stage='CNF',variables=enc.cnf.nv,clauses=len(enc.cnf.clauses),build_seconds=build_seconds)),flush=True)
    try:
        with log_path.open('w',encoding='utf-8') as stream:
            process=subprocess.run([str(CADICAL),str(cnf_path),str(proof_path)],stdout=stream,stderr=subprocess.STDOUT,
                                   timeout=seconds,creationflags=0x08000000 if os.name=='nt' else 0)
        exit_code=process.returncode
    except subprocess.TimeoutExpired:
        exit_code=None
    result=dict(source_file=str(source),linear_only=linear_only,variables=enc.cnf.nv,clauses=len(enc.cnf.clauses),
                build_seconds=build_seconds,seconds=time.monotonic()-started,solver_exit_code=exit_code,
                status='SAT' if exit_code==10 else 'UNSAT' if exit_code==20 else 'UNKNOWN',complete=exit_code in (10,20),
                cnf_file=str(cnf_path),cnf_sha256=sha256(cnf_path.read_bytes()).hexdigest(),
                log_file=str(log_path),proof_file=str(proof_path),
                proof_status='DRAT_OUTPUT_NOT_EXTERNALLY_CHECKED' if exit_code==20 else 'NOT_APPLICABLE_SAT' if exit_code==10 else 'UNFINISHED_NOT_A_CERTIFICATE',
                scope='Fixed attachments and star4 matching; all other old-old edges free. No PSD/rank asserted.')
    if exit_code==10:
        literals=[]
        for line in log_path.read_text(encoding='utf-8').splitlines():
            if line.startswith('v '):
                literals.extend(map(int,line[2:].split()))
        true={v for v in literals if v>0}
        candidate=[[int(v) if isinstance(v,bool) else int(v in true) for v in row] for row in graph]
        validate(candidate,linear_only)
        result.update(adjacency=candidate,labels=LABELS,exact_combinatorial_check=True)
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('adjacency','labels')}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--seconds',type=float,default=60)
    parser.add_argument('--linear-only',action='store_true')
    args=parser.parse_args()
    run(args.source,args.output,args.seconds,args.linear_only)
