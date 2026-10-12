"""Integer square certificates for any induced border of SRG(99,14,1,2).

K=12I+2J-A_B-A_B^2 must equal D D^T for the missing incidence matrix D.
For integer z and k, each missing column has integer c=z.column and
(c-k)(c-k-1)>=0. Thus z.K.z >= (2k+1) z.d - (99-|B|) k(k+1).
Floating eigenvectors only suggest z; all certificates use exact integers.
"""
from pathlib import Path
import argparse
import json
import numpy as np


def matrix(w):
    n=w['vertices'];A=np.zeros((n,n),dtype=np.int64)
    for u,v in w['edges']:A[u,v]=A[v,u]=1
    K=12*np.eye(n,dtype=np.int64)+2*np.ones((n,n),dtype=np.int64)-A-A@A
    return K,np.diag(K).copy()


def evaluate(w,cut):
    K,d=matrix(w);z=np.zeros(len(d),dtype=np.int64)
    for u,value in cut['weights']:z[u]=value
    q=int(z@K@z);total=int(z@d);k=cut['integer_level'];outside=99-len(d)
    required=(2*k+1)*total-outside*k*(k+1)
    return dict(quadratic=q,sum_loads=total,integer_level=k,lower_bound=required,gap=required-q,violated=q<required)


def discover(w,limit=4):
    K,d=matrix(w);n=len(d);outside=99-n
    eigenvalues,vectors=np.linalg.eigh(K.astype(float));found=[];seen=set()
    def score(z):
        total=int(z@d);level=total//outside
        return int(z@K@z)-(2*level+1)*total+outside*level*(level+1)
    for column in range(min(len(d),12)):
        v=vectors[:,column];v=v/max(abs(v))
        for scale in (1,2,3,4,6,8,12):
            z=np.rint(scale*v).astype(np.int64)
            if score(z)<0:break
        else:continue
        while True:
            options=[]
            for u in np.flatnonzero(z):
                zz=z.copy();zz[u]=0;q=score(zz)
                if q<0:options.append((q,int(u),zz))
            if not options:break
            z=min(options,key=lambda item:(item[0],item[1]))[2]
        while True:
            options=[]
            for u in np.flatnonzero(abs(z)>1):
                zz=z.copy();zz[u]-=int(np.sign(z[u]));q=score(zz)
                if q<0:options.append((q,int(u),zz))
            if not options:break
            z=min(options,key=lambda item:(item[0],item[1]))[2]
        if z[np.flatnonzero(z)[0]]<0:z=-z
        signature=tuple(map(int,z))
        if signature in seen:continue
        seen.add(signature)
        cut=dict(kind='integer_residual_square',weights=[[int(u),int(z[u])] for u in np.flatnonzero(z)],
                 integer_level=int(z@d)//outside,
                 law='Sum over missing vertices of (weighted incidence-k)(weighted incidence-k-1) is nonnegative')
        cut['separation']=evaluate(w,cut);assert cut['separation']['violated'];found.append(cut)
        if len(found)>=limit:break
    return found


def install(master,cut):
    n=master.ctx['n'];weights=cut['weights']
    if any(u>=n for u,value in weights):return False
    d=lambda u:14-master.ctx['degree'][u]
    q=sum(value*value*d(u) for u,value in weights)
    for index,(u,a) in enumerate(weights):
        for v,b in weights[index+1:]:
            i,j=sorted((u,v))
            q+=2*a*b*(2-master.edge(i,j)-master.ctx['common'][i,j])
    total=sum(value*d(u) for u,value in weights);k=cut['integer_level']
    master.model.Add(q>=(2*k+1)*total-(99-n)*k*(k+1))
    master.installed.append(cut);return True


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path)
    args=ap.parse_args();w=json.loads(args.source.read_text());cuts=discover(w)
    for c in cuts:c['source']=str(args.source)
    args.output.write_text(json.dumps(cuts,indent=2)+'\n');print(json.dumps(cuts))
