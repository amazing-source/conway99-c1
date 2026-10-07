"""Exact independent audit of the proposed +3-side rank-60 construction.

No LP or graph-exclusion assertion. Eta expansions and Fricke are checked on
nine positive lattice controls; the fixed rank-six neighbour is enumerated.
"""
from fractions import Fraction
from itertools import product
from math import isqrt
from pathlib import Path
import hashlib
import json

from sympy import Matrix, diag
from sympy.matrices.normalforms import hermite_normal_form

from theta7_audit import eta_product, theta_h7, e4, dilate7, multiply, power


def basis(n):
    forms = []
    for j in range(21):
        r1, r7 = 4*j-10, 70-4*j
        assert r1+r7 == 60
        assert r1+7*r7 == 24*(20-j)
        assert 7*r1+r7 == 24*j
        forms.append(([0]*(20-j) + eta_product(n, r1, r7))[:n+1])
    return forms


def coordinates(series, forms):
    result = [0]*21
    remaining = list(series)
    for degree in range(21):
        j = 20-degree
        result[j] = remaining[degree]
        remaining = [x-result[j]*y for x, y in zip(remaining, forms[j])]
    assert not any(remaining), 'Identity failed beyond the interpolation range'
    return result


def fricke_coordinates(cs, alpha):
    assert alpha % 2 == 0
    return [Fraction(7)**(alpha//2+5-2*i)*cs[20-i] for i in range(21)]


def constant_neighbour_gram():
    # Coordinates in (u,e1,...,e5), with ||u||^2=11.
    # Twice a basis of the even sublattice, followed by twice c/2.
    columns = []
    for i in range(5):
        v = [0]*6
        v[i], v[i+1] = 2, -2
        columns.append(v)
    columns.extend([[0, 0, 0, 0, 0, 4], [3, 1, 1, 1, 1, 1]])
    doubled_basis = hermite_normal_form(Matrix.hstack(*map(Matrix, columns)))
    gram = doubled_basis.T*diag(11, 1, 1, 1, 1, 1)*doubled_basis/4
    assert all(x.q == 1 for x in gram)
    assert all(gram[i, i] % 2 == 0 for i in range(6))
    assert gram.det(method='domain-ge') == 11
    assert all(gram[:k, :k].det(method='domain-ge') > 0 for k in range(1, 7))
    inv = gram.inv(method='DM')
    assert all((11*x).q == 1 for x in inv)
    assert all(11*inv[i, i] % 2 == 0 for i in range(6))
    return [[int(x) for x in gram.row(i)] for i in range(6)]


def constant_neighbour_theta(n):
    """DP in original doubled coordinates: common parity, sum == 0 mod 4.

    This uses the diagonal ambient norm, independently of the HNF Gram.
    """
    limit = 8*n
    answer = [0]*(n+1)
    for parity in (0, 1):
        dp = {(0, 0): 1}
        for weight in (11, 1, 1, 1, 1, 1):
            bound = isqrt(limit//weight)
            values = [x for x in range(-bound, bound+1) if x % 2 == parity]
            new = {}
            for (norm, residue), count in dp.items():
                for x in values:
                    norm2 = norm+weight*x*x
                    if norm2 <= limit:
                        key = norm2, (residue+x) % 4
                        new[key] = new.get(key, 0)+count
            dp = new
        for (norm, residue), count in dp.items():
            if residue == 0:
                assert norm % 8 == 0
                answer[norm//8] += count
    return answer


def constant_neighbour_direct(n):
    """Small direct product enumeration, independent of the DP."""
    answer = [0]*(n+1)
    bounds = [isqrt(8*n//w) for w in (11, 1, 1, 1, 1, 1)]
    for parity in (0, 1):
        ranges = [[x for x in range(-b, b+1) if x % 2 == parity] for b in bounds]
        for vector in product(*ranges):
            if sum(vector) % 4:
                continue
            norm = 11*vector[0]**2+sum(x*x for x in vector[1:])
            assert norm % 8 == 0
            if norm <= 8*n:
                answer[norm//8] += 1
    return answer


def path_count_control(adj, name):
    """Count induced P4 by their unique central edge on existing SRGs."""
    size, degree = len(adj), adj[0].bit_count()
    assert all(row.bit_count() == degree and not row >> i & 1 for i, row in enumerate(adj))
    paths = 0
    for u in range(size):
        for v in range(u+1, size):
            common = adj[u] & adj[v]
            adjacent = (adj[u] >> v) & 1
            assert adjacent == ((adj[v] >> u) & 1)
            assert common.bit_count() == (1 if adjacent else 2)
            if not adjacent:
                continue
            left = adj[u] & ~(common | (1 << v))
            right = adj[v] & ~(common | (1 << u))
            assert left.bit_count() == right.bit_count() == degree-2
            local = 0
            while left:
                bit = left & -left
                left -= bit
                local += (right & ~adj[bit.bit_length()-1]).bit_count()
            assert local == (degree-2)*(degree-3)
            paths += local
    assert paths == size*degree*(degree-2)*(degree-3)//2
    return {'graph': name, 'vertices': size, 'degree': degree, 'induced_P4': paths}


def main():
    n = 84
    forms = basis(n)
    h, e = theta_h7(n), e4(n)
    e7 = dilate7(e)
    controls = []
    for a, b, c in [(0, 0, 30)]+[(a, 7-a, 2) for a in range(8)]:
        assert 8*a+8*b+2*c == 60
        alpha = 8*b+c
        original = multiply(multiply(power(e, a), power(e7, b)), power(h, c))
        dual = multiply(multiply(power(e, b), power(e7, a)), power(h, c))
        cs, ds = coordinates(original, forms), coordinates(dual, forms)
        assert fricke_coordinates(cs, alpha) == ds
        assert fricke_coordinates(ds, 60-alpha) == cs
        assert cs[20] == ds[20] == 1 and cs[0] == 7**(35-alpha//2)
        controls.append({'E8_copies': a, 'scaled_E8_copies': b, 'H7_copies': c,
                         'alpha': alpha, 'coordinates': cs, 'dual_coordinates': ds,
                         'checked_through_q_power': n})

    fixed_theta = constant_neighbour_theta(n)
    assert fixed_theta[:6] == constant_neighbour_direct(5)
    assert fixed_theta[:6] == [1, 40, 122, 400, 520, 1040]
    gram = constant_neighbour_gram()
    cs = [0]*21
    for degree in range(5):
        j = 20-degree
        cs[j] = fixed_theta[degree]-sum(cs[k]*forms[k][degree] for k in range(j+1, 21))
    # A5 = 1040 + 52 G.  Its triangular leading coordinate is c15.
    c15_constant = 1040-sum(cs[k]*forms[k][5] for k in range(16, 21))
    root = Path(__file__).resolve().parents[2]
    rook = [sum(1 << j for j in range(9) if i != j and (i//3 == j//3 or i%3 == j%3))
            for i in range(9)]
    graph_controls = [path_count_control(rook, 'rook_3x3')]
    for filename in ('bvls243.edges', 'twin243_switched.edges'):
        source = root/'data/srg243'/filename
        adj = [0]*243
        for line in source.read_text().splitlines():
            u, v = map(int, line.split())
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        entry = path_count_control(adj, filename)
        entry['normalized_lf_sha256'] = hashlib.sha256(source.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        graph_controls.append(entry)
    report = {
        'scope': 'Exact basis, Fricke controls and fixed neighbour audit; no LP exclusion.',
        'basis_order': 'F_j=eta(tau)^(4j-10) eta(7tau)^(70-4j), j=0..20',
        'q_precision_inclusive': n,
        'fricke_rule': 'd_i=7^(alpha/2+5-2i) c_(20-i)',
        'fixed_c16_through_c20': {str(j): cs[j] for j in range(16, 21)},
        'c15_constant': c15_constant, 'c15_grid_coefficient': 52,
        'fixed_neighbour_gram': gram,
        'fixed_neighbour_theta': fixed_theta,
        'dual_lower_bounds': {'B3': 1386, 'B4': 12474, 'B5': 182952},
        'P4_graph_controls': graph_controls,
        'positive_lattice_controls': controls,
        'basis_sha256': hashlib.sha256(json.dumps(forms, separators=(',', ':')).encode()).hexdigest(),
    }
    (root/'data/codex_theta7_rank60_audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    (root/'data/codex_theta7_rank60_basis_q84.json').write_text(json.dumps(forms)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ('positive_lattice_controls', 'fixed_neighbour_theta')}, indent=2))
    print('Nine positive controls, both Fricke directions, and two neighbour enumerations passed.')


if __name__ == '__main__':
    main()
