"""Vertexwise rectangle sums of the SRG common-neighbour equations.

Z=Gamma P, where each column of P indicates one four-vertex rectangle.
For every SRG(v,k,1,2), Gamma^2+Gamma=(k-2)I+2J-B^t B, hence
    (Gamma Z+Z)[w,F]=(k-2)[w in F]+8-2|q(w) intersection F|.
This is k+2 on the own rectangle, 6 on an intersecting rectangle, 8 otherwise.
The aggregate Z^t Z+P^t Z moments follow by summing these rows in a rectangle.
No symmetry, Gram, prism budget or minimal-root assumption is used.

All Boolean-times-integer products use bounds from Python state lists.
No OR-Tools proto-domain indexing is used.
"""

from itertools import combinations


def coordinates_for_catalogue(catalogue, template):
    """Recover the independent H coordinates even for a LAB DFS catalogue.

The component incidence matrix C gives C h_w=0 for every row of H.
Its nonpivot coordinates determine h_w. Since Gamma acts on vertices,
the same relations hold on Gamma H+4H. Checking its nonpivot columns
therefore checks all columns. This uses C1 and k=14, not a fixed Gram.
"""
    if 'free_coordinates' in catalogue:
        return catalogue['free_coordinates']
    import sympy as sp
    rectangles=list(combinations(range(7),2))
    rows=[]
    assert len(template['nontrivial_component_groups'])==7
    for a,groups in enumerate(template['nontrivial_component_groups']):
        assert groups is not None
        used={j for part in groups for j in part}
        parts=list(groups)+[[j] for j in range(7) if j!=a and j not in used]
        for part in parts:
            support={tuple(sorted((a,j))) for j in part}
            rows.append([int(q in support) for q in rectangles])
    _,pivots=sp.Matrix(rows).rref()
    free=[i for i in range(21) if i not in pivots]
    assert len(free)==catalogue['free_dimension']
    # Validate exactly the relation used by this compression on the supplied
    # states; this is not a re-enumeration or completeness audit of LAB's DFS.
    supports=[[i for i,c in enumerate(row) if c] for row in rows]
    for q,item in zip(rectangles,catalogue['row_types']):
        assert item['rectangle']==list(q)
        base=[3*int(q==f)+1-len(set(q)&set(f)) for f in rectangles]
        for z in item['states']:
            h=[w-v for w,v in zip(base,z)]
            assert all(sum(h[i] for i in support)==0 for support in supports)
    return free


def add_row_moments(model, graph, labels, row_types, coordinates, fixed=None):
    k = max(max(label) for label in labels)+1
    rectangles = list(combinations(range(k//2), 2))
    assert [item['rectangle'] for item in row_types] == [list(q) for q in rectangles]
    n = len(labels)
    coordinates = sorted(set(coordinates))
    assert all(0 <= j < len(rectangles) for j in coordinates)
    q_of = [tuple(a//2 for a in label) for label in labels]
    members = [[w for w, q in enumerate(q_of) if q == f] for f in rectangles]
    assert all(len(group) == 4 for group in members)
    if any(not item['states'] for item in row_types):
        model.add(False)
        return {'coordinates': coordinates, 'empty_row_catalogue': True}
    z = {}
    bounds = {}
    for qi, group in enumerate(members):
        for j in coordinates:
            vals = [state[j] for state in row_types[qi]['states']]
            lo, hi = min(vals), max(vals)
            assert 0 <= lo <= hi <= 4
            for w in group:
                bounds[w, j] = (lo, hi)
                z[w, j] = lo if lo == hi else model.new_int_var(lo, hi, f'row_z_{w}_{j}')
                model.add(z[w, j] == sum(graph[w][v] for v in members[j]))
    products = equations = 0
    for w in range(n):
        for j in coordinates:
            terms = [z[w, j]]
            for v in range(n):
                if v == w:
                    continue
                edge = fixed[w][v] if fixed is not None else graph[w][v]
                count = z[v, j]
                if isinstance(edge, int):
                    if edge:
                        terms.append(count)
                elif isinstance(count, int):
                    if count:
                        terms.append(count*edge)
                else:
                    lo, hi = bounds[v, j]
                    term = model.new_int_var(0, hi, f'row_ez_{w}_{v}_{j}')
                    model.add(term == count).only_enforce_if(edge)
                    model.add(term == 0).only_enforce_if(edge.Not())
                    terms.append(term)
                    products += 1
            target = (k-2)*int(q_of[w] == rectangles[j])+8-2*len(set(q_of[w]) & set(rectangles[j]))
            model.add(sum(terms) == target)
            equations += 1
    return {'coordinates': coordinates, 'rectangles': [list(rectangles[j]) for j in coordinates],
            'equations': equations, 'boolean_integer_products': products,
            'all_rectangle_coordinates': len(coordinates) == len(rectangles),
            'domain_bounds_source': 'Explicit integer state lists, no proto-domain reads.'}
