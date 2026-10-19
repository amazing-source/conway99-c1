"""Attach Q12 by four simple factors, then test the exact 24-vertex frontier.

Scope: H01=-H02 nonzero, Q12 and Q45,Q46,Q56 grids, E3 for the core
catalogue. All other rectangles are free. A passing frontier is only
a partial graph, never a Conway construction or a proof of extendibility.
"""

import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_shared_core_colors import PAIRS, PAIR_ID, colourings
from root_component_shared_k3_boundary import matching_catalogue
from root_component_profile_inclusion import inclusion_filter

P4 = tuple(permutations(range(4)))
P4_ID = {p:i for i,p in enumerate(P4)}
RECTANGLES = ((0,1),(0,2),(1,2),(4,5),(4,6),(5,6))
LABELS = tuple((2*a+s,2*b+t) for a,b in RECTANGLES for s,t in product(range(2),repeat=2))
SHARED = tuple(tuple(len(set(a)&set(b)) for b in LABELS) for a in LABELS)
LETTER_MASKS = tuple(sum(1<<i for i,q in enumerate(LABELS) if l in q) for l in range(14))
Y_ROOTS = RECTANGLES[3:]
CROSS = tuple((a,b) for a in (0,1,2) for b in (4,5,6))
ROOT3 = tuple(tuple(sorted((3,a))) for a in (0,1,2,4,5,6))
OUTSIDE = tuple((2*a+s,2*b+t) for a,b in CROSS+ROOT3 for s,t in product(range(2),repeat=2))


def write_result(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.suffix!='.gz':
        atomic_json_write(path,value)
        return
    temporary=path.with_name(path.name+'.tmp')
    temporary.write_bytes(gzip.compress((json.dumps(value,separators=(',',':'))+'\n').encode('utf8'),mtime=0))
    for attempt in range(200):
        try:
            temporary.replace(path);return
        except PermissionError:
            if attempt==199:raise
            time.sleep(.05)


@lru_cache(None)
def rainbow(allowed):
    return tuple(pi for pi,p in enumerate(P4)
                 if all(allowed[p[j]]&(1<<j) for j in range(4)))


class Attachments:
    def __init__(self,core):
        _, factors = colourings(core)
        # A D-label already sees its two core neighbours and its Q12 colour.
        # Three carrying the same upper letter are forbidden.
        forbidden = []
        for j in range(4):
            forbidden.append(sum(1<<k for k,(u,v) in enumerate(PAIRS)
                if (u<4)==(v<4) and u%2==v%2 and u%2==(j//2 if u<4 else j%2)))
        self.factors = [fs for fs in factors if all(not(fs[j]&forbidden[j]) for j in range(4))]
        self.keys = [c['key'] for c in matching_catalogue(core)]
        self.index = {key:i for i,key in enumerate(self.keys)}
        self.options = []; self.support = []
        for key in self.keys:
            ids = [PAIR_ID[tuple(v for v in range(8) if mask&(1<<v))] for mask in key]
            options = {};support = 0
            for fi,fs in enumerate(self.factors):
                allowed = tuple(sum(1<<j for j in range(4) if fs[j]&(1<<k)) for k in ids)
                choices = rainbow(allowed)
                if choices:
                    options[fi] = choices;support |= 1<<fi
            self.options.append(options);self.support.append(support)

    @lru_cache(None)
    def patterns(self,indices):
        a,b,c = indices
        common = self.support[a]&self.support[b]&self.support[c]
        result = set()
        while common:
            bit = common&-common;fi = bit.bit_length()-1;common ^= bit
            for ids in product(self.options[a][fi],self.options[b][fi],self.options[c][fi]):
                choices = [tuple(self.keys[m][e] for e in P4[p]) for m,p in zip(indices,ids)]
                if all(len({choices[g][j] for g in range(3)})==3 for j in range(4)):
                    result.add(ids)
        return tuple(sorted(result))

    def for_boundary(self,boundary):
        keys = tuple(tuple(sorted(boundary[4*b:4*b+4])) for b in range(3))
        indices = tuple(self.index[key] for key in keys)
        corner = [tuple(boundary[4*b:4*b+4].index(mask) for mask in keys[b]) for b in range(3)]
        for ids in self.patterns(indices):
            attached = tuple(tuple(corner[b][e] for e in P4[p]) for b,p in enumerate(ids))
            # Y labels in the same Q12 colour already have that neighbour
            # in common, in addition to their core pair intersection.
            if any((boundary[4*a+attached[a][j]]&boundary[4*b+attached[b][j]]).bit_count()
                   +SHARED[12+4*a+attached[a][j]][12+4*b+attached[b][j]]>1
                   for a,b in ((0,1),(0,2),(1,2)) for j in range(4)):
                continue
            yield attached


def materialize(core,boundary,attached):
    rows = [0]*24
    def edge(u,v):
        rows[u] |= 1<<v;rows[v] |= 1<<u
    for u,v in core['edges']:
        edge(u,v)
    for offset in (8,12,16,20):
        for i,j in combinations(range(4),2):
            if i^j != 3:
                edge(offset+i,offset+j)
    for k,mask in enumerate(boundary):
        for u in range(8):
            if mask&(1<<u):edge(u,12+k)
    for b in range(3):
        for j,k in enumerate(attached[b]):edge(8+j,12+4*b+k)
    assert all(row.bit_count()==5 for row in rows)
    return rows


@lru_cache(None)
def profiles(q):
    roots={l//2 for l in q}
    grids=[range(4*(b+3),4*(b+4)) for b,r in enumerate(Y_ROOTS) if roots.isdisjoint(r)]
    if 3 not in roots:
        first = range(8,12) if 0 in roots else range(8)
        return tuple((a,b) for a,b in product(first,grids[0]))
    a=next(i for i in roots if i!=3)
    if a==0:
        return tuple(product(range(8,12),*grids))
    if a in (1,2):
        return tuple(product(range(8),*grids))
    return tuple(pair+(j,k) for pair in combinations(range(8),2)
                 for j,k in product(range(8,12),grids[0]))


@lru_cache(None)
def profile_features(profile):
    return sum(1<<(24*u+v) for i,u in enumerate(profile) for v in profile[i:])


def propagate_profiles(domains,deficits,letter_deficits):
    """Exact cardinality propagation, including all known-letter equalities.

    Each missing vertex chooses one profile. For any required feature,
    all-or-none occurrence in its domain gives an integer lower/upper
    bound. Equality to a bound removes incompatible optional profiles.
    No numeric solver or relaxation is used.
    """
    demands={24*u+v:deficits[u][v] for u in range(24) for v in range(u,24)}
    demands.update({576+14*u+l:letter_deficits[u][l] for u in range(24) for l in range(14)})
    # N=Q34+Q35+Q36 and Z=Q03+Q04+Q05+Q06. The identities
    # H(K)=H(Q12)=H(Y)=0 force these counts separately.
    demands.update({912+u:3 if u<12 else 1 for u in range(24)})
    demands.update({936+u:0 if u<8 else (4 if u<12 else 2) for u in range(24)})
    features=[]
    profile_masks=[]
    for q,domain in zip(OUTSIDE,domains):
        roots={l//2 for l in q}
        region=912 if 3 in roots and roots&{4,5,6} else (
            936 if 0 in roots and roots&{3,4,5,6} else None)
        features.append([profile_features(p) | sum(1<<(576+14*u+l) for u in p for l in q) |
                         (sum(1<<(region+u) for u in p) if region is not None else 0)
                         for p in domain])
        profile_masks.append([sum(1<<u for u in p) for p in domain])
    active=[list(range(len(d))) for d in domains];rounds=[]
    while True:
        lower=[0]*960;upper=[0]*960;bounds=[]
        for vi,indices in enumerate(active):
            union=0;intersection=(1<<960)-1
            for i in indices:
                f=features[vi][i];union|=f;intersection&=f
            bounds.append((union,intersection))
            for mask,counts in ((union,upper),(intersection,lower)):
                while mask:
                    bit=mask&-mask;counts[bit.bit_length()-1]+=1;mask^=bit
        for k,target in demands.items():
            if not lower[k]<=target<=upper[k]:
                meaning=({'known_vertices':divmod(k,24)} if k<576 else
                         {'known_vertex':(k-576)//14,'upper_letter':(k-576)%14} if k<912 else
                         {'known_vertex':k%24,'outside_region':'N' if k<936 else 'Z'})
                return {'status':'EXCLUDED_PROFILE_PROPAGATION',**meaning,
                        'demand':target,'minimum':lower[k],'maximum':upper[k],
                        'rounds':rounds,'remaining_domain_sizes':list(map(len,active))},None
        tight_lower=sum(1<<k for k,t in demands.items() if lower[k]==t)
        tight_upper=sum(1<<k for k,t in demands.items() if upper[k]==t)
        changes=[]
        for vi,(union,intersection) in enumerate(bounds):
            optional=union&~intersection
            forbidden=optional&tight_lower;required=optional&tight_upper
            kept=[i for i in active[vi] if not(features[vi][i]&forbidden)
                  and features[vi][i]&required==required]
            if not kept:
                return {'status':'EXCLUDED_PROFILE_PROPAGATION','outside_index':vi,
                        'outside_letters':OUTSIDE[vi],'reason':'All profiles violate a tight cardinality bound',
                        'forced_zero_features':[k for k in demands if forbidden&(1<<k)],
                        'forced_one_features':[k for k in demands if required&(1<<k)],
                        'rounds':rounds},None
            if len(kept)<len(active[vi]):
                changes.append({'outside_index':vi,'removed':len(active[vi])-len(kept)})
                active[vi]=kept
        if not changes:
            # Scalar bounds miss the fact that two equal-total features
            # with nested supports must have identical chosen supports.
            inclusion,kept=inclusion_filter([[features[v][i] for i in ids]
                                            for v,ids in enumerate(active)],demands)
            if kept is None:
                return {**inclusion,'rounds':rounds},None
            if inclusion['removed_options']:
                active=[[ids[j] for j in indices] for ids,indices in zip(active,kept)]
                rounds.append({'feature_inclusions':inclusion['inclusions']})
                continue
            # Two missing vertices cannot already have more common
            # known neighbours than mu minus their shared upper letters.
            for vi,vj in combinations(range(len(domains)),2):
                cap=2-len(set(OUTSIDE[vi])&set(OUTSIDE[vj]))
                for a,b in ((vi,vj),(vj,vi)):
                    kept=[i for i in active[a] if any(
                        (profile_masks[a][i]&profile_masks[b][j]).bit_count()<=cap for j in active[b])]
                    if not kept:
                        return {'status':'EXCLUDED_OUTSIDE_PROFILE_C2','outside_vertices':[a,b],
                                'common_known_bound':cap,'rounds':rounds},None
                    if len(kept)<len(active[a]):
                        changes.append({'outside_index':a,'incompatible_with':b,
                                        'removed':len(active[a])-len(kept)})
                        active[a]=kept
            if changes:
                rounds.append(changes)
                continue
            return {'status':'PASSES_PROFILE_PROPAGATION','rounds':rounds},[
                [domain[i] for i in indices] for domain,indices in zip(domains,active)]
        rounds.append(changes)


def frontier(rows,keep_domains=False, pair_capacity=True, propagate=True):
    deficits = [[7 if u==v else 2-((rows[u]>>v)&1)-SHARED[u][v]-(rows[u]&rows[v]).bit_count()
                 for v in range(24)] for u in range(24)]
    assert all(min(row)>=0 for row in deficits)
    letter_deficits = [[2-int(l in LABELS[u])-int((l^1) in LABELS[u])-
                       (rows[u]&LETTER_MASKS[l]).bit_count() for l in range(14)] for u in range(24)]
    assert all(min(row)>=0 for row in letter_deficits)
    domains = [];all_rejections = []
    for qi,q in enumerate(OUTSIDE):
        good = [];rejected = Counter()
        allowed = [all(letter_deficits[v][l]>0 for l in q) for v in range(24)]
        shared_mask = LETTER_MASKS[q[0]]|LETTER_MASKS[q[1]]
        for profile in profiles(q):
            if any(not allowed[v] for v in profile):
                rejected['known_vertex_letter_quota']+=1;continue
            if any(not deficits[u][v] for u,v in combinations(profile,2)):
                rejected['known_pair_saturated']+=1;continue
            if len(profile)==2:
                a,b=profile
                if ((rows[a]&rows[b]&shared_mask) or
                    (((1<<a)|(1<<b))&shared_mask and ((rows[a]>>b)&1))):
                    rejected['new_to_known_C2']+=1;continue
            else:
                mask=sum(1<<v for v in profile)
                if any((rows[v]&mask).bit_count()>2-int(v in profile)-len(set(q)&set(LABELS[v]))
                       for v in range(24)):
                    rejected['new_to_known_C2']+=1;continue
                if any((mask&LETTER_MASKS[l]).bit_count()>2-int(l in q)-int((l^1) in q)
                       for l in range(14)):
                    rejected['new_vertex_letter_quota']+=1;continue
            good.append(profile)
        assert len(good)+sum(rejected.values())==len(profiles(q))
        domains.append(good);all_rejections.append(dict(rejected))
        if not good:
            return {'status':'EXCLUDED_EMPTY_VERTEX_DOMAIN','outside_index':qi,
                    'outside_letters':q,'total_profiles':len(profiles(q)),
                    'rejected_by':dict(rejected),'earlier_domain_sizes':[len(d) for d in domains[:-1]]}
    if pair_capacity:
        minimum=[0]*576;maximum=[0]*576
        for domain in domains:
            union=0;intersection=(1<<576)-1
            for profile in domain:
                features=profile_features(profile);union|=features;intersection&=features
            for mask,counts in ((union,maximum),(intersection,minimum)):
                while mask:
                    bit=mask&-mask;counts[bit.bit_length()-1]+=1;mask^=bit
        failures=[{'known_vertices':[u,v],'demand':deficits[u][v],
                   'minimum':minimum[24*u+v],'maximum':maximum[24*u+v]}
                  for u in range(24) for v in range(u,24)
                  if not minimum[24*u+v]<=deficits[u][v]<=maximum[24*u+v]]
        if failures:
            failures.sort(key=lambda c:(c['maximum']!=0,c['known_vertices']))
            return {'status':'EXCLUDED_PROFILE_CAPACITY',**failures[0],
                    'failed_pairs':len(failures),'domain_sizes':[len(d) for d in domains]}
    propagation=None
    if propagate:
        propagation,reduced=propagate_profiles(domains,deficits,letter_deficits)
        if propagation['status'].startswith('EXCLUDED_'):return propagation
        domains=reduced
    result={'status':'PASSES_PROFILE_PROPAGATION' if propagate else
            ('PASSES_SINGLE_VERTEX_AND_PAIR_CAPACITY' if pair_capacity else 'PASSES_SINGLE_VERTEX_DOMAINS'),
            'domain_sizes':[len(d) for d in domains]}
    if propagation:result['propagation']=propagation
    if keep_domains:
        result.update(domains=domains,residual_gram=deficits,letter_deficits=letter_deficits)
    return result


def solve(core,boundary,attachments,exact_profiles=False):
    counts=Counter();certificates=[]
    for attached in attachments.for_boundary(boundary):
        rows=materialize(core,boundary,attached);counts['valid_partial24']+=1
        certificate=frontier(rows)
        if certificate['status'].startswith('EXCLUDED_'):
            counts['frontier_obstructions']+=1
            certificates.append({'attachments':attached,'certificate':certificate})
            continue
        if exact_profiles:
            from root_component_shared_k3_profile_sat import select_profiles
            exact,cnf,proof=select_profiles(frontier(rows,True))
            counts['exact_profile_selections']+=1
            if exact['status']=='EXCLUDED_PROFILE_SELECTION_UNSAT':
                counts['exact_profile_unsat']+=1
                certificates.append({'attachments':attached,'certificate':exact,'rup_proof':proof})
                continue
            return {'status':exact['status'],'counts':dict(counts),
                    'witness':{'attachments':attached,'rows':rows,'selection':exact,
                               'frontier':frontier(rows,True)},'is_complete_graph':False}
        return {'status':'FEASIBLE_PARTIAL24_FRONTIER','counts':dict(counts),
                'witness':{'attachments':attached,'rows':rows,'frontier':frontier(rows,True)},
                'is_complete_graph':False}
    return {'status':'EXCLUDED_BY_FACTOR_JOIN_AND_FRONTIER','counts':dict(counts),
            'frontier_certificates':certificates,'is_complete_graph':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--boundaries',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--max-boundaries',type=int,default=0)
    parser.add_argument('--start',type=int,default=0)
    parser.add_argument('--exact-profiles',action='store_true')
    args=parser.parse_args();assert not args.output.exists()
    resources=limit_research_process(1);start=time.process_time()
    source=json.loads(gzip.decompress(args.boundaries.read_bytes()))
    assert source['status']=='COMPLETE_20_VERTEX_COVER'
    core=source['core'];attachments=Attachments(core)
    out={'scope':__doc__,'source':str(args.boundaries),
         'source_sha256':hashlib.sha256(args.boundaries.read_bytes()).hexdigest(),
         'core_index':source['core_index'],'resources':resources,'cases':[],
         'total_boundaries':source['boundary_count'],'whole_family_excluded':False,
         'exact_profiles':args.exact_profiles,
         'requested_start':args.start,'requested_max_boundaries':args.max_boundaries,
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'inclusion_filter_sha256':hashlib.sha256(Path(__file__).with_name(
             'root_component_profile_inclusion.py').read_bytes()).hexdigest(),
         'profile_solver_sha256':hashlib.sha256(Path(__file__).with_name(
             'root_component_shared_k3_profile_sat.py').read_bytes()).hexdigest() if args.exact_profiles else None}
    for bi,hex_state in enumerate(source['boundaries_hex']):
        if bi<args.start:continue
        if args.max_boundaries and len(out['cases'])>=args.max_boundaries:break
        boundary=tuple(bytes.fromhex(hex_state))
        result=solve(core,boundary,attachments,exact_profiles=args.exact_profiles)
        out['cases'].append({'boundary_index':bi,'boundary_hex':hex_state,'result':result})
        excluded=result['status'].startswith('EXCLUDED_')
        if len(out['cases'])%100==0 or not excluded:
            out['cpu_seconds']=time.process_time()-start
            write_result(args.output,out)
            print(json.dumps({'core':source['core_index'],'processed':len(out['cases']),
                'boundary_index':bi,'status':result['status'],'cpu_seconds':out['cpu_seconds']}),flush=True)
        if not excluded:break
    out['cpu_seconds']=time.process_time()-start
    out['full_core_coverage']=args.start==0 and len(out['cases'])==source['boundary_count']
    write_result(args.output,out)
    print(json.dumps({'processed':len(out['cases']),'statuses':dict(Counter(r['result']['status'] for r in out['cases'])),
                      'cpu_seconds':out['cpu_seconds'],'full_core_coverage':out['full_core_coverage']}))


if __name__=='__main__':main()
