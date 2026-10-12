"""Enumerate the possible incidence rows of each erased coclique point.

A missing point occurs in 14 blocks and twice alongside each retained point.
Two selected blocks cannot already share two retained points. The dummy
column lets the existing exact enumerator handle this distinct row problem.
"""
from pathlib import Path
import argparse
import json
import subprocess

from hoffman_coexistence_extensions import ExtensionModel,SOURCE,OUT

BASE=Path(__file__).resolve().parents[2]
ENGINE=BASE/'data/codex_hoffman_trades/rows22.exe'


def enumerate_missing_points(blocks,free,folder,seconds=30,limit=1000000):
    free=set(free);fixed=sorted(set(range(22))-free);bs=list(map(set,blocks))
    forbidden=[j for j,b in enumerate(bs) if not (b&free)]
    # Additional quota-zero rows force already full blocks to stay unavailable.
    matrix=[[int(p in b) for b in bs]+[0] for p in fixed]
    matrix += [[int(j==a) for j in range(77)]+[0] for a in forbidden]
    ns=len(matrix)
    lines=[f'{ns} 78']+[' '.join(map(str,row)) for row in matrix]
    lines += ['0 '+' '.join(['0']*ns) for _ in range(77)]
    lines += ['14 '+' '.join(['2']*len(fixed)+['0']*len(forbidden))]
    folder.mkdir(parents=True,exist_ok=True)
    inst=folder/'missing_point.inst';inst.write_text('\n'.join(lines)+'\n')
    run=subprocess.run([str(ENGINE),str(inst),str(folder/'point'),str(seconds),str(limit),'77','78'],
                       capture_output=True,text=True,check=True,timeout=seconds+10)
    stat=run.stdout.strip().split()
    rows=[list(map(int,line.split())) for line in (folder/'point_77.rows').read_text().splitlines()]
    assert all(len(r)==14 and 77 not in r for r in rows)
    result=dict(free=sorted(free),fixed=fixed,statistics=stat,complete=stat[3]=='EXHAUSTED',
                rows=rows,scope='Possible single erased-point rows; other erased points are not coupled yet')
    (folder/'point_domain.json').write_text(json.dumps(result,separators=(',',':')))
    return result


def add_missing_tables(model,data):
    assert data['complete'] and data['free']==model.free
    for p in model.free:
        indices=[j for j in range(77) if not isinstance(model.y[p][j],int)]
        patterns=[]
        for row in data['rows']:
            row=set(row)
            if any(int(j in row)!=y for j,y in enumerate(model.y[p]) if isinstance(y,int)):
                continue
            patterns.append([int(j in row) for j in indices])
        model.m.add_allowed_assignments([model.y[p][j] for j in indices],patterns)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',default='3,4,5,6,7')
    ap.add_argument('--seconds',type=float,default=30)
    args=ap.parse_args()
    item=next(x for x in json.loads(SOURCE.read_text())['items'] if x['design']['key'].startswith(args.prefix))
    folder=OUT/('point_domains_'+args.prefix+'_'+args.free.replace(',','-'))
    result=enumerate_missing_points(item['design']['blocks'],list(map(int,args.free.split(','))),folder,args.seconds)
    print('RESULT',result['statistics'],flush=True)


if __name__=='__main__':main()
