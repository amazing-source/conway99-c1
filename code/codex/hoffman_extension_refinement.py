"""Refine a variable-boundary family by genuine coexistence contradictions.

Every failed fixed design supplies outside vertices whose rows must coexist.
We add these rows SYMBOLICALLY, so they constrain all boundary extensions.
No no-good that merely bans one numerical design is used.
"""
from itertools import combinations
from pathlib import Path
import argparse
import json
import subprocess
import time

from hoffman_coexistence_extensions import ExtensionModel, SOURCE, OUT
from complete_hoffman_trades import instance, arc_consistency
from analyze_hoffman_trade_obstructions import cover_with_four
from hoffman_two_point_trades import design_key

BASE = Path(__file__).resolve().parents[2]
ENUMERATOR = BASE/'data/codex_hoffman_trades/rows22.exe'


def fixed_certificate(blocks, folder, row_seconds=5):
    folder.mkdir(exist_ok=True)
    inst = folder/'input.inst'
    inst.write_text(instance(blocks))
    run = subprocess.run([str(ENUMERATOR),str(inst),str(folder/'row'),str(row_seconds),'1000000'],
                         capture_output=True,text=True,check=True,timeout=77*row_seconds+60)
    (folder/'rows.log').write_text(run.stdout)
    stats = [line.split() for line in run.stdout.splitlines() if line.strip()]
    assert len(stats) == 77
    if any(row[3] != 'EXHAUSTED' for row in stats):
        return dict(status='UNKNOWN_INCOMPLETE_DOMAINS',statistics=stats)
    dom = [[sum(1 << int(j) for j in line.split()) for line in (folder/f'row_{i}.rows').read_text().splitlines()]
           for i in range(77)]
    for i,row in enumerate(dom):
        if not row:
            return dict(status='UNSAT',kind='empty_domain',roots=[i],statistics=stats,
                        domains=[[str(x) for x in d] for d in dom])
    bs = list(map(set,blocks))
    kills = [[0]*77 for _ in range(77)]
    pair = None
    for i,j in combinations(range(77),2):
        z = len(bs[i]&bs[j]); si=sj=0
        for ix,x in enumerate(dom[i]):
            edge=(x>>j)&1
            for iy,y in enumerate(dom[j]):
                if edge == (y>>i)&1 and (x&y).bit_count()+z == 2-edge:
                    si |= 1 << ix; sj |= 1 << iy
        kills[i][j]=((1<<len(dom[i]))-1)^si
        kills[j][i]=((1<<len(dom[j]))-1)^sj
        if not si and (pair is None or len(dom[i])+len(dom[j]) < pair[0]):
            pair=(len(dom[i])+len(dom[j]),i,j)
    if pair:
        _,i,j=pair
        return dict(status='UNSAT',kind='incompatible_pair',roots=[i,j],statistics=stats,
                    domains=[[str(x) for x in d] for d in dom])
    for i in sorted(range(77),key=lambda j:len(dom[j])):
        js=cover_with_four(kills[i],(1<<len(dom[i]))-1)
        if js is not None:
            return dict(status='UNSAT',kind='star',roots=[i]+js,
                        kills={str(j):str(kills[i][j]) for j in js},statistics=stats,
                        domains=[[str(x) for x in d] for d in dom])
    ac=arc_consistency(dom,blocks)
    if ac['status']=='UNSAT_FIXED_DESIGN':
        involved=sorted({j for i,ix,j in ac['deletions']}|{i for i,ix,j in ac['deletions']})
        return dict(status='UNSAT',kind='arc_consistency',roots=involved,statistics=stats,
                    domains=[[str(x) for x in d] for d in dom],arc_certificate=ac)
    return dict(status='ARC_CONSISTENT',statistics=stats,domains=[[str(x) for x in d] for d in dom])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',default='3,4,5')
    ap.add_argument('--seconds',type=float,default=45)
    ap.add_argument('--workers',type=int,default=4)
    ap.add_argument('--iterations',type=int,default=20)
    ap.add_argument('--roots',help='Comma-separated initial rows')
    args=ap.parse_args()
    item=next(x for x in json.loads(SOURCE.read_text())['items'] if x['design']['key'].startswith(args.prefix))
    blocks=item['design']['blocks']; free=list(map(int,args.free.split(',')))
    initial=list(map(int,args.roots.split(','))) if args.roots else item['compact_certificate']['smallest_incompatible_pair']['rows']
    folder=OUT/('refine_'+args.prefix+'_'+args.free.replace(',','-'))
    folder.mkdir(parents=True,exist_ok=True)
    model=ExtensionModel(blocks,free)
    for r in initial: model.add_row(r)
    record=dict(source=item['design']['key'],source_blocks=blocks,free=free,initial_roots=initial,
                arguments=vars(args),iterations=[],status='RUNNING',
                scope='Every SRG Hoffman boundary agreeing with source on all retained point incidences')
    start=time.monotonic()
    for iteration in range(args.iterations):
        result=model.solve(args.seconds,args.workers)
        step=dict(iteration=iteration,model_result=result)
        record['iterations'].append(step)
        print('ITER',iteration,'rows',len(model.rows),result['status'],round(result['seconds'],3),flush=True)
        if result['status']=='INFEASIBLE':
            record['status']='UNSAT_ALL_BOUNDARY_EXTENSIONS'
        elif 'blocks' in result:
            key,aut=design_key(result['blocks'])
            step['boundary_key']=key; step['boundary_automorphism_order']=int(aut)
            cert=fixed_certificate(result['blocks'],folder/f'candidate_{iteration:02}')
            step['fixed_certificate']=cert
            print('BOUNDARY',key[:12],'Aut',aut,cert['status'],cert.get('kind'),cert.get('roots'),flush=True)
            if cert['status']=='UNSAT':
                new=set(cert['roots'])-set(model.rows)
                assert new, 'A returned partial witness violates rows already in the symbolic model'
                for r in sorted(new): model.add_row(r)
                step['added_roots']=sorted(new)
            else:
                record['status']='NEEDS_STRONGER_FIXED_DESIGN_SEARCH'
        else:
            record['status']='UNKNOWN_FAMILY'
        record['elapsed_seconds']=time.monotonic()-start
        record['final_roots']=sorted(model.rows)
        (folder/'result.json').write_text(json.dumps(record,indent=2))
        if record['status']!='RUNNING': break
    else:
        record['status']='ITERATION_LIMIT'
        (folder/'result.json').write_text(json.dumps(record,indent=2))
    print('RESULT',record['status'],'roots',record['final_roots'],flush=True)


if __name__=='__main__': main()
