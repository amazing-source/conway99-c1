"""Expose intersections of transported grids with fixed root grids.

Every induced 3x3 grid D in a Conway graph satisfies A1_D=1+3*1_D.
Thus each exterior vertex has exactly one neighbour in D. Two distinct
grids intersect in zero vertices, one vertex or one whole triangle:
two adjacent intersection vertices force their unique common neighbour;
two nonadjacent intersection vertices force their two common neighbours.
Inside K3 square K3 these closures generate the full grid as soon as the
intersection is not contained in one row or one column.

A transported nine-set is based at an original neighbour a. It omits
the original root and contains no other original neighbour. If it is a
grid, its intersection with an old root grid not containing a therefore
lies in the old four-corner square, which contains no triangle: at most
one corner is shared. If the old grid contains a, the intersection is
already fixed by the four base vertices, and no new corner can lie in it.
These cuts require an actual grid flag; they do not apply to nongrids.
"""
from collections import Counter
from itertools import permutations
from root_component_propagation import LABELS, RECTANGLES


def grid_corner_rows(item,old_grids):
    """All ordered four-corner placements of a transported grid.

    The old root and its fourteen neighbours are outside the new grid,
    except for its root a. Unique domination at those fourteen vertices
    forces its four bases to use four other labels, and its four corners
    to form a perfect matching on the eight remaining labels. An old
    grid cannot contain two of these corners (they would be nonadjacent).
    """
    letter=item['root']
    base_letters=[b for w in item['base_vertices'] for b in LABELS[w] if b!=letter]
    assert len(base_letters)==len(set(base_letters))==4
    assert all(letter in LABELS[w] for w in item['base_vertices'])
    remaining=sorted(set(range(14))-{letter,letter^1}-set(base_letters))
    assert len(remaining)==8
    lookup={p:w for w,p in enumerate(LABELS)}
    domains=[set(c['choices']) for c in item['corners']]
    grids=set(old_grids)
    def matchings(vertices):
        if not vertices:
            yield ()
            return
        u=vertices[0]
        for j in range(1,len(vertices)):
            v=vertices[j]
            if v==(u^1):continue
            for tail in matchings(vertices[1:j]+vertices[j+1:]):
                yield (lookup[u,v],)+tail
    rows=[];total=0;intersection_rejections=0
    for matching in matchings(remaining):
        total+=1
        multiplicity=Counter(tuple(a//2 for a in LABELS[w]) for w in matching)
        if any(n>1 and edge in grids for edge,n in multiplicity.items()):
            intersection_rejections+=1
            continue
        rows.extend(row for row in permutations(matching)
                    if all(w in domain for w,domain in zip(row,domains)))
    assert len(rows)==len(set(rows))
    return rows,{'eight_labels':remaining,'matchings_before_intersections':total,
                 'matchings_removed_by_intersections':intersection_rejections,
                 'allowed_ordered_corner_rows':len(rows)}


def add_grid_intersection_cuts(model,template,rectangles,corner_tables=False):
    nongrids={tuple(e) for e in template['nongrid_edges']}
    if template.get('partial'):
        old_grids=[tuple(e) for e in template['known_grid_edges']]
    else:
        old_grids=[e for e in RECTANGLES if e not in nongrids]
    cuts=0;flags=0;records=[]
    for ri,item in enumerate(rectangles):
        assert 0<=item['root']<14
        root_line=item['root']//2
        active=model.new_bool_var(f'grid_intersection_active_{ri}')
        model.add(sum(item['edges'])==4).only_enforce_if(active)
        model.add(sum(item['edges'])<=2).only_enforce_if(active.Not())
        flags+=1;at_most_one=0;avoid=0
        for edge in old_grids:
            old_corners=set(RECTANGLES[edge])
            selected=sum(flag for corner in item['corners']
                         for w,flag in corner['flags'].items() if w in old_corners)
            if isinstance(selected,int) and selected==0:continue
            if root_line in edge:
                base_count=sum(w in old_corners for w in item['base_vertices'])
                assert base_count in (0,2)
                model.add(selected==0).only_enforce_if(active)
                avoid+=1
            else:
                assert not any(w in old_corners for w in item['base_vertices'])
                model.add(selected<=1).only_enforce_if(active)
                at_most_one+=1
            cuts+=1
        record={'root_letter':item['root'],'old_grid_avoidance_cuts':avoid,
                'old_grid_intersection_at_most_one_cuts':at_most_one}
        if corner_tables:
            rows,table_info=grid_corner_rows(item,old_grids)
            if rows:
                model.add_allowed_assignments([c['actual'] for c in item['corners']],rows).only_enforce_if(active)
            else:
                model.add(active==0)
            record['corner_table']=table_info
        records.append(record)
    return {'scope':__doc__,'old_grids':len(old_grids),'grid_flags':flags,
            'cuts':cuts,'records':records,'corner_tables':corner_tables,
            'unconditional_on_nongrids':False}
