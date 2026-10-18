"""Exact principal-block assumptions for Gram-free count/adjacency models.

A branch fixes only a named principal block of R. For rectangle incidence
P and neighbour counts Z=Gamma P, R=P^t H=4W-P^t Z, with
W_FG=3[F=G]+1-|F intersect G|. Every unmentioned entry remains free.
"""

from copy import deepcopy
from itertools import combinations_with_replacement


def canonical_block(block):
    import sympy as sp
    from root_component_gram_enumeration import integer_psd
    columns = [tuple(q) for q in block.get('coordinate_rectangles', block.get('rectangles', []))]
    raw = block.get('principal_block', block.get('matrix'))
    assert columns and len(set(columns)) == len(columns)
    assert all(len(q) == 2 and 0 <= q[0] < q[1] <= 6 for q in columns)
    assert len(raw) == len(columns) and all(len(row) == len(columns) for row in raw)
    assert all(type(x) is int for row in raw for x in row)
    S = sp.Matrix(raw)
    assert S == S.T and integer_psd(raw)
    return {'rectangles': [list(q) for q in columns], 'matrix': raw}


def energy_predicate(block):
    """Exact Schur bound for a restricted signature, including singular S."""
    import sympy as sp
    block = canonical_block(block)
    S = sp.Matrix(block['matrix'])
    anchors = list(S.rref()[1])
    if not anchors:
        return lambda h: not any(h)
    T = S.extract(anchors, anchors)
    det = int(T.det())
    adj = (T.inv(method='DM') * det).applyfunc(int)
    lift = [[int(x) for x in row] for row in (S[:, anchors] * adj).tolist()]
    ai = [[int(x) for x in row] for row in adj.tolist()]
    def admissible(h):
        z = [h[j] for j in anchors]
        if any(det * h[i] != sum(a*b for a,b in zip(row,z)) for i,row in enumerate(lift)):
            return False
        energy = sum(z[i]*ai[i][j]*z[j] for i in range(len(z)) for j in range(len(z)))
        return 2 * energy <= 5 * det
    return admissible


def filter_catalogue(catalogue, block):
    """Return a CONDITIONAL catalogue, unusable without the same block."""
    assert catalogue['status'] == 'ROW_CATALOGUE_COMPLETE'
    block = canonical_block(block)
    admissible = energy_predicate(block)
    result = deepcopy(catalogue)
    rectangles = [tuple(t['rectangle']) for t in result['row_types']]
    selected = [rectangles.index(tuple(q)) for q in block['rectangles']]
    counts = []
    for item, q in zip(result['row_types'], rectangles):
        before = len(item['states'])
        item['states'] = [z for z in item['states'] if admissible([
            3*int(q == rectangles[j]) + 1 - len(set(q) & set(rectangles[j])) - z[j]
            for j in selected])]
        item['state_count'] = len(item['states'])
        counts.append({'rectangle':list(q), 'before':before, 'after':len(item['states'])})
    result['status'] = 'CONDITIONAL_ROW_CATALOGUE_COMPLETE'
    result['partial_gram'] = block
    return result, counts


def add_count_block(model, counts, rectangles, block):
    """counts[F][G] is sum of z_wG over the four vertices of F."""
    block = canonical_block(block)
    rectangles = [tuple(q) for q in rectangles]
    selected = [rectangles.index(tuple(q)) for q in block['rectangles']]
    for a,b in combinations_with_replacement(range(len(selected)),2):
        i,j = selected[a],selected[b]
        constant = 4*(3*int(i==j)+1-len(set(rectangles[i]) & set(rectangles[j])))
        model.add(counts[i][j] == constant - block['matrix'][a][b])
    return {'fixed_principal_entries':len(selected)*(len(selected)+1)//2,
            'block':block, 'full_Gram_fixed':False, 'all_other_Gram_entries_free':True}


def add_graph_block(model, graph, labels, block):
    """The same assumptions directly on the shared binary adjacency."""
    block = canonical_block(block)
    rectangles = sorted({tuple(a//2 for a in label) for label in labels})
    members = [[w for w,label in enumerate(labels) if tuple(a//2 for a in label)==q]
               for q in rectangles]
    selected = [rectangles.index(tuple(q)) for q in block['rectangles']]
    counts = [[None]*len(rectangles) for _ in rectangles]
    for i,j in combinations_with_replacement(selected,2):
        counts[i][j] = sum(graph[u][v] for u in members[i] for v in members[j])
    return add_count_block(model,counts,rectangles,block)


def test_block(template, coordinates, matrix, *, catalogue=None):
    """Public exact filter; only a named block, with all other entries free.

Supply a cached complete catalogue for repeated calls. Without one, its
enumeration is attempted only through free dimension 7.
"""
    import sympy as sp
    from root_component_z_distribution import RECTANGLES,row_catalogue
    from root_component_partial_gram_microscope import inspect_block
    block=canonical_block({'rectangles':coordinates,'matrix':matrix})
    if catalogue is None:catalogue=row_catalogue(template,max_free=7)
    if catalogue['status']!='ROW_CATALOGUE_COMPLETE':
        return {'status':'UNSUPPORTED_CATALOGUE','catalogue_status':catalogue['status']}
    rows=[];right=[]
    for root,nontrivial in enumerate(template['nontrivial_component_groups']):
        used={j for part in nontrivial for j in part}
        parts=[tuple(p) for p in nontrivial]+[(j,) for j in range(7) if j!=root and j not in used]
        for part in parts:
            support={tuple(sorted((root,j))) for j in part}
            rows.append([int(q in support) for q in RECTANGLES])
            right.append([3*int(q in support)+len(part)*(1-int(root in q))-sum(j in part for j in q)
                          for q in RECTANGLES])
    assert catalogue['component_matrix']==rows and catalogue['right_sides']==right
    selected=[RECTANGLES.index(tuple(q)) for q in block['rectangles']]
    S=sp.Matrix(block['matrix']);checks=[]
    for own,qi in enumerate(selected):
        q=RECTANGLES[qi]
        candidates=sorted({tuple(3*int(q==RECTANGLES[j])+1-len(set(q)&set(RECTANGLES[j]))-z[j]
                                 for j in selected) for z in catalogue['row_types'][qi]['states']})
        checked=inspect_block(S,list(range(len(selected))),own,candidates)
        checked['rectangle']=list(q);checks.append(checked)
        if checked['status']=='EXCLUDED_PARTIAL_BLOCK':
            return {'status':'EXCLUDED_PARTIAL_BLOCK','block':block,'certificate':checked,
                    'full_Gram_required':False,'whole_template_excluded':False}
    return {'status':'PASSES','block':block,
            'rectangle_domain_sizes':[len(c['projected_domain']) for c in checks],
            'full_Gram_required':False,'whole_template_excluded':False}
