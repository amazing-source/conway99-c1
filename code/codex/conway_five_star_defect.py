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

For k=14 there is also a joint bound: at most FOUR of the8 attachment
rows can be h-invariant on the whole old44. If five were invariant,
their disjoint neighbourhoods would partition the36 old labels avoiding
4,5 (and cover all four cross labels between {0,1} and {2,3}). Each of
the three other rows meets each of these five neighbourhoods at most
once. Their total old degree is at least20: it equals24 minus at most
four incidences with cross labels. It is at most15+3+2=20: fifteen
incidences in those five parts, three toward star5, and at most two
toward star4 (an even number, at most3). Equality leaves one of the
three rows needing a partner in X, but it meets all five invariant
neighbourhoods and cannot be adjacent to any of them. The other two
rows already have partners in the old part of star4. Contradiction.
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
    if root_count == 14:
        joint = []
        for row,(left,right) in enumerate(zip(expressions[0]['broken'],expressions[1]['broken'])):
            flag = model.NewBoolVar('defect_%d_joint_%d'%(external_root,row))
            model.AddMaxEquality(flag,[left,right])
            joint.append(flag)
        model.Add(sum(joint)>=4)
        expressions[0]['joint_broken'] = joint
        for item in metadata:
            item['joint_broken_rows_lower_bound'] = 4
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
    if root_count == 14 and report:
        joint = sum(bool(a or b) for a,b in zip(report[0]['rows'],report[1]['rows']))
        for item in report:
            item['joint_broken_rows'] = joint
            item['joint_broken_rows_lower_bound'] = 4
            item['cut_satisfied'] &= joint >= 4
    return report


def add_attachment_demand_cuts(model,labels,graph,root_count=14,external_root=4,
                               conjunction=None):
    """A universal Hall bound on completing neighbours in the new star.

    P consists of the four old labels {0,c},...,{3,c}; X is the new part
    of L_c, and Y the old labels avoiding c,c^1. A z in Y with exactly
    one neighbour x in X needs one more neighbour in P, because z has
    exactly two neighbours in the complete star L_c. For each p in P,
    C2 applied to x,p (already sharing root c) allows at most1-A[x,p]
    such common neighbours. Consequently
        private_Y_neighbours(x) + neighbours_in_P(x) <= 4.
    This holds without fixing any old-old edge or imposing h. It is the
    general form of the new five-demands/four-places obstruction.
    """
    specs=defect_specs(labels,root_count,external_root)
    if not specs:
        return []
    xs=specs[0]['x_indices']
    old=[i for i,p in enumerate(labels) if any(r in p for r in (0,1,2,3))]
    ps=[i for i in old if external_root in labels[i]]
    ys=[i for i in old if external_root not in labels[i] and (external_root^1) not in labels[i]]
    assert len(ps)==4
    if conjunction is None:
        products={}
        def conjunction(a,b):
            if isinstance(a,int):
                return b if a else 0
            if isinstance(b,int):
                return a if b else 0
            key=tuple(sorted((a.Index(),b.Index())))
            if key not in products:
                z=model.NewBoolVar('demand_and_%d_%d'%key)
                model.AddMultiplicationEquality(z,[a,b])
                products[key]=z
            return products[key]
    private={}
    for y in ys:
        degree=sum(graph[x][y] for x in xs)
        flag=model.NewBoolVar('private_%d_%d'%(external_root,y))
        model.Add(degree<=2)
        model.Add(degree==1).OnlyEnforceIf(flag)
        model.Add(degree!=1).OnlyEnforceIf(flag.Not())
        private[y]=flag
    for x in xs:
        demand=sum(conjunction(graph[x][y],private[y]) for y in ys)
        model.Add(demand+sum(graph[x][p] for p in ps)<=4)
    return [dict(external_root=external_root,new_rows=len(xs),old_candidates=len(ys),
                 old_star_vertices=[labels[p] for p in ps],capacity=4,
                 rule='private_Y_neighbours(x) + old_star_neighbours(x) <= 4',
                 scope='Universal complete-star demand bound; no old graph or symmetry assumed.')]


def measure_attachment_demand(labels,adjacency,root_count=14,external_root=4):
    specs=defect_specs(labels,root_count,external_root)
    if not specs:
        return []
    xs=specs[0]['x_indices']
    old=[i for i,p in enumerate(labels) if any(r in p for r in (0,1,2,3))]
    ps=[i for i in old if external_root in labels[i]]
    ys=[i for i in old if external_root not in labels[i] and (external_root^1) not in labels[i]]
    degrees={y:sum(int(adjacency[x][y]) for x in xs) for y in ys}
    rows=[]
    for x in xs:
        private=[labels[y] for y in ys if degrees[y]==1 and adjacency[x][y]]
        used=sum(int(adjacency[x][p]) for p in ps)
        rows.append(dict(vertex=labels[x],private_neighbours=private,demand=len(private),
                         capacity=4-used,old_star_neighbours=used,
                         satisfied=len(private)<=4-used))
    return rows


def add_outside_support_cuts(model,labels,graph,root_count=14,external_root=4,
                              conjunction=None):
    """Every uncovered pair in X must admit an outside common neighbour.

    Two nonmatched X vertices with no old common neighbour require one
    new common neighbour. It cannot lie in L_(c^1), since every vertex
    of that star has exactly one neighbour in L_c. It is therefore an
    outside label {a,b}, with a,b in the k-6 exterior roots and not mates.
    Both endpoints must have positive remaining root capacities at a,b.
    A root set contains such a pair iff it is not contained in any one
    mate pair. This gives cheap Boolean support constraints before any
    assignment of the outside labels.
    """
    specs=defect_specs(labels,root_count,external_root)
    if not specs:
        return []
    xs=specs[0]['x_indices']
    old=[i for i,p in enumerate(labels) if any(r in p for r in (0,1,2,3))]
    present=old+xs
    exterior=[r for r in range(root_count) if r not in (0,1,2,3,external_root,external_root^1)]
    if conjunction is None:
        products={}
        def conjunction(a,b):
            if isinstance(a,int):
                return b if a else 0
            if isinstance(b,int):
                return a if b else 0
            key=tuple(sorted((a.Index(),b.Index())))
            if key not in products:
                z=model.NewBoolVar('outside_and_%d_%d'%key)
                model.AddMultiplicationEquality(z,[a,b])
                products[key]=z
            return products[key]
    available={}
    for x in xs:
        for r in exterior:
            target=2-int(r in labels[x])-int((r^1) in labels[x])
            used=sum(graph[x][z] for z in present if r in labels[z])
            flag=model.NewBoolVar('outside_available_%d_%d'%(x,r))
            model.Add(used<=target)
            model.Add(used<=target-1).OnlyEnforceIf(flag)
            model.Add(used==target).OnlyEnforceIf(flag.Not())
            available[x,r]=flag
    for x,y in combinations(xs,2):
        old_common=sum(conjunction(graph[x][z],graph[y][z]) for z in old)
        need=model.NewBoolVar('outside_required_%d_%d'%(x,y))
        model.Add(need+graph[x][y]+old_common==1)
        compatible={r:conjunction(available[x,r],available[y,r]) for r in exterior}
        if not exterior:
            model.Add(need==0)
        for r in exterior:
            if r>(r^1):
                continue
            model.Add(sum(flag for t,flag in compatible.items() if t not in (r,r^1))>=need)
    return [dict(external_root=external_root,pairs=len(xs)*(len(xs)-1)//2,exterior_roots=exterior,
                 rule='Every uncovered X pair admits a nonmate outside label within both residual root budgets.',
                 scope='Necessary for global84 completion; no fixed old graph or symmetry assumed.')]


def measure_outside_support(labels,adjacency,root_count=14,external_root=4):
    specs=defect_specs(labels,root_count,external_root)
    if not specs:
        return []
    xs=specs[0]['x_indices']
    old=[i for i,p in enumerate(labels) if any(r in p for r in (0,1,2,3))]
    present=old+xs
    exterior=[r for r in range(root_count) if r not in (0,1,2,3,external_root,external_root^1)]
    budgets={x:{r:2-int(r in labels[x])-int((r^1) in labels[x])
               -sum(int(adjacency[x][z]) for z in present if r in labels[z]) for r in exterior} for x in xs}
    report=[]
    for x,y in combinations(xs,2):
        need=1-int(adjacency[x][y])-sum(int(adjacency[x][z])*int(adjacency[y][z]) for z in old)
        if need!=1:
            continue
        allowed=[r for r in exterior if budgets[x][r]>0 and budgets[y][r]>0]
        possible=[(a,b) for a,b in combinations(allowed,2) if b!=(a^1)]
        report.append(dict(pair=[labels[x],labels[y]],left_budgets=budgets[x],right_budgets=budgets[y],
                           allowed_roots=allowed,possible_common_labels=possible,satisfied=bool(possible)))
    return report
