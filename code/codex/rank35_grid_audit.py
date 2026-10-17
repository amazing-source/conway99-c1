"""Exact rank-35 bounds, including the necessary twin-prism correction.

The coefficient -30 is unconditional. Coefficients 84 and 90 are retained
only as explicitly conditional comparisons assuming no twin prisms.
"""
from fractions import Fraction as F
from math import ceil, lcm
import json

import joint_theta_lp_probe as J
from rank43_coset_audit import certified_minimum


def constraints(rank, prism_coefficient, all_sixsets=False):
    a, b, rows0 = J.system_for_rank(rank, J.basis(84), J.audited_lows())
    rows = [(nm, list(f)+[F(0)]*2) for nm, f in rows0]
    def const(c, p=0, rho=0):
        return list(map(F, [c]+[0]*7+[p, rho]))
    for n, low, p, rho in ((3, 66528, 18, 72), (4, 3826746, -prism_coefficient, 4572)):
        f = list(b[n])+[F(p), F(rho)]
        f[0] -= low
        rows.append((f'new_b{n}', f))
    f = [-x for x in b[1]]+[F(0)]*2
    f[0] += 88
    rows += [('b1<=88', f), ('P>=0', const(0, 1)), ('rho>=0', const(0, rho=1)),
             ('P<=1386', const(1386, -1)), ('P>=6rho', const(0, 1, -6))]
    if all_sixsets:
        census = json.loads((J.ROOT/'data/codex_six_vertex_grid_audit.json').read_text())
        losses = {int(q)//2: c for q, c in census['grid']['signed_collisions_by_Q'].items()}
        for n in range(5, 12):
            types = [t for t in census['census']['counts'] if t['edges'] == 11-n]
            low = J.audited_lows()[n]+2*sum(t['constant'] for t in types)
            p = 2*sum(t['prism_coefficient'] for t in types)
            f = list(b[n])+[F(-p), F(losses.get(n, 0))]
            f[0] -= low
            rows.append((f'sixsets_b{n}', f))
    return rows, const


def integer_certificate(result):
    weights = [(name, F(value)) for name, value in result['certificate']]
    denom = lcm(*(w.denominator for _, w in weights))
    return {'objective_multiplier': denom,
            'weights': [(name, int(w*denom)) for name, w in weights],
            'constant': str(F(result['bound'])*denom)}


def main():
    report = []
    for coeff in (-30, 84, 90):
        rows, c = constraints(35, coeff)
        rho = certified_minimum(rows, c(0, rho=1))
        p = certified_minimum(rows, c(0, p=1))
        for result in (rho, p):
            result['integer_lower_bound'] = ceil(F(result['bound']))
            result['integer_certificate'] = integer_certificate(result)
        record = {'rank': 35, 'b4_prism_coefficient': coeff,
                  'assumption': 'none' if coeff == -30 else 'no twin prisms',
                  'rho_minimum': rho, 'P_minimum': p,
                  'rows': [(nm, list(map(str, f))) for nm, f in rows]}
        report.append(record)
        print(record['assumption'], ': b4 coefficient', coeff, 'rho >=', rho['bound'], '=>', rho['integer_lower_bound'],
              'P >=', p['bound'], '=>', p['integer_lower_bound'], flush=True)
        print('rho certificate:', rho['integer_certificate'], flush=True)
    rows, c = constraints(37, -30)
    result = certified_minimum(rows, c(0, rho=1))
    report.append({'rank': 37, 'b4_prism_coefficient': -30, 'rho_minimum': result})
    print('rank37 rho >=', result['bound'], flush=True)
    for rank in (35, 37):
        rows, c = constraints(rank, -30, all_sixsets=True)
        result = certified_minimum(rows, c(0, rho=1))
        p = certified_minimum(rows, c(0, p=1))
        report.append({'rank': rank, 'all_sixsets': True, 'rho_minimum': result,
                       'P_minimum': p})
        print('all sixsets rank', rank, 'rho >=', result['bound'], 'P >=', p['bound'], flush=True)
    rows, c = constraints(35, -30, all_sixsets=True)
    by_name = dict(rows)
    weights = {'a8>=0': 9191, 'a10>=0': 43, 'a11>=0': 11,
               'b2>=462': 1555, '7a7+8a8<=55440': 1300,
               'new_b3': 651, 'new_b4': 34, 'b1<=88': 135344}
    identity = [sum(weight*by_name[name][i] for name, weight in weights.items()) for i in range(10)]
    assert identity == [-20783998]+[0]*7+[12738, 202320]
    integer_pairs = [(p, rho) for p in range(1387) for rho in range(p//6+1)
                     if 101160*rho+6369*p >= 10391999]
    assert min(p for p, _ in integer_pairs) == 450
    assert min(rho for _, rho in integer_pairs) == 16
    # This checks the full rational relaxation at the smallest integer P,
    # while imposing integrality only on the two subgraph counts.
    fixed = rows + [('P>=450', c(-450, p=1)), ('P<=450', c(450, p=-1)),
                    ('rho>=75', c(-75, rho=1)), ('rho<=75', c(75, rho=-1))]
    result = certified_minimum(fixed, c(0))
    report.append({'rank': 35, 'tradeoff_integer_certificate': weights,
                   'weighted_identity': list(map(str, identity)),
                   'integer_P_rho_constraints': '101160*rho+6369*P>=10391999; 0<=6*rho<=P<=1386',
                   'minimum_integer_P': 450, 'minimum_integer_rho': 16,
                   'full_rational_relaxation_at_P450_rho75': result})
    print('Unconditional integer consequences: rho>=16, P>=450; rational relaxation feasible at (450,75).', flush=True)
    # Retain the twin-pair variable instead of replacing it by 5P/2.
    base, _ = constraints(35, 90, all_sixsets=True)
    rows_t = [(nm, list(f)+[F(48 if nm == 'new_b4' else 0)]) for nm, f in base]
    def tform(c=0, p=0, rho=0, tau=0):
        return list(map(F, [c]+[0]*7+[p, rho, tau]))
    rows_t += [('tau>=0', tform(tau=1)), ('2tau<=5P', tform(p=5, tau=-2)),
               ('tau>=6rho-231', tform(c=231, rho=-6, tau=1))]
    tau_min = certified_minimum(rows_t, tform(tau=1))
    by_name = dict(rows_t)
    identity_t = [sum(weight*by_name[name][i] for name, weight in weights.items()) for i in range(11)]
    assert identity_t == [-20783998]+[0]*7+[8658, 202320, 1632]
    # For fixed tau the left side is maximal at P=1386 and at the largest
    # rho permitted by the shared-triangle bound. No theta assumptions here.
    least_tau = next(tau for tau in range(3466)
                     if 101160*min(231, (tau+231)//6)+4329*1386+816*tau >= 10391999)
    assert least_tau == 33
    fixed_t = rows_t + [('P>=1386', tform(c=-1386, p=1)),
                        ('rho>=44', tform(c=-44, rho=1)), ('rho<=44', tform(c=44, rho=-1)),
                        ('tau>=33', tform(c=-33, tau=1)), ('tau<=33', tform(c=33, tau=-1))]
    witness = certified_minimum(fixed_t, tform())
    report.append({'rank': 35, 'twin_pair_minimum': tau_min, 'integer_tau_at_least': least_tau,
                   'weighted_identity': list(map(str, identity_t)),
                   'full_rational_relaxation_at_P1386_rho44_tau33': witness,
                   'rows': [(nm, list(map(str, f))) for nm, f in rows_t]})
    print('Twin pairs: tau >=', tau_min['bound'], '; integer consequence tau>=33.', flush=True)
    (J.ROOT/'data/codex_rank35_grid_audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
