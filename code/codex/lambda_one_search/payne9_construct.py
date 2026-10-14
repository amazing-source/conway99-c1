"""Construct a (243,22,1,2) SRG as a 3-ovoid of a derived quadrangle.

Points are (a,b,c) in GF(9)^3, GF(9)=GF(3)[t]/(t^2+1).
The 891 lines are vertical lines (a,b,c) with b,c fixed, and the affine
isotropic lines p+s*(b*v-c*u,u,v), directions (u,v) in PG(1,9).
The resulting point graph is checked as SRG(729,88,7,11).

Select exactly three points on every line. Any such selection gives a
243-vertex 22-regular graph with lambda=1. Common-neighbour counts of
nonadjacent selected points must still be constrained to mu=2. We lazily
forbid selected K2,3 witnesses; regularity forces equality once all these
upper bounds hold. Optional central-translation cuts are necessary for
asymmetry, rather than symmetry assumptions.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
import time

import igraph as ig
import numpy as np
import pycryptosat

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mixed_windows import graph, verify
sys.path.insert(0, str(HERE / "lab_engine"))
from row_census import counter


def geometry():
    add = [[(x%3+y%3)%3+3*((x//3+y//3)%3) for y in range(9)] for x in range(9)]
    mul = [[((x%3)*(y%3)+2*(x//3)*(y//3))%3+3*(((x%3)*(y//3)+(x//3)*(y%3))%3) for y in range(9)] for x in range(9)]
    neg = [(-x%3)%3+3*((-(x//3))%3) for x in range(9)]
    points = list(itertools.product(range(9), repeat=3))
    idx = {v:i for i,v in enumerate(points)}
    directions = [(1,v) for v in range(9)]+[(0,1)]
    lines = set()
    for a,b,c in points:
        for u,v in directions:
            da = add[mul[b][v]][neg[mul[c][u]]]
            line = tuple(sorted(idx[(add[a][mul[s][da]],add[b][mul[s][u]],add[c][mul[s][v]])] for s in range(9)))
            lines.add(line)
    for b,c in itertools.product(range(9),repeat=2):
        lines.add(tuple(idx[(a,b,c)] for a in range(9)))
    lines = sorted(lines)
    assert len(lines)==891 and all(len(L)==9 for L in lines)
    A = np.zeros((729,729),dtype=np.int64)
    counts = Counter()
    for L in lines:
        counts.update(L)
        for u,v in itertools.combinations(L,2):
            assert not A[u,v]
            A[u,v]=A[v,u]=1
    assert set(counts.values())=={11}
    assert verify(A,88,7,11), "Derived quadrangle point graph failed exact check"
    return points,idx,add,lines,A


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seconds',type=float,default=600)
    p.add_argument('--solve-seconds',type=float,default=30)
    p.add_argument('--seed',type=int,default=1)
    p.add_argument('--break-center',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    start=time.monotonic(); deadline=start+args.seconds
    points,idx,add,lines,A=geometry()
    solver=pycryptosat.Solver(threads=1)
    nv=[729]; stats=Counter(); rng=random.Random(args.seed)
    def new(): nv[0]+=1; return nv[0]
    def emit(clause): solver.add_clause(clause); stats['clauses']+=1
    for L in lines:
        counter(emit,new,[v+1 for v in L],3)
    if args.break_center:
        # Representatives of the four nonzero additive subgroups of GF(9).
        # Every central translation is fixed-point-free on all 729 points.
        for t in [1,3,4,5]:
            diffs=[]; seen=set()
            for i,(a,b,c) in enumerate(points):
                j=idx[(add[a][t],b,c)]
                key=tuple(sorted((i,j)))
                if key in seen: continue
                seen.add(key)
                d=new(); solver.add_xor_clause([i+1,j+1,d],False); diffs.append(d)
            emit(diffs)
        stats['central_translation_subgroups_forbidden']=4
    report={'construction':'3-ovoid in the Payne-derived GF(9) quadrangle',
            'ambient_parameters':[729,88,7,11], 'ambient_exact_check':True,
            'target_parameters':[243,22,1,2], 'break_center':args.break_center,
            'seed':args.seed,'status':'searching','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    discoveries=[]; cache=set()
    def save():
        report.update(seconds=round(time.monotonic()-start,3),stats=dict(stats),discoveries=discoveries)
        (args.output/'result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    save(); print('ENCODED '+json.dumps({'variables':nv[0],'clauses':stats['clauses'],'seconds':report['seconds']}),flush=True)
    while time.monotonic()<deadline:
        sat,sol=solver.solve(time_limit=min(args.solve_seconds,deadline-time.monotonic()))
        stats['solver_calls']+=1
        if sat is False:
            report['status']='UNSAT_for_this_construction'; break
        if sat is None:
            stats['undecided_calls']+=1; save()
            print('WAIT '+json.dumps({'seconds':report['seconds'],'stats':dict(stats)}),flush=True)
            continue
        H=[v for v in range(729) if sol[v+1]]
        assert len(H)==243 and all(sum(sol[v+1] for v in L)==3 for L in lines)
        B=A[np.ix_(H,H)]
        assert np.all(B.sum(1)==22)
        C=B@B
        assert np.all(C[B==1]==1)
        bad=list(zip(*np.where(np.triu((B==0)&(C>2),1))))
        stats['regular_lambda_one_candidates']+=1
        report['last_bad_pairs']=len(bad)
        report['best_bad_pairs']=min(report.get('best_bad_pairs',100000),len(bad))
        if not bad:
            assert verify(B)
            g=graph(B); aut=g.count_automorphisms()
            name=f"constructed_{len(discoveries):03d}_aut{aut}.edges"
            (args.output/name).write_text(''.join(f'{u} {v}\n' for u,v in zip(*np.where(np.triu(B,1)))),encoding='ascii')
            (args.output/(name+'.selection.json')).write_text(json.dumps(H)+'\n',encoding='utf-8')
            discoveries.append({'file':name,'automorphism_group_order':aut,'exact_srg_check':True})
            print('SRG '+json.dumps(discoveries[-1]),flush=True)
            if aut==1:
                report['status']='success_asymmetric_srg'; break
            emit([-v-1 for v in H])
        else:
            rng.shuffle(bad)
            for i,j in bad:
                common=list(map(int,np.flatnonzero(B[i]&B[j])))
                rng.shuffle(common)
                for triple in itertools.islice(itertools.combinations(common,3),3):
                    key=tuple(sorted([H[int(i)],H[int(j)]]+[H[w] for w in triple]))
                    if key not in cache:
                        emit([-v-1 for v in key]); cache.add(key)
                        stats['forbidden_K23_selections']+=1
        save()
        print('PROGRESS '+json.dumps({'seconds':report['seconds'],'bad_pairs':len(bad),'stats':dict(stats)}),flush=True)
    if report['status']=='searching': report['status']='time_limit'
    save(); print('FINAL '+json.dumps(report),flush=True)


if __name__=='__main__': main()
