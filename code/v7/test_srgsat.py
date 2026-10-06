"""Positive/negative controls for srgsat."""
import itertools, time, random
import numpy as np
from srgsat import SRGCompletion, check_srg, TRUE, FALSE

def paley9():
    F=[(a,b) for a in range(3) for b in range(3)]
    A=np.zeros((9,9),dtype=int)
    for i,(a,b) in enumerate(F):
        for j,(c,d) in enumerate(F):
            if i!=j and (a==c or b==d): A[i,j]=1
    return A
def petersen():
    V=list(itertools.combinations(range(5),2)); n=len(V)
    A=np.zeros((n,n),dtype=int)
    for i in range(n):
        for j in range(n):
            if not set(V[i])&set(V[j]): A[i,j]=1
    return A
def bvls243():
    # BvLS: Cayley graph on F3^5 with connection set = 22 weight-? words: use the standard ternary Golay dual construction
    # Fallback: build from the ternary Golay code via coset graph (Berlekamp-van Lint-Seidel graph)
    G=np.array([[1,0,0,0,0,0,1,1,1,1,1],[0,1,0,0,0,0,0,1,2,2,1],[0,0,1,0,0,0,1,0,1,2,2],
                [0,0,0,1,0,0,2,1,0,1,2],[0,0,0,0,1,0,2,2,1,0,1],[0,0,0,0,0,1,1,2,2,1,0]])
    import itertools
    code=set()
    for coef in itertools.product(range(3),repeat=6):
        code.add(tuple((np.array(coef)@G)%3))
    # cosets of the [11,6] code in F3^11: 3^5=243 ; adjacency: differ by weight-1 vector
    reps={}; cos=[]
    def key(v):
        return min(tuple((np.array(v)+np.array(c))%3) for c in [()]) 
    # coset id via syndrome with parity-check H
    from numpy.linalg import matrix_rank
    # parity check: solve H G^T = 0 mod 3 by brute force basis of dual
    dual=[w for w in itertools.product(range(3),repeat=11) if all(sum(a*b for a,b in zip(w,g))%3==0 for g in G)]
    # pick 5 independent dual vectors
    H=[]
    for w in dual:
        if not any(w): continue
        Ht=H+[w]
        M=np.array(Ht)
        # rank mod 3 check by brute: count span size
        span=set()
        for coef in itertools.product(range(3),repeat=len(Ht)):
            span.add(tuple((np.array(coef)@M)%3))
        if len(span)==3**len(Ht): H=Ht
        if len(H)==5: break
    H=np.array(H)
    synd=lambda v: tuple((H@np.array(v))%3)
    allsy=sorted(set(tuple(s) for s in itertools.product(range(3),repeat=5)))
    idx={s:i for i,s in enumerate(allsy)}
    unit=[]
    for p in range(11):
        for a in (1,2):
            e=[0]*11; e[p]=a; unit.append(synd(e))
    A=np.zeros((243,243),dtype=int)
    for s in allsy:
        for u in unit:
            t=tuple((np.array(s)+np.array(u))%3)
            A[idx[s],idx[t]]=1
    return A

def run(A,n,k,lam,mu,nfix,seed=0,label=""):
    rng=random.Random(seed)
    fixed={}
    verts=list(range(nfix))
    for i in verts:
        for j in range(n):
            if j!=i: fixed[(min(i,j),max(i,j))]=int(A[i,j])
    S=SRGCompletion(n,k,lam,mu,fixed); S.add_degrees(); S.add_common()
    t=time.time(); res,model=S.solve(time_limit=120)
    ok=check_srg(S.decode(model),n,k,lam,mu) if res else None
    print(label,"vars",S.pool.top,"clauses",len(S.cnf.clauses),"res",res,"srg",ok,"t",round(time.time()-t,2))

P=paley9(); assert check_srg(P,9,4,1,2)
run(P,9,4,1,2,0,label="paley9 free")
run(P,9,4,1,2,1,label="paley9 seed1")
Pe=petersen(); assert check_srg(Pe,10,3,0,1)
run(Pe,10,3,0,1,0,label="petersen free")
# negative control: srg(10,3,0,1) with a triangle forced (lam=0) -> UNSAT
S=SRGCompletion(10,3,0,1,{(0,1):1,(0,2):1,(1,2):1}); S.add_degrees(); S.add_common()
print("petersen+triangle (expect False):",S.solve(60)[0])
# negative: srg(9,4,1,2) but with mu=1 (no such graph: srg(9,4,1,1) violates k(k-l-1)=(n-k-1)mu: 4*2=8 vs 4*1) -> UNSAT
S=SRGCompletion(9,4,1,1,{}); S.add_degrees(); S.add_common()
print("srg(9,4,1,1) (expect False):",S.solve(60)[0])
B=bvls243(); print("bvls is srg(243,22,1,2):",check_srg(B,243,22,1,2))
# BvLS partial-mask completion: fix all pairs except those inside a random 40-vertex set W (free), expect SAT and srg
rng=random.Random(3); W=set(rng.sample(range(243),40))
fixed={}
for i in range(243):
    for j in range(i+1,243):
        if not (i in W and j in W): fixed[(i,j)]=int(B[i,j])
S=SRGCompletion(243,22,1,2,fixed); S.add_degrees()
S.add_common([(i,j) for i in range(243) for j in range(i+1,243) if i in W or j in W])
t=time.time(); res,model=S.solve(300)
print("bvls mask40: vars",S.pool.top,"clauses",len(S.cnf.clauses),"res",res,"srg",check_srg(S.decode(model),243,22,1,2) if res else None,"t",round(time.time()-t,1))
