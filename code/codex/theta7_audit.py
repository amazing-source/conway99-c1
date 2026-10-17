"""Independent exact audit of LAB's level-7, weight-22 theta basis.

Uses the logarithmic-derivative recurrence for eta products, integer
convolutions, and known positive lattice theta series. No LP is run here.
"""
from fractions import Fraction
from math import isqrt
from pathlib import Path
import hashlib
import json


def multiply(a, b):
    n = min(len(a), len(b)) - 1
    return [sum(a[j] * b[k - j] for j in range(k + 1)) for k in range(n + 1)]


def power(a, exponent):
    result = [1] + [0] * (len(a) - 1)
    while exponent:
        if exponent & 1:
            result = multiply(result, a)
        exponent //= 2
        if exponent:
            a = multiply(a, a)
    return result


def theta_h7(n):
    # Gram [[2,1],[1,4]], so the q-exponent is x^2+xy+2y^2.
    result = [0] * (n + 1)
    bound = 2 * isqrt(n) + 2
    for x in range(-bound, bound + 1):
        for y in range(-bound, bound + 1):
            q = x*x + x*y + 2*y*y
            if q <= n:
                result[q] += 1
    assert result[0] == 1
    return result


def eta_product(n, r1, r7):
    """Coefficients after removing the initial fractional q-power."""
    log_derivative = [0] * (n + 1)
    for d in range(1, n + 1):
        term = -d * (r1 + (r7 if d % 7 == 0 else 0))
        for k in range(d, n + 1, d):
            log_derivative[k] += term
    result = [1] + [0] * n
    for k in range(1, n + 1):
        numerator = sum(log_derivative[j] * result[k - j] for j in range(1, k + 1))
        assert numerator % k == 0
        result[k] = numerator // k
    return result


def basis(n):
    theta = theta_h7(n)
    answer = []
    for j in range(15):
        r1, r7 = 4*j - 7, 49 - 4*j
        assert r1 + r7 == 42
        assert (r1 + 7*r7) // 24 == 14-j
        assert (7*r1 + r7) // 24 == j
        product = multiply(theta, eta_product(n, r1, r7))
        order = 14-j
        row = ([0] * order + product)[:n + 1]
        assert row[order] == 1 and all(x == 0 for x in row[:order])
        answer.append(row)
    return answer


def coordinates(series, forms):
    result = [0] * 15
    remaining = list(series)
    for degree in range(15):
        j = 14 - degree
        result[j] = remaining[degree]
        remaining = [x - result[j] * y for x, y in zip(remaining, forms[j])]
    assert all(x == 0 for x in remaining), 'Series failed beyond the triangular interpolation range'
    return result


def fricke_coordinates(c, alpha):
    assert alpha % 2 == 0
    return [Fraction(7)**(alpha//2 + 3 - 2*i) * c[14-i] for i in range(15)]


def e4(n):
    result = [1] + [0] * n
    for d in range(1, n + 1):
        for k in range(d, n + 1, d):
            result[k] += 240 * d**3
    return result


def dilate7(series):
    return [series[i//7] if i % 7 == 0 else 0 for i in range(len(series))]


def main():
    n = 84
    forms = basis(n)
    h, e = theta_h7(n), e4(n)
    e7 = dilate7(e)
    controls = []
    # E8^a orthogonal sum sqrt(7)E8^b orthogonal sum H7^c.
    # All have rank44; the Fricke dual exchanges a and b.
    for a, b, c in [(0, 0, 22), (5, 0, 2), (4, 1, 2), (3, 2, 2),
                    (2, 3, 2), (1, 4, 2), (0, 5, 2)]:
        assert 8*a + 8*b + 2*c == 44
        alpha = 8*b+c
        original = multiply(multiply(power(e, a), power(e7, b)), power(h, c))
        dual = multiply(multiply(power(e, b), power(e7, a)), power(h, c))
        cs, ds = coordinates(original, forms), coordinates(dual, forms)
        assert fricke_coordinates(cs, alpha) == ds
        assert fricke_coordinates(ds, 44-alpha) == cs
        assert cs[14] == ds[14] == 1 and cs[0] == 7**(25-alpha//2)
        for j, x in enumerate(cs):
            assert x % (7**max(0, 25-alpha//2-2*j)) == 0
        controls.append({'E8_copies': a, 'scaled_E8_copies': b, 'H7_copies': c,
                         'determinant_exponent_alpha': alpha, 'coordinates': cs,
                         'dual_coordinates': ds, 'checked_through_q_power': n})

    # General minimum >=14 forces the seven high-index coefficients.
    cs = [0] * 15
    for degree in range(7):
        j = 14-degree
        cs[j] = int(degree == 0) - sum(cs[k] * forms[k][degree] for k in range(j+1, 15))
    fixed = {str(j): cs[j] for j in range(8, 15)}
    report = {'scope': 'Exact series and Fricke audit; no graph exclusion or LP feasibility claim.',
              'basis_order': 'F_j = theta_H7 eta(tau)^(4j-7) eta(7tau)^(49-4j), j=0..14',
              'q_precision_inclusive': n, 'fixed_c8_through_c14_from_min14': fixed,
              'positive_lattice_controls': controls,
              'basis_sha256': hashlib.sha256(json.dumps(forms, separators=(',', ':')).encode()).hexdigest()}
    root = Path(__file__).resolve().parents[2]
    (root/'data/codex_theta7_audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    (root/'data/codex_theta7_basis_q84.json').write_text(json.dumps(forms)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'positive_lattice_controls'}, indent=2))
    print('All seven positive lattice controls and their Fricke duals passed.')


if __name__ == '__main__':
    main()
