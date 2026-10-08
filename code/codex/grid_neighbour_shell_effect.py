"""Exact shell/theta consequences of the neighbour-moment twin cap 1403."""
from fractions import Fraction as F
import json
import sys

from higher_census_minima import ROOT,certify
from grid_class_bounds import systems,verify
import joint_theta_lp_probe as J
from rank43_coset_audit import certified_minimum


def shell(verify_only):
    source,_,rows = systems()
    width = len(source['parameters'])+1
    rows += [('neighbour_moments_tau<=1403',
              [F(1403)]+[F(0)]*(width-1)+[F(-1),F(0)])]
    objective = [F(0)]*(width+1)+[F(1)]
    path = ROOT/'data/codex_neighbour_moment_b3_bound.json'
    if verify_only: proof = json.loads(path.read_text())
    else:
        proof = certify(rows,objective)
        proof.update(objective=list(map(str,objective)),tau_cap=1403,
                     b3_even_floor=int(-2*((-F(proof['lower_bound']))//2)))
        path.write_text(json.dumps(proof,indent=2)+'\n')
    verify(rows,objective,proof)
    assert F(proof['lower_bound']) == F(137692,3)
    assert proof['tau_cap'] == 1403 and proof['b3_even_floor'] == 45898
    print('Verified b3>=137692/3, hence b3>=45898',flush=True)


def theta(verify_only):
    old = json.loads((ROOT/'data/codex_rank37_dual_frontier_order9_far_triangles.json').read_text())
    a,b = J.family(36,J.basis(84))
    rows = [(name,list(map(F,row))) for name,row in old['base_rows']
            if name not in ('a7<=990','b1<=88')]
    for name,row,constant in [('a7<=842',[-v for v in a[7]],842),
                              ('b1<=44',[-v for v in b[1]],44),
                              ('neighbour_moment_b3>=45898',list(b[3]),-45898)]:
        row[0] += constant
        rows.append((name,row+[F(0)]*2))
    for j in range(22):
        row = [x-(42+2*j)*y for x,y in zip(b[2],b[1])]
        row[0] -= 462-2*j*(j+1)
        rows.append((f'root_norm4_secant_{j}',row+[F(0)]*2))
    objectives = {'b4':[-v for v in b[4]]+[F(0)]*2,
                  'b4+(651/34)b3':[-x-F(651,34)*y for x,y in zip(b[4],b[3])]+[F(0)]*2}
    path = ROOT/'data/codex_neighbour_moment_theta_effect.json'
    report = json.loads(path.read_text()) if verify_only else {
        'rank':37,'a7_cap':842,'b1_cap':44,'b3_floor':45898,'q_precision':84,'cases':{},
        'scope':'Exact theta relaxation with neighbour-moment b3 floor; no rank37 exclusion.'}
    lookup = dict(rows)
    for name,objective in objectives.items():
        proof = report['cases'][name] if verify_only else certified_minimum(rows,objective)
        total = [F(0)]*len(objective)
        for label,w in proof['certificate']:
            w = F(w); assert w>=0
            total = [x+w*y for x,y in zip(total,lookup[label])]
        assert total[1:] == objective[1:] and objective[0]-total[0] == F(proof['bound'])
        point = list(map(F,proof['point']))
        assert all(row[0]+sum(x*y for x,y in zip(row[1:],point))>=0 for _,row in rows)
        assert objective[0]+sum(x*y for x,y in zip(objective[1:],point)) == F(proof['bound'])
        if not verify_only: report['cases'][name] = proof
        print('Verified',name,'<=',-F(proof['bound']),float(-F(proof['bound'])),flush=True)
    if not verify_only: path.write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    verify_only = '--verify-only' in sys.argv
    shell(verify_only)
    theta(verify_only)
