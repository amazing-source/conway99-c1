import json, sys, random, time, itertools, numpy as np
from bstage import gen_columns, target_matrix, pdeg, P13
from seedcvp import class_min_violation
cores=json.load(open('cores27.json'))
k=int(sys.argv[1]); holes=[int(v) for v in sys.argv[2].split(',')]; ns=int(sys.argv[3])
core=cores[k]; A=np.array(core['adj']); M=target_matrix(A)
cols=gen_columns(A,set(tuple(p) for p in core['defect']))
cand={1:[],0:[]}
for b,q in cols:
    if b[0]!=0: continue
    if sum(1 for v in b if v in P13 and v not in holes)>pdeg(0,q): continue
    cand[q].append(tuple(b))
qcore=[-1,-1,1,1,1,1,1,1]+[0]*6+[0 if v in holes else 1 for v in P13]
rng=random.Random(5); st={}
t=time.time(); n=0
while n<ns:
    b1=rng.choice(cand[1]); b2=rng.choice(cand[0])
    if set(b1[1:])&set(b2[1:]): continue
    S=np.zeros((29,29),dtype=np.int64); S[:27,:27]=A
    for v in b1: S[27,v]=S[v,27]=1
    for v in b2: S[28,v]=S[v,28]=1
    S[27,28]=S[28,27]=1
    C=S@S; lim=np.where(S==1,1,2); np.fill_diagonal(lim,99)
    if not (C<=lim).all(): key='lammu'
    else:
        bad=class_min_violation(S,qcore+[1,0])
        key=str(bad[0]) if bad else 'alive'
    st[key]=st.get(key,0)+1; n+=1
print(st, round(time.time()-t,1))
