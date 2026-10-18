"""LAB's signed component identities on the same Gram-free binary Gamma.

For a root line a and a component block P, f is +1/-1 on the two
letters of a inside the component and zero elsewhere. Gamma f vanishes
on Q_a; its restriction d to D_a satisfies
    Gamma[D_a] d = -d,
    <d_P,d_Q> = 8((k/2-1)|P| delta(P,Q)-|P||Q|).
On v in Q_a its boundary sum is
    2*((k/2-1)*1[v in P]-|P|)*sigma_a(v).
These are the common-neighbour identity applied to signed f, whereas
row_neighbor_moments applies it to unsigned rectangle indicators.

The last component is omitted because the sum of all d's is zero.
The code consumes LAB's lemma; it does not rerun any LAB campaign.
"""

from itertools import combinations
from ortools.sat.python import cp_model
from root_component_eigen_equations import add_eigen_equations


def blocks(template, root, line_count):
    given = template['nontrivial_component_groups'][root]
    assert given is not None
    result = [tuple(sorted(p)) for p in given]
    used = [j for part in result for j in part]
    assert len(set(used)) == len(used) and root not in used
    result += [(j,) for j in range(line_count) if j != root and j not in used]
    assert sorted(j for p in result for j in p) == [j for j in range(line_count) if j != root]
    return sorted(result, key=lambda p:(len(p),p))


def add_signed_components(model, graph, labels, template, root_lines, mode='boundary'):
    assert mode in ('norm', 'eigen', 'boundary')
    k = max(max(label) for label in labels)+1
    line_count = k//2
    q_of = [tuple(a//2 for a in label) for label in labels]
    details = []
    for a in sorted(set(root_lines)):
        assert 0 <= a < line_count
        parts = blocks(template, a, line_count)[:-1]
        qa = [w for w, q in enumerate(q_of) if a in q]
        da = [w for w, q in enumerate(q_of) if a not in q]
        sigma = {w: (1 if 2*a in labels[w] else -1) for w in qa}
        columns, bounds, domains, squares = [], [], [], []
        for pi, part in enumerate(parts):
            size = len(part)
            support = [v for v in qa if any(j in part for j in q_of[v])]
            assert len(support) == 4*size
            for w in qa:
                model.add(sum(sigma[v]*graph[w][v] for v in support) == 0)
            values, bs, ds, sq = {}, {}, {}, []
            for w in da:
                if k == 14:
                    total = size-len(set(q_of[w]) & set(part))
                    assert 0 <= total <= 4
                    allowed = [2*p-total for p in range(3) if 0 <= total-p <= 2]
                else:
                    # The Conway uniform component count does not extend to
                    # other k. Only the universal two neighbours per letter.
                    allowed = [-2,-1,0,1,2]
                lo, hi = min(allowed), max(allowed)
                d = lo if lo == hi else model.new_int_var_from_domain(
                    cp_model.Domain.from_values(allowed), f'signed_d_{a}_{pi}_{w}')
                model.add(d == sum(sigma[v]*graph[w][v] for v in support))
                if isinstance(d, int):
                    square = d*d
                else:
                    square = model.new_int_var(0, 4, f'signed_square_{a}_{pi}_{w}')
                    model.add_allowed_assignments([d, square], [(v,v*v) for v in allowed])
                values[w] = d; bs[w] = (lo,hi); ds[w] = allowed; sq.append(square)
            model.add(sum(sq) == 8*size*(line_count-1-size))
            for letter in range(k):
                if letter//2 != a:
                    model.add(sum(values[w] for w in da if letter in labels[w]) == 0)
            columns.append(values); bounds.append(bs); domains.append(ds); squares.append(sq)
        gram_products = 0
        for i, j in combinations(range(len(parts)), 2):
            terms = []
            for w in da:
                x, y = columns[i][w], columns[j][w]
                if isinstance(x, int):
                    terms.append(x*y)
                elif isinstance(y, int):
                    terms.append(y*x)
                else:
                    xy = model.new_int_var(-4,4,f'signed_gram_{a}_{i}_{j}_{w}')
                    model.add_allowed_assignments([x,y,xy],
                        [(u,v,u*v) for u in domains[i][w] for v in domains[j][w]])
                    terms.append(xy); gram_products += 1
            model.add(sum(terms) == -8*len(parts[i])*len(parts[j]))
        info = {'root_line': a, 'independent_components': [list(p) for p in parts],
                'D_size': len(da), 'gram_products': gram_products,
                'conway_parity_domains': k == 14, 'mode': mode}
        if parts and mode != 'norm':
            vertices = da if mode == 'eigen' else list(range(len(labels)))
            subgraph = [[graph[u][v] for v in vertices] for u in vertices]
            values = [[col.get(w,0) for col in columns] for w in vertices]
            bs = [[b.get(w,(0,0)) for b in bounds] for w in vertices]
            offsets = [[0 if w in columns[pi] else
                        2*((line_count-1)*int(any(j in part for j in q_of[w]))-len(part))*sigma[w]
                        for pi, part in enumerate(parts)] for w in vertices]
            info['signed_equations'] = add_eigen_equations(model, subgraph, values, bs,
                                                           eigenvalue=-1, offsets=offsets)
        details.append(info)
    return {'lines': details, 'mode': mode, 'uses_Gram_cover': False,
            'source_lemma': 'LAB 18/10: signed component -1 eigenvectors and their fixed Gram.'}


def template_from_gamma(labels, graph):
    """Extract the component line blocks of a supplied genuine graph for controls."""
    line_count = (max(max(label) for label in labels)+1)//2
    q_of = [tuple(a//2 for a in label) for label in labels]
    groups = []
    for a in range(line_count):
        remaining = set(range(line_count))-{a}
        parts = []
        while remaining:
            start = min(remaining); remaining.remove(start)
            part, stack = {start}, [start]
            while stack:
                b = stack.pop()
                neighbors = {c for c in remaining if any(graph[u][v]
                    for u,q in enumerate(q_of) if set(q)=={a,b}
                    for v,r in enumerate(q_of) if set(r)=={a,c})}
                remaining -= neighbors; part |= neighbors; stack.extend(neighbors)
            if len(part)>1:
                parts.append(sorted(part))
        groups.append(parts)
    return {'nontrivial_component_groups': groups}
