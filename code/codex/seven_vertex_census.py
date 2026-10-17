"""Exact order-seven census with every undetermined invariant retained.

Representatives counted here are NOT automatically distinct vectors in M.
Canonical labels use degree refinement, independently cross-checked against
the earlier exhaustive-permutation convention on all 62 six-vertex types.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import json
import time

from sympy import Matrix, SparseMatrix, Symbol, expand
from joint_theta_small_shells import decode, encode, marks

ROOT = Path(__file__).resolve().parents[2]


@lru_cache(None)
def canonical_orders(adj):
    n = len(adj)
    colours = [row.bit_count() for row in adj]
    while True:
        signatures = [(colours[i], tuple(sorted(colours[j] for j in range(n) if adj[i] >> j & 1)))
                      for i in range(n)]
        palette = {sig: k for k, sig in enumerate(sorted(set(signatures)))}
        new = [palette[sig] for sig in signatures]
        if len(set(new)) == len(set(colours)):
            colours = new
            break
        colours = new
    groups = [[i for i in range(n) if colours[i] == c] for c in sorted(set(colours))]
    best, orders = None, []
    for blocks in product(*(permutations(group) for group in groups)):
        order = tuple(i for block in blocks for i in block)
        code = encode(adj, order)
        if best is None or code < best:
            best, orders = code, [order]
        elif code == best:
            orders.append(order)
    return best, tuple(orders)


@lru_cache(None)
def canon(adj, mark=0):
    code, orders = canonical_orders(adj)
    return code, min(sum(1 << i for i, j in enumerate(order) if mark >> j & 1) for order in orders)


def grow(previous):
    graphs = {}
    for adj in previous.values():
        n = len(adj)
        for mask in range(1 << n):
            new = tuple(adj[i] | (((mask >> i) & 1) << n) for i in range(n))+(mask,)
            if any((new[i] & new[j]).bit_count() > (1 if new[i] >> j & 1 else 2)
                   for i, j in combinations(range(n+1), 2)):
                continue
            code = canon(new)[0]
            graphs[code] = decode(n+1, code)
    return dict(sorted(graphs.items()))


def extension_system(previous_counts, previous_graphs, graphs, params=(99, 14, 1, 2)):
    n = len(next(iter(graphs.values())))
    v, k, lam, mu = params
    rhs = Counter()
    for code, adj in previous_graphs.items():
        for mark in marks(n-1):
            vertices = [i for i in range(n-1) if mark >> i & 1]
            if not vertices:
                weight = v-(n-1)
            elif len(vertices) == 1:
                weight = k-adj[vertices[0]].bit_count()
            else:
                i, j = vertices
                weight = (lam if adj[i] >> j & 1 else mu)-(adj[i] & adj[j]).bit_count()
            rhs[canon(adj, mark)] += previous_counts[code]*weight
    row_indices = {key: i for i, key in enumerate(rhs)}
    entries = {}
    for column, adj in enumerate(graphs.values()):
        col = Counter()
        for v in range(n):
            order = [i for i in range(n) if i != v]
            sub = decode(n-1, encode(adj, order))
            neighbours = sum(1 << i for i, j in enumerate(order) if adj[v] >> j & 1)
            for mark in marks(n-1):
                if neighbours & mark == mark:
                    col[canon(sub, mark)] += 1
        assert not (set(col)-set(rhs))
        entries.update({(row_indices[key], column): value for key, value in col.items() if value})
        if n >= 9 and (column+1) % 1000 == 0:
            print('Built', column+1, 'extension columns, nonzero entries', len(entries), flush=True)
    return SparseMatrix(len(rhs), len(graphs), entries), Matrix(list(rhs.values())), list(rhs)


def family_counts(graphs, solution):
    n = len(next(iter(graphs.values())))
    assert n == 7
    by_kind = Counter()
    by_q = Counter()
    min_degree_three = []
    for (code, adj), value in zip(graphs.items(), solution):
        if min(row.bit_count() for row in adj) >= 3:
            min_degree_three.append({'code': code, 'degrees': sorted(row.bit_count() for row in adj),
                                     'count': str(value)})
        for pair in combinations(range(7), 2):
            negative = sum(1 << i for i in pair)
            positive = 127 ^ negative
            e_neg = int(bool(adj[pair[0]] >> pair[1] & 1))
            e_pos = sum((adj[i] & positive).bit_count() for i in range(7) if positive >> i & 1)//2
            cross = sum((adj[i] & positive).bit_count() for i in pair)
            Q = 22-2*(e_pos+e_neg-cross)
            by_q[Q] += 2*value
            if e_neg == 1 and cross == 0 and e_pos == 6:
                kind = 'bowtie' if max(row.bit_count() for row in adj) == 4 else 'house'
                by_kind[kind] += 2*value
    return {'signed_binary_5_minus_2_by_Q': {str(k): str(expand(v)) for k, v in sorted(by_q.items())},
            'norm8_by_positive_support': {k: str(expand(v)) for k, v in by_kind.items()},
            'minimum_degree_three_types': min_degree_three}


def main():
    start = time.monotonic()
    P = Symbol('P')
    old = json.loads((ROOT/'data/codex_six_vertex_grid_audit.json').read_text())['census']['counts']
    previous_counts, previous_graphs, conversion = {}, {}, {}
    for rec in old:
        adj = decode(6, rec['code'])
        code = canon(adj)[0]
        assert code not in previous_counts
        previous_counts[code] = rec['constant']+rec['prism_coefficient']*P
        previous_graphs[code] = decode(6, code)
        conversion[rec['code']] = code
    assert len(previous_counts) == 62
    graphs = grow(previous_graphs)
    print('Order7 graph types:', len(graphs), 'seconds', round(time.monotonic()-start, 2), flush=True)
    matrix, target, keys = extension_system(previous_counts, previous_graphs, graphs)
    print('Extension matrix:', matrix.shape, 'seconds', round(time.monotonic()-start, 2), flush=True)
    # Keep the elimination over Q, not the symbolic-expression domain Q(P).
    # Both right-hand-side columns are integers; P is reintroduced afterwards.
    rhs_columns = Matrix.hstack(target.subs(P, 0), target.diff(P))
    reduced, pivots = matrix.row_join(rhs_columns).rref()
    assert all(i < len(graphs) for i in pivots)
    free_columns = [i for i in range(len(graphs)) if i not in pivots]
    free = [Symbol('h7_'+str(list(graphs)[i])) for i in free_columns]
    solution = Matrix.zeros(len(graphs), 1)
    for i, parameter in zip(free_columns, free):
        solution[i] = parameter
    for row, col in enumerate(pivots):
        solution[col] = (reduced[row, len(graphs)]+P*reduced[row, len(graphs)+1]
                         -sum(reduced[row, i]*parameter for i, parameter in zip(free_columns, free)))
    assert matrix*solution == target
    assert expand(sum(solution)-comb(99, 7)) == 0
    print('New free parameters:', list(free), 'seconds', round(time.monotonic()-start, 2), flush=True)
    families = family_counts(graphs, solution)
    print(json.dumps(families, indent=2), flush=True)
    assert len(pivots) == len(graphs)-len(free)
    assert [solution[i] for i in free_columns] == list(free)
    params = [P]+list(free)
    report = {'vertices': 7, 'graph_types': len(graphs), 'equations': matrix.rows,
              'rank': len(pivots), 'parameters': list(map(str, params)),
              'free_graph_codes': [list(graphs)[i] for i in free_columns],
              'six_vertex_code_conversion': conversion, 'flag_keys': keys,
              'counts': [{'code': code, 'edges': sum(row.bit_count() for row in adj)//2,
                           'degrees': sorted(row.bit_count() for row in adj), 'count': str(expand(value)),
                           'affine': [str(expand(value).subs({p: 0 for p in params}))]
                                     +[str(expand(value).coeff(p)) for p in params]}
                          for (code, adj), value in zip(graphs.items(), solution)],
              'sparse_matrix': [(i, j, int(matrix[i, j])) for i in range(matrix.rows)
                                for j in range(matrix.cols) if matrix[i, j]],
              'rhs': list(map(str, target)), 'families': families,
              'scope': 'Counts of representatives only. Collision losses must be proved before bounding theta coefficients.'}
    (ROOT/'data/codex_seven_vertex_census.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
