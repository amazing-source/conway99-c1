"""A mixed-relation objective for four-star borders, without any symmetry.

The producer supplies an admissible T-PSD border and side component
counts. This constructs a new residual and lifts its mixed relations;
it does not verify admissibility, PSD, automorphisms, or modular ranks.
The default fixtures are algebraic Gram matrices, NOT Conway graphs.
"""
from itertools import combinations
from pathlib import Path
import argparse
import json

import sympy as sp


LABELS = [(i, j) for i, j in combinations(range(14), 2)
          if j != (i ^ 1) and i < 4]
O = [i for i, p in enumerate(LABELS) if all(x < 4 for x in p)]
LEFT = [i for i, p in enumerate(LABELS) if p[0] < 2 and p[1] >= 4]
RIGHT = [i for i, p in enumerate(LABELS) if 2 <= p[0] < 4 and p[1] >= 4]


def support(matrix):
    """For a PSD matrix, independent columns index a PD principal minor."""
    return list(matrix.rref()[1])


def mixed_residual(T, c_left, c_right, target_nullity=14):
    """Input order is LABELS. Positivity is an input hypothesis.

    The scalar identities use rank(T_X)=23-c for a two-star side.
    R has dimension 19-c_left+delta. Under the hypotheses,
    nullity(T)=c_left+c_right+2-delta+nullity(R), and target14
    is exactly rank(R)<=7+c_right. No ODD9 or involution is assumed.
    """
    T = sp.Matrix(T)
    if T.shape != (44, 44) or T != T.T:
        raise ValueError('Expected a symmetric44x44 matrix.')
    o_local = support(T.extract(O, O))
    delta = 4-len(o_local)
    if delta not in (0, 1):
        raise ValueError('The overlap must have rank3 or4 under the stated geometry.')
    oi = [O[i] for i in o_local]
    F = T.extract(oi, oi)
    Fi = F.inv(method='DM')
    A = T.extract(LEFT, LEFT)-T.extract(LEFT, oi)*Fi*T.extract(oi, LEFT)
    C = T.extract(RIGHT, RIGHT)-T.extract(RIGHT, oi)*Fi*T.extract(oi, RIGHT)
    E = T.extract(LEFT, RIGHT)-T.extract(LEFT, oi)*Fi*T.extract(oi, RIGHT)
    al, cr = support(A), support(C)
    if len(al) != 19-c_left+delta or len(cr) != 19-c_right+delta:
        raise ValueError('Side component inputs do not match the required side-rank formula.')
    Ap, Cp, Ep = A.extract(al, al), C.extract(cr, cr), E.extract(al, cr)
    response = Cp.inv(method='DM')*Ep.T
    R = Ap-Ep*response
    null_basis = R.nullspace()
    lifted = []
    ai, ci = [LEFT[i] for i in al], [RIGHT[i] for i in cr]
    for x in null_basis:
        y = -response*x
        z = -Fi*(T.extract(oi, ai)*x+T.extract(oi, ci)*y)
        vector = sp.zeros(44, 1)
        for indices, values in ((ai, x), (ci, y), (oi, z)):
            for i, value in zip(indices, values):
                vector[i] = value
        # Kernel membership follows from the producer's PSD/range hypotheses.
        lifted.append(vector)
    side_relations = c_left+c_right+2-delta
    mixed = len(null_basis)
    return dict(delta=delta, overlap_rank=4-delta,
        side_relations=side_relations, mixed_relations=mixed,
        residual_dimension=R.rows, residual_rank=R.rows-mixed,
        conditional_full_nullity=side_relations+mixed,
        target_nullity=target_nullity,
        target_residual_rank=21+c_right-target_nullity,
        target_mixed_relations=target_nullity-side_relations,
        residual=R, left_support=ai, right_support=ci,
        overlap_support=oi, lifted_mixed_relations=lifted)


def from_adjacency(gamma, c_left, c_right, labels=LABELS, target_nullity=14):
    """Reorder an already accepted producer matrix; do not validate it."""
    labels = [tuple(sorted(p)) for p in labels]
    if len(labels) != 44 or set(labels) != set(LABELS):
        raise ValueError('Expected exactly the44 four-star labels.')
    order = [labels.index(p) for p in LABELS]
    gamma = sp.Matrix(gamma).extract(order, order)
    T8 = sp.Matrix(44, 44, lambda i, j: 24*int(i == j)-8*gamma[i, j]
                   -3*len(set(LABELS[i]) & set(LABELS[j]))
                   -sum((x ^ 1) in LABELS[j] for x in LABELS[i])+2)
    return mixed_residual(T8, c_left, c_right, target_nullity)


def cross_trade_factors(kernel):
    """All real cross changes preserving a supplied FULL T kernel.

    Delta=P_left*Z*P_right.T, with Z arbitrary. Binary entry bounds, C1'
    and C2 are additional constraints, not imposed or relaxed away here.
    No producer kernel is recomputed by this function.
    """
    N = sp.Matrix(kernel)
    if N.rows != 44:
        raise ValueError('Expected44 rows in the common LABELS order.')
    nl, nr = N.extract(LEFT, range(N.cols)), N.extract(RIGHT, range(N.cols))
    pl, pr = nl.T.nullspace(), nr.T.nullspace()
    PL = sp.Matrix.hstack(*pl) if pl else sp.zeros(20, 0)
    PR = sp.Matrix.hstack(*pr) if pr else sp.zeros(20, 0)
    return dict(left_factor=PL, right_factor=PR,
                parameter_rows=PL.cols, parameter_columns=PR.cols,
                real_dimension=PL.cols*PR.cols,
                kernel_equations_alone_cannot_force_any_h_p=max(PL.cols, PR.cols) > 10)


def overlap_cases():
    """Only the19 possible four-label overlap graphs, with an exact DD proof."""
    labels = [LABELS[i] for i in O]
    edges = list(combinations(range(4), 2))
    ranks = {3: 0, 4: 0}
    for mask in range(1 << len(edges)):
        G = sp.zeros(4)
        for k, (i, j) in enumerate(edges):
            if mask >> k & 1:
                G[i, j] = G[j, i] = 1
        if any(sum(G[i, j] for j, q in enumerate(labels) if c in q) > 1
               for i in range(4) for c in range(4)):
            continue
        T8 = sp.Matrix(4, 4, lambda i, j: 24*int(i == j)-8*G[i, j]
                       -3*len(set(labels[i]) & set(labels[j]))
                       -sum((x ^ 1) in labels[j] for x in labels[i])+2)
        margins = [T8[i, i]-sum(abs(T8[i, j]) for j in range(4) if i != j)
                   for i in range(4)]
        assert all(m >= 0 for m in margins)
        grid = all(G[i, j] == int(bool(set(labels[i]) & set(labels[j])))
                   for i, j in edges)
        assert (not any(margins)) == grid
        # Geometric C4 edges always have strictly negative matrix entries.
        # Irreducible diagonal dominance proves PD unless every margin is zero.
        expected_rank = 3 if grid else 4
        assert T8.rank() == expected_rank
        ranks[expected_rank] += 1
    assert ranks == {3: 1, 4: 18}
    return dict(C1_overlap_patterns=19, rank_histogram=ranks)


def gram_fixture(c_left, c_right, delta, mixed):
    """A rational PSD fixture with forced ranks; not binary/SRG geometry."""
    r0, ra, rc = 4-delta, 19-c_left+delta, 19-c_right+delta
    assert 0 <= mixed <= min(ra, rc)
    T = sp.zeros(44)
    for i in O[:r0]+LEFT[:ra]+RIGHT[:rc]:
        T[i, i] = 1
    for j in range(min(ra, rc)):
        T[LEFT[j], RIGHT[j]] = T[RIGHT[j], LEFT[j]] = 1 if j < mixed else sp.Rational(1, 2)
    # A nontrivial rational congruence exercises the overlap lift.
    change = sp.eye(44)
    for i, j in enumerate(LEFT+RIGHT):
        change[O[i % r0], j] = sp.Rational((i % 5)-2, 3)
    return change.T*T*change


PROOF = [
    'Let O be the four labels02,03,12,13, and X,Y the two24-label sides with intersectionO. Write c_l,c_m for their component counts. The accepted two-star formula gives rank(T_X)=23-c_l and rank(T_Y)=23-c_m.',
    'On O, T has diagonal5/2, entries-1/4-Gamma on the geometric C4, and entries-Gamma on its diagonals. C1 upper bounds forbid a diagonal edge from sharing an endpoint with a C4 edge. All row sums of absolute off-diagonal entries are at most5/2. The geometric C4 connects the matrix. Irreducible diagonal dominance gives rank4 unless all four C4 edges are present, when the matrix is5/4 times its Laplacian and has rank3. Thus delta=null(T_O) is1 exactly for that grid, otherwise0.',
    'Under T PSD, every principal kernel extends by zero to a full kernel vector. The embedded side kernels intersect exactly in the embedded kernel of T_O. Hence their sum has dimension(c_l+1)+(c_m+1)-delta. The remaining nullity m is the dimension of genuinely mixed relations, modulo these side relations.',
    'Eliminate the positive support of O. The remaining blocks A,C have ranks19-c_l+delta and19-c_m+delta. Choose positive principal supports and let E be their cross block. Congruence gives the residual R=A-E*C^-1*E^t. Its nullity is exactly m. After normalization, the cross map A^-1/2*E*C^-1/2 is a contraction; its singular values equal to1 are exactly these mixed relations.',
    'Therefore null(T)=c_l+c_m+2-delta+null(R), and rank(R)=21+c_m-null(T). In particular, the Conway target null(T)>=14 is exactly rank(R)<=7+c_m. These identities require no h*p symmetry and no ODD9.',
    'For the producer profile c=(3,2),nullity11, delta0 means7 side+4 mixed relations and a16x16 residual of rank12. Delta1 means6 side+5 mixed relations and a17x17 residual of rank12. Target14 requires the residual rank to fall to9: exactly three additional mixed relations at fixed c. No value of delta for that seed is assumed here.',
    'For c=(2,2),nullity10, the corresponding residual has dimension17 or18 and rank13. Target14 again requires rank<=9, hence four additional mixed relations at fixed c. The absence of h*p alone neither supplies these relations nor certifies a trivial full automorphism group.',
    'A residual null vector x gives y=-C^-1*E^t*x; adding the overlap coefficients -T_O^-1*(T_OL*x+T_OR*y) on its positive support lifts it to a full mixed relation. The provided API constructs these objects from an already accepted producer border; it does not repeat producer admissibility or PSD validation.',
    'Fix both24-label sides and change only the20x20 cross adjacency block by Delta. For a full kernel basis N, preserving N is exactly Delta*N_R=0 and Delta^t*N_L=0. Since the kernels supported off L and off R have dimensions c_m+1 and c_l+1, respectively, rank(N_L)=nu-c_m-1 and rank(N_R)=nu-c_l-1. Thus all such real changes are P_L*Z*P_R^t, with factor dimensions21+c_m-nu and21+c_l-nu. These equations preserve the central C1 equalities because the four star indicators belong to N.',
    'For c=(3,2),nu11, the cross space has dimension12*13=156. At nu14 it has dimension9*10=90. These are real linear dimensions, not counts of binary trades or admissible graphs. C1-prime, C2, binary entry bounds and U positivity still constrain actual moves. Small real changes preserve T positivity on its positive support, but need not satisfy the other constraints.',
    'A fixed h*p acts on either20-label side by [[0,P],[P,0]], where P permutes the ten outer letters. Every eigenspace has dimension at most10: one ten-coordinate half determines the other. If ALL cross changes u*v^t in the factor spaces were fixed, the two permutations would have to act by scalar reciprocal eigenvalues on those factor spaces. This is impossible if either factor dimension exceeds10.',
    'Consequently, the kernel-preservation equations alone cannot force any fixed h*p when nu<11+max(c_l,c_m). A finite union of proper affine subspaces cannot cover the real solution space, so a generic real cross assignment satisfying those linear equations avoids every h*p. This is a statement about unrestricted real coefficients, not a construction of a binary PSD/C2 graph. At c=(3,2), the dimensional obstruction to forcing symmetry lasts through nu13; at nu14 it disappears, which permits but does not prove symmetry forcing.'
]


def serializable(result):
    if isinstance(result, dict):
        return {key: serializable(value) for key, value in result.items()}
    if isinstance(result, (list, tuple)):
        return [serializable(value) for value in result]
    if isinstance(result, sp.MatrixBase):
        return [[str(x) for x in result.row(i)] for i in range(result.rows)]
    return result


def run():
    cases = [(3, 2, 0, 4), (3, 2, 1, 5), (3, 2, 0, 7),
             (3, 2, 1, 8), (2, 2, 0, 4), (2, 2, 1, 5)]
    reports, trade_reports = [], []
    for cl, cm, delta, mixed in cases:
        T = gram_fixture(cl, cm, delta, mixed)
        result = mixed_residual(T, cl, cm)
        assert result['mixed_relations'] == mixed and result['delta'] == delta
        assert all(T*v == sp.zeros(44, 1) for v in result['lifted_mixed_relations'])
        assert result['conditional_full_nullity'] == 44-T.rank()
        reports.append({key: value for key, value in result.items()
                        if key not in ('residual', 'lifted_mixed_relations', 'left_support',
                                       'right_support', 'overlap_support')})
        if (cl, cm, delta, mixed) in ((3, 2, 0, 4), (3, 2, 0, 7)):
            N = sp.Matrix.hstack(*T.nullspace())
            trades = cross_trade_factors(N)
            PL, PR = trades['left_factor'], trades['right_factor']
            change = sp.zeros(44)
            cross = PL[:, 0]*PR[:, 0].T
            for i, j in ((i, j) for i in range(20) for j in range(20)):
                change[LEFT[i], RIGHT[j]] = change[RIGHT[j], LEFT[i]] = cross[i, j]
            assert change*N == sp.zeros(44, N.cols)
            nu = result['conditional_full_nullity']
            assert PL.cols == 21+cm-nu and PR.cols == 21+cl-nu
            trade_reports.append(dict(nullity=nu, **{key: value for key, value in trades.items()
                                      if key not in ('left_factor', 'right_factor')}))
    return dict(status='SYMMETRY_FREE_MIXED_RELATION_OBJECTIVE', overlap=overlap_cases(),
                algebraic_gram_fixtures=reports, fixtures_are_not_graphs=True,
                kernel_preserving_real_spaces=trade_reports, proof=PROOF)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path,
                        help='JSON with gamma,c_left,c_right and optional labels,target_nullity')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = (serializable(from_adjacency(**json.loads(args.candidate.read_text(encoding='utf-8'))))
              if args.candidate else run())
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('proof', 'residual', 'lifted_mixed_relations')}, indent=2))


if __name__ == '__main__':
    main()
