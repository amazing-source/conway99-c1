"""Lift extra kernels of a finite Gram cover to every actual vertex row.

For a Conway completion H^T H=7R. Thus Rv=0 implies Hv=0, because
||Hv||^2=7 v^T R v=0. Component incidence already supplies some kernel
vectors; only vectors independent of that structural span are added.
The Gram stays variable: a vector is imposed only for selectors whose
Gram annihilates it. No numerical rank threshold or chosen Gram seed.
"""
from collections import defaultdict
from functools import reduce
from math import gcd,lcm

import sympy as sp

from root_component_propagation import RECTANGLES
from root_component_signature_moments import gram_matrix


def primitive(vector):
    scale=lcm(*(int(x.q) for x in vector))
    values=[int(x*scale) for x in vector]
    divisor=reduce(gcd,values)
    values=[x//divisor for x in values]
    if next(x for x in values if x)<0:values=[-x for x in values]
    return tuple(values)


def prepare(template,cover):
    edges=[tuple(e) for e in template['nongrid_edges']]
    positions={edge:i for i,edge in enumerate(edges)};m=len(edges)
    rows=[]
    for root,parts in enumerate(template['nontrivial_component_groups']):
        assert parts is not None,'A complete component template is required.'
        for part in parts:
            row=[0]*m
            for j in part:row[positions[tuple(sorted((root,j)))]]=1
            rows.append(row)
    incidence=sp.Matrix(rows) if rows else sp.zeros(0,m)
    structural=list(incidence.rowspace());structural_rank=len(structural)
    matrices=[];vectors=set();profiles=[]
    for gi,values in enumerate(cover['gram_anchor_values']):
        matrix=gram_matrix(cover,values);assert matrix.shape==(m,m)
        assert incidence*matrix==sp.zeros(incidence.rows,m)
        basis=list(structural);extra=[]
        for vector in matrix.nullspace():
            row=vector.T
            if sp.Matrix.vstack(*(basis+[row])).rank()==len(basis):continue
            basis.append(row);v=primitive(vector)
            assert matrix*sp.Matrix(v)==sp.zeros(m,1)
            vectors.add(v);extra.append(v)
        assert len(basis)==m-matrix.rank()
        matrices.append(matrix)
        profiles.append({'gram_selector':gi,'rank':matrix.rank(),
                         'nullity':m-matrix.rank(),'extra_kernel_dimension':len(extra)})
    # A vector discovered for one Gram may also be valid for others.
    # Compute its complete selector support, not only its discovery basis.
    cuts=[{'vector':list(v),'gram_selectors':[gi for gi,matrix in enumerate(matrices)
                                           if matrix*sp.Matrix(v)==sp.zeros(m,1)]}
          for v in sorted(vectors)]
    return {'scope':__doc__,'gram_count':len(matrices),'matrix_size':m,
            'structural_kernel_rank':structural_rank,'profiles':profiles,
            'extra_vectors':cuts,'all_vectors_checked_exactly':True}


def add(model,graph,template,cover,selector):
    prepared=prepare(template,cover)
    edges=[tuple(e) for e in template['nongrid_edges']]
    count=cover['gram_count'];assert count==prepared['gram_count']
    conditional=any(len(c['gram_selectors'])<count for c in prepared['extra_vectors'])
    flags=[];active_by_support={};equations=0
    if conditional:
        flags=[model.new_bool_var(f'kernel_gram_{i}') for i in range(count)]
        model.add_map_domain(selector,flags)
    for ci,cut in enumerate(prepared['extra_vectors']):
        support=tuple(cut['gram_selectors'])
        active=None
        if len(support)<count:
            if support not in active_by_support:
                active=model.new_bool_var(f'kernel_support_{len(active_by_support)}')
                model.add(active==sum(flags[i] for i in support))
                active_by_support[support]=active
            active=active_by_support[support]
        vector=cut['vector']
        for rectangle,corners in RECTANGLES.items():
            constant=sum(v*(2 if rectangle==edge else 0 if set(rectangle)&set(edge) else 1)
                         for edge,v in zip(edges,vector))
            for w in corners:
                expression=sum(v*graph[w][q] for edge,v in zip(edges,vector) if v
                               for q in RECTANGLES[edge])
                constraint=model.add(expression==constant)
                if active is not None:constraint.only_enforce_if(active)
                equations+=1
    prepared.update(vertex_kernel_equations=equations,
                    conditional_selector_groups=len(active_by_support),
                    gram_selector_fixed=False)
    return prepared
