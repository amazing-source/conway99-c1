"""Positive control for both row enumerators: the 3x3 grid with a Hoffman coclique.
No arbitrary graph automorphisms are imposed. Exhaustive assembly has four
labelled completions of the same boundary, all checked from the SRG definition.
"""
from pathlib import Path
from itertools import product,combinations
import subprocess,tempfile,json
R=Path(__file__).resolve().parents[1]
import os
OUT=Path(os.environ.get('HOFFMAN_OUTPUT_DIR',str(R/'reports')))
OUT.mkdir(parents=True,exist_ok=True)
def main():
 A=[[int(i!=j and (i//3==j//3 or i%3==j%3)) for j in range(9)] for i in range(9)]
 S=[0,4,8];F=[i for i in range(9) if i not in S];Y=[[A[s][v] for v in F] for s in S]
 with tempfile.TemporaryDirectory() as td:
  t=Path(td);inst=t/'grid9.inst'
  text='3 6\n'+'\n'.join(' '.join(map(str,row)) for row in Y)+'\n'
  text+='\n'.join('2 '+' '.join(str(2-Y[p][i]) for p in range(3)) for i in range(6))+'\n'
  inst.write_text(text)
  p=subprocess.run([str(R/'rows22'),str(inst),str(t/'r'),'30','10000'],capture_output=True,text=True,check=True)
  assert 'STOPPED' not in p.stdout
  domains=[]
  for i in range(6):
   rows=[tuple(map(int,s.split())) for s in (t/f'r_{i}.rows').read_text().splitlines()]
   q=subprocess.run([str(R/'rows22_independent'),str(inst),str(t/'ind.rows'),str(i),'30'],capture_output=True,text=True,check=True)
   assert 'STOPPED' not in q.stdout
   assert set(rows)=={tuple(map(int,s.split())) for s in (t/'ind.rows').read_text().splitlines()}
   assert tuple(j for j,v in enumerate(F) if A[F[i]][v]) in rows
   domains.append(rows)
  count=0
  for selected in product(*domains):
   if any((j in selected[i])!=(i in selected[j]) for i,j in combinations(range(6),2)):continue
   B=[row[:] for row in A]
   for i in range(6):
    for j in range(6):B[F[i]][F[j]]=int(j in selected[i])
   if not all(sum(B[i][k]*B[j][k] for k in range(9))==2-B[i][j] for i,j in combinations(range(9),2)):continue
   assert all(sum(row)==4 for row in B)
   count+=1
  assert count==4
  out={'parameters':[9,4,1,2],'row_domain_sizes':list(map(len,domains)),'true_rows_present':True,
       'enumerators_agree':True,'complete_labelled_srg_completions':count}
 (OUT/'positive_control.json').write_text(json.dumps(out,indent=2));print(out)
if __name__=='__main__':main()
