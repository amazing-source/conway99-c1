"""Integer verification of the new variable-border capacity certificates.

Does not import the separator, CP-SAT, SciPy, or the cut evaluator.
"""
from pathlib import Path
from itertools import combinations
from collections import defaultdict
import json

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data/codex_coclique_defects'


def graph(w):
    a=[set() for _ in range(w['vertices'])]
    for u,v in w['edges']:
        assert u!=v and v not in a[u]
        a[u].add(v);a[v].add(u)
    return a


def check_cut(c):
    w=json.loads((ROOT/c['source']).read_text());a=graph(w)
    types={tuple(t['vertices']):t['count'] for t in w['remaining_population']}
    assert all(len(t)==2 for t in types)
    for i,j in combinations(range(4,16),2):
        assert types.get((i,j),0)==2-int(j in a[i])-len(a[i]&a[j])
    group=c['group']
    assert all(len(a[u]&a[v])==2-int(v in a[u]) for u,v in combinations(group,2))
    required=0;capacity=0
    for u,y in zip(group,c['coefficients']):
        assert len(y)==13 and all(isinstance(x,int) for x in y)
        required+=y[0]*(14-len(a[u]))
        for i in range(4,16):required+=y[i-3]*(2-int(i in a[u])-len(a[u]&a[i]))
    for (i,j),multiplicity in types.items():
        offers=[0]
        for u,y in zip(group,c['coefficients']):
            if len(a[u])==14:continue
            if sum((i in a[u],j in a[u],j in a[i]))>=2:continue
            if any(len(a[u]&a[k])==2-int(k in a[u]) for k in (i,j)):continue
            offers.append(y[0]+y[i-3]+y[j-3])
        capacity+=sum(sorted([0,0]+[max(0,x) for x in offers],reverse=True)[:multiplicity]) if c.get('simple_factors') else multiplicity*max(offers)
    assert required>capacity
    assert (required,capacity)==(c['separation']['left'],c['separation']['upper'])
    return dict(source=c['source'],group=group,left=required,upper=capacity)


def check_square(c):
    w=json.loads((ROOT/c['source']).read_text());a=graph(w);weights=c['weights']
    assert all(isinstance(u,int) and isinstance(z,int) for u,z in weights)
    q=sum(z*z*(14-len(a[u])) for u,z in weights)
    for (u,z),(v,t) in combinations(weights,2):q+=2*z*t*(2-int(v in a[u])-len(a[u]&a[v]))
    total=sum(z*(14-len(a[u])) for u,z in weights);k=c['integer_level']
    bound=(2*k+1)*total-(99-len(a))*k*(k+1)
    assert q<bound
    assert (q,total,bound)==(c['separation']['quadratic'],c['separation']['sum_loads'],c['separation']['lower_bound'])
    return dict(source=c['source'],support=len(weights),quadratic=q,integer_lower_bound=bound)


def check_transport(report):
    w=json.loads((ROOT/report['source']).read_text());a=graph(w);b=len(a)
    types=[]
    for t in w['remaining_population']:types.extend([set(t['vertices']) for _ in range(t['count'])])
    assert b+len(types)==99
    a.extend(types)
    for u in range(b,99):
        for s in a[u]:a[s].add(u)
    assert all(len(a[s])==14 for s in range(18))
    candidates=[]
    for u,v in combinations(range(18,99),2):
        if v<b:continue
        if u<b and len(a[u])==14:continue
        if len(a[u]&a[v])>1:continue
        if u<b and any(len(a[u]&a[s]&set(range(b)))==2-int(u in a[s]) for s in a[v]):continue
        candidates.append((u,v))
    valid=set(candidates)
    proofs=[]
    for stage in report['stages']:
        if stage['status']!='EXACT_CONTRADICTION':continue
        weights=defaultdict(int);left=0
        for e in stage['certificate_equations']:
            y=e['coefficient'];reason=e['reason'];u=reason[1]
            if reason[0]=='degree':
                rhs=14-len(a[u]);neighbours=set(range(99))-{u}
            else:
                s=reason[2];rhs=2-int(s in a[u])-len(a[u]&a[s]);neighbours=a[s]-{u}
            assert rhs==e['rhs'];left+=y*rhs
            for v in neighbours:
                pair=tuple(sorted((u,v)))
                if pair in valid:weights[pair]+=y
        for p in stage['certificate_packing']:
            _,u,v,t=p['reason'];z=p['coefficient'];assert z>=0
            assert len(a[u]&a[v]&set(range(b)))==2-int(v in a[u])
            left-=z
            for vertex in (u,v):
                pair=tuple(sorted((vertex,t)));assert pair in valid;weights[pair]-=z
        upper=sum(max(0,x) for x in weights.values())
        assert left>upper and (left,upper)==(stage['left'],stage['upper'])
        proofs.append(dict(mode=stage['mode'],left=left,upper=upper))
    return proofs


def check_pair_choices(report):
    w=json.loads((ROOT/report['source']).read_text());a=graph(w);copies=report['copies'];checked=0
    for subgroup in report['proper_subgroups']:
        assert subgroup['status'] in ('OPTIMAL','FEASIBLE')
        selected={entry['vertex']:entry['copies'] for entry in subgroup['chosen']}
        for u,ks in selected.items():
            assert len(set(ks))==len(ks)==14-len(a[u])
            if report.get('simple_factors'):assert len({tuple(copies[k]) for k in ks})==len(ks)
            for i in range(4,16):
                assert sum(i in copies[k] for k in ks)==2-int(i in a[u])-len(a[u]&a[i])
            for k in ks:
                i,j=copies[k]
                assert sum((i in a[u],j in a[u],j in a[i]))<=1
                assert all(len(a[u]&a[v])<2-int(v in a[u]) for v in (i,j))
        for u,v in combinations(selected,2):
            assert not(set(selected[u])&set(selected[v]))
        checked+=1
    return checked


def positive_square_fixture():
    from itertools import product
    adj=[{v for v in range(9) if u!=v and (u//3==v//3 or u%3==v%3)} for u in range(9)]
    B=[0,1,3,4,8];R=[u for u in range(9) if u not in B]
    for z in product((-1,0,1),repeat=len(B)):
        d=[4-len(adj[u]&set(B)) for u in B]
        q=sum(t*t*x for t,x in zip(z,d))
        for i,j in combinations(range(len(B)),2):
            u,v=B[i],B[j]
            q+=2*z[i]*z[j]*(2-int(v in adj[u])-len(adj[u]&adj[v]&set(B)))
        loads=[sum(t for u,t in zip(B,z) if v in adj[u]) for v in R]
        assert q==sum(x*x for x in loads)
        total=sum(t*x for t,x in zip(z,d));assert total==sum(loads)
        for k in range(-2,3):assert q>=(2*k+1)*total-len(R)*k*(k+1)
    return dict(graph='3x3 rook',signed_weight_vectors=243,status='PASS')


def main():
    cuts=json.loads((DATA/'variable_border_cuts_v4/combined_13_cuts.json').read_text())
    checked=[check_cut(c) for c in cuts]
    sharpened=json.loads((DATA/'variable_border_cuts_v4/combined_13_simple_cuts.json').read_text())
    checked_simple=[check_cut(c) for c in sharpened]
    square_cuts=[c for c in json.loads((DATA/'variable_border_cuts_square_learning_v4/cuts.json').read_text()) if c.get('kind')=='integer_residual_square']
    checked_squares=[check_square(c) for c in square_cuts]
    transport={}
    for file in sorted((DATA/'border_transport_v4').glob('*.json')):
        report=json.loads(file.read_text())
        if isinstance(report,dict) and 'stages' in report:transport[file.name]=check_transport(report)
    pairs=check_pair_choices(json.loads((DATA/'variable_border_cuts_v4/triple_exact_witnesses.json').read_text()))
    simple_pairs=check_pair_choices(json.loads((DATA/'variable_border_cuts_v4/triple_exact_simple_factors.json').read_text()))
    result=dict(status='PASS',variable_border_cuts=len(checked),cut_certificates=checked,
                border_transport_certificates=transport,integral_proper_subgroup_witnesses=pairs,
                strengthened_capacity_certificates=checked_simple,integer_square_certificates=checked_squares,
                simple_integral_proper_subgroup_witnesses=simple_pairs,positive_square_fixture=positive_square_fixture(),
                scope='New certificates only; no re-audit of earlier research')
    (DATA/'checks_coexistence_v4.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
