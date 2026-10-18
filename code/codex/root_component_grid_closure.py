"""Universal Conway grid closure C4 disjoint C3 => K4 disjoint C3.

Uses E3 and the finite 8 -> 20 -> 36 -> missing-vertex exclusion recorded
in COEUR_HUIT_SOMMETS_5602_2026_10_19.txt. Only the seven required grids
and a nongrid diagonal are hypotheses. There is no condition on the
twelve cross rectangles, the component partitions, the Gram, or symmetry.
The template's nongrid_edges is assumed to specify all 21 grid statuses.
"""

from itertools import combinations


def grid_closure_violations(template):
    nongrid={tuple(sorted(q)) for q in template['nongrid_edges']}
    all_edges=set(combinations(range(7),2))
    assert nongrid<=all_edges
    records=[]
    for x in combinations(range(7),4):
        y=tuple(i for i in range(7) if i not in x)
        if any(q in nongrid for q in combinations(y,2)):continue
        for b in x[1:]:
            a=x[0];other=tuple(i for i in x if i not in (a,b))
            diagonals=((a,b),other)
            cycle=set(combinations(x,2))-set(diagonals)
            if cycle&nongrid or not any(q in nongrid for q in diagonals):continue
            records.append({'four_roots':x,'three_roots':y,
                            'required_grids':sorted(cycle|set(combinations(y,2))),
                            'forced_grid_diagonals':diagonals,
                            'contradicting_nongrids':[q for q in diagonals if q in nongrid],
                            'uses_E3':True,'fixed_Gram_required':False,
                            'rule':'C4 disjoint C3 forces K4 disjoint C3'})
    return records
