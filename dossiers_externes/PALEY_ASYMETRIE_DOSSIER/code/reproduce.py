"""Reproduce the Paley boundary reconstruction and, optionally, all auxiliary tests.

Requirements: Python 3.10+, NetworkX and a C++17 compiler (g++).
No network, LLM, SAT library, cloud service, or target graph is used by the constructor.
Catalogue graphs are read only AFTER the constructor has finished.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess
import time

from common import ROOT, catalogue, identify, all_aut, verify_srg, gm_switch
import networkx as nx


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def run(command: list[str], text: str | None = None, timeout: float = 120) -> str:
    ans = subprocess.run(command, input=text, text=True, capture_output=True, timeout=timeout)
    if ans.returncode:
        raise RuntimeError(f"Command failed ({ans.returncode}): {command}\n{ans.stderr}")
    return ans.stdout


def compile_program(name: str, out: Path, compiler: str) -> str:
    executable = out / name
    run([compiler, "-O3", "-std=c++17", str(ROOT/"code"/f"{name}.cpp"),
         "-o", str(executable)])
    return str(executable)


def paley25() -> nx.Graph:
    # Explicit Paley model over F25, alpha^2=2:
    # (r,c) -> (r-c) + (r+c)*alpha. Its adjacency is exactly the following.
    G = nx.empty_graph(25)
    for u,v in combinations(range(25),2):
        r,c = divmod(u,5)
        s,d = divmod(v,5)
        if r == s or c == d or (r+c-s-d) % 5 == 0:
            G.add_edge(u,v)
    verify_srg(G)
    return G


def boundary_input(G: nx.Graph, S: list[int], parameters: tuple[int,int,int,int]) -> str:
    n,k,lam,mu = parameters
    S = sorted(S)
    require(set(G) == set(range(n)), "Unexpected labels")
    # NO original F-F adjacency survives in the constructor's input.
    masks = [
        sum(1 << v for v in G[u] if u in S or v in S)
        for u in range(n)
    ]
    return f"{n} {k} {lam} {mu} {len(S)}\n" + " ".join(map(str,masks)) + "\n" + \
           " ".join(map(str,S)) + "\n"


def parse_search(raw: str, f: int) -> tuple[list[tuple[int,list[int]]], str]:
    lines=raw.splitlines()
    require(bool(lines) and lines[-1].startswith("END EXHAUSTED "), "Incomplete search; NOT a census")
    solutions=[]
    for line in lines[:-1]:
        a=line.split()
        require(len(a) == f+2 and a[0] == "SOL", "Malformed search output")
        weight=int(a[1]); masks=list(map(int,a[2:]))
        require(weight>0, "Invalid multiplicity")
        solutions.append((weight,masks))
    return solutions,lines[-1]


def construct(G: nx.Graph, S: list[int], masks: list[int]) -> nx.Graph:
    F=sorted(set(G)-set(S))
    H=nx.Graph()
    H.add_nodes_from(G)
    H.add_edges_from((u,v) for u,v in G.edges if u in S or v in S)
    for i,j in combinations(range(len(F)),2):
        require((masks[i]>>j&1)==(masks[j]>>i&1), "Nonsymmetric row selection")
        if masks[i]>>j&1:
            H.add_edge(F[i],F[j])
    return H


def search_case(G, S, parameters, name, generator, search, out):
    text=boundary_input(G,S,parameters)
    (out/f"{name}.input").write_text(text)
    domains=run([generator],text)
    (out/f"{name}.domains").write_text(domains)
    raw=run([search,"1000000","30","10000000","3"],domains,timeout=60)
    (out/f"{name}.search").write_text(raw)
    sol,last=parse_search(raw,len(G)-len(S))
    return domains,sol,last


def clique_spreads(G):
    cs=[tuple(c) for c in nx.find_cliques(G) if len(c)==5]
    byv={v:[c for c in cs if v in c] for v in G}
    def recurse(left):
        if not left:
            return 1
        v=min(left)
        return sum(recurse(left-set(c)) for c in byv[v] if set(c)<=left)
    return recurse(set(G))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",type=Path,default=ROOT/"runs"/"replay")
    ap.add_argument("--extra",action="store_true",help="GM census, fixed-boundary ladder and minimum surgery")
    ap.add_argument("--cxx",default="g++")
    args=ap.parse_args()
    require(shutil.which(args.cxx) is not None, f"Compiler not found: {args.cxx}")
    out=args.out.resolve()
    require(not out.exists(),f"Output already exists: {out}. Choose a new --out directory.")
    out.mkdir(parents=True)
    generator=compile_program("boundary_domains",out,args.cxx)
    search=compile_program("boundary_search",out,args.cxx)

    P=paley25(); S=[4,8,12,16,20]
    t0=time.perf_counter()
    domains,sol,last=search_case(P,S,(25,12,5,6),"paley25",generator,search,out)
    print(last,flush=True)
    # Constructor is finished. Only now consult known examples for classification.
    gs=catalogue()
    classified=[]; weighted=Counter(); leaf_counts=Counter(); first={}
    for weight,rows in sol:
        H=construct(P,S,rows); verify_srg(H)
        idx,mapping=identify(H,gs)
        weighted[idx]+=weight; leaf_counts[idx]+=1
        classified.append({"catalogue_id":idx,"rows":rows,
                           "isomorphism_to_catalogue":[mapping[v] for v in range(25)],
                           "weight":weight})
        if idx not in first:
            first[idx]=H
            nx.write_graph6(H,out/f"class_{idx}.g6",header=False)
    (out/"all_completions_classified.json").write_text(json.dumps(classified,indent=2)+"\n")
    require(set(weighted)==set(range(1,16)), "Did not recover exactly the 15 catalogue classes")
    inventory=[]
    for idx,G in enumerate(gs,1):
        ac=len(all_aut(G))
        c5=sum(1 for c in nx.find_cliques(G) if len(c)==5)
        expected=c5*120*1024//ac
        require(expected==weighted[idx], f"Independent labelled-count check failed for graph {idx}")
        inventory.append({"catalogue_id":idx,"aut_order":ac,"K5":c5,
                          "labelled_completions":weighted[idx],
                          "representative_leaves":leaf_counts[idx],
                          "five_clique_partitions":clique_spreads(G)})
    require(sum(weighted.values())==1999872,"Total count mismatch")
    (out/"catalogue_counts.json").write_text(json.dumps(inventory,indent=2)+"\n")
    print("All 15 classes recovered; asymmetric classes:",
          [x["catalogue_id"] for x in inventory if x["aut_order"]==1],flush=True)
    print("Labelled completions:",sum(weighted.values()),flush=True)

    Q=nx.empty_graph(9)
    Q.add_edges_from((u,v) for u,v in combinations(range(9),2)
                    if u//3==v//3 or u%3==v%3)
    _,sol9,last9=search_case(Q,[0,1,2],(9,4,1,2),"paley9",generator,search,out)
    for _,rows in sol9:
        H=construct(Q,[0,1,2],rows)
        verify_srg(H,(9,4,1,2))
        require(nx.is_isomorphic(H,Q),"Paley(9) control changed isomorphism class")
    require(sum(w for w,_ in sol9)==4,"Paley9 labelled count mismatch")
    print(last9,flush=True)

    extra={}
    if args.extra:
        # Each row means this PARTICULAR nested boundary, not every boundary of its size.
        ladder=[]
        for j in range(1,6):
            Sj=sorted(S+[3,7,11,15,24][:j])
            _,leaves,ending=search_case(P,Sj,(25,12,5,6),f"boundary_{5+j}",generator,search,out)
            classes=set()
            for _,rows in leaves:
                H=construct(P,Sj,rows);verify_srg(H);classes.add(identify(H,gs)[0])
            ladder.append({"fixed":Sj,"classes":sorted(classes),
                           "labelled":sum(w for w,_ in leaves),"status":ending})
        extra["boundary_ladder"]=ladder

        gm=compile_program("gm_scan",out,args.cxx)
        transition=nx.Graph(); all_sets={}; gm_result={}
        for idx,G in enumerate(gs,1):
            txt="25\n"+" ".join(str(sum(1<<v for v in G[u])) for u in range(25))+"\n"
            raw=run([gm],txt)
            (out/f"gm_{idx}.txt").write_text(raw)
            sets=[tuple(map(int,line.split()[1:]))for line in raw.splitlines()if line.startswith("SET ")]
            counts=Counter()
            for size,mask in sets:
                H=gm_switch(G,[v for v in range(25)if mask>>v&1])
                target,_=identify(H,gs);counts[size,target]+=1
                transition.add_edge(idx,target)
            all_sets[idx]=sets
            gm_result[idx]=[{"size":a,"target":b,"count":v}for(a,b),v in sorted(counts.items())]
        extra["gm_components"]=[sorted(c)for c in nx.connected_components(transition)]
        extra["gm_transitions"]=gm_result
        require(set(transition.neighbors(2))=={2},"Paley standard GM-isolation check failed")

        closest=compile_program("closest_asymmetric",out,args.cxx)
        F=sorted(set(P)-set(S))
        twins=[]
        for i,u in enumerate(F):
            cl=[j for j,v in enumerate(F) if (set(P[u])&set(S))==(set(P[v])&set(S))]
            if len(cl)==2 and cl[0]==i:
                twins.append(cl)
        asym_ids={r["catalogue_id"]for r in inventory if r["aut_order"]==1}
        candidates=[r for r in classified if r["catalogue_id"]in asym_ids]
        text=f"20 {len(twins)}\n"+"\n".join(" ".join(map(str,t))for t in twins)+"\n"
        text+=" ".join(str(sum(int(P.has_edge(u,v))<<j for j,v in enumerate(F)))for u in F)+"\n"
        text+=str(len(candidates))+"\n"
        text+="\n".join(str(r["catalogue_id"])+" "+" ".join(map(str,r["rows"]))for r in candidates)+"\n"
        (out/"minimum_surgery.input").write_text(text)
        ans=run([closest],text)
        (out/"minimum_surgery.txt").write_text(ans)
        require(int(ans.splitlines()[0].split()[1])==74,"Minimum surgery differs from 74 toggles")
        extra["minimum_edge_toggles_fixed_boundary"]=74
        (out/"extra_results.json").write_text(json.dumps(extra,indent=2)+"\n")
        print("Additional tests:",extra.get("gm_components"),"minimum edge toggles 74",flush=True)
    summary={"status":"EXHAUSTED","classes":15,"asymmetric_classes":2,
             "labelled_completions":sum(weighted.values()),"search":last,"control9":last9,
             "construction_used_target_catalogue":False,
             "elapsed_including_classification_seconds":time.perf_counter()-t0}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))


if __name__=="__main__":
    main()
