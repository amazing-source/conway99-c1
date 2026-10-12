"""Replay each new partial-boundary exclusion directly from its incidences.

This checks the arithmetic of certificates, not by rerunning the searcher's
incremental overlap updates. Coverage also relies on the exhausted finite
search and the exhausted two input domain enumerations documented in the note.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

from hoffman_coexistence_extensions import OUT


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',default='3,4,5,6,7')
    ap.add_argument('--roots')
    ap.add_argument('--column-orbits',action='store_true')
    args=ap.parse_args()
    suffix=args.prefix+'_'+args.free.replace(',','-')
    folder=OUT/('point_prune_'+suffix+('_orbits' if args.column_orbits else '')+
                ('_roots'+'-'.join(map(str,sorted(set(map(int,args.roots.split(',')))))) if args.roots else ''))
    record=json.loads((folder/'result.json').read_text())
    source=json.loads((OUT/('point_domains_'+suffix)/'point_domain.json').read_text())
    assert source['complete'] and record['exhaustive']
    fixed=set(source['fixed']);blocks=list(map(set,record['source_blocks']))
    point_masks=[sum(1<<j for j in row) for row in source['rows']]
    covers=list(map(int,record['projected_cover_masks']))
    root=record['arguments']['root']
    assert blocks[root] <= fixed
    ov=[[len(a&b&fixed) for b in blocks] for a in blocks]
    by_col=[sum(1<<a for a,c in enumerate(covers) if c>>j&1) for j in range(77)]
    single={}
    start=time.monotonic()
    for p in {p for cert in record['cover_prunes'] for p in cert['selected']}:
        valid=0
        for a,c in enumerate(covers):
            common=c&point_masks[p]
            if common.bit_count()!=2:continue
            bit=common&-common
            i=bit.bit_length()-1;j=(common^bit).bit_length()-1
            if ov[i][j]==0:valid |= 1<<a
        single[p]=valid
    for cert in record['cover_prunes']:
        valid=(1<<len(covers))-1
        for p in cert['selected']:valid &= single[p]
        for p,q in combinations(cert['selected'],2):
            common=point_masks[p]&point_masks[q]
            assert common.bit_count()==2
            bit=common&-common
            i=bit.bit_length()-1;j=(common^bit).bit_length()-1
            valid &= ~(by_col[i]&by_col[j])
        r=cert.get('root',root)
        assert blocks[r] <= fixed
        valid &= by_col[r]
        assert valid.bit_count()==cert['covers']
        if cert['kind']=='less_than_eleven':assert valid.bit_count()<11
        else:
            j=cert['other'];available=(valid&by_col[j]).bit_count()
            required=2-len(blocks[r]&blocks[j])
            assert available==cert['available']<required==cert['required']
    output=dict(status='ALL_PRUNE_CERTIFICATES_REPLAYED',count=len(record['cover_prunes']),
                depths=dict(Counter(len(p['selected']) for p in record['cover_prunes'])),
                elapsed_seconds=time.monotonic()-start,
                coverage='Exhausted point-domain search; certificate arithmetic replayed separately')
    (folder/'certificate_replay.json').write_text(json.dumps(output,indent=2))
    print(output)


if __name__=='__main__':main()
