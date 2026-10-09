"""Exact coefficients for note 242: harmonic degree two and root budget.

Standard library only. One positive-lattice control fixes the Fricke sign
and scale. No previous scalar/class theta programs or graph searches run.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

from theta7_audit import eta_product, multiply, power, e4, theta_h7, dilate7


def forms(n):
    return {j: ([0] * (14-j) + eta_product(n, 4*j, 48-4*j))[:n+1]
            for j in range(-1, 14)}


def coordinates(series, fs):
    remaining = list(series)
    answer = {}
    for j in range(13, -2, -1):
        answer[j] = remaining[14-j]
        remaining = [a-answer[j]*b for a, b in zip(remaining, fs[j])]
    assert not any(remaining), 'Residual beyond the interpolation range'
    return answer


def control(fs, n):
    # K=E8^5 orthogonal sum H7^2, determinant 7^2, dimension 44.
    # S=I_40/40 orthogonal sum -I_4/4 is traceless. H7 is 7-modular;
    # the dual isometry on that block preserves this polynomial.
    h = power(theta_h7(n), 2)
    e = power(e4(n), 5)

    def derivative(a):
        return [2*i*x for i, x in enumerate(a)]

    def weighted(a):
        first = multiply(derivative(a), h)
        second = multiply(a, derivative(h))
        return [Q(x, 40)-Q(y, 4) for x, y in zip(first, second)]

    cs = coordinates(weighted(e), fs)
    ds = coordinates(weighted(dilate7(e)), fs)
    predicted = {i: -Q(7)**(2-2*i)*cs[12-i] for i in fs}
    assert ds == predicted
    return {'lattice': 'E8^5 + H7^2', 'alpha': 2,
            'q_precision': n, 'sign_and_scale': 'passed',
            'coordinates': {j: str(v) for j, v in cs.items()},
            'dual_coordinates': {j: str(v) for j, v in ds.items()}}


def symbolic_relation(fs):
    # Variables R=D_M,1, H8..H12=D_L,8..12, X=D_L,13, D=D_M,2.
    names = ['R', 'H8', 'H9', 'H10', 'H11', 'H12', 'X', 'D']
    zero = (0,)*len(names)

    def unit(i, value=1):
        return tuple(value if i == j else 0 for j in range(len(names)))

    targets = {7: unit(0, 7), 13: unit(6), 14: unit(7, 7)}
    targets.update({i: unit(i-7) for i in range(8, 13)})
    cs = {j: zero for j in fs}
    for degree in range(7, 15):
        cs[14-degree] = tuple(targets[degree][i] - sum(
            cs[j][i]*fs[j][degree] for j in range(15-degree, 8))
            for i in range(len(names)))
    # Fricke: c_-1=-7^4 R and D=-52R-c0/49.
    correction = (2548, 0, 0, 0, 0, 0, 0, 49)
    coefficients = tuple(Q(a+b, 4) for a, b in zip(cs[0], correction))
    assert coefficients == (728, 12, 6, 7, 4, 3, 1, 14)
    return dict(zip(names, map(int, coefficients)))


def main():
    n = 32
    fs = forms(n)
    checked_control = control(fs, n)
    relation = symbolic_relation(fs)
    # Trace of the tensor identity, using the established scalar identities.
    scalar_weights = [Q(26*a + extra + 56*b, 44)
                      for a, extra, b in zip(
                          [-2, -16, 7, 2, 1],
                          [12*16, 6*18, 7*20, 4*22, 3*24],
                          [25, 11, 8, 3, 1])]
    assert scalar_weights == [35, 7, Q(35, 2), 7, Q(7, 2)]
    assert Q(26*2632+56*1000, 44) == 2828
    assert Q(26*112-56*16+728*4, 44) == 112
    # Along any root, U=4 and V>=84+8(k-1).
    gap = 728*4+14*(84-8)-2828
    assert gap == 1148 and Q(gap, Q(7, 2)) == 328
    budget = [int(w/Q(7, 2)) for w in scalar_weights]
    assert budget == [10, 2, 5, 2, 1]
    # In the rootless gap branch, all full-layer traceless moments are
    # multiples of D_M,2. This does not make individual classes isotropic.
    l_series = [-14*a-49*b for a, b in zip(fs[1], fs[0])]
    m_series = [a+14*b for a, b in zip(fs[12], fs[11])]
    assert l_series[13:15] == [-14, 7]
    assert m_series[2:7] == [1, -34, 464, -2412, -15108]
    assert Q(26*2632+14*4*1000, 44)-14*42 == 2240
    assert Q(6*10648712+34*4*1000, 44)-34*42 == 1453760
    report = {
        'scope': 'Rank43: any root forces the short-layer budget; '
                 'no norms16..24 therefore forces no roots. '
                 'The rootless branch and rank43 remain open.',
        'harmonic_relation_equals_zero': relation,
        'full_tensor_scalar': {'constant': 2828, 'k': 112,
                              'a8_through_a12': list(map(str, scalar_weights))},
        'root_budget': {'a8_through_a12': budget, 'minimum': 328,
                        'stronger_rhs': '328+12*n8+6*n9+7*n10+4*n11+3*n12+n13',
                        'n_definition': 'number of L1 norm-2j vectors '
                                        'nonorthogonal to the chosen root'},
        'rootless_full_layer_multipliers': {
            'L1_norm26': l_series[13], 'L1_norm28': l_series[14],
            'M_norm4_to12': m_series[2:7]},
        'rootless_positive_identities': [
            'T_L26 + 14*T_extra = 2240*I',
            'T_M6 + 34*T_extra = 1453760*I'],
        'fricke_control': checked_control,
    }
    target = Path(__file__).resolve().parents[2]/'data/codex_theta7_degree2_reduction.json'
    target.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Exact degree-two relation:', relation)
    print('Root budget:', budget, '>= 328; absence16..24 excludes roots.')
    print('One positive-lattice Fricke control passed through q^32.')
    print('Rootless full-layer transfer:', m_series[2:7])


if __name__ == '__main__':
    main()
