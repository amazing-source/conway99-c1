"""Enumerate cyclic 2-(22,4,2) block designs without three-point intersections.
Every orbit under translation has length 11 or 22. The orbit of length 11 is
normalized to translates of {0,1,11,12}, using a unit of Z/22.
No graph automorphism is imposed on any prospective graph completion.
"""
from itertools import combinations
from collections import Counter,defaultdict
import json,time
from pathlib import Path
N=22

def orbit(B):
    return tuple(sorted(set(tuple(sorted((a+t)%N for a in B)) for t in range(N))))

def distvec(B):
    c=[0]*10
    for a,b in combinations(B,2):
        d=min((b-a)%N,(a-b)%N)
        if d==11:return None
        c[d-1]+=1
    return tuple(c)

def verify(blocks):
    assert len(blocks)==77 and len(set(blocks))==77
    assert Counter(a for b in blocks for a in b)==Counter({i:14 for i in range(22)})
    assert Counter(p for b in blocks for p in combinations(b,2))==Counter({p:2 for p in combinations(range(22),2)})

def main():
    start=time.time(); seen=set(); orbs=[]
    for B in combinations(range(N),4):
        O=orbit(B); B=O[0]
        if B in seen:continue
        seen.add(B)
        if len(O)==22:orbs.append((B,O))
    short=orbit((0,1,11,12));target=(1,2,2,2,2,2,2,2,2,1)
    groups=defaultdict(list);cands=[]
    for B,O in orbs:
        v=distvec(B)
        if v is not None and all(a<=b for a,b in zip(v,target)):
            # Intra-orbit intersection <= 2 is already necessary for Conway.
            if all(len(set(B)&set(T))<=2 for T in O if T!=B):
                groups[v].append(len(cands));cands.append((B,O,v))
    ds=[]; nraw=0; nbad=0
    for i,(B,O,v) in enumerate(cands):
        for j in range(i+1,len(cands)):
            C,P,w=cands[j]; need=tuple(t-a-b for t,a,b in zip(target,v,w))
            for k in groups.get(need,[]):
                if k<=j:continue
                E,Q,u=cands[k]; nraw+=1
                blocks=tuple(sorted(short+O+P+Q));verify(blocks)
                if any(len(set(x)&set(y))>2 for x,y in combinations(blocks,2)):
                    nbad+=1;continue
                ds.append({'base_blocks':[B,C,E,(0,1,11,12)],'blocks':blocks})
    # Isomorphism reduction deliberately NOT performed: counts are normalized orbit sets.
    out={'scope':'all cyclic designs, normalized short orbit; no reduction by full design isomorphism',
         'full_block_orbits':len(orbs),'candidate_full_orbits':len(cands),'raw_selections_after_intra_filter':nraw,
         'cross_intersection_rejections':nbad,'designs':ds,'elapsed_seconds':time.time()-start}
    p=Path(__file__).resolve().parents[1]/'data/cyclic_designs22.json';p.write_text(json.dumps(out))
    print({k:v for k,v in out.items() if k!='designs'});print('designs',len(ds))
    for d in ds[:20]:print(d['base_blocks'])
if __name__=='__main__':main()
