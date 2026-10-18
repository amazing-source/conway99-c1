"""Individual C2 equations between every label and every grid corner.

C1 already includes the equations with the root and its letters. Adding
these pairs completes C2 against all nine vertices of each root grid.
The implementation uses C2 directly; it does not assume perfect grid
domination for other SRG(v,k,1,2), in particular SRG(243,22,1,2).
"""

from itertools import combinations


def add_grid_c2(model, graph, labels, grid_rectangles, row_types=None):
    k = max(max(label) for label in labels)+1
    rectangles = list(combinations(range(k//2), 2))
    grids = {tuple(q) for q in grid_rectangles}
    assert grids <= set(rectangles)
    n = len(labels)
    q_of = [tuple(a//2 for a in label) for label in labels]
    members = [[w for w, q in enumerate(q_of) if q == f] for f in rectangles]
    effective = [list(row) for row in graph]
    fixed = {}
    def set_constant(u, v, value):
        key = tuple(sorted((u, v)))
        if key in fixed:
            if fixed[key] != value:
                model.add(False)
            return
        model.add(graph[u][v] == value)
        effective[u][v] = effective[v][u] = value
        fixed[key] = value
    for q, group in zip(rectangles, members):
        if q in grids:
            for u, v in combinations(group, 2):
                set_constant(u, v, int(bool(set(labels[u])&set(labels[v]))))
    if row_types is not None:
        assert [item['rectangle'] for item in row_types] == [list(q) for q in rectangles]
        for group, item in zip(members, row_types):
            if not item['states']:
                model.add(False)
                continue
            for j, target in enumerate(members):
                if all(state[j] == 0 for state in item['states']):
                    for u in group:
                        for v in target:
                            if u != v:
                                set_constant(u, v, 0)
    corners = {w for w, q in enumerate(q_of) if q in grids}
    products = {}
    def product(a, b):
        if isinstance(a, int):
            return b if a else 0
        if isinstance(b, int):
            return a if b else 0
        key = tuple(sorted((a.index, b.index)))
        if key[0] == key[1]:
            return a
        if key not in products:
            value = model.new_bool_var(f'grid_c2_product_{len(products)}')
            model.add(value <= a); model.add(value <= b)
            model.add(value >= a+b-1)
            products[key] = value
        return products[key]
    equations = 0
    for u, v in combinations(range(n), 2):
        if u not in corners and v not in corners:
            continue
        model.add(effective[u][v]+sum(product(effective[u][w], effective[v][w]) for w in range(n))
                  == 2-len(set(labels[u])&set(labels[v])))
        equations += 1
    return {'grids': len(grids), 'grid_corners': len(corners), 'equations': equations,
            'boolean_products': len(products), 'known_constant_edges': len(fixed),
            'uses_Gram_cover': False, 'perfect_domination_assumed': False}
