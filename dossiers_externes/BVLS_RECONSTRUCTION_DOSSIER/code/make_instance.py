from pathlib import Path
import argparse,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('--anchor',default='0,1,2');p.add_argument('--release',default='');p.add_argument('--graph',default='bvls.npy');a=p.parse_args()
G=np.load(ROOT/'data'/a.graph);v=len(G);k=int(G.sum(0)[0]);anchor=[int(x) for x in a.anchor.split(',') if x];release=[int(x) for x in a.release.split(',') if x]
fixed=list(map(int,sorted(set(anchor).union(*[set(np.flatnonzero(G[x])) for x in anchor])-set(release))));free=sorted(set(range(v))-set(fixed));Y=G[np.ix_(fixed,free)];C=G[np.ix_(fixed,fixed)];D=G[np.ix_(free,free)]
R=2-Y-C@Y;d=k-Y.sum(0)
assert np.array_equal(Y@D,R)
with (ROOT/'data'/f'{a.name}.inst').open('w') as f:
 f.write(f'{len(fixed)} {len(free)}\n');f.write('\n'.join(' '.join(map(str,row)) for row in Y)+'\n')
 for i in range(len(free)):f.write(str(d[i])+' '+' '.join(map(str,R[:,i]))+'\n')
(ROOT/'data'/f'{a.name}.json').write_text(json.dumps({'graph':a.graph,'fixed':fixed,'free':free,'anchor':anchor,'release':release}))
print(a.name,'fixed',len(fixed),'free',len(free),'Rrange',R.min(),R.max(), 'degrees',dict(zip(*np.unique(d,return_counts=True))));print('first fixed',fixed[:30])
