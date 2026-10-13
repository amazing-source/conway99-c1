"""Necessary row moments of the missing common-neighbour equations.

For A=[[B,D],[D^t,E]], r=E1 and R_uv=(D^t D)_uv, any SRG(99,14,1,2)
satisfies, for each u in M,
    sum_{v != u} R_uv + sum_w E_uw r_w = 2(|M|-1).
Only O(|M|^2) integer-times-Boolean products are needed. These are not
the complete mixed or residual equations and do not certify a graph.
"""
from itertools import combinations


def add_moments(model, M, edge):
    indices = {v.name: i for i, v in enumerate(model.proto.variables)
               if v.name.startswith('overlap')}
    overlap = {(u, v): model.get_int_var_from_proto_index(indices[f'overlap{u}_{v}'])
               for u, v in combinations(M, 2)}
    # C neighbours alone give these safe bounds; deliberately avoid tighter
    # bounds that would need further profile-specific hypotheses.
    upper = {u: 9 if u in (37, 38) else 10 for u in M}
    degree = {u: model.new_int_var(0, upper[u], f'moment_degree{u}') for u in M}
    for u in M:
        model.add(degree[u] == sum(edge(u, v) for v in M if u != v))
    products = {}
    for u in M:
        for w in M:
            if u == w:
                continue
            x = edge(u, w)
            if isinstance(x, int):
                products[u, w] = degree[w] if x else 0
            else:
                y = model.new_int_var(0, upper[w], f'moment_product{u}_{w}')
                model.add(y == degree[w]).only_enforce_if(x)
                model.add(y == 0).only_enforce_if(x.Not())
                products[u, w] = y
        model.add(sum(overlap[tuple(sorted((u, v)))] for v in M if v != u)
                  + sum(products[u, w] for w in M if w != u) == 2*(len(M)-1))
    return dict(moment_rows=len(M), moment_degree_variables=len(degree),
                moment_product_variables=sum(not isinstance(x, int) for x in products.values()),
                moment_identity='sum(v!=u,R_uv)+sum(w,E_uw*r_w)=2*(m-1)')
