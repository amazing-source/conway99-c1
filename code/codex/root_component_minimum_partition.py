"""Exact auxiliary partition for global c(line)>=m on fixed non-root lines.

The 36 neighbours of a line have connected components of size 6s. With
at least four components they can be merged into exactly four nonempty
bins, whose sizes are 18+6+6+6 or 12+12+6+6. Each of the three colours
has the same even number in each bin. Edges cannot join distinct bins.
For m=3 the three bin half-sizes range from1 to4. More generally the
maximum half-size is7-m, since all other bins must have positive size.
Conversely m nonempty bins with no cross edge imply at least m
connected components. Bin names are ordered by first occurrence in a
known colour class; this only normalizes auxiliary labels, not the graph.
"""

from itertools import combinations
from root_component_propagation import LABELS, RECTANGLES


def add_minimum_partitions(model, gamma, count, balance=False, partition_context=None,
                           minimum_components=4, all_fixed_star_edges=False):
    graph=[[0]*99 for _ in range(99)]
    for a in range(14):
        graph[0][a+1]=graph[a+1][0]=1
        graph[a+1][(a^1)+1]=1
    for w,label in enumerate(LABELS):
        for a in label:
            graph[a+1][w+15]=graph[w+15][a+1]=1
    for u,v in combinations(range(84),2):
        graph[u+15][v+15]=graph[v+15][u+15]=gamma[u][v]
    lines=[]
    pairs = combinations(range(84),2) if all_fixed_star_edges else (
        pair for corners in RECTANGLES.values() for pair in combinations(corners,2))
    for u,v in pairs:
        edge=gamma[u][v]
        common=set(LABELS[u]) & set(LABELS[v])
        if isinstance(edge,int) and edge==1 and len(common)==1:
            lines.append((next(iter(common))+1,u+15,v+15))
    available=sorted(set(lines));lines=available[:count]
    info=add_partitions_for_lines(model,graph,lines,balance=balance,partition_context=partition_context,
                                  minimum_components=minimum_components)
    info.update(requested_line_count=count,available_fixed_line_count=len(available),
                includes_cross_rectangle_lines=all_fixed_star_edges)
    return info


def add_partitions_for_lines(model, graph, lines, balance=False, partition_context=None, tag_prefix='minc',
                             minimum_components=4):
    """Use any fixed triangle whose first colour class is already known."""
    assert minimum_components in (3,4)
    products={};balance_equations=0
    def product(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        if a.index==b.index:return a
        key=tuple(sorted((a.index,b.index)))
        if key not in products:
            v=model.new_bool_var(f'minc_balance_product_{len(products)}')
            model.add(v<=a);model.add(v<=b);model.add(v>=a+b-1)
            products[key]=v
        return products[key]
    for line_number,line in enumerate(lines):
        outside=[w for w in range(99) if w not in line]
        known=[w for w in outside if graph[line[0]][w]==1]
        assert len(known)==12
        flags, bins, members = {}, {}, {}
        tag=f'{tag_prefix}_{line_number}'
        for w in outside:
            members[w]=model.new_bool_var(f'{tag}_member_{w}')
            model.add(sum(graph[a][w] for a in line)==members[w])
            bins[w]=model.new_int_var(0,minimum_components,f'{tag}_bin_{w}')
            flags[w]=[model.new_bool_var(f'{tag}_bin_{w}_{j}') for j in range(minimum_components+1)]
            model.add_exactly_one(flags[w])
            model.add_map_domain(bins[w],flags[w])
            model.add(members[w]+flags[w][0]==1)
        model.add(sum(members.values())==36)
        # Canonical names depend only on the auxiliary partition itself.
        model.add(bins[known[0]]==1)
        previous=1
        for i,w in enumerate(known[1:],1):
            model.add(bins[w]<=previous+1)
            maximum=model.new_int_var(1,minimum_components,f'{tag}_max_{i}')
            model.add_max_equality(maximum,[previous,bins[w]])
            previous=maximum
        halves=[]
        for j in range(1,minimum_components+1):
            half=model.new_int_var(1,7-minimum_components,f'{tag}_half_{j}')
            halves.append(half)
            model.add(sum(flags[w][j] for w in known)==2*half)
            for a in line[1:]:
                terms=[]
                for w in outside:
                    edge=graph[a][w]
                    if isinstance(edge,int):
                        if edge:
                            terms.append(flags[w][j])
                    else:
                        both=model.new_bool_var(f'{tag}_colour_{a}_{w}_{j}')
                        model.add(both<=edge)
                        model.add(both<=flags[w][j])
                        model.add(both>=edge+flags[w][j]-1)
                        terms.append(both)
                model.add(sum(terms)==2*half)
            if balance:
                # A union S of components of N(L), of size6s and with2s
                # vertices per colour, satisfies sum_x d_S(x)=60s and
                # sum_x d_S(x)^2=60s^2 outside L union N(L). Thus each
                # exterior vertex has exactly s neighbours in S.
                for x in outside:
                    terms=[product(graph[x][y],flags[y][j]) for y in outside]
                    model.add(sum(terms)==3*flags[x][j]).only_enforce_if(members[x])
                    model.add(sum(terms)==half).only_enforce_if(members[x].Not())
                    balance_equations+=2
        for u,v in combinations(outside,2):
            edge=graph[u][v]
            if isinstance(edge,int):
                if not edge:
                    continue
                conditions=[members[u],members[v]]
            else:
                conditions=[edge,members[u],members[v]]
            model.add(bins[u]==bins[v]).only_enforce_if(conditions)
        if partition_context is not None:
            partition_context.append({'line':line,'flags':flags,'halves':halves})
    return {'global_minimum_components':minimum_components,'lines':lines,
            'auxiliary_bins_per_line':minimum_components,'normalization':'First occurrence in fixed colour class only.',
            'component_degree_balance':balance,'component_degree_equations':balance_equations,
            'component_degree_products':len(products)}
