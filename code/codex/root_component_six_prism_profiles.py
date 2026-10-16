"""One-hot boundary profiles when a root line has six prism components.

There are 60 outside vertices and six components of six neighbours of
the line. Every outside vertex chooses one neighbour in each component,
two in each of the three colours. Its two colour-zero neighbours are
its fixed label. Hence exactly 96 possible remaining four-symbol rows.
The 240 common-neighbour equations on pairs of nonzero-colour vertices
in different prisms become linear sums of profile indicators.
"""

from itertools import combinations, product
from root_component_propagation import LABELS, RECTANGLES


def add_six_prism_profiles(model, graph, template):
    lookup={p:i for i,p in enumerate(LABELS)}
    roots=[r for r,parts in enumerate(template['nontrivial_component_groups']) if not parts]
    records=[]
    for root in roots:
        groups=[j for j in range(7) if j!=root]
        symbols={j:[lookup[tuple(sorted((2*root+a,2*j+b)))] for a,b in product(range(2),repeat=2)] for j in groups}
        locations={w:(j,a,b) for j in groups for a,b in product(range(2),repeat=2) for w in [symbols[j][2*a+b]]}
        contributions={(u,v):[] for u,v in combinations(sorted(locations),2) if locations[u][0]!=locations[v][0]}
        outside=[w for w,p in enumerate(LABELS) if root not in tuple(a//2 for a in p)]
        row_counts=[]
        for w in outside:
            own={a//2 for a in LABELS[w]}
            remaining=[j for j in groups if j not in own]
            assert len(remaining)==4
            profiles=[]
            for colour_zero in combinations(remaining,2):
                first=set(colour_zero)
                for bits in product(range(2),repeat=4):
                    chosen=tuple(sorted(symbols[j][2*int(j not in first)+bit] for j,bit in zip(remaining,bits)))
                    selected=set(chosen)
                    if any(isinstance(graph[w][v],int) and graph[w][v]!=int(v in selected) for v in locations):
                        continue
                    profiles.append(chosen)
            if not profiles:
                model.add(False)
                return {'empty_profile':w,'root_line':root}
            flags=[model.new_bool_var(f'prism_profile_{root}_{w}_{i}') for i in range(len(profiles))]
            model.add_exactly_one(flags)
            for v in locations:
                model.add(graph[w][v]==sum(flag for flag,profile in zip(flags,profiles) if v in profile))
            for flag,profile in zip(flags,profiles):
                for u,v in combinations(profile,2):
                    contributions[u,v].append(flag)
            row_counts.append(len(profiles))
        for (u,v),terms in contributions.items():
            colour_u,colour_v=locations[u][1],locations[v][1]
            model.add(sum(terms)==(1 if colour_u==colour_v else 2))
        records.append({'root_line':root,'outside_vertices':len(outside),'profile_flags':sum(row_counts),
                        'profiles_per_row':row_counts,'linear_common_neighbour_equations':len(contributions)})
    return {'records':records,'scope':__doc__}
