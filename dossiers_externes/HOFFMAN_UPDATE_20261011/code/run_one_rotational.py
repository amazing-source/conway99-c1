from pathlib import Path
import json,subprocess,time,itertools
from run_designs import comp
R=Path(__file__).resolve().parents[1]
def main():
 ds=json.loads((R/'data/one_rotational_designs22.json').read_text())['designs'];summary=[];start=time.time()
 for k,d in enumerate(ds):
  stem=f'frob{k}';blocks=d['blocks']
  Y=[[int(s in B) for B in blocks] for s in range(22)]
  text='22 77\n'+'\n'.join(' '.join(map(str,r)) for r in Y)+'\n'
  text+='\n'.join('10 '+' '.join(str(2-Y[s][i]) for s in range(22)) for i in range(77))+'\n'
  (R/'data'/f'{stem}.inst').write_text(text)
  p=subprocess.run([str(R/'rows22'),str(R/'data'/f'{stem}.inst'),str(R/'data'/stem),'5','1000000'],capture_output=True,text=True,check=True)
  (R/'reports'/f'{stem}.rows.log').write_text(p.stdout)
  lines=[s.split() for s in p.stdout.splitlines()];assert len(lines)==77 and all(s[3]=='EXHAUSTED' for s in lines)
  dom=[[sum(1<<int(j) for j in s.split()) for s in (R/'data'/f'{stem}_{i}.rows').read_text().splitlines()] for i in range(77)]
  assert all(len(dom[i])==int(lines[i][1]) for i in range(77))
  for i in range(77):
   for x in dom[i]:
    ns=[j for j in range(77) if x>>j&1]
    assert len(ns)==10 and i not in ns
    assert all(sum(int(s in blocks[j]) for j in ns)==2-int(s in blocks[i]) for s in range(22))
    assert all(len(set(blocks[j])&set(blocks[i]))<=1 for j in ns)
    assert all(len(set(blocks[a])&set(blocks[b]))<=1 for a,b in itertools.combinations(ns,2))
  dead,alive,deletions=comp(dom,blocks)
  item={'design':k,'family':'C7:C3 one-rotational','candidate_counts':[len(x) for x in dom],'dead_arc_consistency':dead,'remaining_counts':[len(x) for x in alive],
        'deletions':deletions,'row_enum_nodes':sum(int(s[2]) for s in lines),'seconds':sum(float(s[4]) for s in lines)}
  (R/'reports'/f'{stem}.certificate.json').write_text(json.dumps(item))
  print(k,'domain sizes',min(map(len,dom)),max(map(len,dom)),'AC-DEAD',dead,'deletions',len(deletions),flush=True)
  summary.append({a:b for a,b in item.items() if a not in ['deletions','candidate_counts','remaining_counts']})
 (R/'reports/one_rotational_summary.json').write_text(json.dumps({'items':summary,'elapsed':time.time()-start},indent=2))
 print('TOTAL',len(ds),'closed',sum(x['dead_arc_consistency'] for x in summary),'elapsed',time.time()-start,flush=True)
if __name__=='__main__':main()
