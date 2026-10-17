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


def profile_cuts(graph, template, tables, root, part, code, complementary=False):
    fixed=fixed_line_graph(graph,template,tables,root,part,code)
    profiles=root_profiles(fixed,template,root)
    vertices=profiles['vertices'];position={v:i for i,v in enumerate(vertices)}
    assert all(isinstance(fixed[u][v],int) for u in vertices for v in vertices), 'Other nontrivial components must also be fixed.'
    matrices=[]
    for name,diagonal,factor in [('T',20,-8)]+([('U',50,15)] if complementary else []):
        def base(u,v,name=name):
            common=len(set(LABELS[u]) & set(LABELS[v]))
            mates=sum((a^1) in LABELS[v] for a in LABELS[u])
            return 2-3*common-mates if name=='T' else -2-4*common+mates
        matrix=sp.Matrix([[diagonal if u==v else base(u,v)+factor*fixed[u][v] for v in vertices] for u in vertices])
        null=matrix.nullspace()
        z=sp.Matrix.hstack(*null) if null else sp.zeros(len(vertices),0)
        projection=z*(z.T*z).inv()*z.T if null else sp.zeros(len(vertices))
        inverse=(matrix+projection).inv()-projection
        assert matrix*inverse*matrix==matrix
        denominator=lcm(*(x.q for x in inverse))
        inv=[[int(x*denominator) for x in row] for row in inverse.tolist()]
        nullrows=[[int(x*lcm(*(a.q for a in column))) for x in column] for column in null]
        matrices.append((name,diagonal,factor,base,denominator,inv,nullrows,len(vertices)-len(null)))
    rejected=[];counts=[];rejections_by_projector={item[0]:0 for item in matrices}
    for w,rows in profiles['rows'].items():
        prepared=[]
        for name,diagonal,factor,base,denominator,inv,nullrows,rank in matrices:
            b=[base(w,v) for v in vertices]
            db=[sum(x*y for x,y in zip(row,b)) for row in inv]
            constant=sum(x*y for x,y in zip(b,db))
            prepared.append((name,diagonal,factor,denominator,inv,nullrows,b,db,constant))
        bad=0;maximum={name:None for name,*_ in matrices}
        for profile in rows:
            indices=[position[v] for v in profile]
            invalid=False
            for name,diagonal,factor,denominator,inv,nullrows,b,db,constant in prepared:
                energy=constant+2*factor*sum(db[i] for i in indices)+factor*factor*sum(inv[i][j] for i in indices for j in indices)
                kernel_bad=any(sum(x*y for x,y in zip(row,b))+factor*sum(row[i] for i in indices)!=0 for row in nullrows)
                if kernel_bad or energy>diagonal*denominator:
                    invalid=True;rejections_by_projector[name]+=1
                value=sp.Rational(energy,denominator)
                maximum[name]=value if maximum[name] is None else max(maximum[name],value)
            if invalid:rejected.append((w,profile));bad+=1
        counts.append({'vertex':w,'before':len(rows),'after':len(rows)-bad,
                       'maximum_energy':{name:str(value) if value is not None else None for name,value in maximum.items()}})
    return rejected,{'root':root,'part':list(part),'code':list(code),'matrix_ranks':{item[0]:item[-1] for item in matrices},
                     'profiles_before':sum(r['before'] for r in counts),
                     'profiles_after':sum(r['after'] for r in counts),
                     'rejections_by_projector':rejections_by_projector,'per_vertex':counts}


def add_profile_cuts(model, graph, template, tables, root, part, code, complementary=False):
    rejected,info=profile_cuts(graph,template,tables,root,part,code,complementary=complementary)
    for w,profile in rejected:
        terms=[graph[w][v] for v in profile]
        assert not any(isinstance(e,int) and not e for e in terms)
        model.add_bool_or([e.Not() for e in terms if not isinstance(e,int)])
    return info
