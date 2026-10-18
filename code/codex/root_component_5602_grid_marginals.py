"""Exact 4 x 4 x 4 margins forced by the three Y-grids of 5602.

Every one of the sixteen X-grid vertices chooses one neighbour in each
Y-grid. Their three pairwise margins are completely fixed by C2 and the
eight-vertex core. Four tiny contingency tables must sum to the third
margin. Enumerate the layers and join two pairs using Python integers.
This forgets the assignment to the sixteen labelled corners and hence
is only a necessary condition. No floating point or solver is involved.
"""

from functools import lru_cache
from itertools import product


@lru_cache(None)
def layers(rows,columns):
    output=[]
    def visit(i,remaining,matrix):
        if i==4:
            if not any(remaining):output.append(matrix)
            return
        for row in product(*(range(min(rows[i],n)+1) for n in remaining)):
            if sum(row)==rows[i]:
                visit(i+1,tuple(a-b for a,b in zip(remaining,row)),matrix+row)
    visit(0,columns,())
    return tuple(output)


def test(boundary):
    labels=[(a,b) for i,j in ((0,1),(0,2),(1,2)) for a in (2*i,2*i+1) for b in (2*j,2*j+1)]
    def margin(a,b):
        return tuple(tuple(2-len(set(labels[4*a+i])&set(labels[4*b+j]))-
                           (boundary[4*a+i]&boundary[4*b+j]).bit_count() for j in range(4)) for i in range(4))
    d01,d02,d12=margin(0,1),margin(0,2),margin(1,2)
    assert all(min(row)>=0 and sum(row)==4 for m in (d01,d02,d12) for row in m)
    catalogs=[layers(d01[i],d02[i]) for i in range(4)]
    target=sum(d12,())
    left={}
    for i,a in enumerate(catalogs[0]):
        for j,b in enumerate(catalogs[1]):
            key=tuple(x+y for x,y in zip(a,b))
            if all(x<=y for x,y in zip(key,target)):left.setdefault(key,(i,j))
    witness=None;right_keys=set()
    for i,a in enumerate(catalogs[2]):
        for j,b in enumerate(catalogs[3]):
            key=tuple(t-x-y for t,x,y in zip(target,a,b))
            if min(key)<0:continue
            right_keys.add(key)
            if key in left and witness is None:
                indices=left[key]+(i,j)
                witness=[catalogs[q][s] for q,s in enumerate(indices)]
    if witness is not None:
        assert tuple(sum(m[j] for m in witness) for j in range(16))==target
    return {'status':'PASSES' if witness is not None else 'EXCLUDED_BOUNDARY',
            'margins':[d01,d02,d12],'layer_counts':[len(c) for c in catalogs],
            'left_sums':len(left),'right_complements':len(right_keys),
            'disjoint_sum_sets':not bool(left.keys()&right_keys),
            'integer_table_witness':witness,'scope':__doc__}
