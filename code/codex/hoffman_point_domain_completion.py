"""Exact boundary completion by coexistence of missing-point domains.

Select |free| distinct 14-subsets, pairwise intersecting in exactly two,
with prescribed column multiplicities and final block intersections <=2.
Free point names are removed by selecting a SET of candidate incidence rows.
Every full boundary is then tested by the proved pair-cover lower bound.
"""
from itertools import combinations
from pathlib import Path
from collections import Counter
import argparse
import json
import subprocess
import time
from types import SimpleNamespace
from functools import lru_cache

from hoffman_coexistence_extensions import SOURCE,OUT
from hoffman_missing_point_domains import enumerate_missing_points
from hoffman_two_point_trades import design_key,verify
from complete_hoffman_trades import instance
from hoffman_cover_capacity import projected_covers

BASE=Path(__file__).resolve().parents[2]
ENGINE=BASE/'data/codex_hoffman_trades/rows22.exe'


def capacity_certificate(blocks,root,folder):
    folder.mkdir(exist_ok=True)
    inst=folder/'input.inst';inst.write_text(instance(blocks))
    roots=[root]+[i for i in range(77) if i!=root]
    bs=list(map(set,blocks))
    for i in roots:
        run=subprocess.run([str(ENGINE),str(inst),str(folder/'row'),'10','1000000',str(i),str(i+1)],
                           capture_output=True,text=True,check=True,timeout=20)
        stat=run.stdout.strip().split()
        if stat[3]!='EXHAUSTED':continue
        rows=[list(map(int,line.split())) for line in (folder/f'row_{i}.rows').read_text().splitlines()]
        freq=Counter(j for row in rows for j in row)
        bad=[[j,len(bs[i]&bs[j]),freq[j],2-len(bs[i]&bs[j])] for j in range(77)
             if j!=i and freq[j]<2-len(bs[i]&bs[j])]
        if len(rows)<11 or bad:
            return dict(status='UNSAT_CAPACITY',root=i,complete_domain=rows,
                        domain_size=len(rows),pair_deficits=bad,enumeration=stat)
    return dict(status='CAPACITY_SURVIVOR_OR_INCOMPLETE')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prefix',default='37c3bb63972f')
    ap.add_argument('--free',default='3,4,5,6,7')
    ap.add_argument('--seconds',type=float,default=180)
    ap.add_argument('--limit',type=int,default=50000)
    ap.add_argument('--root',type=int,default=10)
    ap.add_argument('--roots',help='Comma-separated roots whose cover requirements are propagated together')
    ap.add_argument('--no-certificates',action='store_true')
    ap.add_argument('--cover-pruning',action='store_true',help='Use cover deficits before the boundary is complete')
    ap.add_argument('--column-orbits',action='store_true',help='At quota-one branches quotient interchangeable outside columns')
    args=ap.parse_args()
    capacity_roots=sorted(set(map(int,args.roots.split(',')))) if args.roots else [args.root]
    item=next(x for x in json.loads(SOURCE.read_text())['items'] if x['design']['key'].startswith(args.prefix))
    free=sorted(map(int,args.free.split(',')));fixed=set(range(22))-set(free)
    old=list(map(set,item['design']['blocks']))
    assert not(args.no_certificates and args.cover_pruning)
    folder=OUT/(('point_prune_' if args.cover_pruning else 'point_search_')+args.prefix+'_'+args.free.replace(',','-')+
                ('_orbits' if args.column_orbits else '')+
                ('_roots'+'-'.join(map(str,capacity_roots)) if args.roots else ''))
    folder.mkdir(parents=True,exist_ok=True)
    datafolder=OUT/('point_domains_'+args.prefix+'_'+args.free.replace(',','-'))
    if (datafolder/'point_domain.json').exists():
        source=json.loads((datafolder/'point_domain.json').read_text())
    else:source=enumerate_missing_points(item['design']['blocks'],free,datafolder)
    assert source['complete']
    rows=source['rows'];masks=[sum(1<<j for j in row) for row in rows]
    assert len(set(masks))==len(masks)
    n=len(rows)
    by_col=[sum(1<<a for a,row in enumerate(rows) if j in row) for j in range(77)]
    pairs=[list(combinations(row,2)) for row in rows]
    overlap=[[len((a&b)&fixed) for b in old] for a in old]
    quota=[len(b)-len(b&fixed) for b in old]
    nodes=leaves=orbit_skips=0;classes={};seen_leaves=set();stop_reason=None
    prunes=[]
    projected=[];projected_masks=[];projected_stats=None
    if args.cover_pruning:
        assert all(old[r] <= fixed for r in capacity_roots)
        all_projected=set();projected_stats={}
        for r in capacity_roots:
            cc,stat=projected_covers(SimpleNamespace(fixed=fixed,blocks=old),r,folder/f'projected_{r}')
            all_projected.update(map(tuple,cc));projected_stats[r]=stat
        projected=list(map(list,sorted(all_projected)))
        projected_masks=[sum(1<<j for j in c) for c in projected]
    projected_by_col=[sum(1<<a for a,c in enumerate(projected) if j in c) for j in range(77)]
    fixed_overlap=[[len((a&b)&fixed) for b in old] for a in old]
    bases={r:[2-len(old[r]&b) if j!=r else 0 for j,b in enumerate(old)] for r in capacity_roots}
    start=time.monotonic()

    def exactly_two(columns,indices,universe):
        b0=b1=b2=b3=0
        for j in indices:
            carry=columns[j]
            b0,carry=b0^carry,b0&carry
            b1,carry=b1^carry,b1&carry
            b2,carry=b2^carry,b2&carry
            b3 ^= carry
        return universe & ~b0 & b1 & ~b2 & ~b3

    @lru_cache(maxsize=4096)
    def get_compatible(a):
        return exactly_two(by_col,rows[a],(1<<n)-1)

    @lru_cache(maxsize=4096)
    def single_point_covers(a):
        ok=exactly_two(projected_by_col,rows[a],(1<<len(projected))-1)
        for i,j in pairs[a]:
            if fixed_overlap[i][j]:ok &= ~(projected_by_col[i]&projected_by_col[j])
        return ok

    # Targeted check of the bit-sliced population counter used for speed.
    for a in sorted({0,n//2,n-1}):
        assert get_compatible(a)==sum(1<<b for b,mask in enumerate(masks)
                                      if (masks[a]&mask).bit_count()==2)

    def checkpoint(exhaustive=False):
        result=dict(source=item['design']['key'],source_blocks=item['design']['blocks'],
                    free=free,point_domain_count=n,nodes=nodes,sets_of_missing_rows=leaves,
                    classes=list(classes.values()),exhaustive=exhaustive,
                    stop_reason=stop_reason,elapsed_seconds=time.monotonic()-start,
                    arguments=vars(args),cover_prunes=prunes,
                    projected_cover_masks=list(map(str,projected_masks)),projected_statistics=projected_stats,
                    column_orbit_skips=orbit_skips,capacity_roots=capacity_roots)
        if exhaustive and args.cover_pruning:
            result['status']=('UNSAT_ALL_BOUNDARY_EXTENSIONS' if
                all(x.get('certificate',{}).get('status')=='UNSAT_CAPACITY' for x in classes.values())
                else 'UNDECIDED_SURVIVING_BOUNDARIES')
        (folder/'result.json').write_text(json.dumps(result,separators=(',',':')))

    def dfs(av,remaining,selected,cover_ids,symmetry_safe=True):
        nonlocal nodes,leaves,stop_reason,orbit_skips
        if stop_reason:return
        nodes+=1
        if nodes%16384==0:
            progress=dict(nodes=nodes,cover_prunes=len(prunes),complete_boundaries=leaves,
                          classes=len(classes),elapsed_seconds=time.monotonic()-start,
                          current_depth=len(selected))
            (folder/'progress.json').write_text(json.dumps(progress))
            print('PROGRESS',progress,flush=True)
        if nodes%1024==0 and time.monotonic()-start>args.seconds:
            stop_reason='TIME_LIMIT';return
        if args.cover_pruning:
            for r in capacity_roots:
                root_covers=cover_ids&projected_by_col[r]
                cover_count=root_covers.bit_count()
                if cover_count<11:
                    prunes.append(dict(selected=selected,root=r,kind='less_than_eleven',covers=cover_count))
                    return
                base=bases[r]
                bad=next((j for j in range(77) if (root_covers&projected_by_col[j]).bit_count()<base[j]),None)
                if bad is not None:
                    prunes.append(dict(selected=selected,root=r,kind='pair_capacity',other=bad,
                                       available=(root_covers&projected_by_col[bad]).bit_count(),
                                       required=base[bad],covers=cover_count))
                    return
        if remaining==0:
            assert not any(quota)
            keyset=tuple(sorted(selected))
            assert keyset not in seen_leaves, 'Duplicate enumeration path'
            seen_leaves.add(keyset);leaves+=1
            blocks=[set(b&fixed) for b in old]
            for p,a in zip(free,keyset):
                for j in rows[a]:blocks[j].add(p)
            blocks=[sorted(b) for b in blocks]
            key,aut=design_key(blocks)
            if key not in classes:
                verify(tuple(tuple(b) for b in blocks))
                rec=dict(key=key,aut=int(aut),blocks=blocks)
                if not args.no_certificates:
                    rec['certificate']=capacity_certificate(blocks,args.root,folder/('design_'+key[:12]))
                classes[key]=rec
                print('CLASS',len(classes),key[:12],'Aut',aut,
                      rec.get('certificate',{}).get('status'),
                      'nodes',nodes,'seconds',round(time.monotonic()-start,2),flush=True)
                checkpoint()
            if leaves>=args.limit:stop_reason='SOLUTION_LIMIT'
            return
        if av.bit_count()<remaining:return
        best=None;bestscore=None
        for j,r in enumerate(quota):
            if r:
                opts=av&by_col[j];count=opts.bit_count()
                if count<r:return
                # Prefer a quota-one constraint. General include/exclude
                # branching below also handles larger quotas without a cap.
                score=(count if r==1 else count*(count-1)//2 if r==2 else count**r)
                if bestscore is None or score<bestscore:
                    best=j;bestscore=score
        assert best is not None
        opts=av&by_col[best]
        use_orbits=args.column_orbits and symmetry_safe and quota[best]==1
        signatures=set()
        groups=None
        if use_orbits:
            # Columns may be permuted only within equal retained/selected
            # incidence vectors. Fixing 'best' still leaves each row orbit
            # characterized by its number of entries in these classes.
            # Quota one removes ALL rows meeting best after a choice, so
            # earlier branch alternatives do not break this symmetry.
            groups=[]
            for j,b in enumerate(old):
                sig=sum(1<<p for p in b&fixed)
                for a in selected:sig=(sig<<1)|int(j in rows[a])
                groups.append(sig)
        next_symmetry_safe=symmetry_safe and quota[best]==1
        while opts and not stop_reason:
            bit=opts&-opts;opts-=bit;av &= ~bit
            a=bit.bit_length()-1
            if use_orbits:
                signature=tuple(sorted(Counter(groups[j] for j in rows[a]).items()))
                if signature in signatures:
                    orbit_skips+=1
                    continue
                signatures.add(signature)
            # This is the first chosen row on 'best'; earlier alternatives
            # are excluded, so each set of missing rows has one search path.
            next_av=av&get_compatible(a)
            for j in rows[a]:
                quota[j]-=1
                assert quota[j]>=0
                if quota[j]==0:next_av &= ~by_col[j]
            for i,j in pairs[a]:
                assert overlap[i][j]<2
                overlap[i][j]+=1
                if overlap[i][j]==2:next_av &= ~(by_col[i]&by_col[j])
            next_covers=cover_ids
            if args.cover_pruning:
                next_covers=cover_ids&single_point_covers(a)
                for previous in selected:
                    common=masks[a]&masks[previous]
                    assert common.bit_count()==2
                    bit=common&-common
                    i=bit.bit_length()-1;j=(common^bit).bit_length()-1
                    next_covers &= ~(projected_by_col[i]&projected_by_col[j])
            dfs(next_av,remaining-1,selected+[a],next_covers,next_symmetry_safe)
            for i,j in pairs[a]:overlap[i][j]-=1
            for j in rows[a]:quota[j]+=1

    dfs((1<<n)-1,len(free),[],(1<<len(projected))-1)
    checkpoint(exhaustive=stop_reason is None)
    print('RESULT','EXHAUSTED' if stop_reason is None else stop_reason,'nodes',nodes,
          'sets',leaves,'classes',len(classes),'cover_prunes',len(prunes),
          'prune_depths',dict(Counter(len(p['selected']) for p in prunes)),
          'column_orbit_skips',orbit_skips,
          'seconds',time.monotonic()-start,flush=True)


if __name__=='__main__':main()
