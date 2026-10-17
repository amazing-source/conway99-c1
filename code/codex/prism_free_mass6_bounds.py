"""Mass-six same-sum collisions for prism-free norm-eight supports <=9.

Every representative and its partner are checked for induced prisms in
both signs. The (6,3) triple channel equals the e(W)<=8 channel already
enumerated, because the only admissible six-vertex graph with >=9 edges
is a triangular prism. Other masses and changes of sum are excluded.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import comb
import argparse
import gzip
import json
import time

import numpy as np
from scipy.optimize import linprog

from higher_census_minima import ROOT
from mass6_family_patterns import PairCounts, channels, name
from six_three_small_mass_bounds import admissible, extend, colour_key
from pencil_collision_bounds import read
from pencil_degree_moment_bounds import model as grid_model
from grid_pair_collision_bounds import model as nongrid_model
from f0_prism_bounds import pair_model, verify
from six_three_mass6_profile_lp import certificate


def prism_free(graph, support):
    for vertices in combinations(support,6):
        mask=sum(1<<v for v in vertices)
        if all((graph[v]&mask).bit_count()==3 for v in vertices):
            # K3,3 is inadmissible (three common neighbours); the other
            # cubic graph on six vertices is the triangular prism.
            return False
    return True


def six_vertex_check():
    edges=list(combinations(range(6),2)); dense=[]
    for bits in range(1<<15):
        if bits.bit_count()<9: continue
        graph=[0]*6
        for bit,(i,j) in enumerate(edges):
            if bits>>bit&1: graph[i]|=1<<j; graph[j]|=1<<i
        if admissible(graph):
            assert bits.bit_count()==9 and all(row.bit_count()==3 for row in graph)
            assert not prism_free(graph,range(6))
            dense.append(bits)
    assert len(dense)==60
    return len(dense)


def direct_counts(rep,ids,edges):
    full=np.column_stack((rep.vectors,rep.common))
    partner=np.column_stack((rep.other,rep.common))
    totals=Counter()
    for tags in ([ids] if rep.a==rep.b else [ids,[rep.reverse[i] for i in ids]]):
        graph=extend(rep.graph,[rep.profiles[i][0] for i in tags],edges)
        matrix=np.array([[(row>>i)&1 for i in range(len(graph))] for row in graph],dtype=np.int16)
        keep=np.ones(len(full),dtype=bool)
        for vector in (full,partner):
            q=3*np.sum(vector*vector,axis=1)+(vector.sum(axis=1)//3)**2-np.sum((vector@matrix)*vector,axis=1)
            keep &= q==8
        @lru_cache(None)
        def pf(support): return prism_free(graph,support)
        for j in np.flatnonzero(keep):
            a=int(np.count_nonzero(rep.vectors[j,:6]==1))
            b=int(np.count_nonzero(rep.vectors[j,6:]==-1))
            two_sided=1<=a<=5 and 1<=b<=5
            totals['two_sided']+=int(two_sided)
            free=all(pf(tuple(np.flatnonzero(sign*vector[j]==1)))
                     for vector in (full,partner) for sign in (1,-1))
            if free: assert two_sided
            totals['pf']+=int(free)
            if free and rep.a==rep.b:
                assert a+b==6
                totals['pf_ties']+=1
                apex_sum=sum(int(rep.common[j,k]) for k,tag in enumerate(tags)
                             if (rep.profiles[tag][0]&63).bit_count()==2)
                if abs(a+apex_sum)<=4 and abs(-b+apex_sum)<=4:
                    totals['grid_pool_ties']+=1
    return {key:rep.factor*totals[key] for key in ('two_sided','pf','pf_ties','grid_pool_ties')}


def generate(verify_only=False):
    start=time.monotonic(); dense=six_vertex_check()
    source=read('codex_mass6_family_patterns')['by_outside_size']
    report={'scope':__doc__,'dense_six_vertex_graphs_checked':dense,'by_outside_size':{}}
    exact=Counter(); differences=Counter(); exact_ties={'grid':Counter(),'nongrid':Counter()}
    for r in range(3):
        data=source[str(r)]
        reps={f'{name(a)}_{name(b)}':PairCounts(data['core_adjacency'],data['profiles'],a,b)
              for a,b in channels(r)}
        patterns=[]
        for row in data['patterns']:
            costs={label:direct_counts(rep,row['profiles'],row['edges']) for label,rep in reps.items()}
            counts={label:value['pf'] for label,value in costs.items()}
            for label,value in counts.items():
                assert value<=row['counts'][label]
                if value!=row['counts'][label]: differences[label]+=1
            if r<2:
                capacity=1
                for i,n in Counter(row['profiles']).items(): capacity*=comb(data['profiles'][i][1],n)
                for label,value in counts.items(): exact[label]+=capacity*value
                for label,value in costs.items():
                    exact_ties['grid'][label]+=capacity*value['grid_pool_ties']
                    exact_ties['nongrid'][label]+=capacity*value['pf_ties']
            patterns.append({'profiles':row['profiles'],'edges':row['edges'],'counts':counts,
                             'two_sided_counts':{label:value['two_sided'] for label,value in costs.items()},
                             'pf_ties':{label:value['pf_ties'] for label,value in costs.items()},
                             'grid_pool_ties':{label:value['grid_pool_ties'] for label,value in costs.items()}})
        report['by_outside_size'][str(r)]=dict(data,patterns=patterns)
        print('Verified prism-free patterns',r,len(patterns),'seconds',round(time.monotonic()-start,1),flush=True)
    assert set(differences)<= {'71_60','71_71'}
    assert sum(exact.values())==2922
    report['exact_small_channels']=dict(exact)
    report['exact_tie_small_channels']={kind:dict(values) for kind,values in exact_ties.items()}
    report['changed_pattern_counts']=dict(differences)
    # Internal (6,3) is the sole remaining triple channel for prism-free
    # representatives. Check its archived costs, then apply the two grid cuts.
    data=source['3']; rep=PairCounts(data['core_adjacency'],data['profiles'],(6,3),(6,3))
    a_count=np.count_nonzero(rep.vectors[:,:6]==1,axis=1)
    b_count=np.count_nonzero(rep.vectors[:,6:]==-1,axis=1)
    assert np.all(a_count+b_count==6)
    triple=[]
    for row in data['patterns']:
        ids,edges=row['profiles'],row['edges']; signed=rep.base.copy()
        for j,i in enumerate(ids): signed+=rep.common[:,j]*rep.dots[:,i]
        for bit,(i,j) in enumerate(combinations(range(3),2)):
            if edges>>bit&1: signed+=rep.common[:,i]*rep.common[:,j]
        keep=signed==rep.target
        for base,dots in rep.positive:
            ep=base.copy()
            for j,i in enumerate(ids): ep+=rep.cp[:,j]*dots[:,i]
            for bit,(i,j) in enumerate(combinations(range(3),2)):
                if edges>>bit&1:ep+=rep.cp[:,i]*rep.cp[:,j]
            keep &= ep<=8
        assert 2*np.count_nonzero(keep)==row['counts']['63_63']
        t=np.zeros(len(keep),dtype=np.int16)
        for j,i in enumerate(ids):
            if (data['profiles'][i][0]&63).bit_count()==2:t+=rep.common[:,j]
        keep &= (np.abs(a_count+t)<=4)&(np.abs(-b_count+t)<=4)
        triple.append({'profiles':ids,'edges':edges,'grid_pool_ties':2*int(np.count_nonzero(keep))})
    report['triple_pool_patterns']=triple
    path=ROOT/'data/codex_prism_free_mass6_patterns.json.gz'
    if verify_only: assert read('codex_prism_free_mass6_patterns')==report
    else:
        with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:stream.write(json.dumps(report).encode())
    print('Exact small channels',dict(exact),'changed patterns',dict(differences),flush=True)
    print('Tie small channels',report['exact_tie_small_channels'],'triple patterns',len(triple),flush=True)


def model(kind,ties=False):
    refined=kind=='grid'
    caps,rows,matrix,constants,_=grid_model(2) if refined else nongrid_model('all','nongrid')
    pf=read('codex_prism_free_mass6_patterns')
    field=('grid_pool_ties' if refined else 'pf_ties') if ties else 'counts'
    if refined:
        pencil=read('codex_pencil_2_patterns'); meta=pencil['cells']
        triple=pencil['by_outside_size']['3']; small=pencil['by_outside_size']['2']
        lookup={(tuple(row['profiles']),row['edges']):sum(row[field].values())
                for row in pf['by_outside_size']['2']['patterns']}
        pf71={(tuple(row['profiles']),row['edges']):row['counts']['71_71']
              for row in pf['by_outside_size']['2']['patterns']}
        assert all(pf71[colour_key(tuple(meta[i]['base'] for i in row['profiles']),row['edges'])]==0
                   for row in small['patterns'])
        small=dict(small,patterns=[dict(row,counts={'F0':lookup[colour_key(tuple(meta[i]['base'] for i in row['profiles']),row['edges'])]})
                                  for row in small['patterns']])
    else:
        triple=read('codex_mass6_family_patterns')['by_outside_size']['3']
        small=pf['by_outside_size']['2']
        small=dict(small,patterns=[dict(row,counts={'F0':sum(row[field].values())}) for row in small['patterns']])
    pairs,pc,pr,pm,pconst,offset,po=pair_model(small)
    assert caps[:len(pc)]==pc and len(caps)==len(pairs)+len(triple['patterns'])
    offset+=sum((pf['exact_tie_small_channels'][kind] if ties else pf['exact_small_channels']).values())
    if ties and refined:
        pool={(tuple(row['profiles']),row['edges']):row['grid_pool_ties'] for row in pf['triple_pool_patterns']}
        tc=[-pool[colour_key(tuple(meta[i]['base'] for i in row['profiles']),row['edges'])]
            for row in triple['patterns']]
    else:tc=[-row['counts']['63_63'] for row in triple['patterns']]
    objective=po+tc
    return caps,rows,matrix,constants,offset,objective


def scope(kind,ties):
    if not ties:return __doc__
    return ('Upper bound for mass-six same-sum equal-support collisions of prism-free Q8 representatives of support <=9. '
            + ('Both defining grid net sums have absolute value <=4. ' if kind=='grid' else
               'No defining grids are available; only equal support size and prism-freeness are imposed. ')
            +'These filters relax the globally shortest pool. Its numerator is not counted, and no lower bound for its losses is asserted.')


def run(kind,verify_only=False,ties=False):
    started=time.monotonic();caps,rows,matrix,constants,offset,objective=model(kind,ties)
    suffix=f'{kind}_ties' if ties else kind
    path=ROOT/f'data/codex_prism_free_mass6_{suffix}.json.gz'
    report=read(f'codex_prism_free_mass6_{suffix}') if verify_only else {
        'kind':kind,'variables':len(caps),'rows':len(rows),'scope':scope(kind,ties),'ties_only':ties,'results':{}}
    assert report['variables']==len(caps) and report['rows']==len(rows)
    assert report['ties_only']==ties and report['scope']==scope(kind,ties)
    for label,sign in ([('upper',1)] if ties else [('upper',1),('negative_lower',-1)]):
        target=[sign*x for x in objective]
        if not verify_only:
            print('Solving prism-free',kind,label,flush=True)
            result=linprog(np.array(target,dtype=float),A_ub=-matrix,b_ub=constants,
                           bounds=list(zip([0]*len(caps),caps)),method='highs-ipm')
            assert result.success,result.message
            proof=certificate(rows,caps,target,result)
            upper=F(proof['collision_upper_bound'])+sign*offset
            report['results'][label]={'certificate':proof,'objective_constant':sign*offset,
                                     'upper_bound':str(upper),'even_upper_bound':int(2*(upper//2))}
        record=report['results'][label]
        verify(rows,caps,target,record['certificate'])
        upper=F(record['certificate']['collision_upper_bound'])+sign*offset
        assert F(record['upper_bound'])==upper and record['objective_constant']==sign*offset
        assert record['even_upper_bound']==2*(upper//2)
        print('Verified prism-free',kind,label,'<=',record['even_upper_bound'],'rational',str(upper),
              'seconds',round(time.monotonic()-started,1),flush=True)
        if not verify_only:
            with gzip.GzipFile(filename=path,mode='wb',mtime=0) as stream:stream.write(json.dumps(report).encode())


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--generate',action='store_true')
    parser.add_argument('--verify-only',action='store_true');parser.add_argument('--kind',choices=('grid','nongrid'),default='grid')
    parser.add_argument('--ties',action='store_true')
    args=parser.parse_args()
    if args.generate:generate(args.verify_only)
    else:run(args.kind,args.verify_only,args.ties)
