"""Exact mod-7 obstruction to a repeated hub around a six-grid line.

Six grids G_k through Theta, plus H^i_{0k} for all three apices and k=1..5,
plus H^0_{1k}, k=2..5, cannot coexist with H^1_{12} when rank_7(A-3I)=37.
All unknown intersections are binary; tightness gives two ones in each
triple. The finite tree is certified by nonzero order-20 minors.
No SRG completion or exclusion of every six-grid line is asserted.
"""
from collections import Counter
from itertools import product
import argparse
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / 'data/codex_grid_kernel_rank_obstruction.json.gz'
BASE = [('G', k) for k in range(6)] + [('H', i, 0, k) for i in range(3) for k in range(1, 6)]
EXTRAS = [('H', 0, 1, k) for k in range(2, 6)] + [('H', 1, 1, 2)]


def options(extra):
    available = [k for k in range(1, 6) if k not in extra[2:]]
    assert len(available) == 3
    return list(product(available, repeat=2))


def gram(choices):
    labels = BASE + EXTRAS[:len(choices)]
    missing = {extra: dict(zip([i for i in range(3) if i != extra[1]], choice))
               for extra, choice in zip(EXTRAS, choices)}
    out = [[0] * len(labels) for _ in labels]
    for i, u in enumerate(labels):
        for j in range(i, len(labels)):
            v = labels[j]
            if u == v:
                value = 9
            elif u[0] == v[0] == 'G':
                value = 3
            elif u[0] == 'G' or v[0] == 'G':
                g, h = (u, v) if u[0] == 'G' else (v, u)
                value = 3 if g[1] in h[2:] else 1
            elif u[1] == v[1]:
                value = 3 if set(u[2:]) & set(v[2:]) else 1
            elif set(u[2:]) & set(v[2:]):
                value = 0
            else:
                star, extra = (u, v) if u[2] == 0 else (v, u)
                assert star in BASE and extra in missing
                value = int(star[3] != missing[extra][star[1]])
            out[i][j] = out[j][i] = value
    return out


def rank_pivots(matrix):
    a = [[v % 7 for v in row] for row in matrix]
    n, m = len(a), len(a[0])
    order = list(range(n))
    pivot_rows, pivot_cols = [], []
    r = 0
    for j in range(m):
        p = next((i for i in range(r, n) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        order[r], order[p] = order[p], order[r]
        pivot_rows.append(order[r])
        pivot_cols.append(j)
        inv = pow(a[r][j], -1, 7)
        a[r] = [v * inv % 7 for v in a[r]]
        for i in range(r + 1, n):
            c = a[i][j]
            if c:
                a[i] = [(x - c * y) % 7 for x, y in zip(a[i], a[r])]
        r += 1
        if r == n:
            break
    return r, pivot_rows, pivot_cols


def minor_det(matrix, rows, cols):
    # Independent determinant calculation for the archived certificate.
    a = [[matrix[i][j] % 7 for j in cols] for i in rows]
    result = 1
    for j in range(len(a)):
        p = next((i for i in range(j, len(a)) if a[i][j]), None)
        if p is None:
            return 0
        if p != j:
            a[j], a[p] = a[p], a[j]
            result = -result
        diagonal = a[j][j]
        result = result * diagonal % 7
        inv = pow(diagonal, -1, 7)
        for i in range(j + 1, len(a)):
            c = a[i][j] * inv % 7
            for k in range(j + 1, len(a)):
                a[i][k] = (a[i][k] - c * a[j][k]) % 7
            a[i][j] = 0
    return result % 7


def token(choices):
    return tuple(tuple(x) for x in choices)


def generate():
    report = {'scope': __doc__, 'modulus': 7, 'rank_bound': 19,
              'base_labels': BASE, 'extra_labels': EXTRAS,
              'base_rank': rank_pivots(gram(()))[0], 'stages': [], 'rejected': []}
    survivors = [()]
    for extra in EXTRAS:
        next_survivors, distribution = [], Counter()
        for prefix in survivors:
            for choice in options(extra):
                current = prefix + (choice,)
                matrix = gram(current)
                rank, rows, cols = rank_pivots(matrix)
                distribution[rank] += 1
                if rank <= 19:
                    next_survivors.append(current)
                else:
                    rows, cols = rows[:20], cols[:20]
                    det = minor_det(matrix, rows, cols)
                    assert det
                    report['rejected'].append({'choices': current, 'rank': rank,
                                               'rows': rows, 'cols': cols, 'det_mod7': det})
        report['stages'].append({'rank_distribution': dict(distribution),
                                 'survivors': len(next_survivors)})
        survivors = next_survivors
    assert not survivors
    # Normalize tuples and integer dictionary keys before checking the archive.
    report = json.loads(json.dumps(report))
    verify(report)
    with gzip.GzipFile(filename=PATH, mode='wb', mtime=0) as stream:
        stream.write(json.dumps(report, separators=(',', ':')).encode('utf-8'))


def verify(report):
    assert report['scope'] == __doc__ and report['modulus'] == 7 and report['rank_bound'] == 19
    assert report['base_labels'] == [list(x) for x in BASE]
    assert report['extra_labels'] == [list(x) for x in EXTRAS]
    assert report['base_rank'] == rank_pivots(gram(()))[0] == 18
    records = {token(row['choices']): row for row in report['rejected']}
    assert len(records) == len(report['rejected'])
    used = set()
    survivors = [()]
    stages = []
    for extra in EXTRAS:
        next_survivors, distribution = [], Counter()
        for prefix in survivors:
            for choice in options(extra):
                current = prefix + (choice,)
                matrix = gram(current)
                actual_rank = rank_pivots(matrix)[0]
                distribution[str(actual_rank)] += 1
                if current in records:
                    row = records[current]
                    rows, cols = row['rows'], row['cols']
                    assert len(rows) == len(cols) == len(set(rows)) == len(set(cols)) == 20
                    assert all(0 <= i < len(matrix) for i in rows + cols)
                    assert minor_det(matrix, rows, cols) == row['det_mod7'] != 0
                    assert actual_rank == row['rank'] >= 20
                    used.add(current)
                else:
                    assert actual_rank <= 19
                    next_survivors.append(current)
        stages.append({'rank_distribution': dict(distribution), 'survivors': len(next_survivors)})
        survivors = next_survivors
    assert not survivors and used == set(records)
    assert stages == report['stages']
    # A rejected prefix covers every subsequent completion. These disjoint
    # branches account for all 9^5 possibilities before rank pruning.
    coverage = sum(9 ** (len(EXTRAS) - len(prefix)) for prefix in used)
    assert coverage == 9 ** 5 == 59049
    assert len(used) == 433
    print('Verified', len(used), 'nonzero order-20 minors, covering all', coverage, 'choices.', flush=True)
    for i, row in enumerate(stages, 1):
        print('Stage', i, row, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        with gzip.open(PATH, 'rt', encoding='utf-8') as stream:
            verify(json.load(stream))
    else:
        generate()
