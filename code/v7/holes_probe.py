import json, sys, itertools, random, time
from bstage import solve_core, P13
cores=json.load(open('cores27.json'))
k=int(sys.argv[1]); tl=float(sys.argv[2]); nsamp=int(sys.argv[3])
core=cores[k]
cols=core['columns']  # t-pairs of 14..26
# admissible hole sets: endpoint t's need >=1 hole among their 13-nbrs (t-equation: 4-deg13+holes>=0)
E=core['zero_edge']
def ok(H):
    for t in range(6):
        d=sum(1 for c in cols if t in c); hh=sum(1 for i in H if t in cols[i])
        if 4-d+hh<0: return False
    return True
cands=[H for H in itertools.combinations(range(13),4) if ok(H)]
# quotient by identical t-pairs
canon={}
for H in cands:
    key=tuple(sorted(tuple(cols[i]) for i in H))
    canon.setdefault(key,H)
print('admissible',len(cands),'up to equal t-pairs',len(canon),flush=True)
random.seed(1)
keys=list(canon)
for key in random.sample(keys,min(nsamp,len(keys))):
    H=canon[key]
    holes=[14+i for i in H]
    def extra(m,colsl,n,used,h):
        for v in P13: m.Add(h[v]==(1 if v in holes else 0))
    r=solve_core(core,time_limit=tl,extra=extra)
    print(key,r['status'],r['time'],flush=True)
