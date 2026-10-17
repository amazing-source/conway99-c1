"""Second-order, exact mod-5 filters for the LOCAL <z,hM> family.

This extends the constant-term test in z5_hm_rank_obstruction.py.  It
does not enumerate graphs, read producer data, or assert sufficiency of
any congruence.  All arithmetic is in F5[e]/(e^4), with zeta -> 1+e.
Run this file to reproduce deterministic algebraic fixtures and a report.
The fixtures are coefficient assignments, not claimed admissible graphs.
"""
from itertools import permutations, product
from pathlib import Path
import argparse
import json
import random

P = 5
ZERO = (0, 0, 0, 0)


def add(x, y):
    return tuple((a+b) % P for a, b in zip(x, y))


def scale(x, s):
    return tuple(s*a % P for a in x)


def mul(x, y):
    return tuple(sum(x[i]*y[k-i] for i in range(k+1)) % P for k in range(4))


def monomial(k):
    # Generalized binomial coefficients also cover negative Laurent powers.
    out, value = [], 1
    for j in range(4):
        if j:
            value = value*(k-j+1)//j
        out.append(value % P)
    return tuple(out)


def conjugate(x):
    # e -> (1+e)^(-1)-1 = -e+e^2-e^3.
    q = (0, 4, 1, 4)
    answer, power = ZERO, (1, 0, 0, 0)
    for coefficient in x:
        answer = add(answer, scale(power, coefficient))
        power = mul(power, q)
    return answer


def polynomial(coefficients):
    answer = ZERO
    for k, coefficient in enumerate(coefficients):
        answer = add(answer, scale(monomial(k), coefficient))
    return answer


def determinant(matrix):
    answer = ZERO
    for perm in permutations(range(len(matrix))):
        term = (1, 0, 0, 0)
        for i, j in enumerate(perm):
            term = mul(term, matrix[i][j])
        inversions = sum(perm[i] > perm[j] for i in range(len(perm))
                         for j in range(i+1, len(perm)))
        answer = add(answer, scale(term, (-1)**inversions))
    return answer


def fourier_matrix(block, B, C, sign):
    """Return 2T+ or 4T- in F5[e]/e^4; B,C are 2x2 arrays of 5 counts."""
    gamma = [[ZERO for _ in range(4)] for _ in range(4)]
    for start, key in ((0, 'left'), (2, 'right')):
        typ, a, s = block[key]
        off = monomial(a)
        if typ == 'D':
            off = add(off, scale(monomial(s), sign))
        else:
            gamma[start][start] = gamma[start+1][start+1] = (sign % P, 0, 0, 0)
        gamma[start][start+1] = off
        gamma[start+1][start] = conjugate(off)
    for i, j in product(range(2), repeat=2):
        cross = add(polynomial(B[i][j]), scale(polynomial(C[i][1-j]), sign))
        gamma[i][2+j] = cross
        gamma[2+j][i] = conjugate(cross)
    f = (1, -1, 1, -1)
    factor = 2 if sign == 1 else 4
    return [[add(((3*factor*int(i == j)-(1 if sign == 1 else f[i]*f[j])) % P,
                  0, 0, 0), scale(gamma[i][j], -factor))
             for j in range(4)] for i in range(4)]


def quotient(B, C):
    def signed_count(A):
        n = sum(A[0][0])
        assert all(sum(A[i][j]) == (n if i == j else 2-n)
                   for i, j in product(range(2), repeat=2))
        return 2*n-2
    return signed_count(B), signed_count(C)


def moments(B, C):
    def moment(A, degree):
        return [[sum(k**degree*x for k, x in enumerate(A[i][j])) % P
                 for j in range(2)] for i in range(2)]
    bm, cm = moment(B, 1), moment(C, 1)
    b2, c2 = moment(B, 2), moment(C, 2)
    D = [[(bm[i][j]-cm[i][1-j]) % P for j in range(2)] for i in range(2)]
    D2 = [[(b2[i][j]-c2[i][1-j]) % P for j in range(2)] for i in range(2)]
    f = (1, -1)
    return dict(D=D,
        alpha=sum(D[i][j]*f[j] for i, j in product(range(2), repeat=2)) % P,
        beta=sum(f[i]*D[i][j] for i, j in product(range(2), repeat=2)) % P,
        p=sum(f[i]*D[i][j]*f[j] for i, j in product(range(2), repeat=2)) % P,
        s2=sum(f[i]*D2[i][j]*f[j] for i, j in product(range(2), repeat=2)) % P,
        total=sum(bm[i][j]+cm[i][j] for i, j in product(range(2), repeat=2)) % P)


def filter_candidate(block, B, C):
    """Necessary modular filters; 'not proved' never means 'singular'.

    This only requires the parameterization, not the graph to pass C2/PSD.
    The nullity caps in the report are conditional on C1/C1'/C2 and T/U PSD,
    because they use the earlier theorem a,b<=1 over Q(zeta5).
    """
    for key in ('left', 'right'):
        typ, a, s = block[key]
        assert typ in ('D', 'M') and a in range(5)
        assert s in range(5) if typ == 'D' else s is None
    for A in (B, C):
        assert len(A) == 2 and all(len(row) == 2 for row in A)
        assert all(len(cell) == 5 and all(x in (0, 1) for x in cell)
                   for row in A for cell in row)
    t, w = quotient(B, C)
    e, f = (1 if block[key][0] == 'D' else -1 for key in ('left', 'right'))
    allowed = {(0, 0), (0, 2), (2, 0)}
    if e == f == 1:
        allowed |= {(-2, 0), (0, -2)}
    assert (t, w) in allowed, 'The z-trivial T/U quotient already excludes this type.'
    d = ((7-2*e)*(7-2*f)-(2*(t+w)+1)**2) % P
    dm = determinant(fourier_matrix(block, B, C, -1))
    dp = determinant(fourier_matrix(block, B, C, 1))
    # det is fixed by conjugation.  These identities cover all assignments.
    assert dm[1] == dp[1] == 0
    assert dm[3] == -dm[2] % P and dp[3] == -dp[2] % P
    assert dm[0] == 576*d % P
    m = moments(B, C)
    formula = None
    if e != f and t+w == 2:
        key = 'left' if e == 1 else 'right'
        _, a, s = block[key]
        D = m['D']
        delta = ([(D[0][j]-D[1][j]) % P for j in range(2)] if e == 1
                 else [(D[i][0]-D[i][1]) % P for i in range(2)])
        q = (delta[0]*delta[1]-2*s*(a-s)) % P
        # With kernel (1,-1) on the D side, the complementary minor is 1 mod5.
        assert dm == (0, 0, q, -q % P)
        formula = dict(kind='mixed_D_M', D_side=key, delta=delta,
                       a=a, s=s, q=q)
    elif e == f == -1 and t == w == 0:
        a, b = block['left'][1], block['right'][1]
        alpha, beta, p, s2 = (m[k] for k in ('alpha', 'beta', 'p', 's2'))
        q = (a*alpha-b*beta-alpha*alpha-beta*beta+p*p-s2) % P
        # Kernel (1,-1,-1,1); complementary minor is 1 mod5.
        assert dm == (0, 0, q, -q % P)
        formula = dict(kind='M_M', a=a, b=b, alpha=alpha, beta=beta,
                       p=p, s2=s2, q=q)
    elif e == f == 1 and t+w == 2:
        p, total = m['p'], m['total']
        assert dm == (0, 0, p*p % P, -p*p % P)
        assert dp == (0, 0, 4*total*total % P, -4*total*total % P)
        formula = dict(kind='D_D_nullity6', p=p, total=total)
    minus_nonsingular = any(dm)
    plus_nonsingular = any(dp)
    nu0 = 6 if e == f == 1 and t+w == 2 else 5
    return dict(epsilon=[e, f], t=t, w=w, determinant_minus_mod5=list(dm),
        determinant_plus_mod5=list(dp), moment_formula=formula,
        minus_proved_nonsingular=minus_nonsingular,
        plus_proved_nonsingular=plus_nonsingular,
        conditional_nullity_upper_bound=nu0+4*(not minus_nonsingular)+4*(not plus_nonsingular))


def coefficient_fixture(rng, t):
    n = (t+2)//2
    A = [[[0]*5 for _ in range(2)] for _ in range(2)]
    for i, j in product(range(2), repeat=2):
        for k in rng.sample(range(5), n if i == j else 2-n):
            A[i][j][k] = 1
    return A


PROOF = [
    'Phi5(1+e)=e^4 in F5[e]. Hence Z[zeta5]/5 is F5[e]/e^4. A nonzero determinant in this ring proves nonsingularity over Q(zeta5), even if the constant term vanishes.',
    'The Laurent determinant is invariant under X->X^-1. Its expansion c0+c1*e+c2*e^2+c3*e^3 therefore has c1=0 and c3=-c2 over F5. The second-order test uses the entire reduction modulo5; a zero reduction is inconclusive.',
    'In the five remaining nu0=5 quotient types, N(1)=4T_-(1) has rank3 overF5. Let v span its kernel and E be the other three coordinate vectors. With H=E^t*N(1)*E, the second-order Schur term is Q=v^t*N2*v+(E^t*N1*v)^t*H^-1*(E^t*N1*v). Here N1 is skew-symmetric, which accounts for the plus sign.',
    'Write D1=moment1(B-CM). In a mixed D/M type with t+w=2, put delta_j=D1[0,j]-D1[1,j] if D is on the left; put delta_i=D1[i,0]-D1[i,1] otherwise. A negative cyclotomic kernel requires delta_0*delta_1=2*s*(a-s) mod5, where a,s belong to that D side. The determinant coefficients are (0,0,Q,-Q).',
    'For M/M and t=w=0, set f=(1,-1), j=(1,1), alpha=j^t*D1*f, beta=f^t*D1*j, p=f^t*D1*f, and S2=f^t*moment2(B-CM)*f. A negative cyclotomic kernel requires S2=a*alpha-b*beta-alpha^2-beta^2+p^2 mod5. The determinant coefficients are (0,0,Q,-Q).',
    'In D/D, t+w=2, let p=f^t*moment1(B-CM)*f and L=sum of all first moments of B+C. The reductions of det(4T_-) and det(2T_+) are respectively p^2*(e^2-e^3) and4*L^2*(e^2-e^3). Thus nonzero p excludes b, and nonzero L excludes a. Both nonzero imply total nullity6; nullity14 requires p=L=0. Neither congruence is asserted sufficient.',
    'Combining these filters with the earlier exact a,b<=1 theorem gives candidate-specific caps. For nu0=5, Q!=0 on the negative side proves nullity<=9. For nu0=6, both first moments nonzero prove nullity6. This is not a proof of a universal local ceiling9.',
    'These are filters on the small circulant coefficient blocks. No producer graph, saved kernel, enumeration, or exact PSD result is recomputed. The deterministic fixtures check polynomial identities on synthetic coefficient assignments only; the Schur derivation supplies the universal argument.'
]


def run():
    rng = random.Random(20261015)
    types = [('D', 'M', 2, 0), ('D', 'M', 0, 2),
             ('M', 'D', 2, 0), ('M', 'D', 0, 2), ('M', 'M', 0, 0),
             ('D', 'D', 2, 0), ('D', 'D', 0, 2)]
    examples, total, rejected = {}, 0, 0
    for lt, rt, t, w in types:
        for _ in range(16):
            block = {key: [typ, rng.randrange(5) if typ == 'D' else rng.randrange(1, 5),
                           rng.randrange(5) if typ == 'D' else None]
                     for key, typ in (('left', lt), ('right', rt))}
            B, C = coefficient_fixture(rng, t), coefficient_fixture(rng, w)
            result = filter_candidate(block, B, C)
            total += 1
            rejected += result['minus_proved_nonsingular']
            tag = result['moment_formula']['kind']
            if tag not in examples and result['minus_proved_nonsingular']:
                examples[tag] = dict(block=block, B=B, C=C, result=result)
    return dict(status='EXACT_SECOND_ORDER_CYCLOTOMIC_FILTER',
                synthetic_identity_fixtures=total,
                fixtures_with_negative_sector_proved_nonsingular=rejected,
                fixtures_are_not_asserted_admissible_graphs=True,
                examples=examples, proof=PROOF)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--candidate', type=Path,
                        help='JSON with keys block, B, C, in the existing <z,hM> parameterization')
    args = parser.parse_args()
    report = filter_candidate(**json.loads(args.candidate.read_text(encoding='utf-8'))) if args.candidate else run()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('examples', 'proof')}, indent=2))


if __name__ == '__main__':
    main()
