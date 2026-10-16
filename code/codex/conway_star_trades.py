"""Balanced two-row exchanges preserving an entire global star.

Write S=L4, T=L5, O=the other60 labels. The O columns are exactly the
nonmatching pairs of S. For i,j in S and each eligible k, let a_k and
b_k be the labels of columns {i,k} and {j,k}. Choose a nonempty set K
such that sum(incidence(a_k)) == sum(incidence(b_k)). Exchanging i,j
in those 2|K| columns preserves every root count, every column weight,
and the bijection of O onto nonmatching pairs. The unique T columns
of i and j may also be exchanged, provided their incidence difference
is included in the balance equation. It therefore preserves
all degrees and all mutual C2 equations of the twelve assigned rows.
The internal S matching is unchanged; S--T remains a perfect matching.

The theorem is exact; the search below covers only these exchanges,
not all star frames or all sequences of exchanges.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time
from collections import deque

sys.path.insert(0,str(Path(__file__).resolve().parent))
from conway_star_extension import read_frame, solve_selected


def balanced_trades(labels,rows,root=4,allow_mate_star=True):
    star=sorted(rows)
    assert len(star)==12 and all(root in labels[z] for z in star)
    pre={tuple(p for p in star if rows[p][z]):z for z,q in enumerate(labels)
         if root not in q and (root^1) not in q}
    assert len(pre)==60 and all(len(p)==2 for p in pre)
    for i,j in combinations(star,2):
        pairs=[]
        for k in star:
            a=tuple(sorted((i,k))); b=tuple(sorted((j,k)))
            if k not in (i,j) and a in pre and b in pre:
                x,y=pre[a],pre[b]
                vector=[int(r in labels[x])-int(r in labels[y]) for r in range(14)]
                pairs.append((k,x,y,vector))
        if allow_mate_star:
            x=next(z for z,q in enumerate(labels) if (root^1) in q and rows[i][z])
            y=next(z for z,q in enumerate(labels) if (root^1) in q and rows[j][z])
            pairs.append((-1,x,y,[int(r in labels[x])-int(r in labels[y]) for r in range(14)]))
        for mask in range(1,1<<len(pairs)):
            if mask.bit_count()<2:
                continue
            chosen=[p for t,p in enumerate(pairs) if mask>>t&1]
            if all(sum(p[3][r] for p in chosen)==0 for r in range(14)):
                yield i,j,chosen


def verify_partial(labels,rows):
    """Verify every assigned row and all common-neighbour capacity bounds."""
    for z,row in rows.items():
        assert row[z]==0 and sum(row)==12
        for r in range(14):
            assert sum(row[q] for q,p in enumerate(labels) if r in p)==2-int(r in labels[z])-int((r^1) in labels[z])
    for z,q in combinations(rows,2):
        assert rows[z][q]==rows[q][z]
        assert sum(a*b for a,b in zip(rows[z],rows[q]))+rows[z][q]==2-len(set(labels[z])&set(labels[q]))
    for q,w in combinations(range(len(labels)),2):
        common=sum(row[q]*row[w] for row in rows.values())
        edge=rows[q][w] if q in rows else rows[w][q] if w in rows else 0
        assert common+edge+len(set(labels[q])&set(labels[w]))<=2,(labels[q],labels[w])
    for q,pair in enumerate(labels):
        for r in range(14):
            used=sum(row[q] for p,row in rows.items() if r in labels[p])
            assert used<=2-int(r in pair)-int((r^1) in pair),(pair,r)


def run(source,output,target=(0,10),seconds=2):
    started=time.monotonic()
    labels,fixed=read_frame(source)
    z=labels.index(tuple(target))
    trades=sorted(balanced_trades(labels,fixed),key=lambda t:len(t[2]))
    attempts=[]
    result=dict(source_file=str(source),target=target,balanced_exchange_count=len(trades),
                scope='Only balanced exchanges from this frame are searched; no exhaustive claim over star frames.')
    for i,j,chosen in trades:
        rows={p:row.copy() for p,row in fixed.items()}
        for _,a,b,_ in chosen:
            for q in (a,b):
                rows[i][q],rows[j][q]=rows[j][q],rows[i][q]
        verify_partial(labels,rows)
        extension=solve_selected(labels,rows,[z],seconds)
        description=dict(rows=[labels[i],labels[j]],changed_columns=[labels[q] for _,a,b,_ in chosen for q in (a,b)],
                         changed_edges=4*len(chosen),status=extension['status'],solver_seconds=extension['seconds'])
        attempts.append(description)
        print(json.dumps(description),flush=True)
        if 'rows' in extension:
            rows[z]=extension['rows'][0]
            verify_partial(labels,rows)
            result.update(status='REPAIRED_AND_EXTENDED',trade=description,
                          global_new_rows=dict(labels=labels,row_labels=[labels[p] for p in sorted(rows)],
                                               rows=[rows[p] for p in sorted(rows)],
                                               exact_root_and_pair_counts=True,all_partial_c2_caps=True))
            break
    else:
        result['status']='NO_REPAIR_IN_THIS_FINITE_EXCHANGE_SET' if all(a['status']=='INFEASIBLE' for a in attempts) else 'EXCHANGE_SEARCH_INCOMPLETE'
    result.update(attempts=attempts,seconds=time.monotonic()-started)
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('attempts','global_new_rows')}),flush=True)
    return result


def search(source,output,target=(0,10),seconds=2,max_states=100,time_limit=60):
    started=time.monotonic()
    labels,previous=read_frame(source)
    fixed={z:row for z,row in previous.items() if 4 in labels[z]}
    targets=[target] if len(target)==2 and isinstance(target[0],int) else target
    ids=[labels.index(tuple(p)) for p in targets]
    assert all(z not in fixed for z in ids)
    star=sorted(fixed)
    def key(rows):
        return tuple(tuple(rows[p]) for p in star)
    queue=deque([(fixed,[])])
    seen={key(fixed)}
    attempts=[]
    result=dict(source_file=str(source),targets=targets,max_states=max_states,time_limit=time_limit,
                previous_extra_rows_recomputed=[labels[z] for z in previous if z not in fixed],
                scope='Search component of balanced exchanges, with an explicit state limit. No exhaustive claim over star frames.')
    found=False
    while queue and len(attempts)<max_states and time.monotonic()<started+time_limit:
        parent,path=queue.popleft()
        extension=None
        for z in ids:
            item=solve_selected(labels,parent,[z],seconds)
            if 'rows' not in item:
                extension=item
                break
        if extension is None:
            extension=item if len(ids)==1 else solve_selected(labels,parent,ids,seconds,pair_constraints=True)
        attempts.append(dict(state=len(attempts),path_length=len(path),status=extension['status'],solver_seconds=extension['seconds']))
        if 'rows' in extension:
            values=dict(parent)
            values.update(zip(ids,extension['rows']))
            verify_partial(labels,values)
            result.update(status='REPAIRED_AND_EXTENDED',path=path,
                          global_new_rows=dict(labels=labels,row_labels=[labels[p] for p in sorted(values)],
                                               rows=[values[p] for p in sorted(values)],
                                               exact_root_and_pair_counts=True,all_partial_c2_caps=True))
            found=True
            break
        for i,j,chosen in sorted(balanced_trades(labels,parent),key=lambda t:len(t[2])):
            rows={p:row.copy() for p,row in parent.items()}
            for _,a,b,_ in chosen:
                for q in (a,b):
                    rows[i][q],rows[j][q]=rows[j][q],rows[i][q]
            signature=key(rows)
            if signature in seen:
                continue
            seen.add(signature)
            verify_partial(labels,rows)
            description=dict(rows=[labels[i],labels[j]],changed_columns=[labels[q] for _,a,b,_ in chosen for q in (a,b)],
                             changed_edges=4*len(chosen))
            next_path=path+[description]
            queue.append((rows,next_path))
    if not found:
        result['status']='BALANCED_COMPONENT_NO_REPAIR' if not queue and all(a['status']=='INFEASIBLE' for a in attempts) else 'BALANCED_SEARCH_INCOMPLETE'
    result.update(attempts=attempts,visited_states=len(attempts),queued_unvisited=len(queue),seconds=time.monotonic()-started)
    Path(output).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('attempts','global_new_rows')}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--target',default='0,10')
    parser.add_argument('--targets',help='JSON list of rows to reconstruct jointly; implies a component search.')
    parser.add_argument('--seconds',type=float,default=2)
    parser.add_argument('--max-states',type=int,default=1)
    parser.add_argument('--time-limit',type=float,default=60)
    args=parser.parse_args()
    if args.max_states>1 or args.targets:
        target=json.loads(args.targets) if args.targets else tuple(map(int,args.target.split(',')))
        search(args.source,args.output,target,args.seconds,args.max_states,args.time_limit)
    else:
        run(args.source,args.output,tuple(map(int,args.target.split(','))),args.seconds)
