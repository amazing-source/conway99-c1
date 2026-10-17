"""Exact checks for notes/165_CODEX_NORM14_RANK33.md.

Run from the repository root: python code/codex/norm14_audit.py
Requires SymPy. No search, floating point pruning, or solver is used.
The 99-vertex example below is deliberately NOT an SRG: it checks the
Schur formula and rejects the false implication trace(R)=16 => R^2=R.
"""
import json
from itertools import combinations, permutations, product
from pathlib import Path

import sympy as sp


def rref_mod(matrix, prime=7):
    a = [[int(x) % prime for x in row] for row in matrix.tolist()]
    pivots = []
    for c in range(matrix.cols):
        r = len(pivots)
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, prime)
        a[r] = [(x * inv) % prime for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [(x - f * y) % prime for x, y in zip(a[i], a[r])]
        pivots.append(c)
        if len(pivots) == len(a):
            break
    return sp.Matrix(a), pivots


def rank7(matrix):
    return len(rref_mod(matrix)[1])


def inverse7(matrix):
    n = matrix.rows
    reduced, pivots = rref_mod(matrix.row_join(sp.eye(n)))
    assert pivots[:n] == list(range(n))
    answer = reduced[:, n:]
    assert (matrix * answer).applyfunc(lambda x: x % 7) == sp.eye(n)
    return answer


def rook_control():
    vertices = list(product(range(3), repeat=2))
    A = sp.Matrix(9, 9, lambda i, j: int(i != j and
                  (vertices[i][0] == vertices[j][0] or vertices[i][1] == vertices[j][1])))
    assert A * A == 2 * sp.eye(9) - A + 2 * sp.ones(9)
    # The two diagonals of a rectangle give a norm-4 (-2)-eigenvector.
    P, Q, Z = [0, 4], [1, 3], [8]
    phi = sp.Matrix([int(i in P) - int(i in Q) for i in range(9)])
    assert A * phi == -2 * phi and phi.dot(phi) == 4
    C = P + Q + Z
    X = [i for i in range(9) if i not in C]
    assert all(sum(A[x, z] for z in Z) == 1 for x in X)
    for coclique in (P + Z, Q + Z):
        assert A.extract(coclique, coclique) == sp.zeros(3)
    E = (sp.eye(9) - A + sp.ones(9) / 3) / 3
    assert E * E == E and sp.trace(E) == 4
    # One redundant core coordinate is omitted, as in the 99 reduction.
    I = P + Q
    inverse = E.extract(I, I).inv(method='DM')
    R = E.extract(X, X) - E.extract(X, I) * inverse * E.extract(I, X)
    assert R == sp.zeros(4)
    F = (A - sp.eye(9)).extract(C, C)
    D = A.extract(C, X)
    core_rank3 = len(rref_mod(F, 3)[1])
    augmented_rank3 = len(rref_mod(F.row_join(D), 3)[1])
    full_rank3 = len(rref_mod(A - sp.eye(9), 3)[1])
    assert core_rank3 == augmented_rank3 == full_rank3 == 4
    return {'norm': 4, 'core_rank': 4, 'residual_rank': 0,
            'core_mod3_rank': core_rank3, 'full_mod3_rank': full_rank3}


def fano_uniqueness(B):
    pairs = set(combinations(range(7), 2))
    triples = list(combinations(range(7), 3))
    covered = {t: set(combinations(t, 2)) for t in triples}
    solutions = set()

    def visit(remaining, blocks):
        if not remaining:
            solutions.add(tuple(sorted(blocks)))
            return
        first = min(remaining)
        for t in triples:
            if first in covered[t] and covered[t] <= remaining:
                visit(remaining - covered[t], blocks + [t])

    visit(pairs, [])
    canonical = [tuple(i for i in range(7) if B[i, j] == 0) for j in range(7)]
    orbit = {tuple(sorted(tuple(sorted(p[i] for i in t)) for t in canonical))
             for p in permutations(range(7))}
    assert solutions == orbit and len(solutions) == 30
    return len(solutions)


def main():
    B = sp.Matrix(7, 7, lambda i, j:
                  sum(((i + 1) >> k & 1) * ((j + 1) >> k & 1) for k in range(3)) % 2)
    assert B * B.T == 2 * sp.eye(7) + 2 * sp.ones(7)
    assert B * sp.ones(7, 1) == 4 * sp.ones(7, 1)
    X = [(p, q, c) for p in range(7) for q in range(7) for c in range(2 - B[p, q])]
    assert len(X) == 70
    assert sum(B[p, q] for p, q, _ in X) == 28

    core_A = sp.zeros(29)
    core_A[:7, 7:14] = B
    core_A[7:14, :7] = B.T
    F = core_A - 3 * sp.eye(29)
    C = 27 * sp.eye(29) - 9 * core_A + sp.ones(29)
    kernel = sp.Matrix([3] * 14 + [-1] * 15)
    assert C * kernel == sp.zeros(29, 1)
    C0 = C[:28, :28]
    inverse = C0.inv(method='DM')
    det = C0.det(method='domain-ge')
    assert det == 3**67 * 7**7

    # Regular synthetic input: repeated disjoint triples, intentionally not a design.
    triples = [tuple(range(3 * (i % 5), 3 * (i % 5) + 3)) for i in range(70)]
    D = sp.zeros(29, 70)
    for i, ((p, q, _), T) in enumerate(zip(X, triples)):
        D[p, i] = D[7 + q, i] = 1
        for z in T:
            D[14 + z, i] = 1
    H = sp.Matrix(70, 70, lambda i, j: int((i - j) % 70 in {1, 2, 3, 4, 35, 66, 67, 68, 69}))
    A = core_A.row_join(D).col_join(D.T.row_join(H))
    assert A == A.T and A * sp.ones(99, 1) == 14 * sp.ones(99, 1)
    assert not any(A[i, i] for i in range(99))

    cross = sp.ones(29, 70) - 9 * D
    assert C[:, :28] * inverse * cross[:28, :] == cross
    R = (27 * sp.eye(70) - 9 * H + sp.ones(70)
         - cross[:28, :].T * inverse * cross[:28, :]) / 63
    K = sp.zeros(70)
    for i, (p, q, _) in enumerate(X):
        for j, (p2, q2, _) in enumerate(X):
            intersection = len(set(triples[i]) & set(triples[j]))
            K[i, j] = (63 * int(i == j) + 12 - 21 * H[i, j] - 7 * intersection
                       - 9 * int(p == p2) - 9 * int(q == q2) - 3 * (B[p, q2] + B[p2, q]))
    assert 147 * R == K
    assert all(R[i, i] == sp.Rational(2 * (6 - B[p, q]), 49) for i, (p, q, _) in enumerate(X))
    assert sp.trace(R) == 16
    # One diagonal already disproves idempotence; do not treat this as a graph witness.
    defect00 = sum(R[0, j] * R[j, 0] for j in range(70)) - R[0, 0]
    assert defect00 != 0
    assert A * A + A != 12 * sp.eye(99) + 2 * sp.ones(99)

    f_rank = rank7(F)
    augmented_rank = rank7(F.row_join(D))
    assert (f_rank, augmented_rank) == (23, 28)
    assert f_rank + 2 * (augmented_rank - f_rank) == 33
    # A hand-built kernel basis: v=e_i-e_6, u=Bv/3 over F7.
    V = sp.zeros(7, 6)
    for i in range(6):
        V[i, i] = 1
        V[6, i] = -1
    W = ((5 * B * V).col_join(V).col_join(sp.zeros(15, 6))).applyfunc(lambda x: x % 7)
    assert (F * W).applyfunc(lambda x: x % 7) == sp.zeros(29, 6)
    assert rank7(W) == 6 and rank7(D.T * W) == 5
    phi_core = sp.Matrix([1] * 7 + [-1] * 7 + [0] * 15)
    assert (F * phi_core).applyfunc(lambda x: x % 7) == sp.zeros(29, 1)
    assert D.T * phi_core == sp.zeros(70, 1)

    # Sharpness of the block-rank lemma over F7, without Boolean graph constraints.
    # Independent columns of a symmetric rank-r matrix index a nonsingular principal block.
    I = rref_mod(F)[1]
    FI = F.extract(I, I)
    DI = D.extract(I, range(70))
    free_completion = (DI.T * inverse7(FI) * DI).applyfunc(lambda x: x % 7)
    completed = F.row_join(D).col_join(D.T.row_join(free_completion))
    assert rank7(completed) == 33
    assert rank7(K) == 5  # independent cross-check: five 49-primary factors of N_X

    report = {
        'status': 'exact algebra checks passed; no 99-graph existence claim',
        'rook_positive_control': rook_control(),
        'labelled_fano_planes_one_isomorphism_class': fano_uniqueness(B),
        'core_mod7_rank': f_rank,
        'core_augmented_mod7_rank': augmented_rank,
        'kernel_coupling_mod7_rank': 5,
        'conditional_rank7_lower_bound': 33,
        'unrestricted_mod7_completion_rank': rank7(completed),
        'negative_projector_core_rank': 28,
        'negative_projector_core_minor_determinant': str(det),
        'residual_trace': str(sp.trace(R)),
        'residual_diagonal_apex': '10/49',
        'residual_diagonal_other': '12/49',
        'synthetic_negative_control_idempotence_defect_00': str(defect00),
        'rank_147R_mod7': rank7(K),
    }
    destination = Path(__file__).resolve().parents[2] / 'data' / 'codex_norm14_audit.json'
    destination.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
