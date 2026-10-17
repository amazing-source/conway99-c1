"""Reconstruct only the new proofs and witnesses using integer arithmetic."""
from pathlib import Path
from itertools import combinations
from collections import defaultdict
import json

from coclique_defect_gluing import gluing_data
from coclique_two_exception_cycles import partitions,cycle_edges,verify_witness

BASE=Path(__file__).resolve().parents[2]/'data/codex_coclique_defects'


def reconstruct(core,pop):
    S=[set() for _ in core['charges']]
    for i,j in core['edges']:S[i].add(j);S[j].add(i)
    rows=[];colours=[]
    for item in pop['selected_rows']:
        for k in range(item['count']):rows.append(set(item['vertices']));colours.append(k<item['coclique_count'])
    h=[[2-int(i in R)-len(S[i]&R) for i in range(len(S))] for R in rows]
    assert all(min(v)>=0 for v in h)
    edges=[(u,v) for u,v in combinations(range(len(rows)),2) if not(colours[u] and colours[v])
           and len(rows[u]&rows[v])<2 and all(h[u][i]>0 for i in rows[v]) and all(h[v][i]>0 for i in rows[u])]
    return S,rows,colours,h,edges


def certificate(core,pop,proof):
    S,rows,C,h,edges=reconstruct(core,pop);weights=[0]*len(edges);lhs=0
    source=proof['equations'] if isinstance(proof.get('equations'),list) else proof.get('coefficients',[])
    for item in source:
        reason=item['reason'];u=reason[1];coefficient=item['coefficient']
        if reason[0]=='degree':rhs=core['parameters']['degree']-len(rows[u]);selected=set(range(len(rows)))
        elif reason[0]=='coclique_degree':rhs=4;selected={v for v in range(len(rows)) if C[v]}
        else:rhs=h[u][reason[2]];selected={v for v in range(len(rows)) if reason[2] in rows[v]}
        assert rhs==item['rhs'];lhs+=coefficient*rhs
        for j,(a,b) in enumerate(edges):
            if (a==u and b in selected) or (b==u and a in selected):weights[j]+=coefficient
    edge_index={e:j for j,e in enumerate(edges)}
    for item in proof.get('packing',[]):
        u,v=item['saturated_pair'];w=item['neighbour'];z=item['coefficient']
        assert len(rows[u]&rows[v])==2 and z>=0 and w not in (u,v)
        idx=sorted([edge_index[tuple(sorted((u,w)))],edge_index[tuple(sorted((v,w)))]])
        assert idx==item['variables'] and item['rhs']==1
        lhs-=z
        for j in idx:weights[j]-=z
    rhs=sum(max(0,w) for w in weights)
    assert lhs>rhs
    expected=proof['verification'];assert expected['left']==lhs and expected['upper_bound']==rhs
    return dict(left=lhs,right=rhs)


def family_cut(core,pop,cut):
    data=gluing_data(core);masks=data['rows'];index={r:i for i,r in enumerate(masks)};n=len(core['charges'])
    counts=defaultdict(int)
    for item in pop['selected_rows']:
        t=index[sum(1<<i for i in item['vertices'])]
        counts[2*t]+=item['coclique_count'];counts[2*t+1]+=item['count']-item['coclique_count']
    ww={int(a):w for a,w in cut['weights'].items()};zero=[0]*(n+2)
    def h(a):return [2-int(masks[a//2]>>i&1)-(data['neighbours'][i]&masks[a//2]).bit_count() for i in range(n)]
    def allowed(a,b):
        ra,rb=masks[a//2],masks[b//2]
        return (a%2 or b%2) and (ra&rb).bit_count()<2 and all(h(a)[i]>0 for i in range(n) if rb>>i&1) and all(h(b)[i]>0 for i in range(n) if ra>>i&1)
    left=sum(p*(w[0]*(14-masks[a//2].bit_count())+w[1]*(4 if a%2 else 0)+sum(w[2+i]*v for i,v in enumerate(h(a))))
             for a,p in counts.items() for w in [ww.get(a,zero)])
    correction=defaultdict(int);penalty=0
    for item in cut['packing_weights']:
        a,b=item['leaves'];c=item['centre'];z=item['coefficient']
        assert (masks[a//2]&masks[b//2]).bit_count()==2 and z>=0
        assert allowed(a,c) and allowed(b,c) and c not in (a,b)
        pairs=counts[a]*counts[b] if a!=b else counts[a]*(counts[a]-1)//2
        penalty+=z*pairs*counts[c]
        if a==b:correction[tuple(sorted((a,c)))]+=z*(counts[a]-1)
        else:
            correction[tuple(sorted((a,c)))]+=z*counts[b]
            correction[tuple(sorted((b,c)))]+=z*counts[a]
    right=penalty
    for a in sorted(counts):
        for b in sorted(counts):
            if b<a or not allowed(a,b):continue
            wa,wb=ww.get(a,zero),ww.get(b,zero);ra,rb=masks[a//2],masks[b//2]
            K=wa[0]+wb[0]+(wa[1] if b%2==0 else 0)+(wb[1] if a%2==0 else 0)
            K+=sum(wa[2+i] for i in range(n) if rb>>i&1)+sum(wb[2+i] for i in range(n) if ra>>i&1)
            pairs=counts[a]*counts[b] if a!=b else counts[a]*(counts[a]-1)//2
            right+=max(0,K-correction[a,b])*pairs
    assert left>right
    assert (left,right)==(cut['source_evaluation']['left'],cut['source_evaluation']['right'])
    return dict(left=left,right=right)


def main():
    report={};core=json.loads((BASE/'core_a0_e2.json').read_text())
    old=json.loads((BASE/'learned_cuts_e2_combined/population_003.json').read_text())
    proofs=[(core,old,BASE/'integer_frontier_probe/saturated_pair_certificate.json')]
    for folder in ('negative_edge_population_certificates','hcomplete_population_certificates'):
        for p in (BASE/folder).glob('*_certificate.json'):
            r=json.loads(p.read_text())
            if r['status']!='EXACT_CONTRADICTION':continue
            proofs.append((json.loads(p.with_name(p.name.replace('_certificate','_core')).read_text()),
                           json.loads(p.with_name(p.name.replace('_certificate','_population')).read_text()),p))
    p=BASE/'learned_cuts_e2_packing/survivor_certificate.json'
    proofs.append((core,json.loads((p.parent/'population.json').read_text()),p))
    report['new_certificates']={str(p.relative_to(BASE)):certificate(c,pop,json.loads(p.read_text())) for c,pop,p in proofs}
    report['family_cuts']=[family_cut(core,old,json.loads((BASE/'learned_cuts_e2_packing/family_cut.json').read_text())),
        family_cut(core,json.loads((BASE/'learned_cuts_e2_packing_continuation/excluded_population_000.json').read_text()),
                   json.loads((BASE/'learned_cuts_e2_packing_continuation/cut_000.json').read_text()))]
    checked=0
    for name in ('variable_core_cycles','variable_core_cycles_population','variable_core_triangle_h0','variable_core_hcomplete_h0','variable_core_hcomplete_h1'):
        for path in (BASE/name).glob('cycles_*.json'):
            witness=json.loads(path.read_text())
            if 'edges' in witness:assert verify_witness(witness);checked+=1
    report['new_induced_witnesses']=checked
    for p in partitions(6):
        adj=defaultdict(set)
        for i,j in cycle_edges(p):adj[i].add(j);adj[j].add(i)
        assert len(adj)==24 and all(len(x)==2 for x in adj.values())
        remaining=set(adj);sizes=[]
        while remaining:
            todo=[remaining.pop()];size=0
            while todo:
                u=todo.pop();size+=1
                for v in adj[u]&remaining:remaining.remove(v);todo.append(v)
            sizes.append(size)
        assert sorted(sizes)==[4*k for k in p]
    report['cycle_partitions']=len(list(partitions(6)))
    # The parity source equations are checked independently via their actual
    # variable sets, and every source RHS is integral.
    from coclique_completion_certificate import equations
    eq,_,_,_=equations(core,old,prune_incompatible=True)
    parity=json.loads((BASE/'integer_frontier_probe/parity_cuts.json').read_text())
    for cut in parity['cuts']:
        support=set();rhs=0
        for i in cut['equations']:support.symmetric_difference_update(eq[i]['variables']);rhs^=eq[i]['rhs']%2
        assert support==set(cut['support']) and rhs==cut['odd_rhs']
        assert set(cut['flipped'])<=support and len(cut['flipped'])%2!=rhs
    report['new_parity_cuts']=len(parity['cuts']);report['status']='PASS'
    (BASE/'checks_coexistence_v3.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
