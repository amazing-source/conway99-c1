"""Transport the full c>=4 component-graph cover to a neighbouring root.

No prism budget is imposed at the new root. Use all200 component templates
(116 nongrid graphs), not the79 templates filtered at a low-prism root.
The new seven lines are the old-root line and the six fixed matched pairs
in its Gamma star. Only nongrid status is transported here; missing rotated
rectangles remain free Booleans in the necessary graph-cover table.
"""
from functools import lru_cache
from itertools import combinations,permutations
from math import isqrt
from root_component_propagation import LABELS
from root_component_quotient import EDGES,relabel


@lru_cache(maxsize=256)
def allowed_rows(masks,incidence):
    """All relabelings with precisely the given nongrid neighbours of line0."""
    target_ng=[i+1 for i,value in enumerate(incidence) if value]
    target_grid=[i+1 for i,value in enumerate(incidence) if not value]
    tail_masks=set();relabelings=0
    for mask in masks:
        neighbours=[[] for _ in range(7)]
        for ei,(a,b) in enumerate(EDGES):
            if mask&(1<<ei):neighbours[a].append(b);neighbours[b].append(a)
        for root in range(7):
            ng=neighbours[root]
            if len(ng)!=len(target_ng):continue
            grids=[i for i in range(7) if i!=root and i not in ng]
            for left in permutations(target_ng):
                for right in permutations(target_grid):
                    image=[None]*7;image[root]=0
                    for a,b in zip(ng,left):image[a]=b
                    for a,b in zip(grids,right):image[a]=b
                    result=relabel(mask,image)
                    assert tuple((result>>i)&1 for i in range(6))==incidence
                    tail_masks.add(result>>6);relabelings+=1
    return tuple(tuple((mask>>i)&1 for i in range(15)) for mask in sorted(tail_masks)),relabelings


def add_rotated_template_cover(model,rectangles,template,all_templates,eigen_context=None):
    assert len(all_templates)==200, 'Use the complete pre-budget component cover.'
    masks=tuple(sorted({t['graph_mask'] for t in all_templates}))
    assert len(masks)==116
    old_ng={tuple(e) for e in template['nongrid_edges']}
    groups={}
    for rectangle in rectangles:groups.setdefault(rectangle['root'],[]).append(rectangle)
    info=[]
    for root,items in sorted(groups.items()):
        lines=sorted(tuple(line) for line in items[0]['all_lines'])
        if len(lines)!=6:continue
        assert all(sorted(tuple(line) for line in item['all_lines'])==lines for item in items)
        assert all(root in LABELS[w] for line in lines for w in line)
        incidence=[]
        for u,v in lines:
            a=next(b for b in LABELS[u] if b!=root)
            b=next(c for c in LABELS[v] if c!=root)
            # The old-root line and this line form a grid exactly when they
            # lie in one of the known prism components of the old line.
            grid=(b==(a^1) and tuple(sorted((root//2,a//2))) not in old_ng)
            incidence.append(int(not grid))
        pairs=list(combinations(range(6),2));pair_index={pair:i for i,pair in enumerate(pairs)}
        nongrid=[model.new_bool_var(f'rotated_template_ng_{root}_{a}_{b}') for a,b in pairs]
        for item in items:
            first=tuple(item['base_vertices'][:2]);second=tuple(item['base_vertices'][2:])
            a,b=sorted((lines.index(first),lines.index(second)))
            flag=nongrid[pair_index[a,b]]
            model.add(sum(item['edges'])<=2).only_enforce_if(flag)
            model.add(sum(item['edges'])==4).only_enforce_if(flag.Not())
        rows,relabelings=allowed_rows(masks,tuple(incidence))
        model.add_allowed_assignments(nongrid,rows)
        flow_equations=0;flow_variables=0;old_rectangle_bounds=0
        if eigen_context is not None:
            # The21 rectangle vectors at any root have zero sum at each of
            # its seven incident lines. Pair them with the OLD eigenvectors
            # to transport this identity across the two coordinate charts.
            # A missing rectangle keeps a free bounded scalar; no corner or
            # local graph is chosen for it.
            original=items[0]['old_root_rectangles']
            observed={tuple(sorted((lines.index(tuple(item['base_vertices'][:2])),
                                    lines.index(tuple(item['base_vertices'][2:]))))):item for item in items}
            for di,qnorm in enumerate(eigen_context['lattice_norms']):
                ys={};cap=isqrt(8*qnorm)
                for item in original:
                    j=lines.index(tuple(item['line']))+1
                    value=sum(eigen_context['values'][di][w] for w in item['gamma_vertices'])
                    edge_count=item['edge_count'];assert 0<=edge_count<=4
                    if edge_count==3:model.add(False)
                    local_cap=isqrt(qnorm*(8-2*edge_count))
                    model.add(value>=-local_cap);model.add(value<=local_cap)
                    old_rectangle_bounds+=2;ys[0,j]=value
                for a,b in pairs:
                    if (a,b) in observed:
                        value=observed[a,b]['spectral_sums'][di]
                    else:
                        value=model.new_int_var(-cap,cap,f'rotated_chart_sum_{root}_{di}_{a}_{b}')
                        model.add(value==0).only_enforce_if(nongrid[pair_index[a,b]].Not())
                        flow_variables+=1
                    ys[a+1,b+1]=value
                for a in range(7):
                    model.add(sum(value for pair,value in ys.items() if a in pair)==0)
                    flow_equations+=1
        info.append({'root_letter':root,'old_line_nongrid_incidence':incidence,
                     'fixed_matched_lines':[list(line) for line in lines],
                     'realized_rectangles':len(items),'allowed_nongrid_graphs':len(rows),
                     'cover_relabelings_before_deduplication':relabelings,
                     'cross_chart_zero_sum_equations':flow_equations,
                     'missing_rectangle_projection_variables':flow_variables,
                     'old_root_rectangle_projection_bounds':old_rectangle_bounds})
    return {'all_prebudget_component_templates':200,'all_prebudget_nongrid_graphs':116,
            'roots':info,'new_root_prism_budget':None,'scope':__doc__}
