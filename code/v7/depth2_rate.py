import json, sys, random, time, numpy as np
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
demand=np.array([int(M[0,l]) if l>=8 else 0 for l in range(27)])
rng=random.Random(7)
def build(pairs):
    n=27+2*len(pairs); S=np.zeros((n,n),dtype=np.int64); S[:27,:27]=A
    for i,(b1,b2) in enumerate(pairs):
        u,w=27+2*i,28+2*i
        for v in b1: S[u,v]=S[v,u]=1
        for v in b2: S[w,v]=S[v,w]=1
        S[u,w]=S[w,u]=1
    return S
def test(pairs):
    S=build(pairs)
    used=np.zeros(27,dtype=int)
    for p in pairs:
        for b in p:
            for v in b[1:]: used[v]+=1
    if (used>demand).any(): return 'demand'
    C=S@S; lim=np.where(S==1,1,2); np.fill_diagonal(lim,99)
    if not (C<=lim).all(): return 'lammu'
    bad=class_min_violation(S,qcore+[1,0]*len(pairs))
    return str(bad[0]) if bad else 'alive'
def randpair():
    while True:
        b1=rng.choice(cand[1]); b2=rng.choice(cand[0])
        if not set(b1[1:])&set(b2[1:]): return (b1,b2)
alive1=[]
while len(alive1)<60:
    p=randpair()
    if test([p])=='alive': alive1.append(p)
st={}; t=time.time()
for it in range(ns):
    p1=rng.choice(alive1); p2=randpair()
    r=test([p1,p2]); st[r]=st.get(r,0)+1
print('depth2',st,round(time.time()-t,1))
alive2=[]
tries=0
while len(alive2)<30 and tries<200000:
    tries+=1
    p1=rng.choice(alive1); p2=randpair()
    if test([p1,p2])=='alive': alive2.append([p1,p2])
print('collected alive2',len(alive2),'tries',tries)
st={}
for it in range(ns):
    ps=rng.choice(alive2); p3=randpair()
    r=test(ps+[p3]); st[r]=st.get(r,0)+1
print('depth3',st)
