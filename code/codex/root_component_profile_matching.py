"""Hall obstructions and supported edges for a necessary perfect matching."""


def matching_support(domains):
    domains=[tuple(sorted(set(row))) for row in domains];n=len(domains)
    assert all(0<=r<n for row in domains for r in row)
    owner=[-1]*n
    def augment(left,seen):
        for right in domains[left]:
            if right in seen:continue
            seen.add(right)
            if owner[right]<0 or augment(owner[right],seen):
                owner[right]=left;return True
        return False
    for left in range(n):augment(left,set())
    matched=[-1]*n
    for right,left in enumerate(owner):
        if left>=0:matched[left]=right
    if -1 in matched:
        lefts={left for left in range(n) if matched[left]<0};rights=set();pending=list(lefts)
        while pending:
            left=pending.pop()
            for right in domains[left]:
                rights.add(right)
                mate=owner[right]
                assert mate>=0
                if mate not in lefts:lefts.add(mate);pending.append(mate)
        assert rights==set().union(*(set(domains[l]) for l in lefts))
        assert len(rights)<len(lefts)
        return {'status':'EXCLUDED_PERFECT_MATCHING_HALL','left_set':sorted(lefts),
                'neighbours':sorted(rights),'deficit':len(lefts)-len(rights)},None
    # Reverse matched edges. An unmatched edge belongs to a perfect
    # matching exactly when it lies on a directed alternating cycle.
    graph=[[] for _ in range(2*n)]
    for left,row in enumerate(domains):
        for right in row:
            u,v=(n+right,left) if matched[left]==right else (left,n+right)
            graph[u].append(v)
    indices={};low={};stack=[];onstack=set();component={}
    def visit(v):
        indices[v]=len(indices);low[v]=indices[v];stack.append(v);onstack.add(v)
        for w in graph[v]:
            if w not in indices:visit(w);low[v]=min(low[v],low[w])
            elif w in onstack:low[v]=min(low[v],indices[w])
        if low[v]==indices[v]:
            while True:
                w=stack.pop();onstack.remove(w);component[w]=v
                if w==v:break
    for v in range(2*n):
        if v not in indices:visit(v)
    supported=[tuple(r for r in row if matched[l]==r or component[l]==component[n+r])
               for l,row in enumerate(domains)]
    return {'status':'PERFECT_MATCHING_SUPPORTED','matching':matched,
            'removed_edges':sum(map(len,domains))-sum(map(len,supported))},supported
