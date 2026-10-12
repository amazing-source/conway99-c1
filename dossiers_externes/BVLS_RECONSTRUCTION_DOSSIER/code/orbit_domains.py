"""Transport complete row domains using explicitly verified automorphisms of the frozen boundary."""
from pathlib import Path
import itertools,subprocess,json,time,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
name=sys.argv[1];meta=json.loads((ROOT/'data'/f'{name}.json').read_text());A=np.load(ROOT/'data'/meta['graph']);fixed=meta['fixed'];free=meta['free'];n=len(free);pts=np.array(list(itertools.product(range(3),repeat=5)));weights=np.array([81,27,9,3,1]);maps=np.loadtxt(ROOT/'data/linear_aut.txt',dtype=int).reshape(-1,5,5)
# All affine BvLS automorphisms preserving the anchor T={0,1,2}; filter boundary and graph.
ps=[];fset=set(fixed)
for M in maps:
 if np.any(M[:4,4]):continue
 for c in range(3):
  P=((pts@M.T+np.array([0,0,0,0,c]))%3)@weights
  if set(P[fixed])==fset and np.array_equal(A[np.ix_(P,P)],A):ps.append(P.tolist())
assert ps;print('Boundary group maps',len(ps),flush=True)
fidx={v:i for i,v in enumerate(free)};reps=[];unseen=set(range(n));trans={}
while unseen:
 r=min(unseen);orb={fidx[p[free[r]]] for p in ps};reps.append(r)
 for p in ps:
  j=fidx[p[free[r]]]
  if j not in trans:trans[j]=(r,[fidx[p[x]] for x in free])
 unseen-=orb
print('row orbits',[(r,sum(rr==r for rr,p in trans.values())) for r in reps],flush=True)
base=ROOT/'data'/name
rlogs={};t0=time.time()
for r in reps:
 cmd=[str(ROOT/'code/rows'),str(base.with_suffix('.inst')),str(base),'90','2000000',str(r),str(r+1)]
 line=subprocess.check_output(cmd,text=True).strip();print(line,flush=True);rlogs[r]=line.split();assert rlogs[r][3]=='EXHAUSTED','representative incomplete'
(domdir:=ROOT/'data'/f'{name}_reps').mkdir(exist_ok=True)
logs=[]
for r in reps:(domdir/f'{r}.rows').write_bytes((ROOT/'data'/f'{name}_{r}.rows').read_bytes())
for j,(r,p) in sorted(trans.items()):
 rows=[list(map(int,s.split())) for s in (domdir/f'{r}.rows').read_text().splitlines()];image=[sorted(p[k] for k in row) for row in rows]
 (ROOT/'data'/f'{name}_{j}.rows').write_text(''.join(' '.join(map(str,row))+'\n' for row in image))
 logs.append(f'{j} {len(image)} {rlogs[r][2]} EXHAUSTED {rlogs[r][4]}')
(ROOT/'reports'/f'{name}.log').write_text('\n'.join(logs)+'\n')
(ROOT/'reports'/f'{name}_transport.json').write_text(json.dumps({'group_order':len(ps),'representatives':reps,'transport':trans,'seconds':time.time()-t0,'representative_logs':rlogs}))
print('complete',name,'seconds',time.time()-t0,flush=True)
