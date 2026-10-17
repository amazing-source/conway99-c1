"""Safe first-component relabellings inside the stabilizer of a fixed Gram.

A root permutation must preserve every prescribed component group, fix the
selected root and its selected component, and fix the entire Gram entrywise
under the induced rectangle permutation. Its restriction to component pairs
can then be combined with the existing mate flips and root-mate swap.
"""

from functools import lru_cache
from root_component_quotient import graph_automorphisms


def normalized(groups):
    return tuple(tuple(sorted(tuple(sorted(part)) for part in row)) for row in groups)


@lru_cache(maxsize=None)
def template_permutations(mask, groups):
    result=[]
    for permutation in graph_automorphisms(mask):
        image=[[] for _ in range(7)]
        for root,row in enumerate(groups):
            image[permutation[root]]=[[permutation[j] for j in part] for part in row]
        if normalized(image)==groups:
            result.append(tuple(permutation))
    return tuple(result)


def first_component_stabilizer(template, matrix):
    _,root,part=min((-len(part),root,tuple(sorted(part)))
                   for root,parts in enumerate(template['nontrivial_component_groups']) for part in parts)
    edges=[tuple(e) for e in template['nongrid_edges']]
    edge_index={edge:i for i,edge in enumerate(edges)}
    raw=[[int(x) for x in row] for row in matrix.tolist()]
    retained=[];global_stabilizer=[]
    for permutation in template_permutations(template['graph_mask'],normalized(template['nontrivial_component_groups'])):
        ep=[edge_index[tuple(sorted((permutation[a],permutation[b])))] for a,b in edges]
        if all(raw[i][j]==raw[ep[i]][ep[j]] for i in range(len(edges)) for j in range(len(edges))):
            global_stabilizer.append(permutation)
            if permutation[root]==root and {permutation[j] for j in part}==set(part):
                retained.append(permutation)
    restrictions=sorted({tuple(part.index(p[j]) for j in part) for p in retained})
    assert tuple(range(len(part))) in restrictions
    # An exhaustive stabilizer must induce a group, not a selected set of maps.
    assert all(tuple(p[q[i]] for i in range(len(part))) in restrictions for p in restrictions for q in restrictions)
    return {'root_line':root,'part':list(part),'root_permutations':[list(p) for p in retained],
            'global_root_permutations':[list(p) for p in global_stabilizer],
            'part_permutations':[list(p) for p in restrictions],
            'complete_template_and_gram_stabilizer_checked':True}


def add_root_orbit_minimum(model, components, action, canonical_map):
    """Choose the smallest possible first code over the entire root orbit.

For any completion minimize its first-component code over all Gram-preserving
root relabellings and all mate flips. Every component that can be moved to
that position has normalized image at least as large. The normalized image
is invariant under every mate flip, so remaining mate-lex choices are safe.
    """
    from root_component_local_tables import component_pair_relabel_map
    from ortools.sat.python import cp_model
    root,part=action['root_line'],action['part']
    first=next(c for c in components if c['root']==root and c['part']==part)
    base=len(first['record']['internal_matchings'])
    def key(code):return code[0]*base*base+code[1]*base+code[2]
    first_key=key(first['selectors'])
    counts=[]
    for component in components:
        if component is first:continue
        pair_images=sorted({tuple(part.index(p[j]) for j in component['part'])
                            for p in action['global_root_permutations']
                            if p[component['root']]==root and {p[j] for j in component['part']}==set(part)})
        if not pair_images:continue
        maps=[component_pair_relabel_map(component['record'],image) for image in pair_images]
        rows=[]
        for code in component['codes']:
            images=[(pp[code[0]],mm[code[1]],mm[code[2]]) for pp,mm in maps]
            assert all(image in canonical_map for image in images), 'The entire filtered code domain must transform with the fixed Gram.'
            rows.append(list(code)+[min(key(canonical_map[image]) for image in images)])
        target=model.new_int_var_from_domain(cp_model.Domain.from_values(sorted({row[-1] for row in rows})),
                                            f'root_orbit_code_{component["root"]}_{component["part"][0]}')
        model.add_allowed_assignments(component['selectors']+[target],rows)
        model.add(first_key<=target)
        counts.append({'root_line':component['root'],'part':component['part'],
                       'pair_relabelings':len(pair_images),'table_rows':len(rows)})
    return {'compared_components':counts,'whole_fixed_gram_stabilizer_order':len(action['global_root_permutations']),
            'normalization':'First component is minimum over its whole root orbit and all mate flips.'}
