"""Pure-Python certificate: an asymmetric SRG can contain Hoffman cocliques.
All adjacency equations, the complete five-coclique census and a vertex-invariant
asymmetry certificate are computed from the matrix, not from recorded claims.
"""
from pathlib import Path
from itertools import combinations
import json
R=Path(__file__).resolve().parents[1]
import os
OUT=Path(os.environ.get('HOFFMAN_OUTPUT_DIR',str(R/'reports')))
OUT.mkdir(parents=True,exist_ok=True)
def bits(x):
 while x:
  b=x&-x;yield b.bit_length()-1;x-=b

def verify():
 text=(R/'data/paley_asymmetric25.adj').read_text().splitlines();n=len(text)
 assert n==25 and all(len(s)==n and set(s)<={'0','1'} for s in text)
 A=[sum((ch=='1')<<j for j,ch in enumerate(s)) for s in text]
 assert all(not(a>>i&1) and a.bit_count()==12 for i,a in enumerate(A))
 for i,j in combinations(range(n),2):
  assert (A[i]>>j&1)==(A[j]>>i&1)
  assert (A[i]&A[j]).bit_count()==(5 if A[i]>>j&1 else 6)
 # Invariant seed = numbers of K4 and K5 containing a vertex.
 seeds=[]
 for v in range(n):
  ns=list(bits(A[v]))
  seeds.append(tuple(sum(all(A[a]>>b&1 for a,b in combinations(C,2)) for C in combinations(ns,k)) for k in (3,4)))
 def colors(keys):
  ids={x:i for i,x in enumerate(sorted(set(keys)))}
  return [ids[x] for x in keys]
 col=colors(seeds);refinements=[col]
 while len(set(col))<n:
  nxt=colors([(col[v],tuple(sorted(col[w] for w in bits(A[v])))) for v in range(n)])
  assert len(set(nxt))>len(set(col)), 'Not an asymmetry certificate'
  refinements.append(nxt);col=nxt
 # Any automorphism preserves seeds and each refinement; 25 singleton colours => identity.
 cocliques=[]
 for C in combinations(range(n),5):
  if any(A[a]>>b&1 for a,b in combinations(C,2)):continue
  mask=sum(1<<a for a in C)
  assert all((A[i]&mask).bit_count()+3*int(i in C)==3 for i in range(n))
  cocliques.append(list(C))
 assert len(cocliques)==3
 result={'parameters':[25,12,5,6],'srg_verified':True,'automorphism_group_order':1,
         'invariant_seed':'numbers of K4 and K5 through the vertex','seed_values':seeds,
         'refinement_colours':refinements,'refinement_class_counts':[len(set(c)) for c in refinements],
         'hoffman_cocliques':cocliques,'hoffman_identity':'(A+3I)x=3*1','full_five_subset_census':53130}
 (OUT/'paley_counterexample_verified.json').write_text(json.dumps(result,indent=2))
 print('SRG(25,12,5,6) verified; Aut=1 by invariant refinement:',result['refinement_class_counts'])
 print('Exactly three Hoffman cocliques:',cocliques)
 return result
if __name__=='__main__':verify()
