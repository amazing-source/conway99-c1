"""Strict integer PSD cuts, a fractional ODD8 model and an ODD9 diagnostic.

For every balanced20-label outer subset S, binary C1 and T PSD imply
e(O union S)<=48, improving49 from ordinary PSD. No symmetry, U, C2,
O-grid assumption or proof of ODD9 is used for this cut.

This is NOT a counterexample to binary C1/C1'/C2, T/U-positive ODD9.
Universal binary ODD9 was subsequently refuted by LAB message843;
that producer result is accepted here without re-verification.
The model satisfies the linear counts, entry bounds and T/U positivity,
and its internal star matchings belong to the exact matching polytope.
It violates C2 and is fractional. A parity argument excludes its specific
extra relation for every binary C1 border.
No producer graph or kernel is read by the default calculation.
"""
from fractions import Fraction
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import argparse
import json

import sympy as sp
from sympy.polys.matrices import DomainMatrix


LABELS = [(i, j) for i, j in combinations(range(14), 2)
          if j != (i ^ 1) and i < 4]
INDEX = {p: i for i, p in enumerate(LABELS)}
SCALE = 3600


def rank(matrix):
    return DomainMatrix.from_Matrix(sp.Matrix(matrix)).rank()


def positive_rank(matrix):
    """Small exact PSD test by rational Schur complements, for our8x8 model."""
    A = [[Fraction(x) for x in row] for row in matrix.tolist()]
    answer = 0
    while A:
        if any(A[i][i] < 0 for i in range(len(A))):
            raise AssertionError('Negative diagonal in an exact Schur complement.')
        if any(A[i][i] == 0 and any(A[i]) for i in range(len(A))):
            raise AssertionError('Nonzero row at a zero PSD diagonal.')
        pivot = next((i for i in range(len(A)) if A[i][i]), None)
        if pivot is None:
            return answer
        keep = [i for i in range(len(A)) if i != pivot]
        A = [[A[i][j]-A[i][pivot]*A[pivot][j]/A[pivot][pivot]
              for j in keep] for i in keep]
        answer += 1
    return answer


def stars():
    return sp.Matrix(44, 4, lambda i, c: int(c in LABELS[i]))


def primitive(vector):
    denominator = lcm(*(int(x.q) for x in vector))
    entries = [int(denominator*x) for x in vector]
    common = gcd(*entries)
    entries = [x//common for x in entries]
    if next(x for x in entries if x) < 0:
        entries = [-x for x in entries]
    return entries


def kernel_projection_profile(kernel, c_left, labels=LABELS):
    """Consume a COMPLETE producer kernel under T PSD; no T is inspected.

    The columns must be a basis, in the supplied label order. The input
    hypotheses and rank(T_X)=23-c_left are not re-verified here.
    """
    labels = [tuple(sorted(p)) for p in labels]
    if len(labels) != 44 or set(labels) != set(LABELS):
        raise ValueError('Expected exactly the44 four-star labels.')
    order = [labels.index(p) for p in LABELS]
    N = sp.Matrix(kernel)
    if N.rows != 44:
        raise ValueError('Expected44 rows in the kernel basis.')
    N = N.extract(order, range(N.cols))
    C = sp.Matrix(10, 44, lambda y, i: int(LABELS[i] in ((2, y+4), (3, y+4))))
    projected = C*N
    rho = rank(projected)
    defect = N.cols-c_left-2-rho
    if not 0 <= defect <= 9:
        raise ValueError('Input hypotheses are inconsistent with the dimension formula.')
    result = dict(input_kernel_dimension=N.cols, c_left=c_left,
                  even_sum_projection_rank=rho, odd_rank_gain=9-defect,
                  ODD9_defect=defect,
                  scope='Conditional on a complete kernel basis, T PSD and the side-rank formula.')
    if defect:
        star_difference = stars()[:, 2]-stars()[:, 3]
        for coefficients in projected.nullspace():
            n = N*coefficients
            mean = sum(n[INDEX[2, y]] for y in range(4, 14))/10
            n -= mean*star_difference
            if any(n[INDEX[2, y]] for y in range(4, 14)):
                assert all(n[INDEX[2, y]] == -n[INDEX[3, y]] for y in range(4, 14))
                assert sum(n[INDEX[2, y]] for y in range(4, 14)) == 0
                result['extra_odd_relation'] = primitive(n)
                break
        assert 'extra_odd_relation' in result
    return result


def flat_odd_cut(left_plus, right_plus, assume_overlap_grid=False):
    """Strict integer T-PSD cut: e(O union S)<=48; grid special case e(S)<=44.

    Pick five positive outer letters on star0, their complement on star1,
    five on star2 and their complement on star3. Then |S|=20, with five
    labels per central star and two per outer letter. The ordinary PSD
    bound on O union S is49. This uses integrality and T PSD, not U/C2.
    """
    left_plus, right_plus = set(left_plus), set(right_plus)
    if any(len(a) != 5 or not a <= set(range(4, 14)) for a in (left_plus, right_plus)):
        raise ValueError('Choose five outer letters4..13 on each side.')
    positive = [i for i, (c, y) in enumerate(LABELS) if y >= 4 and (
        (c == 0 and y in left_plus) or (c == 1 and y not in left_plus)
        or (c == 2 and y in right_plus) or (c == 3 and y not in right_plus))]
    assert len(positive) == 20
    selected = positive if assume_overlap_grid else sorted(positive+[
        i for i, p in enumerate(LABELS) if p[1] < 4])
    bound = 44 if assume_overlap_grid else 48
    return dict(selected_indices=selected, selected_labels=[LABELS[i] for i in selected],
                positive_outer_indices=positive,
                edge_coefficients=[[i, j, 1] for i, j in combinations(selected, 2)],
                upper_bound=bound, ordinary_PSD_upper_bound=bound+1,
                hypotheses='Binary C1 border, T PSD.'+(
                    ' O is the geometric grid.' if assume_overlap_grid else ''))


def flat_odd_cuts():
    """31752 indexed directions, identifying a cut with its complement."""
    subsets = list(combinations(range(4, 14), 5))
    for left in subsets:
        if 4 not in left:
            continue
        for right in subsets:
            yield flat_odd_cut(left, right)


def model():
    P = sp.Matrix([[1, 1, 2, 2], [1, 1, 2, 2],
                   [2, 2, 1, 1], [2, 2, 1, 1]])
    # Diagonal, central-mate, other-line same sign, other-line opposite sign.
    q0, q1, q2, q3 = map(sp.Rational, ('2/25', '-9/100', '2/25', '-7/80'))
    Q = sp.Matrix([[q0, q1, q2, q3], [q1, q0, q3, q2],
                   [q2, q3, q0, q1], [q3, q2, q1, q0]])
    t = sp.Matrix([1, -1]*5)
    H = (sp.ones(10)-sp.eye(10))/9
    D = t*t.T-sp.eye(10)+H
    outer = sp.kronecker_product(P, H)+sp.kronecker_product(Q, D)
    G = sp.zeros(44)
    for i, p in enumerate(LABELS):
        for j, q in enumerate(LABELS):
            if p[1] < 4 and q[1] < 4 and i != j:
                G[i, j] = int(bool(set(p) & set(q)))
            if p[1] >= 4 and q[1] >= 4:
                G[i, j] = outer[10*p[0]+p[1]-4, 10*q[0]+q[1]-4]
    K = sp.Matrix(44, 44, lambda i, j: sp.Rational(
        3*len(set(LABELS[i]) & set(LABELS[j]))
        +sum((x ^ 1) in LABELS[j] for x in LABELS[i])-2, 8))
    L = sp.Matrix(44, 44, lambda i, j: sp.Rational(
        4*len(set(LABELS[i]) & set(LABELS[j]))
        -sum((x ^ 1) in LABELS[j] for x in LABELS[i])+2, 15))
    GI, TI, UI = SCALE*G, SCALE*(3*sp.eye(44)-G-K), SCALE*(4*sp.eye(44)+G-L)
    assert all(x.q == 1 for A in (GI, TI, UI) for x in A)
    assert min(GI) == 0 and max(GI) == SCALE and not any(GI.diagonal())
    for i, p in enumerate(LABELS):
        for c in range(14):
            value = sum(GI[i, j] for j, q in enumerate(LABELS) if c in q)
            cap = SCALE*(1 if c in p or (c ^ 1) in p else 2)
            assert value == cap if c < 4 else value <= cap

    def lift(center, exterior):
        return sp.Matrix([0 if p[1] < 4 else center[p[0]]*exterior[p[1]-4]
                          for p in LABELS])

    characters = [sp.Matrix(v) for v in ((1, 1, 1, 1), (1, 1, -1, -1),
                                        (1, -1, 1, -1), (1, -1, -1, 1))]
    plus, minus = [], []
    for i in range(4):
        a, b = sp.zeros(10, 1), sp.zeros(10, 1)
        a[2*i] = a[2*i+1] = 1
        a[8] = a[9] = -1
        b[2*i], b[2*i+1], b[8], b[9] = 1, -1, -1, 1
        plus.append(a); minus.append(b)
    assert rank(sp.Matrix.hstack(sp.ones(10, 1), t, *plus, *minus)) == 10
    modes = []
    positive_T = positive_U = 0
    for k, center in enumerate(characters):
        pc = (center.T*P*center)[0]/4
        qc = (center.T*Q*center)[0]/4
        for name, vectors, mate in (('t', [t], -1), ('mate_plus_zero_sum', plus, 1),
                                    ('mate_minus_perp_t', minus, -1)):
            h_eigen = -sp.Rational(1, 9)
            d_eigen = sp.Rational(80 if name == 't' else -10, 9)
            gamma_eigen = pc*h_eigen+qc*d_eigen
            geometric_K = sp.Rational(3+mate, 2) if k == 0 else 0
            geometric_L = sp.Rational(4*(4-mate), 15) if k == 0 else 0
            te, ue = 3-gamma_eigen-geometric_K, 4+gamma_eigen-geometric_L
            assert te >= 0 and ue > 0
            for exterior in vectors:
                v = lift(center, exterior)
                assert TI*v == SCALE*te*v and UI*v == SCALE*ue*v
            positive_T += len(vectors)*int(bool(te > 0))
            positive_U += len(vectors)
            modes.append(dict(central_character=list(center), exterior_mode=name,
                              multiplicity=len(vectors), T_eigenvalue=str(te), U_eigenvalue=str(ue)))
    triv = []
    for p in ((0, 2), (0, 3), (1, 2), (1, 3)):
        e = sp.zeros(44, 1); e[INDEX[p]] = 1; triv.append(e)
    for c in range(4):
        e = sp.zeros(4, 1); e[c] = 1; triv.append(lift(e, sp.ones(10, 1)))
    W = sp.Matrix.hstack(*triv)
    rank_t0 = positive_rank(W.T*TI*W)
    rank_u0 = positive_rank(W.T*UI*W)
    assert (rank_t0, rank_u0) == (3, 4)
    assert (positive_T+rank_t0, positive_U+rank_u0) == (38, 40)
    extra = lift(characters[2], t)
    grid = sp.Matrix([int(p[1] < 4) for p in LABELS])
    N = sp.Matrix.hstack(stars(), grid, extra)
    assert rank(N) == 6 and TI*N == sp.zeros(44, 6)
    assert GI*extra == 3*SCALE*extra and K*extra == sp.zeros(44, 1)
    profile = kernel_projection_profile(N, 2)
    assert profile['odd_rank_gain'] == 8
    witness = sp.Matrix(profile['extra_odd_relation'])
    assert TI*witness == sp.zeros(44, 1)
    G2 = GI*GI
    violation = max((G2[i, j]+SCALE*GI[i, j]+SCALE*SCALE*(
        len(set(LABELS[i]) & set(LABELS[j]))-2), i, j)
        for i in range(44) for j in range(i))
    excess, i, j = violation
    assert excess > 0
    matching = matching_average()
    assert GI.extract([INDEX[0, y] for y in range(4, 14)],
                      [INDEX[0, y] for y in range(4, 14)]) == SCALE*matching
    cut = flat_odd_cut(range(4, 14, 2), range(4, 14, 2))
    internal = sum(GI[i, j] for i, j, _ in cut['edge_coefficients'])/SCALE
    assert internal == 49
    return dict(status='EXACT_ODD9_INTEGER_CUTS_AND_RELAXATION_OBSTRUCTION',
        binary_ODD9_status='REFUTED_BY_LAB_MESSAGE_843',
        binary_ODD9_provenance='Producer exact counterexamples accepted without re-verification; this fractional model is separate.',
        fractional_model_is_not_a_graph=True, labels=LABELS,
        scale=SCALE, adjacency_scaled=[[int(x) for x in GI.row(i)] for i in range(44)],
        formula=dict(P=P.tolist(), Q=[[str(x) for x in Q.row(i)] for i in range(4)],
                     t=list(t), H='(J10-I10)/9', D='t*t^t-I10+H',
                     Gamma='C4 on O, no O-outer edges, P tensor H + Q tensor D on40.'),
        C1=True, C1prime=True, entry_bounds_0_1=True, diagonal_zero=True,
        T_PSD=True, U_PSD=True, T_nullity=6, U_nullity=4,
        exact_outer_modes=modes, trivial_8d_positive_ranks=[rank_t0, rank_u0],
        internal_matching_polytope=dict(explicit_matchings=225,
            same_sign_edge_weight='1/5', opposite_sign_edge_weight='1/25'),
        side_components=[2, 2], odd_profile=profile,
        extra_relation=list(extra),
        strict_integer_cut=dict(selected_labels=cut['selected_labels'],
            upper_bound=48, ordinary_PSD_upper_bound=49, fractional_model_value=str(internal),
            indexed_h_odd_directions=126*252,
            cut_energy_identity='q^t*T*q=8*(49-e(O union S))',
            binary_strict_energy_lower_bound=8,
            overlap_grid_specialization='e(S)<=44, improving ordinary PSD bound45'),
        binary_saturation_fixture=binary_saturation_fixture(),
        non_grid_energy_identity=non_grid_identity_fixture(),
        C2_violation=dict(labels=[LABELS[i], LABELS[j]],
                          weighted_common_neighbours=str(sp.Rational(G2[i, j], SCALE*SCALE)),
                          edge_weight=str(sp.Rational(GI[i, j], SCALE)),
                          excess=str(sp.Rational(excess, SCALE*SCALE))),
        proof=PROOF)


def pairings(four):
    a = four[0]
    for b in four[1:]:
        rest = [x for x in four if x not in (a, b)]
        yield [(a, b), tuple(rest)]


def matching_average():
    """Uniformly average225 actual perfect matchings on ten vertices."""
    plus, minus = list(range(0, 10, 2)), list(range(1, 10, 2))
    counts, total = sp.zeros(10), 0
    for a, b in product(plus, minus):
        for left, right in product(pairings([x for x in plus if x != a]),
                                   pairings([x for x in minus if x != b])):
            edges = [(a, b)]+left+right
            assert sorted(x for edge in edges for x in edge) == list(range(10))
            for i, j in edges:
                counts[i, j] += 1; counts[j, i] += 1
            total += 1
    assert total == 225
    expected = sp.Matrix(10, 10, lambda i, j: 0 if i == j else
                         sp.Rational(1, 5 if i % 2 == j % 2 else 25))
    assert counts/total == expected
    return expected


def binary_saturation_fixture():
    """Our C1 binary saturation example is NOT PSD; export its negative witness."""
    G = sp.zeros(44)

    def edge(p, q):
        i, j = INDEX[p], INDEX[q]
        assert i != j and not G[i, j]
        G[i, j] = G[j, i] = 1

    for p, q in combinations(((0, 2), (0, 3), (1, 2), (1, 3)), 2):
        if set(p) & set(q):
            edge(p, q)
    for c in range(4):
        for y, z in ((0, 1), (2, 4), (6, 8), (3, 5), (7, 9)):
            edge((c, 4+y), (c, 4+z))
    mate = [i ^ 1 for i in range(10)]
    rotate = [2*((i//2+1) % 5)+i % 2 for i in range(10)]
    flip_rotate = [x ^ 1 for x in rotate]
    special = list(range(6))+[9, 8, 7, 6]
    for c, d, perms in ((0, 1, [mate]), (2, 3, [mate]),
                        (0, 2, [mate, flip_rotate]), (0, 3, [mate, special]),
                        (1, 2, [mate, flip_rotate]), (1, 3, [list(range(10)), rotate])):
        for permutation in perms:
            for i, j in enumerate(permutation):
                edge((c, 4+i), (d, 4+j))
    for i, p in enumerate(LABELS):
        for c in range(4):
            cap = 1 if c in p or (c ^ 1) in p else 2
            assert sum(G[i, j] for j, q in enumerate(LABELS) if c in q) == cap
    cut = flat_odd_cut(range(4, 14, 2), range(4, 14, 2))
    assert sum(G[i, j] for i, j, _ in cut['edge_coefficients']) == 49
    positive = set(cut['positive_outer_indices'])
    q = sp.Matrix([0 if p[1] < 4 else (1 if i in positive else -1)
                   for i, p in enumerate(LABELS)])
    K8 = sp.Matrix(44, 44, lambda i, j:
        3*len(set(LABELS[i]) & set(LABELS[j]))
        +sum((x ^ 1) in LABELS[j] for x in LABELS[i])-2)
    T8 = 24*sp.eye(44)-8*G-K8
    assert K8*q == sp.zeros(44, 1) and (q.T*T8*q)[0] == 0
    i = INDEX[0, 4]
    s = (T8*q)[i]/8
    assert s % 2 == 1
    v = 5*q
    v[i] -= 2*s
    value = (v.T*T8*v)[0]
    assert value == -80*s*s < 0
    return dict(scope='Our binary C1 example at the forbidden PSD equality; not a valid PSD border.',
        adjacency_rows_hex=[format(sum(int(G[i, j]) << j for j in range(44)), '011x')
                            for i in range(44)],
        induced_edges=49, flat_direction_energy=0, selected_row=LABELS[i],
        residual=str(s), negative_witness=[int(x) for x in v],
        quadratic_value_for_8T=int(value))


def non_grid_identity_fixture():
    """Check the general identity on an O-empty C1 fractional fixture."""
    G = sp.zeros(44)
    for i, p in enumerate(LABELS):
        for j, q in enumerate(LABELS):
            if (p[1] < 4) != (q[1] < 4):
                G[i, j] = sp.Rational(1, 10)
            elif p[1] >= 4 and q[1] >= 4 and p[1] != q[1]:
                G[i, j] = sp.Rational(4 if p[0]//2 == q[0]//2 else 9, 45)
    for i, p in enumerate(LABELS):
        for c in range(4):
            assert sum(G[i, j] for j, q in enumerate(LABELS) if c in q) == (
                1 if c in p or (c ^ 1) in p else 2)
    for lp, rp in ((range(4, 14, 2), range(4, 14, 2)), (range(4, 9), range(9, 14)),
                   ((4, 5, 7, 10, 12), (5, 6, 9, 11, 13))):
        cut = flat_odd_cut(lp, rp)
        positive = set(cut['positive_outer_indices'])
        q = sp.Matrix([0 if p[1] < 4 else (1 if i in positive else -1)
                       for i, p in enumerate(LABELS)])
        energy = (q.T*(3*sp.eye(44)-G)*q)[0]  # Kq=0 from the balances.
        edges = sum(G[i, j] for i, j, _ in cut['edge_coefficients'])
        assert energy == 8*(49-edges)
    return dict(overlap_edges=0, own_C1_fractional_directions=3, identity='PASS',
                scope='Only the general energy identity is tested; no PSD claim for this fixture.')


PROOF = [
    'Kernel diagnostic: under T PSD, a relation of the Gram vectors on a subspace extends to a full kernel vector. The projection of N=kerT onto the new20 labels has kernel kerT_X of dimension c_l+1. The even-sum map C_m(n)_y=n_2y+n_3y has rank rho. Thus its odd projected relations have dimension nu-rho-c_l-1, and the odd rank gain is10 minus that number, or11+c_l-nu+rho. The known star2-minus-star3 relation accounts for one odd dependence. Hence ODD9 defect=nu-c_l-2-rho.',
    'A deficient even-sum projection produces a full kernel vector whose new coordinates are antisymmetric. Subtracting the average times the known star difference makes their ten coefficients sum to zero. A nonzero centered coefficient vector is an actual additional odd relation. The diagnostic consumes a producer kernel and never recomputes its admissibility, PSD or rank.',
    'In the explicit fractional model, the four central characters diagonalize P and Q. The exterior decomposition is: constants; t=(1,-1)^5; the4-dimensional mate-even zero-sum space; and the4-dimensional mate-odd space perpendicular to t. H has eigenvalue-1/9 on all three nonconstant parts; D has80/9 on t and-10/9 on the other eight dimensions. The exported36 exact common eigenvectors have nonnegative T and positive U eigenvalues. The remaining8-dimensional quotient has exact PSD ranks3 and4. Hence nullities6 and4, respectively.',
    'The T kernel has the four star indicators, the O-grid indicator, and n(c,y)=(1,-1,1,-1)_c*t_y with n|O=0. These six vectors are independent and exhaust it. Both weighted two-star networks have two components: O, and the connected20 exterior labels. The even-sum projection has rank1, so the odd rank gain is8.',
    'The fractional entries satisfy C1, C1-prime and the interval[0,1] exactly. Each internal ten-vertex matching matrix is an explicit average of225 actual matchings: select one cross edge between the two five-element sign classes, then one of three matchings on each remaining four-element set. Its same-sign entries are1/5 and its opposite-sign entries1/25. Thus adding all odd-set matching inequalities does not remove this fractional example.',
    'The model violates the actual quadratic C2 inequality; an exact offending pair is exported. It therefore does not refute ODD9, nor show that integrality alone or C2 alone is indispensable. It shows that linear star counts, entry bounds, internal matching polytopes, and simultaneous T/U positivity are insufficient.',
    'Binary parity obstruction, without an O-grid assumption: at any outer vertex, C1 sums to6 over the four central stars. An O-neighbour is counted twice and an outer neighbour once, so its outer degree is6-2*d_O, hence even. Let n vanish on O, have odd integer coordinates at every outer vertex, and have zero root-letter incidence. Then K*n=0. A T-kernel relation would imply Gamma*n=3n. The left side is a sum of an even number of odd integers and is even, while the right side is odd. Contradiction. A general ODD9 failure need not have these incidence and parity properties. Universal binary ODD9 has been refuted by the separate producer counterexamples reported in LAB message843; this restricted obstruction remains valid.',
    'General strict cut: choose S of20 outer labels, with five per central star and two per outer letter. Put q=+1 on S,-1 on its outer complement,0 on O; Kq=0. Write H=e(O,F), H_S=e(O,S), E0=e(O). Summing C1 on O gives H=16-4E0. Summing on S gives2e(S)+cut(S,F-S)=120-2H_S. Also e(F)=120-H. Substitution into q^t*T*q=120-2e(F)+4cut yields exactly8*(49-e(O union S)). T PSD gives e(O union S)<=49. Equality would put q in the kernel and contradict parity. Since this edge count is integral, e(O union S)<=48 and q^t*T*q>=8. No U, C2 or symmetry is used.',
    'If O happens to be a grid, C1 forbids O-F edges, so the general cut specializes to e(S)<=44. Equivalently the6-regular outer graph has cut(S,F-S)>=32, versus30 from the ordinary PSD inequality.',
    'At the forbidden binary equality e(O union S)=49, let s_i=(T*q)_i at any outer vertex. It is an odd nonzero integer. Since T_ii=5/2, v=5q-2*s_i*e_i has v^t*T*v=-10*s_i^2, or v^t*(8T)*v=-80*s_i^2. The report includes our explicit C1 binary equality fixture and its exact negative witness; it is intentionally not a PSD border.',
    'The h-odd subclass chooses five positive letters on star0 and independently five on star2; the other two stars use the complements. Identifying q with-q leaves126*252=31752 indexed cuts. The API generates any selected cut or iterates them; no list of31752 dense rows is materialized by default. The fractional model has e(O union S)=49 and is separated by the new strict integer cut.'
]


def json_safe(value):
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, sp.Integer):
        return int(value)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel-input', type=Path,
                        help='JSON with kernel,c_left, and optionally labels; producer hypotheses required.')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = (kernel_projection_profile(**json.loads(args.kernel_input.read_text(encoding='utf-8')))
              if args.kernel_input else model())
    report = json_safe(report)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key not in
                     ('labels', 'adjacency_scaled', 'exact_outer_modes', 'extra_relation', 'proof')}, indent=2))


if __name__ == '__main__':
    main()
