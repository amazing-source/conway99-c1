"""Transport the full c>=4 component-graph cover to a neighbouring root.

No prism budget is imposed at the new root. Use all200 component templates
(116 nongrid graphs), not the79 templates filtered at a low-prism root.
The new seven lines are the old-root line and the six fixed matched pairs
in its Gamma star. Only nongrid status is transported here; missing rotated
rectangles remain free Booleans in the necessary graph-cover table.
An optional frozen exclusion frontier is applied conditionally when the
new root itself has prism sum<=51; larger sums retain the full cover.
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


def add_residual_component_identities(model,root,lines,items,incidence,nongrid,pair_index,pairing_maps):
    """Transport component relations as FULL vectors, including the old line.

At the new root delta_ij=-T'1_Qij. For each incident line i,
sum_j delta_ij=0. Four nongrid rectangles must split into two opposite
pairs, since c>=4 forces two size12 components. The same pairing flags
are used for known short-vector projections and all residual coordinates.
Only a complete set of fifteen variable rectangles is used here.
    """
    if len(items)!=15 or not all('integer_residual_coordinates' in item for item in items):
        return {'complete_stars':0,'zero_sum_equations':0,'pairing_equations':0}
    vectors={}
    for item in items:
        a,b=sorted((lines.index(tuple(item['base_vertices'][:2])),lines.index(tuple(item['base_vertices'][2:]))))
        assert (a+1,b+1) not in vectors
        vectors[a+1,b+1]=item['integer_residual_coordinates']
    for original in items[0]['old_root_rectangles']:
        j=lines.index(tuple(original['line']))+1
        vectors[0,j]=original['integer_residual_coordinates']
    assert set(vectors)==set(combinations(range(7),2))
    assert all(len(row)==98 for row in vectors.values()) # old-root coordinate is identically zero
    zero_sum=0;paired=0
    for a in range(7):
        incident_vectors={b:vectors[tuple(sorted((a,b)))] for b in range(7) if b!=a}
        for w in range(98):
            values=[row[w] for row in incident_vectors.values()]
            if all(isinstance(v,int) and v==0 for v in values):continue
            model.add(sum(values)==0);zero_sum+=1
        if a not in pairing_maps:
            neighbours=list(incident_vectors)
            incident={b:incidence[max(a,b)-1] if min(a,b)==0 else
                nongrid[pair_index[min(a,b)-1,max(a,b)-1]] for b in neighbours}
            four=model.new_bool_var(f'residual_four_nongrids_{root}_{a}')
            model.add(sum(incident.values())==4).only_enforce_if(four)
            model.add(sum(incident.values())!=4).only_enforce_if(four.Not())
            pairing={}
            for b,c in combinations(neighbours,2):
                if any(isinstance(incident[x],int) and incident[x]==0 for x in (b,c)):continue
                flag=model.new_bool_var(f'residual_component_pair_{root}_{a}_{b}_{c}')
                model.add(flag<=four)
                for x in (b,c):model.add(flag<=incident[x])
                pairing[b,c]=flag
            for b in neighbours:
                model.add(sum(flag for pair,flag in pairing.items() if b in pair)==incident[b]).only_enforce_if(four)
            pairing_maps[a]=pairing
        for (b,c),flag in pairing_maps[a].items():
            for u,v in zip(incident_vectors[b],incident_vectors[c]):
                if isinstance(u,int) and isinstance(v,int) and u==v==0:continue
                model.add(u+v==0).only_enforce_if(flag);paired+=1
    return {'complete_stars':1,'residual_vectors':21,'coordinates_per_vector':99,
            'zero_sum_equations':zero_sum,'pairing_equations':paired,'scope':add_residual_component_identities.__doc__}


def add_rotated_template_cover(model,rectangles,template,all_templates,eigen_context=None,low_budget_snapshot=None):
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
        low_info=None
        if low_budget_snapshot is not None and len(items)==15:
            from root_component_low_budget_transport import add_conditional_cover
            low_masks=tuple(sorted({all_templates[i]['graph_mask'] for i in low_budget_snapshot['allowed_template_indices']}))
            assert list(low_masks)==low_budget_snapshot['allowed_nongrid_masks']
            low_rows,_=allowed_rows(low_masks,tuple(incidence))
            low_info=add_conditional_cover(model,root,items,nongrid,low_rows,low_budget_snapshot)
        flow_equations=0;flow_variables=0;old_rectangle_bounds=0
        spectral_energy_cuts=0;energy_tables=0;pairing_equations=0;pairing_maps={}
        if eigen_context is not None:
            # The21 rectangle vectors at any root have zero sum at each of
            # its seven incident lines. Pair them with the OLD eigenvectors
            # to transport this identity across the two coordinate charts.
            # A missing rectangle keeps a free bounded scalar; no corner or
            # local graph is chosen for it.
            original=items[0]['old_root_rectangles']
            observed={tuple(sorted((lines.index(tuple(item['base_vertices'][:2])),
                                    lines.index(tuple(item['base_vertices'][2:]))))):item for item in items}
            projections=[]
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
                projections.append(ys)
                squares={}
                for (a,b),value in ys.items():
                    # Some old-root sums are expressions rather than variables.
                    y=model.new_int_var(-cap,cap,f'rotated_energy_sum_{root}_{di}_{a}_{b}')
                    model.add(y==value)
                    square=model.new_int_var(0,cap*cap,f'rotated_energy_square_{root}_{di}_{a}_{b}')
                    model.add_allowed_assignments([y,square],[(v,v*v) for v in range(-cap,cap+1)])
                    squares[a,b]=square;energy_tables+=1
                for a in range(7):
                    # Incident rectangle vectors have a positive semidefinite
                    # Laplacian Gram with diagonal<=8, hence operator<=16I.
                    model.add(sum(v for pair,v in squares.items() if a in pair)<=16*qnorm)
                    spectral_energy_cuts+=1
                local_energy=[]
                for li,(u,v) in enumerate(lines):
                    hu=eigen_context['values'][di][u];hv=eigen_context['values'][di][v]
                    ulo,uhi=eigen_context['bounds'][di][u];vlo,vhi=eigen_context['bounds'][di][v]
                    energy=model.new_int_var(0,8*qnorm,f'rotated_star_energy_{root}_{di}_{li}')
                    allowed=[]
                    for x in range(ulo,uhi+1):
                        for y in range(vlo,vhi+1):
                            cost=3*(x*x+y*y)+2*x*y
                            if cost<=8*qnorm:allowed.append((x,y,cost))
                    model.add_allowed_assignments([hu,hv,energy],allowed)
                    local_energy.append(energy);energy_tables+=1
                # Projection of h away from the new closed star has norm
                # 7q-(7/8)L, L=sum_pairs(3(h_u^2+h_v^2)+2h_uh_v).
                # The21 Gamma rectangles are disjoint four-sets, so their
                # squared sums total at most4 times that remaining norm.
                model.add(2*sum(squares.values())+7*sum(local_energy)<=56*qnorm)
                spectral_energy_cuts+=1
            for a in range(7):
                neighbours=[b for b in range(7) if b!=a]
                incident={b:incidence[max(a,b)-1] if min(a,b)==0 else
                    nongrid[pair_index[min(a,b)-1,max(a,b)-1]] for b in neighbours}
                four=model.new_bool_var(f'rotated_four_nongrids_{root}_{a}')
                model.add(sum(incident.values())==4).only_enforce_if(four)
                model.add(sum(incident.values())!=4).only_enforce_if(four.Not())
                pairing={}
                for b,c in combinations(neighbours,2):
                    if any(isinstance(incident[x],int) and incident[x]==0 for x in (b,c)):continue
                    flag=model.new_bool_var(f'rotated_component_pair_{root}_{a}_{b}_{c}')
                    model.add(flag<=four)
                    for x in (b,c):model.add(flag<=incident[x])
                    pairing[b,c]=flag
                    for ys in projections:
                        model.add(ys[tuple(sorted((a,b)))]+ys[tuple(sorted((a,c)))]==0).only_enforce_if(flag)
                        pairing_equations+=1
                for b in neighbours:
                    model.add(sum(flag for pair,flag in pairing.items() if b in pair)==incident[b]).only_enforce_if(four)
                pairing_maps[a]=pairing
                # Four nongrid neighbours force the 12+12+6+6 pattern. Its
                # two size12 components pair opposite rectangle vectors.
        residual_info=add_residual_component_identities(model,root,lines,items,incidence,nongrid,pair_index,pairing_maps)
        info.append({'root_letter':root,'old_line_nongrid_incidence':incidence,
                     'fixed_matched_lines':[list(line) for line in lines],
                     'realized_rectangles':len(items),'allowed_nongrid_graphs':len(rows),
                     'cover_relabelings_before_deduplication':relabelings,
                     'cross_chart_zero_sum_equations':flow_equations,
                     'missing_rectangle_projection_variables':flow_variables,
                     'old_root_rectangle_projection_bounds':old_rectangle_bounds,
                     'spectral_energy_inequalities':spectral_energy_cuts,
                     'spectral_energy_tables':energy_tables,
                     'degree_four_component_pairing_equations':pairing_equations,
                     'full_residual_component_identities':residual_info})
        if low_info is not None:info[-1]['conditional_low_budget_cover']=low_info
    return {'all_prebudget_component_templates':200,'all_prebudget_nongrid_graphs':116,
            'roots':info,'new_root_prism_budget':None,'scope':__doc__}
