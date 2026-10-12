"""Reproducible native search for joint Hoffman neighbourhood obligations."""
from pathlib import Path
from types import SimpleNamespace
import argparse
import hashlib
import json
import subprocess
import time

from hoffman_coexistence_extensions import SOURCE,OUT
from hoffman_cover_capacity import projected_covers
from hoffman_missing_point_domains import enumerate_missing_points

BASE=Path(__file__).resolve().parents[2]
CPP=Path(__file__).with_suffix('.cpp')
ENGINE=OUT/'coexistence_v2.exe'


def write_instance(path,root,erased,rows,point_rows,quota,missing,known):
    data=[f'77 {root} {erased} {len(rows)} {len(point_rows)}',
          ' '.join(map(str,quota)),' '.join(map(str,missing))]
    data += [' '.join(map(str,r)) for r in known]
    data += [' '.join(map(str,r)) for r in rows]
    data += [' '.join(map(str,r)) for r in point_rows]
    path.write_text('\n'.join(data)+'\n')


def fixture_check(folder):
    edges=[(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(1,3),(1,5),
           (1,6),(1,7),(1,8),(1,9),(2,4),(2,5),(2,6),(2,7),
           (2,8),(2,9),(3,4),(3,5),(3,6),(3,7),(3,9),(4,8)]
    rows=[];next_one=11
    for a in range(10):
        pattern={a+1} if a<4 else {5+2*((a-4)//2),6+2*((a-4)//2)}
        extra=set(range(next_one,next_one+(3 if a<4 else 4)));next_one+=len(extra)
        zeros={47+t for t,e in enumerate(edges) if a in e}
        rows.append(sorted(pattern|extra|zeros))
    rows=[list(range(1,11))]+rows
    quota=[0]+[1]*4+[2]*6+[1]*36+[2]*24+[0]*6
    reports={}
    for label,rr,expected in [('positive',rows,'FEASIBLE_LABELLED_STAR_NOT_SRG'),
                               ('negative',rows[:-1],'UNSAT_ALL_BOUNDARY_EXTENSIONS')]:
        inp=folder/f'fixture_{label}.inst';out=folder/f'fixture_{label}.json'
        write_instance(inp,0,0,rr,[],quota,[1]*77,[[0]*77 for _ in range(77)])
        subprocess.run([str(ENGINE),str(inp),str(out),'10','100000','0'],check=True,capture_output=True)
        result=json.loads(out.read_text());assert result['status']==expected,result
        reports[label]=result['status']
    return reports


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',default='3,4,5,6,7,8')
    ap.add_argument('--root',type=int,default=10)
    ap.add_argument('--seconds',type=float,default=300)
    ap.add_argument('--max-nodes',type=int,default=100000000)
    ap.add_argument('--no-points',action='store_true')
    args=ap.parse_args();OUT.mkdir(exist_ok=True)
    if not ENGINE.exists() or ENGINE.stat().st_mtime<CPP.stat().st_mtime:
        subprocess.run(['g++','-std=c++20','-O3','-march=native',str(CPP),'-o',str(ENGINE)],check=True)
    item=next(x for x in json.loads(SOURCE.read_text())['items'] if x['design']['key'].startswith(args.prefix))
    blocks=item['design']['blocks'];bs=list(map(set,blocks));free=sorted(map(int,args.free.split(',')))
    fixed=set(range(22))-set(free);root=args.root;assert bs[root]<=fixed
    folder=OUT/('coexistence_v2_'+args.prefix+'_'+args.free.replace(',','-')+
                ('_no_points' if args.no_points else '')+('_root'+str(root) if root!=10 else ''))
    folder.mkdir(parents=True,exist_ok=True)
    fixture=fixture_check(folder)
    covers,pstat=projected_covers(SimpleNamespace(fixed=fixed,blocks=bs),root,folder/'projected')
    rows=[[j for j in c if j!=root] for c in covers]
    pdir=OUT/('point_domains_'+args.prefix+'_'+args.free.replace(',','-'))
    if args.no_points:
        pdata=dict(rows=[],complete=True,free=free,statistics=['NOT_USED'])
    elif (pdir/'point_domain.json').exists():pdata=json.loads((pdir/'point_domain.json').read_text())
    else:pdata=enumerate_missing_points(blocks,free,pdir)
    assert pdata['complete'] and pdata['free']==free
    quota=[2-len(bs[root]&b) if j!=root else 0 for j,b in enumerate(bs)]
    missing=[4-len(b&fixed) for b in bs]
    known=[[len(a&b&fixed) for b in bs] for a in bs]
    inp=folder/'input.inst';out=folder/'native_result.json'
    write_instance(inp,root,0 if args.no_points else len(free),rows,pdata['rows'],quota,missing,known)
    start=time.monotonic()
    cmd=[str(ENGINE),str(inp),str(out),str(args.seconds),str(args.max_nodes),str(int(not args.no_points))]
    with (folder/'search.log').open('w',encoding='utf8') as log:
        process=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        for line in process.stdout:
            print(line,end='',flush=True);log.write(line);log.flush()
        if process.wait()!=0:raise RuntimeError('Native search failed')
    result=json.loads(out.read_text())
    if 'central_index' in result:
        central=set(rows[result['central_index']]);centres=result['assigned_centres']
        ss=[set(rows[a]) for a in result['transported_indices']]
        assert set(centres)==central and len({tuple(sorted(s)) for s in ss})==10
        assert [sum(j in s for s in ss) for j in range(77)]==quota
        for x,j in enumerate(centres):
            assert j in ss[x]
            for y,k in enumerate(centres[:x]):
                paired=(k in ss[x]);assert paired==(j in ss[y])
                common=len(ss[x]&ss[y])
                if paired:assert known[j][k]==0 and common==2
                else:assert known[j][k]+common<=1<=known[j][k]+common+min(missing[j],missing[k])
        result['central']=sorted(central);result['transported']=[sorted(s) for s in ss]
    result.update(source=item['design']['key'],source_blocks=blocks,free=free,root=root,
                  candidate_rows=len(rows),point_domain_count=len(pdata['rows']),
                  projection_statistics=pstat,point_statistics=pdata['statistics'],
                  arguments=vars(args),fixture_check=fixture,wall_seconds=time.monotonic()-start,
                  input_sha256=hashlib.sha256(inp.read_bytes()).hexdigest(),
                  engine_source_sha256=hashlib.sha256(CPP.read_bytes()).hexdigest(),
                  scope='All C1 Hoffman completions of this retained incidence template; a feasible output remains only a necessary star relaxation')
    (folder/'result.json').write_text(json.dumps(result,indent=2))
    print('SAVED',folder/'result.json',flush=True)


if __name__=='__main__':main()
