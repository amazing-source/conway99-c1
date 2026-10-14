"""Try exact incidence-fixing orthogonal reflections of rank30 boundaries.

For an alternating four-cycle u of the root-label incidence matrix D,
H=I-u*u^t/2 is orthogonal and fixes D. Thus H Gamma H preserves both
Gram inequalities and the rank, if it is again a binary adjacency.
No seed rank or PSD check is repeated.
"""
import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_star_rank_repairs import LABELS, load_gamma, boundary_masks
from three_star_connected_repairs import classify_gamma


def four_cycles():
    index = {p:i for i, p in enumerate(LABELS)}
    result = set()
    for a, b in combinations(range(14), 2):
        for x, y in combinations([c for c in range(14) if c not in (a, b)], 2):
            edges = [(tuple(sorted((a, x))), 1), (tuple(sorted((b, y))), 1),
                     (tuple(sorted((a, y))), -1), (tuple(sorted((b, x))), -1)]
            if not all(p in index for p, _ in edges):
                continue
            u = tuple(sorted((index[p], v) for p, v in edges))
            if u[0][1] < 0:
                u = tuple((i, -v) for i, v in u)
            result.add(u)
    assert len(result) == 156
    return sorted(result)


def analyse(gamma, closed_pairs):
    q = [int(p[0] in (0, 1) and p[1]//2 in closed_pairs) for p in LABELS]
    counts = Counter()
    candidates = []
    for entries in four_cycles():
        counts['incidence_four_cycles'] += 1
        dot = sum(v*q[i] for i, v in entries)
        if not dot:
            counts['fixes_closed_relation'] += 1
            continue
        counts['moves_closed_relation'] += 1
        u = dict(entries)
        Gu = [sum(gamma[i][j]*v for j, v in entries) for i in range(34)]
        theta_values = {Gu[i]*v for i, v in entries}
        if len(theta_values) != 1:
            counts['nonzero_diagonal_after_conjugation'] += 1
            continue
        theta = next(iter(theta_values))
        if any(Gu[i] not in (-2, 0, 2) for i in range(34) if i not in u):
            counts['nonintegral_after_conjugation'] += 1
            continue
        w = [Gu[i]-theta*u.get(i, 0) for i in range(34)]
        out = [[gamma[i][j]-(u.get(i, 0)*w[j]+w[i]*u.get(j, 0))//2
                for j in range(34)] for i in range(34)]
        assert all(out[i][i] == 0 and all(out[i][j] in (0, 1) for j in range(34))
                   for i in range(34))
        counts['binary_conjugates'] += 1
        rows = boundary_masks(out)
        if any(row.bit_count() > 14 for row in rows) or any(
                (rows[i] & rows[j]).bit_count() > 2-((rows[i] >> j) & 1)
                for i in range(49) for j in range(i+1, 49)):
            counts['local_cap_rejections'] += 1
            continue
        structure = classify_gamma(out)
        candidates.append(dict(u=entries, theta=theta, dot_closed_relation=dot,
                               new_relation_twice=[2*q[i]-dot*u.get(i, 0) for i in range(34)],
                               components=structure['outer_pair_components'], gamma=out))
    return dict(status='EXACT_INCIDENCE_REFLECTION_SCAN', counts=dict(counts),
                candidates=candidates,
                scope='The156 alternating four-cycles supported on the34 labels only. General orthogonal transformations and larger switching sets are not exhausted.')


def self_test():
    import sympy as sp
    from three_star_rank_repairs import k8
    K = sp.Matrix(34, 34, lambda i, j:sp.Rational(k8(LABELS[i], LABELS[j]), 8))
    D = sp.Matrix(14, 34, lambda a, j:int(a in LABELS[j]))
    q = sp.Matrix([int(p[0] in (0, 1) and p[1] in (2, 3)) for p in LABELS])
    w = sp.Matrix([sp.Rational(1 if i < 4 else -1, 2) for i in range(14)])
    assert D.T*w == q
    checks = 0
    for other in range(2, 7):
        members = {2, 3, 2*other, 2*other+1}
        q = sp.Matrix([int(p[0] in (0, 1) and p[1] in members) for p in LABELS])
        formula = sp.Matrix([int(p[1] in members) if p[0] in (0, 1)
                             else 1+int(p[1] in members)-2 for p in LABELS])
        assert K*q == formula
        for entries in four_cycles():
            u = sp.zeros(34, 1)
            for i, value in entries:
                u[i] = value
            dot = (u.T*q)[0]
            if not dot:
                continue
            assert D*u == sp.zeros(14, 1)
            z = 2*q-dot*u
            negative = [i for i in range(34) if z[i] < 0]
            assert len(negative) == 1
            i = negative[0]
            assert z[i] == -1 and (3*z-K*z)[i] == -1
            checks += 1
    return dict(status='VERIFIED_OWN_SYMBOLIC_IDENTITIES',
                closed_four_label_incidence_formula=True, two_line_templates=5,
                moving_reflection_obstructions=checks, no_peer_rank_recomputed=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gamma')
    parser.add_argument('--closed-pairs', type=int, nargs='+')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    else:
        if not args.gamma or not args.closed_pairs:
            parser.error('--gamma and --closed-pairs are required.')
        result = analyse(load_gamma(args.gamma), args.closed_pairs)
        result['input'] = args.gamma
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k, v in result.items() if k not in ('candidates', 'scope')}))


if __name__ == '__main__':
    main()
