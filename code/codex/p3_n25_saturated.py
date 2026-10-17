"""P3/N25 WITH ALL TRIANGLES INTERNAL: finite supports and certificates.

This conditional subfamily does NOT exhaust the forced P3/N25 target.
See note 245 for the stronger direct proof and the open-triangle obstruction.
The optional boundary LP is a necessary relaxation, not a graph construction.
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import reduce
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from math import gcd, lcm
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[2]
PERMS = list(permutations(range(3)))
PATHS = {
    1: (1, 1), 2: (1, 3, 2), 3: (2, 3, 5, 4),
    4: (2, 3, 5, 6, 2), 5: (2, 3, 5, 6, 3, 1),
    6: (2, 3, 5, 6, 3, 5, 4),
}


def relabel(t, p):
    return tuple(sum(1 << p[i] for i in range(3) if m >> i & 1) for m in t)


def path_key(t):
    return min(t, t[::-1])


def shapes():
    """The 22 shapes after n2+3s >= 5, before assigning positive labels."""
    for star in range(2):
        for b in product(range(13), range(7), range(5), range(4), range(3), range(3)):
            if sum((i + 1) * v for i, v in enumerate(b)) + 3 * star != 12:
                continue
            n2 = sum(i * v for i, v in enumerate(b))
            if 5 <= n2 + 3 * star <= 6:
                yield star, b, 1 + n2 + 2 * star, n2


def supports():
    variants = {l: sorted({path_key(relabel(t, p)) for p in PERMS})
                for l, t in PATHS.items()}
    seen = set()
    for star, b, n0, n2 in shapes():
        choices = [list(combinations_with_replacement(variants[l], b[l - 1]))
                   for l in range(1, 7)]
        for groups in product(*choices):
            paths = tuple(sorted(t for group in groups for t in group))
            labels = [m for t in paths for m in t] + ([7, 1, 2, 4] if star else [])
            if any(sum(m >> i & 1 for m in labels) != 8 for i in range(3)):
                continue
            if any(sum(m & pair == pair for m in labels) > 2 for pair in (3, 5, 6)):
                continue
            canonical = min(tuple(sorted(path_key(relabel(t, p)) for t in paths))
                            for p in PERMS)
            if (star, canonical) in seen:
                continue
            seen.add((star, canonical))
            yield {'id': len(seen), 'star': star, 'path_counts': b,
                   'isolates': n0, 'degree2': n2, 'paths': canonical}


def adjacency(row):
    a = [[0] * 28 for _ in range(28)]
    offset = 3
    blocks = [(t, False) for t in row['paths']]
    if row['star']:
        blocks.append(((7, 1, 2, 4), True))
    for labels, is_star in blocks:
        for j, mask in enumerate(labels):
            for i in range(3):
                if mask >> i & 1:
                    a[i][offset + j] = a[offset + j][i] = 1
            if j:
                k = offset if is_star else offset + j - 1
                a[k][offset + j] = a[offset + j][k] = 1
        offset += len(labels)
    assert offset + row['isolates'] == 28
    return a


def primitive(v):
    den = lcm(*(x.denominator for x in v))
    w = [int(x * den) for x in v]
    g = reduce(gcd, w, 0)
    return [x // g for x in w] if g else w


def exact_psd(a):
    """Rational congruence elimination; negative witness or integer nullspace."""
    n = len(a)
    q = [[Fraction(x) for x in row] for row in a]
    basis = [[Fraction(i == j) for i in range(n)] for j in range(n)]
    active = list(range(n))
    while active:
        for i in active:
            if q[i][i] < 0:
                v = primitive(basis[i])
                value = sum(v[j] * a[j][k] * v[k] for j in range(n) for k in range(n))
                assert value < 0
                return {'negative_vector': v, 'value': value}
        p = next((i for i in active if q[i][i] > 0), None)
        if p is None:
            for i, j in combinations(active, 2):
                if q[i][j]:
                    sign = -1 if q[i][j] > 0 else 1
                    v = primitive([x + sign * y for x, y in zip(basis[i], basis[j])])
                    value = sum(v[j] * a[j][k] * v[k] for j in range(n) for k in range(n))
                    assert value < 0
                    return {'negative_vector': v, 'value': value}
            return {'kernel': [primitive(basis[i]) for i in active]}
        active.remove(p)
        factors = {i: q[p][i] / q[p][p] for i in active}
        for i in active:
            basis[i] = [x - factors[i] * y for x, y in zip(basis[i], basis[p])]
        for i in active:
            for j in active:
                q[i][j] -= factors[i] * q[p][j]
    return {'kernel': []}


def gram(a, which):
    n = len(a)
    if which == 0:
        return [[27 * (i == j) - 9 * a[i][j] + 1 for j in range(n)] for i in range(n)]
    return [[44 * (i == j) + 11 * a[i][j] - 2 for j in range(n)] for i in range(n)]


def boundary(row, spectral_one_vertex=False):
    import numpy as np
    from scipy.optimize import linprog
    from twisted_prism_extension import certify_infeasible, spectral_masks
    a = np.array(adjacency(row), dtype=np.int64)
    deficit = 2 - a - a @ a
    pairs = list(combinations(range(28), 2))
    # Since every edge is already triangulated, all outside masks are independent.
    forbidden = [(i, j) for i, j in pairs if a[i, j] or deficit[i, j] == 0]
    candidates = []
    for k in range(3):
        for pp in combinations(range(3), k):
            if any(deficit[i, j] == 0 for i, j in combinations(pp, 2)):
                continue
            available = [q for q in range(3, 28) if not any(a[p, q] for p in pp)]
            for nn in combinations(available, 4 + k):
                mask = np.zeros(28, dtype=np.int64)
                mask[list(pp) + list(nn)] = 1
                candidates.append(mask)
    candidates = np.array(candidates, dtype=np.int64).reshape((-1, 28))
    keep = np.all(candidates @ a <= 2 - candidates, axis=1)
    for i, j in forbidden:
        keep &= candidates[:, i] * candidates[:, j] == 0
    candidates = candidates[keep]
    for which, (const, coef) in enumerate(((1, -9), (-2, 11))):
        for v in row['projectors'][which]['kernel']:
            keep = coef * (candidates @ np.array(v, dtype=np.int64)) + const * sum(v) == 0
            candidates = candidates[keep]
    before = len(candidates)
    if spectral_one_vertex and before:
        candidates = spectral_masks(a, candidates, 14)
    rows = [np.ones(len(candidates), dtype=np.int64)]
    rows += [candidates[:, i] for i in range(28)]
    rows += [candidates[:, i] * candidates[:, j] for i, j in pairs]
    m = np.array(rows, dtype=np.int64)
    b = np.r_[71, 14 - a.sum(axis=0), [deficit[i, j] for i, j in pairs]].astype(np.int64)
    upper = np.full(len(candidates), 71, dtype=np.int64)
    result = None if not len(candidates) else linprog(np.zeros(len(candidates)), A_eq=m,
                          b_eq=b, bounds=(0, 71), method='highs')
    report = {'masks_after_kernel': before, 'masks': len(candidates)}
    if result is None or result.status == 2:
        cert = certify_infeasible(m, b, upper)
        if cert:
            y = np.array(cert['row_multipliers'], dtype=np.int64)
            values = y @ m
            lower = sum(min(0, int(c) * 71) for c in values)
            target = sum(int(c) * int(d) for c, d in zip(y, b))
            assert lower == cert['box_lower_bound'] > target == cert['target']
            report.update(status='excluded_exact', certificate=cert)
        else:
            report['status'] = 'numerically_infeasible_uncertified'
    elif result.success:
        report.update(status='lp_feasible_unresolved', max_residual=float(abs(m @ result.x - b).max()))
    else:
        report.update(status='solver_unknown', solver_message=result.message)
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--boundary', action='store_true')
    parser.add_argument('--one-vertex-spectral', action='store_true')
    parser.add_argument('--out', type=Path, default=ROOT / 'data/codex_p3_n25_saturated.json')
    args = parser.parse_args()
    started = time.monotonic()
    report = {'scope': 'CONDITIONAL: P3 independent, N25, (A+4I)(1_P-1_N)=-4*1, ALL support triangles internal; note245',
              'shapes_before_labelling': list(shapes()), 'supports': []}
    for row in supports():
        a = adjacency(row)
        row['projectors'] = [exact_psd(gram(a, which)) for which in range(2)]
        row['status'] = ('excluded_exact_spectral' if any('negative_vector' in q for q in row['projectors'])
                         else 'passes_support_spectra')
        if args.boundary and row['status'] == 'passes_support_spectra':
            row['boundary'] = boundary(row, args.one_vertex_spectral)
            row['status'] = row['boundary']['status']
        report['supports'].append(row)
        print(json.dumps({'id': row['id'], 'status': row['status'],
                          'masks': row.get('boundary', {}).get('masks')}), flush=True)
    report['counts'] = dict(Counter(r['status'] for r in report['supports']))
    report['elapsed_seconds'] = time.monotonic() - started
    args.out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'counts': report['counts'], 'seconds': report['elapsed_seconds']}), flush=True)


if __name__ == '__main__':
    main()
