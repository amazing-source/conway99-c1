"""Paley and an asymmetric SRG can have exactly the SAME Hoffman boundary.
Complement the explicit clique-boundary reconstruction from the Paley dossier.
Pure Python; no isomorphism package or matrix approximations.
"""
from pathlib import Path
from itertools import combinations
import json
from verify_paley_counterexample import verify as verify_asym
R=Path(__file__).resolve().parents[1]
import os
OUT=Path(os.environ.get('HOFFMAN_OUTPUT_DIR',str(R/'reports')))
OUT.mkdir(parents=True,exist_ok=True)
def read(f):
 rows=(R/'data'/f).read_text().splitlines()
 assert len(rows)==25 and all(len(r)==25 and set(r)<={'0','1'} for r in rows)
 return [[int(x) for x in r] for r in rows]
def check(A):
 assert all(A[i][i]==0 and sum(A[i])==12 for i in range(25))
 for i,j in combinations(range(25),2):
  assert A[i][j]==A[j][i]
  assert sum(A[i][k]*A[j][k] for k in range(25))==6-A[i][j]
def main():
 verify_asym();P=read('paley25.adj');H=read('paley_asymmetric25.adj')
 PC=read('paley25_complement.adj');HC=read('paley_asymmetric25_complement.adj')
 # Check original P directly as a finite-field Paley graph, F5[t]/(t^2-2).
 sq={((a*a+2*b*b)%5,2*a*b%5) for a in range(5) for b in range(5) if (a,b)!=(0,0)}
 coord=[((r-c)%5,(r+c)%5) for r in range(5) for c in range(5)]
 assert all(P[i][j]==int(((a-c)%5,(b-d)%5) in sq) for i,(a,b) in enumerate(coord) for j,(c,d) in enumerate(coord))
 # A nonsquare multiplication gives an explicit isomorphism P -> its complement.
 ns=next((a,b) for a in range(5) for b in range(5) if (a,b)!=(0,0) and (a,b) not in sq)
 ix={x:i for i,x in enumerate(coord)};a,b=ns
 perm=[ix[((a*c+2*b*d)%5,(a*d+b*c)%5)] for c,d in coord]
 assert all(P[i][j]==PC[perm[i]][perm[j]] for i in range(25) for j in range(25))
 for A,AC in [(P,PC),(H,HC)]:
  assert all(AC[i][j]==(0 if i==j else 1-A[i][j]) for i in range(25) for j in range(25))
  check(A);check(AC)
 S=json.loads((R/'reports/paley_original_transformation.json').read_text())['fixed_clique']
 assert all(PC[i]==HC[i] for i in S)
 for A in (PC,HC):
  assert all(not A[i][j] for i in S for j in S)
  assert all(sum(A[i][j] for j in S)+3*int(i in S)==3 for i in range(25))
 F=sorted(set(range(25))-set(S))
 blocks=[tuple(i for i in S if PC[i][j]) for j in F]
 assert all(len(b)==3 for b in blocks)
 assert all(sum(i in b and j in b for b in blocks)==6 for i,j in combinations(S,2))
 out={'fixed_hoffman_coclique':S,'outside_vertices':F,'identical_hoffman_blocks':blocks,
      'design_parameters':[2,5,3,6],'original_paley_isomorphism_to_complement':perm,
      'removed_edges':[(i,j) for i,j in combinations(range(25),2) if PC[i][j] and not HC[i][j]],
      'added_edges':[(i,j) for i,j in combinations(range(25),2) if HC[i][j] and not PC[i][j]],
      'asymmetry_proof':'complementation preserves the entire automorphism group; H checked by singleton invariant colours',
      'all_claims_checked':True}
 assert len(out['removed_edges'])==len(out['added_edges'])==37
 (OUT/'same_hoffman_boundary_verified.json').write_text(json.dumps(out,indent=2))
 print('Identical Hoffman coclique AND entire boundary incidence: verified')
 print('Source is isomorphic to Paley; target is asymmetric: verified')
if __name__=='__main__':main()
