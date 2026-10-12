"""Convert variable-core cycle witnesses to full populations and certify failures."""
from pathlib import Path
from collections import defaultdict
import argparse
import hashlib
import json
import time

from coclique_completion_certificate import certificate
from coclique_defect_cut_loop import local_choices


def convert(witness):
    n=witness['vertices'];adj=[set() for _ in range(n)]
    for i,j in witness['edges']:adj[i].add(j);adj[j].add(i)
    q=[2]*4+[1]*12+[-1]*2
    core=dict(charges=q,boundary_degrees=[4-v for v in q],
              edges=[e for e in witness['edges'] if max(e)<18],
              parameters=dict(degree=14,r=3,shift=2),
              profile=dict(b1=0,b2=4,b3=12,b4=60,b5=2))
    cells=defaultdict(lambda:[0,0]);C=set(witness['coclique'])
    for v in range(18,n):
        row=tuple(sorted(i for i in adj[v] if i<18));cells[row][0]+=1;cells[row][1]+=int(v in C)
    for item in witness['remaining_population']:
        row=tuple(item['vertices']);cells[row][0]+=item['count'];cells[row][1]+=item['coclique_count']
    pop=dict(selected_rows=[dict(vertices=row,count=v[0],coclique_count=v[1]) for row,v in sorted(cells.items())])
    assert sum(x['count'] for x in pop['selected_rows'])==81
    assert sum(x['coclique_count'] for x in pop['selected_rows'])==21
    return core,pop


def run(source,folder):
    folder.mkdir(parents=True,exist_ok=True);results=[]
    for p in sorted(source.glob('cycles_*.json')):
        witness=json.loads(p.read_text())
        if 'edges' not in witness:continue
        stem=p.stem;core,pop=convert(witness)
        (folder/f'{stem}_core.json').write_text(json.dumps(core,indent=2)+'\n')
        (folder/f'{stem}_population.json').write_text(json.dumps(pop,indent=2)+'\n')
        proof=certificate(core,pop,30,sparse=True,prune_incompatible=True)
        proof['source_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        (folder/f'{stem}_certificate.json').write_text(json.dumps(proof,indent=2)+'\n')
        local=local_choices(core,pop)
        (folder/f'{stem}_local.json').write_text(json.dumps(local,indent=2)+'\n')
        result=dict(partition=witness['partition'],status=proof['status'],seconds=proof['seconds'],
                    local_feasible=local['feasible'],local_total=local['total'])
        if 'verification' in proof:result['gap']=proof['verification']['gap']
        results.append(result);print(json.dumps(result),flush=True)
        (folder/'summary.json').write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path)
    args=ap.parse_args();run(args.source,args.output)
