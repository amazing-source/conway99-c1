"""Exact utilities for the Paley/Paulus reconstruction experiment."""
from __future__ import annotations
from collections import Counter
from itertools import combinations
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
def verify_srg(G,parameters=(25,12,5,6)):
    n,k,lam,mu=parameters
    assert set(G)==set(range(n)) and not G.is_directed() and nx.number_of_selfloops(G)==0
    assert all(G.degree(v)==k for v in G)
    for u,v in combinations(G,2):
        cn=len(set(G[u])&set(G[v]))
        assert cn==(lam if G.has_edge(u,v) else mu),(u,v,cn)
    return True
def prepare(G):
    state=(tuple(sorted(G)),tuple(sorted(tuple(sorted(e)) for e in G.edges)))
    if G.graph.get('_signature_state')==state and all('sig' in G.nodes[v] for v in G):return G
    counts={v:[0,0] for v in G}
    for C in nx.enumerate_all_cliques(G):
        if len(C)>5:break
        if len(C) in (4,5):
            for v in C:counts[v][len(C)-4]+=1
    sig={v:tuple(counts[v]) for v in G};seed=sig.copy()
    labels={s:i for i,s in enumerate(sorted(set(sig.values())))}
    col={v:labels[sig[v]] for v in G}
    for _ in range(len(G)):
        keys={v:(col[v],tuple(sorted(col[w] for w in G[v]))) for v in G}
        labels={s:i for i,s in enumerate(sorted(set(keys.values())))}
        new={v:labels[keys[v]] for v in G}
        if len(set(new.values()))==len(set(col.values())):
            col=new;break
        col=new
    for v in G:G.nodes[v]['sig']=(seed[v],col[v])
    G.graph['fingerprint']=tuple(sorted(G.nodes[v]['sig'] for v in G))
    G.graph['_signature_state']=state
    return G
def iso_map(G,H):
    prepare(G);prepare(H)
    if G.graph['fingerprint']!=H.graph['fingerprint']:return None
    matcher=nx.algorithms.isomorphism.GraphMatcher(G,H,node_match=lambda a,b:a['sig']==b['sig'])
    return next(matcher.isomorphisms_iter(),None)
def all_aut(G):
    prepare(G)
    return list(nx.algorithms.isomorphism.GraphMatcher(G,G,node_match=lambda a,b:a['sig']==b['sig']).isomorphisms_iter())
def catalogue():
    gs=nx.read_graph6(ROOT/'data/sr251256.g6')
    for G in gs:verify_srg(G);prepare(G)
    return gs
def identify(G,gs):
    prepare(G)
    for i,H in enumerate(gs,1):
        m=iso_map(G,H)
        if m is not None:
            assert all(G.has_edge(u,v)==H.has_edge(m[u],m[v]) for u,v in combinations(G,2))
            return i,m
    raise ValueError('No match in verified catalogue')
def gm_switch(G,vertices):
    S=set(vertices);k=len(S);O=set(G)-S
    assert k%2==0 and k>0
    assert len({len(set(G[v])&S) for v in S})==1
    assert all(len(set(G[v])&S) in (0,k//2,k) for v in O)
    H=nx.Graph();H.add_nodes_from(G);H.add_edges_from(G.edges)
    for v in O:
        if len(set(G[v])&S)==k//2:
            for u in S:
                if H.has_edge(u,v):H.remove_edge(u,v)
                else:H.add_edge(u,v)
    verify_srg(H)
    return H
