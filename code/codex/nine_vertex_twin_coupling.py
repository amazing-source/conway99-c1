"""Exact coupling 8*tau <= N4 and conditional raw-family loss thresholds.

The coefficients of tau below are exploratory penalties, not asserted
collision counts for the (6,3) family.
"""
from fractions import Fraction as F
import json

from higher_census_minima import ROOT, certify


def main():
    source = json.loads((ROOT/'data/codex_order9_census.json').read_text())
    raw = json.loads((ROOT/'data/codex_order9_raw_family_minima.json').read_text())
    rows = [(str(r['code']), list(map(F, r['affine']))) for r in source['counts']]
    width = len(source['parameters'])+1
    P = [F(0), F(1)]+[F(0)]*(width-2)
    rho = dict(rows)['13262907120']
    N4 = list(map(F, raw['Q4_edges9_3_cross0']['objective']))
    objective = [-x for x in N4]
    result = certify(rows, objective)
    result['objective'] = list(map(str, objective))
    report = {'N4_maximum': str(-F(result['lower_bound'])), 'N4_certificate': result}
    print('N4 <=', report['N4_maximum'], flush=True)
    augmented = [(name, row+[F(0)]) for name, row in rows]
    augmented += [('tau>=0', [F(0)]*width+[F(1)]),
                  ('2tau<=5P', [5*x for x in P]+[F(-2)]),
                  ('tau<=2P+3rho', [2*x+3*y for x, y in zip(P, rho)]+[F(-1)]),
                  ('8tau<=N4', N4+[F(-8)])]
    objective = [F(0)]*width+[F(-1)]
    twin_cap = certify(augmented, objective)
    twin_cap['objective'] = list(map(str, objective))
    report['tau_maximum'] = str(-F(twin_cap['lower_bound']))
    report['tau_certificate'] = twin_cap
    print('tau <=', report['tau_maximum'], flush=True)
    report['joint_raw_penalties'] = {}
    N6 = list(map(F, raw['Q6_TOTAL']['objective']))
    N8 = list(map(F, raw['Q8_TOTAL']['objective']))
    for c in (0, 48, 480, 1000, 2794):
        objective = [x+F(651, 34)*y for x, y in zip(N8, N6)]+[F(-c)]
        result = certify(augmented, objective)
        result['objective'] = list(map(str, objective))
        report['joint_raw_penalties'][str(c)] = result
        print('N8+(651/34)N6-', c, 'tau >=', result['lower_bound'], flush=True)
    report['scope'] = 'Tau coupling is proved; penalty coefficients are conditional exploration only, not new theta bounds.'
    (ROOT/'data/codex_nine_vertex_twin_coupling.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
