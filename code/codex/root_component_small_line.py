"""At most m connected components in the neighbourhood of a fixed line.

A rooted forest witnesses the bound. Each member has one parent or is
a root, parent edges belong to the actual graph, and depths strictly
increase. At most m roots are allowed. This is equivalent to c(L)<=m;
there is no assumption about the sizes or isomorphism types of components.
"""
from itertools import combinations


def add_small_line(model,graph,line,maximum_components=3,tag='small_line'):
    n=len(graph);line=tuple(line)
    assert len(set(line))==3 and 1<=maximum_components
    for u,v in combinations(line,2):model.add(graph[u][v]==1)
    outside=[w for w in range(n) if w not in line]
    member={};roots={};depth={};parents={w:[] for w in outside};arcs=0
    for w in outside:
        member[w]=model.new_bool_var(f'{tag}_member_{w}')
        model.add(sum(graph[a][w] for a in line)==member[w])
        roots[w]=model.new_bool_var(f'{tag}_root_{w}')
        model.add(roots[w]<=member[w])
        depth[w]=model.new_int_var(0,len(outside)-1,f'{tag}_depth_{w}')
        model.add(depth[w]==0).only_enforce_if(roots[w])
        model.add(depth[w]==0).only_enforce_if(member[w].Not())
    for u,v in combinations(outside,2):
        edge=graph[u][v]
        if isinstance(edge,int) and not edge:continue
        for source,target in ((u,v),(v,u)):
            parent=model.new_bool_var(f'{tag}_parent_{source}_{target}')
            model.add(parent<=edge)
            model.add(parent<=member[source]);model.add(parent<=member[target])
            model.add(depth[target]>=depth[source]+1).only_enforce_if(parent)
            parents[target].append(parent);arcs+=1
    for w in outside:model.add(sum(parents[w])+roots[w]==member[w])
    model.add(sum(roots.values())<=maximum_components)
    return {'line':list(line),'maximum_components':maximum_components,
            'forest_parent_arcs':arcs,'scope':__doc__,
            'no_component_size_assumption':True,'prism_budget_at_line_assumed':False}
