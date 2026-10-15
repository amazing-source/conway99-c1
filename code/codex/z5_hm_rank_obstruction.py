"""A finite obstruction for the LOCAL four-star family <z,hM>.

z=(4 6 8 10 12)(5 7 9 11 13), h=(01)(23), M=(45)...(12 13).
No extension of these permutations to the hypothetical 99-vertex graph
is assumed.  Under C1,C1',C2 and T,U PSD, null_Q(T)<=14.  If null_Q(T)=14,
rank_F7(8T)>=29.  Combining this with the previously established GLOBAL
requirements rank_Q(T)<=30 and rank_F7(8T)<=28 excludes this local family.
It does NOT prove the observed local nullity ceiling9 or exclude all C1.

This is a new exhaustive calculation of small cyclotomic rank obstructions,
not an enumeration or recheck of producer graph files.  Standard library
only.  The supplied 520 integer negative witnesses are checked exactly;
no floating-point test or external solver verdict enters the proof.

Geometry and completeness argument are exported in the result JSON.  The
default certificate path is relative to this repository; use --certificates
for a portable copy.  --output optionally writes the complete small report.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json

# Z[zeta_5], basis 1,z,z^2,z^3.  The same representation modulo7 is F_(7^4).
ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def scale(a, k):
    return tuple(k*x for x in a)


def poly(coefficients):
    out = [0]*5
    for i, c in enumerate(coefficients):
        out[i % 5] += c
    return tuple(out[i]-out[4] for i in range(4))


def mul(a, b):
    out = [0]*7
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return poly(out)


def conj(a):
    out = [0]*5
    for i, x in enumerate(a):
        out[-i % 5] += x
    return poly(out)


def norm(a):
    return mul(a, conj(a))


def equal(a, b, modulus=None):
    return a == b if modulus is None else all((x-y) % modulus == 0 for x, y in zip(a, b))


Z = [poly([0]*k+[1]) for k in range(5)]
LABELS = [(0, 2), (0, 3), (1, 2), (1, 3)] + [
    (c, 4+2*i+b) for c, b, i in product(range(4), range(2), range(5))]
INDEX = {p: i for i, p in enumerate(LABELS)}
STAR = [sum(1 << i for i, p in enumerate(LABELS) if c in p) for c in range(14)]
PAIRS = [(i, j, len(set(p) & set(q)))
         for i, p in enumerate(LABELS) for j, q in enumerate(LABELS[:i])]
K8 = [[3*len(set(p) & set(q))+sum((x ^ 1) in q for x in p)-2
       for q in LABELS] for p in LABELS]
L15 = [[4*len(set(p) & set(q))-sum((x ^ 1) in q for x in p)+2
        for q in LABELS] for p in LABELS]


def diagonal(side, typ, a, s):
    """Scaled lower 2x2 block [[A,-r],[-bar(r),A]]: 2T+ or4T-."""
    if side == '+':
        r = add(ONE, scale(Z[a], 2))
        return (5, add(r, scale(Z[s], 2))) if typ == 'D' else (3, r)
    r = sub(scale(Z[a], 4), ONE)
    return (11, sub(r, scale(Z[s], 4))) if typ == 'D' else (15, r)


def column_pool(side, col, modular_target=False):
    """A superset of every possible cross-column from two 2-regular blocks."""
    out = []
    if side == '+':
        pool = {n: [] for n in range(5)}
        for c in product(range(3), repeat=5):
            if sum(c) <= 4:
                pool[sum(c)].append(c)
        # Target quotient normalizes B-counts to diag(2,2), C-counts to all1.
        ms = (3 if col == 0 else 1,) if modular_target else range(5)
        pairs = ((p, q) for m in ms for p in pool[m] for q in pool[4-m])
    else:
        pairs = []
        for count in range(3):
            for plus in combinations(range(10), count):
                for minus in combinations([i for i in range(10) if i not in plus], count):
                    c = [0]*10
                    for i in plus:
                        c[i] = 1
                    for i in minus:
                        c[i] = -1
                    if modular_target and sum(c[:5]) != (1 if col == 0 else -1):
                        continue
                    pairs.append((tuple(c[:5]), tuple(c[5:])))
    for p, q in pairs:
        if side == '+':
            u, v = add(ONE, scale(poly(p), 2)), add(ONE, scale(poly(q), 2))
        else:
            sign = 1 if col == 0 else -1
            u = add(scale(ONE, sign), scale(poly(p), 4))
            v = sub(scale(poly(q), 4), scale(ONE, sign))
        out.append((p, q, u, v, norm(u), norm(v)))
    return out


def small_rank_blocks(side, modulus=None):
    """Enumerate ALL rank<=2 blocks with an invertible left 2x2 block.

    First enforce the two diagonal Schur equations (3x3 minors), then
    the off-diagonal equation.  No eigenvalues or rank heuristics.
    """
    modular_target = modulus is not None
    pools = {col: column_pool(side, col, modular_target) for col in (0, 1)}
    blocks, counts, singular = [], [0, 0], []
    types = ('D',) if modular_target else ('D', 'M')
    for typ in types:
        for a in range(5):
            for s in (range(5) if typ == 'D' else (None,)):
                if typ == 'M' and a == 0:
                    continue  # C2: two common neighbours in addition to a shared letter.
                A, r = diagonal(side, typ, a, s)
                det = sub(scale(ONE, A*A), norm(r))
                if equal(det, ZERO, modulus):
                    assert side == '+' and (typ, a, s) == ('D', 0, 0)
                    singular.append((typ, a, s))
                    continue
                found = {0: [], 1: []}
                for col in (0, 1):
                    for p, q, u, v, nu, nv in pools[col]:
                        term = mul(r, mul(conj(u), v))
                        value = add(scale(add(nu, nv), A), add(term, conj(term)))
                        for right_type in types:
                            B = diagonal(side, right_type, 0, 0 if right_type == 'D' else None)[0]
                            if equal(value, scale(det, B), modulus):
                                found[col].append((right_type, p, q, u, v))
                    counts[col] += len(found[col])
                for c1, c2 in product(found[0], found[1]):
                    rt, p, q, u, v = c1
                    rt2, w0, x0, w, x = c2
                    if rt != rt2:
                        continue
                    expected = 4 if side == '+' else 0
                    if sum(p)+sum(w0) != expected or sum(q)+sum(x0) != expected:
                        continue
                    cross = add(mul(conj(u), add(scale(w, A), mul(r, x))),
                                mul(conj(v), add(mul(conj(r), w), scale(x, A))))
                    for b in range(5):
                        for t in (range(5) if rt == 'D' else (None,)):
                            if rt == 'M' and b == 0:
                                continue
                            rr = diagonal(side, rt, b, t)[1]
                            if equal(cross, neg(mul(det, rr)), modulus):
                                blocks.append(dict(left=[typ, a, s], right=[rt, b, t],
                                    **{('S' if side == '+' else 'D'): [[p, w0], [q, x0]]}))
    return blocks, dict(pool_sizes=[len(pools[j]) for j in (0, 1)],
                       columns=counts, blocks=len(blocks), singular_left=singular)


def plus_lifts(S):
    """All binary B,C such that S=B+C*M and B,C have row/column sums2."""
    fixed, singles = [], []
    for row, col, k in product(range(2), range(2), range(5)):
        if S[row][col][k] == 2:
            fixed.append((row, col, k))
        elif S[row][col][k] == 1:
            singles.append((row, col, k))
    for chosen in combinations(singles, 4-len(fixed)):
        edges = fixed+list(chosen)
        if any(sum(x[j] == b for x in edges) != 2 for j in (0, 1) for b in (0, 1)):
            continue
        B = [[[0]*5 for _ in range(2)] for _ in range(2)]
        for row, col, k in edges:
            B[row][col][k] = 1
        C = [[[S[row][1-col][k]-B[row][1-col][k] for k in range(5)]
              for col in range(2)] for row in range(2)]
        yield B, C


def target_minus_lifts(D):
    """All B-C*M lifts in the normalized nullity-fourteen quotient."""
    if any(x > 0 for row, col in ((0, 1), (1, 0)) for x in D[row][col]):
        return
    if any(sum(D[row][col]) != -1 for row, col in ((0, 1), (1, 0))):
        return
    for a, b in product(range(5), repeat=2):
        B = [[[0]*5 for _ in range(2)] for _ in range(2)]
        CM = [[[-x for x in D[row][col]] for col in range(2)] for row in range(2)]
        okay = True
        for row, k in ((0, a), (1, b)):
            for i in range(5):
                CM[row][row][i] = int(i == k)
                B[row][row][i] = D[row][row][i]+int(i == k)
                if B[row][row][i] not in (0, 1):
                    okay = False
        if okay:
            yield B, [[CM[row][1-col] for col in range(2)] for row in range(2)]


def graph(block, B, C):
    rows = [0]*44

    def edge(p, q):
        u, v = INDEX[p], INDEX[q]
        assert u != v
        rows[u] |= 1 << v
        rows[v] |= 1 << u

    def outer(c, b, i):
        return c, 4+2*(i % 5)+b

    for p, q in (((0, 2), (0, 3)), ((0, 2), (1, 2)),
                 ((0, 3), (1, 3)), ((1, 2), (1, 3))):
        edge(p, q)
    for center, key in ((0, 'left'), (2, 'right')):
        typ, a, s = block[key]
        for i in range(5):
            edge(outer(center, 0, i), outer(center, 1, i+a))
            edge(outer(center+1, 0, i), outer(center+1, 1, i-a))
            for b in range(2):
                other = (outer(center+1, b, i+(s if b == 0 else -s)) if typ == 'D'
                         else outer(center+1, 1-b, i))
                edge(outer(center, b, i), other)
    for r, c, k, i in product(range(2), range(2), range(5), range(5)):
        if B[r][c][k]:
            edge(outer(0, r, i), outer(2, c, i+k))
            edge(outer(1, 1-r, i), outer(3, 1-c, i+k))
        if C[r][c][k]:
            edge(outer(0, r, i), outer(3, c, i+k))
            edge(outer(1, 1-r, i), outer(2, 1-c, i+k))
    return rows


def admissibility_failure(rows):
    for i, p in enumerate(LABELS):
        for c in range(14):
            cap = 1 if c in p or (c ^ 1) in p else 2
            degree = (rows[i] & STAR[c]).bit_count()
            if (c < 4 and degree != cap) or (c >= 4 and degree > cap):
                return dict(kind='C1' if c < 4 else 'C1prime', label=p,
                            star=c, degree=degree, cap=cap)
    for i, j, shared in PAIRS:
        common = (rows[i] & rows[j]).bit_count()
        edge = (rows[i] >> j) & 1
        if common+shared > 2-edge:
            return dict(kind='C2', pair=[LABELS[i], LABELS[j]],
                        common=common, shared=shared, edge=edge)
    return None


def integer_matrix(rows, side):
    if side == 'T':
        return [[24*int(i == j)-8*((rows[i] >> j) & 1)-K8[i][j]
                 for j in range(44)] for i in range(44)]
    if side == 'U':
        return [[60*int(i == j)+15*((rows[i] >> j) & 1)-L15[i][j]
                 for j in range(44)] for i in range(44)]
    raise ValueError('Unknown side')


def graph_digest(rows):
    return sha256(b''.join(row.to_bytes(6, 'little') for row in rows)).hexdigest()


def check_negative(rows, certificate):
    assert certificate['graph_sha256'] == graph_digest(rows)
    q = [0]*44
    for i, v in certificate['q_sparse']:
        assert 0 <= i < 44 and isinstance(v, int) and q[i] == 0 and v != 0
        q[i] = v
    M = integer_matrix(rows, certificate['side'])
    value = sum(q[i]*M[i][j]*q[j] for i in range(44) for j in range(44))
    assert value == certificate['quadratic_value'] and value < 0
    return value


def rational_psd_rank(matrix):
    A = [[Fraction(x) for x in row] for row in matrix]
    rank = 0
    while A:
        n = len(A)
        if any(A[i][i] < 0 for i in range(n)):
            return None
        if any(A[i][i] == 0 and any(A[i]) for i in range(n)):
            return None
        pivot = next((i for i in range(n) if A[i][i] > 0), None)
        if pivot is None:
            return rank
        ix = [i for i in range(n) if i != pivot]
        A = [[A[i][j]-A[i][pivot]*A[pivot][j]/A[pivot][pivot] for j in ix] for i in ix]
        rank += 1
    return rank


def rank_mod7(matrix):
    A = [[x % 7 for x in row] for row in matrix]
    rank = 0
    for col in range(len(A[0])):
        pivot = next((i for i in range(rank, len(A)) if A[i][col]), None)
        if pivot is None:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        inv = pow(A[rank][col], -1, 7)
        A[rank] = [x*inv % 7 for x in A[rank]]
        for i in range(rank+1, len(A)):
            value = A[i][col]
            A[i] = [(x-value*y) % 7 for x, y in zip(A[i], A[rank])]
        rank += 1
    return rank


def quotient_table():
    orbits = [[i] for i in range(4)] + [list(range(4+5*k, 9+5*k)) for k in range(8)]
    KG = [[sum(K8[i][j] for i in x for j in y) for y in orbits] for x in orbits]
    LG = [[sum(L15[i][j] for i in x for j in y) for y in orbits] for x in orbits]
    result = []
    for e, f, t, w in product((1, -1), (1, -1), (-2, 0, 2), (-2, 0, 2)):
        G = [[0]*12 for _ in range(12)]

        def pair(i, j, value):
            G[i][j] = G[j][i] = value

        for i, j in ((0, 1), (0, 2), (1, 3), (2, 3)):
            pair(i, j, 1)
        for c in range(4):
            pair(4+2*c, 5+2*c, 5)
        for c, epsilon in ((0, e), (2, f)):
            for b in (0, 1):
                pair(4+2*c+b, 4+2*(c+1)+(b if epsilon == 1 else 1-b), 5)
        for c, d, u in ((0, 2, (t+2)//2), (0, 3, (w+2)//2),
                         (1, 2, (w+2)//2), (1, 3, (t+2)//2)):
            for b, other in product(range(2), repeat=2):
                pair(4+2*c+b, 4+2*d+other, 5*(u if b == other else 2-u))
        T = [[24*len(orbits[i])*int(i == j)-8*G[i][j]-KG[i][j]
              for j in range(12)] for i in range(12)]
        U = [[60*len(orbits[i])*int(i == j)+15*G[i][j]-LG[i][j]
              for j in range(12)] for i in range(12)]
        rt, ru = rational_psd_rank(T), rational_psd_rank(U)
        if rt is not None and ru is not None:
            result.append(dict(epsilon=[e, f], t=t, w=w, nullity=12-rt,
                               rank_T_mod7=rank_mod7(T)))
    assert len(result) == 14
    assert {row['nullity'] for row in result} == {5, 6}
    target = [r for r in result if r['nullity'] == 6]
    assert len(target) == 2 and all(r['epsilon'] == [1, 1] and r['t']+r['w'] == 2
                                    and r['rank_T_mod7'] == 5 for r in target)
    return result


def geometry_fixture(block, B, C):
    """Test the new Fourier formulas against direct44-label geometry.

    Uses one of OUR finite lifts, not any producer graph.  Exact arithmetic.
    """
    rows = graph(block, B, C)
    for side, sign in (('+', 1), ('-', -1)):
        gamma = [[ZERO for _ in range(4)] for _ in range(4)]
        for start, key in ((0, 'left'), (2, 'right')):
            typ, a, s = block[key]
            off = Z[a] if typ == 'M' else add(Z[a], scale(Z[s], sign))
            gamma[start][start+1], gamma[start+1][start] = off, conj(off)
            if typ == 'M':
                gamma[start][start] = gamma[start+1][start+1] = scale(ONE, sign)
        for i, j in product(range(2), repeat=2):
            x = add(poly(B[i][j]), scale(poly(C[i][1-j]), sign))
            gamma[i][2+j], gamma[2+j][i] = x, conj(x)
        basis = []
        for center, b in product((0, 2), range(2)):
            vec = {}
            for i in range(5):
                vec[INDEX[center, 4+2*i+b]] = Z[i]
                vec[INDEX[center+1, 4+2*i+1-b]] = scale(Z[i], sign)
            basis.append(vec)
        f = [1, -1, 1, -1]
        for which in ('T', 'U'):
            M = integer_matrix(rows, which)
            for i, j in product(range(4), repeat=2):
                value = ZERO
                for p, x in basis[i].items():
                    for q, y in basis[j].items():
                        value = add(value, scale(mul(conj(x), y), M[p][q]))
                if which == 'T':
                    offset = 24*int(i == j)-(4 if side == '+' else 2*f[i]*f[j])
                    expected = sub(scale(ONE, offset), scale(gamma[i][j], 8))
                else:
                    offset = 60*int(i == j)-(3 if side == '+' else 5*f[i]*f[j])
                    expected = add(scale(ONE, offset), scale(gamma[i][j], 15))
                assert value == scale(expected, 10)


PROOF = [
    'C1 makes the four z-fixed labels O a C4. C1 then forbids every O-to-outer edge. Each outer star matching is even_i--odd_(i+a); the mate-star matching is either D_s=diag(z^s,z^-s), or M. In the latter case a=0 violates C2.',
    'On each nontrivial z-character, split by g=hM into4x4 blocks. T+=3I-Gamma+-J/2, T-=3I-Gamma--ff^t/4, f=(1,-1,1,-1). Gamma cross-blocks are B+C*M and B-C*M. Each B,C is binary circulant with row and column sums2.',
    'The z-trivial space has dimension12. After C1 its variable tests reduce to T on M-: [[7/2-e,-t-w-1/2],[-t-w-1/2,7/2-f]] and [[4+e,-t+w],[-t+w,4+f]]. Direct exact12x12 T/U quotient tests leave14 cases, nullities5 or6. Nullity6 leaves only e=f=1, (t,w)=(2,0) or(0,2).',
    'Over Q(zeta5), left principal2x2 blocks of T+ are positive definite unless D,a=s=0: triangle inequality on 1+2z^a+2z^s (diagonal5) or 1+2z^a (diagonal3). T- blocks are always positive definite: off-diagonal modulus<=9<11 or<=5<15. Thus rank<=2 forces the entire2x2 Schur complement to vanish.',
    'Each T+ cross column uses two coefficient vectors in{0,1,2}^5 with total4. Each T- cross column uses at most2 positive and2 negative coefficients across10 positions. These finite pools cover every binary B,C. The code first tests both diagonal Schur equations, then its off-diagonal equation, exactly in Z[zeta5].',
    'For T+,128 possible first columns and128 second columns give304 rank2 blocks;3152 binary lifts,520 admissible. Every admissible lift has an explicit integer q with q^t(8T)q<0 or q^t(15U)q<0. For T-,32 first and32 second columns give no rank2 block. Hence both field nullities a,b are<=1.',
    'If just one T+ diagonal block is singular, exchange the two lines. If both are singular, both sides contain all5 exterior grids. T-kernel indicators force zero edges between corresponding grids and a perfect matching between distinct grids. Since hM acts antipodally on each C4, those matchings are C4 automorphisms. On normalized checkerboards U is [[2I5,B],[B^t,2I5]], B diagonal0, otherwise+/-1. PSD implies BB^t=4I; two rows overlap in3 positions, so their inner product is odd: impossible. This last argument does not require z.',
    'Galois conjugacy gives null_Q T=nu0+4a+4b<=14. A Conway completion needs nullity>=14, hence nu0=6,a=b=1. Swapping2,3 normalizes the remaining quotient to B having diagonal cell-counts2 and off-diagonal0, C all cell-counts1. This swap commutes with z and hM.',
    'In that quotient the z-trivial rank overF7 is5. Phi5 is irreducible overF7 since7 has order4 modulo5. The rational character splitting remains invertible modulo7: group order10 and denominators2,4,5,8,15 are units.',
    'The same necessary Schur equations modulo7 have no T+ rank<=2 block (88 columns on each side). Its only singular left principal block is the same grid case, covered by line exchange or the both-grid contradiction. For T-,212 columns on each side yield16 blocks. Only8 binary lifts have the normalized cell-counts, and all8 violate C1prime:3 neighbours in a partial outer star whose cap is2. Therefore both field ranks are>=3.',
    'Consequently, whenever local T/U PSD and rational nullity14 hold, rank_F7(8T)>=5+4*3+4*3=29. The accepted earlier GLOBAL bound rank_F7(8T)<=28 rules out extension of every border in this local symmetry family. That global bound is an input from the existing research, not proved anew here.',
    'No claim that all local PSD borders have nullity<=9, that all their relations are side relations, or that H-MATCH/C1 is resolved in general.'
]


def run(certificates):
    certs = json.loads(Path(certificates).read_text(encoding='utf-8'))['certificates']
    plus, plus_report = small_rank_blocks('+')
    minus, minus_report = small_rank_blocks('-')
    assert plus_report['columns'] == [128, 128] and len(plus) == 304
    assert minus_report['columns'] == [32, 32] and not minus
    counts, psd_sides, used, fixtures = Counter(), Counter(), 0, set()
    for block in plus:
        for B, C in plus_lifts(block['S']):
            rows = graph(block, B, C)
            fixture_type = (block['left'][0], block['right'][0])
            if fixture_type not in fixtures:
                geometry_fixture(block, B, C)
                fixtures.add(fixture_type)
            failure = admissibility_failure(rows)
            counts[failure['kind'] if failure else 'admissible'] += 1
            if failure:
                continue
            check_negative(rows, certs[used])
            psd_sides[certs[used]['side']] += 1
            used += 1
    assert used == len(certs) == 520 and sum(counts.values()) == 3152
    assert dict(psd_sides) == {'U': 416, 'T': 104}
    table = quotient_table()
    plus7, p7_report = small_rank_blocks('+', 7)
    minus7, m7_report = small_rank_blocks('-', 7)
    assert not plus7 and p7_report['columns'] == [88, 88]
    assert len(minus7) == 16 and m7_report['columns'] == [212, 212]
    witnesses = []
    for block in minus7:
        for B, C in target_minus_lifts(block['D']):
            rows = graph(block, B, C)
            failure = admissibility_failure(rows)
            assert failure and failure['kind'] == 'C1prime'
            assert failure['degree'] == 3 and failure['cap'] == 2
            witnesses.append(dict(block=block, B=B, C=C, failure=failure))
    assert len(witnesses) == 8
    assert all(pow(7, i, 5) != 1 for i in (1, 2, 3)) and pow(7, 4, 5) == 1
    return dict(status='EXACT_FINITE_LOCAL_FAMILY_OBSTRUCTION', labels=LABELS,
        theorem='Local <z,hM>-invariant admissible T/U-PSD borders have nullityT<=14; at nullity14 their F7 rank is>=29.',
        global_input='Every Conway border must have rational rankT<=30 and rank_F7(8T)<=28 (accepted earlier global result).',
        consequence='No Conway completion of this entire LOCAL symmetry family; no global automorphism assumption.',
        open='The observed local ceiling9 and absence of mixed relations are not proved.',
        rational_plus=plus_report, rational_minus=minus_report, lifts=dict(counts),
        negative_certificates=dict(count=used, sides=dict(psd_sides), arithmetic='integer'),
        quotient_table=table, modular_plus=p7_report, modular_minus=m7_report,
        modular_C1prime_witnesses=witnesses,
        checks=dict(exact_fourier_geometry_fixtures=sorted(fixtures), field_degree_mod7=4), proof=PROOF)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates', type=Path, default=Path(__file__).resolve().parents[2]
        / 'data/codex_local_global_20261015/z5_hm_negative_certificates.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(args.certificates)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'rational_plus', 'rational_minus', 'lifts',
        'negative_certificates', 'modular_plus', 'modular_minus', 'checks')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
