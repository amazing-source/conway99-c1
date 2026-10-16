"""Construct new outer-root geometries of an accepted 44-vertex graph.

Central star memberships are fixed, but the ten outer roots are rebuilt
as compatible transversals of their four groups of ten vertices. This
allows new Gram spectra and kernels, unlike an orthogonal conjugation.
"""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from hmatch_cycle_reflections import B, H, INDEX, LABELS, load_graph, new_candidate_checks
from hmatch_pure_switch_kernel_gate import integer_kernel
from hmatch_broken_mate_family import rank_at_least
from odd9_endpoint_mate_family import exact_psd


def spectral_annihilator(gamma):
    """All admissible root columns annihilate these intrinsic eigenspaces.

    For Gamma q=3q and 1^tq=0, T PSD gives
    0<=8q^tTq=-(Bq)^t(3I+M)(Bq)<=0, so Bq=0.
    For Gamma q=-4q, U PSD similarly gives Bq=0 (and 1^tq=0).
    This holds for every new root geometry and every mate involution M.
    """
    lower=integer_kernel(np.vstack([gamma-3*np.eye(44,dtype=int),np.ones((1,44),dtype=int)]))
    upper=integer_kernel(gamma+4*np.eye(44,dtype=int))
    return np.hstack([lower,upper]),dict(eigen3_zero_sum=lower.shape[1],eigen_minus4=upper.shape[1])


def transversals(gamma):
    groups=[[INDEX[(c,y)] for y in range(4,14)] for c in range(4)]
    # Adding a shared outer root is possible exactly when this C2 cap holds.
    compatible=(gamma@gamma+gamma <= 1)
    annihilator,dimensions=spectral_annihilator(gamma)
    filtered=0
    columns=[]
    for vertices in product(*groups):
        if not all(compatible[i,j] for i,j in combinations(vertices,2)):
            continue
        if np.any(annihilator[list(vertices)].sum(axis=0)):
            filtered+=1
            continue
        counts=gamma[:,vertices].sum(axis=1)
        if np.any(counts>2) or np.any(counts[list(vertices)]>1):
            continue
        pure_break=False
        for central in (0,2):
            for overlap in range(4):
                label=tuple(sorted((central,overlap)))
                if label not in INDEX:
                    continue
                i=INDEX[label]
                if gamma[vertices[central],i] != gamma[vertices[central+1],H[i]]:
                    pure_break=True
        columns.append(dict(vertices=tuple(vertices),counts=counts,
                            mask=sum(1<<i for i in vertices),overlap_break=pure_break))
    return groups,columns,dict(**dimensions,spectrally_rejected=filtered)


def covers(groups,columns,deadline):
    outer=sorted(i for group in groups for i in group)
    full=sum(1<<i for i in outer)
    containing={v:[i for i,c in enumerate(columns) if v in c['vertices']] for v in outer}
    timed_out=False
    def visit(used,chosen):
        nonlocal timed_out
        if time.monotonic()>=deadline:
            timed_out=True
            yield None
            return
        if used==full:
            yield tuple(sorted(chosen,key=lambda i:columns[i]['vertices'][0]))
            return
        available={v:[i for i in containing[v] if not(columns[i]['mask']&used)]
                   for v in outer if not((used>>v)&1)}
        v=min(available,key=lambda v:len(available[v]))
        for i in available[v]:
            yield from visit(used|columns[i]['mask'],chosen+[i])
            if timed_out:
                return
    yield from visit(0,[])


def mate_choices(columns,selected):
    allowed={}
    for a,b in combinations(range(10),2):
        left,right=columns[selected[a]],columns[selected[b]]
        allowed[a,b]=(np.all(left['counts'][list(right['vertices'])]<=1)
                      and np.all(right['counts'][list(left['vertices'])]<=1))
    def visit(left):
        if not left:
            yield []
            return
        a=left[0]
        for b in left[1:]:
            if allowed[tuple(sorted((a,b)))]:
                for tail in visit([x for x in left if x not in (a,b)]):
                    yield [(a,b)]+tail
    yield from visit(list(range(10)))


def construct(gamma,groups,columns,deadline,output):
    statistics=Counter()
    hit=None
    complete=True
    last_print=time.monotonic()
    central_gram=B[:4].T@B[:4]
    central_mate=B[:4].T@B[[1,0,3,2]]
    for selected in covers(groups,columns,deadline):
        if selected is None or time.monotonic()>=deadline:
            complete=False
            break
        statistics['partitions']+=1
        broken=any(columns[i]['overlap_break'] for i in selected)
        if not broken:
            broken=any(gamma[columns[i]['vertices'][c],columns[j]['vertices'][c]]
                       !=gamma[columns[i]['vertices'][c+1],columns[j]['vertices'][c+1]]
                       for i,j in combinations(selected,2) for c in (0,2))
        if not broken:
            statistics['H_MATCH_INTACT_PARTITIONS']+=1
            continue
        incidence=np.zeros((10,44),dtype=np.int64)
        for a,i in enumerate(selected):
            incidence[a,list(columns[i]['vertices'])]=1
        gram=central_gram+incidence.T@incidence
        # Both matrices majorize an admissible T/U for EVERY outer M.
        lower_bound=24*np.eye(44,dtype=np.int64)-8*gamma-2*gram+2
        if not exact_psd(lower_bound)[0]:
            statistics['T_MAJORANT_NOT_PSD']+=1
            continue
        upper_bound=60*np.eye(44,dtype=np.int64)+15*gamma-3*gram-2
        if not exact_psd(upper_bound)[0]:
            statistics['U_MAJORANT_NOT_PSD']+=1
            continue
        statistics['PARTITIONS_PASS_MAJORANTS']+=1
        tbase=24*np.eye(44,dtype=np.int64)-8*gamma-3*gram-central_mate+2
        ubase=60*np.eye(44,dtype=np.int64)+15*gamma-4*gram+central_mate-2
        for pairs in mate_choices(columns,selected):
            if time.monotonic()>=deadline:
                complete=False
                break
            statistics['mate_assignments']+=1
            mate=list(range(10))
            for a,b in pairs:
                mate[a],mate[b]=b,a
            mate_gram=incidence.T@incidence[mate]
            t8=tbase-mate_gram
            if rank_at_least(t8)>=31:
                statistics['RANK_AT_LEAST_31_MOD101']+=1
                continue
            t_psd,rank_t,reason=exact_psd(t8)
            if not t_psd:
                statistics['T_NOT_PSD']+=1
                continue
            if rank_t>30:
                statistics['RANK_ABOVE_30_EXACT']+=1
                continue
            u_psd,rank_u,reason=exact_psd(ubase+mate_gram)
            if not u_psd:
                statistics['U_NOT_PSD']+=1
                continue
            relabelling=list(range(44))
            for number,(a,b) in enumerate(pairs):
                for root_index,column_index in [(4+2*number,a),(5+2*number,b)]:
                    for central,vertex in enumerate(columns[selected[column_index]]['vertices']):
                        relabelling[vertex]=INDEX[(central,root_index)]
            candidate=np.zeros((44,44),dtype=np.int64)
            candidate[np.ix_(relabelling,relabelling)]=gamma
            assert new_candidate_checks(candidate)=='H_MATCH_BROKEN'
            canonical_mate=B.T@B[[r ^ 1 for r in range(14)]]
            canonical_t8=24*np.eye(44,dtype=np.int64)-8*candidate-3*(B.T@B)-canonical_mate+2
            canonical_u15=60*np.eye(44,dtype=np.int64)+15*candidate-4*(B.T@B)+canonical_mate-2
            assert np.array_equal(canonical_t8[np.ix_(relabelling,relabelling)],t8)
            assert np.array_equal(canonical_u15[np.ix_(relabelling,relabelling)],ubase+mate_gram)
            hit=dict(labels=LABELS,edges=[[i,j] for i,j in combinations(range(44),2) if candidate[i,j]],
                new_root_columns=[list(columns[i]['vertices']) for i in selected],outer_mates=pairs,
                exact_certificates=dict(T_PSD=True,U_PSD=True,rank_T=rank_t,rank_U=rank_u),
                combinatorial_verdict='H_MATCH_BROKEN')
            target=Path(output).with_name(Path(output).stem+'_HIT.json')
            target.write_text(json.dumps(hit,indent=2)+'\n',encoding='utf-8')
            hit=str(target)
            break
        if hit or not complete:
            break
        if time.monotonic()-last_print>=5:
            print(json.dumps(dict(stage='SEARCH',statistics=dict(statistics))),flush=True)
            last_print=time.monotonic()
    return dict(statistics=dict(statistics),exhausted=complete and hit is None,hit=hit)


def run(source,name=None,output=None,seconds=30):
    started=time.monotonic()
    records=json.loads(Path(source).read_text(encoding='utf-8'))
    if 'labels' in records:
        records={Path(source).stem:records}
    if name is not None:
        records={name:records[name]}
    for record_name,record in records.items():
        gamma=load_graph(record)
        groups,columns,spectral=transversals(gamma)
        if output is not None:
            print(json.dumps(dict(stage='ROOT_COLUMNS',source=record_name,
                                  transversals=len(columns),spectral=spectral)),flush=True)
            result=construct(gamma,groups,columns,started+seconds,output)
            result.update(source_file=str(source),source=record_name,transversals=len(columns),
                          spectral=spectral,seconds=time.monotonic()-started,
                          scope='All transversal outer-root assignments on these fixed four central stars, with all compatible outer mates, subject to the reported time limit. Gram spectra and kernels are free. No assertion about other unlabelled Gamma or other central stars.')
            Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(result),flush=True)
            return result
        mates=0
        broken_pairs=0
        disjoint=0
        for left,right in combinations(columns,2):
            if left['mask']&right['mask']:
                continue
            disjoint+=1
            if any(gamma[left['vertices'][c],right['vertices'][c]] != gamma[left['vertices'][c+1],right['vertices'][c+1]] for c in (0,2)):
                broken_pairs+=1
            if np.all(left['counts'][list(right['vertices'])]<=1) and np.all(right['counts'][list(left['vertices'])]<=1):
                mates+=1
        print(json.dumps(dict(source=record_name,transversals=len(columns),
            spectral=spectral,
            overlap_breaks=sum(c['overlap_break'] for c in columns),
            disjoint_pairs=disjoint,broken_matching_pairs=broken_pairs,
            compatible_mate_pairs=mates,seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--name')
    parser.add_argument('--output')
    parser.add_argument('--seconds',type=float,default=30)
    args=parser.parse_args()
    run(args.source,args.name,args.output,args.seconds)
