"""Exact CSP of complete binary row domains; pair compatibility is equivalent to SRG completion."""
from pathlib import Path
import argparse,time,json,collections,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('--seconds',type=float,default=120);p.add_argument('--limit',type=int,default=100000);a=p.parse_args()
meta=json.loads((ROOT/'data'/f'{a.name}.json').read_text());free=meta['free'];fixed=meta['fixed'];n=len(free)
log=(ROOT/'reports'/f'{a.name}.log').read_text().splitlines();assert len(log)==n and all(x.split()[3]=='EXHAUSTED' for x in log),'Incomplete row domains'
G=np.load(ROOT/'data'/meta['graph']);Y=G[np.ix_(fixed,free)];Z=Y.T@Y
rows=[]
for i in range(n):
 ls=[tuple(map(int,line.split())) for line in (ROOT/'data'/f'{a.name}_{i}.rows').read_text().splitlines()]
 masks=[sum(1<<x for x in row) for row in ls];assert len(set(masks))==len(masks)==int(log[i].split()[1]);rows.append(masks)
assert all(rows)
print('Row domains',collections.Counter(map(len,rows)),flush=True)
t0=time.time();support=[[{} for _ in rr] for rr in rows]
for i in range(n):
 for j in range(i+1,n):
  z=int(Z[i,j]);si=[0]*len(rows[i]);sj=[0]*len(rows[j])
  for u,r in enumerate(rows[i]):
   b=(r>>j)&1;need=2-b-z
   for v,s in enumerate(rows[j]):
    if ((s>>i)&1)==b and (r&s).bit_count()==need:si[u]|=1<<v;sj[v]|=1<<u
  for u,ss in enumerate(si):support[i][u][j]=ss
  for v,ss in enumerate(sj):support[j][v][i]=ss
print('Pair supports built',round(time.time()-t0,3),flush=True)
dom=[(1<<len(r))-1 for r in rows]
def propagate(ds,dirty):
 queue=collections.deque(dirty);inq=set(dirty)
 while queue:
  i=queue.popleft();inq.remove(i);di=ds[i]
  for j in range(n):
   if j==i:continue
   dj=ds[j];new=0
   while dj:
    bit=dj&-dj;u=bit.bit_length()-1;dj^=bit
    if support[j][u][i]&di:new|=bit
   if not new:return False
   if new!=ds[j]:
    ds[j]=new
    if j not in inq:inq.add(j);queue.append(j)
 return True
count=0;nodes=0;stop=False;classes={};dest=ROOT/'data'/f'{a.name}_solutions';dest.mkdir(exist_ok=True)
def grids(H):
 nb=[set(np.flatnonzero(r).tolist()) for r in H];hist=collections.Counter();total=0
 for x in range(len(H)):
  lines=[(u,v) for u in nb[x] for v in (nb[x]&nb[u]) if u<v];g=0
  for ix,(u,v) in enumerate(lines):
   for w,z in lines[ix+1:]:
    rest=[(nb[s]&nb[t])-{x} for s,t in [(u,w),(u,z),(v,w),(v,z)]]
    if any(len(y)!=1 for y in rest):continue
    S={x,u,v,w,z,*[next(iter(y)) for y in rest]}
    if len(S)==9 and all(len(nb[t]&S)==4 for t in S):g+=1
  hist[g]+=1;total+=g
 return total//9,dict(sorted(hist.items()))
def dfs(ds):
 global count,nodes,stop
 if stop:return
 nodes+=1
 if time.time()-t0>a.seconds:stop=True;return
 unresolved=[i for i in range(n) if ds[i].bit_count()>1]
 if not unresolved:
  count+=1;H=G.copy()
  for i,x in enumerate(free):
   m=rows[i][ds[i].bit_length()-1]
   for j,y in enumerate(free):H[x,y]=(m>>j)&1
  assert np.array_equal(H,H.T) and np.all(H.sum(0)==22) and np.array_equal(H@H+H,20*np.eye(243,dtype=int)+2*np.ones((243,243),dtype=int))
  b='\n'.join(''.join(map(str,r)) for r in H)+'\n';(dest/f'{count:06d}.adj').write_text(b)
  ng,hist=grids(H);key=str((ng,hist));classes[key]=classes.get(key,0)+1
  if count<=20 or count%100==0:print('solution',count,'grids',ng,hist, 'changed edges',np.count_nonzero(H-G)//2,flush=True)
  if count>=a.limit:stop=True
  return
 i=min(unresolved,key=lambda i:ds[i].bit_count());d=ds[i]
 while d:
  bit=d&-d;d^=bit;new=ds.copy();new[i]=bit
  if propagate(new,[i]):dfs(new)
  if stop:return
if propagate(dom,range(n)):
 print('After full arc consistency',collections.Counter(d.bit_count() for d in dom),flush=True);dfs(dom)
res={'name':a.name,'status':'STOPPED' if stop else 'EXHAUSTED','solutions':count,'nodes':nodes,'seconds':time.time()-t0,'grid_signatures':classes,'fixed':fixed,'free':free}
(ROOT/'reports'/f'{a.name}_assembly.json').write_text(json.dumps(res,indent=2));print(res,flush=True)
