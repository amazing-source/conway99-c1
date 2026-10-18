"""Necessary integer Gram and eigen equations for complete rotated stars.

For a new rectangle Q_ij, its nine-set residual is d_ij=-T 1_Qij,
where T^2=7T and T is the projector numerator in the new coordinates.
Consequently, for two DISTINCT rectangles,
  d_ij dot d_ik = -7 e(Q_ij,Q_ik),
  d_ij dot d_kl = 7(4-e(Q_ij,Q_kl))  when i,j,k,l are distinct.
Thus the dot products are divisible by7, nonpositive in the first case,
and at most28 in the second. Norms<=56 bound them below by-56.
Opposite-pair component identities plus incident nonpositivity also force
orthogonality between the two distinct size12 components at a line.

Optional full Gamma eigen equations impose A d=-4d at the84 original
Gamma vertices. The other15 equations already belong to the residual
model. All cuts are necessary; no adjacency or automorphism is assumed.
"""
from itertools import combinations
from root_component_propagation import LABELS

PRODUCT_DOMAIN_ENCODING = 'python_list_endpoints_v2'


def complete_stars(rectangles):
    groups={}
    for item in rectangles:groups.setdefault(item['root'],[]).append(item)
    result=[]
    for root,items in sorted(groups.items()):
        if len(items)!=15 or not all('integer_residual_coordinates' in r for r in items):continue
        lines=sorted(tuple(line) for line in items[0]['all_lines']);assert len(lines)==6
        vectors={};old_edges={}
        for item in items:
            a,b=sorted((lines.index(tuple(item['base_vertices'][:2])),lines.index(tuple(item['base_vertices'][2:]))))
            vectors[a+1,b+1]=item['integer_residual_coordinates']
        for item in items[0]['old_root_rectangles']:
            pair=(0,lines.index(tuple(item['line']))+1)
            vectors[pair]=item['integer_residual_coordinates'];old_edges[pair]=item['edge_count']
        assert set(vectors)==set(combinations(range(7),2))
        assert all(len(v)==98 for v in vectors.values())
        result.append((root,vectors,old_edges))
    return result


def add_gram_cuts(model,rectangles,mode='incident'):
    assert mode in ('incident','all')
    products={};records=[]
    def product(a,b):
        if isinstance(a,int):return a*b
        if isinstance(b,int):return b*a
        key=tuple(sorted((a.index,b.index)))
        if key not in products:
            # OR-Tools 9.15's pybind repeated-field wrapper does not implement
            # Python negative indexing reliably: domain[-1] can return 0.
            # Copy to actual Python lists before reading interval endpoints.
            da=list(model.proto.variables[a.index].domain);db=list(model.proto.variables[b.index].domain)
            bounds=[x*y for x in (da[0],da[-1]) for y in (db[0],db[-1])]
            value=model.new_int_var(min(bounds),max(bounds),f'rotated_residual_dot_product_{len(products)}')
            model.add_multiplication_equality(value,[a,b]);products[key]=value
        return products[key]
    for root,vectors,_ in complete_stars(rectangles):
        count=0;incident_count=0;entries={}
        for first,second in combinations(sorted(vectors),2):
            incident=bool(set(first)&set(second))
            if mode=='incident' and not incident:continue
            q=model.new_int_var(-8,0 if incident else 4,f'rotated_residual_gram_{root}_{first}_{second}')
            model.add(sum(product(a,b) for a,b in zip(vectors[first],vectors[second]))==7*q)
            entries[first,second]=q
            count+=1;incident_count+=int(incident)
        records.append({'root':root,'gram_entries':count,'incident_nonpositive_entries':incident_count})
        next(item for item in rectangles if item['root']==root)['residual_gram_entries']=entries
    return {'mode':mode,'integer_products':len(products),'roots':records,'scope':__doc__,
            'product_domain_encoding':PRODUCT_DOMAIN_ENCODING}


def add_eigen_cuts(model,graph,rectangles,count_per_root):
    assert count_per_root>0
    products={};records=[];equations=0
    def product(edge,value):
        if isinstance(edge,int):return edge*value
        if isinstance(value,int):return value*edge
        key=(edge.index,value.index)
        if key not in products:
            domain=list(model.proto.variables[value.index].domain)
            p=model.new_int_var(min(0,domain[0]),max(0,domain[-1]),f'rotated_residual_eigen_product_{len(products)}')
            model.add(p==value).only_enforce_if(edge)
            model.add(p==0).only_enforce_if(edge.Not());products[key]=p
        return products[key]
    for root,vectors,old_edges in complete_stars(rectangles):
        # The known old-line nongrids are tried first. In a size18 component
        # any two of its three nonzero rectangle vectors are independent.
        old=[pair for pair in sorted(old_edges)
             if not isinstance(old_edges[pair],int) or old_edges[pair]<4]
        candidates=old+[pair for pair in sorted(vectors) if pair not in old_edges]
        selected=candidates[:count_per_root]
        for pair in selected:
            vector=vectors[pair];old_values=vector[:14];gamma=vector[14:]
            for u in range(84):
                model.add(sum(old_values[a] for a in LABELS[u])+sum(product(graph[u][v],gamma[v]) for v in range(84))==-4*gamma[u])
                equations+=1
        records.append({'root':root,'selected_rectangles':[list(p) for p in selected]})
    return {'count_per_root':count_per_root,'new_gamma_eigen_equations':equations,
            'edge_integer_products':len(products),'roots':records,'scope':__doc__,
            'product_domain_encoding':PRODUCT_DOMAIN_ENCODING}


def add_gram_kernel_cuts(model, rectangles):
    """Expose necessary Gram relations already implied by full residual vectors.

    R_pq = dot(delta_p,delta_q)/7, R_pp = 8-2e_p. For every
    root line i, sum_{q incident i} delta_q=0, hence R times its
    incidence column is zero. Every two-by-two principal minor is PSD.
    Since the rectangle incidence columns have squared norm four and
    T is seven times a projector, 0<=R<=28I and sum_q R_pq^2<=28R_pp.
    No component minimum, fixed Gram, or new-root prism budget is used.
    """
    from ortools.sat.python import cp_model
    records = []
    for root,vectors,old_edges in complete_stars(rectangles):
        items = [item for item in rectangles if item['root']==root]
        first = items[0]
        entries = first['residual_gram_entries']
        assert len(entries)==210
        lines = sorted(tuple(line) for line in first['all_lines'])
        edge_counts = dict(old_edges)
        for item in items:
            a,b = sorted((lines.index(tuple(item['base_vertices'][:2])),
                          lines.index(tuple(item['base_vertices'][2:]))))
            edge_counts[a+1,b+1] = sum(item['edges'])
        diagonals = {}
        for pair in sorted(vectors):
            d = model.new_int_var_from_domain(cp_model.Domain.from_values([0,4,6,8]),
                                             f'rotated_gram_diagonal_{root}_{pair}')
            model.add(d==8-2*edge_counts[pair]); diagonals[pair]=d
        for pair in sorted(vectors):
            for line in range(7):
                terms = [diagonals[pair] if other==pair else entries[tuple(sorted((pair,other)))]
                         for other in vectors if line in other]
                model.add(sum(terms)==0)
        allowed = [(a,b,q) for a in (0,4,6,8) for b in (0,4,6,8)
                   for q in range(-8,5) if q*q<=a*b]
        for (a,b),value in entries.items():
            model.add_allowed_assignments([diagonals[a],diagonals[b],value],allowed)
        squares = {}
        for (a,b),value in entries.items():
            square = model.new_int_var(0,64,f'rotated_gram_energy_square_{root}_{a}_{b}')
            model.add_allowed_assignments([value,square],[(v,v*v) for v in range(-8,5)])
            squares[a,b] = square
        for pair,d in diagonals.items():
            square = model.new_int_var(0,64,f'rotated_gram_energy_diagonal_{root}_{pair}')
            model.add_allowed_assignments([d,square],[(v,v*v) for v in (0,4,6,8)])
            model.add(square+sum(s for (a,b),s in squares.items() if pair in (a,b))<=28*d)
        records.append({'root':root,'kernel_equations':147,'principal_minor_tables':210,
                        'spectral_row_energy_bounds':21})
    return {'roots':records,'scope':add_gram_kernel_cuts.__doc__}


def unsafe_product_reports(value):
    """Find historical product metadata lacking the corrected encoding stamp."""
    if isinstance(value, dict):
        uses_products = (value.get('edge_integer_products',0)>0 or
            (value.get('integer_products',0)>0 and 'Necessary integer Gram' in value.get('scope','')))
        if uses_products and value.get('product_domain_encoding') != PRODUCT_DOMAIN_ENCODING:
            yield value
        for child in value.values():
            yield from unsafe_product_reports(child)
    elif isinstance(value, list):
        for child in value:
            yield from unsafe_product_reports(child)
