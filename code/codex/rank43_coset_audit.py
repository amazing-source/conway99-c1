"""Exact certificates for nonzero short-vector classes at rank 43."""
from fractions import Fraction as F
from collections import Counter
from itertools import product
import json

import joint_theta_lp_probe as J


def certified_minimum(rows, objective):
    result = J.solver.simplex([f[1:] for _, f in rows], [-f[0] for _, f in rows], objective[1:])
    assert result[0] == 'optimal'
    _, value, multipliers, point = result
    assert all(w >= 0 for w in multipliers)
    identity = [sum(w*f[i] for w, (_, f) in zip(multipliers, rows)) for i in range(len(objective))]
    assert identity[1:] == objective[1:]
    bound = objective[0]-identity[0]
    assert bound == objective[0]+value
    assert all(f[0]+sum(a*b for a, b in zip(f[1:], point)) >= 0 for _, f in rows)
    assert objective[0]+sum(a*b for a, b in zip(objective[1:], point)) == bound
    return {'bound': str(bound), 'point': list(map(str, point)),
            'certificate': [(name, str(w)) for (name, _), w in zip(rows, multipliers) if w],
            'checked_constraints': len(rows)}


def main():
    forms = J.basis(84)
    all_rank_identities = []
    for rank in (35, 37, 39, 41, 43):
        aa, bb = J.family(rank-1, forms)
        m = (45-rank)//2
        constant = 329*(7**m+1)
        coeff_b1 = 7**(m+1)
        check = [2*aa[8][i]+16*aa[9][i]+aa[13][i]-7*aa[7][i]-coeff_b1*bb[1][i]
                 -7*aa[10][i]-2*aa[11][i]-aa[12][i] for i in range(8)]
        assert check == [F(constant)]+[F(0)]*7
        all_rank_identities.append({'rank': rank, 'constant': constant, 'coefficient_b1': coeff_b1})
    a, b, rows = J.system_for_rank(43, forms, J.audited_lows())
    total = [sum(a[n][i] for n in range(8, 14)) for i in range(8)]
    identity = [2*a[8][i]+16*a[9][i]+a[13][i]-7*a[7][i]-49*b[1][i]
                -7*a[10][i]-2*a[11][i]-a[12][i] for i in range(8)]
    assert identity == [F(2632)]+[F(0)]*7
    nonzero = certified_minimum(rows, total)
    assert F(nonzero['bound']) == F(329, 2)
    # Introduce a real variable t bounding all six shell coefficients from above.
    maximum_rows = [(name, list(f)+[F(0)]) for name, f in rows]
    maximum_rows += [(f't>=a{n}', [-x for x in a[n]]+[F(1)]) for n in range(8, 14)]
    maximum = certified_minimum(maximum_rows, [F(0)]*8+[F(1)])
    assert F(maximum['bound']) == F(2632, 19)
    no18 = certified_minimum(rows+[('a9<=0', [-x for x in a[9]])], total)
    assert F(no18['bound']) == F(15756, 7)
    # A mixed feasible point disproves the tempting either/or interpretation.
    fixed18 = list(a[9]); fixed18[0] -= 100
    mixed = certified_minimum(rows+[('a9>=100', fixed18), ('a9<=100', [-x for x in fixed18])], total)
    p = list(map(F, mixed['point']))
    values = {n: a[n][0]+sum(x*y for x, y in zip(a[n][1:], p)) for n in range(7, 14)}
    assert values[9] == 100
    assert sum(values[n] for n in range(8, 14) if n != 9) < 2252
    mixed['a7_through_a13'] = {str(n): str(v) for n, v in values.items()}
    # The anisotropic plane is represented by q(x,y)=x^2+y^2 over F_7.
    distribution = Counter((x*x+y*y) % 7 for x, y in product(range(7), repeat=2))
    assert distribution == {0: 1, **{q: 8 for q in range(1, 7)}}
    pairs = {}
    for norm in (16, 18, 20, 22, 24, 26):
        allowed = [norm-7*k for k in range(1, 8)
                   if 4*norm-14*k >= 14]
        if norm == 16:
            allowed.remove(9)  # note 173 excludes a Fano difference
        if norm == 18:
            allowed.remove(11)  # note 176 extends that exclusion to norm 18
        pairs[str(norm)] = allowed
    report = {'nonzero_short_vectors': nonzero, 'maximum_short_shell': maximum,
              'without_norm18': no18, 'mixed_counterexample_to_either_or': mixed,
              'quadratic_values_in_anisotropic_plane': dict(distribution),
              'pairwise_inner_products_for_same_nonzero_class': pairs,
              'integer_consequences': {'nonzero_vectors_at_least': 166,
                                       'one_shell_at_least': 140, 'one_class_at_least': 18},
              'three_shell_identity': '2a8+16a9+a13=2632+7a7+49b1+7a10+2a11+a12',
              'possible_norms_of_forced_class': [16, 18, 26],
              'all_rank_identity_checks': all_rank_identities,
              'scope': 'Exact LP bounds and finite quadratic-plane check; no exclusion of rank43.'}
    (J.ROOT/'data/codex_rank43_coset_audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v['bound'] for k, v in report.items() if isinstance(v, dict) and 'bound' in v}, indent=2))
    print('Mixed feasible shell counts:', mixed['a7_through_a13'])
    print('Verified: >=166 nonzero vectors, >=140 in a shell, >=18 in one class.')


if __name__ == '__main__':
    main()
