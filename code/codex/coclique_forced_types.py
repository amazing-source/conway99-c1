"""A direct family criterion: forced users of a repeated type form no odd cycle."""
from pathlib import Path
from itertools import combinations
from collections import deque
import argparse
import json

from coclique_variable_border_cuts import border_data


def odd_cycle(vertices,edges):
    graph={u:set() for u in vertices}
    for u,v in edges:
        if u in graph and v in graph:graph[u].add(v);graph[v].add(u)
    colour={};parent={}
    for start in vertices:
        if start in colour:continue
        colour[start]=0;parent[start]=None;queue=deque([start])
        while queue:
            u=queue.popleft()
            for v in sorted(graph[u]):
                if v not in colour:
                    colour[v]=1-colour[u];parent[v]=u;queue.append(v)
                elif colour[v]==colour[u]:
                    pu=[];pv=[];x=u
                    while x is not None:pu.append(x);x=parent[x]
                    x=v
                    while x is not None:pv.append(x);x=parent[x]
                    shared=next(x for x in pu if x in pv)
                    cycle=pu[:pu.index(shared)+1]+pv[:pv.index(shared)][::-1]
                    assert len(cycle)%2==1
                    assert all(tuple(sorted((a,b))) in edges for a,b in zip(cycle,cycle[1:]+cycle[:1]))
                    return cycle
    return None


def scan(w):
    n,a,m,d,r,allowed,sat=border_data(w)
    forced={row:{} for row in m};local=[]
    for u in range(18,n):
        eligible=[row for row in m if allowed[u,row]]
        for row in eligible:
            bounds=[dict(kind='degree',demand=d[u],other_types=[t for t in eligible if t!=row])]
            bounds.extend(dict(kind='quota',anchor=i,demand=r[u,i],other_types=[t for t in eligible if i in t and t!=row]) for i in row)
            strongest=max(bounds,key=lambda b:b['demand']-len(b['other_types']))
            lower=strongest['demand']-len(strongest['other_types'])
            if lower>=1:forced[row][u]=dict(lower=lower,**strongest)
            if lower>1:local.append(dict(vertex=u,type=row,lower=lower,proof=strongest))
    obstructions=[]
    for row,users in forced.items():
        if m[row]==1:
            pair=next((list(e) for e in sat if all(u in users for u in e)),None)
            if pair:obstructions.append(dict(type=row,multiplicity=1,vertices=pair,left=2,upper=1,forcing={str(u):users[u] for u in pair}))
        elif m[row]==2:
            cycle=odd_cycle(sorted(users),sat)
            if cycle:obstructions.append(dict(type=row,multiplicity=2,vertices=cycle,left=len(cycle),upper=len(cycle)-1,
                                             forcing={str(u):users[u] for u in cycle}))
    return dict(local_single_type_violations=local,coexistence_obstructions=obstructions)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path)
    args=ap.parse_args();result=scan(json.loads(args.source.read_text()));result['source']=str(args.source)
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
