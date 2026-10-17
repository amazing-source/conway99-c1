"""Symbolic boundary exclusion by the eleven distinct covers lemma.

Projected covers are enumerated once on retained incidences. A selector may
be true only if all missing incidences make that cover a genuine linear
2-cover. Any C1 completion forces at least eleven such covers through EACH
outside vertex. Counterexamples supply another vertex needing that capacity.
"""
from itertools import combinations
from pathlib import Path
import argparse
import json
import subprocess
import time

from hoffman_coexistence_extensions import ExtensionModel,SOURCE,OUT
from hoffman_two_point_trades import design_key
from complete_hoffman_trades import instance

BASE=Path(__file__).resolve().parents[2]
ENGINE=BASE/'data/codex_hoffman_trades/rows22.exe'


def projected_covers(model,r,folder):
    folder.mkdir(exist_ok=True)
    fixed=sorted(model.fixed)
    lines=[f'{len(fixed)} 77']
    lines+=[' '.join(str(int(p in b)) for b in model.blocks) for p in fixed]
    lines+=['10 '+' '.join(str(2-int(p in b)) for p in fixed) for b in model.blocks]
    inst=folder/'projected.inst'; inst.write_text('\n'.join(lines)+'\n')
    run=subprocess.run([str(ENGINE),str(inst),str(folder/'row'),'20','500000',str(r),str(r+1)],
                       capture_output=True,text=True,check=True,timeout=30)
    stat=run.stdout.strip().split()
    if stat[3]!='EXHAUSTED':
        raise RuntimeError('Projected cover enumeration is incomplete: '+run.stdout)
    rows=[list(map(int,line.split())) for line in (folder/f'row_{r}.rows').read_text().splitlines()]
    return [sorted(row+[r]) for row in rows],stat


def add_capacity(model,r,folder,pair_capacity=False,resolution=False):
    covers,stat=projected_covers(model,r,folder)
    m=model.m; selectors=[]
    if not hasattr(model,'linear_pair'):
        model.linear_pair={}
    for ci,cover in enumerate(covers):
        v=m.new_bool_var(f'cover{r}_{ci}');selectors.append(v)
        for p in model.free:
            m.add(sum(model.y[p][j] for j in cover)==2).only_enforce_if(v)
        guards=[]
        for a,b in combinations(cover,2):
            ov=model.block_overlap[a,b]
            if isinstance(ov,int):
                assert ov<=1
                continue
            if (a,b) not in model.linear_pair:
                linear=m.new_bool_var(f'linear{a}_{b}')
                m.add(ov<=1).only_enforce_if(linear)
                model.linear_pair[a,b]=linear
            guards.append(model.linear_pair[a,b])
        if guards:m.add_bool_and(guards).only_enforce_if(v)
    if resolution:
        assert model.blocks[r] <= model.fixed
        m.add(sum(selectors)==10)
        for j in range(77):
            if j!=r:
                z=len(model.blocks[r]&model.blocks[j])
                m.add(sum(v for v,c in zip(selectors,covers) if j in c)==2-z)
        model.add_row(r)
        central=model.rows[r]
        for v,c in zip(selectors,covers):
            m.add(sum((2 if len(model.blocks[r]&model.blocks[j])==1 else 1)*central[j]
                      for j in c if j!=r)==2).only_enforce_if(v)
    else:
        m.add(sum(selectors)>=11)
        if pair_capacity:
            for j in range(77):
                if j!=r:
                    m.add(sum(v for v,c in zip(selectors,covers) if j in c)>=
                          2-model.block_overlap[tuple(sorted((r,j)))])
    return dict(root=r,projected_covers=len(covers),enumeration=stat,
                pair_capacity=pair_capacity,resolution=resolution)


def find_deficient(blocks,folder,already,pair_capacity=False):
    folder.mkdir(exist_ok=True)
    inst=folder/'input.inst';inst.write_text(instance(blocks))
    run=subprocess.run([str(ENGINE),str(inst),str(folder/'row'),'10','1000000'],
                       capture_output=True,text=True,check=True,timeout=830)
    stats=[line.split() for line in run.stdout.splitlines() if line.strip()]
    assert len(stats)==77
    deficient=[int(s[0]) for s in stats if s[3]=='EXHAUSTED' and int(s[1])<11]
    deficits={}
    if pair_capacity:
        bs=list(map(set,blocks))
        for r in range(77):
            if stats[r][3]!='EXHAUSTED':continue
            rows=[set(map(int,line.split())) for line in (folder/f'row_{r}.rows').read_text().splitlines()]
            bad=[[j,len(bs[r]&bs[j]),sum(j in row for row in rows)] for j in range(77)
                 if j!=r and sum(j in row for row in rows)<2-len(bs[r]&bs[j])]
            if bad:
                deficits[r]=bad
                if r not in deficient:deficient.append(r)
    assert not(set(deficient)&set(already)), 'A capacity constraint returned a deficient model'
    if not deficient:
        return dict(status='CAPACITY_SURVIVOR',statistics=stats)
    root=min(deficient,key=lambda r:int(stats[r][1]))
    rows=[list(map(int,line.split())) for line in (folder/f'row_{root}.rows').read_text().splitlines()]
    return dict(status='UNSAT_CAPACITY',root=root,count=len(rows),rows=rows,
                deficient=deficient,statistics=stats,pair_deficits=deficits.get(root,[]))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',default='3,4,5,6,7')
    ap.add_argument('--root',type=int,default=10)
    ap.add_argument('--seconds',type=float,default=60)
    ap.add_argument('--workers',type=int,default=4)
    ap.add_argument('--iterations',type=int,default=12)
    ap.add_argument('--pair-capacity',action='store_true')
    ap.add_argument('--resolution',action='store_true')
    args=ap.parse_args()
    item=next(x for x in json.loads(SOURCE.read_text())['items'] if x['design']['key'].startswith(args.prefix))
    model=ExtensionModel(item['design']['blocks'],list(map(int,args.free.split(','))))
    folder=OUT/('capacity_'+args.prefix+'_'+args.free.replace(',','-')+
                ('_resolution' if args.resolution else '_pairs' if args.pair_capacity else ''))
    folder.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    initial=add_capacity(model,args.root,folder/f'root_{args.root}',args.pair_capacity,args.resolution)
    roots=[args.root]
    record=dict(source=item['design']['key'],source_blocks=item['design']['blocks'],free=model.free,
                initial=initial,iterations=[],status='RUNNING',arguments=vars(args))
    print('CAPACITY',initial,flush=True)
    for iteration in range(args.iterations):
        result=model.solve(args.seconds,args.workers)
        step=dict(iteration=iteration,model_result=result)
        record['iterations'].append(step)
        print('ITER',iteration,'roots',roots,result['status'],round(result['seconds'],3),flush=True)
        if result['status']=='INFEASIBLE':
            record['status']='UNSAT_ALL_BOUNDARY_EXTENSIONS'
        elif 'blocks' in result:
            key,aut=design_key(result['blocks'])
            step.update(boundary_key=key,automorphism_order=int(aut))
            cert=find_deficient(result['blocks'],folder/f'candidate_{iteration:02}',roots,args.pair_capacity)
            step['capacity_certificate']=cert
            print('BOUNDARY',key[:12],'Aut',aut,cert['status'],cert.get('root'),cert.get('count'),flush=True)
            if cert['status']=='UNSAT_CAPACITY':
                root=cert['root'];roots.append(root)
                step['added_capacity']=add_capacity(model,root,folder/f'root_{root}',args.pair_capacity,args.resolution)
                print('CAPACITY',step['added_capacity'],flush=True)
            else:record['status']='NEEDS_DISTANCE_OR_RESOLUTION'
        else:record['status']='UNKNOWN_FAMILY'
        record['elapsed_seconds']=time.monotonic()-start
        record['capacity_roots']=roots
        (folder/'result.json').write_text(json.dumps(record,indent=2))
        if record['status']!='RUNNING':break
    else:
        record['status']='ITERATION_LIMIT'
        (folder/'result.json').write_text(json.dumps(record,indent=2))
    print('RESULT',record['status'],flush=True)


if __name__=='__main__':main()
