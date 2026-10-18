"""Gram-free energy cuts inferred from exact component identities.

If H_A+H_B+H_X+H_Y-H_C-H_D=0 and X,Y are disjoint from C, then
R_CC=8 forces h_C=2 on Q_C and h_D <= h_A+h_B there. Consequently
R_AC+R_BC<0 gives a coordinate <=-16 of H v for
v=11(e_A+e_B)+e_C+7e_D. The root Schur bound gives
256 <= (5/2) v^t R v. Since R is integral with even diagonal,
v^t R v is even and therefore >=104. All three expressions are linear
in the unfixed Gram, itself affine in the rectangle edge counts.
"""

from itertools import combinations


def patterns(template):
    import sympy as sp
    rectangles=list(combinations(range(7),2));lookup={q:i for i,q in enumerate(rectangles)}
    rows=[]
    for root,parts in enumerate(template['nontrivial_component_groups']):
        used={j for part in parts for j in part}
        for part in [tuple(p) for p in parts]+[(j,) for j in range(7) if j!=root and j not in used]:
            support={tuple(sorted((root,j))) for j in part}
            rows.append([int(q in support) for q in rectangles])
    C=sp.Matrix(rows);kernel=C.nullspace()
    nongrid={tuple(q) for q in template['nongrid_edges']}
    records=[]
    for center in range(7):
        for ends in combinations([i for i in range(7) if i!=center],2):
            other=[i for i in range(7) if i!=center and i not in ends]
            first=other[0]
            for second in other[1:]:
                left=(first,second);right=tuple(i for i in other if i not in left)
                cross=[lookup[tuple(sorted((i,j)))] for i in left for j in right]
                stars=[lookup[tuple(sorted((center,j)))] for j in ends]
                relation=[int(i in cross)-int(i in stars) for i in range(21)]
                if any(sum(a*b for a,b in zip(relation,k)) for k in kernel):continue
                matching0=(cross[0],cross[3]);matching1=(cross[1],cross[2])
                for c,d in (stars,stars[::-1]):
                    if rectangles[c] not in nongrid:continue
                    for chosen,remaining in ((matching0,matching1),(matching1,matching0)):
                        a,b=sorted(chosen);x,y=sorted(remaining)
                        assert set(rectangles[c]).isdisjoint(rectangles[x])
                        assert set(rectangles[c]).isdisjoint(rectangles[y])
                        records.append({'A':a,'B':b,'C':c,'D':d,'X':x,'Y':y,
                                        'relation':relation,'direction':[[a,11],[b,11],[c,1],[d,7]],
                                        'minimum_norm_when_triggered':104})
    assert len({(r['A'],r['B'],r['C'],r['D']) for r in records})==len(records)
    return rectangles,records


def violations(R, records):
    result=[]
    for r in records:
        a,b,c,d=(r[k] for k in ('A','B','C','D'))
        if R[c][c]!=8 or R[a][c]+R[b][c]>=0:continue
        norm=sum(x*y*R[i][j] for i,x in r['direction'] for j,y in r['direction'])
        if norm<104:result.append({**r,'observed_norm':norm,'cross_sum':R[a][c]+R[b][c]})
    return result


def add_energy_implications(model, counts, rectangles, template, *, e3=False):
    standard,records=patterns(template)
    assert [tuple(q) for q in rectangles]==standard
    def R(i,j):
        i,j=sorted((i,j))
        return 4*(3*int(i==j)+1-len(set(standard[i])&set(standard[j])))-counts[i][j]
    empty={};negative={}
    for n,r in enumerate(records):
        a,b,c,d=(r[k] for k in ('A','B','C','D'))
        if c not in empty:
            flag=model.new_bool_var(f'energy_empty_{c}')
            model.add(R(c,c)==8).only_enforce_if(flag)
            model.add(R(c,c)!=8).only_enforce_if(flag.Not());empty[c]=flag
        key=(a,b,c)
        if key not in negative:
            flag=model.new_bool_var(f'energy_negative_{a}_{b}_{c}')
            model.add(R(a,c)+R(b,c)<=-1).only_enforce_if(flag)
            model.add(R(a,c)+R(b,c)>=0).only_enforce_if(flag.Not());negative[key]=flag
        norm=sum(x*y*R(i,j) for i,x in r['direction'] for j,y in r['direction'])
        model.add(norm>=104).only_enforce_if([empty[c],negative[key]])
    result = {'component_identities':len({tuple(r['relation']) for r in records}),
            'energy_implications':len(records),'flags':len(empty)+len(negative),
            'fixed_Gram_required':False,'principle':__doc__}
    if e3:
        from root_component_opposite_core import add_opposite_count_cuts
        result['opposite_column_cuts'] = add_opposite_count_cuts(model,counts,rectangles,template)
        from root_component_grid_closure import grid_closure_violations
        result['grid_closure_violations'] = grid_closure_violations(template)
        if result['grid_closure_violations']:
            model.add(False)
    return result
