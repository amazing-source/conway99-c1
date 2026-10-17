"""Exact small induced-subgraph census and joint projection shells for C1.

Counts are obtained from extension identities involving zero, one or two
marked vertices. A rank test reports any freedom; no unknown count is guessed.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import json

from sympy import Matrix


def decode(n, code):
    adj = [0]*n
    for k, (i, j) in enumerate(combinations(range(n), 2)):
        if code >> k & 1:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    return tuple(adj)


def encode(adj, order):
    return sum(1 << k for k, (i, j) in enumerate(combinations(range(len(order)), 2))
               if adj[order[i]] >> order[j] & 1)


@lru_cache(None)
def canonical_flag(adj, mark=0):
    return min((encode(adj, p), sum(1 << i for i, j in enumerate(p) if mark >> j & 1))
               for p in permutations(range(len(adj))))


def allowed_graphs(n):
    answer = {}
    for code in range(1 << comb(n, 2)):
        adj = decode(n, code)
        if any((adj[i] & adj[j]).bit_count() > (1 if adj[i] >> j & 1 else 2)
               for i, j in combinations(range(n), 2)):
            continue
        canon, _ = canonical_flag(adj)
        answer[canon] = decode(n, canon)
    return dict(sorted(answer.items()))


def marks(n):
    return [sum(1 << i for i in c) for s in range(min(2, n)+1)
            for c in combinations(range(n), s)]


def extension_census(previous, n, params):
    size, degree, lam, mu = params
    graphs = allowed_graphs(n)
    rhs = Counter()
    for code, count in previous.items():
        adj = decode(n-1, code)
        for mark in marks(n-1):
            key = canonical_flag(adj, mark)
            chosen = [i for i in range(n-1) if mark >> i & 1]
            if not chosen:
                value = size-(n-1)
            elif len(chosen) == 1:
                value = degree-adj[chosen[0]].bit_count()
            else:
                i, j = chosen
                value = (lam if adj[i] >> j & 1 else mu)-(adj[i] & adj[j]).bit_count()
            rhs[key] += count*value
    columns = []
    for adj in graphs.values():
        coeff = Counter()
        for v in range(n):
            order = [i for i in range(n) if i != v]
            sub = decode(n-1, encode(adj, order))
            neighbours = sum(1 << i for i, j in enumerate(order) if adj[v] >> j & 1)
            for mark in marks(n-1):
                if neighbours & mark == mark:
                    coeff[canonical_flag(sub, mark)] += 1
        assert not (set(coeff)-set(rhs))
        columns.append([coeff[key] for key in rhs])
    matrix = Matrix.hstack(*map(Matrix, columns))
    target = Matrix(list(rhs.values()))
    solution, parameters = matrix.gauss_jordan_solve(target)
    print('vertices', n, 'types', len(graphs), 'equations', len(rhs),
          'free_parameters', len(parameters), flush=True)
    if parameters:
        print('free solutions', list(zip(graphs, map(str, solution))), flush=True)
        raise RuntimeError('Extension identities leave freedom; do not claim exact counts')
    assert all(x.q == 1 and x >= 0 for x in solution)
    assert matrix*solution == target
    counts = dict(zip(graphs, map(int, solution)))
    assert sum(counts.values()) == comb(size, n)
    independent_rows = list(matrix.T.rref()[1])
    assert len(independent_rows) == len(graphs)
    minor_det = matrix[independent_rows, :].det(method='domain-ge')
    assert minor_det != 0
    return counts, {'vertices': n, 'graph_types': len(graphs), 'equations': len(rhs),
                    'counts_by_canonical_edge_code': counts,
                    'flag_keys': list(rhs), 'constraint_matrix': [list(map(int, matrix.row(i))) for i in range(matrix.rows)],
                    'right_hand_side': list(rhs.values()),
                    'independent_rows': independent_rows, 'nonzero_minor_determinant': str(minor_det)}


def joint_shells(counts):
    shells = {n: Counter() for n in range(2, 6)}
    for support in range(2, 6):
        for code, multiplicity in counts[support].items():
            adj = decode(support, code)
            for vector in product((-1, 1), repeat=support):
                sm = sum(vector)
                if sm % 3:
                    continue
                aq = sum(2*vector[i]*vector[j] for i, j in combinations(range(support), 2)
                         if adj[i] >> j & 1)
                q = 3*support-aq+(sm//3)**2
                qb = 7*support-q
                shells[support][(q, qb)] += multiplicity
    # Norm five also contains the same-sign patterns +/- (2 e_i + e_j).
    for code, multiplicity in counts[2].items():
        for vector in ((2, 1), (1, 2), (-2, -1), (-1, -2)):
            aq = 2*vector[0]*vector[1]*code
            q = 15-aq+1
            shells[5][(q, 35-q)] += multiplicity
    return {str(n): [{'Q': q, 'Qbar': qb, 'count': count}
                    for (q, qb), count in sorted(shell.items())]
            for n, shell in shells.items()}


def main():
    params = (99, 14, 1, 2)
    counts, censuses = {1: {0: 99}}, []
    for n in range(2, 6):
        counts[n], report = extension_census(counts[n-1], n, params)
        censuses.append(report)
    shells = joint_shells(counts)
    # Every induced subset of the 3x3 rook graph is enumerated directly.
    rook = tuple(sum(1 << j for j in range(9) if i != j and (i//3 == j//3 or i%3 == j%3))
                 for i in range(9))
    rook_counts = {0: 9}
    for n in range(2, 6):
        rook_counts, _ = extension_census(rook_counts, n, (9, 4, 1, 2))
        direct = Counter()
        for vertices in combinations(range(9), n):
            sub = decode(n, encode(rook, vertices))
            direct[canonical_flag(sub)[0]] += 1
        assert all(rook_counts.get(key, 0) == direct.get(key, 0) for key in set(rook_counts) | set(direct))
    # Independent combinatorial derivation of the newly strengthened norm-10 bound.
    paths, claws, triangle_isolates, cycles, paws = 91476, 27720, 13860, 2079, 8316
    far_paths = 52*paths-2*(4*cycles)  # each house gives two P4 with an external 3-neighbour
    norm5_q10 = 2*(far_paths+51*claws+51*triangle_isolates+40*cycles+42*paws)
    assert norm5_q10 == 14586264
    assert next(row['count'] for row in shells['5'] if row['Q'] == 10) == norm5_q10
    totals = {str(n): factor*comb(99, n)+(4*comb(99, 2) if n == 5 else 0)
              for n, factor in ((2, 2), (3, 2), (4, 6), (5, 10))}
    assert all(sum(row['count'] for row in rows) == totals[n] for n, rows in shells.items())
    lower_m = Counter()
    for rows in shells.values():
        for row in rows:
            lower_m[row['Q']//2] += row['count']
    assert lower_m[5] == 18001368
    print(json.dumps(shells, indent=2), flush=True)
    report = {'parameters': params, 'induced_subgraph_censuses': censuses,
              'joint_shells': shells,
              'total_U_shells': totals, 'lower_bounds_M_q_coefficients': dict(sorted(lower_m.items())),
              'independent_norm5_Q10_count': norm5_q10,
              'direct_graph_control': 'All subsets of sizes 2..5 of the rook_3x3 graph',
              'scope': 'Exact low-norm pairs in U; no theta feasibility or graph-exclusion assertion.'}
    root = Path(__file__).resolve().parents[2]
    (root/'data/codex_joint_theta_small_shells.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
