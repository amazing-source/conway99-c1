"""BvLS reconstructed from the exact ternary Golay generator in source golay.py."""
from pathlib import Path
import itertools, hashlib, json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
G=np.array([[1,0,0,0,0,0,1,1,1,1,1],[0,1,0,0,0,0,0,1,2,2,1],[0,0,1,0,0,0,1,0,1,2,2],[0,0,0,1,0,0,2,1,0,1,2],[0,0,0,0,1,0,2,2,1,0,1],[0,0,0,0,0,1,1,2,2,1,0]],dtype=np.int64)
dual=sorted(tuple(np.r_[(-G[:,6:]@np.array(t))%3,t]) for t in itertools.product(range(3),repeat=5))
H=[]; span={(0,)*11}
for w in dual:
 if w not in span:
  H.append(w)
  span={tuple((np.array(c)@np.array(H))%3) for c in itertools.product(range(3),repeat=len(H))}
 if len(H)==5:break
H=np.array(H);pts=list(itertools.product(range(3),repeat=5));idx={p:i for i,p in enumerate(pts)}
A=np.zeros((243,243),dtype=np.int64)
for i,p in enumerate(pts):
 for h in H.T:
  for e in (1,2):A[i,idx[tuple((np.array(p)+e*h)%3)]]=1
assert np.array_equal(A,A.T) and not np.diag(A).any() and np.all(A.sum(axis=1)==22)
assert np.array_equal(A@A+A,20*np.eye(243,dtype=int)+2*np.ones((243,243),dtype=int))
b=''.join(f'{i} {j}\n' for i in range(243) for j in range(i+1,243) if A[i,j]).encode()
blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert blob=='cfc398cea8d6d75905f1db06f264607abd9c2b68',(blob,'coordinate mismatch')
(ROOT/'data/bvls.edges').write_bytes(b);np.save(ROOT/'data/bvls.npy',A)
(ROOT/'data/golay_basis.json').write_text(json.dumps(H.tolist()))
print('Verified all 29403 pairs; exact Git blob',blob)
