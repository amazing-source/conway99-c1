"""Exact lambda=1 using actual triangle indicators, plus triangle cores.

A Gamma edge sharing a root label already has its common neighbour in
N(o), so lies in no Gamma triangle. Every other Gamma edge lies in exactly
one. Indicators are equivalent to ALL THREE edges being present; merely
choosing an edge decomposition into triangles would be insufficient.

Under C1, every Gamma vertex then lies in exactly five Gamma triangles.
For the 60 vertices outside any root line and its neighbourhood, each
vertex lies in at least one core triangle, and there are exactly 32-t(l)
such triangles, where t(l) is the triangle count in the cubic neighbourhood.
If c(l)=6, those 60 vertices partition into exactly twenty triangles.
"""

from itertools import combinations
from root_component_propagation import LABELS


def add_lambda_one_triangles(model, graph, labels):
    n=len(graph)
    incident=[[] for _ in range(n)]
    edge_triangles={pair:[] for pair in combinations(range(n),2)}
    triangles=[]
    forbidden=set()
    auxiliary=0
    for vertices in combinations(range(n),3):
        pairs=list(combinations(vertices,2))
        edges=[graph[u][v] for u,v in pairs]
        if any(isinstance(e,int) and e==0 for e in edges):
            continue
        unknown=[e for e in edges if not isinstance(e,int)]
        if any(set(labels[u]) & set(labels[v]) for u,v in pairs):
            key=tuple(sorted(e.index for e in unknown))
            if key not in forbidden:
                model.add_bool_or([e.Not() for e in unknown])
                forbidden.add(key)
            continue
        if not unknown:
            flag=1
        elif len(unknown)==1:
            flag=unknown[0]
        else:
            flag=model.new_bool_var('actual_triangle_'+'_'.join(map(str,vertices)))
            for edge in unknown:model.add(flag<=edge)
            model.add(flag>=sum(unknown)-len(unknown)+1)
            auxiliary+=1
        triangles.append((vertices,flag))
        for w in vertices:incident[w].append(flag)
        for pair in pairs:edge_triangles[pair].append(flag)
    equations=0
    for (u,v),flags in edge_triangles.items():
        if not (set(labels[u]) & set(labels[v])):
            model.add(sum(flags)==graph[u][v])
            equations+=1
    return triangles,incident,{'triangle_indicators':auxiliary,'possible_triangles':len(triangles),
                               'edge_triangle_equations':equations,'forbidden_shared_label_triangles':len(forbidden)}


def add_exact_triangle_structure(model, graph, template):
    triangles,incident,info=add_lambda_one_triangles(model,graph,LABELS)
    for flags in incident:model.add(sum(flags)==5)
    lookup={p:i for i,p in enumerate(LABELS)}
    core_info=[]
    for root in range(7):
        outside={w for w,p in enumerate(LABELS) if root not in tuple(a//2 for a in p)}
        local={w:[] for w in outside}
        flags=[]
        for vertices,flag in triangles:
            if set(vertices)<=outside:
                flags.append(flag)
                for w in vertices:local[w].append(flag)
        prism_triangles=[]
        for a in range(14):
            if a//2!=root:
                u=lookup[tuple(sorted((2*root,a)))];v=lookup[tuple(sorted((2*root+1,a)))]
                prism_triangles.append(graph[u][v])
        model.add(sum(flags)+sum(prism_triangles)==32)
        six_prisms=not template['nontrivial_component_groups'][root]
        for fs in local.values():
            model.add(sum(fs)==1) if six_prisms else model.add(sum(fs)>=1)
        core_info.append({'root_line':root,'vertices':len(outside),'possible_triangles':len(flags),
                          'vertex_triangle_count':1 if six_prisms else 'at least 1',
                          'triangle_count':'32 minus t(root line)'})
    info.update(gamma_triangles_per_vertex=5,cores=core_info,scope=__doc__)
    return info
