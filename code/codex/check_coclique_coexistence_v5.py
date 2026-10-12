"""Independent integer checks for V5; no search/separator/solver imports."""
from pathlib import Path
from itertools import combinations, product
import json

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'data/codex_coclique_defects'


def read(source):
    w=json.loads((ROOT/source).read_text());a=[set() for _ in range(w['vertices'])]
    for u,v in w['edges']:
        assert u!=v and v not in a[u];a[u].add(v);a[v].add(u)
    return w,a


def saturated(a,u,v):return len(a[u]&a[v])==2-int(v in a[u])


def multiplicity(w,a,row):
    i,j=row;m=2-int(j in a[i])-len(a[i]&a[j])
    assert m in (0,1,2)
    assert m==next((t['count'] for t in w['remaining_population'] if tuple(t['vertices'])==row),0)
    return m


def factors(w,a):
    y={(t['vertex'],tuple(t['type'])):t['count'] for t in w['factors']}
    assert all(value==1 for value in y.values())
    for u in range(18,len(a)):
        rows=[row for (v,row) in y if v==u]
        assert len(rows)==14-len(a[u])
        for i in range(4,16):assert sum(i in row for row in rows)==2-int(i in a[u])-len(a[u]&a[i])
        for row in rows:
            assert multiplicity(w,a,row)>0
            assert int(row[0] in a[u])+int(row[1] in a[u])+int(row[1] in a[row[0]])<=1
    return y


def check_cycle(c):
    w,a=read(c['source']);row=tuple(c['type']);m=multiplicity(w,a,row);cycle=c['cycle']
    assert len(set(cycle))==len(cycle) and (len(cycle)==2 or len(cycle)%2==1)
    assert all(saturated(a,u,v) for u,v in zip(cycle,cycle[1:]+cycle[:1]))
    y={(t['vertex'],tuple(t['type'])):t['count'] for t in w['factors']}
    left=sum(y.get((u,row),0) for u in cycle);upper=(len(cycle)//2)*m
    assert left>upper and (left,upper)==(c['separation']['left'],c['separation']['upper'])
    return dict(type=row,length=len(cycle),left=left,upper=upper,source=c['source'])


def check_square(c):
    w,a=read(c['source']);weights=c['weights'];q=sum(z*z*(14-len(a[u])) for u,z in weights)
    for (u,z),(v,t) in combinations(weights,2):q+=2*z*t*(2-int(v in a[u])-len(a[u]&a[v]))
    total=sum(z*(14-len(a[u])) for u,z in weights);k=c['integer_level'];bound=(2*k+1)*total-(99-len(a))*k*(k+1)
    assert q<bound and (q,total,bound)==(c['separation']['quadratic'],c['separation']['sum_loads'],c['separation']['lower_bound'])
    return dict(source=c['source'],quadratic=q,lower_bound=bound)


def colour_witness(vertices,a,closed=None,quota=None):
    for colours in product((0,1),repeat=len(vertices)):
        mapping=dict(zip(vertices,colours))
        if any(mapping[u]==mapping[v] and saturated(a,u,v) for u,v in combinations(vertices,2)):continue
        if closed is not None and any(sum(u in a[closed] and mapping[u]==c for u in vertices)>quota for c in (0,1)):continue
        return [[u,mapping[u]] for u in vertices]
    return None


def proper_witnesses(vertices,a,closed=None,quota=None):
    assert colour_witness(vertices,a,closed,quota) is None
    result=[]
    for size in range(1,len(vertices)):
        for group in combinations(vertices,size):
            colours=colour_witness(group,a,closed,quota);assert colours is not None
            result.append(dict(vertices=group,colours=colours))
    return result


def check_star(c):
    w,a=read(c['source']);row=tuple(c['type']);m=multiplicity(w,a,row)
    u=c['center'];leaves=c['leaves'];s=c['closed_vertex'];q=c['quota'];group=[u]+leaves
    assert len(a[s])==14 and 2-len(a[s]&set(row))<=q
    assert len(set(group))==q+2 and len(leaves)==q+1 and m<=2
    assert all(v in a[s] and saturated(a,u,v) for v in leaves)
    assert all(not saturated(a,v,t) for v,t in combinations(leaves,2))
    y={(t['vertex'],tuple(t['type'])):t['count'] for t in w['factors']}
    left=sum(y.get((v,row),0) for v in group);assert left==len(group)>len(leaves)
    assert colour_witness(group,a) is not None
    proper=proper_witnesses(group,a,s,q)
    return dict(source=c['source'],type=row,closed_vertex=s,center=u,leaves=leaves,quota=q,
                bipartite=True,forced_same_copy=len(leaves),capacity=q,proper_group_witnesses=proper)


def closed_identities(w,a):
    identities=[]
    y={(t['vertex'],tuple(t['type'])):t['count'] for t in w['factors']}
    for s in (0,1,2,3,16,17):
        assert len(a[s])==14
        weights=sorted(a[s]);total=sum(14-len(a[u]) for u in weights)
        q=total+2*sum(2-int(v in a[u])-len(a[u]&a[v]) for u,v in combinations(weights,2))
        assert (total,q)==(2*(99-len(a)),4*(99-len(a)))
        if w.get('closed_star_balances'):
            for t in w['remaining_population']:
                row=tuple(t['vertices']);m=t['count']
                assert sum(y.get((u,row),0) for u in range(18,len(a)) if u in a[s])==m*(2-len(a[s]&set(row)))
        identities.append(dict(vertex=s,total=total,squares=q,variance=0))
    return identities


def positive_fixture():
    a=[{v for v in range(9) if u!=v and (u//3==v//3 or u%3==v%3)} for u in range(9)]
    B=[0]+sorted(a[0]);R=sorted(set(range(9))-set(B));s=0
    loads=[len(a[t]&a[s]) for t in R];assert loads==[2]*len(R)
    assert sum(loads)==2*len(R) and sum(c*c for c in loads)==4*len(R)
    equality_cases=0
    for z in product((-1,0,1),repeat=len(B)):
        c=[sum(v for u,v in zip(B,z) if u in a[t]) for t in R]
        total=sum(c);q=sum(v*v for v in c)
        for k in range(-2,3):
            if q==(2*k+1)*total-len(R)*k*(k+1):
                assert all(v in (k,k+1) for v in c);equality_cases+=1
    return dict(graph='3x3 rook',complete_star=s,missing_copy_loads=loads,integer_equality_cases=equality_cases)


def main():
    path=DATA/'copy_star_learning_v5/cuts.json';cuts=json.loads(path.read_text())
    new=[c for c in cuts if '_v5' in c.get('source','')]
    cycles=[check_cycle(c) for c in new if c['kind']=='copy_cycle_capacity']
    squares=[check_square(c) for c in new if c['kind']=='integer_residual_square']
    stars=[check_star(c) for c in new if c['kind']=='copy_closed_star_capacity']
    sources=sorted({c['source'] for c in new});checked_sources=[]
    for source in sources:
        w,a=read(source);factors(w,a)
        checked_sources.append(dict(source=source,closed_balances=w.get('closed_star_balances',False),identities=closed_identities(w,a)))
    examples=json.loads((DATA/'copy_sharing_light_v5/chordless_odd_cycles.json').read_text())
    w,a=read(examples['source']);proper=[]
    for proof in examples['proofs']:
        cycle=proof['cycle'];assert sum(saturated(a,u,v) for u,v in combinations(cycle,2))==len(cycle)
        assert multiplicity(w,a,tuple(proof['type']))==2
        proper.append(dict(type=proof['type'],cycle=cycle,proper_group_witnesses=proper_witnesses(cycle,a)))
    force=json.loads((DATA/'copy_sharing_light_v5/forced_double_types.json').read_text());forcing_count=0
    w,a=read(force['source'])
    m={tuple(t['vertices']):t['count'] for t in w['remaining_population']}
    for item in force['forced']:
        target=tuple(item['type'])
        for f in item['users']:
            u=f['vertex'];beta=f['prices'];required=sum(beta[i-4]*(2-int(i in a[u])-len(a[u]&a[i])) for i in range(4,16));bound=0
            for row in m:
                if row==target or len(a[u])==14:continue
                if any(2-int(i in a[u])-len(a[u]&a[i])==0 for i in row):continue
                if int(row[0] in a[u])+int(row[1] in a[u])+int(row[1] in a[row[0]])>1:continue
                bound+=max(0,sum(beta[i-4] for i in row))
            assert required>bound and (required,bound)==(f['required'],f['other_upper']);forcing_count+=1
    result=dict(status='PASS',scope='Only new V5 certificates and allocations; no independent CP-SAT UNSAT proof claimed',
                cycle_cuts=len(cycles),new_square_cuts=len(squares),closed_star_cuts=len(stars),
                cycles=cycles,squares=squares,stars=stars,sources=checked_sources,
                chordless_cycle_examples=proper,local_forcing_certificates=forcing_count,positive_equality_fixture=positive_fixture())
    (DATA/'checks_coexistence_v5.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cycles','squares','stars','sources','chordless_cycle_examples')}))


if __name__=='__main__':main()
