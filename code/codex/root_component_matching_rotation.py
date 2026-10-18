"""Rotate one complete star after fixing ONLY its internal perfect matching.

The cross permutation and the matching in the opposite star stay variable.
For each matched pair u,v, its two opposite-star partners p,q are selected
by their actual adjacency entries. The old-line nine-set is consequently
{o,a,a*,b,c,u,v,p,q}; no opposite-star graph is chosen. This partitions the
existing complete component-code cover by its first matching index only.
"""
from itertools import combinations
from root_component_propagation import LABELS
from root_component_rotated_rectangles import add_fixed_star_rectangles


def add_matching_rotation(model,graph,template,tables,context,matching_index):
    root=context['root'];part=context['part'];letter=2*root
    record=next(r for r in tables['records'] if r['vertices']==6*len(part))
    lookup={pair:i for i,pair in enumerate(LABELS)}
    letters=[a for j in part for a in (2*j,2*j+1)]
    vertices=[lookup[tuple(sorted((letter,a)))] for a in letters]
    present={tuple(edge) for edge in record['internal_matchings'][matching_index]}
    fixed=[list(row) for row in graph]
    model.add(context['selectors'][1]==matching_index)
    for i,j in combinations(range(len(vertices)),2):
        value=int((i,j) in present);u,v=vertices[i],vertices[j]
        model.add(graph[u][v]==value)
        fixed[u][v]=fixed[v][u]=value
    star=[w for w,pair in enumerate(LABELS) if letter in pair]
    opposite=[w for w,pair in enumerate(LABELS) if letter^1 in pair]
    outside=[w for w,pair in enumerate(LABELS) if all(a//2!=root for a in pair)]
    assert len(star)==len(opposite)==12 and len(outside)==60
    assert all(isinstance(fixed[u][v],int) for u in star for v in star)
    rectangles=[]
    info=add_fixed_star_rectangles(model,fixed,[(letter,star,outside)],15,rectangle_context=rectangles)
    if len(rectangles)!=15:
        assert info.get('empty_corner_domain')
        model.add(False)
        return fixed,rectangles,dict(info,scope=__doc__)
    partners={}
    for u in star:
        choices=[w for w in opposite if not isinstance(fixed[u][w],int) or fixed[u][w]]
        assert choices
        flags={w:fixed[u][w] for w in choices}
        model.add(sum(flags.values())==1)
        selector=model.new_int_var(0,len(choices)-1,f'matching_partner_index_{letter}_{u}')
        model.add(selector==sum(i*flags[w] for i,w in enumerate(choices)))
        actual=model.new_int_var(min(choices),max(choices),f'matching_partner_vertex_{letter}_{u}')
        model.add(actual==sum(w*flags[w] for w in choices))
        partners[u]={'choices':choices,'flags':flags,'selector':selector,'actual':actual}
    model.add_all_different([p['actual'] for p in partners.values()])
    nongrids={tuple(edge) for edge in template['nongrid_edges']};original=[]
    for u,v in rectangles[0]['all_lines']:
        p,q=partners[u],partners[v]
        b=next(a for a in LABELS[u] if a!=letter)
        c=next(a for a in LABELS[v] if a!=letter)
        entries=[fixed[x][y] for x in p['choices'] for y in q['choices']]
        slot=model.new_int_var(0,len(entries)-1,f'matching_partner_pair_{u}_{v}')
        model.add(slot==p['selector']*len(q['choices'])+q['selector'])
        edge=model.new_bool_var(f'matching_partner_edge_{u}_{v}')
        model.add_element(slot,entries,edge)
        def contains(partner,a):
            return sum(flag for w,flag in partner['flags'].items() if a in LABELS[w])
        total=model.new_int_var(0,4,f'matching_old_rectangle_edges_{u}_{v}')
        model.add(total==int(c==b^1)+edge+sum(contains(partner,a) for partner in (p,q) for a in (b,c)))
        grid=c==b^1 and tuple(sorted((root,b//2))) not in nongrids
        model.add(total==4 if grid else total<=2)
        shared=int(c==b^1)+edge+contains(p,b)+contains(q,c)
        original.append({'line':(u,v),'gamma_base':[u,v],'gamma_corners':[p,q],
                         'edge_count':4 if grid else total,'shared_label_edges':shared,
                         'old_neighbours':[letter,letter^1,b,c]})
    for item in rectangles:item['old_root_rectangles']=original
    info.update(scope=__doc__,matching_index=matching_index,opposite_partner_domains=[len(p['choices']) for p in partners.values()],
                fixed_cross_permutation=False,fixed_opposite_matching=False)
    return fixed,rectangles,info
