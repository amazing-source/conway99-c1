import json, itertools, time, numpy as np
from seedcvp import class_min_violation
cores=json.load(open('cores27.json')); orbits=json.load(open('core_orbits.json'))
P13=list(range(14,27)); res={}; t=time.time(); surv={}
for k,core in enumerate(cores):
    cols=core['columns']; A=np.array(core['adj'])
    st={}; alive=[]
    for H in itertools.combinations(range(13),4):
        if not all(4-sum(1 for c in cols if t_ in c)+sum(1 for i in H if t_ in cols[i])>=0 for t_ in range(6)):
            st['t-equation']=st.get('t-equation',0)+1; continue
        holes=[14+i for i in H]
        q=[-1,-1,1,1,1,1,1,1]+[0]*6+[0 if v in holes else 1 for v in P13]
        bad=class_min_violation(A,q)
        key=str(bad[0]) if bad else 'alive'
        st[key]=st.get(key,0)+1
        if not bad: alive.append(holes)
    res[k]=st; surv[k]=alive
    print(k,st,round(time.time()-t,1),flush=True)
json.dump({'stats':res,'survivors':surv},open('core_full_sweep.json','w'))
tot={}
for st in res.values():
    for kk,v in st.items(): tot[kk]=tot.get(kk,0)+v
print('TOTAL',tot)
print('orbit representatives survivors:',sum(len(surv[o[0]]) for o in orbits))
