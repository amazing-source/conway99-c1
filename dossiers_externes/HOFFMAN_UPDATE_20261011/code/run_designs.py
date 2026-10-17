from pathlib import Path
import subprocess,json,time,itertools
R=Path(__file__).resolve().parents[1]
def comp(dom,blocks):
 """Arc consistency with compact integer bitsets; each deletion gets a reason."""
 n=len(dom); Z=[[len(set(b)&set(c)) for c in blocks] for b in blocks]
 alive=[(1<<len(d))-1 for d in dom]; support={}
 for i in range(n):
  for j in range(i+1,n):
   sd=[]; rev=[0]*len(dom[j])
   for ix,x in enumerate(dom[i]):
    ns=0;a=(x>>j)&1
    for iy,y in enumerate(dom[j]):
     if a != ((y>>i)&1):continue
     if (x&y).bit_count() + Z[i][j] != 2-a:continue
     ns|=1<<iy;rev[iy]|=1<<ix
    sd.append(ns)
   support[i,j]=sd;support[j,i]=rev
 def materialize():
  return [{a for a in range(len(dom[i])) if alive[i]>>a&1} for i in range(n)]
 deletions=[];change=True
 while change:
  change=False
  for i in range(n):
   todo=alive[i]
   while todo:
    bit=todo&-todo;todo-=bit;ix=bit.bit_length()-1
    for j in range(n):
     if i==j:continue
     if not (support[i,j][ix]&alive[j]):
      deletions.append([i,ix,j]);alive[i]^=bit;change=True;break
   if not alive[i]:return True,materialize(),deletions
 return False,materialize(),deletions

def main():
 ds=json.loads((R/'data/cyclic_designs22.json').read_text())['designs'];summary=[];start=time.time()
 for k,d in enumerate(ds):
  Y=[[int(s in B) for B in d['blocks']] for s in range(22)]
  text='22 77\n'+'\n'.join(' '.join(map(str,r)) for r in Y)+'\n'
  text+='\n'.join('10 '+' '.join(str(2-Y[s][i]) for s in range(22)) for i in range(77))+'\n'
  (R/'data'/f'cyc{k}.inst').write_text(text)
  p=subprocess.run([str(R/'rows22'),str(R/'data'/f'cyc{k}.inst'),str(R/'data'/f'cyc{k}'),'5','1000000'],capture_output=True,text=True,check=True)
  (R/'reports'/f'cyc{k}.rows.log').write_text(p.stdout)
  lines=[s.split() for s in p.stdout.splitlines()];assert len(lines)==77 and all(s[3]=='EXHAUSTED' for s in lines)
  dom=[[sum(1<<int(j) for j in s.split()) for s in (R/'data'/f'cyc{k}_{i}.rows').read_text().splitlines()] for i in range(77)]
  assert all(len(dom[i])==int(lines[i][1]) for i in range(77))
  for i in range(77):
   for x in dom[i]:
    ns=[j for j in range(77) if x>>j&1]
    assert len(ns)==10 and i not in ns
    assert all(sum(int(s in d['blocks'][j]) for j in ns)==2-int(s in d['blocks'][i]) for s in range(22))
    assert all(len(set(d['blocks'][j])&set(d['blocks'][i]))<=1 for j in ns)
    assert all(len(set(d['blocks'][a])&set(d['blocks'][b]))<=1 for a,b in itertools.combinations(ns,2))
  dead,alive,deletions=comp(dom,d['blocks'])
  item={'design':k,'candidate_counts':[len(x) for x in dom],'dead_arc_consistency':dead,'remaining_counts':[len(x) for x in alive],
        'deletions':deletions,'row_enum_nodes':sum(int(s[2]) for s in lines),'seconds':sum(float(s[4]) for s in lines)}
  (R/'reports'/f'cyc{k}.certificate.json').write_text(json.dumps(item))
  print(k,'domain sizes',min(map(len,dom)),max(map(len,dom)),'AC-DEAD',dead,'deletions',len(deletions),flush=True)
  summary.append({a:b for a,b in item.items() if a not in ['deletions','candidate_counts','remaining_counts']})
 (R/'reports/cyclic_summary.json').write_text(json.dumps({'items':summary,'elapsed':time.time()-start},indent=2))
 print('TOTAL',len(ds),'closed',sum(x['dead_arc_consistency'] for x in summary),'elapsed',time.time()-start,flush=True)
if __name__=='__main__':main()
