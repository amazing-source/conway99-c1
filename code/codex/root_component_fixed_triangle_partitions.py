"""Use c>=4 at cross-colour triangles exposed by fixing a component code.

A fixed point b of the cross permutation gives the actual triangle
(b,(a,b),(a*,b)). It need not have been fixed in the unrestricted template,
so the baseline's partitions at its first two already-known lines do not
cover it. P16/P17 expose two such triangles with mate labels b,b*, whereas
P136/P137 expose none. Apply the same universal component bound here, with
exact exterior balance and known eigenvector sums; do not assume symmetry.
"""
from itertools import combinations
from root_component_propagation import LABELS
from root_component_minimum_partition import add_partitions_for_lines


def add_fixed_cross_triangle_partitions(model,original,fixed,root,count,eigen_context=None,star_count=0):
    graph=[[0]*99 for _ in range(99)]
    for a in range(14):
        graph[0][a+1]=graph[a+1][0]=1
        graph[a+1][(a^1)+1]=1
    for w,label in enumerate(LABELS):
        for a in label:graph[a+1][w+15]=graph[w+15][a+1]=1
    for u,v in combinations(range(84),2):graph[u+15][v+15]=graph[v+15][u+15]=fixed[u][v]
    lookup={p:i for i,p in enumerate(LABELS)};lines=[]
    for b in range(14):
        if b//2==root:continue
        u=lookup[tuple(sorted((2*root,b)))];v=lookup[tuple(sorted((2*root+1,b)))]
        if not isinstance(fixed[u][v],int) or fixed[u][v]!=1:continue
        if isinstance(original[u][v],int) and original[u][v]==1:continue
        lines.append((b+1,u+15,v+15))
    star_lines=[]
    for a in (2*root,2*root+1):
        vertices=[u for u,label in enumerate(LABELS) if a in label]
        for u,v in combinations(vertices,2):
            if not isinstance(fixed[u][v],int) or fixed[u][v]!=1:continue
            if isinstance(original[u][v],int) and original[u][v]==1:continue
            star_lines.append((a+1,u+15,v+15))
    selected=lines[:count]+star_lines[:star_count];context=[]
    info=add_partitions_for_lines(model,graph,selected,balance=True,partition_context=context,
                                  tag_prefix='fixed_cross_triangle')
    info['available_new_cross_triangles']=len(lines)
    info['available_new_star_triangles']=len(star_lines)
    lower_bounds=[]
    for triangle,partition in zip(selected,context):
        # The old root is the first known vertex in the colour class of b,
        # hence its auxiliary bin is1. Every surely present edge transports
        # this bin name. A deficient known six-vertex component cannot close
        # at size6, so its bin must have at least12 vertices.
        sure={w for w in range(99) if w not in triangle and any(isinstance(graph[a][w],int) and graph[a][w]==1 for a in triangle)}
        connected={0};pending=[0];assert 0 in sure
        while pending:
            u=pending.pop()
            for v in sure-connected:
                if isinstance(graph[u][v],int) and graph[u][v]==1:
                    connected.add(v);pending.append(v)
        minimum=len(connected)
        if any(sum(v!=u and (not isinstance(graph[u][v],int) or graph[u][v]==1) for v in connected)<3 for u in connected):
            minimum+=1
        half=(minimum+5)//6
        model.add(partition['halves'][0]>=half)
        lower_bounds.append({'triangle':list(triangle),'known_connected_vertices':sorted(connected),
                             'minimum_component_vertices':6*half})
    info['old_line_component_lower_bounds']=lower_bounds
    if eigen_context is not None and context:
        from root_component_short_vectors import add_component_signature_cuts
        info['component_signature_cuts']=add_component_signature_cuts(model,context,eigen_context)
    info['scope']=__doc__
    return info
