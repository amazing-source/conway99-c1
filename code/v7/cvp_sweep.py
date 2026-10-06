import json, itertools, time
import numpy as np
from coset_cvp import run
cores=json.load(open('cores27.json'))
out=[]
t0=time.time()
for k,core in enumerate(cores):
    cols=core['columns']
    def ok(H):
        for t in range(6):
            d=sum(1 for c in cols if t in c); hh=sum(1 for i in H if t in cols[i])
            if 4-d+hh<0: return False
        return True
    adm=[H for H in itertools.combinations(range(13),4) if ok(H)]
    stats={}
    for H in adm:
        res=run(core,[14+i for i in H],bound=34)
        lv0=sorted(v for (l,v) in res if l==0)
        key=(lv0[0] if lv0 else None)
        stats[key]=stats.get(key,0)+1
        if key is not None and key<40:
            out.append({'core':k,'holes':[14+i for i in H],'level0':lv0})
    print(k,'admissible',len(adm),'min level-0 norm (<=34) counts',stats,round(time.time()-t0,1),flush=True)
json.dump(out,open('cvp_sweep_hits.json','w'))
print('hits',len(out))
