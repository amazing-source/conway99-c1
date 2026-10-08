"""Exact rank-37 theta inequality retaining the Fano census parameter."""
from fractions import Fraction as F
import argparse
import json


def main(verify_only=False):
    import joint_theta_lp_probe as J
    a, b = J.family(36, J.basis(84))
    def affine(constant=0, terms=()):
        result = [F(constant)]+[F(0)]*7
        for factor, form in terms:
            result = [x+F(factor)*y for x, y in zip(result, form)]
        return result
    rows = {
        'a10>=0': a[10],
        'a11>=0': a[11],
        '7a7+8a8<=55440': affine(55440, [(-7,a[7]),(-8,a[8])]),
        'b1<=44': affine(44, [(-1,b[1])]),
        'root_norm4_secant_21': affine(462, [(1,b[2]),(-84,b[1])]),
    }
    weights = {
        'a10>=0': F(301,34),
        'a11>=0': F(77,34),
        '7a7+8a8<=55440': F(8463,272),
        'b1<=44': F(2362,17),
        'root_norm4_secant_21': F(1555,34),
    }
    total = [sum(weight*rows[name][i] for name, weight in weights.items()) for i in range(8)]
    price = F(450359,272); base = F(15457549); b3price = F(651,34)
    expected = affine(base, [(price,a[7]),(-1,b[4]),(-b3price,b[3])])
    assert total == expected and all(weight >= 0 for weight in weights.values())
    coupling = json.loads((J.ROOT/'data/codex_fano_grid_coupling_rho125.json').read_text())
    assert F(coupling['rho_coefficient']) == F(273,2)
    assert F(coupling['constant']) == F(42273,2)
    assert F(2,21)*F(coupling['rho_coefficient']) == 13
    assert F(2,21)*F(coupling['constant']) == 2013
    report = {
        'rank': 37, 'q_precision': 84,
        'identity': '15457549+(450359/272)a7-b4-(651/34)b3=sum(weight*nonnegative_row)',
        'row_weights': {name: str(weight) for name, weight in weights.items()},
        'verified_identity_coefficients': list(map(str,total)),
        'F10_coefficient_after_coupling': str(price*F(2,21)),
        'uniform_Fano_grid_cut': 'a7+13rho<=2013',
        'stronger_Fano_prism_grid_cut': '14a7+25P+32rho<=28182',
        'uniform_theta_grid_cut': '272b4+5208b3+5854667rho<=5111025995',
        'conditional_cases': {},
        'scope': 'Exact theta upper bound coupled to F10; conditional cases are not unconditional rank exclusions.'}
    assert 272*b3price == 5208 and 272*price*13 == 5854667
    assert 272*(base+2013*price) == 5111025995
    for rho in (125,126):
        suffix = '' if rho == 126 else f'_rho{rho}'
        source = json.loads((J.ROOT/f'data/codex_fano_grid_coupling{suffix}.json').read_text())
        assert source['conditional_rho'] == rho
        upper = F(source['conditional_F10_upper_bound'])
        a7cap = min(842, int(2*(upper//21)))
        b4cap = base+price*a7cap-b3price*45898
        report['conditional_cases'][str(rho)] = {
            'F10_upper_bound': str(upper), 'a7_even_upper_bound': a7cap,
            'unoriented_Fano_upper_bound': a7cap//2,
            'b4_rational_upper_bound': str(b4cap),
            'b4_even_upper_bound': int(2*(b4cap//2)),
        }
        print('rho',rho,report['conditional_cases'][str(rho)],flush=True)
    path = J.ROOT/'data/codex_fano_grid_theta_link.json'
    if verify_only:
        assert json.loads(path.read_text()) == report
    else:
        path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Verified all eight theta coefficients and five nonnegative weights.',flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--verify-only',action='store_true')
    args = parser.parse_args()
    main(args.verify_only)
