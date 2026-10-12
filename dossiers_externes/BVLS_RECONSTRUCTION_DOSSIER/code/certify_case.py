from pathlib import Path
import numpy as np,json,itertools,collections,sys
ROOT=Path(__file__).resolve().parents[1];name=sys.argv[1];meta=json.loads((ROOT/'data'/f'{name}.json').read_text());A=np.load(ROOT/'data'/meta['graph']);S=meta['fixed'];F=meta['free'];U=meta['release'];n=len(F)
rows=[]
for i in range(n):rows.append([sum(1<<int(j) for j in s.split()) for s in (ROOT/'data'/f'{name}_{i}.rows').read_text().splitlines()])
Y=A[np.ix_(S,F)];C=A[np.ix_(S,S)];R=2-Y-C@Y;Z=Y.T@Y;d=22-Y.sum(0)
for i,ls in enumerate(rows):
 for m in ls:
  assert m.bit_count()==d[i] and not (m>>i)&1
  b=np.array([(m>>j)&1 for j in range(n)],dtype=int);assert np.array_equal(Y@b,R[:,i])
refs={'BvLS':np.load(ROOT/'data/bvls.npy'),'twin':np.load(ROOT/'data/twin.npy'),'Gamma3':np.load(ROOT/'data/gamma3.npy')}
res=[];dest=ROOT/'data'/f'{name}_canonical';dest.mkdir(exist_ok=True)
if (ROOT/'data'/f'{name}.sol').exists():sols=[(int(s.split()[0]),list(map(int,s.split()[1:]))) for s in (ROOT/'data'/f'{name}.sol').read_text().splitlines()]
else:sols=[]
for k,(weight,ds) in enumerate(sols):
 H=A.copy()
 for i,x in enumerate(F):H[x,F]=[(rows[i][ds[i]]>>j)&1 for j in range(n)]
 assert np.array_equal(H,H.T) and not H.diagonal().any() and np.all(H.sum(0)==22)
 assert np.array_equal(H@H+H,20*np.eye(243,dtype=int)+2*np.ones((243,243),dtype=int))
 outside=[v for v in range(243) if v not in U];iso=None
 for label,X in refs.items():
  if not np.array_equal(H[np.ix_(outside,outside)],X[np.ix_(outside,outside)]):continue
  perm=list(range(243));ok=True
  for u in U:
   matches=[v for v in U if np.array_equal(H[u,outside],X[v,outside])]
   if len(matches)!=1:ok=False;break
   perm[u]=matches[0]
  if ok and len(set(perm))==243 and np.array_equal(H,X[np.ix_(perm,perm)]):iso=(label,perm);break
 assert iso, 'NOT MATCHED TO REFERENCES'
 (dest/f'{k}.adj').write_text('\n'.join(''.join(map(str,row)) for row in H)+'\n')
 rho=[3*(v//3)+(v%3+1)%3 for v in range(243)]
 inv=[0]*243
 for u,v in enumerate(iso[1]):inv[v]=u
 tau=[inv[rho[iso[1][u]]] for u in range(243)]
 assert all(tau[u]!=u and tau[tau[tau[u]]]==u for u in range(243))
 assert np.array_equal(H,H[np.ix_(tau,tau)])
 res.append({'order3_automorphism':tau,'weight':weight,'class':iso[0],'permutation_to_reference':iso[1],'changed_edges':int(np.count_nonzero(H-A)//2)})
print('Verified leaves and explicit isomorphisms',[(x['class'],x['weight'],x['changed_edges']) for x in res],flush=True)
root=min(range(n),key=lambda i:len(rows[i]));bad=[];survive=[]
for a,r in enumerate(rows[root]):
 witness=None
 for j in range(n):
  if j==root:continue
  e=(r>>j)&1;need=2-e-int(Z[root,j]);
  if not any(((s>>root)&1)==e and (r&s).bit_count()==need for s in rows[j]):witness=j;break
 if witness is None:survive.append(a)
 else:bad.append({'candidate':a,'incompatible_row':witness})
print('Anchor',root,'global',F[root],'domains',len(rows[root]),'pair certificates',len(bad),'survive',survive,flush=True)
report={'case':name,'canonical_solutions':res,'total_labelled':sum(x['weight'] for x in res),'anchor_index':root,'anchor_vertex':F[root],'pair_obstructions':bad,'anchor_survivors':survive}
(ROOT/'reports'/f'{name}_certificate.json').write_text(json.dumps(report,indent=2))
