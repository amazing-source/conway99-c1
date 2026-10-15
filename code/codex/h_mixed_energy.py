"""Exact cost of breaking h, and a mean-only capacity bound for the mixed block.

Answer to LAB792. All checks use own algebraic fixtures or the sixteen binary
2x2 blocks; no producer rank or positivity certificate is rechecked.
"""
import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

sys.path.insert(0, str(Path(__file__).resolve().parent))
from h_even_network import geometry
from four_star_profile_join import LABELS


def shorted_upper(upper, kernel):
    """Short a producer-positive upper block to ker(kernel^T).

    The columns of kernel span ker(A), where the lower PSD block A forces
    kernel^T B=0. Positivity of upper is a hypothesis, not checked here.
    """
    upper, kernel = sp.Matrix(upper), sp.Matrix(kernel)
    middle = kernel.T*upper*kernel
    pivots = DomainMatrix.from_Matrix(middle).rref()[1]
    if not pivots:
        result = upper
    else:
        columns = (upper*kernel).extract(range(upper.rows), pivots)
        principal = middle.extract(pivots, pivots)
        result = upper-columns*principal.inv(method='DM')*columns.T
    if kernel.T*result != sp.zeros(kernel.cols, upper.cols):
        raise ValueError('Input does not satisfy the stated PSD/kernel range contract.')
    return result


def orientation_energy_gram(upper_even_inverse, upper_odd_inverse, channels):
    """Exact weighted energy for broken h-edge orientation signs.

    Supply the producer's Moore-Penrose inverses of the upper parity blocks.
    Each channel is (i,j,kind), i<j, kind='parallel' or 'crossed', according
    to which of the two h-edge-orbits has mean1/2. No ranks are computed.
    """
    left, right = sp.Matrix(upper_even_inverse), sp.Matrix(upper_odd_inverse)
    sparse = []
    for i, j, kind in channels:
        if i >= j or kind not in ('parallel', 'crossed'):
            raise ValueError('Each channel requires i<j and a valid edge-orbit kind.')
        first = -sp.Rational(1, 2) if kind == 'parallel' else sp.Rational(1, 2)
        sparse.append(((i, j, first), (j, i, -sp.Rational(1, 2))))
    result = sp.Matrix(len(sparse), len(sparse), lambda k, l:
        sum(x*y*left[m, i]*right[j, n] for i, j, x in sparse[k] for m, n, y in sparse[l]))
    assert result == result.T
    return result


def diagonal_minorant(energy):
    """Cheap rational certificate; an inconclusive bound is not an exclusion."""
    energy = sp.Matrix(energy)
    d = [energy[i, i]-sum(abs(energy[i, j]) for j in range(energy.cols) if j != i)
         for i in range(energy.rows)]
    # H-diag(d) is symmetric diagonally dominant with nonnegative diagonal.
    return dict(diagonal=list(map(str, d)), universal_sign_energy_at_least=str(sum(d)),
                rank10_upper_contraction_impossible=bool(sum(d) > 10),
                scope='Rejection requires the upper range conditions and rankB<=10; otherwise this is only an energy bound.')


def counts_and_mixed(gamma, plus, minus, h):
    gamma = sp.Matrix(gamma)
    mixed = -plus.T*gamma*minus/2
    delta = gamma-gamma.extract(h, h)
    edge_orbits = 0
    for i, j in combinations(range(44), 2):
        image = tuple(sorted((h[i], h[j])))
        if (i, j) < image and gamma[i, j] != gamma[image[0], image[1]]:
            edge_orbits += 1
    blocks = 0
    for i, j in combinations(range(22), 2):
        blocks += int(bool(mixed[i, j] or mixed[j, i]))
    frobenius = sum(x*x for x in mixed)
    assert 2*frobenius == edge_orbits
    assert sum(x*x for x in delta) == 4*edge_orbits
    assert blocks <= edge_orbits <= 2*blocks
    return dict(broken_vertex_orbit_pairs=blocks, broken_edge_orbits=edge_orbits,
                mixed_frobenius_squared=str(frobenius))


def report():
    table = []
    by_cost = Counter()
    for a, b, c, d in product((0, 1), repeat=4):
        x, y = a-d, b-c
        bij, bji = -sp.Rational(x-y, 2), -sp.Rational(x+y, 2)
        broken = x*x+y*y
        energy = bij*bij+bji*bji
        assert 2*energy == broken
        if broken == 1:
            assert bij*bij == bji*bji == sp.Rational(1, 4)
        if broken == 2:
            assert sorted([bij*bij, bji*bji]) == [0, 1]
        by_cost[broken] += 1
        table.append(dict(block=[[a, b], [c, d]], broken_edge_orbits=broken,
                          B_ij=str(bij), B_ji=str(bji), energy=str(energy)))
    assert by_cost == {0: 4, 1: 8, 2: 4}
    g = geometry()
    plus = g['basis']
    minus = sp.zeros(44, 22)
    index = {p: i for i, p in enumerate(LABELS)}
    h = list(range(44))
    for j, (p, q) in enumerate(g['orbits']):
        i, k = index[p], index[q]
        minus[i, j], minus[k, j] = 1, -1
        h[i], h[k] = k, i
    assert plus.T*minus == sp.zeros(22)
    assert minus.T*minus == 2*sp.eye(22)
    rng = random.Random(792)
    fixtures = []
    for numerator in (1, 2, 3):
        gamma = sp.zeros(44)
        for i, j in combinations(range(44), 2):
            gamma[i, j] = gamma[j, i] = int(rng.randrange(8) < numerator)
        fixtures.append(counts_and_mixed(gamma, plus, minus, h))
    # A nontrivial shorting fixture: the original upper trace is7, the capacity
    # on the prescribed two-dimensional range has trace2.
    factor = sp.Matrix([[1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 1, 0], [0, 0, 0, 1]])
    upper = factor*factor.T
    kernel = sp.eye(4)[:, 2:]
    short = shorted_upper(upper, kernel)
    assert short == sp.diag(1, 1, 0, 0)
    # Check the new sparse energy formula against direct dense traces.
    channels = [(0, 1, 'parallel'), (0, 1, 'crossed'), (1, 2, 'parallel'), (0, 2, 'crossed')]
    linv = sp.Matrix([[2, 1, 0], [1, 3, 1], [0, 1, 2]])
    rinv = sp.Matrix([[3, 0, 1], [0, 2, 0], [1, 0, 3]])
    energy = orientation_energy_gram(linv, rinv, channels)
    blocks = []
    for i, j, kind in channels:
        block = sp.zeros(3)
        block[i, j] = -sp.Rational(1, 2) if kind == 'parallel' else sp.Rational(1, 2)
        block[j, i] = -sp.Rational(1, 2)
        blocks.append(block)
    assert energy == sp.Matrix(4, 4, lambda i, j: sp.trace(linv*blocks[i]*rinv*blocks[j].T))
    assert orientation_energy_gram(sp.eye(3), sp.eye(3), channels) == sp.eye(4)/2
    minorant = diagonal_minorant(energy)
    for signs in product((-1, 1), repeat=4):
        mixed = sum((sign*block for sign, block in zip(signs, blocks)), sp.zeros(3))
        value = (sp.Matrix(signs).T*energy*sp.Matrix(signs))[0]
        assert value == sp.trace(linv*mixed*rinv*mixed.T)
        assert value >= sp.Rational(minorant['universal_sign_energy_at_least'])
    return dict(status='EXACT_BROKEN_EDGE_ENERGY_AND_MEAN_CAPACITY',
        definitions=dict(Q_plus='One+1 at both labels of each h-orbit; normalize by sqrt2.',
                         Q_minus='One+1 and one-1 per h-orbit; normalize by sqrt2.',
                         B='-Q_plus^T Gamma Q_minus/2, the mixed block of T.',
                         Delta='Gamma-H Gamma H; entries0,+1,-1.',
                         b='Number of unordered edge-orbits {e,h(e)} of size2 with exactly one edge present.',
                         q='Number of unordered pairs of vertex-orbits whose2x2 block is not h-invariant.'),
        exact_identity='||Delta||_F^2=4b=8||B||_F^2, hence ||B||_F^2=b/2 and q/2<=||B||_F^2<=q.',
        operator_bound=dict(general='||B||_op^2>=b/(2 rankB).',
                            central_stars='rankB<=20 from the two known even and odd star differences.',
                            positive_rank10='If T>=0 and rankA=10, B^T kerA=0, so rankB<=10 and ||B||_op^2>=b/20>=q/20.',
                            forty='Forty broken edge-orbits give Frobenius norm squared20 exactly. Forty broken vertex-orbit pairs give squared Frobenius norm in[20,40]. Either interpretation forces operator norm at least sqrt2 under the rank10/PSD hypotheses.'),
        block_table=table,
        mean_only_capacity=dict(definition='Let N span kerA. For U0 diagonal blocks Abar,Cbar PSD, define S=Abar-Abar*N*(N^T*Abar*N)^+*N^T*Abar. It is the shorted upper form on rangeA.',
            equivalence='Under N^T B=0, [[Abar,-B],[-B^T,Cbar]] PSD iff [[S,-B],[-B^T,Cbar]] PSD.',
            spectral_bound='b/2=||B||_F^2 <= sum_{i=1}^{r} s_i*c_i, where s_i,c_i are decreasing eigenvalues of S,Cbar and r=rankB<=rankA (using r=rankA gives a safe mean-only bound).',
            exact_simple_bound='If Cbar<=beta*I, then b<=2*beta*trace(S). For valid T0,U0, beta=7 is always safe: b<=14*trace(S).',
            rejection='A mean violating this bound has no positive binary orientation with that broken-edge pattern. The necessary bound may still pass for all current means; none are tested here.'),
        weighted_orientation_energy=dict(parameterization='For a fixed half-integral mean Gamma0, the b broken edge-orbits have independent signs epsilon_k in{+1,-1} before admissibility. B=sum epsilon_k B_k, with Frobenius inner products <B_k,B_l>=delta_kl/2.',
            weighted_gram='H_kl=trace(Abar^+ B_k Cbar^+ B_l^T). If the upper range conditions hold, epsilon^T H epsilon is the squared Frobenius norm of Abar^{+1/2} B Cbar^{+1/2}.',
            necessary='U PSD implies all its singular values<=1; together with rankB<=10, epsilon^T H epsilon<=10.',
            lower_certificate='Any rational diagonal d with H-diag(d) PSD gives epsilon^T H epsilon>=sum(d), since epsilon_k^2=1. A certificate sum(d)>10 rejects every orientation of this mean.',
            scope='An exact certificate template, not a computed universal bound, solved Ising model, or affordable exhaustive enumeration claim.'),
        proof=[
            'Each broken unordered edge-orbit contributes four unit squares to Delta. In the orthonormal h-parity basis Delta=[[0,-2B],[-2B^T,0]], hence its Frobenius norm squared is8||B||_F^2.',
            'For the binary2x2 block [[a,b],[c,d]], put x=a-d,y=b-c. Then B_ij=-(x-y)/2,B_ji=-(x+y)/2. Their squared sum is(x^2+y^2)/2. A singly broken block has two entries of absolute value1/2; a doubly broken block has one entry of absolute value1 and one zero.',
            'The count b is determined by the half-integral mean: a broken edge-orbit is precisely one whose averaged entries equal1/2. Changing only orientation signs cannot reduce the unweighted Frobenius norm; it can change the singular values and the weighted energy.',
            'Shorting follows by eliminating the kerA coordinates from the positive upper block; the mixed columns have zero entries there. On the remaining support, B=S^(1/2) K Cbar^(1/2) with K a contraction. The trace rearrangement bound gives the spectral capacity and the scalar beta bound.',
            'The weighted contraction is linear in the orientation signs. Its squared Frobenius norm is the stated positive semidefinite quadratic form. A diagonal minorant supplies the exact sign-independent certificate.'],
        own_checks=dict(binary_blocks=16, block_cost_histogram=dict(by_cost), arbitrary_binary_matrix_fixtures=fixtures,
                        shorting_fixture=dict(original_trace=str(sp.trace(upper)), short_trace=str(sp.trace(short)), result='PASS'),
                        weighted_sign_fixture=dict(channels=4, exact_sign_choices=16, sparse_vs_dense='PASS',
                                                   identity_metric='H=I/2', diagonal_certificate=minorant),
                        scope='Arbitrary binary matrices are not claimed C1/C2 borders; the normalization identity holds for every binary graph. No peer graph read.'),
        limitations='The norm count is exact, but by itself does not force tU<1, prove H-INV, or exclude C1. No current mean has been rejected by the new capacity certificate in this report.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'exact_identity', 'operator_bound', 'own_checks', 'limitations')}))
