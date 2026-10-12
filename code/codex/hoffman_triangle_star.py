"""Coexistence of a central row with the ten transported neighbour rows.

Four central neighbours are paired with C-points. The six others form three
triangles through the centre. Transported rows in one such triangle share
its two other vertices; rows from different triangles intersect at most once.
All statuses describe a necessary local-star relaxation, never a full SRG.
"""
from collections import defaultdict
from itertools import combinations
import time
from hoffman_resolution_filter import resolution


def bits(mask):
    while mask:
        bit=mask&-mask;mask-=bit
        yield bit.bit_length()-1


def triangle_star(rows,quotas,one_mask,known_overlap,max_total_nodes=1000000,
                  overlap_bounds=False,seconds=None,progress=None,support=None,
                  labelled=False,missing=None):
    count=trials=nodes=support_prunes=0;had_unknown=False
    start=time.monotonic()
    for central in rows:
        count+=1
        if seconds is not None and time.monotonic()-start>seconds:
            return dict(status='UNKNOWN',reason='TIME_LIMIT',centres_tested=count-1,
                        matchings_tested=trials,nodes=nodes)
        if progress is not None and count%50==0:
            progress(dict(centres_tested=count-1,matchings_tested=trials,nodes=nodes,
                          support_prunes=support_prunes,seconds=time.monotonic()-start))
        live_support=support.masks[central] if support is not None else None
        if support is not None and not support.possible(live_support):
            support_prunes+=1;continue
        singles=list(bits(central&one_mask));zeros=list(bits(central&~one_mask))
        assert len(singles)==4 and len(zeros)==6
        bins=defaultdict(list)
        for row in rows:
            pat=central&row
            if pat.bit_count()==1 and pat&one_mask or pat.bit_count()==2 and not pat&one_mask:
                bins[pat].append(row)
        if any(not bins[1<<j] for j in singles):continue
        allowed={}
        for j,k in combinations(zeros,2):
            if known_overlap[j][k]:continue
            pat=(1<<j)|(1<<k)
            cc=bins[pat]
            if any((a&b).bit_count()==2 for a,b in combinations(cc,2)):
                allowed[j,k]=pat

        def matchings(left):
            if not left:
                yield []
                return
            j=left[0]
            for k in left[1:]:
                pair=tuple(sorted((j,k)))
                if pair in allowed:
                    for rest in matchings([v for v in left[1:] if v!=k]):
                        yield [pair]+rest

        for matching in matchings(zeros):
            patterns=[1<<j for j in singles]+[allowed[pair] for pair in matching]
            candidates=[row for pat in patterns for row in bins[pat]]
            labels=[pat for pat in patterns for row in bins[pat]]
            # Different central triangles are nonadjacent and already have
            # the central vertex as a common neighbour. Known C-neighbours
            # further reduce the permitted intersection of transported rows.
            bounds=None
            if overlap_bounds:
                bounds={(a,b): (2 if a==b else
                         1-min(known_overlap[j][k] for j in bits(a) for k in bits(b)))
                        for a in patterns for b in patterns}
            trials+=1
            if labelled:
                from hoffman_centred_resolution import centred_resolution
                centres=singles+[j for pair in matching for j in pair]
                pats=[1<<j for j in singles]+[allowed[pair] for pair in matching for _ in pair]
                result=centred_resolution(centres,[bins[p] for p in pats],pats,quotas,
                    known_overlap,missing,max_nodes=max(1,min(50000,max_total_nodes-nodes)),
                    support=support,support_start=live_support)
            else:
                result=resolution(candidates,quotas,max_nodes=max(1,min(50000,max_total_nodes-nodes)),
                                  patterns=labels,pattern_bounds=bounds,
                                  support=support,support_start=live_support)
            nodes+=result['nodes']
            support_prunes+=result['support_prunes']
            if result['status']=='SAT_RESOLUTION_ONLY':
                return dict(status='FEASIBLE_TRIANGLE_STAR_NOT_SRG',central=str(central),
                            transported=([str(r) for r in result['witness_rows']] if labelled else
                                         [str(candidates[k]) for k in result['witness']]),
                            assigned_centres=result.get('centres'),
                            triangle_pairs=matching,centres_tested=count,matchings_tested=trials,
                            nodes=nodes,support_prunes=support_prunes)
            if result['status']=='UNKNOWN':had_unknown=True
            if nodes>=max_total_nodes:
                return dict(status='UNKNOWN',centres_tested=count,matchings_tested=trials,
                            nodes=nodes,support_prunes=support_prunes)
    return dict(status='UNKNOWN' if had_unknown else 'UNSAT_TRIANGLE_STAR',
                centres_tested=count,matchings_tested=trials,nodes=nodes,support_prunes=support_prunes)


def fixture_check():
    # A genuine feasible instance of this relaxation, not a claimed SRG.
    # Private overlap-one columns and edges of this degree-(6^4,4^6)
    # graph give the ten transported rows. Forbidden pairs are the triangles.
    edges=[(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(1,3),(1,5),
           (1,6),(1,7),(1,8),(1,9),(2,4),(2,5),(2,6),(2,7),
           (2,8),(2,9),(3,4),(3,5),(3,6),(3,7),(3,9),(4,8)]
    rows=[];next_one=11
    for a in range(10):
        central={a+1} if a<4 else {5+2*((a-4)//2),6+2*((a-4)//2)}
        extra=set(range(next_one,next_one+(3 if a<4 else 4)))
        next_one+=len(extra)
        zeros={47+t for t,e in enumerate(edges) if a in e}
        rows.append(sum(1<<j for j in central|extra|zeros))
    rows=[sum(1<<j for j in range(1,11))]+rows
    one=sum(1<<j for j in list(range(1,5))+list(range(11,47)))
    quota=[0]+[1]*4+[2]*6+[1]*36+[2]*24+[0]*6
    ov=[[0]*77 for _ in range(77)]
    positive=triangle_star(rows,quota,one,ov)
    negative=triangle_star(rows[:-1],quota,one,ov)
    labelled_positive=triangle_star(rows,quota,one,ov,labelled=True,missing=[1]*77)
    labelled_negative=triangle_star(rows[:-1],quota,one,ov,labelled=True,missing=[1]*77)
    assert positive['status']=='FEASIBLE_TRIANGLE_STAR_NOT_SRG'
    assert negative['status']=='UNSAT_TRIANGLE_STAR'
    assert labelled_positive['status']=='FEASIBLE_TRIANGLE_STAR_NOT_SRG'
    assert labelled_negative['status']=='UNSAT_TRIANGLE_STAR'
    witness=list(map(int,positive['transported']))
    assert len(set(witness))==10
    assert [sum((w>>j)&1 for w in witness) for j in range(77)]==quota
    return dict(positive=positive['status'],negative=negative['status'],
                labelled_positive=labelled_positive['status'],labelled_negative=labelled_negative['status'])


def main():
    import argparse,json,time
    from types import SimpleNamespace
    from hoffman_coexistence_extensions import SOURCE,OUT
    from hoffman_cover_capacity import projected_covers
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',default='3,4,5,6,7')
    ap.add_argument('--root',type=int,default=10)
    ap.add_argument('--max-nodes',type=int,default=2000000)
    ap.add_argument('--overlap-bounds',action='store_true')
    ap.add_argument('--seconds',type=float,default=None)
    ap.add_argument('--point-support',action='store_true')
    ap.add_argument('--labelled',action='store_true')
    args=ap.parse_args()
    fixture=fixture_check()
    item=next(x for x in json.loads(SOURCE.read_text())['items'] if x['design']['key'].startswith(args.prefix))
    bs=list(map(set,item['design']['blocks']))
    free=list(map(int,args.free.split(',')));fixed=set(range(22))-set(free)
    assert bs[args.root]<=fixed
    folder=OUT/('triangle_star_'+args.prefix+'_'+args.free.replace(',','-')+
                ('_overlap' if args.overlap_bounds else '')+
                ('_points' if args.point_support else '')+
                ('_labelled' if args.labelled else '')+
                ('_root'+str(args.root) if args.root!=10 else ''))
    folder.mkdir(parents=True,exist_ok=True)
    covers,stats=projected_covers(SimpleNamespace(fixed=fixed,blocks=bs),args.root,folder/'projected')
    rows=[sum(1<<j for j in cover if j!=args.root) for cover in covers]
    quotas=[2-len(bs[args.root]&b) if i!=args.root else 0 for i,b in enumerate(bs)]
    one=sum(1<<i for i,b in enumerate(bs) if len(bs[args.root]&b)==1)
    ov=[[len(a&b&fixed) for b in bs] for a in bs]
    support=None
    if args.point_support:
        from hoffman_point_support import PointSupport
        from hoffman_missing_point_domains import enumerate_missing_points
        pointfolder=OUT/('point_domains_'+args.prefix+'_'+args.free.replace(',','-'))
        if (pointfolder/'point_domain.json').exists():
            pdata=json.loads((pointfolder/'point_domain.json').read_text())
        else:pdata=enumerate_missing_points(item['design']['blocks'],free,pointfolder)
        assert pdata['complete'] and pdata['free']==sorted(free)
        support=PointSupport(pdata['rows'],rows,ov,[4-len(b&fixed) for b in bs],len(free))
        print('POINT_SUPPORT',len(pdata['rows']),'rows',len(rows),'covers',flush=True)
    start=time.monotonic()
    def progress(rec):
        (folder/'progress.json').write_text(json.dumps(rec,indent=2))
        print('PROGRESS',rec,flush=True)
    result=triangle_star(rows,quotas,one,ov,args.max_nodes,
                         overlap_bounds=args.overlap_bounds,seconds=args.seconds,progress=progress,support=support,
                         labelled=args.labelled,missing=[4-len(b&fixed) for b in bs])
    if support is not None and 'central' in result:
        pool=support.masks[int(result['central'])]
        for row in result['transported']:pool &= support.masks[int(row)]
        result['point_support']=support.describe(pool)
    result.update(source=item['design']['key'],source_blocks=item['design']['blocks'],
                  free=free,root=args.root,candidate_rows=len(rows),projection_statistics=stats,
                  arguments=vars(args),seconds=time.monotonic()-start,fixture_check=fixture,
                  scope='All C1 Hoffman completions of the retained incidence template; necessary triangle-star coexistence')
    (folder/'result.json').write_text(json.dumps(result,indent=2))
    print({k:v for k,v in result.items() if k not in ('source_blocks',)},flush=True)


if __name__=='__main__':main()
