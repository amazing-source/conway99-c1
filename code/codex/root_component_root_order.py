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


def root_choice_requirements(value):
    result=set()
    if isinstance(value,dict):
        if value.get('minimum_prism_root') is True:result.add('prisms')
        if value.get('weighted_prism_grid_root') is True:result.add('weighted_prisms_grids')
        if value.get('root_order') in ('prisms','weighted_prisms_grids'):result.add(value['root_order'])
        for child in value.values():result.update(root_choice_requirements(child))
    if isinstance(value,list):
        for child in value:result.update(root_choice_requirements(child))
    return result


def requires_minimum_root(value):
    return bool(root_choice_requirements(value))


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
            'root_order':'prisms',
            'usable_in_arbitrary_low_budget_root_frontier': False, 'cuts': records}


def add_weighted_root_budget(model, graph, template):
    """Choose a root with9s+8g<=504, using the certified3P+4G<=2772."""
    grids=21-len(template['nongrid_edges'])
    cost=sum(graph[u][v] for corners in RECTANGLES.values()
             for u,v in combinations(corners,2) if set(LABELS[u]) & set(LABELS[v]))
    model.add(9*cost+8*grids<=504)
    return {'root_order':'weighted_prisms_grids','weighted_prism_grid_root':True,
            'root_grid_count':grids,'root_prism_budget':(504-8*grids)//9,
            'inequality':'9s(original_root)+8g(original_root)<=504',
            'usable_in_arbitrary_low_budget_root_frontier':False}


def add_weighted_root_comparisons(model, graph, template, rectangles):
    """Choose a GLOBAL minimum of9s+8g; do not also minimize s alone."""
    grids=21-len(template['nongrid_edges'])
    cost=sum(graph[u][v] for corners in RECTANGLES.values()
             for u,v in combinations(corners,2) if set(LABELS[u]) & set(LABELS[v]))
    score=9*cost+8*grids
    groups={}
    for item in rectangles:groups.setdefault(item['root'],[]).append(item)
    records=[]
    def is_grid(value,tag):
        if isinstance(value,int):
            assert value in (0,1,2,4)
            return int(value==4)
        flag=model.new_bool_var(tag)
        model.add(value==4).only_enforce_if(flag)
        model.add(value<=2).only_enforce_if(flag.Not())
        return flag
    for root,items in sorted(groups.items()):
        if len(items)!=15:continue
        originals=items[0]['old_root_rectangles'];assert len(originals)==6
        new_cost=sum(row['shared_label_edges'] for row in originals)
        new_cost+=sum(item['edges'][i] for item in items for i in (0,1,4,5))
        new_grids=sum(is_grid(row['edge_count'],f'weighted_root_{root}_old_grid_{i}')
                      for i,row in enumerate(originals))
        new_grids+=sum(is_grid(sum(item['edges']),f'weighted_root_{root}_grid_{i}')
                       for i,item in enumerate(items))
        model.add(9*new_cost+8*new_grids>=score)
        records.append({'new_root_letter':root,'inequality':'9s(new)+8g(new)>=9s(original)+8g(original)'})
    return {'root_order':'weighted_prisms_grids','weighted_prism_grid_root':True,
            'usable_in_arbitrary_low_budget_root_frontier':False,'cuts':records}
