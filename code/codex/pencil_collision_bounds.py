"""Binary mass-six collision bounds conditional on a pencil of m grids.

Refine the 24 far points of a fixed twin pair into the other m-2 prisms
and the three apex fibres of the remaining cubic graph. This is a necessary
profile model, not a claim of existence or a complete all-mass collision audit.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
import argparse
import gzip
import json
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,vstack,hstack

from higher_census_minima import ROOT
from six_three_small_mass_bounds import colour_key,admissible
from six_three_mass6_profile_lp import build,certificate
from f0_prism_bounds import pair_model,verify


def read(name):
    with gzip.open(ROOT/f'data/{name}.json.gz','rt') as stream:
        return json.load(stream)


def cells(m,base):
    out=[]
    for block in range(m-2):
        for vertex in range(6):
            out.append({'base':0,'mask':0,'size':1,'kind':'Z',
                        'colour':vertex%3,'block':block,'vertex':vertex})
    if m<6:
        for colour in range(3):
            out.append({'base':0,'mask':0,'size':12-2*m,'kind':'Z',
                        'colour':colour,'block':None,'vertex':None})
    for i,(mask,size) in enumerate(base['profiles']):
        degree=(mask&63).bit_count()
        if degree==0: continue
        if degree==1:
            vertices=[j for j in range(12) if mask>>j&1]
            out.append({'base':i,'mask':mask,'size':size,'kind':'B',
                        'quota':[2-sum(v%3==c for v in vertices) for c in range(3)]})
        else:
            assert degree==2 and size==1
            colour=next(j for j in range(3) if mask>>j&1)
            out.append({'base':i,'mask':mask,'size':1,'kind':'A','colour':colour})
    assert sum(x['size'] for x in out)==87
    assert sum(x['size'] for x in out if x['kind']=='Z')==24
    return out


def fixed_edge(a,b):
    if a['kind']=='A' or b['kind']=='A':
        if a['kind']!='A': a,b=b,a
        if b['kind']=='A': return 1
        if b['kind']=='B': return 0
        return int(a['colour']==b['colour'])
    if a['kind']=='Z' and b['kind']=='Z':
        if a['block'] is None and b['block'] is None: return None
        if a['block']!=b['block']: return 0
        u,v=a['vertex'],b['vertex']
        return int(u!=v and (u//3==v//3 or u%3==v%3))
    if {a['kind'],b['kind']}=={'B','Z'}:
        if a['kind']!='B': a,b=b,a
        if a['quota'][b['colour']]==0: return 0
    return None


def generate(m,verify_only=False):
    start=time.monotonic()
    source=read('codex_mass6_family_patterns')['by_outside_size']
    split=read('codex_f0_internal_pattern_split')
    base=source['3']; meta=cells(m,base)
    # The three apices and their triangle are known, even when a chosen
    # outside triple does not itself contain an apex.
    core=list(base['core_adjacency'])+[0]*3
    for colour in range(3):
        a=12+colour
        for v in [colour,colour+3,colour+6,colour+9]:
            core[a]|=1<<v; core[v]|=1<<a
        for other in range(3):
            if other!=colour: core[a]|=1<<(12+other)
    assert admissible(core)

    @lru_cache(None)
    def local_valid(tags,edges):
        graph=list(core); chosen=[]
        for base_id,colour in tags:
            mask=base['profiles'][base_id][0]
            degree=(mask&63).bit_count()
            if degree==2:
                chosen.append(12+next(c for c in range(3) if mask>>c&1))
            else:
                if degree==0: mask=1<<(12+colour)
                vertex=len(graph); chosen.append(vertex); graph.append(mask)
                for u in range(vertex):
                    if mask>>u&1: graph[u]|=1<<vertex
        for bit,(i,j) in enumerate(combinations(range(len(tags)),2)):
            u,v=chosen[i],chosen[j]
            if edges>>bit&1:
                graph[u]|=1<<v;graph[v]|=1<<u
            elif graph[u]>>v&1: return False
        return admissible(graph)

    report={'pencil_size':m,'cells':meta,'by_outside_size':{}}
    for r in (2,3):
        coarse={ (tuple(row['profiles']),row['edges']):dict(row['counts'])
                 for row in source[str(r)]['patterns'] }
        if r==3:
            for row in split['patterns']:
                key=(tuple(row['profiles']),row['edges'])
                coarse[key].update(row['counts'])
        patterns=[]
        for ids in combinations_with_replacement(range(len(meta)),r):
            if any(n>meta[i]['size'] for i,n in Counter(ids).items()): continue
            items=[meta[i] for i in ids]
            ij=list(combinations(range(r),2))
            known=[fixed_edge(items[i],items[j]) for i,j in ij]
            base_ids=tuple(item['base'] for item in items)
            tags=tuple((item['base'],item.get('colour',-1)) for item in items)
            for edges in range(1<<len(ij)):
                if any(v is not None and v!=((edges>>bit)&1) for bit,v in enumerate(known)): continue
                if colour_key(ids,edges)!=(ids,edges): continue
                key=colour_key(base_ids,edges)
                if key not in coarse: continue
                # Every B point sees exactly one point in each extra prism,
                # and exactly quota[c] far points of apex colour c.
                # Every Z point sees exactly one far point of each colour.
                valid=True
                for centre,item in enumerate(items):
                    neighbours=[items[j if i==centre else i] for bit,(i,j) in enumerate(ij)
                                if centre in (i,j) and edges>>bit&1
                                and items[j if i==centre else i]['kind']=='Z']
                    colours=Counter(x['colour'] for x in neighbours)
                    if item['kind']=='B':
                        if any(n>item['quota'][c] for c,n in colours.items()): valid=False
                        blocks=Counter(x['block'] for x in neighbours if x['block'] is not None)
                        if any(n>1 for n in blocks.values()): valid=False
                    elif item['kind']=='Z' and any(n>1 for n in colours.values()): valid=False
                if not valid or not local_valid(tags,edges): continue
                patterns.append({'profiles':ids,'edges':edges,'counts':coarse[key]})
        block={'core_adjacency':base['core_adjacency'],
               'profiles':[(x['mask'],x['size']) for x in meta],'patterns':patterns}
        report['by_outside_size'][str(r)]=block
        print('Pencil',m,'outside',r,'cells',len(meta),'patterns',len(patterns),
              'seconds',round(time.monotonic()-start,1),flush=True)
    path=ROOT/f'data/codex_pencil_{m}_patterns.json.gz'
    if verify_only:
        with gzip.open(path,'rt') as stream:
            assert json.load(stream)==json.loads(json.dumps(report))
    else:
        with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:
            stream.write(json.dumps(report).encode())
    return report


def model(m):
    packet=read(f'codex_pencil_{m}_patterns');meta=packet['cells']
    data=packet['by_outside_size']['3']
    pairs,caps,rows,matrix,constants=build(data)
    small=packet['by_outside_size']['2']
    small=dict(small,patterns=[dict(row,counts={'F0':sum(row['counts'].values())})
                               for row in small['patterns']])
    pp,pc,pr,pm,pconst,offset,po=pair_model(small)
    assert pairs==pp and caps[:len(pp)]==pc
    chosen=[i for i,(name,_,_) in enumerate(pr) if name.startswith(('forced_','forbidden_'))]
    extra=[pr[i] for i in chosen]
    index={pair:j for j,pair in enumerate(pairs)}
    def eq(name,constant,coeff):
        extra.append((name+'+',-constant,coeff))
        extra.append((name+'-',constant,{i:-v for i,v in coeff.items()}))
    for pair,j in index.items():
        val=fixed_edge(meta[pair[0]],meta[pair[1]])
        if val is not None: eq(f'fixed_{pair}',val*caps[j],{j:1})
    for i,cell in enumerate(meta):
        if cell['kind'] not in ('B','Z'): continue
        for colour in range(3):
            coeff={j:(2 if pair[0]==pair[1] else 1)
                   for pair,j in index.items() if i in pair
                   and meta[pair[1] if pair[0]==i else pair[0]]['kind']=='Z'
                   and meta[pair[1] if pair[0]==i else pair[0]]['colour']==colour}
            quota=cell['quota'][colour] if cell['kind']=='B' else 1
            eq(f'far_colour_{i}_{colour}',cell['size']*quota,coeff)
        if cell['kind']=='B':
            for block in range(m-2):
                coeff={j:1 for pair,j in index.items() if i in pair
                       and meta[pair[1] if pair[0]==i else pair[0]].get('block')==block}
                eq(f'one_in_prism_{i}_{block}',cell['size'],coeff)
    rr,cc,vv=[],[],[]
    for r,(_,_,coeff) in enumerate(extra):
        for c,v in coeff.items():rr.append(r);cc.append(c);vv.append(v)
    addon=coo_matrix((vv,(rr,cc)),shape=(len(extra),len(caps))).tocsr()
    rows+=extra;matrix=vstack((matrix,addon)).tocsr()
    constants=np.concatenate((constants,np.array([c for _,c,_ in extra],dtype=float)))
    # Exact zero/one-point channels: 1488 + 954 + 1224 + 480.
    offset+=4146
    objectives={
        'all_including90':(offset,po+[-row['counts']['63_63']-row['counts']['90_90'] for row in data['patterns']]),
        'all_except90':(offset,po+[-row['counts']['63_63'] for row in data['patterns']]),
        'F0_disjoint':(0,[0]*len(pairs)+[-row['counts']['disjoint_negative_triangles'] for row in data['patterns']])}
    total_offset,total_objective=objectives['all_including90']
    objectives['negative_all_including90']=(-total_offset,[-x for x in total_objective])
    return caps,rows,matrix,constants,objectives


def run(m,verify_only=False,selected=None):
    start=time.monotonic();caps,rows,matrix,constants,objectives=model(m)
    path=ROOT/f'data/codex_pencil_{m}_collision_bounds.json.gz'
    if verify_only or path.exists():
        with gzip.open(path,'rt') as stream:report=json.load(stream)
    else: report={'pencil_size':m,'results':{},'scope':__doc__}
    if verify_only:
        assert report['variables']==len(caps) and report['rows']==len(rows)
        if selected is None:selected=list(report['results'])
    else:report.update(variables=len(caps),rows=len(rows))
    for label,(offset,objective) in objectives.items():
        if selected is not None and label not in selected:continue
        if not verify_only:
            print('Solving pencil',m,label,flush=True)
            result=linprog(np.array(objective,dtype=float),A_ub=-matrix,b_ub=constants,
                           bounds=list(zip([0]*len(caps),caps)),method='highs-ipm')
            assert result.success,result.message
            proof=certificate(rows,caps,objective,result)
            upper=F(proof['collision_upper_bound'])+offset
            report['results'][label]={'certificate':proof,'objective_constant':offset,
                                     'upper_bound':str(upper),'even_upper_bound':int(2*(upper//2))}
        record=report['results'][label]
        verify(rows,caps,objective,record['certificate'])
        upper=F(record['certificate']['collision_upper_bound'])+offset
        assert record['objective_constant']==offset and F(record['upper_bound'])==upper
        assert record['even_upper_bound']==2*(upper//2)
        print('Verified pencil',m,label,'<=',record['even_upper_bound'],
              'rational',str(upper),'seconds',round(time.monotonic()-start,1),flush=True)
        if not verify_only:
            with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:
                stream.write(json.dumps(report).encode())


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--size',type=int,choices=(2,3,4,6),required=True)
    parser.add_argument('--generate',action='store_true')
    parser.add_argument('--verify-only',action='store_true')
    parser.add_argument('--objectives',nargs='+')
    args=parser.parse_args()
    if args.generate:generate(args.size,args.verify_only)
    else:run(args.size,args.verify_only,args.objectives)
