"""Complete forest-label enumeration for P3/N25, allowing outside triangles.

Uses the analytic reductions in note245, and certificates for new exclusions.
No support is declared impossible from a floating eigenvalue alone.
"""
import argparse
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
import time

import numpy as np
from p3_n25_saturated import ROOT, PERMS, relabel, path_key, adjacency, gram, exact_psd


def variants(length):
    result = set()
    for ends in product((1, 2, 4), repeat=2):
        for mid in product((3, 5, 6), repeat=length - 1):
            t = (ends[0],) + mid + (ends[1],)
            if any((t[i] & t[i + 1]).bit_count() > 1 for i in range(length)):
                continue
            if any((t[i] & t[i + 2]).bit_count() > 1 for i in range(length - 1)):
                continue
            if any(sum(bool(t[j] >> p & 1) for j in (i - 1, i + 1) if 0 <= j < len(t))
                   > (1 if t[i] >> p & 1 else 2) for i in range(len(t)) for p in range(3)):
                continue
            result.add(path_key(t))
    return sorted(result)


def shapes():
    for star in range(2):
        for b in product(range(13), range(7), range(5), range(4), range(3), range(3)):
            if sum((i + 1) * v for i, v in enumerate(b)) + 3 * star != 12:
                continue
            n2 = sum(i * v for i, v in enumerate(b))
            if n2 + 3 * star > 6 or (star == 0 and n2 <= 2):
                continue
            yield star, b, 1 + n2 + 2 * star, n2


def component_data(t):
    degrees = tuple(sum(m >> p & 1 for m in t) for p in range(3))
    pairs = tuple(sum(m & p == p for m in t) for p in (3, 5, 6))
    delta = sum(t[i] & t[i + 1] == 0 for i in range(len(t) - 1))
    xn = sum((t[i - 1] & t[i + 1]).bit_count() for i in range(1, len(t) - 1))
    return degrees, pairs, delta, xn


def enumerate_supports():
    all_variants = {l: variants(l) for l in range(1, 7)}
    group_cache = {}
    seen = set()
    for star, b, n0, n2 in shapes():
        groups = []
        for l in range(6, 0, -1):
            count = b[l - 1]
            if not count:
                continue
            key = (l, count, star)
            if key not in group_cache:
                choices = []
                for ts in combinations_with_replacement(all_variants[l], count):
                    data = [component_data(t) for t in ts]
                    degrees = tuple(sum(d[0][i] for d in data) for i in range(3))
                    pairs = tuple(sum(d[1][i] for d in data) for i in range(3))
                    if max(degrees) <= 8 - 2 * star and max(pairs) <= 2 - star:
                        choices.append((ts, degrees, pairs, sum(d[2] for d in data), sum(d[3] for d in data)))
                group_cache[key] = choices
            groups.append(group_cache[key])

        def recurse(idx, paths, degrees, pairs, delta, xn):
            if idx == len(groups):
                if degrees != (8, 8, 8):
                    return
                xp = sum(c * (c - 1) for c in pairs)
                if delta < 2 or 3 * delta < 21 - 4 * (n2 + 3 * star) + xp + xn:
                    return
                canonical = min(tuple(sorted(path_key(relabel(t, p)) for t in paths)) for p in PERMS)
                if (star, canonical) in seen:
                    return
                seen.add((star, canonical))
                yield {'id': len(seen), 'star': star, 'path_counts': b,
                       'isolates': n0, 'degree2': n2, 'paths': canonical,
                       'outside_N_triangles': delta, 'X_N': xn}
                return
            for ts, dd, cc, de, xx in groups[idx]:
                d = tuple(degrees[i] + dd[i] for i in range(3))
                c = tuple(pairs[i] + cc[i] for i in range(3))
                if max(d) > 8 or max(c) > 2:
                    continue
                yield from recurse(idx + 1, paths + ts, d, c, delta + de, xn + xx)

        yield from recurse(0, (), (2 * star,) * 3, (star,) * 3, 0, 0)


def spectral_result(row):
    a = adjacency(row)
    for which in range(2):
        q = gram(a, which)
        values, vectors = np.linalg.eigh(np.array(q, dtype=float))
        if values[0] < -1e-8:
            for scale in (10, 100, 1000, 10000, 100000):
                v = np.rint(scale * vectors[:, 0]).astype(np.int64).tolist()
                val = sum(v[i] * q[i][j] * v[j] for i in range(28) for j in range(28))
                if val < 0:
                    return {'status': 'excluded_exact_spectral', 'projector': which,
                            'negative_vector': v, 'value': val}
            exact = exact_psd(q)
            if 'negative_vector' in exact:
                return dict(status='excluded_exact_spectral', projector=which, **exact)
    return {'status': 'not_excluded_by_support_spectra'}


def boundary_pilot(row, dual_first=False):
    from scipy.optimize import linprog
    from twisted_prism_extension import certify_infeasible
    a = np.array(adjacency(row), dtype=np.int64)
    deficit = 2 - a - a @ a
    pairs = list(combinations(range(28), 2))
    forbidden = [sum(1 << j for j in range(28) if i != j and deficit[i, j] == 0)
                 for i in range(28)]
    candidates = []
    for k in range(4):
        for pp in combinations(range(3), k):
            if any(deficit[p, q] == 0 for p, q in combinations(pp, 2)):
                continue
            available = [q for q in range(3, 28) if all(deficit[p, q] > 0 for p in pp)]
            for nn in combinations(available, 4 + k):
                bits = 0
                good = True
                for q in nn:
                    if bits & forbidden[q]:
                        good = False
                        break
                    bits |= 1 << q
                if good:
                    mask = np.zeros(28, dtype=np.int64)
                    mask[list(pp) + list(nn)] = 1
                    candidates.append(mask)
    candidates = np.array(candidates, dtype=np.int64).reshape((-1, 28))
    candidates = candidates[np.all(candidates @ a <= 2 - candidates, axis=1)]
    for which, (const, coef) in enumerate(((1, -9), (-2, 11))):
        exact = exact_psd(gram(a.tolist(), which))
        assert 'kernel' in exact
        for v in exact['kernel']:
            assert 28 * abs(coef) * max(map(abs, v), default=0) + abs(const * sum(v)) < 2**63
            candidates = candidates[coef * (candidates @ np.array(v)) + const * sum(v) == 0]
    matrix = np.array([np.ones(len(candidates), dtype=np.int64)]
                      + [candidates[:, i] for i in range(28)]
                      + [candidates[:, i] * candidates[:, j] for i, j in pairs])
    rhs = np.r_[71, 14 - a.sum(axis=0), [deficit[i, j] for i, j in pairs]].astype(np.int64)
    result = None if not len(candidates) or dual_first else linprog(np.zeros(len(candidates)),
                     A_eq=matrix, b_eq=rhs, bounds=(0, 71), method='highs', options={'time_limit': 30})
    report = {'id': row['id'], 'delta': row['outside_N_triangles'], 'masks': len(candidates)}
    if result is not None and result.success:
        report.update(status='lp_feasible_unresolved', max_residual=float(abs(matrix @ result.x - rhs).max()))
    elif result is None or result.status in (1, 2):
        cert = certify_infeasible(matrix, rhs, np.full(len(candidates), 71, dtype=np.int64))
        if cert:
            y = np.array(cert['row_multipliers'], dtype=np.int64)
            lower = sum(min(0, int(c) * 71) for c in y @ matrix)
            target = sum(int(x) * int(b) for x, b in zip(y, rhs))
            assert lower == cert['box_lower_bound'] > target == cert['target']
            report.update(status='excluded_exact', certificate=cert)
        else:
            report['status'] = ('no_certificate_found' if dual_first or (result is not None and result.status == 1)
                                else 'numerically_infeasible_uncertified')
    else:
        report['status'] = 'solver_unknown'
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT / 'data/codex_p3_n25_open_triangles.json')
    parser.add_argument('--pilot', action='store_true', help='Read saved enumeration and test three delta2 forest shapes')
    parser.add_argument('--ids', help='Comma-separated saved support IDs; boundary test only')
    parser.add_argument('--delta', type=int, help='Boundary test of all spectral survivors with this delta')
    parser.add_argument('--boundary-out', type=Path)
    parser.add_argument('--dual-first', action='store_true', help='Seek an exact separating certificate directly')
    args = parser.parse_args()
    if args.ids or args.delta is not None:
        report = json.loads(args.out.read_text())
        wanted = ({int(v) for v in args.ids.split(',')} if args.ids else
                  {r['id'] for r in report['supports'] if r['outside_N_triangles'] == args.delta
                   and r['status'] == 'not_excluded_by_support_spectra'})
        if args.boundary_out is None:
            args.boundary_out = ROOT / 'data/codex_p3_n25_boundary.json'
        results = []
        for row in report['supports']:
            if row['id'] not in wanted:
                continue
            result = boundary_pilot(row, args.dual_first)
            results.append(result)
            print(json.dumps({k: v for k, v in result.items() if k != 'certificate'}), flush=True)
            args.boundary_out.write_text(json.dumps(results, indent=2) + '\n')
        return
    if args.pilot:
        report = json.loads(args.out.read_text())
        chosen, seen = [], set()
        for row in report['supports']:
            key = row['star'], tuple(row['path_counts'])
            if (row['outside_N_triangles'] == 2 and row['status'] == 'not_excluded_by_support_spectra'
                    and key not in seen):
                chosen.append(row)
                seen.add(key)
            if len(chosen) == 3:
                break
        results = []
        for row in chosen:
            result = boundary_pilot(row)
            results.append(result)
            print(json.dumps({k: v for k, v in result.items() if k != 'certificate'}), flush=True)
        (ROOT / 'data/codex_p3_n25_boundary_pilot.json').write_text(json.dumps(results, indent=2) + '\n')
        return
    started = time.monotonic()
    report = {'scope': 'All 32 forest shapes; arbitrary admissible positive labels; note245', 'supports': []}
    for row in enumerate_supports():
        row.update(spectral_result(row))
        report['supports'].append(row)
        if len(report['supports']) % 100 == 0:
            print(json.dumps({'processed': len(report['supports']), 'seconds': time.monotonic() - started}), flush=True)
    report['counts'] = dict(Counter(r['status'] for r in report['supports']))
    report['by_delta'] = {str(k): dict(Counter(r['status'] for r in report['supports'] if r['outside_N_triangles'] == k))
                          for k in sorted({r['outside_N_triangles'] for r in report['supports']})}
    report['elapsed_seconds'] = time.monotonic() - started
    args.out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('counts', 'by_delta', 'elapsed_seconds')}), flush=True)


if __name__ == '__main__':
    main()
