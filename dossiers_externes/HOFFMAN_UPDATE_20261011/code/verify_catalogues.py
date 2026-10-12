"""Independent finite catalogue audit using all 231 point pairs, not difference vectors.
Regenerate complete block orbits from explicit permutations; pick three full
orbits whose point-pair incidence counts fill the required vector. Reject
three-point intersections directly and compare with the recorded catalogues.
"""
from itertools import combinations
from collections import Counter,defaultdict
from pathlib import Path
import time,json
R=Path(__file__).resolve().parents[1]
import os
OUT=Path(os.environ.get('HOFFMAN_OUTPUT_DIR',str(R/'reports')))
OUT.mkdir(parents=True,exist_ok=True)
PAIRS=list(combinations(range(22),2));PI={p:i for i,p in enumerate(PAIRS)}
def orbit(B,perms):
 return tuple(sorted(set(tuple(sorted(p[a] for a in B)) for p in perms)))
def counts(blocks):
 a=[0]*231
 for B in blocks:
  for p in combinations(B,2):a[PI[p]]+=1
 return tuple(a)
def audit(family,perms,finite,short_bases,orbit_length,path):
 t0=time.time();short=tuple(sorted(set(b for B in short_bases for b in orbit(B,perms))))
 target=tuple(2-c for c in counts(short));assert min(target)>=0
 seen=set();eligible=[];by=defaultdict(list);total=0
 for B in combinations(finite,4):
  if B in seen:continue
  O=orbit(B,perms);seen.update(O)
  if len(O)!=orbit_length:continue
  total+=1;ct=counts(O)
  if any(a>b for a,b in zip(ct,target)):continue
  # no intersection tests here: they are applied after selecting complete designs
  by[ct].append(len(eligible));eligible.append((O,ct))
 print(family,'full orbits',total,'point-pair-eligible',len(eligible),flush=True)
 result=set();raw=0;bad=0
 for i,(O,a) in enumerate(eligible):
  for j in range(i+1,len(eligible)):
   P,b=eligible[j];need=tuple(x-y-z for x,y,z in zip(target,a,b))
   if min(need)<0:continue
   for k in by.get(need,[]):
    if k<=j:continue
    Q,c=eligible[k];raw+=1;blocks=tuple(sorted(short+O+P+Q));assert len(blocks)==77
    assert counts(blocks)==(2,)*231
    if any(len(set(b)&set(c))>2 for b,c in combinations(blocks,2)):bad+=1;continue
    result.add(blocks)
 recorded={tuple(tuple(b) for b in d['blocks']) for d in json.loads((R/'data'/path).read_text())['designs']}
 assert result==recorded,(family,len(result),len(recorded),len(result-recorded),len(recorded-result))
 return {'family':family,'full_orbits':total,'eligible_orbits':len(eligible),'design_selections_before_intersection_test':raw,
         'rejected_for_intersection_three':bad,'admissible_normalized_designs':len(result),'agrees_with_primary_catalogue':True,'seconds':time.time()-t0}
def main():
 out=[]
 out.append(audit('cyclic',[[ (a+t)%22 for a in range(22)] for t in range(22)],range(22),[(0,1,11,12)],22,'cyclic_designs22.json'))
 from one_rotational_designs import P
 out.append(audit('C7:C3 fixing infinity',P,range(21),[(0,1,2,21),(0,4,11,21)],21,'one_rotational_designs22.json'))
 (OUT/'catalogues_verified.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
