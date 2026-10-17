"""Exact Schur cuts for all 24 star vertices after fixing a line component.

Given the component code, all edges inside the root line's two Gamma stars
are known when the other components are prisms. The matrix 8T on those
24 vertices is fixed. Every outside neighbour profile must lie in its
column space and satisfy b^t (8T)^+ b <= 20. This tests one necessary
principal submatrix of the global PSD matrix T, not a full graph.
"""

from itertools import combinations
from math import lcm
import sympy as sp

from root_component_line_profiles import root_profiles
from root_component_propagation import LABELS


def fixed_line_graph(graph, template, tables, root, part, code):
    lookup={p:i for i,p in enumerate(LABELS)}
    record=next(r for r in tables['records'] if r['vertices']==6*len(part))
    letters=[a for j in part for a in (2*j,2*j+1)]
    stars=[[lookup[tuple(sorted((2*root+c,a)))] for a in letters] for c in range(2)]
    p,m0,m1=code
    permutation=record['cross_permutations'][p]
    fixed=[list(row) for row in graph]
    for c,m in enumerate((m0,m1)):
        edges={tuple(e) for e in record['internal_matchings'][m]}
        for i,j in combinations(range(len(letters)),2):
            fixed[stars[c][i]][stars[c][j]]=fixed[stars[c][j]][stars[c][i]]=int((i,j) in edges)
    for i,u in enumerate(stars[0]):
        for j,v in enumerate(stars[1]):fixed[u][v]=fixed[v][u]=int(permutation[i]==j)
    return fixed


def profile_cuts(graph, template, tables, root, part, code):
    fixed=fixed_line_graph(graph,template,tables,root,part,code)
    profiles=root_profiles(fixed,template,root)
    vertices=profiles['vertices'];position={v:i for i,v in enumerate(vertices)}
    assert all(isinstance(fixed[u][v],int) for u in vertices for v in vertices), 'Other nontrivial components must also be fixed.'
    def base(u,v):
        common=len(set(LABELS[u]) & set(LABELS[v]))
        mates=sum((a^1) in LABELS[v] for a in LABELS[u])
        return 2-3*common-mates
    matrix=sp.Matrix([[20 if u==v else base(u,v)-8*fixed[u][v] for v in vertices] for u in vertices])
    null=matrix.nullspace()
    z=sp.Matrix.hstack(*null)
    projection=z*(z.T*z).inv()*z.T
    inverse=(matrix+projection).inv()-projection
    assert matrix*inverse*matrix==matrix
    denominator=lcm(*(x.q for x in inverse))
    inv=[[int(x*denominator) for x in row] for row in inverse.tolist()]
    nullrows=[[int(x*lcm(*(a.q for a in column))) for x in column] for column in null]
    rejected=[];counts=[]
    for w,rows in profiles['rows'].items():
        b=[base(w,v) for v in vertices]
        db=[sum(x*y for x,y in zip(row,b)) for row in inv]
        constant=sum(x*y for x,y in zip(b,db))
        bad=0; maximum=None
        for profile in rows:
            indices=[position[v] for v in profile]
            energy=constant-16*sum(db[i] for i in indices)+64*sum(inv[i][j] for i in indices for j in indices)
            kernel_bad=any(sum(x*y for x,y in zip(row,b))!=8*sum(row[i] for i in indices) for row in nullrows)
            if kernel_bad or energy>20*denominator:
                rejected.append((w,profile));bad+=1
            maximum=energy if maximum is None else max(maximum,energy)
        counts.append({'vertex':w,'before':len(rows),'after':len(rows)-bad,
                       'maximum_energy':str(sp.Rational(maximum,denominator)) if maximum is not None else None})
    return rejected,{'root':root,'part':list(part),'code':list(code),'matrix_rank':matrix.rank(),
                     'profiles_before':sum(r['before'] for r in counts),
                     'profiles_after':sum(r['after'] for r in counts),'per_vertex':counts}


def add_profile_cuts(model, graph, template, tables, root, part, code):
    rejected,info=profile_cuts(graph,template,tables,root,part,code)
    for w,profile in rejected:
        terms=[graph[w][v] for v in profile]
        assert not any(isinstance(e,int) and not e for e in terms)
        model.add_bool_or([e.Not() for e in terms if not isinstance(e,int)])
    return info
