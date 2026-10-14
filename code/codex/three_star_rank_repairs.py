"""Exact rank-one loss under star-preserving edge switches of a 34-label seed.

The seed's PSD/rank31 certification is a PRECONDITION, supplied by its
producer. This script computes a new response metric and explores changes;
it does not independently certify the seed's rank or reconstruct the seed.
No result here is a full SRG. Only one-switch repairs are exhausted.
"""
import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import json
import sys
import time

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_ambient_upper import upper15, psd_or_witness


CENTRES = (0, 1, 2)
LABELS = tuple(p for p in combinations(range(14), 2)
               if p[1] != (p[0] ^ 1) and set(p).intersection(CENTRES))
GROUPS = tuple(tuple(i for i, p in enumerate(LABELS)
                     if tuple(c for c in CENTRES if c in p) == (c0,))
               for c0 in CENTRES)
STARS = sp.Matrix(34, 3, lambda i, c: int(c in LABELS[i]))


def load_gamma(path):
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    labels = [tuple(sorted(p)) for p in data.get('labels', LABELS)]
    matrix = data.get('gamma', data.get('adjacency'))
    if len(labels) != 34 or set(labels) != set(LABELS):
        raise ValueError('Expected the 34 labels meeting centres {0,1,2}.')
    if matrix is None or len(matrix) != 34 or any(len(row) != 34 for row in matrix):
        raise ValueError('Expected a 34 by 34 gamma/adjacency matrix.')
    if any(x not in (0, 1) for row in matrix for x in row):
        raise ValueError('Seed adjacency must be binary.')
    old = {p:i for i, p in enumerate(labels)}
    gamma = [[int(matrix[old[p]][old[q]]) for q in LABELS] for p in LABELS]
    if any(gamma[i][i] or gamma[i][j] != gamma[j][i]
           for i in range(34) for j in range(34)):
        raise ValueError('Expected a symmetric adjacency with zero diagonal.')
    return gamma


def k8(p, q):
    return 3*len(set(p).intersection(q)) + sum((c ^ 1) in q for c in p) - 2


def spectral_matrix(gamma):
    return sp.Matrix(34, 34, lambda i, j:
                     24*int(i == j)-8*gamma[i][j]-k8(LABELS[i], LABELS[j]))


def quotient_basis():
    # Three anchors belonging to just one centre each eliminate star sums.
    anchors = [g[0] for g in GROUPS]
    others = [i for i in range(34) if i not in anchors]
    Z = sp.zeros(34, 31)
    for j, i in enumerate(others):
        Z[i, j] = 1
        for c, anchor in enumerate(anchors):
            Z[anchor, j] = -STARS[i, c]
    assert STARS.T * Z == sp.zeros(3, 31)
    return Z


def response_metric(M):
    """Return integer W,d with T^+ = W/d, for M=8T with the stated kernel."""
    if M*STARS != sp.zeros(34, 3):
        raise ValueError('Input does not obey the three exact star relations.')
    Z = quotient_basis()
    H = Z.T*M*Z
    # This inverse is required for the NEW switch responses. No seed rank scan.
    inverse = H.inv(method='DM')
    den = lcm(*(int(x.q) for x in inverse))
    numerator = inverse.applyfunc(lambda x: int(x*den))
    W = 8*Z*numerator*Z.T
    common = gcd(den, *(int(x) for x in W))
    return [[int(W[i, j])//common for j in range(34)] for i in range(34)], den//common


def rectangles():
    """Each unordered rectangle is yielded once; no overlap vertex can move."""
    for first, second in combinations(GROUPS, 2):
        for (u, r), (v, s) in product(combinations(first, 2), combinations(second, 2)):
            yield u, r, v, s
    for group in GROUPS:
        for a, b, c, d in combinations(group, 4):
            yield a, b, c, d
            yield a, c, b, d
            yield a, d, b, c


def binary_sign(gamma, rectangle):
    u, r, v, s = rectangle
    values = gamma[u][v], gamma[r][s], gamma[u][s], gamma[r][v]
    if values == (0, 0, 1, 1):
        return 1
    if values == (1, 1, 0, 0):
        return -1
    return 0


def boundary_masks(gamma):
    rows = [0]*49
    for c in range(14):
        rows[0] |= 1 << (1+c)
        rows[1+c] |= 1 | (1 << (1+(c ^ 1)))
    for i, p in enumerate(LABELS):
        for c in p:
            rows[1+c] |= 1 << (15+i)
            rows[15+i] |= 1 << (1+c)
        for j, value in enumerate(gamma[i]):
            if value:
                rows[15+i] |= 1 << (15+j)
    return rows


def switch_caps(rows, rectangle):
    """Only pairs affected by a legal binary switch need new cap checks."""
    u, r, v, s = (15+i for i in rectangle)
    changed = {u, r, v, s}
    updated = rows[:]
    for i, j in ((u, v), (r, s), (u, s), (r, v)):
        updated[i] ^= 1 << j
        updated[j] ^= 1 << i
    # Degrees, three star sums, and all other common-neighbour counts persist.
    for i in changed:
        for j in range(49):
            if i == j or (j in changed and j < i):
                continue
            common = (updated[i] & updated[j]).bit_count()
            edge = (updated[i] >> j) & 1
            if common > 2-edge:
                return False
    return True


def switch_response(W, den, rectangle, sign):
    u, r, v, s = rectangle
    alpha = W[u][u]+W[r][r]-2*W[u][r]
    beta = W[v][v]+W[s][s]-2*W[v][s]
    gamma = W[u][v]-W[u][s]-W[r][v]+W[r][s]
    numerator = (den-sign*gamma)**2-alpha*beta
    return numerator, alpha, beta, gamma


def switched(gamma, rectangle):
    out = [row[:] for row in gamma]
    u, r, v, s = rectangle
    for i, j in ((u, v), (r, s), (u, s), (r, v)):
        out[i][j] = out[j][i] = 1-out[i][j]
    return out


def extra_relation(W, den, rectangle, sign, beta, gamma):
    u, r, v, s = rectangle
    q = [sign*beta*(row[u]-row[r]) + (den-sign*gamma)*(row[v]-row[s]) for row in W]
    common = gcd(*q)
    q = [x//common for x in q]
    if next(x for x in q if x) < 0:
        q = [-x for x in q]
    return q


def exact_psd(matrix):
    """Exact scalar Schur pivots; a zero PSD pivot must have a zero row."""
    M = matrix.copy()
    for i in range(M.rows):
        pivot = M[i, i]
        if pivot < 0:
            return False
        if not pivot:
            if any(M[i, j] for j in range(i+1, M.cols)):
                return False
            continue
        for j in range(i+1, M.rows):
            for k in range(j, M.cols):
                value = M[j, k]-M[j, i]*M[i, k]/pivot
                M[j, k] = M[k, j] = value
    return True


def analyse(gamma, candidate_directory):
    start = time.perf_counter()
    M = spectral_matrix(gamma)
    W, den = response_metric(M)
    rows = boundary_masks(gamma)
    counts = Counter()
    repairs = []
    positive_moves = []
    closest = []
    for rectangle in rectangles():
        counts['rectangle_geometries'] += 1
        sign = binary_sign(gamma, rectangle)
        if not sign:
            continue
        counts['binary_legal'] += 1
        if not switch_caps(rows, rectangle):
            counts['local_cap_rejections'] += 1
            continue
        counts['locally_admissible'] += 1
        value, alpha, beta, cross = switch_response(W, den, rectangle, sign)
        # Positive definiteness on the quotient is the producer's precondition.
        if not (alpha > 0 and beta > 0 and alpha*beta > cross*cross):
            raise ValueError('The seed PSD/rank31 precondition fails on a switch subspace.')
        if value < 0:
            counts['destroys_PSD'] += 1
        elif value > 0:
            counts['PSD_but_still_rank31'] += 1
            positive_moves.append(dict(rectangle=rectangle, sign=sign))
        else:
            counts['PSD_rank30'] += 1
            new_gamma = switched(gamma, rectangle)
            q = extra_relation(W, den, rectangle, sign, beta, cross)
            new_M = spectral_matrix(new_gamma)
            # Verify the newly constructed relation, not the seed's rank.
            assert new_M*sp.Matrix(q) == sp.zeros(34, 1)
            assert STARS.T*sp.Matrix(q) == sp.zeros(3, 1)
            upper = psd_or_witness(upper15(new_gamma))['psd']
            record = dict(rectangle=rectangle, sign=sign, extra_relation=q,
                          ambient_upper_gram_psd=upper)
            if upper:
                path = candidate_directory / f'rank30_switch_{len(repairs):04d}.json'
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(dict(labels=LABELS, gamma=new_gamma,
                                                provenance=record), indent=2)+'\n', encoding='utf-8')
                record['candidate_path'] = str(path)
            repairs.append(record)
        closest.append((abs(value), value, rectangle, sign))
    assert counts['rectangle_geometries'] == 10585
    closest.sort()
    return dict(
        status='EXACT_ONE_SWITCH_ANALYSIS_CONDITIONAL_ON_PRODUCER_PSD_RANK31',
        labels=LABELS, counts=dict(counts), repairs=repairs,
        psd_rank31_moves=positive_moves,
        response_metric_denominator=den,
        determinant_ratio_denominator=den*den,
        closest_by_absolute_determinant_ratio=[dict(numerator=v, rectangle=r, sign=s)
                                               for _, v, r, s in closest[:10]],
        elapsed_seconds=time.perf_counter()-start,
        scope=[
            'The input PSD/rank31 certification is taken from its producer, not repeated.',
            'Every binary legal single rectangle switch preserving all three star sums is covered.',
            'All such switches fix both overlap-vertex rows and all vertex degrees.',
            'Longer or simultaneous trades, or trades moving overlap rows, are not exhausted.',
            'Rank30 is only a necessary condition; the fifty outside columns remain to be constructed.',
            'No consequence about automorphism groups follows from these ranks alone.'
        ])


def walk(gamma, maximum_states, candidate_directory):
    """Bounded exploration through PSD/rank31 neighbours, with an exact metric."""
    start = time.perf_counter()
    key = lambda g: bytes(v for row in g for v in row)
    queue = deque([(gamma, [])])
    seen = {key(gamma)}
    counts = Counter()
    processed = 0
    repairs = []
    seed_moves = None
    while queue and processed < maximum_states:
        current, history = queue.popleft()
        report = analyse(current, candidate_directory/f'state_{processed:05d}')
        if seed_moves is None:
            seed_moves = report['psd_rank31_moves']
        counts.update(report['counts'])
        processed += 1
        for repair in report['repairs']:
            repairs.append(dict(path=history+[dict(rectangle=repair['rectangle'], sign=repair['sign'])],
                                **repair))
        if any('candidate_path' in r for r in report['repairs']):
            break
        for move in report['psd_rank31_moves']:
            neighbour = switched(current, move['rectangle'])
            code = key(neighbour)
            if code not in seen:
                seen.add(code)
                queue.append((neighbour, history+[move]))
    found = any('candidate_path' in r for r in repairs)
    return dict(
        status='RANK30_REPAIR_FOUND' if found else
               'BOUNDED_PSD_SWITCH_SEARCH' if queue else 'PSD_RANK31_SWITCH_COMPONENT_EXHAUSTED',
        processed_states=processed, maximum_states=maximum_states,
        discovered_states=len(seen), pending_states=len(queue),
        counts=dict(counts), repairs=repairs, seed_psd_rank31_moves=seed_moves,
        seed_sha256=sha256(key(gamma)).hexdigest(), elapsed_seconds=time.perf_counter()-start,
        scope=[
            'Only paths through locally admissible PSD/rank31 rectangle neighbours are explored.',
            'All states preserve the seed overlap rows and all vertex degrees.',
            'Intermediate states are not filtered by T<=7Pi_SS; exported rank30 repairs are.',
            'A bounded search is not an exclusion; component exhaustion only concerns this move family.',
            'No full SRG is constructed and no automorphism conclusion follows.'
        ])


def self_test():
    Z = quotient_basis()
    P = sp.eye(34)-STARS*(STARS.T*STARS).inv()*STARS.T
    assert Z.shape == (34, 31)
    shapes = list(rectangles())
    assert len(shapes) == 10585
    rectangle = shapes[0]
    u, r, v, s = rectangle
    a, b = sp.zeros(34, 1), sp.zeros(34, 1)
    a[u], a[r], b[v], b[s] = 1, -1, 1, -1
    checks = []
    for scale in (1, 2, 3):
        W, den = response_metric(8*scale*P)
        for sign in (-1, 1):
            value, alpha, beta, cross = switch_response(W, den, rectangle, sign)
            # Here alpha=beta=2/scale, cross=0. All three outcomes occur.
            assert sp.Rational(value, den*den) == 1-sp.Rational(4, scale*scale)
            if scale == 2:
                q = extra_relation(W, den, rectangle, sign, beta, cross)
                changed = scale*P-sign*(a*b.T+b*a.T)
                assert changed*sp.Matrix(q) == sp.zeros(34, 1)
                assert exact_psd(changed)
            checks.append(dict(scale=scale, sign=sign, determinant_ratio=str(sp.Rational(value, den*den))))
    assert exact_psd(sp.Matrix([[0, 0], [0, 1]]))
    assert not exact_psd(sp.Matrix([[0, 1], [1, 1]]))
    assert not exact_psd(sp.diag(1, -1))
    return dict(status='OWN_SWITCH_FORMULA_CHECKS_PASS', rectangle_geometries=len(shapes), cases=checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gamma')
    parser.add_argument('--assume-psd-rank31', action='store_true',
                        help='Use the producer certification; do not audit the seed rank.')
    parser.add_argument('--output', required=True)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--walk-states', type=int, default=1,
                        help='Optional bounded exploration of PSD/rank31 neighbours.')
    args = parser.parse_args()
    output = Path(args.output)
    if args.self_test:
        result = self_test()
    else:
        if not args.gamma or not args.assume_psd_rank31:
            parser.error('--gamma and --assume-psd-rank31 are required for a producer-certified seed.')
        if args.walk_states < 1:
            parser.error('--walk-states must be positive.')
        gamma = load_gamma(args.gamma)
        result = (analyse(gamma, output.parent/'rank30_repairs') if args.walk_states == 1 else
                  walk(gamma, args.walk_states, output.parent/'rank30_repairs'))
        result['input'] = args.gamma
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k, v in result.items() if k in (
        'status', 'counts', 'elapsed_seconds', 'cases', 'processed_states', 'pending_states')}))


if __name__ == '__main__':
    main()
