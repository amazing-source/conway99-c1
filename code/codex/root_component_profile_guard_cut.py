"""Lift a continuation contradiction to a subset of fixed profile choices.

Unfixed profiles are relaxed separately at every incident edge. For a
fixed row, an edge contributes to a known-pair quota necessarily if
ALL compatible profiles of its other endpoint contain that known
vertex, and possibly if ANY does. Lower/upper cardinality constraints
therefore contain every genuine completion. Their propagation can
prove a profile no-good without fixing all outside profiles.
"""

from collections import deque
from itertools import combinations
from root_component_p3_neighbor_support import prepare_profile, edge_failure

if not __debug__:
    raise RuntimeError('Guard-cut certificates require assertions; do not use python -O.')


def propagate(bounds, edge_count, proof=None):
    state = [-1]*edge_count; trace = []
    if proof is not None:
        for step in proof['trace']:
            c = bounds[step['constraint']]
            free = [e for e in c['edges'] if state[e] == -1]
            ones = sum(state[e] == 1 for e in c['edges'])
            assert free == step['edges'] and free
            assert (step['value'] == 0 and ones == c['upper']) or (step['value'] == 1 and ones+len(free) == c['lower'])
            for e in free: state[e] = step['value']
        c = bounds[proof['conflict']]; ones = sum(state[e] == 1 for e in c['edges'])
        free = sum(state[e] == -1 for e in c['edges'])
        assert ones > c['upper'] or ones+free < c['lower']
        return True
    occurrence = [[] for _ in state]
    for ci, c in enumerate(bounds):
        for e in c['edges']: occurrence[e].append(ci)
    queue = deque(range(len(bounds))); pending = set(queue)
    while queue:
        ci = queue.popleft(); pending.remove(ci); c = bounds[ci]
        free = [e for e in c['edges'] if state[e] == -1]
        ones = sum(state[e] == 1 for e in c['edges'])
        if ones > c['upper'] or ones+len(free) < c['lower']:
            result = {'trace': trace, 'conflict': ci}
            assert propagate(bounds, edge_count, result)
            return result
        if not free or (ones != c['upper'] and ones+len(free) != c['lower']): continue
        value = int(ones+len(free) == c['lower'])
        trace.append({'constraint': ci, 'edges': free, 'value': value})
        for e in free:
            state[e] = value
            for cj in occurrence[e]:
                if cj not in pending: pending.add(cj); queue.append(cj)
    return None


class GuardOracle:
    def __init__(self, rows, known, outside, domains, selected, root_count=7):
        self.rows=rows; self.known=known; self.outside=outside; self.domains=domains
        self.selected=selected; self.roots=root_count
        self.prepared=[[prepare_profile(rows,known,q,p,root_count) for p in d] for q,d in zip(outside,domains)]
        self.relaxed={}
        for x,pi in enumerate(selected):
            a=self.prepared[x][pi]
            for y,domain in enumerate(self.prepared):
                if x==y: continue
                choices=[b['mask'] for b in domain if edge_failure(a,b) is None]
                if choices:
                    union=0; inter=(1<<len(rows))-1
                    for b in choices: union|=b; inter&=b
                    self.relaxed[x,y]=(union,inter)

    def system(self,fixed):
        fixed=set(fixed);edges=[];incidence={x:[] for x in fixed}
        for x,y in combinations(range(len(self.domains)),2):
            if x not in fixed and y not in fixed:continue
            if x in fixed and y in fixed:
                a=self.prepared[x][self.selected[x]];b=self.prepared[y][self.selected[y]]
                if edge_failure(a,b) is not None:continue
                ei=len(edges);edges.append((x,y))
                incidence[x].append((ei,y,b['mask'],b['mask']))
                incidence[y].append((ei,x,a['mask'],a['mask']))
            else:
                a,b=(x,y) if x in fixed else (y,x)
                if (a,b) not in self.relaxed:continue
                union,inter=self.relaxed[a,b];ei=len(edges);edges.append((x,y))
                incidence[a].append((ei,b,union,inter))
        bounds=[]
        for x in sorted(fixed):
            pi=self.selected[x];p=self.domains[x][pi];q=self.outside[x]
            a=self.prepared[x][pi];row=incidence[x];roots={l//2 for l in q}
            def add(kind,index,edges,lo,hi):
                bounds.append({'vertex':x,'kind':kind,'index':index,'edges':edges,'lower':lo,'upper':hi})
            target=2*self.roots-2-len(p)
            add('degree',None,[e for e,_,_,_ in row],target,target)
            for l in range(2*self.roots):
                target=(1 if l//2 in roots else 2)-sum(l in self.known[v] for v in p)
                add('letter',l,[e for e,y,_,_ in row if l in self.outside[y]],target,target)
            for u,known_row in enumerate(self.rows):
                target=2-int(u in p)-len(set(q)&set(self.known[u]))-(a['mask']&known_row).bit_count()
                possible=[e for e,y,union,inter in row if union&(1<<u)]
                mandatory=[e for e,y,union,inter in row if inter&(1<<u)]
                if possible==mandatory:add('known_equal',u,possible,target,target)
                else:
                    add('known_lower',u,possible,target,len(possible))
                    add('known_upper',u,mandatory,0,target)
        return edges,bounds

    def refute(self,fixed):
        edges,bounds=self.system(fixed);proof=propagate(bounds,len(edges))
        return proof

    def minimize(self):
        fixed=set(range(len(self.domains)))
        if self.refute(fixed) is None:return None
        trials=0
        for x in sorted(fixed):
            trial=fixed-{x};trials+=1
            if self.refute(trial) is not None:fixed=trial
        edges,bounds=self.system(fixed);proof=propagate(bounds,len(edges));assert proof is not None
        return {'kind':'continuation_guard','guards':[(x,self.selected[x]) for x in sorted(fixed)],
                'support_options':[],'proof':proof,'constraint_count':len(bounds),'edge_count':len(edges),
                'minimization_trials':trials,'scope':'This guard subset has no completion; no global family exclusion.'}


def check_guard_cut(rows,known,outside,domains,cut,root_count=7):
    selected=[0]*len(domains)
    for x,pi in cut['guards']:selected[x]=pi
    oracle=GuardOracle(rows,known,outside,domains,selected,root_count)
    edges,bounds=oracle.system(x for x,pi in cut['guards'])
    return propagate(bounds,len(edges),cut['proof'])


def controls():
    o=GuardOracle([0],[(0,2)],[(0,3),(1,2),(1,3)],[[[0]],[[0]],[[],[0]]],[0,0,0],2)
    assert o.refute({0,1,2}) is None
    o=GuardOracle([0],[(0,2)],[(0,3),(1,2),(1,3)],[[[0]],[[0]],[[],[0]]],[0,0,1],2)
    cut=o.minimize();assert cut is not None
    assert check_guard_cut(o.rows,o.known,o.outside,o.domains,cut,2)
    return {'rook_completion_preserved':True,'false_profile_guard':cut}
