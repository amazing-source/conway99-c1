"""Realize the full integer residual of a variable rotated nine-set.

For x=1_S, |S|=9, put d=(A-3I)x-1. The SRG identity gives
Ad=-4d, sum(d)=0 and ||d||^2=56-14e, where S has14+e edges.
Thus e=4 forces A1_S=1+3*1_S at EVERY vertex. For e<=2 the
same exact norm controls all99 coordinates, not just known projections.

Here S consists of an original neighbour a, four fixed Gamma vertices
and four selected Gamma corners. The old root has residual zero. The
fourteen old-neighbour coordinates are label counts, and the84 others
are adjacency sums. We also impose the fourteen old-neighbour -4
equations, which are linear in these residual coordinates.
"""

from root_component_propagation import LABELS


def add_rotated_residual_cuts(model, graph, rectangles):
    assert len(graph)==84
    records=[];elements=0;square_tables=0;linear_eigen=0;original_cache={}
    def nine_set(root,base,corners,old_labels,contains_old_root,edge_count,tag):
        nonlocal elements,square_tables,linear_eigen
        assert len(base)+len(corners)+len(old_labels)+int(contains_old_root)==9
        assert len(set(old_labels))==len(old_labels)
        assert len(old_labels)-1-3*int(contains_old_root)==0 # residual at old root
        squares=[];old=[];gamma=[]
        def coordinate(name, expression, zero=False):
            nonlocal square_tables
            if zero:
                model.add(expression==0)
                return 0
            # Norm<=56 bounds every integer coordinate by7 in absolute
            # value. The direct definition bounds it below by-4.
            value=model.new_int_var(-4,7,name)
            model.add(value==expression)
            square=model.new_int_var(0,49,name+'_square')
            model.add_allowed_assignments([value,square],[(v,v*v) for v in range(-4,8)])
            squares.append(square);square_tables+=1
            return value
        for b in range(14):
            count=sum(b in LABELS[w] for w in base)
            count+=sum(flag for corner in corners for w,flag in corner['flags'].items() if b in LABELS[w])
            expression=int(contains_old_root)+int((b^1) in old_labels)+count-1-3*int(b in old_labels)
            old.append(coordinate(f'{tag}_old_{b}',expression,zero=b//2==root//2))
        for w in range(84):
            terms=[graph[w][v] for v in base]
            for ci,corner in enumerate(corners):
                values=[graph[w][v] for v in corner['choices']]
                if all(isinstance(v,int) for v in values) and len(set(values))==1:
                    value=values[0]
                else:
                    value=model.new_bool_var(f'{tag}_adj_{w}_{ci}')
                    model.add_element(corner['selector'],values,value)
                    elements+=len(values)
                terms.append(value)
            membership=int(w in base)+sum(corner['flags'].get(w,0) for corner in corners)
            expression=sum(b in old_labels for b in LABELS[w])+sum(terms)-1-3*membership
            gamma.append(coordinate(f'{tag}_gamma_{w}',expression,zero=root in LABELS[w]))
        norm=56-14*edge_count
        model.add(sum(squares)==norm)
        model.add(sum(old)+sum(gamma)==0)
        model.add(sum(old)==0) # eigen-equation at the original root
        for b in range(14):
            model.add(old[b^1]+sum(gamma[w] for w,p in enumerate(LABELS) if b in p)==-4*old[b])
            linear_eigen+=1
        for b in range(0,14,2):
            # On every triangle L, sum_N(L)d=-6sum_Ld. Integrality and
            # total sum zero give positive/negative mass<=||d||^2/2.
            model.add(12*(old[b]+old[b+1])<=norm)
            model.add(-12*(old[b]+old[b+1])<=norm)
        return old+gamma
    for ri,item in enumerate(rectangles):
        root=item['root'];base=item['base_vertices'];corners=item['corners']
        assert 0<=root<14 and len(base)==4 and len(corners)==4
        assert all(root in LABELS[w] for w in base)
        item['integer_residual_coordinates']=nine_set(root,base,corners,[root],False,sum(item['edges']),f'rotated_residual_{ri}')
        for original in item['old_root_rectangles']:
            key=(root,tuple(original['line']))
            if key not in original_cache:
                original_cache[key]=nine_set(root,original['gamma_vertices'],[],original['old_neighbours'],True,
                    original['edge_count'],f'rotated_old_residual_{root}_{key[1][0]}')
            original['integer_residual_coordinates']=original_cache[key]
        records.append({'root_letter':root,'base_vertices':base,'coordinates':99,
                        'exact_squared_norm':'56-14e','old_star_eigen_equations':15})
    return {'rectangles':len(records),'old_line_rectangles':len(original_cache),'records':records,'element_entries':elements,
            'square_tables':square_tables,'linear_neighbour_eigen_equations':linear_eigen,
            'scope':__doc__}
