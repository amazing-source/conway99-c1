"""Independent checks of the finite exclusion.
(1) Check every design, every candidate, every logged logical deletion.
(2) Re-enumerate representative row domains with a separate binary-search C++ code.
(3) Transport those domains by explicit DESIGN automorphisms to every other row.
No automorphism of a completed graph is assumed in step (3).
"""
from pathlib import Path
import itertools,json,subprocess,time,argparse
from collections import Counter
R=Path(__file__).resolve().parents[1]
import os
OUT=Path(os.environ.get('HOFFMAN_OUTPUT_DIR',str(R/'reports')))
OUT.mkdir(parents=True,exist_ok=True)

def read_domains(stem):
 out=[]
 for i in range(77):
  lines=(R/'data'/f'{stem}_{i}.rows').read_text().splitlines()
  rows=[tuple(map(int,l.split())) for l in lines]
  assert all(tuple(sorted(set(r)))==r for r in rows)
  assert len(set(rows))==len(rows)
  out.append(rows)
 return out

def verify_one(stem,entry,perms,recheck=True):
 B=[tuple(x) for x in entry['blocks']];sets=list(map(set,B));ix={x:i for i,x in enumerate(B)}
 assert len(B)==len(ix)==77
 assert Counter(x for b in B for x in b)==Counter({i:14 for i in range(22)})
 assert Counter(x for b in B for x in itertools.combinations(b,2))==Counter({x:2 for x in itertools.combinations(range(22),2)})
 N=[[len(b&c) for c in sets] for b in sets]
 assert all(N[i][j]<=2 for i in range(77) for j in range(i))
 domains=read_domains(stem);domainsets=[set(x) for x in domains]
 for i,rows in enumerate(domains):
  for ns in rows:
   assert len(ns)==10 and i not in ns
   assert all(sum(p in sets[j] for j in ns)==2-int(p in sets[i]) for p in range(22))
   assert all(N[i][j]<=1 for j in ns)
   assert all(N[j][k]<=1 for j,k in itertools.combinations(ns,2))
 # independent enumeration of one target from each orbit, then exact domain transport
 done=set();comparisons=0;commands=[]
 for target in range(77):
  if target in done:continue
  if recheck:
   output=OUT/f'{stem}_independent_{target}.rows'
   p=subprocess.run([str(R/'rows22_independent'),str(R/'data'/f'{stem}.inst'),str(output),str(target),'30'],capture_output=True,text=True,check=True)
   assert 'EXHAUSTED' in p.stdout and 'STOPPED' not in p.stdout
   recomputed={tuple(map(int,l.split())) for l in output.read_text().splitlines()}
   assert recomputed==domainsets[target],(stem,target,len(recomputed),len(domainsets[target]))
   commands.append(p.stdout.strip());output.unlink()
  for perm in perms:
   bp=[ix[tuple(sorted(perm[p] for p in block))] for block in B]
   assert len(set(bp))==77
   j=bp[target]
   transformed={tuple(sorted(bp[k] for k in ns)) for ns in domains[target]}
   assert transformed==domainsets[j],(stem,target,j,'transport mismatch')
   done.add(j);comparisons+=1
 assert len(done)==77
 # Independently replay deletion certificate using direct neighbour-set intersections.
 cert=json.loads((R/'reports'/f'{stem}.certificate.json').read_text())
 assert cert['candidate_counts']==list(map(len,domains))
 assert cert['dead_arc_consistency']
 alive=[set(range(len(rows))) for rows in domains]
 ds=[[set(row) for row in rows] for rows in domains]
 for i,a,j in cert['deletions']:
  assert i!=j and a in alive[i]
  ri=ds[i][a]
  for b in alive[j]:
   rj=ds[j][b];edge=int(j in ri)
   compatible=(edge==int(i in rj) and len(ri&rj)+N[i][j]==2-edge)
   assert not compatible,(stem,i,a,j,b)
  alive[i].remove(a)
 assert any(not row for row in alive),(stem,'no empty domain')
 assert list(map(len,alive))==cert['remaining_counts']
 return {'stem':stem,'independent_row_searches':commands,'domain_transport_checks':comparisons,'candidate_rows':sum(map(len,domains)),
         'deletions_checked':len(cert['deletions']),'empty_row':[i for i,a in enumerate(alive) if not a]}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--family',choices=['cyclic','one_rotational','all'],default='all');ap.add_argument('--no-reenumeration',action='store_true')
 args=ap.parse_args();start=time.time();result=[]
 if args.family in ('cyclic','all'):
  perms=[[(i+t)%22 for i in range(22)] for t in range(22)]
  ds=json.loads((R/'data/cyclic_designs22.json').read_text())['designs']
  for k,d in enumerate(ds):
   result.append(verify_one(f'cyc{k}',d,perms,not args.no_reenumeration));print('cyclic',k,'verified',flush=True)
 if args.family in ('one_rotational','all'):
  from one_rotational_designs import P
  ds=json.loads((R/'data/one_rotational_designs22.json').read_text())['designs']
  for k,d in enumerate(ds):
   result.append(verify_one(f'frob{k}',d,P,not args.no_reenumeration));print('one_rotational',k,'verified',flush=True)
 summary={'family':args.family,'independent_reenumeration':not args.no_reenumeration,'verified_designs':len(result),
          'verified_candidate_rows':sum(x['candidate_rows'] for x in result),'deletions':sum(x['deletions_checked'] for x in result),
          'independent_row_search_count':sum(len(x['independent_row_searches']) for x in result),'elapsed_seconds':time.time()-start,'details':result}
 (OUT/f'verification_{args.family}.json').write_text(json.dumps(summary,indent=2));print('VERIFIED',len(result),'in',time.time()-start,flush=True)
if __name__=='__main__':main()
