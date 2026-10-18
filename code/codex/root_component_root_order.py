"""Choose a globally minimal prism-incidence root, with explicit scope.

Let s(x) be the sum of t(L) over the seven lines through x. We may choose
the original root x to minimize s over all99 vertices. The existing
average bound gives s(x)<=51. At every complete transported star y we
can then impose s(y)>=s(x), with both counts computed from actual edges.

This is a ROOT CHOICE, not a necessary inequality at an arbitrary root.
An exclusion using it cannot be transported to every root of budget<=51.
It is useful for closing a complete cover of globally minimal roots.
"""
from itertools import combinations
from root_component_propagation import LABELS, RECTANGLES


def requires_minimum_root(value):
    if isinstance(value,dict):
        if value.get('minimum_prism_root') is True or value.get('requires_globally_minimal_root') is True:
            return True
        return any(requires_minimum_root(v) for v in value.values())
    if isinstance(value,list):
        return any(requires_minimum_root(v) for v in value)
    return False


def arbitrary_root_rejection(report):
    from root_component_rotated_gram import unsafe_product_reports
    if any(unsafe_product_reports(report)):
        return 'WITHDRAWN_PRODUCT_DOMAIN_ENCODING'
    if requires_minimum_root(report):
        return 'REQUIRES_GLOBALLY_MINIMUM_ROOT'
    return None


def add_minimum_root_cuts(model, graph, rectangles):
    old_cost = sum(graph[u][v] for corners in RECTANGLES.values()
                   for u,v in combinations(corners,2) if set(LABELS[u]) & set(LABELS[v]))
    groups = {}
    for item in rectangles:
        groups.setdefault(item['root'], []).append(item)
    records = []
    for root, items in sorted(groups.items()):
        if len(items) != 15:
            continue
        originals = items[0]['old_root_rectangles']
        assert len(originals) == 6
        new_cost = sum(row['shared_label_edges'] for row in originals)
        new_cost += sum(item['edges'][i] for item in items for i in (0,1,4,5))
        model.add(new_cost >= old_cost)
        records.append({'new_root_letter': root, 'inequality': 's(new_root)>=s(original_root)'})
    return {'scope': __doc__, 'requires_globally_minimal_root': True,
            'usable_in_arbitrary_low_budget_root_frontier': False, 'cuts': records}
