"""Common-neighbour layers on the distance-two vertices of an SRG(v,k,1,2).

Labels are the two neighbours in N(root), with matched letters 2i,2i+1.
The same encoder serves the Conway fixed-Gram model and positive controls.
"""

from collections import Counter
from itertools import combinations


def label_pair_layer(a, b):
    letters_a, letters_b = set(a), set(b)
    roots_a, roots_b = {v // 2 for v in letters_a}, {v // 2 for v in letters_b}
    if roots_a == roots_b:
        return 1
    if letters_a & letters_b:
        return 2
    if roots_a & roots_b:
        return 3
    return 4


def add_c2_layers(model, graph, labels, layer):
    """Add exactly the former signature_joint C2 loop, with variable size."""
    assert 0 <= layer <= 4
    n = len(labels)
    assert len(graph) == n and all(len(row) == n for row in graph)
    products = {}

    def product(a, b):
        if isinstance(a, int):
            assert a in (0, 1)
            return b if a else 0
        if isinstance(b, int):
            assert b in (0, 1)
            return a if b else 0
        key = tuple(sorted((a.index, b.index)))
        if key not in products:
            p = model.new_bool_var(f"p{len(products)}")
            model.add(p <= a)
            model.add(p <= b)
            model.add(p >= a + b - 1)
            products[key] = p
        return products[key]

    counts = Counter()
    for u, v in combinations(range(n), 2):
        which = label_pair_layer(labels[u], labels[v])
        if which <= layer:
            model.add(graph[u][v] + sum(product(graph[u][z], graph[v][z]) for z in range(n))
                      == 2 - len(set(labels[u]) & set(labels[v])))
            counts[which] += 1
    return {"equations": sum(counts.values()), "equations_by_stratum": dict(counts),
            "boolean_products": len(products), "maximum_layer": layer}
