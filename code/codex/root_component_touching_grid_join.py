"""Finite 36-vertex extension with two adjacent nongrid X rectangles.

Keep an opposite disjoint pair Q03,Q12 and the three Y grids. Of the
four other X rectangles, the two through `centre` are nongrids and the
other two are grids. Their eight nongrid vertices induce C8 or 2C4.

Enumerate two grid attachments, then eight labelled triples of Y
neighbours with the exact residual pair margins. Carry the entire
114-element catalogue of admissible 2-regular cores during this search.
Finally enumerate the two bijections to the disjoint X grids. This is
an integer search, without a chosen Gram or a symmetry of the graph.
Limits return UNKNOWN, never an exclusion. A surviving 36-vertex graph
is only a partial graph, not an SRG(99,14,1,2).
"""

import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_5602_grid_join import (
    LABELS, SHARED, PERMS, PAIRS, attachment_margins, grid_catalogue, square,
)
from root_component_5602_grid_marginals import test as margin_test

XRECTS = ((0,1), (0,2), (1,3), (2,3))
YRECTS = ((4,5), (4,6), (5,6))
WORDS = tuple(product(range(4), repeat=3))
WORD_CELLS = tuple(tuple(16*k+4*w[a]+w[b] for k,(a,b) in enumerate(PAIRS)) for w in WORDS)
OUTSIDE = tuple((2*a+s,2*b+t) for a in range(4) for b in range(4,7)
                for s,t in product(range(2),repeat=2))
F = (3,2,1,0)


@lru_cache(maxsize=8)
def boundary_margins(boundary):
    return margin_test(boundary)


@lru_cache(maxsize=8)
def cached_grid_catalogue(q,boundary,margins):
    return grid_catalogue(q,boundary,margins)[0]


@lru_cache(None)
def grid_words(ids):
    return tuple(tuple(PERMS[ids[b]][i] for b in range(3)) for i in range(4))


@lru_cache(None)
def conjugate_oppositions(ids):
    return tuple(tuple(PERMS[pid].index(F[PERMS[pid][i]]) for i in range(4)) for pid in ids)


@lru_cache(None)
def opposite_profile_images(oppositions,z):
    """Only 3^3 opposition triples and 4^3 words occur in this table.

An edge to grid corner t requires z_b in {t,F(t),O_b(t)} for every
Y grid b: otherwise the grid corner and Y neighbour already have
three common neighbours. The coincidence counts also respect the
nongrid-to-grid C2 inequalities before the unknown core is added.
"""
    count=tuple(z.count(j) for j in range(4))
    return tuple(t for t in range(4)
                 if all(z[b] in (t,F[t],oppositions[b][t]) for b in range(3))
                 and all(count[j]+square(t,j)<=2-int(t==j) for j in range(4)))


def profile_images(ids,word):
    z=tuple(PERMS[ids[b]].index(word[b]) for b in range(3))
    return opposite_profile_images(conjugate_oppositions(ids),z)


def layout(centre):
    nongrids = tuple(q for q,r in enumerate(XRECTS) if centre in r)
    grids = tuple(q for q in range(4) if q not in nongrids)
    vertices = tuple(8+4*q+i for q in nongrids for i in range(4))
    opposite = tuple(next(q for q in grids if set(XRECTS[q]).isdisjoint(XRECTS[r])) for r in nongrids)
    return nongrids, grids, vertices, opposite


def mapped_cores(records, centre):
    """Relabel LAB's Q01,Q02 cores without imposing a new quotient."""
    nongrids,_,vertices,_ = layout(centre)
    others = [next(a for a in XRECTS[q] if a != centre) for q in nongrids]
    canonical = [(s,2*b+t) for b in (1,2) for s,t in product(range(2),repeat=2)]
    root_map = (centre,*others)
    mapping = []
    for q in canonical:
        label = tuple(sorted(2*root_map[l//2]+l%2 for l in q))
        mapping.append(vertices.index(LABELS.index(label)))
    output=[]
    for record in records:
        k=[[0]*8 for _ in range(8)]
        for i,j in record['edges']:
            a,b=mapping[i],mapping[j]; k[a][b]=k[b][a]=1
        deficit=[[0 if i==j else 2-k[i][j]-SHARED[vertices[i]][vertices[j]]-
                  sum(k[i][w]*k[j][w] for w in range(8)) for j in range(8)] for i in range(8)]
        assert all(sum(row)==2 for row in k)
        output.append((k,deficit))
    return output


@lru_cache(maxsize=4)
def core_filter_data(edge_records,centre):
    patterns=mapped_cores([{'edges':e} for e in edge_records],centre)
    allowed=[[[sum(1<<ki for ki,(_,t) in enumerate(patterns) if n<=t[u][v])
               for n in range(4)] for v in range(8)] for u in range(8)]
    return patterns,allowed


def base_domains(boundary, margins, vertices):
    counts=[[sum(bool(bits&(1<<i)) for i in range(8) if l in LABELS[i]) for l in range(8)]
            for bits in boundary]
    result=[]
    for v in vertices:
        domain=[]
        for wi,w in enumerate(WORDS):
            if any(sum(bool(boundary[4*b+w[b]]&(1<<u)) for b in range(3))>
                   2-SHARED[v][u] for u in range(8)): continue
            if any(margins[k][w[a]][w[b]]==0 for k,(a,b) in enumerate(PAIRS)): continue
            if any(counts[4*b+w[b]][l]>=2 for b in range(3) for l in LABELS[v]): continue
            domain.append(wi)
        result.append(domain)
    return result,counts


def materialize(core,boundary,centre,grid_ids,words,k,matchings):
    _,grids,vertices,opposite=layout(centre)
    g=[[0]*36 for _ in range(36)]
    def edge(u,v): g[u][v]=g[v][u]=1
    for u,v in combinations(range(8),2):
        if core[u][v]: edge(u,v)
    for j,bits in enumerate(boundary):
        for u in range(8):
            if bits&(1<<u): edge(u,24+j)
    for q in grids:
        for i,j in combinations(range(4),2):
            if square(i,j): edge(8+4*q+i,8+4*q+j)
        for b,pid in enumerate(grid_ids[q]):
            for i,j in enumerate(PERMS[pid]): edge(8+4*q+i,24+4*b+j)
    for b in range(3):
        for i,j in combinations(range(4),2):
            if square(i,j): edge(24+4*b+i,24+4*b+j)
    for i,v in enumerate(vertices):
        for b,j in enumerate(words[i]): edge(v,24+4*b+j)
    for i,j in combinations(range(8),2):
        if k[i][j]: edge(vertices[i],vertices[j])
    for side,p in enumerate(matchings):
        for i,j in enumerate(p): edge(vertices[4*side+i],8+4*opposite[side]+j)
    return g


def check_partial(g,centre):
    """Check the necessary 36-vertex conditions, with correct closed pairs."""
    _,grids,_,_=layout(centre)
    for u in range(36):
        if sum(g[u]) != (6 if u<24 else 8): return 'degree'
        for l in range(14):
            if (sum(g[u][v] for v in range(36) if l in LABELS[v])>
                    2-int(l in LABELS[u])-int((l^1) in LABELS[u])): return 'letter_quota'
    for u,v in combinations(range(36),2):
        n=sum(g[u][w]*g[v][w] for w in range(36))
        target=2-g[u][v]-SHARED[u][v]
        closed=v<8 or u>=24 or (u//4==v//4 and u//4-2 in grids)
        if n>target or (closed and n!=target): return 'common_neighbours'
    return None


def frontier(g,centre):
    """Complete four-neighbour profiles, now allowing two nongrid neighbours."""
    nongrids,grids,vertices,_=layout(centre)
    deficits=[[12-sum(g[u]) if u==v else 2-g[u][v]-SHARED[u][v]-
               sum(g[u][w]*g[v][w] for w in range(36)) for v in range(36)] for u in range(36)]
    ld=[[2-int(l in LABELS[u])-int((l^1) in LABELS[u])-
         sum(g[u][v] for v in range(36) if l in LABELS[v]) for l in range(14)] for u in range(36)]
    assert all(min(r)>=0 for r in deficits+ld)
    domains=[]
    for qi,q in enumerate(OUTSIDE):
        a,b=(l//2 for l in q)
        xgrids=[r for r in grids if a not in XRECTS[r]]
        ygrid=next(i for i,r in enumerate(YRECTS) if b not in r)
        # Each missing vertex has two neighbours in the 16-vertex block.
        n_ng=2-len(xgrids)
        good=[]; rejected=Counter(); total=0
        for u,ng,gs,y in product(range(8),combinations(vertices,n_ng),
                                 product(range(4),repeat=len(xgrids)),range(4)):
            profile=(u,*ng,*(8+4*r+j for r,j in zip(xgrids,gs)),24+4*ygrid+y)
            assert len(profile)==4; total+=1
            if any(deficits[i][j]==0 for i,j in combinations(profile,2)):
                rejected['known_pair_saturated']+=1;continue
            if any(ld[v][l]==0 for v in profile for l in q):
                rejected['known_vertex_letter_quota']+=1;continue
            if any(sum(g[v][u] for u in profile)>2-int(v in profile)-len(set(q)&set(LABELS[v]))
                   for v in range(36)):
                rejected['new_to_known_C2']+=1;continue
            if any(sum(l in LABELS[v] for v in profile)>2-int(l in q)-int((l^1) in q)
                   for l in range(14)):
                rejected['new_vertex_letter_quota']+=1;continue
            good.append(profile)
        if not good:
            return {'status':'EXCLUDED_EMPTY_VERTEX_DOMAIN','outside_index':qi,'outside_letters':q,
                    'total_profiles':total,'rejected_by':dict(rejected),
                    'earlier_domain_sizes':[len(d) for d in domains]}
        domains.append(good)
    for u in range(36):
        for v in range(u,36):
            demand=deficits[u][v]
            minimum=sum(all(u in p and v in p for p in d) for d in domains)
            maximum=sum(any(u in p and v in p for p in d) for d in domains)
            if not minimum<=demand<=maximum:
                return {'status':'EXCLUDED_PROFILE_CAPACITY','known_vertices':[u,v],
                        'demand':demand,'minimum':minimum,'maximum':maximum,
                        'domain_sizes':[len(d) for d in domains]}
    return {'status':'PASSES_SINGLE_VERTEX_AND_PAIR_CAPACITY','domain_sizes':[len(d) for d in domains]}


class SearchLimit(Exception):
    pass


def solve(core,boundary,centre,records,node_limit=0,use_frontier=False):
    start=time.process_time();boundary=tuple(boundary);marginal=boundary_margins(boundary)
    out={'centre':centre,'is_complete_graph':False,'uses_E3':True}
    if marginal['status']=='EXCLUDED_BOUNDARY':
        return {**out,'status':'EXCLUDED_BY_INTEGER_MARGINS','cpu_seconds':time.process_time()-start}
    margins=tuple(marginal['margins']);target=sum((sum(m,()) for m in margins),())
    nongrids,grids,vertices,opposite=layout(centre)
    cats={q:cached_grid_catalogue(q,boundary,margins) for q in grids}
    out['grid_catalogue_sizes']=[len(cats[q]) for q in grids]
    domains,core_letter_counts=base_domains(boundary,margins,vertices)
    out['nongrid_row_domain_sizes']=list(map(len,domains))
    edge_records=tuple(tuple(tuple(e) for e in r['edges']) for r in records)
    patterns,allowed=core_filter_data(edge_records,centre)
    counts=Counter();witness=None;certificates=[]

    def finish(ids,assigned,kmask,options):
        nonlocal witness
        counts['complete_row_assignments']+=1
        words=[WORDS[i] for i in assigned]
        while kmask:
            low=kmask&-kmask;ki=low.bit_length()-1;kmask-=low
            k,_=patterns[ki];match_cats=[]
            for side,q in enumerate(opposite):
                attached_words=grid_words(ids[q])
                good=[]
                for p in PERMS:
                    if any(p[i] not in options[4*side+i][assigned[4*side+i]] for i in range(4)):continue
                    inverse=[p.index(j)+4*side for j in range(4)]
                    valid=True
                    # All nongrid-to-this-grid C2 inequalities.
                    for u in range(8):
                        for j in range(4):
                            common=sum(a==b for a,b in zip(words[u],attached_words[j]))+k[u][inverse[j]]
                            if u//4==side:common+=square(p[u%4],j)
                            adj=int(u//4==side and p[u%4]==j)
                            if common>2-adj-SHARED[vertices[u]][8+4*q+j]:valid=False;break
                        if not valid:break
                    if not valid:continue
                    for i in range(4):
                        u=4*side+i;gv=8+4*q+p[i]
                        for l in range(8):
                            if (sum(k[u][v] for v in range(8) if l in LABELS[vertices[v]])+int(l in LABELS[gv])>
                                    2-int(l in LABELS[vertices[u]])-int((l^1) in LABELS[vertices[u]])):valid=False;break
                        if not valid:break
                        for b in range(3):
                            for j in range(4):
                                n=sum(k[u][v] for v in range(8) if words[v][b]==j)
                                n+=square(words[u][b],j)+int(attached_words[p[i]][b]==j)
                                if n>2-int(words[u][b]==j):valid=False;break
                                # Grid corner p[i] has its two square neighbours and u.
                                n=sum(square(p[i],t) for t in range(4) if attached_words[t][b]==j)
                                n+=square(attached_words[p[i]][b],j)+int(words[u][b]==j)
                                if n>2-int(attached_words[p[i]][b]==j):valid=False;break
                            if not valid:break
                        if not valid:break
                    if valid:good.append(p)
                match_cats.append(good)
                if not good:break
            if len(match_cats)<2 or not all(match_cats):continue
            for ma,mb in product(*match_cats):
                g=materialize(core,boundary,centre,ids,words,k,(ma,mb))
                failure=check_partial(g,centre)
                if failure:counts['last_check_'+failure]+=1;continue
                counts['valid_partial36']+=1
                cert=frontier(g,centre) if use_frontier else None
                record={'grid_ids':ids,'words':words,'pair_core_index':ki,'matchings':[ma,mb]}
                if cert and cert['status'].startswith('EXCLUDED_'):
                    counts['frontier_obstruction']+=1
                    certificates.append({'construction':record,'certificate':cert});continue
                witness={**record,'adjacency':g,'frontier':cert};return True
        return False

    def grid_pair(ids):
        ga,gb=grids
        wa=grid_words(ids[ga]);wb=grid_words(ids[gb])
        if any(sum(a==b for a,b in zip(wa[i],wb[j]))>2-SHARED[8+4*ga+i][8+4*gb+j]
               for i,j in product(range(4),repeat=2)):return False
        residual=[t-a-b for t,a,b in zip(target,attachment_margins(ids[ga]),attachment_margins(ids[gb]))]
        if min(residual)<0:return False
        used=[r[:] for r in core_letter_counts]
        for q,wq in ((ga,wa),(gb,wb)):
            for i,w in enumerate(wq):
                for b,j in enumerate(w):
                    for l in LABELS[8+4*q+i]:used[4*b+j][l]+=1
        if any(max(r)>2 for r in used):return False
        ds=[];options=[]
        for u,v in enumerate(vertices):
            q=opposite[u//4];wq=wa if q==ga else wb
            other=wb if q==ga else wa;oq=gb if q==ga else ga
            good=[];match_options={}
            for wi in domains[u]:
                w=WORDS[wi]
                if any(residual[c]==0 for c in WORD_CELLS[wi]):continue
                if any(used[4*b+w[b]][l]>=2 for b in range(3) for l in LABELS[v]):continue
                if any(sum(a==b for a,b in zip(w,other[j]))>2-SHARED[v][8+4*oq+j] for j in range(4)):continue
                ts=profile_images(ids[q],w)
                if ts:good.append(wi);match_options[wi]=ts
            if not good:return False
            ds.append(good);options.append(match_options)
        counts['grid_pairs_with_row_domains']+=1
        order=sorted(range(8),key=lambda u:len(ds[u]));assigned=[-1]*8
        def visit(depth,kmask):
            counts['nodes']+=1
            if node_limit and counts['nodes']>node_limit:raise SearchLimit
            if depth==8:
                assert not any(residual)
                return finish(ids,assigned,kmask,options)
            u=order[depth];v=vertices[u]
            for wi in ds[u]:
                cells=WORD_CELLS[wi];w=WORDS[wi]
                if any(residual[c]==0 for c in cells):continue
                if any(used[4*b+w[b]][l]>=2 for b in range(3) for l in LABELS[v]):continue
                mask=kmask
                for z in order[:depth]:
                    n=sum(a==b for a,b in zip(w,WORDS[assigned[z]]));mask&=allowed[u][z][n]
                    if not mask:break
                if not mask:continue
                assigned[u]=wi
                for c in cells:residual[c]-=1
                for b,j in enumerate(w):
                    for l in LABELS[v]:used[4*b+j][l]+=1
                if visit(depth+1,mask):return True
                for c in cells:residual[c]+=1
                for b,j in enumerate(w):
                    for l in LABELS[v]:used[4*b+j][l]-=1
                assigned[u]=-1
            return False
        return visit(0,(1<<len(patterns))-1)
    try:
        for aa,bb in product(cats[grids[0]],cats[grids[1]]):
            counts['grid_pairs']+=1
            if grid_pair({grids[0]:aa,grids[1]:bb}):break
        status='FEASIBLE_PARTIAL_36' if witness else 'EXCLUDED_BY_EXHAUSTIVE_JOIN'
    except SearchLimit:
        status='UNKNOWN_NODE_LIMIT'
    out.update(status=status,counts=dict(counts),witness=witness,
               frontier_certificates=certificates,cpu_seconds=time.process_time()-start)
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cover',type=Path,required=True)
    p.add_argument('--pair-cores',type=Path,required=True)
    p.add_argument('--orbit',type=int,nargs='*')
    p.add_argument('--boundary-indices',type=int,nargs='*')
    p.add_argument('--centres',type=int,nargs='+',default=[0,1,2,3])
    p.add_argument('--node-limit',type=int,default=0)
    p.add_argument('--log-every',type=int,default=25)
    p.add_argument('--frontier',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--resume',action='store_true')
    args=p.parse_args();assert args.resume or not args.output.exists()
    resources=limit_research_process(1)
    data=json.loads(args.cover.read_text(encoding='utf8'))
    orbits=data.get('orbit_reduction',data)['orbits']
    records=json.loads(args.pair_cores.read_text(encoding='utf8'))
    sources={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in (args.cover,args.pair_cores)}
    out={'scope':__doc__,'resources':resources,'sources':sources,
        'cases':[],'global_Conway_exclusion':False,'whole_family_excluded':False}
    completed=set()
    if args.resume:
        out=json.loads(args.output.read_text(encoding='utf8'))
        assert out['sources']==sources
        for rec in out['cases']:
            key=(rec['orbit'],rec['boundary_index'],rec['result']['centre'])
            assert key not in completed
            completed.add(key)
    out.setdefault('program_versions',[]).append({
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'resumed_after_cases':len(completed),'node_limit':args.node_limit,
        'frontier_enabled':args.frontier,'uses_27_opposition_profiles':True})
    for oi,orbit in enumerate(orbits):
        if args.orbit is not None and oi not in args.orbit:continue
        for bi,case in enumerate(orbit['boundaries']['cases']):
            if args.boundary_indices is not None and bi not in args.boundary_indices:continue
            for centre in args.centres:
                assert centre in range(4)
                if (oi,bi,centre) in completed:continue
                result=solve(orbit['representative'],case['core_neighbours_of_grid_vertices'],
                             centre,records,args.node_limit,args.frontier)
                out['cases'].append({'orbit':oi,'boundary_index':bi,'result':result})
                out['counts']=dict(Counter(r['result']['status'] for r in out['cases']))
                atomic_json_write(args.output,out)
                if len(out['cases'])%args.log_every==0 or not result['status'].startswith('EXCLUDED_'):
                    print(json.dumps({'orbit':oi,'boundary_index':bi,'centre':centre,
                                      'processed':len(out['cases']),'status':result['status'],
                                      'counts':out['counts'],
                                      'total_cpu_seconds':sum(c['result']['cpu_seconds'] for c in out['cases'])}),flush=True)
    print(json.dumps({'processed':len(out['cases']),'counts':out.get('counts'),
                      'total_cpu_seconds':sum(c['result']['cpu_seconds'] for c in out['cases'])}),flush=True)


if __name__=='__main__':main()
