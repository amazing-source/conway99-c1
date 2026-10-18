"""Keep the individual common-neighbour counts for the six pairs of each rectangle.

Rectangle moments count their sum. Here the same binary Gamma allocates
the common neighbours to the six specific corner pairs. This is exactly
the intrarectangle C2 layer, with no Gram or prism budget.
"""

from itertools import combinations


def add_corner_c2(model, graph, labels, coordinates=None):
    k = max(max(label) for label in labels)+1
    rectangles = list(combinations(range(k//2),2))
    selected = set(range(len(rectangles)) if coordinates is None else coordinates)
    assert selected <= set(range(len(rectangles)))
    q_of = [tuple(a//2 for a in label) for label in labels]
    products = {}
    def product(a,b):
        if isinstance(a,int):
            return b if a else 0
        if isinstance(b,int):
            return a if b else 0
        key = tuple(sorted((a.index,b.index)))
        if key[0] == key[1]:
            return a
        if key not in products:
            value = model.new_bool_var(f'corner_c2_product_{len(products)}')
            model.add(value <= a); model.add(value <= b)
            model.add(value >= a+b-1)
            products[key] = value
        return products[key]
    equations = 0
    for qi,q in enumerate(rectangles):
        if qi not in selected:
            continue
        members = [w for w,r in enumerate(q_of) if r == q]
        assert len(members) == 4
        for u,v in combinations(members,2):
            model.add(graph[u][v]+sum(product(graph[u][w],graph[v][w]) for w in range(len(labels)))
                      == 2-len(set(labels[u]) & set(labels[v])))
            equations += 1
    return {'rectangles':len(selected),'equations':equations,'boolean_products':len(products),
            'individual_C2_layer':1,'uses_Gram_cover':False}
