"""Necessary defects for the ACTUAL cross-star matchings, not a symmetry.

Notation: L_r is the12 labels containing r. X={(4,y):6<=y<14}.
For the root line {a,a^1}, phi:L_a->L_(a^1) is the unique matching
of cross edges. For x in X, let P_a(x) count matching edges with both
endpoints adjacent to x. Its two neighbour sets on the two stars have
size2, hence their symmetric difference under phi has size4-2P_a(x).

FIRST THEOREM. Let t_a be the number of transverse matching edges
{a,w}--{a^1,w}, and delta_a indicate the one with w=4. Then

    sum_x P_a(x) + t_a - 2 delta_a <= 10,
    D_a := sum_x (4-2P_a(x)) >= 12+2t_a-4delta_a >= 10.

Proof. Every counted occurrence is the third vertex of an actual edge,
so lambda1 permits at most one occurrence per matching edge. Transverse
edges already have their common root w as third vertex. If delta_a=0,
the two distinct nontransverse edges incident with {a,4} and {a^1,4}
cannot be counted either: x and that endpoint already share root4, so
an additional triangle would violate lambda1. This leaves at most
12-t_a-2(1-delta_a) available edges. If delta_a=1, t_a>=1; otherwise
D_a>=12. A broken row contributes at most4, so at least3 rows break
each phi. Globally, at most floor((12-t_a)/2) of the60 outside vertices
can have both neighbour sets exactly paired by phi.

JOINT THEOREM. Let b count X rows breaking at least one of phi_0,phi_2.
Let d_1=Gamma[02,13], d_2=Gamma[03,12]. Then

    b + (d_1 AND d_2) >= 4.

Proof. Suppose at least five rows F are invariant under both matchings;
choose five of them, and let R be the other three vertices of X. On
the old44 labels, form H from the union of the two matchings. Every
noncross label has degree1 in H. A cross label in C={02,03,12,13} has
degree2 unless its two matching partners coincide. Coincidence is
possible only at one of the two diagonal edges02--13,03--12.

For an invariant x, N_old(x) is closed under H. It can only contain
isolated K2 components: a two-edge path in N(x) contradicts lambda1.
These old neighbourhoods are pairwise disjoint, since a shared H edge
would have two third vertices in F. No label in P={04,14,24,34} can
belong to one: x and that label already have root4 as third vertex.

Let c be the number of diagonal K2 components selected by F, so c<=2.
The five rows have40 incidences with the four central stars. Cross
labels are counted twice, hence they select40-2c distinct old labels,
of which40-4c are noncross. Only36 noncross labels avoid P, so c>=1.
If c=2, both diagonal edges exist, as claimed.

If c=1 and the other diagonal is absent, all36 permitted noncross
labels are selected by F. The two unselected cross labels u,v must
therefore have their H neighbours in P: an edge u--v would be the
missing diagonal and would belong to both matchings. Each of u,v has
two distinct neighbours in P, exhausting its two neighbours in L4.
Neither can be adjacent to R. The two selected cross labels already
have one neighbour in F, so have at most one in R each. Consequently
R has at most2 cross incidences, and at least24-2=22 old neighbours
counted with multiplicity. Each R row meets each F old neighbourhood
at most once (otherwise two common old neighbours plus root4 violate
mu2). This allows at most15 incidences into their union, and at most3
more into P, since each R row has one neighbour in L4. There are no
other available old labels. Thus22<=18, a contradiction. Both diagonal
edges must exist whenever five rows are simultaneously invariant.

These are necessary conditions, not a proof excluding all Conway
graphs. In particular the joint lower bound is3 when both diagonals
are present. The previous lower bound4 for h is a different theorem.
"""


def add_phi_cuts(model,labels,graph,conjunction=None):
    """Apply to a complete variable matrix on the52-label five-star set.

    Missing labels mean these cuts are inapplicable. Unknown edges must
    be variables, never zero placeholders. The surrounding constructor
    supplies the central root counts and common-neighbour constraints.
    """
    labels=[tuple(p) for p in labels]
    index={p:i for i,p in enumerate(labels)}
    pair=lambda a,b:tuple(sorted((a,b)))
    required={pair(a,w) for a in range(5) for w in range(14) if w not in (a,a^1)}
    if not required.issubset(index):
        return []
    products={}
    if conjunction is None:
        def conjunction(a,b):
            if isinstance(a,int):
                return b if a else 0
            if isinstance(b,int):
                return a if b else 0
            if a.Index()==b.Index():
                return a
            key=tuple(sorted((a.Index(),b.Index())))
            if key not in products:
                value=model.NewBoolVar('phi_and_%d_%d'%key)
                model.AddMultiplicationEquality(value,[a,b])
                products[key]=value
            return products[key]
    edge=lambda p,q:graph[index[p]][index[q]]
    new=[pair(4,y) for y in range(6,14)]
    overlaps=[]
    metadata=[]
    for a in (0,2):
        w_values=[w for w in range(14) if w not in (a,a^1)]
        left=[pair(a,w) for w in w_values]
        right=[pair(a^1,w) for w in w_values]
        row_overlap=[]
        for x in new:
            total=sum(conjunction(edge(x,p),conjunction(edge(x,q),edge(p,q)))
                      for p in left for q in right)
            model.Add(total<=2)
            row_overlap.append(total)
        transverse=sum(edge(p,q) for p,q in zip(left,right))
        delta=edge(pair(a,4),pair(a^1,4))
        model.Add(sum(row_overlap)+transverse-2*delta<=10)
        overlaps.append(row_overlap)
        metadata.append(dict(kind='actual_cross_matching',line=[a,a^1],
                             formula='sum_overlap + transverse - 2*delta4 <= 10',
                             minimum_broken_rows=3))
    broken=[]
    for i,x in enumerate(new):
        flag=model.NewBoolVar('phi_joint_broken_%d'%i)
        total=overlaps[0][i]+overlaps[1][i]
        model.Add(total==4).OnlyEnforceIf(flag.Not())
        model.Add(total<=3).OnlyEnforceIf(flag)
        broken.append(flag)
    diagonals=conjunction(edge((0,2),(1,3)),edge((0,3),(1,2)))
    model.Add(sum(broken)+diagonals>=4)
    metadata.append(dict(kind='joint_actual_matchings',
                         formula='broken_union + AND(edge02_13,edge03_12) >= 4'))
    return metadata
