"""Study where lambda-one SRGs lose the symmetries of a rooted star.

Input graphs and their SRG parameters are accepted from the research corpus;
this is not an independent group or parameter audit of the peer's graphs.

For a root x, let F be its non-neighbors. Keep yz in E(G[F]) precisely when
the unique triangle containing yz has its third point in N(x). This graph
T_x is mu-regular. Indeed, each a in N(x) intersect N(y) pairs y with the
third vertex z of its triangle with a. That z is in F, and distinct a give
distinct z. T_x is triangle-free by uniqueness of edge triangles.
For mu=2 it is a union of cycles of length at least four.

Isomorphism invariants of T_x are intrinsic root colors of the ORIGINAL G.
Refining these colors along G-neighborhoods can expose asymmetry beyond
the identical immediate matching neighborhoods. We do not compute Aut(G).
Optional rooted skeletons retain star edges and T_x edges only; their group
orders measure residual local freedoms, not the full graph group.
"""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

import igraph as ig
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/codex_asymmetry_mechanisms_20261014'


def read_graph(path):
    edges=[tuple(map(int,line.split())) for line in path.read_text().splitlines() if line.strip()]
    n=1+max(max(e) for e in edges)
    adj=[set() for _ in range(n)]
    for a,b in edges:
        adj[a].add(b);adj[b].add(a)
    return adj


def triangle_table(adj):
    third={}
    for a,neighbors in enumerate(adj):
        for b in neighbors:
            if a<b:
                common=adj[a]&adj[b]
                # This is the definition domain of the derived object.
                assert len(common)==1
                c=next(iter(common))
                third[a,b]=third[b,a]=c
    return third


def transport(adj,third,x,mu):
    F=sorted(set(range(len(adj)))-adj[x]-{x})
    h={v:set() for v in F}
    for a in adj[x]:
        for y in adj[a]:
            if y in h:
                z=third[a,y]
                assert z in h
                h[y].add(z)
    assert all(len(ns)==mu for ns in h.values())
    assert all(y in h[z] for y,ns in h.items() for z in ns)
    return h


def cycles(h):
    remaining=set(h); sizes=[]
    while remaining:
        v=min(remaining); component={v}; stack=[v];remaining.remove(v)
        while stack:
            for w in h[stack.pop()]&remaining:
                remaining.remove(w);component.add(w);stack.append(w)
        sizes.append(len(component))
    assert min(sizes)>=4
    return tuple(sorted(sizes))


def square_signature(h):
    common=Counter()
    for ns in h.values():
        common.update(itertools.combinations(sorted(ns),2))
    squares_at=Counter({v:0 for v in h})
    for (a,b),c in common.items():
        if c>1:
            squares_at[a]+=c*(c-1)//2
            squares_at[b]+=c*(c-1)//2
    # Each 4-cycle has exactly one vertex opposite a specified vertex,
    # so this already counts cycles through each vertex once.
    return tuple(sorted(Counter(squares_at.values()).items()))


def compress(signatures):
    labels={s:i for i,s in enumerate(sorted(set(signatures)))}
    return [labels[s] for s in signatures]


def refine(adj,initial):
    colors=compress(initial); counts=[len(set(colors))]
    while True:
        new=compress([(colors[v],tuple(sorted(colors[w] for w in adj[v]))) for v in range(len(adj))])
        if len(set(new))==len(set(colors)):
            return colors,counts
        colors=new;counts.append(len(set(colors)))


def skeleton(adj,h,x):
    R=adj[x]|{x}
    edges={(a,b) for a in R for b in adj[a] if a<b}
    edges|={(b,a) for a in R for b in adj[a] if b<a}
    edges|={(a,b) for a in h for b in h[a] if a<b}
    return ig.Graph(n=len(adj),edges=sorted(edges))


def study(name,path,mu):
    start=time.monotonic(); adj=read_graph(path); third=triangle_table(adj)
    signatures=[]; roots=[]
    for x in range(len(adj)):
        h=transport(adj,third,x,mu)
        sig=cycles(h) if mu==2 else square_signature(h)
        signatures.append(sig)
    colors,rounds=refine(adj,signatures)
    counts=Counter(colors)
    # One root per *intrinsic color*, not an assertion of vertex-orbit equality.
    # Only groups of newly constructed skeletons are computed.
    for c in sorted(counts):
        x=colors.index(c); h=transport(adj,third,x,mu)
        order=skeleton(adj,h,x).count_automorphisms(color=[int(v==x) for v in range(len(adj))])
        roots.append({'color':c,'root':x,'class_size':counts[c],
                      'rooted_skeleton_group_order':order,
                      'transport_signature':signatures[x]})
    result={'name':name,'source':str(path.relative_to(ROOT)),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'n':len(adj),'k':len(adj[0]),'lambda':1,'mu':mu,
            'initial_invariant':'transport_cycle_lengths' if mu==2 else 'transport_per_vertex_4cycle_histogram',
            'refinement_class_counts':rounds,'stable_class_sizes':sorted(counts.values()),
            'colors':colors,'initial_signatures':signatures,'representative_roots':roots,
            'full_group_upper_bound':min(r['class_size']*r['rooted_skeleton_group_order'] for r in roots),
            'full_graph_group_not_recomputed':True,'seconds':time.monotonic()-start}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/(name+'.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['name','refinement_class_counts','stable_class_sizes','seconds']}),flush=True)
    print('SKELETON_ORDERS '+json.dumps([r['rooted_skeleton_group_order'] for r in roots]),flush=True)
    return result


def main():
    lab=ROOT/'data/codex_asymmetry_synthesis_20261014/lab_sources'
    paths=[('bvls243',ROOT/'data/srg243/bvls243.edges',2),
           ('twin243',ROOT/'data/srg243/twin243_switched.edges',2),
           ('gamma3',ROOT/'data/srg243/family/gamma3_aut864.edges',2),
           ('gamma4',ROOT/'data/srg243/family/gamma4_aut3888.edges',2),
           ('gamma5',lab/'new243_tricayley_Z3x4_grids25.edges',2),
           ('gamma6',lab/'new243_trade_aut108.edges',2),
           ('gamma7',lab/'new243_trade_aut162.edges',2),
           ('gamma8',lab/'new243_trade_aut108_b.edges',2),
           ('hemi378',ROOT/'data/codex_lambda_one_construction_20261014/seed378/hemi_s1.edges',8)]
    results=[study(name,path,mu) for name,path,mu in paths]
    summary=[{k:r[k] for k in ['name','n','k','mu','refinement_class_counts','stable_class_sizes','representative_roots','full_group_upper_bound','seconds']} for r in results]
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
