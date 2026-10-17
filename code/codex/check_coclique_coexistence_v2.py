"""Short independent checks of the NEW reductions and arithmetic certificates."""
from pathlib import Path
from itertools import combinations
import json
import time

BASE=Path(__file__).resolve().parents[2]
DATA=BASE/'data/codex_coclique_defects'


def check_local_choices(core,population,report):
    rows=[];inc=[]
    for item in population['selected_rows']:
        for k in range(item['count']):rows.append(set(item['vertices']));inc.append(k<item['coclique_count'])
    neighbours=[set() for _ in core['charges']]
    for i,j in core['edges']:neighbours[i].add(j);neighbours[j].add(i)
    verified=0
    for item in report['results']:
        if item['status'] not in ('OPTIMAL','FEASIBLE'):continue
        z=item['vertex'];choice=item['neighbours'];assert z not in choice and len(choice)==len(set(choice))
        assert len(choice)==core['parameters']['degree']-len(rows[z])
        assert sum(inc[w] for w in choice)==(0 if inc[z] else 4)
        assert all(len(rows[z]&rows[w])<=1 for w in choice)
        for i in range(len(neighbours)):
            assert sum(i in rows[w] for w in choice)==2-int(i in rows[z])-len(neighbours[i]&rows[z])
        verified+=1
    assert verified==report['feasible']
    return verified==len(rows)


def check_cut(core,population,cut):
    from coclique_defect_gluing import gluing_data
    data=gluing_data(core);rows=data['rows'];n=len(core['charges']);lookup={r:t for t,r in enumerate(rows)}
    h=[[2-int(r>>i&1)-(r&m).bit_count() for i,m in enumerate(data['neighbours'])] for r in rows]
    zeros=[sum(1<<i for i,v in enumerate(hh) if v==0) for hh in h]
    def allowed(t,u):return (rows[t]&rows[u]).bit_count()<=1 and not(rows[t]&zeros[u] or rows[u]&zeros[t])
    counts=[0]*(2*len(rows))
    for item in population['selected_rows']:
        t=lookup[sum(1<<i for i in item['vertices'])]
        counts[2*t]=item['coclique_count'];counts[2*t+1]=item['count']-item['coclique_count']
    if cut['kind']=='conditional_cover':
        t=lookup[sum(1<<i for i in cut['root'])];a=2*t+int(not cut['in_coclique']);w=cut['weights']
        assert counts[a]>=1
        left=w[0]*(14-rows[t].bit_count())+w[1]*(4 if a%2 else 0)+sum(w[2+i]*h[t][i] for i in range(n));right=0
        for b,p in enumerate(counts):
            if not(a%2 or b%2) or not allowed(t,b//2):continue
            k=max(0,w[0]+(w[1] if b%2==0 else 0)+sum(w[2+i] for i in range(n) if rows[b//2]>>i&1))
            right+=k*(p-int(a==b))
        assert left>right
    else:
        weights={int(a):w for a,w in cut['weights'].items()};zero=[0]*(n+2);left=right=0
        for a,w in weights.items():
            t=a//2;left+=counts[a]*(w[0]*(14-rows[t].bit_count())+w[1]*(4 if a%2 else 0)+sum(w[2+i]*h[t][i] for i in range(n)))
        selected=[a for a,p in enumerate(counts) if p]
        for index,a in enumerate(selected):
            for b in selected[index:]:
                if not(a%2 or b%2) or not allowed(a//2,b//2):continue
                wa,wb=weights.get(a,zero),weights.get(b,zero)
                k=wa[0]+wb[0]+(wa[1] if b%2==0 else 0)+(wb[1] if a%2==0 else 0)
                k+=sum(wa[2+i] for i in range(n) if rows[b//2]>>i&1)+sum(wb[2+i] for i in range(n) if rows[a//2]>>i&1)
                right+=max(0,k)*(counts[a]*(counts[a]-1)//2 if a==b else counts[a]*counts[b])
        assert left==cut['observed_left'] and right==cut['observed_right'] and left>right
    return dict(left=left,right=right,kind=cut['kind'])


def check_certificate(core,population,proof):
    neighbours=[set() for _ in core['charges']]
    for i,j in core['edges']:neighbours[i].add(j);neighbours[j].add(i)
    rows=[];inc=[]
    for item in population['selected_rows']:
        for k in range(item['count']):rows.append(set(item['vertices']));inc.append(k<item['coclique_count'])
    n=len(rows);s=len(neighbours)
    need=[[2-int(i in r)-len(neighbours[i]&r) for i in range(s)] for r in rows]
    weights={};left=0
    for term in proof['coefficients']:
        reason=term['reason'];z=reason[1];coefficient=term['coefficient']
        if reason[0]=='degree':rhs=core['parameters']['degree']-len(rows[z])
        elif reason[0]=='coclique_degree':
            assert not inc[z];rhs=4 if core['parameters']['degree']==14 else 2
        else:assert reason[0]=='common_with_core';rhs=need[z][reason[2]]
        assert rhs==term['rhs'];left+=rhs*coefficient
        for w in range(n):
            if w==z or (inc[z] and inc[w]) or len(rows[z]&rows[w])>=2:continue
            if proof.get('prune_incompatible',False):
                if any(need[z][i]==0 for i in rows[w]) or any(need[w][i]==0 for i in rows[z]):continue
            participates=(reason[0]=='degree' or (reason[0]=='coclique_degree' and inc[w]) or
                          (reason[0]=='common_with_core' and reason[2] in rows[w]))
            if participates:
                e=tuple(sorted((z,w)));weights[e]=weights.get(e,0)+coefficient
    bound=sum(max(0,v) for v in weights.values())
    assert left>bound
    assert left==proof['verification']['left'] and bound==proof['verification']['upper_bound']
    expected={tuple(item['edge']):item['weight'] for item in proof['verification']['edge_weights']}
    assert {e:w for e,w in weights.items() if w}==expected
    return dict(left=left,right=bound,equations=len(proof['coefficients']))


def h_cycle_reduction():
    pairs=list(combinations(range(4),2));survivors=[]
    for mask in range(1<<len(pairs)):
        adj=[set() for _ in range(4)]
        for k,(i,j) in enumerate(pairs):
            if mask>>k&1:adj[i].add(j);adj[j].add(i)
        p=mask.bit_count()
        if not 2<=p<=4:continue
        if any(len(adj[i]&adj[j])>2-int(j in adj[i]) for i,j in pairs):continue
        budget=12-p-sum(len(a)*(len(a)-1)//2 for a in adj)
        if budget<20-4*p:continue
        assert p==4 and all(len(a)==2 for a in adj)
        survivors.append(mask)
    assert len(survivors)==3
    return dict(labelled_C4=3)


def negative_density():
    maxima={}
    for n in (5,6):
        pairs=list(combinations(range(n),2));best=0
        for mask in range(1<<len(pairs)):
            adj=[0]*n
            for k,(i,j) in enumerate(pairs):
                if mask>>k&1:adj[i]|=1<<j;adj[j]|=1<<i
            if any(x==0 for x in adj):continue
            if any((adj[i]&adj[j]).bit_count()>2-int(adj[i]>>j&1) for i,j in pairs):continue
            budget=n*(n-1)-mask.bit_count()-sum(x.bit_count()*(x.bit_count()-1)//2 for x in adj)
            if budget<5*n-21:continue
            best=max(best,mask.bit_count())
        maxima[n]=best
    assert maxima=={5:6,6:7}
    return maxima


def main():
    start=time.monotonic();core=json.loads((DATA/'core_a0_e2.json').read_text())
    verified={};cuts={};strict_coexistence=[]
    for p in DATA.glob('*_farkas_sparse*.json'):
        proof=json.loads(p.read_text())
        if proof['status']!='EXACT_CONTRADICTION':continue
        prefix=p.name.split('_farkas')[0]
        population=json.loads((DATA/(prefix+'.json')).read_text())
        verified[p.name]=check_certificate(core,population,proof)
    for folder in sorted(DATA.glob('learned_cuts_e2_*')):
        for p in sorted(folder.glob('certificate_*.json')):
            proof=json.loads(p.read_text())
            if proof['status']!='EXACT_CONTRADICTION':continue
            population=json.loads(p.with_name(p.name.replace('certificate_','population_')).read_text())
            verified[f'{folder.name}/{p.name}']=check_certificate(core,population,proof)
            cut_path=p.with_name(p.name.replace('certificate_','cut_'))
            if cut_path.exists():cuts[f'{folder.name}/{cut_path.name}']=check_cut(core,population,json.loads(cut_path.read_text()))
            local_path=p.with_name(p.name.replace('certificate_','local_choices_'))
            if local_path.exists() and check_local_choices(core,population,json.loads(local_path.read_text())):
                strict_coexistence.append(f'{folder.name}/{p.name}')
    from coclique_defect_cut_loop import Master
    from ortools.sat.python import cp_model
    grid=json.loads((DATA/'grid9_positive_control.json').read_text())
    master=Master(grid,9,2);solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    assert solver.Solve(master.model) in (cp_model.OPTIMAL,cp_model.FEASIBLE)
    # Feasible full SRG control must not have any real LP separator.
    from coclique_completion_certificate import certificate
    population=json.loads((DATA/'grid9_positive_control_triangles.json').read_text())
    control=certificate(grid,population,10,sparse=True,prune_incompatible=True)
    assert control['status']=='NO_CERTIFICATE' and control['lp_status']==2
    result=dict(status='PASS',h_cycle=h_cycle_reduction(),negative_density=negative_density(),
                exact_certificates=verified,learned_family_cuts=cuts,all_local_choices_feasible_but_no_reciprocal_completion=strict_coexistence,
                grid9_master='FEASIBLE',grid9_separator='NONE',seconds=time.monotonic()-start)
    (DATA/'checks_coexistence_v2.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],certificates=len(verified),family_cuts=len(cuts),strict_coexistence=len(strict_coexistence),seconds=result['seconds'])),flush=True)


if __name__=='__main__':main()
