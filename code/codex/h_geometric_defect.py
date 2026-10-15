"""Small exact coupling blocks for g=h*p with a non-mate-preserving p.

All core functions need SymPy only. No graph seed is loaded. The producer
supplies positive mean blocks; the low-rank test computes their new coupling
residual, rather than re-auditing diagonal positivity or graph admissibility.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix


def matching_partition(partner):
    """Alternating component sizes in M union partner, measured in mate pairs."""
    unseen, sizes = set(range(10)), []
    while unseen:
        root = unseen.pop()
        component, stack = {root}, [root]
        while stack:
            i = stack.pop()
            for j in (i ^ 1, partner[i]):
                if j not in component:
                    component.add(j)
                    unseen.remove(j)
                    stack.append(j)
        sizes.append(len(component)//2)
    return tuple(sorted(sizes, reverse=True))


def rank_factor(matrix):
    """Rational full-column-rank X,Y with matrix=X*Y^T."""
    matrix = sp.Matrix(matrix)
    columns = DomainMatrix.from_Matrix(matrix).rref()[1]
    if not columns:
        return sp.zeros(matrix.rows, 0), sp.zeros(matrix.cols, 0)
    x = matrix.extract(range(matrix.rows), columns)
    rows = DomainMatrix.from_Matrix(x.T).rref()[1]
    yt = x.extract(rows, range(x.cols)).inv(method='DM')*matrix.extract(rows, range(matrix.cols))
    assert x*yt == matrix
    return x, yt.T


def geometric_defect(outer_involution, labels=None):
    """p maps outer letter4+i to4+p[i]; g=(01)(23)*p on the44 labels.

    The default label order is lexical. Pass the producer's label order when
    comparing its mean blocks; the two columns per orbit use the first index
    as the positive sign of the odd vector. Q columns have norm sqrt(2).
    """
    p = list(outer_involution)
    if sorted(p) != list(range(10)) or any(p[p[i]] != i for i in range(10)):
        raise ValueError('p must be an involution on indices0,...,9.')
    expected = {(i, j) for i, j in combinations(range(14), 2) if (i ^ 1) != j and i < 4}
    labels = sorted(expected) if labels is None else [tuple(sorted(pair)) for pair in labels]
    if len(labels) != 44 or set(labels) != expected:
        raise ValueError('Expected the44 non-mate labels meeting0,1,2,3.')
    letter_image = [1, 0, 3, 2]+[4+i for i in p]
    index = {pair: i for i, pair in enumerate(labels)}
    image = [index[tuple(sorted(letter_image[x] for x in pair))] for pair in labels]
    assert all(image[i] != i and image[image[i]] == i for i in range(44))
    orbits = [(i, image[i]) for i in range(44) if i < image[i]]
    plus, minus = sp.zeros(44, 22), sp.zeros(44, 22)
    for k, (i, j) in enumerate(orbits):
        plus[i, k] = plus[j, k] = 1
        minus[i, k], minus[j, k] = 1, -1
    intersection = sp.Matrix(44, 44, lambda i, j: len(set(labels[i]) & set(labels[j])))
    conjugate = sp.Matrix(44, 44, lambda i, j: sum((x ^ 1) in labels[j] for x in labels[i]))
    k = (3*intersection+conjugate-2*sp.ones(44))/8
    ell = (4*intersection-conjugate+2*sp.ones(44))/15
    defect = k-k.extract(image, image)
    assert ell-ell.extract(image, image) == -sp.Rational(8, 15)*defect
    partner = [p[p[i] ^ 1] for i in range(10)]
    for i, a in enumerate(labels):
        for j, b in enumerate(labels):
            expected_entry = sp.S.Zero
            if a[1] >= 4 and b[1] >= 4:
                y, z = a[1]-4, b[1]-4
                expected_entry = sp.Rational(int(z == (y ^ 1))-int(z == partner[y]), 8)
            assert defect[i, j] == expected_entry
    mixed = plus.T*defect*minus/2
    assert plus.T*defect*plus == minus.T*defect*minus == sp.zeros(22)
    assert -plus.T*k*minus/2 == -mixed/2
    assert -plus.T*ell*minus/2 == sp.Rational(4, 15)*mixed
    x, y = rank_factor(mixed)
    partition = matching_partition(partner)
    assert x.cols == 5-len(partition)
    return dict(labels=labels, image=image, plus=plus, minus=minus,
                matching_partition=partition, defect=defect, mixed_defect=mixed,
                coupling_rank=x.cols, factor_even=x, factor_odd=y)


def metric_on_range(positive_block, columns):
    """Compute columns^T A^+ columns exactly; A PSD is a producer hypothesis."""
    block, columns = sp.Matrix(positive_block), sp.Matrix(columns)
    if block.rows != block.cols or columns.rows != block.rows:
        raise ValueError('Incompatible square block and column factor.')
    pivots = DomainMatrix.from_Matrix(block).rref()[1]
    if not pivots:
        if columns != sp.zeros(*columns.shape):
            return None
        return sp.zeros(columns.cols)
    principal = block.extract(pivots, pivots)
    selected = columns.extract(pivots, range(columns.cols))
    solved = principal.inv(method='DM')*selected
    if block.extract(range(block.rows), pivots)*solved != columns:
        return None
    return selected.T*solved


def coupling_residual(even, odd, factor_even, factor_odd, scale):
    """Reduce [[even,scale*XY^T],[scale*YX^T,odd]] PSD to at most4x4.

    Positive diagonal blocks and full-column-rank factors are hypotheses.
    After the two range conditions, residual=(scale^2*G_even)^(-1)-G_odd.
    Its PSD is equivalent to full PSD. Its nullity is the extra full nullity
    above the mean block kernel. For T use scale=-1/2; for U use4/15.
    """
    x, y, scale = sp.Matrix(factor_even), sp.Matrix(factor_odd), sp.Rational(scale)
    if x.cols != y.cols or scale == 0:
        raise ValueError('Equal factor widths and a nonzero scale are required.')
    if not x.cols:
        return dict(status='NO_MIXED_COUPLING', dimension=0, residual=sp.zeros(0), extra_nullity=0)
    ga, gc = metric_on_range(even, x), metric_on_range(odd, y)
    if ga is None or gc is None:
        return dict(status='RANGE_OBSTRUCTION', even_in_range=ga is not None, odd_in_range=gc is not None)
    residual = ga.inv(method='DM')/(scale*scale)-gc
    return dict(status='EXACT_SMALL_COUPLING_RESIDUAL', dimension=x.cols,
                even_metric=ga, odd_metric=gc, residual=residual,
                scope='Full block PSD iff residual PSD, conditional on positive diagonal blocks. Nullity(full)=nullity(even)+nullity(odd)+nullity(residual) when PSD.')


def all_matchings(unmatched=tuple(range(10)), current=None):
    current = {} if current is None else current
    if not unmatched:
        yield [current[i] for i in range(10)]
        return
    i = unmatched[0]
    for j in unmatched[1:]:
        rest = tuple(x for x in unmatched if x not in (i, j))
        yield from all_matchings(rest, current | {i: j, j: i})


def report():
    # The inertia helper is needed only for own small algebraic examples.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        from h_nullity_volume import rational_inertia
    except ModuleNotFoundError:
        from codex_h_nullity_volume import rational_inertia

    histogram = Counter(matching_partition(partner) for partner in all_matchings())
    assert sum(histogram.values()) == 945 and len(histogram) == 7
    cases = []
    for partition, count in sorted(histogram.items()):
        # On each alternating2r-cycle, reflection exchanges the two matchings.
        p, start = list(range(10)), 0
        for pairs in partition:
            length = 2*pairs
            for j in range(length):
                p[start+j] = start+(-j) % length
            start += length
        data = geometric_defect(p)
        assert data['matching_partition'] == partition
        cases.append(dict(partition=partition, remated_matchings=count,
                          defect_rank=2*data['coupling_rank'], coupling_rank=data['coupling_rank'],
                          mixed_defect_frobenius_squared=str(sp.trace(data['mixed_defect']*data['mixed_defect'].T))))
    by_rank = Counter()
    for case in cases:
        by_rank[case['coupling_rank']] += case['remated_matchings']
    assert by_rank == {0: 1, 1: 20, 2: 140, 3: 400, 4: 384}

    # Abstract parity blocks with the same rank-one defect/scales as a single
    # non-mate swap. They demonstrate why that defect alone is not a wall13.
    examples = []
    for mean_nullity, saturate in ((14, False), (13, True)):
        even_zeros = mean_nullity-2
        a = sp.diag(*([0]*even_zeros+[1]*(22-even_zeros)))
        c = sp.diag(*([0]*2+[1]*20))
        x, y = sp.eye(22)[:, even_zeros], sp.eye(22)[:, 2]
        if saturate:
            a[even_zeros, even_zeros] = c[2, 2] = sp.Rational(1, 2)
        lower = coupling_residual(a, c, x, y, -sp.Rational(1, 2))
        aprime = cprime = sp.diag(*([0]*2+[1]*20))
        upper = coupling_residual(aprime, cprime, x, y, sp.Rational(4, 15))
        li, ui = rational_inertia(lower['residual']), rational_inertia(upper['residual'])
        assert li['negative'] == ui['negative'] == 0
        assert mean_nullity+li['zero'] == 14 and 4+ui['zero'] == 4
        examples.append(dict(mean_nullity=mean_nullity, lower_residual=str(lower['residual'][0]),
                             upper_residual=str(upper['residual'][0]), T_nullity=14, U_nullity=4,
                             kernel_g_invariant=not saturate,
                             scope='Abstract positive parity blocks, not a binary adjacency or a Conway border.'))
    # A small full block confirms the residual inertia / extra-nullity identity.
    for cross_scale, expected in ((sp.Rational(1, 2), (4, 0, 0)), (1, (3, 0, 1)), (2, (3, 1, 0))):
        a, c, x, y = sp.eye(2), sp.eye(2), sp.Matrix([1, 0]), sp.Matrix([1, 0])
        small = coupling_residual(a, c, x, y, cross_scale)
        b = cross_scale*x*y.T
        full = a.row_join(b).col_join(b.T.row_join(c))
        inertia = rational_inertia(full)
        assert tuple(inertia[k] for k in ('positive', 'negative', 'zero')) == expected
        residual_inertia = rational_inertia(small['residual'])
        assert inertia['negative'] == residual_inertia['negative']
        assert inertia['zero'] == residual_inertia['zero']
    range_failure = coupling_residual(sp.diag(0, 1), sp.eye(2), sp.Matrix([1, 0]), sp.Matrix([1, 0]), 1)
    assert range_failure['status'] == 'RANGE_OBSTRUCTION'
    return dict(status='EXACT_GEOMETRIC_DEFECT_COUPLING_RANK_AT_MOST_FOUR',
                formula='For g=h*p and Gamma g-invariant, D=K-gKg=(J4 tensor (M-pMp))/8 on the40 outer-star labels, zero on the4 overlap labels. gTg=T+D and gUg=U-(8/15)D.',
                ranks='If M union pMp has c alternating components on the ten outer letters, rankD=10-2c and mixed defect rank r=5-c<=4. Common matching edges count as components of size2.',
                parity='In orthonormal g parity, D=[[0,E],[E^T,0]], T_mixed=-E/2 and U_mixed=(4/15)E. These mixed blocks are FIXED by geometry, independently of Gamma.',
                exact_psd='Factor E=X*Y^T rationally. Under positive diagonal blocks and both range conditions, T PSD iff4*G_A^(-1)-G_C PSD, G_A=X^T A^+ X,G_C=Y^T C^+ Y. U PSD iff(225/16)*G_Aprime^(-1)-G_Cprime PSD. Both residuals have size r<=4.',
                nullity='Under T PSD, nullityT=nullity(T_mean)+nullity(lower_residual). Thus kerT is g-invariant iff the lower residual is positive definite; this includes the rank-zero case vacuously.',
                proof=[
                    'Intersection counts and the constant geometric term are unchanged by any outer permutation. Only the outer mate-incidence matrix changes, equally in each of the4x4 central-star blocks, giving the tensor formula. Its coefficient in the upper correction is-1/15 instead of+1/8, hence the upper defect ratio-8/15.',
                    'On an alternating cycle of length2s, M-pMp=M*(I-M*pMp). The product of the two matchings consists of two s-cycles, so the kernel has dimension2 and the rank is2s-2, including rank0 for a common edge. Sum over components. Since g is an involution exchanging the matchings, gDg=-D and each parity off-block has half the defect rank.',
                    'Writing T_mixed=a*X*Y^T, range compatibility permits Schur complementation on the positive supports. The nontrivial residual is (a^2*G_A)^(-1)-G_C, with the same negative and zero inertia as the full Schur complement outside its positive unaffected directions. The scales are a=-1/2 for T and a=4/15 for U.'
                ],
                geometric_types=cases, remated_matchings_by_coupling_rank=dict(by_rank),
                abstract_nullity14_examples=examples,
                peer805_interpretation='The reported N=gN for HB_1 means its rank-one lower residual is STRICTLY positive: the coupling adds no null direction. Its13 rather than14 null vectors are a property of the mean blocks in that lineage, not a consequence of rankD=2 alone.',
                limitations='No producer graph read or re-audited, no nullity14 graph constructed, and no family excluded. The945 count classifies remated geometric matchings, not adjacency matrices or means. The abstract examples do not impose all Conway geometry, binary entries or C1/C2.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('status', 'remated_matchings_by_coupling_rank', 'abstract_nullity14_examples', 'limitations')}))
