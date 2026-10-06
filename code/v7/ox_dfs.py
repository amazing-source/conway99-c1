"""Randomised DFS sampler of O_x configurations (see ox_sample.py for the constraint list), + class test on seed."""
import json, sys, random, itertools, time
import numpy as np
from bstage import gen_columns, target_matrix, pdeg, P13, T
from seedcvp import class_min_violation
from ox_sample import seed_matrix, lam_mu_ok
LAB = T + P13

def run(core, holes, nsamp, seed, maxnodes=200000):
    A=np.array(core['adj']); M=target_matrix(A)
    cols=gen_columns(A,set(tuple(p) for p in core['defect']))
    cand={1:[],0:[]}
    for b,q in cols:
        if b[0]!=0: continue
        p13=[v for v in b if v in P13]
        if sum(1 for v in p13 if v not in holes)>pdeg(0,q): continue
        cand[q].append(frozenset(b[1:]))
    demand={l:int(M[0,l]) for l in LAB}
    paircap={(l,l2):int(M[l,l2]) for l,l2 in itertools.combinations(LAB,2)}
    slots=[1]*6+[0]*4
    rng=random.Random(seed)
    found=[]
    for it in range(nsamp):
        nodes=[0]
        chosen=[]
        rem=dict(demand); pu={}
        def ok(b):
            for l in b:
                if rem[l]<=0: return False
            for l,l2 in itertools.combinations(sorted(b),2):
                if pu.get((l,l2),0)+1>paircap[(l,l2)]: return False
            for c in chosen:
                if len(b & c)>=2: return False
            return True
        def apply(b,s):
            for l in b: rem[l]-=s
            for l,l2 in itertools.combinations(sorted(b),2): pu[(l,l2)]=pu.get((l,l2),0)+s
        def matching_exists(bs):
            # 4 Zx (6..9) each matched to a distinct Bx (0..5) with disjoint labels, remaining 2 Bx disjoint
            Z=[6,7,8,9]
            for perm in itertools.permutations(range(6),4):
                if all(not (bs[z] & bs[p]) for z,p in zip(Z,perm)):
                    rest=[i for i in range(6) if i not in perm]
                    if not (bs[rest[0]] & bs[rest[1]]):
                        return [(p,z) for z,p in zip(Z,perm)]+[tuple(rest)]
            return None
        res=[None]
        def dfs(s):
            nodes[0]+=1
            if nodes[0]>maxnodes: return True
            if s==10:
                if all(v==0 for v in rem.values()):
                    mt=matching_exists(chosen)
                    if mt: res[0]=(list(chosen),mt); return True
                return False
            # remaining capacity check
            opts=[b for b in cand[slots[s]] if ok(b)]
            rng.shuffle(opts)
            for b in opts[:40]:
                apply(b,1); chosen.append(b)
                if dfs(s+1): return True
                chosen.pop(); apply(b,-1)
            return False
        dfs(0)
        if res[0]:
            found.append(res[0])
    return found

if __name__=="__main__":
    cores=json.load(open('cores27.json'))
    k=int(sys.argv[1]); holes=[int(v) for v in sys.argv[2].split(',')]; ns=int(sys.argv[3]); sd=int(sys.argv[4])
    t=time.time(); F=run(cores[k],holes,ns,sd)
    st={'killed':0,'alive':0,'lammu_bad':0}; kinds={}
    for bs,mt in F:
        bsl=[tuple([0]+sorted(b)) for b in bs]
        S,q=seed_matrix(cores[k],holes,bsl,mt)
        if not lam_mu_ok(S): st['lammu_bad']+=1; continue
        bad=class_min_violation(S,q)
        if bad: st['killed']+=1; kinds[bad[0]]=kinds.get(bad[0],0)+1
        else: st['alive']+=1
    print('found',len(F),'of',ns,st,kinds,round(time.time()-t,1))
