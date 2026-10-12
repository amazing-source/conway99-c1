"""Check all archived reconstruction witnesses and their isomorphism maps.
Pure Python, standard library only. This checks witnesses and counts, not the
exhaustiveness of the C++ search: rerun reproduce.py for that.
"""
from pathlib import Path
import json
from collections import Counter
from itertools import combinations
from verify_witness import read_adj, check_srg, require, field_paley25
ROOT=Path(__file__).resolve().parents[1]

def read_graph6(line):
    data=line.strip()
    if data.startswith(">>graph6<<"):
        data=data[10:]
    require(data and ord(data[0])-63<63,"Only short graph6 is used in this dataset")
    n=ord(data[0])-63
    bits=[(ord(c)-63>>shift)&1 for c in data[1:]for shift in range(5,-1,-1)]
    require(len(bits)>=n*(n-1)//2,"Truncated graph6")
    A=[0]*n;i=0
    for v in range(1,n):
        for u in range(v):
            if bits[i]:
                A[u]|=1<<v;A[v]|=1<<u
            i+=1
    return A

def main():
    P=read_adj(ROOT/"data/paley25.adj")
    require(P==field_paley25(),"Reference is not Paley")
    graphs=[read_graph6(x)for x in (ROOT/"data/sr251256.g6").read_text().splitlines()if x.strip()]
    require(len(graphs)==15,"Not the 15-entry dataset")
    for A in graphs:
        require(len(A)==25,"Wrong order")
        check_srg(A,12,5,6)
    S={4,8,12,16,20};F=sorted(set(range(25))-S)
    baseline=[P[u] if u in S else sum((P[u]>>v&1)<<v for v in S)for u in range(25)]
    records=json.loads((ROOT/"resultats/all_completions_classified.json").read_text())
    raw=(ROOT/"resultats/paley25_anchor5.search").read_text().splitlines()
    require(raw[-1].startswith("END EXHAUSTED "),"Archived search is not labelled exhausted")
    sol=[tuple(map(int,l.split()[1:]))for l in raw[:-1]if l.startswith("SOL ")]
    require(len(sol)==len(records)==3983,"Archive length mismatch")
    counts=Counter();seen=set()
    for rec,entry in zip(records,sol):
        rows=rec["rows"];weight=rec["weight"]
        require((weight,*rows)==entry,"Record differs from raw row output")
        require(tuple(rows)not in seen,"Duplicate leaf")
        seen.add(tuple(rows))
        A=baseline.copy()
        require(len(rows)==20 and all(0<=r<1<<20 for r in rows),"Bad free row")
        for i,u in enumerate(F):
            A[u]|=sum((rows[i]>>j&1)<<v for j,v in enumerate(F))
        check_srg(A,12,5,6)
        p=rec["isomorphism_to_catalogue"];idx=rec["catalogue_id"]
        require(sorted(p)==list(range(25))and 1<=idx<=15,"Not a bijective catalogue map")
        B=graphs[idx-1]
        require(all((A[u]>>v&1)==(B[p[u]]>>p[v]&1)for u,v in combinations(range(25),2)),
                "Invalid graph isomorphism")
        require(weight>0 and weight&(weight-1)==0,"Unexpected symmetry weight")
        counts[idx]+=weight
    require(len(counts)==15 and sum(counts.values())==1999872,"Incorrect class/label count")
    expected=json.loads((ROOT/"resultats/catalogue_counts.json").read_text())
    for rec in expected:
        require(counts[rec["catalogue_id"]]==rec["enumerated_labelled_one_clique"],
                "Count differs from independent table")
    print("15 catalogue matrices satisfy every SRG equation.")
    print("3983 reconstructed representatives and their full isomorphism maps: checked.")
    print("Weighted labelled total: 1999872; all 15 isomorphism classes represented.")
    print("Exhaustiveness is supplied by the separately reproducible exact search, not inferred from this file.")
if __name__=="__main__":
    main()
