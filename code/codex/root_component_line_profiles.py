"""Linearize common neighbours using complete outside rows at a root line.

For any root line r, its 36 neighbours split into the prescribed components
of size 6s. An outside vertex has exactly s neighbours in each component,
two neighbours of each colour. Its two colour-zero neighbours are fixed
by its label. Enumerate all four remaining neighbours (two in each star)
subject to these counts and already-forced edges. This uses no local seed.

All 276 C2 equations on pairs of star vertices split into an inside sum
over 24 vertices and an outside sum over 60 vertices. Profile indicators
make the latter linear. The few inside products are retained exactly.
For different components the inside sum is zero and the target is 1
for the same colour, 2 otherwise.
"""

from itertools import combinations
from root_component_propagation import LABELS


def add_triple_packing(model, rows):
    """No two outside vertices may share three of the 36 line neighbours."""
    triples={}
    for w,profiles,flags in rows:
        for profile,flag in zip(profiles,flags):
            full=sorted([a+1 for a in LABELS[w]]+[v+15 for v in profile])
            for triple in combinations(full,3):
                terms,owners=triples.setdefault(triple,([],set()))
                terms.append(flag);owners.add(w)
    count=0
    for terms,owners in triples.values():
        if len(owners)>1:
            model.add(sum(terms)<=1)
            count+=1
    return count


def root_profiles(graph, template, root):
    lookup={p:i for i,p in enumerate(LABELS)}
    parts=[tuple(p) for p in template['nontrivial_component_groups'][root]]
    grouped={j for p in parts for j in p}
    parts+= [(j,) for j in range(7) if j!=root and j not in grouped]
    part_of={j:i for i,p in enumerate(parts) for j in p}
    letters=[a for a in range(14) if a//2!=root]
    stars=[[lookup[tuple(sorted((2*root+c,a)))] for a in letters] for c in range(2)]
    vertices=stars[0]+stars[1]
    position={w:i for i,w in enumerate(vertices)}
    locations={w:(part_of[a//2],colour) for colour,row in enumerate(stars) for a,w in zip(letters,row)}
    masks=[sum(1<<position[w] for w in vertices if locations[w][0]==i) for i in range(len(parts))]
    rows={}
    for w,label in enumerate(LABELS):
        if root in tuple(a//2 for a in label):
            continue
        own={a//2 for a in label}
        targets=[len(p)-len(own & set(p)) for p in parts]
        choices=[]
        for row in stars:
            allowed=[v for v in row if not isinstance(graph[w][v],int) or graph[w][v]==1]
            forced={v for v in row if isinstance(graph[w][v],int) and graph[w][v]==1}
            choices.append([tuple(p) for p in combinations(allowed,2) if forced.issubset(p)])
        profiles=[]
        for a in choices[0]:
            for b in choices[1]:
                profile=tuple(sorted(a+b))
                mask=sum(1<<position[v] for v in profile)
                if all((mask & cmask).bit_count()==target for cmask,target in zip(masks,targets)):
                    profiles.append(profile)
        rows[w]=profiles
    return {'root':root,'vertices':vertices,'locations':locations,'rows':rows,
            'flag_count':sum(map(len,rows.values())),'component_sizes':[6*len(p) for p in parts]}


def add_line_profiles(model, graph, template, count, triple_packing=False):
    candidates=[root_profiles(graph,template,root) for root in range(7)]
    candidates.sort(key=lambda x:(x['flag_count'],x['root']))
    records=[]
    products={}
    def product(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        if a.index==b.index:return a
        key=tuple(sorted((a.index,b.index)))
        if key not in products:
            p=model.new_bool_var(f'line_profile_product_{len(products)}')
            model.add(p<=a);model.add(p<=b);model.add(p>=a+b-1)
            products[key]=p
        return products[key]
    for data in candidates[:count]:
        root,locations=data['root'],data['locations']
        contributions={(u,v):[] for u,v in combinations(sorted(locations),2)}
        profile_rows=[]
        for w,profiles in data['rows'].items():
            if not profiles:
                model.add(False)
                return {'empty_profile':w,'root_line':root}
            flags=[model.new_bool_var(f'line_profile_{root}_{w}_{i}') for i in range(len(profiles))]
            model.add_exactly_one(flags)
            profile_rows.append((w,profiles,flags))
            for v in locations:
                model.add(graph[w][v]==sum(flag for flag,profile in zip(flags,profiles) if v in profile))
            for flag,profile in zip(flags,profiles):
                for u,v in combinations(profile,2):
                    contributions[u,v].append(flag)
        for (u,v),terms in contributions.items():
            inside=sum(product(graph[u][z],graph[v][z]) for z in locations)
            model.add(graph[u][v]+inside+sum(terms)==2-len(set(LABELS[u]) & set(LABELS[v])))
        records.append({'root_line':root,'component_sizes':data['component_sizes'],
                        'profile_flags':data['flag_count'],'outside_vertices':len(data['rows']),
                        'common_neighbour_equations':len(contributions),
                        'triple_packing_constraints':add_triple_packing(model,profile_rows) if triple_packing else 0})
    return {'records':records,'inside_products':len(products),'scope':__doc__}
