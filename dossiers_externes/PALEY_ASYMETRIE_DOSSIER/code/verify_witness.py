"""Verify the reconstructed asymmetric SRG and two elementary asymmetry certificates.
No third-party package, network connection or SAT solver is used.
"""
from pathlib import Path
from itertools import combinations, permutations
from collections import Counter
import json
ROOT=Path(__file__).resolve().parents[1]
def require(ok,message):
    if not ok:raise ValueError(message)
def read_adj(path):
    lines=Path(path).read_text().splitlines();n=len(lines)
    require(n>0 and all(len(r)==n and set(r)<={"0","1"} for r in lines),"invalid binary matrix")
    return [sum((c=="1")<<j for j,c in enumerate(r))for r in lines]
def check_srg(A,k,lam,mu):
    n=len(A);require(all(not(A[i]>>i&1)for i in range(n)),"loop")
    require(all(A[i].bit_count()==k for i in range(n)),"incorrect degree")
    for i,j in combinations(range(n),2):
        a=A[i]>>j&1;require(a==(A[j]>>i&1),"asymmetric matrix")
        require((A[i]&A[j]).bit_count()==(lam if a else mu),f"common-neighbour mismatch {i},{j}")
def field_paley25():
    sq={( (a*a+2*b*b)%5, (2*a*b)%5)for a in range(5)for b in range(5)if (a,b)!=(0,0)}
    require(len(sq)==12,"bad finite field")
    coords=[((r-c)%5,(r+c)%5)for r in range(5)for c in range(5)]
    return [sum(( ((a-c)%5,(b-d)%5) in sq)<<j for j,(c,d)in enumerate(coords))for a,b in coords]
def cliques(A,k):
    return [tuple(c)for c in combinations(range(len(A)),k)
            if all(A[u]>>v&1 for u,v in combinations(c,2))]
def rank_keys(keys):
    order={x:i for i,x in enumerate(sorted(set(keys)))}
    return [order[x]for x in keys]
def colour_certificate(A):
    n=len(A);nb=[[j for j in range(n)if A[i]>>j&1]for i in range(n)];seed=[]
    for v in range(n):
        seed.append(tuple(sum(all(A[a]>>b&1 for a,b in combinations(T,2))
                          for T in combinations(nb[v],k))for k in(3,4)))
    col=rank_keys(seed);out=[col]
    while True:
        nxt=rank_keys([(col[v],tuple(sorted(col[w]for w in nb[v])))for v in range(n)])
        if len(set(nxt))==len(set(col)):break
        out.append(nxt);col=nxt
    return {"seeds":[list(x)for x in seed],"colours":out,"n_colours":[len(set(c))for c in out]}
def cross_components(A,X,Y):
    U=set(X)|set(Y);nb={u:{v for v in U if ((u in X)!=(v in X))and A[u]>>v&1}for u in U}
    require(all(len(s)==2 for s in nb.values()),"cross graph is not 2-regular")
    sizes=[]
    while U:
        stack=[next(iter(U))];comp=set(stack)
        while stack:
            for v in nb[stack.pop()]-comp:comp.add(v);stack.append(v)
        sizes.append(len(comp));U-=comp
    return sorted(sizes)
def check_core_certificate(A,cert):
    cs=[list(c)for c in cliques(A,5)]
    X,Y,Z=cert["cliques_ordered"]
    require(sorted(map(sorted,cs))==sorted(map(sorted,[X,Y,Z])),"not exactly the three recorded K5")
    require(len(set(X+Y+Z))==15,"K5 not disjoint")
    require(cross_components(A,X,Y)==[10] and cross_components(A,X,Z)==[10]
            and cross_components(A,Y,Z)==[4,6],"wrong intrinsic ordering of the three cliques")
    U=sorted(X+Y+Z);R=sorted(set(range(25))-set(U))
    xset=set(X)
    prof=lambda v:frozenset(x for x in X if A[v]>>x&1)
    automorphisms=[]
    # X is the unique clique meeting each of the other two in a cross-C10.
    # Once X is permuted, images in Y and Z are determined by their two neighbours in X.
    for destY,destZ in [(Y,Z),(Z,Y)]:
        lookupY={prof(v):v for v in destY};lookupZ={prof(v):v for v in destZ}
        require(len(lookupY)==len(lookupZ)==5,"non-distinct cross-C10 profiles")
        for im in permutations(X):
            p=dict(zip(X,im));ok=True
            for domain,lookup in [(Y,lookupY),(Z,lookupZ)]:
                for v in domain:
                    q=frozenset(p[x]for x in prof(v))
                    if q not in lookup:ok=False;break
                    p[v]=lookup[q]
                if not ok:break
            if ok and all((A[u]>>v&1)==(A[p[u]]>>p[v]&1)for u,v in combinations(U,2)):
                automorphisms.append(p)
    require(len(automorphisms)==2,"core automorphism count not two")
    recorded=[{int(k):v for k,v in p.items()}for p in cert["core_automorphisms"]]
    require({tuple(p[u]for u in U)for p in recorded}=={tuple(p[u]for u in U)for p in automorphisms},"core certificate mismatch")
    profiles={v:frozenset(u for u in U if A[v]>>u&1)for v in R}
    require(len(set(profiles.values()))==10,"external profiles not injective")
    surviving=[]
    for p in automorphisms:
        if all(frozenset(p[u]for u in pr)in profiles.values()for pr in profiles.values()):
            surviving.append(p)
    require(len(surviving)==1 and all(surviving[0][u]==u for u in U),"nontrivial core action survives")
    # All full automorphisms preserve the set of all K5s, hence U.
    # The only possible action on U is identity; distinct profiles force identity on R.
    return True
def main():
    P=read_adj(ROOT/"data/paley25.adj");A=read_adj(ROOT/"data/paley25_to_asymmetric.adj")
    require(P==field_paley25(),"initial graph is not the specified Paley graph")
    check_srg(P,12,5,6);check_srg(A,12,5,6)
    cert=json.loads((ROOT/"certificats/explicit_transformation.json").read_text())
    removed=[[i,j]for i,j in combinations(range(25),2)if P[i]>>j&1 and not(A[i]>>j&1)]
    added=[[i,j]for i,j in combinations(range(25),2)if A[i]>>j&1 and not(P[i]>>j&1)]
    require(removed==cert["removed_edges"] and added==cert["added_edges"],"edge-change certificate mismatch")
    require(len(removed)==len(added)==37,"unexpected surgery size")
    require(all(A[v]==P[v]for v in cert["fixed_clique"]),"changed fixed boundary")
    colours=colour_certificate(A)
    require(colours==cert["asymmetry_certificate"],"colour certificate mismatch")
    require(colours["n_colours"][-1]==25,"colours do not certify asymmetry")
    check_core_certificate(A,json.loads((ROOT/"certificats/asymmetry_core_certificate.json").read_text()))
    print("Paley(25), independently constructed over F_25: OK")
    print("Reconstructed graph: SRG(25,12,5,6), all 300 pairs exact")
    print("37 edges removed + 37 added; fixed K5 and all its incidences unchanged")
    print("Asymmetry proof 1, intrinsic colour refinement:",colours["n_colours"])
    print("Asymmetry proof 2: two core automorphisms; one killed by the attachment profiles")
    print("Aut(reconstructed graph) = {identity}")
if __name__=="__main__":main()
