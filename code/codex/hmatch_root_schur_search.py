"""Reconstruct outer-root geometries using exact Schur matrices of size10.

With central incidence C fixed, write T8=A0-W(3I+M)W^t and
U15=D0-W(4I-M)W^t. A0,D0 are PSD by the accepted producer certificates.
For candidate root columns W in both ranges, these are PSD iff
E_T=(3I-M)/8-W^t A0^+ W and E_U=(4I+M)/15-W^t D0^+ W are PSD.
Furthermore rank(T8)=rank(A0)-10+rank(E_T). Search partial exact covers
and partial mate matchings with these necessary and sufficient conditions.
The old kernel, new kernel, and Gram spectra are unrestricted.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parent))
from hmatch_cycle_reflections import B, H, INDEX, LABELS, load_graph, new_candidate_checks
from hmatch_new_root_geometry import transversals
from hmatch_broken_mate_family import rank_at_least
from odd9_endpoint_mate_family import exact_psd


def range_gram(base,columns):
    """Integer numerator of W^t base^+ W via an invertible principal block.

    PSD of base is inherited, not independently retested. The returned
    range tests are exact and are required for NEW incidence columns.
    """
    matrix=sp.Matrix(base.tolist())
    pivots=list(matrix.rref()[1])
    inverse=matrix.extract(pivots,pivots).inv()
    denominator=lcm(*(int(x.q) for x in inverse))
    inverse_num=np.array([[int(x*denominator) for x in row] for row in inverse.tolist()],dtype=object)
    w=np.zeros((len(columns),44),dtype=object)
    for j,c in enumerate(columns):
        w[j,list(c['vertices'])]=1
    restricted=w[:,pivots]
    image=base[:,pivots].astype(object)@inverse_num@restricted.T
    in_range=np.all(image==denominator*w.T,axis=0)
    gram=restricted@inverse_num@restricted.T
    return dict(rank=len(pivots),denominator=denominator,gram=gram,in_range=in_range)


def broken(gamma,columns,selected):
    overlap=[i for i,p in enumerate(LABELS) if max(p)<4]
    if any(gamma[i,j]!=gamma[H[i],H[j]] for i,j in combinations(overlap,2)):
        return True
    return (any(columns[i]['overlap_break'] for i in selected)
            or any(gamma[columns[i]['vertices'][c],columns[j]['vertices'][c]]
                   != gamma[columns[i]['vertices'][c+1],columns[j]['vertices'][c+1]]
                   for i,j in combinations(selected,2) for c in (0,2)))


def canonical_graph(gamma,columns,selected,partners):
    permutation=list(range(44))
    pairs=[(i,j) for i,j in enumerate(partners) if i<j]
    assert len(pairs)==5
    for number,(a,b) in enumerate(pairs):
        for root_index,column_index in [(4+2*number,a),(5+2*number,b)]:
            for central,vertex in enumerate(columns[selected[column_index]]['vertices']):
                permutation[vertex]=INDEX[(central,root_index)]
    candidate=np.zeros((44,44),dtype=np.int64)
    candidate[np.ix_(permutation,permutation)]=gamma
    return candidate,pairs


def materialize(source,report_file,output):
    """Save and check one newly reconstructed geometry, not the source form."""
    record=json.loads(Path(source).read_text(encoding='utf-8'))
    report=json.loads(Path(report_file).read_text(encoding='utf-8'))
    if 'labels' not in record:
        record=record[report['source']]
    control=report['first_admissible_intact_control']
    columns=[dict(vertices=tuple(v)) for v in control['root_columns']]
    partners=[-1]*10
    for a,b in control['outer_mates']:
        partners[a],partners[b]=b,a
    candidate,_=canonical_graph(load_graph(record),columns,list(range(10)),partners)
    verdict=new_candidate_checks(candidate)
    assert verdict=='H_MATCH_INTACT'
    mate_gram=B.T@B[[r ^ 1 for r in range(14)]]
    t8=24*np.eye(44,dtype=np.int64)-8*candidate-3*(B.T@B)-mate_gram+2
    u15=60*np.eye(44,dtype=np.int64)+15*candidate-4*(B.T@B)+mate_gram-2
    tp,tr,_=exact_psd(t8)
    up,ur,_=exact_psd(u15)
    assert tp and up and tr==control['rank_T'] and ur==control['rank_U']
    artifact=dict(source_file=str(source),construction_report=str(report_file),labels=LABELS,
        edges=[[i,j] for i,j in combinations(range(44),2) if candidate[i,j]],
        exact_certificates=dict(T_PSD=True,U_PSD=True,rank_T=tr,nullity_T=44-tr,rank_U=ur),
        combinatorial_verdict=verdict,root_geometry=control,
        scope='New root incidence and Gram forms; unlabelled 44-vertex adjacency is unchanged. This is a local block, not a complete SRG.')
    Path(output).write_text(json.dumps(artifact,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(file=str(output),certificates=artifact['exact_certificates'],verdict=verdict)),flush=True)
    return artifact


def run(source,output,name,seconds,extension_probe=False):
    started=time.monotonic()
    records=json.loads(Path(source).read_text(encoding='utf-8'))
    if 'labels' in records:
        record_name,record=Path(source).stem,records
    else:
        if name is None:
            raise ValueError('--name required for a multi-record source')
        record_name,record=name,records[name]
    gamma=load_graph(record)
    groups,columns,spectral=transversals(gamma)
    c=B[:4]
    cg=c.T@c
    cm=c.T@c[[1,0,3,2]]
    abase=24*np.eye(44,dtype=np.int64)-8*gamma-3*cg-cm+2
    dbase=60*np.eye(44,dtype=np.int64)+15*gamma-4*cg+cm-2
    lower=range_gram(abase,columns)
    upper=range_gram(dbase,columns)
    rank_bound=40-lower['rank']
    dt,du=lower['denominator'],upper['denominator']
    gt,gu=lower['gram'],upper['gram']
    td=[3*dt-8*int(gt[i,i]) for i in range(len(columns))]
    ud=[4*du-15*int(gu[i,i]) for i in range(len(columns))]
    eligible=[i for i in range(len(columns)) if lower['in_range'][i] and upper['in_range'][i]
              and td[i]>=0 and ud[i]>=0]
    pair_types=np.zeros((len(columns),len(columns)),dtype=np.uint8)
    pair_statistics=Counter()
    for i,j in combinations(eligible,2):
        if columns[i]['mask']&columns[j]['mask']:
            continue
        kind=0
        for is_mate in (0,1):
            tij=-8*int(gt[i,j])-is_mate*dt
            uij=-15*int(gu[i,j])+is_mate*du
            if tij*tij>td[i]*td[j] or uij*uij>ud[i]*ud[j]:
                continue
            if is_mate and (np.any(columns[i]['counts'][list(columns[j]['vertices'])]>1)
                            or np.any(columns[j]['counts'][list(columns[i]['vertices'])]>1)):
                continue
            kind|=1<<is_mate
        pair_types[i,j]=pair_types[j,i]=kind
        pair_statistics[str(kind)]+=1
    deadline=started+seconds
    summary=dict(source=record_name,initial_columns=len(columns),eligible_columns=len(eligible),
                 rank_A0=lower['rank'],rank_D0=upper['rank'],rank_E_T_at_most=rank_bound,
                 denominator_T=str(dt),denominator_U=str(du),spectral=spectral,
                 pair_types=dict(pair_statistics))
    print(json.dumps(dict(stage='SCHUR_PREPARED',**summary)),flush=True)
    outer=sorted(i for group in groups for i in group)
    full=sum(1<<i for i in outer)
    containing={v:[i for i in eligible if v in columns[i]['vertices']] for v in outer}
    statistics=Counter()
    first_control=None
    hit=None
    extension_candidate=None
    extension_failures=[]
    last_print=time.monotonic()

    def visit(used,selected,partners,et,eu):
        nonlocal last_print,first_control,hit,extension_candidate
        if time.monotonic()>=deadline:
            raise TimeoutError
        statistics['nodes']+=1
        if time.monotonic()-last_print>=5:
            print(json.dumps(dict(stage='SEARCH',statistics=dict(statistics))),flush=True)
            last_print=time.monotonic()
        if used==full:
            if any(p<0 for p in partners):
                statistics['UNPAIRED_COMPLETIONS']+=1
                return
            statistics['ADMISSIBLE_GEOMETRIES']+=1
            rank_et=exact_psd(et)[1]
            rank_eu=exact_psd(eu)[1]
            candidate,pairs=canonical_graph(gamma,columns,selected,partners)
            verdict=new_candidate_checks(candidate)
            assert verdict in ('H_MATCH_INTACT','H_MATCH_BROKEN')
            expected_broken=broken(gamma,columns,selected)
            assert (verdict=='H_MATCH_BROKEN')==expected_broken
            certificate=dict(root_columns=[list(columns[i]['vertices']) for i in selected],
                outer_mates=pairs,rank_T=lower['rank']-10+rank_et,
                rank_U=upper['rank']-10+rank_eu,
                E_T_numerator=[[str(x) for x in row] for row in et],E_T_denominator=str(8*dt),
                E_U_numerator=[[str(x) for x in row] for row in eu],E_U_denominator=str(15*du))
            if not expected_broken:
                statistics['H_MATCH_INTACT']+=1
                if first_control is None:
                    first_control=certificate
                if extension_probe:
                    from four_star_completion_columns import probe_extension
                    probe=probe_extension(candidate,seconds=max(.01,min(10,deadline-time.monotonic())))
                    statistics['EXTENSION_'+probe['status']]+=1
                    if probe['status']=='ALL_LINEAR_COLUMNS_FEASIBLE':
                        target=Path(output).with_name(Path(output).stem+'_EXTENSION_CANDIDATE.json')
                        target.write_text(json.dumps(dict(source=record_name,source_file=str(source),labels=LABELS,
                            edges=[[i,j] for i,j in combinations(range(44),2) if candidate[i,j]],
                            exact_certificates=dict(T_PSD=True,U_PSD=True,rank_T=certificate['rank_T'],rank_U=certificate['rank_U']),
                            construction=certificate,linear_extension_witnesses=probe),indent=2)+'\n',encoding='utf-8')
                        extension_candidate=str(target)
                    elif len(extension_failures)<6:
                        extension_failures.append(dict(local_solution=statistics['ADMISSIBLE_GEOMETRIES'],**probe))
                return
            # These are genuinely NEW candidate forms: check the constructed
            # integer adjacency and both exact full forms before delivering.
            mate_gram=B.T@B[[r ^ 1 for r in range(14)]]
            t8=24*np.eye(44,dtype=np.int64)-8*candidate-3*(B.T@B)-mate_gram+2
            u15=60*np.eye(44,dtype=np.int64)+15*candidate-4*(B.T@B)+mate_gram-2
            t_psd,rank_t,_=exact_psd(t8)
            u_psd,rank_u,_=exact_psd(u15)
            assert t_psd and u_psd and rank_t<=30
            assert rank_t==certificate['rank_T'] and rank_u==certificate['rank_U']
            target=Path(output).with_name(Path(output).stem+'_HIT.json')
            target.write_text(json.dumps(dict(source=record_name,source_file=str(source),labels=LABELS,
                edges=[[i,j] for i,j in combinations(range(44),2) if candidate[i,j]],
                exact_certificates=dict(T_PSD=True,U_PSD=True,rank_T=rank_t,rank_U=rank_u),
                construction=certificate),indent=2)+'\n',encoding='utf-8')
            hit=str(target)
            return
        available={v:[i for i in containing[v] if not(columns[i]['mask']&used)
                      and all(pair_types[i,j] for j in selected)]
                   for v in outer if not((used>>v)&1)}
        vertex=min(available,key=lambda v:len(available[v]))
        for i in available[vertex]:
            possible=[-1]+[j for j,p in enumerate(partners) if p<0]
            for new_mate in possible:
                if not all(pair_types[i,old]&(2 if j==new_mate else 1) for j,old in enumerate(selected)):
                    statistics['MATE_TYPE_PRUNES']+=1
                    continue
                trow=[-8*int(gt[i,j])-(dt if k==new_mate else 0) for k,j in enumerate(selected)]
                urow=[-15*int(gu[i,j])+(du if k==new_mate else 0) for k,j in enumerate(selected)]
                nt=[row+[trow[k]] for k,row in enumerate(et)]+[trow+[td[i]]]
                nu=[row+[urow[k]] for k,row in enumerate(eu)]+[urow+[ud[i]]]
                modular=np.array([[int(x)%101 for x in row] for row in nt],dtype=np.int64)
                if rank_at_least(modular,threshold=rank_bound+1)>=rank_bound+1:
                    statistics['SMALL_RANK_PRUNES']+=1
                    continue
                t_psd,rank_t,_=exact_psd(nt)
                if not t_psd or rank_t>rank_bound:
                    statistics['SMALL_T_PRUNES']+=1
                    continue
                if not exact_psd(nu)[0]:
                    statistics['SMALL_U_PRUNES']+=1
                    continue
                next_partners=partners+[new_mate]
                if new_mate>=0:
                    next_partners[new_mate]=len(selected)
                visit(used|columns[i]['mask'],selected+[i],next_partners,nt,nu)
                if hit or extension_candidate:
                    return
    exhausted=False
    try:
        if rank_bound>=0:
            visit(0,[],[],[],[])
        exhausted=hit is None and extension_candidate is None
    except TimeoutError:
        pass
    result=dict(**summary,source_file=str(source),statistics=dict(statistics),
                exhausted=exhausted,hit=hit,first_admissible_intact_control=first_control,
                extension_candidate=extension_candidate,extension_failure_examples=extension_failures,
                seconds=time.monotonic()-started,
                scope='Exact reconstruction of all outer-root transversals and outer mate matchings on these fixed central stars and this fixed unlabelled Gamma, with new spectra/kernels/ranks. Exhaustiveness only if exhausted=true. No universal H-MATCH claim.')
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='first_admissible_intact_control'}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--name')
    parser.add_argument('--seconds',type=float,default=45)
    parser.add_argument('--extension-probe',action='store_true')
    args=parser.parse_args()
    run(args.source,args.output,args.name,args.seconds,args.extension_probe)
