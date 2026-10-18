"""Explain a touching-core obstruction as forbidden bijections to a grid.

Input: complete eight-word candidates extracted from the finite join.
For each compatible core, produce a four-row Hall witness when possible,
or an explicit violated C2 inequality for each of the 24 permutations.
This diagnoses the supplied row candidates; it does not certify that
their generating search or the family coverage was complete.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from root_component_touching_grid_join import mapped_cores,layout,LABELS,SHARED,PERMS,square
from root_component_resources import atomic_json_write,limit_research_process


def diagnose(candidate,k,centre,side):
    _,_,vertices,opposite=layout(centre)
    q=opposite[side];ids=candidate['grid_ids']
    grid_ids=ids[q] if q in ids else ids[str(q)]
    gw=[tuple(PERMS[grid_ids[b]][j] for b in range(3)) for j in range(4)]
    words=candidate['words'];domains=[];forbidden={}
    for i in range(4):
        u=4*side+i;domain=[]
        for t in range(4):
            reason=None;gv=8+4*q+t
            for l in range(8):
                actual=sum(k[u][v] for v in range(8) if l in LABELS[vertices[v]])+int(l in LABELS[gv])
                bound=2-int(l in LABELS[vertices[u]])-int((l^1) in LABELS[vertices[u]])
                if actual>bound:
                    reason={'kind':'letter_quota','letter':l,'actual':actual,'bound':bound};break
            for j in range(4):
                actual=sum(a==b for a,b in zip(words[u],gw[j]))+square(t,j)
                bound=2-int(t==j)
                if reason is None and actual>bound:
                    reason={'kind':'nongrid_grid_lower_bound','grid_corner':j,'actual':actual,'bound':bound}
            for b in range(3):
                for j in range(4):
                    actual=sum(k[u][v] for v in range(8) if words[v][b]==j)
                    actual+=square(words[u][b],j)+int(gw[t][b]==j)
                    bound=2-int(words[u][b]==j)
                    if reason is None and actual>bound:
                        reason={'kind':'nongrid_Y_C2','Y_grid':b,'Y_corner':j,'actual':actual,'bound':bound}
                    actual=sum(square(t,s) for s in range(4) if gw[s][b]==j)
                    actual+=square(gw[t][b],j)+int(words[u][b]==j)
                    bound=2-int(gw[t][b]==j)
                    if reason is None and actual>bound:
                        reason={'kind':'grid_Y_C2','Y_grid':b,'Y_corner':j,'actual':actual,'bound':bound}
            if reason is None:domain.append(t)
            else:forbidden[f'{i}-{t}']=reason
        domains.append(domain)
    for size in range(1,5):
        for rows in combinations(range(4),size):
            images=sorted({j for i in rows for j in domains[i]})
            if len(images)<size:
                return {'status':'EXCLUDED_HALL','side':side,'grid_rectangle_index':q,
                        'domains':domains,'hall_rows':rows,'hall_images':images,
                        'forbidden_images':forbidden}
    rejected=[];survivors=[]
    for pi,p in enumerate(PERMS):
        if any(p[i] not in domains[i] for i in range(4)):
            i=next(i for i in range(4) if p[i] not in domains[i])
            rejected.append({'permutation_index':pi,'forbidden_image':[i,p[i]]});continue
        inverse=[4*side+p.index(j) for j in range(4)];reason=None
        for u in range(8):
            for j in range(4):
                actual=sum(a==b for a,b in zip(words[u],gw[j]))+k[u][inverse[j]]
                if u//4==side:actual+=square(p[u%4],j)
                bound=2-int(u//4==side and p[u%4]==j)-SHARED[vertices[u]][8+4*q+j]
                if actual>bound:
                    reason={'permutation_index':pi,'nongrid_vertex':u,'grid_corner':j,
                            'actual':actual,'bound':bound};break
            if reason:break
        if reason:rejected.append(reason)
        else:survivors.append(pi)
    return {'status':'EXCLUDED_ALL_BIJECTIONS' if not survivors else 'PASSES_BIJECTIONS',
            'side':side,'domains':domains,'forbidden_images':forbidden,
            'rejected_permutations':rejected,'surviving_permutations':survivors}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--traces',type=Path,required=True)
    p.add_argument('--pair-cores',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();assert not args.output.exists();limit_research_process(1)
    source=json.loads(args.traces.read_text(encoding='utf8'))
    records=json.loads(args.pair_cores.read_text(encoding='utf8'))
    centre=source['centre'];cores=mapped_cores(records,centre)
    result=[];counts=Counter()
    for ri,candidate in enumerate(source['row_candidates']):
        for ki in candidate['compatible_cores']:
            certs=[diagnose(candidate,cores[ki][0],centre,side) for side in range(2)]
            obstruction=next((c for c in certs if c['status'].startswith('EXCLUDED_')),None)
            status=obstruction['status'] if obstruction else 'PASSES_BOTH_BIJECTIONS'
            counts[status]+=1
            result.append({'row_candidate':ri,'core_index':ki,'status':status,
                           'obstruction':obstruction,'both_sides':certs})
    out={'scope':__doc__,'input':str(args.traces),'row_candidate_count':len(source['row_candidates']),
         'counts':dict(counts),'certificates':result,'global_Conway_exclusion':False}
    atomic_json_write(args.output,out)
    print(json.dumps({'rows':out['row_candidate_count'],'core_word_pairs':len(result),'counts':dict(counts)}))


if __name__=='__main__':main()
