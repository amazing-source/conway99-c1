"""Fast integer checks of the packaged constructions, domains, and explicit transports.
This validates witnesses and finite obstructions. Completeness is reproduced by reproduce.py.
"""
from pathlib import Path
import itertools,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
def read_adj(p):
 A=[[int(c) for c in line.strip()] for line in p.read_text().splitlines() if line.strip()];n=len(A)
 assert all(len(r)==n for r in A) and all(A[i][i]==0 for i in range(n));assert all(A[i][j]==A[j][i] for i in range(n) for j in range(n));return A
def edges(p,n=243):
 A=[[0]*n for _ in range(n)]
 for l in p.read_text().splitlines():
  u,v=map(int,l.split());assert 0<=u<v<n and not A[u][v];A[u][v]=A[v][u]=1
 return A
def srg(A,k):
 n=len(A);nb=[{j for j,x in enumerate(r) if x} for r in A];assert all(len(s)==k for s in nb)
 for i in range(n):
  for j in range(i):assert len(nb[i]&nb[j])==2-A[i][j],(i,j)
 return nb
A=edges(ROOT/'data/bvls.edges');B=edges(ROOT/'data/twin.edges');srg(A,22);srg(B,22)
meta=json.loads((ROOT/'data/prism2.json').read_text());F=meta['free'];S=meta['fixed'];R=[]
for i in range(len(F)):
 R.append([sum(1<<int(j) for j in line.split()) for line in (ROOT/'data'/f'prism2_{i}.rows').read_text().splitlines()])
# Each raw domain element satisfies its defining equations, including the pair ceiling.
Y=[[A[x][y] for y in F] for x in S];Z=[[sum(A[z][x]*A[z][y] for z in S) for y in F] for x in F]
for i,x in enumerate(F):
 assert len(R[i])==len(set(R[i]))
 for mask in R[i]:
  cols=[j for j in range(len(F)) if (mask>>j)&1];assert i not in cols and len(cols)==22-sum(A[s][x] for s in S)
  for a,s in enumerate(S):assert sum(Y[a][j] for j in cols)==2-A[s][x]-sum(A[s][t]*A[t][x] for t in S)
  assert all(Z[j][k]<=1 for j,k in itertools.combinations(cols,2))
rep=json.loads((ROOT/'reports/prism2_certificate.json').read_text());i=rep['anchor_index'];eliminated=set()
for ob in rep['pair_obstructions']:
 a,j=ob['candidate'],ob['incompatible_row'];r=R[i][a];e=(r>>j)&1
 assert not any(((s>>i)&1)==e and (r&s).bit_count()+Z[i][j]==2-e for s in R[j]);eliminated.add(a)
assert eliminated.isdisjoint(rep['anchor_survivors']) and eliminated|set(rep['anchor_survivors'])==set(range(len(R[i])))
for j,res in enumerate(rep['canonical_solutions']):
 H=read_adj(ROOT/'data/prism2_canonical'/f'{j}.adj');srg(H,22);ref=A if res['class']=='BvLS' else B;perm=res['permutation_to_reference'];assert sorted(perm)==list(range(243));assert all(H[u][v]==ref[perm[u]][perm[v]] for u in range(243) for v in range(243));assert all(H[x]==A[x] for x in S)
 tau=res['order3_automorphism']
 assert sorted(tau)==list(range(243))
 assert all(tau[u]!=u and tau[tau[tau[u]]]==u for u in range(243))
 assert all(H[u][v]==H[tau[u]][tau[v]] for u in range(243) for v in range(243))
# Check all exhibited affine transports without trusting their discovery routine.
pts=list(itertools.product(range(3),repeat=5));idx={p:i for i,p in enumerate(pts)};conn={pts[j] for j in range(243) if A[0][j]}
def mp(M,x):return tuple(sum(M[a][b]*x[b] for b in range(5))%3 for a in range(5))
def perm_of(r):
 M=r['M'];t=r['t'];assert {mp(M,x) for x in conn}==conn;p=[idx[tuple((z+t[a])%3 for a,z in enumerate(mp(M,x)))] for x in pts];assert len(set(p))==243;return p
cov=json.loads((ROOT/'reports/coverage.json').read_text());comps=cov['prisms_at_T'];U=comps[0]+comps[1];images=set()
for r in cov['two_prism_transports']:
 p=perm_of(r);assert {p[x] for x in [0,1,2]}=={0,1,2};im=tuple(sorted(p[x] for x in U));assert list(im)==r['target'];images.add(im)
assert images=={tuple(sorted(a+b)) for a,b in itertools.combinations(comps,2)} and len(images)==45
Ts=set()
for r in cov['triangle_transports']:
 p=perm_of(r);im=tuple(sorted(p[x] for x in [0,1,2]));assert list(im)==r['target'] and all(A[x][y] for x,y in itertools.combinations(im,2));Ts.add(im)
assert len(Ts)==891
assert len(R[i])==28 and len(eliminated)==26
print('OK: integer SRG checks, all packaged row-domain entries, 26 pair-obstruction certificates, explicit isomorphisms and order-three automorphisms, 891 triangle transports and 45 prism-pair transports.')
print('Completeness of the row domains and search: run reproduce.py; this script does not infer completeness merely from stored data.')
