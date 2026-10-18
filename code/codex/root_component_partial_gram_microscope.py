"""Find an obstructed principal Gram block, without fixing the full Gram.

For any principal block S of R, a genuine signature restricted to S lies
in im(S) and has h^t S^+ h <= 5/2. Four signatures in rectangle q must
sum to S[:,q] when q is among the selected coordinates. All other Gram
entries remain free. Complete component row catalogues are accepted as
input, not regenerated; the finite filtering uses exact integers only.
"""

import argparse
import hashlib
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import random
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from root_component_resources import atomic_json_write, limit_research_process
from root_component_signature_saturation import saturate


def inspect_block(R, columns, own, candidates):
    """candidates are whole, component-compatible rows in nongrid order."""
    import sympy as sp
    columns = tuple(columns)
    assert own in columns
    S = R.extract(columns, columns)
    anchors = list(S.rref()[1])
    rank = len(anchors)
    if rank:
        T = S.extract(anchors, anchors)
        denominator = int(T.det())
        assert denominator > 0
        adj = (T.inv(method='DM') * denominator).applyfunc(int)
        lift = S[:, anchors] * adj
        ai = [[int(x) for x in row] for row in adj.tolist()]
        li = [[int(x) for x in row] for row in lift.tolist()]
    kept = set()
    for row in candidates:
        h = tuple(row[j] for j in columns)
        if not rank:
            if not any(h):
                kept.add(h)
            continue
        z = [h[i] for i in anchors]
        if any(denominator * h[i] != sum(a*b for a,b in zip(li[i],z)) for i in range(len(columns))):
            continue
        energy = sum(z[i]*ai[i][j]*z[j] for i in range(rank) for j in range(rank))
        if 2 * energy <= 5 * denominator:
            kept.add(h)
    domain = sorted(kept)
    target = [int(x) for x in S[:,columns.index(own)]]
    saturation = saturate(domain, target)
    reduced = saturation['signatures']
    pairs = {}
    for i,j in combinations_with_replacement(range(len(reduced)),2):
        key = tuple(x+y for x,y in zip(reduced[i],reduced[j]))
        pairs.setdefault(key,(i,j))
    witness = None
    for key, first in pairs.items():
        second = pairs.get(tuple(x-y for x,y in zip(target,key)))
        if second is not None:
            witness = list(first+second)
            break
    return {'columns':list(columns), 'principal_block':[[int(x) for x in row] for row in S.tolist()],
            'rank':rank,'original_row_count':len(candidates),'projected_domain':domain,
            'target':target,'saturation':saturation,'four_sum':witness,
            'status':'EXCLUDED_PARTIAL_BLOCK' if witness is None else 'PASSES'}


def main():
    import sympy as sp
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--gram-result',type=Path,required=True)
    p.add_argument('--catalogue',type=Path,required=True)
    p.add_argument('--rectangle',type=int,nargs=2,required=True)
    p.add_argument('--restarts',type=int,default=12)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();assert not a.output.exists()
    resources=limit_research_process(1)
    record=json.loads(a.gram_result.read_text(encoding='utf-8-sig'))
    catalogue_record=json.loads(a.catalogue.read_text(encoding='utf-8-sig'))
    catalogue=catalogue_record['catalogue']
    catalogue_template=json.loads(Path(catalogue_record['source_bundle']).read_text(encoding='utf-8-sig'))['template']
    gram_template=json.loads((Path(record['source'])/'partition.json').read_text(encoding='utf-8-sig'))['template']
    assert catalogue_template==gram_template,'Catalogue and Gram must belong to the same component template.'
    assert catalogue['status']=='ROW_CATALOGUE_COMPLETE'
    rectangles=list(combinations(range(7),2));q=tuple(a.rectangle)
    edges=[tuple(e) for e in record['edges']];own=edges.index(q)
    types=next(t for t in catalogue['row_types'] if tuple(t['rectangle'])==q)
    positions=[rectangles.index(e) for e in edges]
    candidates=sorted({tuple(3*int(q==e)+1-len(set(q)&set(e))-z[j]
                             for e,j in zip(edges,positions)) for z in types['states']})
    R=sp.Matrix(record['gram']);cache={}
    from root_component_gram_enumeration import integer_psd
    assert R==R.T and all(x.q==1 for x in R) and integer_psd(R.tolist())
    def test(columns):
        key=tuple(sorted(columns))
        if key not in cache:cache[key]=inspect_block(R,key,own,candidates)
        return cache[key]
    start=time.process_time();all_columns=list(range(len(edges)))
    original=test(all_columns)
    assert original['status']=='EXCLUDED_PARTIAL_BLOCK','The supplied rectangle is not obstructed by this test.'
    rng=random.Random(731);minima=[]
    for restart in range(a.restarts):
        columns=all_columns.copy();order=[i for i in columns if i!=own]
        if restart:rng.shuffle(order)
        for i in order:
            trial=[j for j in columns if j!=i]
            if test(trial)['status']=='EXCLUDED_PARTIAL_BLOCK':columns=trial
        minima.append(columns)
    best=min(minima,key=lambda c:(test(c)['rank'],len(c),tuple(c)))
    cert=test(best)
    cert['coordinate_rectangles']=[list(edges[i]) for i in best]
    result={'scope':__doc__,'source_gram':str(a.gram_result),'source_catalogue':str(a.catalogue),
            'source_gram_sha256':hashlib.sha256(a.gram_result.read_bytes()).hexdigest(),
            'source_catalogue_sha256':hashlib.sha256(a.catalogue.read_bytes()).hexdigest(),
            'template':catalogue_template,
            'rectangle':list(q),'nongrid_edges':[list(e) for e in edges],
            'full_gram_rank':R.rank(),'block_has_smaller_rank':cert['rank']<R.rank(),
            'best_block':cert,'tested_blocks':len(cache),'greedy_minima':minima,
            'globally_minimum_block_proved':False,'cpu_seconds':time.process_time()-start,
            'whole_template_excluded':False,'global_conway_exclusion':False,'resources':resources}
    atomic_json_write(a.output,result,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('best_block','greedy_minima','nongrid_edges')}),flush=True)
    print(json.dumps({k:v for k,v in cert.items() if k not in ('projected_domain','saturation')}),flush=True)


if __name__=='__main__':main()
