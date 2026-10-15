"""Exact sign reduction and operator-direction cuts for a fixed h-mean.

Standalone SymPy module. Kernels and positive mean blocks are supplied by the
producer. No graph, rank certificate, or PSD certificate is re-audited here.
"""
import argparse
from itertools import product
import json
from math import gcd, lcm
from pathlib import Path
import random

import sympy as sp
from sympy.polys.matrices import DomainMatrix


def sparse_channels(size, channels):
    """Same signs as h_mixed_energy.orientation_energy_gram."""
    result = []
    for i, j, kind in channels:
        if not 0 <= i < j < size or kind not in ('parallel', 'crossed'):
            raise ValueError('Expected (i,j,parallel/crossed), 0<=i<j<size.')
        first = -sp.Rational(1, 2) if kind == 'parallel' else sp.Rational(1, 2)
        result.append(((i, j, first), (j, i, -sp.Rational(1, 2))))
    if len(set(map(tuple, channels))) != len(channels):
        raise ValueError('An edge-orbit channel may occur only once.')
    return result


def primitive_row(row):
    row = list(map(sp.Rational, row))
    scale = lcm(*(int(x.q) for x in row))
    integers = [int(scale*x) for x in row]
    divisor = gcd(*integers)
    if not divisor:
        return tuple(integers)
    first = next(x for x in integers if x)
    divisor *= 1 if first > 0 else -1
    return tuple(x//divisor for x in integers)


def range_equations(size, channels, left_kernels=(), right_kernels=()):
    """R*epsilon=0 iff every supplied N_left^T B and B*N_right vanishes.

    For simultaneous T,U positivity, pass the kernels of A,A' on the left
    and C,C' on the right. Alternatively use the correctly shorted blocks.
    Individual channels are allowed to leak: only their signed sum matters.
    """
    sparse = sparse_channels(size, channels)
    rows = []
    for source, side in ((left_kernels, 'left'), (right_kernels, 'right')):
        for kernel in source:
            kernel = sp.Matrix(kernel)
            if kernel.rows != size:
                raise ValueError('Kernel columns must have the block dimension.')
            for k in range(kernel.cols):
                for t in range(size):
                    if side == 'left':
                        row = [sum(kernel[i, k]*x for i, j, x in terms if j == t)
                               for terms in sparse]
                    else:
                        row = [sum(x*kernel[j, k] for i, j, x in terms if i == t)
                               for terms in sparse]
                    if any(row):
                        rows.append(primitive_row(row))
    unique = sorted(set(rows))
    return sp.Matrix(unique) if unique else sp.zeros(0, len(channels))


def reduce_sign_kernel(equations):
    """Exact epsilon=L*z, with free signs z, and pair-sign propagation.

    Every feasible epsilon is represented; remaining conditions are that all
    rows of L*z equal +/-1. All constraints are homogeneous, so epsilon and
    -epsilon form a pair. This gives <=2^(d-1) trials after propagation.
    """
    equations = sp.Matrix(equations)
    b = equations.cols
    reduced, pivots = DomainMatrix.from_Matrix(equations).rref()
    rref = reduced.to_Matrix()
    free = [i for i in range(b) if i not in pivots]
    base = dict(channels=b, equation_rank=len(pivots), linear_dimension=len(free))

    def impossible(reason, **detail):
        return dict(base, status='NO_SIGN_VECTOR', reason=reason, **detail)

    # Integral parity is stronger than real consistency of a homogeneous system.
    for i in range(len(pivots)):
        row = primitive_row(rref.row(i))
        if sum(row) % 2:
            return impossible('Odd sum in a primitive integer homogeneous row.',
                              primitive_row=list(row))
    lift = sp.zeros(b, len(free))
    for k, i in enumerate(free):
        lift[i, k] = 1
    for row, pivot in enumerate(pivots):
        for k, j in enumerate(free):
            lift[pivot, k] = -rref[row, j]

    merges = 0
    while True:
        d = lift.cols
        parent, sign = list(range(d)), [1]*d

        def find(i):
            if parent[i] != i:
                root, relative = find(parent[i])
                sign[i] *= relative
                parent[i] = root
            return parent[i], sign[i]

        def join(i, j, relative):
            ri, si = find(i)
            rj, sj = find(j)
            if ri == rj:
                return si*sj == relative
            parent[ri], sign[ri] = rj, relative*si*sj
            return True

        for i in range(b):
            support = [(j, lift[i, j]) for j in range(d) if lift[i, j]]
            if not support:
                return impossible('A channel is forced to zero.', channel=i)
            if len(support) == 1 and abs(support[0][1]) != 1:
                return impossible('A channel has a forced magnitude other than one.',
                                  channel=i, magnitude=str(abs(support[0][1])))
            if len(support) == 2:
                (j, a), (k, c) = support
                relative = (1-a*a-c*c)/(2*a*c)
                if relative not in (-1, 1):
                    return impossible('A two-term channel cannot have magnitude one.',
                                      channel=i, forced_sign_product=str(relative))
                if not join(j, k, int(relative)):
                    return impossible('Contradictory pair-sign relations.', channel=i)
        roots = sorted({find(i)[0] for i in range(d)})
        if len(roots) == d:
            break
        root_index = {root: i for i, root in enumerate(roots)}
        quotient = sp.zeros(d, len(roots))
        for i in range(d):
            root, relative = find(i)
            quotient[i, root_index[root]] = relative
        merges += d-len(roots)
        lift = lift*quotient
    assert equations*lift == sp.zeros(equations.rows, lift.cols)
    d = lift.cols
    return dict(base, status='EXACT_SIGN_LIFT', propagated_dimension=d,
                pair_merges=merges, trials_mod_global_sign=2**max(0, d-1),
                lift=[[str(x) for x in lift.row(i)] for i in range(b)],
                scope='The remaining row conditions |L*z|=1 are mandatory; range feasibility alone is not graph admissibility or PSD.')


def operator_direction_cut(upper_left, upper_right, channels, left, right):
    """Integer |c.epsilon|<=rhs forced by the two test vectors (u,+/-v).

    For U=[[A',-B],[-B^T,C']], positivity implies
    |2*u^T*B*v| <= u^T*A'*u + v^T*C'*v.
    Supply rational directions, for example rationalized components of a
    producer's violating vector. Validity does not require an eigenvalue test.
    """
    upper_left, upper_right = sp.Matrix(upper_left), sp.Matrix(upper_right)
    u, v = sp.Matrix(left), sp.Matrix(right)
    size = upper_left.rows
    if upper_left.shape != (size, size) or upper_right.shape != (size, size):
        raise ValueError('Expected two square blocks of equal size.')
    if u.shape != (size, 1) or v.shape != (size, 1):
        raise ValueError('Expected column directions of the block dimension.')
    sparse = sparse_channels(size, channels)
    coeff = [2*sum(u[i]*x*v[j] for i, j, x in terms) for terms in sparse]
    rhs = (u.T*upper_left*u)[0]+(v.T*upper_right*v)[0]
    numbers = list(map(sp.Rational, coeff+[rhs]))
    scale = lcm(*(int(x.q) for x in numbers))
    integers = [int(x*scale) for x in numbers]
    divisor = gcd(*integers) or 1
    integers = [x//divisor for x in integers]
    return dict(coefficients=integers[:-1], rhs=integers[-1],
                meaning='abs(sum coefficients[k]*epsilon[k])<=rhs',
                scope='Necessary operator-direction cut, not a sufficient PSD test.')


def enumerate_reduced_signs(reduction, cuts=(), max_dimension=14, sample_limit=16):
    """Small, explicitly bounded search; never starts an oversized enumeration."""
    if reduction['status'] == 'NO_SIGN_VECTOR':
        return dict(status='NO_RANGE_FEASIBLE_ORIENTATION', reason=reduction['reason'])
    if reduction['channels'] == 0:
        lift = sp.zeros(0, 0)
    else:
        lift = sp.Matrix(reduction['lift'])
    b, d = lift.shape
    if d > max_dimension:
        return dict(status='NOT_ENUMERATED', dimension=d,
                    trials_mod_global_sign=reduction['trials_mod_global_sign'],
                    max_dimension=max_dimension)
    rows = []
    for i in range(b):
        den = lcm(*(int(x.q) for x in lift.row(i)))
        rows.append(([int(x*den) for x in lift.row(i)], den))
    for cut in cuts:
        if len(cut['coefficients']) != b:
            raise ValueError('Direction cut and lift need the same channels.')
    tried = range_feasible = survivors = 0
    samples = []
    assignments = ((),) if not d else ((1,)+tail for tail in product((-1, 1), repeat=d-1))
    for signs in assignments:
        tried += 1
        epsilon = []
        for row, den in rows:
            val = sum(c*z for c, z in zip(row, signs))
            if abs(val) != den:
                break
            epsilon.append(val//den)
        if len(epsilon) != b:
            continue
        range_feasible += 1
        if any(abs(sum(c*x for c, x in zip(cut['coefficients'], epsilon))) > cut['rhs']
               for cut in cuts):
            continue
        survivors += 1
        if len(samples) < sample_limit:
            samples.append(epsilon)
    status = 'ORIENTATIONS_SURVIVE_NECESSARY_FILTERS' if survivors else 'ALL_ORIENTATIONS_EXCLUDED_BY_SUPPLIED_CONSTRAINTS'
    return dict(status=status, trials=tried, range_feasible_mod_sign=range_feasible,
                survivors_mod_sign=survivors, sample_representatives=samples,
                scope='An exhaustive result for this fixed channel system and supplied valid constraints only; no assertion about untested means or Conway.')


def report():
    # Pair propagation is genuinely stronger than homogeneous linear reduction.
    eq = sp.Matrix([[-1, -2, 1]])
    reduced = reduce_sign_kernel(eq)
    assert reduced['linear_dimension'] == 2 and reduced['propagated_dimension'] == 1
    assert enumerate_reduced_signs(reduced)['range_feasible_mod_sign'] == 1
    parity = reduce_sign_kernel(sp.Matrix([[1, 1, 1]]))
    assert parity['status'] == 'NO_SIGN_VECTOR'
    impossible_magnitude = reduce_sign_kernel(sp.Matrix([[1, -2]]))
    assert impossible_magnitude['status'] == 'NO_SIGN_VECTOR'
    # A three-term lift retains a genuine nonlinear magnitude condition.
    nonlinear = reduce_sign_kernel(sp.Matrix([[-1, -1, -1, 1]]))
    nonlinear_count = enumerate_reduced_signs(nonlinear)
    assert nonlinear_count['trials'] == 4 and nonlinear_count['range_feasible_mod_sign'] == 3

    channels = [(0, 1, 'parallel'), (0, 1, 'crossed')]
    null = sp.Matrix([1, 0])
    equations = range_equations(2, channels, left_kernels=[null])
    cancelled = reduce_sign_kernel(equations)
    count = enumerate_reduced_signs(cancelled)
    assert count['range_feasible_mod_sign'] == 1
    assert count['sample_representatives'] == [[1, 1]]
    # Each B_k leaks into the forbidden first row, but their sum does not.
    terms = sparse_channels(2, channels)
    blocks = []
    for sparse in terms:
        block = sp.zeros(2)
        for i, j, value in sparse:
            block[i, j] = value
        blocks.append(block)
    assert all(null.T*block != sp.zeros(1, 2) for block in blocks)
    assert null.T*(blocks[0]+blocks[1]) == sp.zeros(1, 2)

    # Artificial ten-dimensional mean: weighted Frobenius=9/4<=10 for all
    # orientations, yet normalized operator norm=3/2. Two exact cuts reject all.
    upper = sp.eye(10)*sp.Rational(2, 3)
    cuts = [operator_direction_cut(upper, upper, channels, sp.eye(10)[:, i], sp.eye(10)[:, j])
            for i, j in ((0, 1), (1, 0))]
    unconstrained = reduce_sign_kernel(sp.zeros(0, 2))
    rejected = enumerate_reduced_signs(unconstrained, cuts)
    assert rejected['range_feasible_mod_sign'] == 2 and rejected['survivors_mod_sign'] == 0
    for signs in product((-1, 1), repeat=2):
        mixed = sum((z*block for z, block in zip(signs, blocks)), sp.zeros(2))
        assert sp.trace(mixed*mixed.T)*sp.Rational(9, 4) == sp.Rational(9, 4)
    oversized = enumerate_reduced_signs(reduce_sign_kernel(sp.zeros(0, 40)))
    assert oversized['status'] == 'NOT_ENUMERATED'
    # Compare the reduction with literal sign enumeration on small new systems,
    # including systems deliberately containing a known sign solution.
    rng = random.Random(795)
    for trial in range(48):
        b = 2+trial % 5
        nrows = trial % 4
        witness = [rng.choice((-1, 1)) for _ in range(b)]
        rows = [[rng.randrange(-2, 3) for _ in range(b)] for _ in range(nrows)]
        if trial % 2:
            for row in rows:
                row[-1] = -sum(x*y for x, y in zip(row[:-1], witness[:-1]))*witness[-1]
        equations = sp.Matrix(rows) if rows else sp.zeros(0, b)
        direct = sum(all(sum(row[i]*signs[i] for i in range(b)) == 0 for row in rows)
                     for signs in product((-1, 1), repeat=b))//2
        candidate = reduce_sign_kernel(equations)
        obtained = (0 if candidate['status'] == 'NO_SIGN_VECTOR' else
                    enumerate_reduced_signs(candidate)['range_feasible_mod_sign'])
        assert direct == obtained
    return dict(status='EXACT_SIGN_REDUCTION_AND_OPERATOR_CUTS',
                proof=[
                    'The supplied range equations are homogeneous rational equations R*epsilon=0. RREF expresses every epsilon as L*z using actual free coordinates of epsilon; z therefore consists of signs.',
                    'The exact remaining requirement is that every row of L*z have magnitude one. A two-term row a*z_i+c*z_j forces z_i*z_j=(1-a^2-c^2)/(2*a*c). Values other than +/-1 are impossible; valid values identify sign variables, repeatedly.',
                    'All original constraints and direction cuts are invariant under global sign reversal. Fix one remaining sign to+1: at most2^(d-1) trials suffice for a mean of reduced dimension d. This is a conditional per-mean bound, not a uniform bound over all means.',
                    'PSD tested against (u,+/-v) gives the absolute linear cut |2*u^T*B*v|<=u^T*Aprime*u+v^T*Cprime*v. The cut is exact for rational vectors even when found by floating-point singular vectors; it sees individual directions rather than total energy.'
                ],
                pair_propagation=reduced, odd_row_obstruction=parity,
                nonlinear_fixture=nonlinear_count,
                cancelling_channel_leakage=count,
                own_small_systems_against_direct_sign_count=48,
                operator_fixture=dict(dimension=10, weighted_frobenius_squared='9/4',
                                      normalized_operator_norm='3/2', cuts=cuts, enumeration=rejected),
                large_dimension_guard=oversized,
                fixture_scope='Own algebraic fixtures only. No fixture is asserted to be a binary Conway border or an SRG; no peer mean read.',
                limitations='No new C1 family or actual mean excluded. The actual reduced dimensions of the peer means have not been computed here.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status', 'nonlinear_fixture', 'operator_fixture', 'large_dimension_guard', 'limitations')}))
