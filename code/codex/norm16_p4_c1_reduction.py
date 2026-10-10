"""Cover the C_de=1 branch of P3+P4 in the four tight-cut attachments.

Enumerate only the four P4 columns; propagate the sole other degree-two
Z vertex, its two leaves and the four isolated columns. Quotient the
resulting supports by explicit graph isomorphisms. Boundary certificates
are then needed only for the representatives, without a rank assumption.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
import argparse
import json
import networkx as nx
import numpy as np
from norm16_schur_data import ROOT,source_data,matrices
from norm16_independent_catalogue import adjacency,positive_semidefinite
from norm16_tight_boundary import solve


def templates(c,u):
    for d in range(8):
        for e in range(8):
            if c[d][e]!=1 or ((d in u)!=(e in u)):
                continue
            if any(c[d][j]==2 for j in range(8) if j not in (d,e)):
                continue
            rest=[j for j in range(8) if j not in (d,e)]
            for aa in combinations(rest,3):
                # Reversal of the P4 swaps its central columns. Choose one.
                if rest[0] not in aa or len((set(aa)|{d})&u)!=2:
                    continue
                bb=tuple(j for j in rest if j not in aa)
                if any(c[i][j]==2 for part in (aa,bb) for i,j in combinations(part,2)):
                    continue
                leaves=[{e,i,j} for i in aa for j in bb
                        if c[e][i]<2 and c[e][j]<2 and c[i][j]<2
                        and 1<=len({e,i,j}&u)<=2]
                for left,right in product(leaves,repeat=2):
                    if left==right or any(c[i][j]+int({i,j}<=left)+int({i,j}<=right)>2
                                          for i,j in combinations(range(8),2)):
                        continue
                    yield d,e,[left,{d,*aa},{d,*bb},right]


def remaining(c,columns):
    cap=2-np.array(c,dtype=int)
    np.fill_diagonal(cap,0)
    for s in columns:
        for i,j in combinations(s,2):
            cap[i,j]-=1;cap[j,i]-=1
    return cap


def isolated_completions(cap,residual,u):
    us=sorted(u);vs=sorted(set(range(8))-u)
    if min(residual)<0 or sum(residual[d] for d in us)!=4 or sum(residual[d] for d in vs)!=4:
        return
    def walk(k,needed,columns):
        if k==len(us):
            if all(needed[v]==0 for v in vs):
                yield columns
            return
        d=us[k]
        for choices in combinations_with_replacement(vs,needed[d]):
            counts=Counter(choices)
            if any(n>needed[v] or n>cap[d,v] for v,n in counts.items()):
                continue
            rr=needed.copy()
            for v,n in counts.items():rr[v]-=n
            yield from walk(k+1,rr,columns+[{d,v} for v in choices])
    yield from walk(0,list(residual),[])


def enumerate_case(oi):
    cores,cases,forests=source_data();core=cores[3]['representatives'][0]
    attach=cases[3]['orbits'][oi]['representative']
    shadows=[set(r[:2])|{8+q for q in r[2:]} for r in attach]
    c=[[len(s&t) if i!=j else 0 for j,t in enumerate(shadows)] for i,s in enumerate(shadows)]
    record=next(r for r in json.loads((ROOT/'data/codex_norm16_shadow_connectivity.json').read_text())['records'] if r['case']==3 and r['orbit']==oi)
    u=set(record['tight_subsets'][0]);forest=next(f for f in forests if f['id']==2)
    assert [(i,j) for i,j in combinations(range(11),2) if forest['adjacency_Z'][i][j]]==[(0,1),(1,2),(3,4),(4,5),(5,6)]
    counts=Counter();seeds=[]
    for d,e,p4 in templates(c,u):
        counts['P4_templates']+=1
        cap=remaining(c,p4)
        centers=[set(t) for t in combinations(range(8),4)
                 if len(set(t)&u)==2 and all(len(set(t)&s)<=2 for s in p4)
                 and all(cap[i,j]>0 for i,j in combinations(t,2))]
        if not centers:counts['P4_without_P3_center']+=1
        for center in centers:
            counts['P4_with_chosen_center']+=1
            base=p4+[center];ca=remaining(c,base)
            leaves=[set(t) for t in combinations(range(8),3)
                    if 1<=len(set(t)&u)<=2 and len(set(t)&center)<=1
                    and all(len(set(t)&s)<=2 for s in p4)
                    and all(ca[i,j]>0 for i,j in combinations(t,2))]
            for left,right in combinations(leaves,2):
                if len(left&right)>1 or center&left&right:continue
                cols=[left,center,right]+p4;cc=remaining(c,cols)
                if np.min(cc)<0:continue
                residual=[4-sum(i in s for s in cols) for i in range(8)]
                for isolated in isolated_completions(cc,residual,u):
                    allcols=cols+isolated
                    masks=[sum(1<<z for z,s in enumerate(allcols) if d in s) for d in range(8)]
                    a=adjacency(core,attach,forest,masks);common=a@a
                    if any(common[i,j]>2-a[i,j] for i,j in combinations(range(35),2)):continue
                    seed={'case':3,'orbit':oi,'forest':2,'D_Z_row_masks':masks}
                    seeds.append(seed);counts['D_Z_supports']+=1
    return dict(counts),seeds


def graph(seed):
    cores,cases,forests=source_data()
    a=adjacency(cores[3]['representatives'][0],cases[3]['orbits'][seed['orbit']]['representative'],
                next(f for f in forests if f['id']==2),seed['D_Z_row_masks'])
    g=nx.from_numpy_array(a)
    for i in g:g.nodes[i]['part']=0 if i<8 else 1 if i<16 else 2 if i<24 else 3
    return g


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--solve',action='store_true')
    parser.add_argument('--max-boundaries',type=int,default=1,help='Bound the new LP probes; stop at the first feasible relaxation.')
    args=parser.parse_args()
    result={'scope':__doc__,'case_counts':[],'representatives':[],'covered_supports':[]}
    graphs=[]
    for oi in (0,1,21,22):
        counts,seeds=enumerate_case(oi);result['case_counts'].append({'orbit':oi,**counts})
        for seed in seeds:
            g=graph(seed);index=None;mapping=None
            for j,h in enumerate(graphs):
                gm=nx.algorithms.isomorphism.GraphMatcher(g,h,node_match=nx.algorithms.isomorphism.categorical_node_match('part',None))
                if gm.is_isomorphic():index=j;mapping=gm.mapping;break
            if index is None:
                index=len(graphs);graphs.append(g);result['representatives'].append({'seed':seed});mapping={i:i for i in range(35)}
            result['covered_supports'].append({'seed':seed,'representative':index,'permutation_to_representative':[mapping[i] for i in range(35)]})
        print(json.dumps({'orbit':oi,**counts,'representatives_so_far':len(graphs)}),flush=True)
    target=ROOT/'data/codex_norm16_p4_c1_reduction.json'
    for r in result['representatives']:
        s=r['seed'];scale,h,w=matrices(3,s['orbit'],2)
        k=[[3-7*((mask>>z)&1) for z in range(11)] for mask in s['D_Z_row_masks']]
        schur=[[h[d][e]-sum(k[d][z]*w[z][t]*k[e][t] for z in range(11) for t in range(11)) for e in range(8)] for d in range(8)]
        r['exact_Schur_PSD']=positive_semidefinite(schur)
    target.write_text(json.dumps(result,indent=2)+'\n')
    if args.solve:
        tested=0
        for i,r in enumerate(result['representatives']):
            if not r['exact_Schur_PSD']:continue
            if tested>=args.max_boundaries:break
            cert=solve(r['seed']);r['boundary_result']=cert
            tested+=1
            target.write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps({'representative':i,'LP_status':cert['LP_status'],'exact_rhs_dot':cert.get('exact_Farkas',{}).get('rhs_dot')}),flush=True)
            if cert['LP_status']==0:break
        result['boundary_campaign_status']='Bounded probe only; no full boundary campaign.'
        target.write_text(json.dumps(result,indent=2)+'\n')
