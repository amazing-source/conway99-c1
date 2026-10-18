"""Finite integer enumeration of the 36-vertex grid core of template 5602.

An opposite pair of X-grids has one perfect matching M between them.
Their three coincidence permutations through the Y-grids sum to
M + F M + M F, where F interchanges opposite corners of a square.
There are 456 ordered decompositions for all 24 choices of M. Attach
one X-grid, derive the opposite one from these patterns, and join the
two opposite pairs by the three fixed Y-grid common-neighbour margins.
No SAT solver, floating point, chosen Gram, or time-based exclusion.
"""

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_5602_grid_core import CORE, GRIDS, closed_pair
from root_component_5602_grid_marginals import test as marginal_test

PERMS = tuple(permutations(range(4)))
PERM_ID = {p:i for i,p in enumerate(PERMS)}
F = (3,2,1,0)
PAIRS = ((0,1),(0,2),(1,2))
LABELS = tuple((a,b) for q in CORE+GRIDS
               for a in (2*q[0],2*q[0]+1) for b in (2*q[1],2*q[1]+1))
SHARED = tuple(tuple(len(set(a)&set(b)) for b in LABELS) for a in LABELS)


def square(i,j):
    return int(i!=j and F[i]!=j)


@lru_cache(None)
def patterns():
    result=[]
    for mi,m in enumerate(PERMS):
        target=[[0]*4 for _ in range(4)]
        for i in range(4):
            for j in (m[i],m[F[i]],F[m[i]]):target[i][j]+=1
        valid=[p for p in PERMS if all(target[i][p[i]] for i in range(4))]
        for p,q in product(valid,repeat=2):
            remaining=[row[:] for row in target]
            for i in range(4):
                remaining[i][p[i]]-=1
                remaining[i][q[i]]-=1
            if any(min(row)<0 or sum(row)!=1 for row in remaining):continue
            r=tuple(row.index(1) for row in remaining)
            if r in PERM_ID:result.append((mi,(PERM_ID[p],PERM_ID[q],PERM_ID[r])))
    assert len(result)==456
    return tuple(result)


@lru_cache(None)
def transition(mi,pi,li):
    """Return the opposite grid attachment, checking both X-to-Y C2 bounds."""
    m,p,left=PERMS[mi],PERMS[pi],PERMS[li]
    right=[0]*4
    for i in range(4):right[p[i]]=left[i]
    for i,k in product(range(4),repeat=2):
        c=sum(square(i,j)*(left[j]==k) for j in range(4))
        c+=square(left[i],k)+(right[m[i]]==k)
        if c>2-(left[i]==k):return -1
        c=sum(square(i,j)*(right[j]==k) for j in range(4))
        c+=square(right[i],k)+(left[m.index(i)]==k)
        if c>2-(right[i]==k):return -1
    return PERM_ID[tuple(right)]


def grid_catalogue(q,boundary,margins):
    domains=[]
    for w in range(8+4*q,12+4*q):
        valid=set()
        for choices in product(range(4),repeat=3):
            neighbours=[24+4*b+j for b,j in enumerate(choices)]
            if any(sum(bool(boundary[v-24]&(1<<u)) for v in neighbours)>2-SHARED[w][u]
                   for u in range(8)):continue
            if any(margins[k][choices[a]][choices[b]]==0 for k,(a,b) in enumerate(PAIRS)):continue
            # Already two core neighbours with the same upper letter leave
            # no quota for an X-grid neighbour carrying that letter.
            if any(sum(bool(boundary[v-24]&(1<<u)) for u in range(8) if letter in LABELS[u])>=2
                   for v in neighbours for letter in LABELS[w]):continue
            valid.add(choices)
        domains.append(valid)
    catalogue=[]
    for ids in product(range(24),repeat=3):
        ps=[PERMS[i] for i in ids]
        if all(tuple(p[i] for p in ps) in domains[i] for i in range(4)):
            catalogue.append(ids)
    return catalogue,[len(d) for d in domains]


@lru_cache(None)
def attachment_margins(ids):
    ps=[PERMS[i] for i in ids]
    result=[0]*48
    for k,(a,b) in enumerate(PAIRS):
        for i in range(4):result[16*k+4*ps[a][i]+ps[b][i]]+=1
    return tuple(result)


def pair_catalogue(left,right,target):
    lookup=set(right);result=defaultdict(list)
    for ids in left:
        for mi,ps in patterns():
            rids=tuple(transition(mi,p,l) for p,l in zip(ps,ids))
            if -1 in rids or rids not in lookup:continue
            margins=tuple(a+b for a,b in zip(attachment_margins(ids),attachment_margins(rids)))
            if any(a>b for a,b in zip(margins,target)):continue
            result[margins].append((ids,rids,mi))
    return result


def materialize(core,boundary,pair03,pair12):
    g=[[0]*36 for _ in range(36)]
    for u,v in combinations(range(8),2):g[u][v]=g[v][u]=core[u][v]
    for qi in range(2,9):
        for i,j in combinations(range(4),2):g[4*qi+i][4*qi+j]=g[4*qi+j][4*qi+i]=square(i,j)
    for j,bits in enumerate(boundary):
        for i in range(8):g[i][24+j]=g[24+j][i]=int(bool(bits&(1<<i)))
    for qa,qb,record in ((0,3,pair03),(1,2,pair12)):
        left,right,mi=record
        for qi,ids in ((qa,left),(qb,right)):
            for b,pid in enumerate(ids):
                for i,j in enumerate(PERMS[pid]):g[8+4*qi+i][24+4*b+j]=g[24+4*b+j][8+4*qi+i]=1
        for i,j in enumerate(PERMS[mi]):g[8+4*qa+i][8+4*qb+j]=g[8+4*qb+j][8+4*qa+i]=1
    return g


def check_graph(g):
    for w in range(36):
        for letter in range(14):
            bound=2-int(letter in LABELS[w])-int((letter^1) in LABELS[w])
            if sum(g[w][v] for v in range(36) if letter in LABELS[v])>bound:return 'letter_quota'
    masks=[sum(1<<j for j,x in enumerate(row) if x) for row in g]
    for u,v in combinations(range(36),2):
        total=(masks[u]&masks[v]).bit_count();target=2-g[u][v]-SHARED[u][v]
        if total>target:return 'common_neighbour_bound'
        if closed_pair(u,v) and total!=target:return 'closed_pair_equality'
    return None


def solve(core,boundary):
    start=time.process_time();marginal=marginal_test(boundary)
    out={'method':'exhaustive integer grid join','is_complete_graph':False}
    if marginal['status']=='EXCLUDED_BOUNDARY':
        out.update(status='EXCLUDED_BY_INTEGER_MARGINS',marginal=marginal,cpu_seconds=time.process_time()-start)
        return out
    margins=marginal['margins'];target=sum((sum(m,()) for m in margins),())
    cats=[];row_domains=[]
    for q in range(4):
        c,d=grid_catalogue(q,boundary,margins);cats.append(c);row_domains.append(d)
    out.update(row_domains=row_domains,grid_catalogue_sizes=[len(c) for c in cats])
    pair03=pair_catalogue(cats[0],cats[3],target)
    pair12=pair_catalogue(cats[1],cats[2],target)
    out['pair_catalogue_sizes']=[sum(map(len,p.values())) for p in (pair03,pair12)]
    out['pair_margin_keys']=[len(p) for p in (pair03,pair12)]
    counts=Counter();joins=0
    for key,lefts in pair03.items():
        rem=tuple(a-b for a,b in zip(target,key))
        for a,b in product(lefts,pair12.get(rem,())):
            joins+=1;g=materialize(core,boundary,a,b);failure=check_graph(g)
            if failure:counts[failure]+=1;continue
            out.update(status='FEASIBLE_PARTIAL_36',adjacency=g,labels=LABELS,
                       integer_witness_checked=True,pair_witness=[a,b],joined_candidates=joins,
                       rejected_joins=dict(counts),cpu_seconds=time.process_time()-start)
            return out
    out.update(status='EXCLUDED_BY_EXHAUSTIVE_JOIN',joined_candidates=joins,
               rejected_joins=dict(counts),cpu_seconds=time.process_time()-start)
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cores',type=Path,required=True)
    p.add_argument('--orbit',type=int,nargs='*')
    p.add_argument('--boundary-indices',type=int,nargs='*')
    p.add_argument('--previous',type=Path,help='Only UNKNOWN cases of a previous grid-core campaign.')
    p.add_argument('--stop-on-feasible',action='store_true')
    p.add_argument('--log-every',type=int,default=1)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();assert not args.output.exists();resources=limit_research_process(1)
    data=json.loads(args.cores.read_text(encoding='utf8'))
    orbits=data.get('orbit_reduction',data)['orbits']
    selected=None
    if args.previous:
        selected={(c['orbit'],c['boundary_index']) for c in json.loads(args.previous.read_text(encoding='utf8'))['cases']
                  if c['result']['status']=='UNKNOWN'}
    out={'scope':__doc__,'source':str(args.cores),'source_sha256':hashlib.sha256(args.cores.read_bytes()).hexdigest(),
         'resources':resources,'cases':[],'whole_template_excluded':False,'global_Conway_exclusion':False}
    for i,orbit in enumerate(orbits):
        if args.orbit is not None and i not in args.orbit:continue
        for j,case in enumerate(orbit['boundaries']['cases']):
            if args.boundary_indices is not None and j not in args.boundary_indices:continue
            if selected is not None and (i,j) not in selected:continue
            result=solve(orbit['representative'],case['core_neighbours_of_grid_vertices'])
            out['cases'].append({'orbit':i,'boundary_index':j,'mask':orbit['mask'],'result':result})
            atomic_json_write(args.output,out)
            if len(out['cases'])%args.log_every==0 or result['status']=='FEASIBLE_PARTIAL_36':
                print(json.dumps({'orbit':i,'boundary_index':j,'processed':len(out['cases']),
                                  'counts':dict(Counter(c['result']['status'] for c in out['cases'])),
                                  **{k:v for k,v in result.items()
                              if k not in ('adjacency','labels','marginal','pair_witness')}}),flush=True)
            if args.stop_on_feasible and result['status']=='FEASIBLE_PARTIAL_36':return
    out['counts']=dict(Counter(c['result']['status'] for c in out['cases']))
    out['total_cpu_seconds']=sum(c['result']['cpu_seconds'] for c in out['cases'])
    atomic_json_write(args.output,out)
    print(json.dumps({'processed':len(out['cases']),'counts':out['counts'],
                      'total_cpu_seconds':out['total_cpu_seconds']}),flush=True)


if __name__=='__main__':main()
