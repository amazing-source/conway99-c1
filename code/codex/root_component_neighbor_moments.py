"""Nonnegative rectangle moments without a Gram cover or a rank hypothesis.

For Q a root rectangle, z_w=|N_Gamma(w) intersect Q| and e_Q its internal
edge count. The six common-neighbour equations imply
  sum_w binom(z_w,2) + e_Q = 8.
For distinct rectangles Q,F, the sixteen cross equations imply
  sum_w z_Q(w)*z_F(w) + e(Q,F) = 24 (one root line in common), 32 otherwise.
These identities hold for every SRG(v,k,1,2) root reduction. They are
explicit aggregates of the existing pair equations, intended to improve
propagation, not new restrictions on the class of admissible graphs.
"""

from itertools import combinations, product


def root_rectangles(labels):
    labels = [tuple(p) for p in labels]
    k = max(a for p in labels for a in p) + 1
    assert k >= 4 and k % 2 == 0
    assert set(labels) == {p for p in combinations(range(k), 2) if p[1] != (p[0] ^ 1)}
    assert len(set(labels)) == len(labels)
    rectangles = {q: [w for w, p in enumerate(labels) if tuple(a // 2 for a in p) == q]
                  for q in combinations(range(k // 2), 2)}
    assert all(len(ws) == 4 for ws in rectangles.values())
    return k, rectangles


def add_neighbor_moments(model, labels, graph, *, mixed=False, selected=None):
    """Return the column counts and exact aggregation metadata.

No OR-Tools domain endpoints are read. All bounds come from the letter
quotas; each nonlinear expression uses its complete finite value table.
"""
    k, rectangles = root_rectangles(labels)
    if selected is not None:
        wanted = {tuple(sorted(q)) for q in selected}
        assert wanted <= rectangles.keys()
        rectangles = {q: ws for q, ws in rectangles.items() if q in wanted}
    assert rectangles
    n = len(labels)
    assert len(graph) == n and all(len(row) == n for row in graph)
    before_variables = len(model.proto.variables)
    before_constraints = len(model.proto.constraints)
    columns, upper_bounds, histogram_costs = {}, {}, {}
    local_edges = {}
    for q, corners in rectangles.items():
        counts, uppers, costs = [], [], []
        for w, label in enumerate(labels):
            same_line = bool(set(a // 2 for a in label) & set(q))
            upper = 2 if same_line else 4
            entries = [graph[w][u] for u in corners]
            if all(isinstance(x, int) for x in entries):
                z = sum(entries)
                assert 0 <= z <= upper
                cost = z * (z - 1) // 2
            else:
                z = model.new_int_var(0, upper, f'neighbor_count_{q}_{w}')
                cost = model.new_int_var(0, upper * (upper - 1) // 2, f'neighbor_pairs_{q}_{w}')
                model.add(z == sum(entries))
                model.add_allowed_assignments([z, cost], [(v, v * (v - 1) // 2)
                                                          for v in range(upper + 1)])
            counts.append(z)
            uppers.append(upper)
            costs.append(cost)
        e = sum(graph[u][v] for u, v in combinations(corners, 2))
        model.add(sum(costs) + e == 8)
        model.add(sum(counts) == 4 * (k - 2))
        sharing = [w for w, label in enumerate(labels)
                   if len(set(a // 2 for a in label) & set(q)) == 1]
        model.add(sum(counts[w] for w in sharing) + 4 * e == 16)
        columns[q], upper_bounds[q], histogram_costs[q], local_edges[q] = counts, uppers, costs, e
    mixed_count = 0
    if mixed:
        for q, f in combinations(rectangles, 2):
            products = []
            for w, (a, b) in enumerate(zip(columns[q], columns[f])):
                if isinstance(a, int) or isinstance(b, int):
                    value = a * b
                else:
                    ua, ub = upper_bounds[q][w], upper_bounds[f][w]
                    value = model.new_int_var(0, ua * ub, f'neighbor_mixed_{q}_{f}_{w}')
                    model.add_allowed_assignments([a, b, value],
                                                  [(x, y, x * y) for x, y in product(range(ua + 1), range(ub + 1))])
                products.append(value)
            cross_edges = sum(graph[u][v] for u in rectangles[q] for v in rectangles[f])
            model.add(sum(products) + cross_edges == (24 if set(q) & set(f) else 32))
            mixed_count += 1
    metadata = {'scope': __doc__, 'root_degree': k, 'rectangles': len(rectangles),
                'diagonal_count_identities': len(rectangles), 'mixed_count_identities': mixed_count,
                'added_variables': len(model.proto.variables) - before_variables,
                'added_constraints': len(model.proto.constraints) - before_constraints,
                'uses_gram_cover': False, 'rank_assumption': None, 'assumes_minimum_line_components': False,
                'nonlinearity_encoding': 'Exact finite tables; no multiplication constraints or domain introspection.'}
    return {'columns': columns, 'costs': histogram_costs, 'local_edges': local_edges,
            'upper_bounds': upper_bounds, 'info': metadata}
