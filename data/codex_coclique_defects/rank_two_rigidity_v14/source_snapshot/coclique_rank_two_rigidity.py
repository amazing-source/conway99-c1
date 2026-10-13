"""Exact certificates for rank-two differences of strongly regular graphs.

For Conway parameters (99,14,1,2), every nonzero rank-two difference
between two adjacency matrices with the same parameters is a transposition
of two vertices. This is a conditional rigidity theorem, not existence or
nonexistence. For a fixed boundary, augmented nullity at most two therefore
gives uniqueness up to a permutation fixing the boundary.

Controls also include a nonisomorphic rank-two switch for (16,6,2,2),
so the conclusion is not incorrectly extended to arbitrary parameters.
"""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import sympy as sp
from coclique_regular_completion import eliminate_regular
from coclique_global_completion import encode, integral_completion


def check_graph(A, k, lam, mu):
    n = A.rows
    assert A.shape == (n, n) and A == A.T
    assert all(x in (0, 1) for x in A)
    assert all(A[i, i] == 0 for i in range(n))
    assert A*sp.ones(n, 1) == k*sp.ones(n, 1)
    assert A*A == (k-mu)*sp.eye(n)+(lam-mu)*A+mu*sp.ones(n)


def possible_nonswap_sizes(k, lam, mu):
    """Necessary integer conditions when both sign classes have size >=2."""
    answers = []
    cap = max(lam, mu)
    for p in range(2, cap+1):
        for q in range(2, cap+1):
            for alpha in range(-p, p):
                beta = lam-mu-alpha
                if -q <= beta < q and p*q == k-mu+(lam-mu)*alpha-alpha*alpha:
                    answers.append(dict(p=p, q=q, alpha=alpha, beta=beta))
    return answers


def certificate(A, other, k, lam, mu):
    A, other = sp.Matrix(A), sp.Matrix(other)
    check_graph(A, k, lam, mu)
    check_graph(other, k, lam, mu)
    T = other-A
    assert T.rank() == 2
    n = A.rows
    support = [i for i in range(n) if any(T.row(i))]
    first = support[0]
    V = [j for j in support if T[first, j]]
    U = [i for i in support if i not in V]
    u, v = sp.zeros(n, 1), sp.zeros(n, 1)
    for j in V:
        v[j] = T[first, j]
    for i in U:
        u[i] = T[i, V[0]]/v[V[0]]
    assert T == u*v.T+v*u.T
    assert set(u).issubset({-1, 0, 1}) and set(v).issubset({-1, 0, 1})
    assert sum(u) == sum(v) == 0
    p, q = len(U)//2, len(V)//2
    assert len(U) == 2*p and len(V) == 2*q
    alpha = (A*u+p*v)[U[0]]/u[U[0]]
    beta = (A*v+q*u)[V[0]]/v[V[0]]
    assert alpha.is_Integer and beta.is_Integer
    assert A*u == alpha*u-p*v and A*v == -q*u+beta*v
    assert alpha+beta == lam-mu
    assert p*q == k-mu+(lam-mu)*alpha-alpha*alpha
    if p >= 2:
        assert q <= max(lam, mu)
    if q >= 2:
        assert p <= max(lam, mu)
    swapped = None
    if p == 1 or q == 1:
        swapped = U if p == 1 else V
        permutation = list(range(n))
        a, b = swapped
        permutation[a], permutation[b] = b, a
        assert other == A[permutation, permutation]
        assert (q if p == 1 else p) == k-mu+(lam-mu)*(-A[a, b])-A[a, b]**2
    if (k, lam, mu) == (14, 1, 2):
        assert min(p, q) == 1 and max(p, q) == 12 and swapped is not None
    return dict(p=p, q=q, alpha=int(alpha), beta=int(beta),
                u=list(map(int, u)), v=list(map(int, v)), rank=2,
                support_size=len(support), transposition=swapped)


def complete_nullity_two_pair(B, D, k=14, mu=2):
    """Exact, solver-free completion when h=2 and two D columns coincide.

Requires lambda=mu-1, as in eliminate_regular. If applicable, returns
either no completion or two labelled completions related by the swap.
NOT_APPLICABLE is not an exclusion of other boundaries.
"""
    B, D = sp.Matrix(B), sp.Matrix(D)
    data = eliminate_regular(B, D, k, mu)
    if data['nullity'] != 2 or k == mu:
        return dict(status='NOT_APPLICABLE', reason='Requires augmented nullity two and k>mu')
    pairs = [(a, b) for a, b in combinations(range(D.cols), 2) if D[:, a] == D[:, b]]
    if not pairs:
        return dict(status='NOT_APPLICABLE', reason='No repeated boundary column')
    a, b = pairs[0]
    m, nu = D.cols, k-mu
    u = sp.zeros(m, 1)
    u[a], u[b] = 1, -1
    candidates = [z-u*(u.T*z)[0]/2 for z in data['constraint_matrix'].nullspace()]
    z = next(z for z in candidates if any(z))
    reject = lambda reason: dict(status='NO_SRG_COMPLETION', pair=[a, b], reason=reason)
    if z[a] or z[b]:
        return reject('The orthogonal kernel direction does not vanish on the repeated pair')
    magnitudes = {abs(x) for x in z if x}
    if len(magnitudes) != 1:
        return reject('The orthogonal kernel direction has unequal nonzero magnitudes')
    v = z/next(iter(magnitudes))
    assert set(v).issubset({-1, 0, 1}) and sum(v) == 0
    if (v.T*v)[0] != 2*nu:
        return reject('The orthogonal kernel direction has the wrong support size')
    E0 = data['E0']
    e = 2*E0[a, a]
    if e not in (0, 1):
        return reject('The repeated-pair edge forced by the diagonal is not binary')
    centre = E0-e*u*u.T/2+sp.Rational(e-1, 2*nu)*v*v.T
    half_trade = (u*v.T+v*u.T)/2
    E = centre-half_trade
    if not all(x.is_Integer for x in E):
        return reject('The two possible completions are nonintegral')
    other = centre+half_trade
    integral_completion(B, D, E, k, mu)
    permutation = list(range(m))
    permutation[a], permutation[b] = b, a
    assert other == E[permutation, permutation]
    return dict(status='TWO_LABELLED_COMPLETIONS', pair=[a, b], edge=int(e),
                isomorphism_classes=1, u=list(map(int, u)), v=list(map(int, v)),
                completions=[encode(E), encode(other)])


def controls(folder):
    folder.mkdir(parents=True, exist_ok=True)
    reports = []
    rook = sp.Matrix(9, 9, lambda i, j: int(i != j and (i//3 == j//3 or i%3 == j%3)))
    vertices = list(combinations(range(5), 2))
    petersen = sp.Matrix(10, 10, lambda i, j: int(set(vertices[i]).isdisjoint(vertices[j])))
    for name, A, k, lam, mu, a, b in (
        ('rook_adjacent_swap', rook, 4, 1, 2, 0, 1),
        ('rook_nonadjacent_swap', rook, 4, 1, 2, 0, 4),
        ('petersen_nonadjacent_swap', petersen, 3, 0, 1, 0, 1),
    ):
        permutation = list(range(A.rows))
        permutation[a], permutation[b] = b, a
        other = A[permutation, permutation]
        cert = certificate(A, other, k, lam, mu)
        assert cert['transposition'] is not None
        reports.append(dict(name=name, parameters=[A.rows, k, lam, mu],
                            A=A.tolist(), other=other.tolist(), certificate=cert))

    # An actual nonisomorphic rank-two switch with different SRG parameters.
    A = sp.Matrix(16, 16, lambda i, j: int(i != j and (i//4 == j//4 or i%4 == j%4)))
    u = sp.zeros(16, 1)
    for i, sign in ((0, 1), (5, 1), (10, -1), (15, -1)):
        u[i] = sign
    v = -A*u/2
    other = A+u*v.T+v*u.T
    cert = certificate(A, other, 6, 2, 2)
    count = lambda M: sum(all(M[i, j] for i, j in combinations(S, 2))
                          for S in combinations(range(16), 4))
    counts = [count(A), count(other)]
    assert counts == [8, 0] and cert['transposition'] is None
    reports.append(dict(name='nonisomorphic_rank_two_control', parameters=[16, 6, 2, 2],
                        A=A.tolist(), other=other.tolist(), certificate=cert, cliques4=counts))
    arithmetic = possible_nonswap_sizes(14, 1, 2)
    assert arithmetic == []
    assert possible_nonswap_sizes(6, 2, 2) == [dict(p=2, q=2, alpha=0, beta=0)]
    for report in reports:
        # All matrix entries have already been checked to be integers.
        encoded = json.dumps(report, indent=2, default=int)+'\n'
        (folder/(report['name']+'.json')).write_text(encoded, encoding='utf-8')
    # A new singular boundary: h=2, one repeated pair, no closed star.
    outside = [0, 7, 3, 6, 8, 9]
    border = [i for i in range(10) if i not in outside]
    B, D = petersen[border, border], petersen[border, outside]
    completed = complete_nullity_two_pair(B, D, 3, 1)
    assert completed['status'] == 'TWO_LABELLED_COMPLETIONS'
    assert encode(petersen[outside, outside]) in completed['completions']
    completed.update(B=encode(B), D=encode(D), border=border, outside=outside, k=3, mu=1)
    (folder/'petersen_nullity_two.json').write_text(json.dumps(completed, indent=2)+'\n', encoding='utf-8')
    # Same Gram and degrees as an actual rook boundary, but two duplicate pairs.
    B = rook[[0, 1, 3], [0, 1, 3]]
    D = sp.Matrix([[1, 1, 0, 0, 0, 0],
                   [1, 0, 1, 1, 0, 0],
                   [1, 0, 0, 0, 1, 1]])
    rejected = complete_nullity_two_pair(B, D, 4, 2)
    assert rejected['status'] == 'NO_SRG_COMPLETION'
    assert rejected['reason'] == 'The orthogonal kernel direction has the wrong support size'
    rejected.update(B=encode(B), D=encode(D), k=4, mu=2,
                    scope='A Gram-valid toy boundary, not a Conway branch')
    (folder/'gram_valid_rejected_factor.json').write_text(json.dumps(rejected, indent=2)+'\n', encoding='utf-8')
    summary = dict(status='PASS', controls=[dict(name=r['name'], **r['certificate']) for r in reports],
                   conway_nonswap_integer_cases=arithmetic,
                   conway_conclusion='Every nonzero rank-two difference is a vertex transposition on support 26',
                   nullity_two_completion=completed['status'], gram_valid_rejection=rejected['status'],
                   source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   scope='Conditional rigidity theorem; no Conway adjacency matrix constructed or excluded')
    (folder/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status='PASS',controls=len(reports),conway_nonswap_integer_cases=arithmetic,
                         different_parameters_cliques4=counts, nullity_two_completion=completed['status'],
                         gram_valid_rejection=rejected['status'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    controls(parser.parse_args().folder)
