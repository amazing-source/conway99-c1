import json, sys, numpy as np
from fractions import Fraction
import sympy as sp
from bstage import gen_columns, target_matrix
cores=json.load(open('cores27.json'))
for k in [0,5,10,14,21]:
    A=np.array(cores[k]['adj'])
    K=sp.Matrix(27*np.eye(27,dtype=int)-9*A+1)
    Kp=K.pinv()  # exact rational pseudo-inverse
    cols=gen_columns(A,set(tuple(p) for p in cores[k]['defect']))
    seen={}
    for b,q in cols:
        if b in seen: continue
        kv=sp.Matrix([1-9*(1 if i in b else 0) for i in range(27)])
        s=28-(kv.T*Kp*kv)[0]
        seen[b]=s
    vals=sorted(set(seen.values()))
    neg=sum(1 for v in seen.values() if v<0)
    print(k,'distinct b',len(seen),'Schur<0:',neg,'values',[str(v) for v in vals][:12])
