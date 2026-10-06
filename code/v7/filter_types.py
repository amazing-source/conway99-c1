import json, sys, time, itertools, numpy as np
from bstage import gen_columns
from colfilter import filter_columns
cores=json.load(open('cores27.json'))
k=int(sys.argv[1]); holes=[int(v) for v in sys.argv[2].split(',')]
core=cores[k]
cols=gen_columns(np.array(core['adj']),set(tuple(p) for p in core['defect']))
dead,nw=filter_columns(core,holes,cols)
need={(0,1):6,(0,0):4,(1,1):6,(1,0):4,(2,1):2,(2,0):8,(5,1):2,(5,0):8}
for g in (3,4,6,7): need[(g,1)]=1; need[(g,0)]=7
from bstage import pdeg, QCORE, P13
tot={}; alive={}
for (b,q),d in zip(cols,dead):
    g=b[0]
    # hole-dependent local rule
    p13=[v for v in b if v in P13]; lim=pdeg(g,q)-(1 if QCORE[g]==1 else 0)
    if sum(1 for v in p13 if v not in holes)>lim: continue
    tot[(g,q)]=tot.get((g,q),0)+1
    if not d: alive[(g,q)]=alive.get((g,q),0)+1
for key in sorted(need): print(key,'need',need[key],'local-valid',tot.get(key,0),'alive after residual filter',alive.get(key,0))
