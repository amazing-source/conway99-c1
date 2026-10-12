"""Explicit transports: all BvLS triangles, all pairs of near prisms, and three mate pairs in one layer."""
from pathlib import Path
import itertools,json,collections
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
A=np.load(ROOT/'data/bvls.npy');pts=np.array(list(itertools.product(range(3),repeat=5)));ws=np.array([81,27,9,3,1]);Ms=np.loadtxt(ROOT/'data/linear_aut.txt',dtype=int).reshape(-1,5,5)
T={0,1,2};near=set().union(*[set(np.flatnonzero(A[t]).tolist()) for t in T])-T
comps=[];rest=near.copy()
while rest:
 comp={min(rest)};q=list(comp)
 while q:
  u=q.pop()
  for v in near&set(np.flatnonzero(A[u]).tolist()):
   if v not in comp:comp.add(v);q.append(v)
 comps.append(sorted(comp));rest-=comp
assert len(comps)==10 and all(len(c)==6 for c in comps)
U=set(comps[0]+comps[1]);W={3,6,9,18,27,54};pair_trans={};layer_trans={};direction_trans={};group_size=0
for M in Ms:
 # Verify preservation of the exact connection set (sufficient for a linear Cayley automorphism).
 P=(pts@M.T%3)@ws
 assert set(P[np.flatnonzero(A[0])])==set(np.flatnonzero(A[0]))
 direction=tuple(sorted([int(P[1]),int(P[2])]))
 direction_trans.setdefault(direction,M.tolist())
 if set(P[list(T)])!=T:continue
 for c in range(3):
  p=((pts@M.T+np.array([0,0,0,0,c]))%3)@ws;group_size+=1
  im=tuple(sorted(p[list(U)].tolist()));pair_trans.setdefault(im,{'M':M.tolist(),'t':[0,0,0,0,c]})
  im2=tuple(sorted(p[list(W)].tolist()));layer_trans.setdefault(im2,{'M':M.tolist(),'t':[0,0,0,0,c]})
assert len(pair_trans)==45 and set(pair_trans)=={tuple(sorted(a+b)) for a,b in itertools.combinations(comps,2)}
assert len(layer_trans)==360
tri_trans={}
for direction,M in direction_trans.items():
 M=np.array(M)
 for t in pts:
  p=((pts@M.T+t)%3)@ws;im=tuple(sorted(p[list(T)].tolist()));tri_trans.setdefault(im,{'M':M.tolist(),'t':t.tolist()})
actual={tuple(sorted((x,y,z))) for x in range(243) for y in np.flatnonzero(A[x]) for z in set(np.flatnonzero(A[x]))&set(np.flatnonzero(A[y])) if x<y<z}
assert set(tri_trans)==actual and len(actual)==891
report={'prisms_at_T':comps,'linear_maps_checked':len(Ms),'triangle_stabilising_maps':group_size,'triangle_transports':[{'target':list(k),**v} for k,v in tri_trans.items()],'two_prism_transports':[{'target':list(k),**v} for k,v in pair_trans.items()],'three_pairs_one_layer_transports':[{'target':list(k),**v} for k,v in layer_trans.items()]}
(ROOT/'reports/coverage.json').write_text(json.dumps(report))
print('Verified:',len(actual),'triangles;',len(pair_trans),'prism pairs;',len(layer_trans),'three-pair releases; group maps',group_size)
