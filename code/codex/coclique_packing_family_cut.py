"""Average a saturated-pair certificate into a reusable population inequality.

For cell populations p, the inequality has the form
  sum p_a L_a <= sum z_abc T_abc(p)
                 + sum max(0,K_ab-M_ab(p))*P_ab(p).
P counts possible edges; T counts saturated-pair/centre triples. It follows
by weighting quotas and packing premises and bounding each remaining edge.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
from math import lcm,gcd
from functools import reduce
import argparse
import json
import time

from ortools.sat.python import cp_model
from coclique_defect_cut_loop import Master
from coclique_saturated_pairs import system,verify


def derive(master,pop,proof):
    eq,edges,rows,packing=system(master.core,pop)
    y=[0]*len(eq);z=[0]*len(packing)
    for item in proof['equations']:y[item['index']]=item['coefficient']
    for item in proof['packing']:z[item['index']]=item['coefficient']
    assert verify(eq,edges,packing,y,z)['valid']
    colours=[]
    for item in pop['selected_rows']:
        colours.extend(k<item['coclique_count'] for k in range(item['count']))
    cells=[2*master.lookup[sum(1<<i for i in row)]+int(not colours[v]) for v,row in enumerate(rows)]
    counts=defaultdict(int)
    for a in cells:counts[a]+=1
    sums=defaultdict(lambda:[0]*(master.n+2))
    for item in proof['equations']:
        reason=eq[item['index']]['reason'];a=cells[reason[1]]
        coord=0 if reason[0]=='degree' else 1 if reason[0]=='coclique_degree' else 2+reason[2]
        sums[a][coord]+=item['coefficient']
    triple_sums=defaultdict(int)
    for item in proof['packing']:
        premise=packing[item['index']];u,v=premise['saturated_pair'];w=premise['neighbour']
        a,b=sorted((cells[u],cells[v]));c=cells[w]
        assert c not in (a,b)
        triple_sums[a,b,c]+=item['coefficient']
    ww={a:[Fraction(t,counts[a]) for t in values] for a,values in sums.items()}
    zz={key:Fraction(value,(counts[key[0]]*counts[key[1]] if key[0]!=key[1] else
                  counts[key[0]]*(counts[key[0]]-1)//2)*counts[key[2]]) for key,value in triple_sums.items()}
    denominator=lcm(*[x.denominator for values in ww.values() for x in values],*[x.denominator for x in zz.values()])
    w={a:[int(x*denominator) for x in values] for a,values in ww.items()}
    z={key:int(x*denominator) for key,x in zz.items()}
    divisor=reduce(gcd,[abs(x) for values in w.values() for x in values]+list(z.values()))
    w={a:[x//divisor for x in values] for a,values in w.items()};z={k:x//divisor for k,x in z.items()}
    cut=dict(weights={str(a):values for a,values in w.items()},
             packing_weights=[dict(leaves=[a,b],centre=c,coefficient=t) for (a,b,c),t in z.items()],
             scope='Every common population of this support, not only the source witness')
    checked=evaluate(master,cut,counts);assert checked['gap']>0,checked
    cut['source_evaluation']=checked
    return cut


def terms(master,cut):
    weights={int(a):w for a,w in cut['weights'].items()};zero=[0]*(master.n+2)
    lhs={}
    for a,w in weights.items():
        t=a//2
        lhs[a]=w[0]*(master.degree-master.rows[t].bit_count())+w[1]*(master.cdegree if a%2 else 0)+sum(w[i+2]*v for i,v in enumerate(master.h[t]))
    corrections=defaultdict(lambda:defaultdict(int));constants=defaultdict(int)
    for item in cut['packing_weights']:
        a,b=item['leaves'];c=item['centre'];z=item['coefficient']
        if a!=b:
            corrections[tuple(sorted((a,c)))][b]+=z
            corrections[tuple(sorted((b,c)))][a]+=z
        else:
            pair=tuple(sorted((a,c)));corrections[pair][a]+=z;constants[pair]-=z
    edge_terms=[]
    for a in range(len(master.p)):
        for b in range(a,len(master.p)):
            if a not in weights and b not in weights:continue
            if not(a%2 or b%2) or b//2 not in master.allowed[a//2]:continue
            if a==b and master.upper[a//2]<2:continue
            wa,wb=weights.get(a,zero),weights.get(b,zero);ra,rb=master.rows[a//2],master.rows[b//2]
            K=wa[0]+wb[0]+(wa[1] if b%2==0 else 0)+(wb[1] if a%2==0 else 0)
            K+=sum(wa[2+i] for i in range(master.n) if rb>>i&1)+sum(wb[2+i] for i in range(master.n) if ra>>i&1)
            # When both endpoints exist, correction >=0. A nonpositive K
            # therefore contributes zero; an absent endpoint has zero pairs.
            if K<=0:continue
            edge_terms.append((a,b,K-constants[a,b],dict(corrections[a,b])))
    return lhs,edge_terms


def evaluate(master,cut,counts):
    counts=defaultdict(int,counts);lhs,edges=terms(master,cut)
    left=sum(v*counts[a] for a,v in lhs.items());right=0
    for item in cut['packing_weights']:
        a,b=item['leaves'];c=item['centre']
        pairs=counts[a]*counts[b] if a!=b else counts[a]*(counts[a]-1)//2
        right+=item['coefficient']*pairs*counts[c]
    for a,b,K,corr in edges:
        paircount=counts[a]*counts[b] if a!=b else counts[a]*(counts[a]-1)//2
        right+=max(0,K-sum(t*counts[c] for c,t in corr.items()))*paircount
    return dict(left=left,right=right,gap=left-right)


def install(master,cut):
    m=master.model;p=master.p
    def pair(a,b):
        a,b=sorted((a,b));ua,ub=master.upper[a//2],master.upper[b//2]
        if (a,b) not in master.products:
            if a==b:
                sq=m.NewIntVar(0,ua*ua,f'pack_sq{a}');m.AddMultiplicationEquality(sq,[p[a],p[a]])
                v=m.NewIntVar(0,ua*(ua-1)//2,f'pack_pairs{a}');m.Add(2*v==sq-p[a])
            else:
                v=m.NewIntVar(0,ua*ub,f'pack_pairs{a}_{b}');m.AddMultiplicationEquality(v,[p[a],p[b]])
            master.products[a,b]=v
        return master.products[a,b],ua*ub if a!=b else ua*(ua-1)//2
    left,edges=terms(master,cut);right=[]
    for idx,item in enumerate(cut['packing_weights']):
        a,b=item['leaves'];c=item['centre'];v,u=pair(a,b)
        triple=m.NewIntVar(0,u*master.upper[c//2],f'pack_triple{idx}')
        m.AddMultiplicationEquality(triple,[v,p[c]]);right.append(item['coefficient']*triple)
    for idx,(a,b,K,corr) in enumerate(edges):
        v,u=pair(a,b)
        if corr:
            score=m.NewIntVar(0,K,f'pack_score{idx}')
            m.AddMaxEquality(score,[0,K-sum(t*p[c] for c,t in corr.items())])
            weighted=m.NewIntVar(0,K*u,f'pack_weighted{idx}')
            m.AddMultiplicationEquality(weighted,[score,v]);right.append(weighted)
        else:right.append(K*v)
    m.Add(sum(t*p[a] for a,t in left.items())<=sum(right))
    return dict(edge_terms=len(edges),packing_terms=len(cut['packing_weights']),products=len(master.products))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--seconds',type=float,default=90)
    args=ap.parse_args();root=Path('data/codex_coclique_defects');folder=args.folder;folder.mkdir(parents=True,exist_ok=True)
    core=json.loads((root/'core_a0_e2.json').read_text());master=Master(core)
    for name in ('learned_cuts_e2_run1','learned_cuts_e2_pruned','learned_cuts_e2_combined'):
        for path in sorted((root/name).glob('certificate_*.json')):
            proof=json.loads(path.read_text())
            if proof['status']=='EXACT_CONTRADICTION':master.learn(json.loads(path.with_name(path.name.replace('certificate_','population_')).read_text()),proof)
    pop=json.loads((root/'learned_cuts_e2_combined/population_003.json').read_text())
    proof=json.loads((root/'integer_frontier_probe/saturated_pair_certificate.json').read_text())
    cut=derive(master,pop,proof);(folder/'family_cut.json').write_text(json.dumps(cut,indent=2)+'\n')
    stats=install(master,cut);print(json.dumps(dict(inherited=len(master.cuts),new_cut=stats,evaluation=cut['source_evaluation'])),flush=True)
    solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=args.seconds;solver.parameters.num_search_workers=6
    solver.parameters.log_search_progress=True;solver.parameters.log_to_stdout=False
    with (folder/'solver.log').open('w') as log:
        solver.log_callback=lambda line:(log.write(line+'\n'),log.flush())
        status=solver.Solve(master.model)
    result=dict(status=solver.StatusName(status),seconds=solver.WallTime(),branches=solver.NumBranches(),conflicts=solver.NumConflicts(),
                inherited_cuts=len(master.cuts),new_cuts=1,stats=stats,scope='One support, eleven cuts; SAT is not an SRG')
    if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):(folder/'population.json').write_text(json.dumps(master.witness(solver),indent=2)+'\n')
    (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
