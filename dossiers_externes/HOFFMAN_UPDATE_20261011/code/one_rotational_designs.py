"""Enumerate simple 1-rotational 2-(22,4,2) designs under C7:C3.
The group fixes infinity, and acts regularly on 21 points. Two short orbits
of blocks through infinity are fixed up to Aut(C7:C3); three full orbits
of four finite points are then enumerated. No symmetry on graph completions.
"""
from itertools import combinations
from collections import Counter,defaultdict
from pathlib import Path
import json,time
V=[(a,i) for a in range(7) for i in range(3)]
idx={x:i for i,x in enumerate(V)}
def mul(x,y):
 a,i=x;b,j=y
 return ((a+pow(2,i,7)*b)%7,(i+j)%3)
def inv(x):
 a,i=x
 return ((-pow(2,(-i)%3,7)*a)%7,(-i)%3)
P=[[idx[mul(g,x)] for x in V]+[21] for g in V]
def orbit(B):return tuple(sorted(set(tuple(sorted(p[x] for x in B)) for p in P)))
pclasses=sorted({min(idx[x],idx[inv(x)]) for x in V if x!=(0,0)})
pcidx={x:i for i,x in enumerate(pclasses)}
def pair_class(i,j):
 x=mul(inv(V[i]),V[j])
 return pcidx[min(idx[x],idx[inv(x)])]

def main():
 start=time.time()
 # Each infinity orbit is a left coset partition of a subgroup of order 3.
 H0=(0,idx[(0,1)],idx[(0,2)],21)
 H1=(0,idx[(1,1)],idx[(3,2)],21)
 O0,O1=orbit(H0),orbit(H1)
 assert len(O0)==len(O1)==7 and not set(O0)&set(O1)
 short=O0+O1
 short_counts=Counter(pair_class(a,b) for B in short for a,b in combinations(B,2) if b<21)
 # There are 21 unordered finite pairs in each orbit; each short orbit supplies them once.
 assert all(c%21==0 for c in short_counts.values())
 target=tuple(2-short_counts[c]/21 for c in range(10))
 assert all(x.is_integer() if isinstance(x,float) else True for x in target)
 target=tuple(map(int,target));print('target',target,flush=True)
 seen=set();allorbs=[];cands=[];by=defaultdict(list)
 for B in combinations(range(21),4):
  if B in seen:continue
  O=orbit(B);seen.update(O);assert len(O)==21
  B=O[0];allorbs.append((B,O))
  c=Counter(pair_class(a,b) for a,b in combinations(B,2));v=tuple(c[i] for i in range(10))
  if any(v[i]>target[i] for i in range(10)):continue
  # all block intersections at most 2; also with the short orbits
  if any(len(set(B)&set(C))>2 for C in O if C!=B):continue
  if any(len(set(B)&set(C))>2 for C in short):continue
  by[v].append(len(cands));cands.append((B,O,v))
 print('all',len(allorbs),'candidates',len(cands),flush=True)
 ds=[];raw=0;bad=0
 for i,(B,O,v) in enumerate(cands):
  for j in range(i+1,len(cands)):
   C,P,w=cands[j];need=tuple(t-a-b for t,a,b in zip(target,v,w))
   for k in by.get(need,[]):
    if k<=j:continue
    E,Q,u=cands[k];raw+=1
    blocks=tuple(sorted(short+O+P+Q))
    assert len(blocks)==77 and len(set(blocks))==77
    assert Counter(a for b in blocks for a in b)==Counter({a:14 for a in range(22)})
    assert Counter(p for b in blocks for p in combinations(b,2))==Counter({p:2 for p in combinations(range(22),2)})
    if any(len(set(x)&set(y))>2 for x,y in combinations(blocks,2)):bad+=1;continue
    ds.append({'base_blocks':[B,C,E,H0,H1],'blocks':blocks})
 out={'group':'C7:C3, multiplication (a,i)(b,j)=(a+2^i b,i+j)',
      'fixed_point':21,'all_full_orbits':len(allorbs),'candidates':len(cands),'raw_selections':raw,
      'bad_intersections':bad,'designs':ds,'seconds':time.time()-start}
 R=Path(__file__).resolve().parents[1]
 (R/'data/one_rotational_designs22.json').write_text(json.dumps(out))
 print({k:v for k,v in out.items() if k!='designs'},flush=True)
 print('accepted designs',len(ds),flush=True)
 for x in ds[:20]:print(x['base_blocks'],flush=True)
if __name__=='__main__':main()
