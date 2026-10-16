"""Necessary symmetry defect in five complete root stars, lambda=1, mu=2.

The roots are paired by r -> r^1. Take stars 0,1,2,3,c (c=4 by
default), and h=(0 1)(2 3). Put X={{c,y}:y outside {0,1,2,3,c,c^1}}.
For either a=0 or a=2, index L_a by w != a,a^1 and put
    p_w={a,w}, q_w=h(p_w), A_xw=Gamma[x,p_w], B_xw=Gamma[x,q_w].
Each row has sum A=sum B=2. Thus its defect is 4-2 sum_w A_xw B_xw.

For w=c,c^1, A_xw+B_xw<=1 by the root counts. For every other w,
at most ONE x sees both p_w and q_w: otherwise two vertices of X
would share the root c and two second-neighbourhood vertices, violating
mu=2. This also caps the two disjoint pairs (w=0,1 when a=2) at one.
Consequently P=sum A*B <= k-4, and D=4(k-6)-2P >= 2k-16.
Each row contributes 0,2 or4, so at least ceil((k-8)/2) rows break h
when k>8. For k=14 these bounds are D>=12 and at least3 of8 rows.

The proof assumes neither an h-invariant old block nor any automorphism
of the complete graph. The cut is necessary, not a construction or a
nonexistence proof. Peer893 supplied the invariant-extension pigeonhole;
the quantitative defect and the shared-root improvement are new here.

If p_w,q_w already have e_w + c_w contributions from their mutual edge
and common neighbours outside X, their remaining capacity is
2-|p_w intersect q_w|-e_w-c_w. Cap it at one. The sum of these capacities
strengthens the lower bound without fixing any old graph.
"""
from itertools import combinations
from math import ceil


def defect_specs(labels, root_count=14, external_root=4):
    """Return two indexed comparisons, or [] if the five stars are absent."""
    if root_count < 6 or root_count % 2:
        raise ValueError('An even root count >=6 is required.')
    c = external_root
    if not 4 <= c < root_count:
        raise ValueError('The external root must be outside 0,1,2,3.')
    labels = [tuple(sorted(p)) for p in labels]
    index = {p:i for i,p in enumerate(labels)}
    if len(index) != len(labels):
        raise ValueError('Repeated root-pair labels.')
    all_labels = [p for p in combinations(range(root_count), 2)
                  if p[1] != (p[0] ^ 1)]
    required = {p for p in all_labels if any(r in p for r in (0,1,2,3,c))}
    if not required <= index.keys():
        return []
    x_labels = [(c,y) if c < y else (y,c) for y in range(root_count)
                if y not in (0,1,2,3,c,c^1)]
    x_indices = [index[p] for p in x_labels]
    specs = []
    for a in (0,2):
        pairs = []
        for w in range(root_count):
            if w in (a,a^1):
                continue
            hw = w^1 if w < 4 else w
            p, q = tuple(sorted((a,w))), tuple(sorted((a^1,hw)))
            pairs.append(dict(w=w,p=index[p],q=index[q],
                              capacity=2-len(set(p)&set(q)),
                              forbidden=w in (c,c^1)))
        lower = max(0,2*root_count-16)
        specs.append(dict(compared_roots=[a,a^1],external_root=c,
                          x_indices=x_indices,x_labels=x_labels,pairs=pairs,
                          lower_bound=lower,broken_rows_lower_bound=ceil(lower/4)))
    return specs


def add_defect_cuts(model, labels, graph, root_count=14, external_root=4,
                    conjunction=None):
    """Add necessary cuts; return JSON metadata and CP defect expressions.

    graph entries are Boolean CP variables or integer constants. The
    caller may supply its existing cached conjunction function. Complete
    stars are detected from labels; a 44/45-vertex model is left untouched.
    """
    specs = defect_specs(labels,root_count,external_root)
    if not specs:
        return [],[]
    if conjunction is None:
        products = {}
        def conjunction(x,y):
            if isinstance(x,int):
                return y if x else 0
            if isinstance(y,int):
                return x if y else 0
            if x.Index() == y.Index():
                return x
            key = tuple(sorted((x.Index(),y.Index())))
            if key not in products:
                z = model.NewBoolVar('defect_and_%d_%d'%key)
                model.AddMultiplicationEquality(z,[x,y])
                products[key] = z
            return products[key]
    metadata,expressions = [],[]
    for spec in specs:
        a = spec['compared_roots'][0]
        prefix = 'defect_%d_%d_'%(external_root,a)
        x_indices = spec['x_indices']
        outside = [z for z in range(len(labels)) if z not in x_indices]
        overlaps = [[] for _ in spec['pairs']]
        row_defects,broken = [],[]
        for row,x in enumerate(x_indices):
            left,right,differences = [],[],[]
            for column,pair in enumerate(spec['pairs']):
                av,bv = graph[x][pair['p']],graph[x][pair['q']]
                left.append(av)
                right.append(bv)
                q = model.NewBoolVar(prefix+'xor_%d_%d'%(row,column))
                model.AddBoolXOr([av,bv,q.Not()])
                differences.append(q)
                overlaps[column].append(conjunction(av,bv))
            # These counts hold in every completion. Making them explicit
            # also connects the XOR cuts to the full84 Gram-only model.
            model.Add(sum(left)==2)
            model.Add(sum(right)==2)
            defect = model.NewIntVar(0,4,prefix+'row_%d'%row)
            half = model.NewIntVar(0,2,prefix+'half_%d'%row)
            nonzero = model.NewBoolVar(prefix+'broken_%d'%row)
            model.Add(defect==sum(differences))
            model.Add(defect==2*half)
            model.Add(half>=1).OnlyEnforceIf(nonzero)
            model.Add(half==0).OnlyEnforceIf(nonzero.Not())
            row_defects.append(defect)
            broken.append(nonzero)
        usable = []
        for column,pair in enumerate(spec['pairs']):
            if pair['forbidden']:
                model.Add(sum(overlaps[column])==0)
                continue
            p,q,capacity = pair['p'],pair['q'],pair['capacity']
            load = graph[p][q]+sum(conjunction(graph[p][z],graph[q][z])
                                   for z in outside)
            available = model.NewBoolVar(prefix+'usable_%d'%column)
            model.Add(load<=capacity)
            model.Add(load<=capacity-1).OnlyEnforceIf(available)
            model.Add(load>=capacity).OnlyEnforceIf(available.Not())
            # The bound1, even for disjoint old pairs, uses the common
            # root of all X vertices; this is an integer packing bound.
            model.Add(sum(overlaps[column])<=available)
            usable.append(available)
        total = model.NewIntVar(0,4*len(x_indices),prefix+'total')
        model.Add(total==sum(row_defects))
        model.Add(total>=spec['lower_bound'])
        model.Add(sum(broken)>=spec['broken_rows_lower_bound'])
        strengthened = 4*len(x_indices)-2*sum(usable)
        model.Add(total>=strengthened)
        model.Add(4*sum(broken)>=strengthened)
        metadata.append(dict(compared_roots=spec['compared_roots'],
                             external_root=external_root,x_labels=spec['x_labels'],
                             lower_bound=spec['lower_bound'],
                             broken_rows_lower_bound=spec['broken_rows_lower_bound'],
                             xor_variables=len(x_indices)*len(spec['pairs']),
                             contextual_capacity_cut=True,
                             scope='Necessary lambda1/mu2 condition; no symmetry assumed.'))
        expressions.append(dict(total=total,rows=row_defects,broken=broken))
    return metadata,expressions


def measure_defects(labels, adjacency, root_count=14, external_root=4):
    """Exact diagnostics, not a substitute for full SRG validation."""
    report = []
    for spec in defect_specs(labels,root_count,external_root):
        xs = spec['x_indices']
        outside = [z for z in range(len(labels)) if z not in xs]
        rows = [sum(abs(int(adjacency[x][p['p']])-int(adjacency[x][p['q']]))
                    for p in spec['pairs']) for x in xs]
        capacities = []
        for pair in spec['pairs']:
            if pair['forbidden']:
                continue
            p,q = pair['p'],pair['q']
            load = int(adjacency[p][q])+sum(int(adjacency[p][z])*int(adjacency[q][z])
                                          for z in outside)
            capacities.append(min(1,pair['capacity']-load))
        contextual = 4*len(xs)-2*sum(capacities)
        report.append(dict(compared_roots=spec['compared_roots'],
                           external_root=external_root,total=sum(rows),rows=rows,
                           broken_rows=sum(bool(d) for d in rows),
                           lower_bound=spec['lower_bound'],
                           contextual_lower_bound=contextual,
                           remaining_pair_capacities=capacities,
                           cut_satisfied=min(capacities,default=0)>=0 and sum(rows)>=contextual))
    return report
