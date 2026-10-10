"""Boundary relaxation retaining only core+D and one whole P4 component.

All seven other Z vertices remain unspecified except for their D degrees.
This tests a P4 placement uniformly over those remaining placements.
"""
from itertools import combinations
from collections import Counter
import json
import argparse
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from norm16_schur_data import ROOT,source_data
from norm16_independent_catalogue import adjacency


def boundary(seed):
    cores,cases,forests=source_data();ci,oi,fid=seed['case'],seed['orbit'],seed['forest']
    core=cores[ci]['representatives'][0];attachment=cases[ci]['orbits'][oi]['representative']
    f=next(f for f in forests if f['id']==fid);az=f['adjacency_Z'];deg=list(map(sum,az))
    middle=next((i,j) for i,j in combinations(range(11),2) if az[i][j] and deg[i]==deg[j]==2)
    left=next(i for i in range(11) if az[i][middle[0]] and i!=middle[1])
    right=next(i for i in range(11) if az[i][middle[1]] and i!=middle[0])
    path=[left,*middle,right];indices=list(range(24))+[24+z for z in path]
    full=adjacency(core,attachment,f,seed['D_Z_row_masks']);a=full[np.ix_(indices,indices)];common=a@a
    record=next(r for r in json.loads((ROOT/'data/codex_norm16_shadow_connectivity.json').read_text())['records'] if (r['case'],r['orbit'])==(ci,oi))
    u,v=record['tight_subsets'];hist=Counter(deg[z]+2 for z in range(11) if z not in path)
    saturated=[(1<<i)|(1<<j) for i,j in combinations(range(28),2) if common[i,j]==2-a[i,j]]
    rowmasks=[sum(1<<i for i,x in enumerate(row) if x) for row in a]
    labels=[];rhs=[];entries=[];columns=[]
    def eq(label,target):
        labels.append(label);rhs.append(int(target));return len(rhs)-1
    drows=[eq(['degree',i],14-sum(a[i])) for i in range(28)]
    prows={(i,j):eq(['pair',i,j],2-a[i,j]-common[i,j]) for i,j in combinations(range(28),2)}
    def valid(mask):
        return not any(mask&pair==pair for pair in saturated) and all((mask&row).bit_count()<=2-((mask>>i)&1) for i,row in enumerate(rowmasks))
    def column(kind,mask,extra):
        ns=[i for i in range(28) if mask>>i&1]
        ci=len(columns);columns.append([kind,mask]);rows=[extra]+[drows[i] for i in ns]+[prows[i,j] for i,j in combinations(ns,2)]
        entries.extend((r,ci,1) for r in rows)
    for p in range(8):
        for q in range(8,16):
            copies=2-a[p,q]-common[p,q]
            if not copies:continue
            cr=eq(['cell',p,q-8],copies)
            for du in [None]+u:
                for dv in [None]+v:
                    ds=[d for d in (du,dv) if d is not None];base=(1<<p)|(1<<q)|sum(1<<(16+d) for d in ds)
                    for zm in range(16):
                        if zm.bit_count()>1+len(ds):continue
                        mask=base|(zm<<24)
                        if valid(mask):column('B',mask,cr)
    for r,n in sorted(hist.items()):
        er=eq(['outside_Z_D_degree',r],n)
        for ds in combinations(range(8),r):
            if not(1<=len(set(ds)&set(u))<=2 and 1<=len(set(ds)&set(v))<=2):continue
            mask=sum(1<<(16+d) for d in ds)
            if valid(mask):column('Z',mask,er)
    rr,cc,val=zip(*entries)
    m=coo_matrix((val,(rr,cc)),shape=(len(rhs),len(columns)),dtype=np.int64).tocsr()
    return m,np.array(rhs),labels,columns,path


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--forest',type=int,default=2);args=p.parse_args()
    seed=next(s for s in json.loads((ROOT/'data/codex_norm16_tight_seed_sample.json').read_text())['seeds'] if s['forest']==args.forest)
    m,b,labels,columns,path=boundary(seed)
    answer=linprog(np.zeros(len(columns)),A_eq=m,b_eq=b,bounds=(0,None),method='highs')
    out={'scope':__doc__,'seed':seed,'P4_vertices':path,'columns':len(columns),'LP_status':int(answer.status),'message':answer.message}
    if answer.success:out['maximum_residual']=float(np.max(abs(m@answer.x-b)))
    (ROOT/f'data/codex_norm16_p4_boundary_f{args.forest}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)
