"""Constructive relabelling of (0,2), without assuming graph automorphisms.

First orient e,f by residual degrees, then rotate the labelled H cycle if
the common neighbour is in C8 or ZH, and finally restore every signature
ordering. Anchor vertices do not lie in the sorted groups, so this is valid.
"""
import numpy as np


def sorted_groups():
    return [[2*i,2*i+1] for i in range(4)]+[list(range(8,21))]+[
        list(range(39+6*i,45+6*i)) for i in range(4)]+[list(range(63,99))]


def canonicalize(A):
    A = np.asarray(A,dtype=np.int64)
    assert A.shape == (99,99) and np.array_equal(A,A.T)
    M = [37,38]+list(range(63,99))
    order = list(range(99))
    if A[37,M].sum() > A[38,M].sum():
        order[37],order[38] = order[38],order[37]
    common = np.flatnonzero(A[37]*A[38]).tolist()
    assert len(common) == 1
    t = common[0]
    j = t//2 if t < 8 else (t-39)//6 if 39 <= t < 63 else 0
    if j:
        for i in range(4):
            h = (i+j)%4
            order[21+i] = 21+h
            order[25+i] = 25+h
            for k in range(2):
                order[2*i+k] = 2*h+k
                order[29+2*i+k] = 29+2*h+k
            for k in range(6):
                order[39+6*i+k] = 39+6*h+k
    A1 = A[np.ix_(order,order)]
    secondary = list(range(99))
    for group in sorted_groups():
        def score(u):
            anchors = range(21,37) if group[0] >= 63 else range(21,39)
            value = sum((1 << (s-21))*int(A1[u,s]) for s in anchors)
            return 4*value+int(A1[u,37])+2*int(A1[u,38]) if group[0] >= 63 else value
        for u,v in zip(group,sorted(group,key=score)):
            secondary[u] = v
    permutation = [order[v] for v in secondary]
    return A[np.ix_(permutation,permutation)],permutation


def add_canonicalization(model, edge):
    indices = {v.name:i for i,v in enumerate(model.proto.variables)
               if v.name.startswith(('v10_degree','v10_common_'))}
    degree = lambda u:model.get_int_var_from_proto_index(indices[f'v10_degree{u}'])
    model.add(degree(37) <= degree(38))
    for location,t in (('C8',1),('C13',20),('ZH',44)):
        flag = model.get_bool_var_from_proto_index(indices[f'v10_common_{location}'])
        model.add(edge(37,t) == 1).only_enforce_if(flag)
        model.add(edge(38,t) == 1).only_enforce_if(flag)
    # Secondary keys only: preserve the previous primary ordering on H+L.
    def score(u):
        return 4*sum((1 << (s-21))*edge(u,s) for s in range(21,37))+edge(u,37)+2*edge(u,38)
    for u,v in zip(range(63,98),range(64,99)):
        model.add(score(u) <= score(v))
    return dict(canonical_constraints=42, negative_degree_orientation=True,
                fixed_common_neighbour_representatives=dict(C8=1,C13=20,ZH=44),
                canonical_scope='Preserves at least one labelling of every (0,2) graph')
