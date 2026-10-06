import json, sys, time, numpy as np
from bstage import gen_columns
from colfilter import filter_columns
from bstage2 import model
cores=json.load(open('cores27.json'))
k=int(sys.argv[1]); holes=[int(v) for v in sys.argv[2].split(',')]; tl=float(sys.argv[3])
core=cores[k]
cols=gen_columns(np.array(core['adj']),set(tuple(p) for p in core['defect']))
t=time.time(); dead,nw=filter_columns(core,holes,cols); print('filter killed',int(dead.sum()),'of',len(cols),round(time.time()-t,1),flush=True)
r=model(core,use_q=True,fix_holes=holes,time_limit=tl,workers=2,colmask=~dead)
print('reduced B-stage:',r['status'],r['time'],r['ncols'],flush=True)
