"""Extend the exact induced-graph census to orders eight and nine.

Retains all free parameters. Target-family counts are counts of signed
representatives, not proven lower bounds for distinct projected vectors.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb
import argparse
import json
import time

from sympy import Matrix, Symbol, expand
from seven_vertex_census import ROOT, decode, grow, extension_system


@lru_cache(None)
def ir_orders(adj):
    """Canonical labelling by individualisation/refinement, with automorphisms.

    Every choice in the first nonsingleton cell is explored, so the set of
    leaf orders and its minimum are invariant under relabelling. Retaining
    all minimum orders also gives canonical markings, not only graphs.
    """
    n = len(adj)
    def refine(cells):
        while True:
            masks = [sum(1 << i for i in cell) for cell in cells]
            updated = []
            for cell in cells:
                by_signature = {}
                for i in cell:
                    sig = tuple((adj[i] & mask).bit_count() for mask in masks)
                    by_signature.setdefault(sig, []).append(i)
                updated.extend(tuple(by_signature[sig]) for sig in sorted(by_signature))
            if len(updated) == len(cells):
                return tuple(updated)
            cells = updated
    degrees = sorted({row.bit_count() for row in adj})
    initial = tuple(tuple(i for i in range(n) if adj[i].bit_count() == degree) for degree in degrees)
    best, orders = None, []
    from seven_vertex_census import encode
    def search(cells):
        nonlocal best, orders
        cells = refine(cells)
        split = next((j for j, cell in enumerate(cells) if len(cell) > 1), None)
        if split is None:
            order = tuple(cell[0] for cell in cells)
            code = encode(adj, order)
            if best is None or code < best:
                best, orders = code, [order]
            elif code == best:
                orders.append(order)
            return
        cell = cells[split]
        for i in cell:
            search(cells[:split]+((i,), tuple(j for j in cell if j != i))+cells[split+1:])
    search(initial)
    return best, tuple(orders)


def target_families(n, graphs, solution):
    counts = Counter()
    smallest = []
    for (code, adj), value in zip(graphs.items(), solution):
        if min(row.bit_count() for row in adj) >= 3:
            smallest.append({'code': code, 'degrees': sorted(row.bit_count() for row in adj), 'count': str(value)})
        for negative_vertices in combinations(range(n), 4 if n == 8 else 3):
            negative = sum(1 << i for i in negative_vertices)
            positive = ((1 << n)-1) ^ negative
            e_neg = sum((adj[i] & negative).bit_count() for i in negative_vertices)//2
            e_pos = sum((adj[i] & positive).bit_count() for i in range(n) if positive >> i & 1)//2
            cross = sum((adj[i] & positive).bit_count() for i in negative_vertices)
            Q = 3*n+(0 if n == 8 else 1)-2*(e_pos+e_neg-cross)
            if Q > 8:
                continue
            key = f'Q{Q}_edges{e_pos}_{e_neg}_cross{cross}'
            counts[key] += (1 if n == 8 else 2)*value
    return {'signed_representative_counts': {k: str(expand(v)) for k, v in sorted(counts.items())},
            'minimum_degree_three_types': smallest}


def run(n):
    start = time.monotonic()
    source = ROOT/'data'/('codex_seven_vertex_census.json' if n == 8 else 'codex_order8_census.json')
    previous = json.loads(source.read_text())
    if n == 9:
        import seven_vertex_census as C
        C.canonical_orders = ir_orders
        C.canon.cache_clear()
    old_params = [Symbol(name) for name in previous['parameters']]
    previous_counts, previous_graphs = {}, {}
    from sympy import Rational
    for row in previous['counts']:
        code = row['code']
        previous_graphs[code] = decode(n-1, code)
        coeff = list(map(Rational, row['affine']))
        previous_counts[code] = coeff[0]+sum(c*p for c, p in zip(coeff[1:], old_params))
    graphs = grow(previous_graphs)
    print('Order', n, 'graph types:', len(graphs), 'seconds', round(time.monotonic()-start, 2), flush=True)
    matrix, target, keys = extension_system(previous_counts, previous_graphs, graphs)
    print('Extension matrix:', matrix.shape, 'seconds', round(time.monotonic()-start, 2), flush=True)
    zero = {p: 0 for p in old_params}
    rhs_columns = Matrix.hstack(target.subs(zero), *(target.diff(p) for p in old_params))
    if n == 9:
        from sparse_census_elimination import eliminate
        coordinates, free_columns, pivots = eliminate(matrix, rhs_columns, verbose=True)
    else:
        reduced, pivots = matrix.row_join(rhs_columns).rref()
        assert all(i < len(graphs) for i in pivots), 'New relations on previous invariants require separate handling.'
        free_columns = [i for i in range(len(graphs)) if i not in pivots]
    free = [Symbol(f'h{n}_{list(graphs)[i]}') for i in free_columns]
    params = old_params+free
    if n == 9:
        solution = coordinates*Matrix([1]+params)
    else:
        solution = Matrix.zeros(len(graphs), 1)
        for i, p in zip(free_columns, free):
            solution[i] = p
        for row, col in enumerate(pivots):
            solution[col] = (reduced[row, len(graphs)]
                             +sum(reduced[row, len(graphs)+1+i]*p for i, p in enumerate(old_params))
                             -sum(reduced[row, i]*p for i, p in zip(free_columns, free)))
    print('Rational elimination done: rank', len(pivots), 'new free parameters', len(free),
          'seconds', round(time.monotonic()-start, 2), flush=True)
    # Check via coefficient matrices to keep verification over Q.
    if n != 9:
        coordinates = Matrix([[value.subs({p: 0 for p in params})]+[value.coeff(p) for p in params]
                              for value in solution])
    padded_rhs = rhs_columns.row_join(Matrix.zeros(matrix.rows, len(free)))
    assert matrix*coordinates == padded_rhs
    totals = [sum(coordinates[:, i]) for i in range(coordinates.cols)]
    assert totals == [comb(99, n)]+[0]*len(params)
    families = target_families(n, graphs, solution)
    print('Target families:', families['signed_representative_counts'], flush=True)
    report = {'vertices': n, 'graph_types': len(graphs), 'equations': matrix.rows,
              'canonical_convention': 'individualisation_refinement' if n == 9 else 'degree_refinement_then_all_cell_permutations',
              'rank': len(pivots), 'parameters': list(map(str, params)),
              'new_free_graph_codes': [list(graphs)[i] for i in free_columns],
              'flag_keys': keys,
              'counts': [{'code': code, 'edges': sum(row.bit_count() for row in adj)//2,
                           'degrees': sorted(row.bit_count() for row in adj), 'count': str(expand(value)),
                           'affine': list(map(str, coordinates.row(i)))}
                          for i, ((code, adj), value) in enumerate(zip(graphs.items(), solution))],
              'sparse_matrix': [(i, j, int(value)) for (i, j), value in matrix.todok().items()],
              'rhs_affine_columns': [list(map(str, rhs_columns.row(i))) for i in range(rhs_columns.rows)],
              'families': families, 'seconds': round(time.monotonic()-start, 3),
              'scope': 'Counts of representatives only; no assertion of distinct projections or rank exclusion.'}
    (ROOT/f'data/codex_order{n}_census.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print('Order', n, 'complete in', round(time.monotonic()-start, 2), 'seconds.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--order', type=int, choices=(8, 9), default=8)
    run(parser.parse_args().order)
