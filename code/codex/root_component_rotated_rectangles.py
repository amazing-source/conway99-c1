"""No-three-edge rectangles at a root-neighbour after fixing its two stars.

Fixing a whole line neighbourhood fixes the six matched pairs in each of
its two Gamma stars. Each is a line through the corresponding original
root neighbour a. For two distinct such pairs, each cross pair has exactly
one common Gamma neighbour (the other common neighbour is a). Those four
vertices form a rectangle at a, so its induced edge count cannot be three.
The corners remain variables: no outside neighbourhood or witness is fixed.

In corner order00,01,10,11, a diagonal edge excludes every row/column edge:
otherwise its endpoint has two neighbours carrying the same mate label.
Together with E3 this leaves exactly15 edge patterns (one empty, six with
one edge, seven with two edges, and the single four-cycle of row/column edges).
"""

from itertools import combinations
from root_component_propagation import LABELS
from root_component_boundary_psd import fixed_line_graph


def add_rotated_rectangles(model, graph, template, tables, root, part, code, count):
    fixed=fixed_line_graph(graph,template,tables,root,part,code)
    stars=[[w for w,p in enumerate(LABELS) if 2*root+bit in p] for bit in range(2)]
    outside=[w for w,p in enumerate(LABELS) if all(a//2!=root for a in p)]
    assert len(outside)==60
    assert all(isinstance(fixed[u][v],int) for star in stars for u in star for v in star)
    return add_fixed_star_rectangles(model,fixed,[(2*root+bit,star,outside) for bit,star in enumerate(stars)],count)


def add_grid_rotations(model, graph, count):
    """Use all already fixed prism lines, without fixing any component code."""
    stars=[]
    for root in range(7):
        outside=[w for w,p in enumerate(LABELS) if all(a//2!=root for a in p)]
        for bit in range(2):
            star=[w for w,p in enumerate(LABELS) if 2*root+bit in p]
            stars.append((2*root+bit,star,outside))
    return add_fixed_star_rectangles(model,graph,stars,count)


def add_fixed_star_rectangles(model, fixed, rooted_stars, count, required_roots=(), rectangle_constraints=None, grid_dominance_roots=()):
    """Rooted stars list (root identifier, known colour class, outside60)."""
    plans=[]
    for root_letter,star,outside in rooted_stars:
        lines=[(u,v) for u,v in combinations(star,2) if isinstance(fixed[u][v],int) and fixed[u][v]==1]
        assert len({w for line in lines for w in line})==2*len(lines)
        for first,second in combinations(lines,2):
            pairs=[tuple(sorted((u,v))) for u in first for v in second]
            choices=[]
            for u,v in pairs:
                if isinstance(fixed[u][v],int):assert fixed[u][v]==0
                else:model.add(fixed[u][v]==0)
                choices.append([w for w in outside if not any(isinstance(e,int) and e==0 for e in (fixed[u][w],fixed[v][w]))])
            cost=sum(len(choices[i])*len(choices[j]) for i,j in combinations(range(4),2))
            plans.append((cost,root_letter,first,second,pairs,choices))
    plans.sort()
    edge_patterns=[]
    for mask in range(64):
        bits=[(mask>>i)&1 for i in range(6)]
        if sum(bits) not in (0,1,2,4):continue
        if (bits[2] or bits[3]) and any(bits[i] for i in (0,1,4,5)):continue
        edge_patterns.append(bits)
    assert len(edge_patterns)==15
    products={};corners={};records=[];element_entries=0;dominance_records=[]
    def product(a,b):
        if isinstance(a,int):return b if a else 0
        if isinstance(b,int):return a if b else 0
        if a.index==b.index:return a
        key=tuple(sorted((a.index,b.index)))
        if key not in products:
            value=model.new_bool_var(f'rotated_corner_product_{len(products)}')
            model.add(value<=a);model.add(value<=b);model.add(value>=a+b-1)
            products[key]=value
        return products[key]
    def corner(pair,choices):
        if pair in corners:
            assert corners[pair]['choices']==choices
            return corners[pair]
        u,v=pair
        if not choices:
            model.add(False)
            return {'choices':[]}
        flags=[product(fixed[u][w],fixed[v][w]) for w in choices]
        model.add(sum(flags)==1)
        selector=model.new_int_var(0,len(choices)-1,f'rotated_corner_{u}_{v}')
        model.add(selector==sum(i*flag for i,flag in enumerate(flags)))
        actual=model.new_int_var(min(choices),max(choices),f'rotated_corner_vertex_{u}_{v}')
        model.add(actual==sum(w*flag for w,flag in zip(choices,flags)))
        value={'choices':choices,'selector':selector,'actual':actual,'flags':dict(zip(choices,flags))}
        corners[pair]=value
        return value
    selected=[plan for i,plan in enumerate(plans) if i<count or plan[1] in required_roots]
    for _,root_letter,first,second,pairs,choices in selected:
        cs=[corner(pair,domain) for pair,domain in zip(pairs,choices)]
        if any(not c['choices'] for c in cs):
            return {'empty_corner_domain':True,'root_letter':root_letter,'lines':[first,second]}
        model.add_all_different([c['actual'] for c in cs])
        es=[]
        for i,j in combinations(range(4),2):
            a,b=cs[i],cs[j]
            entries=[fixed[u][v] for u in a['choices'] for v in b['choices']]
            slot=model.new_int_var(0,len(entries)-1,f'rotated_slot_{len(records)}_{i}_{j}')
            model.add(slot==a['selector']*len(b['choices'])+b['selector'])
            edge=model.new_bool_var(f'rotated_edge_{len(records)}_{i}_{j}')
            model.add_element(slot,entries,edge)
            es.append(edge);element_entries+=len(entries)
        model.add(sum(es)!=3)
        model.add(sum(es)<=4)
        model.add_allowed_assignments(es,edge_patterns)
        prescribed_grid=rectangle_constraints(root_letter,first,second,es) if rectangle_constraints is not None else None
        if root_letter in grid_dominance_roots and prescribed_grid is not False:
            # Here root_letter is an actual vertex index in a full graph.
            # For an induced 3x3 grid G in a Conway graph, every exterior
            # vertex has one neighbour in G: both sum d and sum d^2 are90.
            # Thus A*1_G=1+3*1_G. Corners remain selected variables.
            assert len(fixed)==99
            tag=f'rotated_grid_dominance_{len(dominance_records)}'
            active=1 if prescribed_grid is True else model.new_bool_var(tag+'_active')
            if prescribed_grid is not True:
                model.add(sum(es)==4).only_enforce_if(active)
                model.add(sum(es)!=4).only_enforce_if(active.Not())
            base=[root_letter,*first,*second]
            for w in range(99):
                neighbour_terms=[fixed[w][v] for v in base]
                membership=int(w in base)+sum(c['flags'].get(w,0) for c in cs)
                for i,c in enumerate(cs):
                    entries=[fixed[w][v] for v in c['choices']]
                    if len(entries)==1:value=entries[0]
                    else:
                        value=model.new_bool_var(f'{tag}_{w}_{i}')
                        model.add_element(c['selector'],entries,value)
                        element_entries+=len(entries)
                    neighbour_terms.append(value)
                constraint=model.add(sum(neighbour_terms)==1+3*membership)
                if prescribed_grid is not True:constraint.only_enforce_if(active)
            dominance_records.append({'root':root_letter,'lines':[list(first),list(second)],
                'unconditional':prescribed_grid is True,'equations':99})
        records.append({'root_letter':root_letter,'lines':[list(first),list(second)],
                        'corner_domain_sizes':[len(c['choices']) for c in cs]})
    return {'rectangles':records,'available_fixed_line_pairs':len(plans),
            'allowed_six_edge_patterns':len(edge_patterns),
            'distinct_corner_variables':len(corners),'common_neighbour_products':len(products),
            'grid_dominance':dominance_records,
            'element_entries':element_entries,'scope':__doc__}
