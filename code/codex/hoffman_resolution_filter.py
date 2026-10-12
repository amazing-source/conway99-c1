"""Exact necessary ten-row resolution on a (possibly projected) domain.

UNSAT is returned only after exhaustion. Node limits return UNKNOWN.
Different selected rows have intersection at most two; column quotas are
2-|B_root intersect B_j|, with zero on the root itself.
"""


def resolution(rows,quotas,max_nodes=10000,patterns=None,pattern_bounds=None,
               support=None,support_start=None):
    n=len(rows);width=len(quotas)
    incidence=[[j for j in range(width) if row>>j&1] for row in rows]
    assert all(len(cols)==10 for cols in incidence)
    assert sum(quotas)==100
    by_col=[sum(1<<a for a,row in enumerate(rows) if row>>j&1) for j in range(width)]
    compatibility=[sum(1<<b for b,other in enumerate(rows)
                       if (row&other).bit_count()<=(pattern_bounds[patterns[a],patterns[b]]
                           if pattern_bounds is not None else
                           2 if patterns is None or patterns[a]==patterns[b] else 1))
                   for a,row in enumerate(rows)]
    quota=list(quotas);nodes=0;limited=False;witness=None

    support_prunes=0

    def dfs(av,chosen,live_support):
        nonlocal nodes,limited,witness,support_prunes
        nodes+=1
        if nodes>max_nodes:limited=True;return False
        if support is not None and not support.possible(live_support):
            support_prunes+=1;return False
        left=10-len(chosen)
        if left==0:
            assert not any(quota)
            witness=chosen;return True
        if av.bit_count()<left:return False
        best=None;score=None
        for j,r in enumerate(quota):
            if r:
                count=(av&by_col[j]).bit_count()
                if count<r:return False
                s=count if r==1 else count*(count-1)//2
                if score is None or s<score:best=j;score=s
        assert best is not None
        options=av&by_col[best]
        while options and not limited:
            bit=options&-options;options-=bit;av &=~bit
            a=bit.bit_length()-1;next_av=av&compatibility[a]
            for j in incidence[a]:
                quota[j]-=1
                if quota[j]==0:next_av &=~by_col[j]
            next_support=(live_support&support.masks[rows[a]] if support is not None else None)
            found=dfs(next_av,chosen+[a],next_support)
            for j in incidence[a]:quota[j]+=1
            if found:return True
        return False

    available=(1<<n)-1
    for j,q in enumerate(quota):
        if q==0:available &=~by_col[j]
    sat=dfs(available,[],support_start)
    return dict(status='SAT_RESOLUTION_ONLY' if sat else 'UNKNOWN' if limited else 'UNSAT_RESOLUTION',
                nodes=nodes,witness=witness,support_prunes=support_prunes)
