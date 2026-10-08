"""Parameterised census from order one, in a basis of dense graph counts.

Produces independent-test packets for SRG(v,k,1,2). Checks every count on
the 3x3 rook graph and reproduces the existing (99,14) census exactly.
The 243-vertex packets are predictions, pending independent actual counts.
"""
from collections import Counter
from itertools import combinations
from math import comb
import argparse
import json
import time

from sympy import Matrix, Rational, Symbol
from seven_vertex_census import ROOT, canon, decode, encode, grow, extension_system
from sparse_census_elimination import eliminate
import seven_vertex_census as census

DEGREE_CANONICAL_ORDERS = census.canonical_orders


def affine_families(n, graphs, coordinates):
    weights = {}
    for j, (code, adj) in enumerate(graphs.items()):
        def add(name, multiplicity):
            weights.setdefault(name, [0]*len(graphs))[j] += multiplicity
        if n == 7:
            for Y in combinations(range(7), 2):
                ym = sum(1 << i for i in Y); wm = 127 ^ ym
                ep = sum((adj[i] & wm).bit_count() for i in range(7) if wm >> i & 1)//2
                en = sum((adj[i] & ym).bit_count() for i in Y)//2
                cross = sum((adj[i] & wm).bit_count() for i in Y)
                if (ep, en, cross) == (6, 1, 0):
                    bowtie = max((adj[i] & wm).bit_count() for i in range(7) if wm >> i & 1) == 4
                    add('bowtie_minus_far_edge' if bowtie else 'house_minus_far_edge', 2)
        if n == 8:
            for Y in combinations(range(8), 4):
                ym = sum(1 << i for i in Y); wm = 255 ^ ym
                ep = sum((adj[i] & wm).bit_count() for i in range(8) if wm >> i & 1)//2
                en = sum((adj[i] & ym).bit_count() for i in Y)//2
                cross = sum((adj[i] & wm).bit_count() for i in Y)
                if (ep, en, cross) == (4, 4, 0):
                    add('F8_four_minus_four', 1)
            for y in range(8):
                degree = adj[y].bit_count()
                e = sum(row.bit_count() for row in adj)//2-degree
                if e-degree in (10, 11):
                    add(f'seven_minus_one_edges{e}_cross{degree}', 2)
        if n == 9:
            for Y in combinations(range(9), 3):
                ym = sum(1 << i for i in Y); wm = 511 ^ ym
                ep = sum((adj[i] & wm).bit_count() for i in range(9) if wm >> i & 1)//2
                en = sum((adj[i] & ym).bit_count() for i in Y)//2
                cross = sum((adj[i] & wm).bit_count() for i in Y)
                if ep+en-cross >= 10:
                    add(f'six_minus_three_edges{ep}_{en}_cross{cross}', 2)
    return {name: list(map(str, (Matrix([w])*coordinates).row(0))) for name, w in weights.items()}


def run(v, k, maximum_order=8):
    start = time.monotonic()
    census.canonical_orders = DEGREE_CANONICAL_ORDERS
    census.canon.cache_clear()
    graphs = {0: (0,)}
    coords = Matrix([[v]])
    params = []
    stages = []
    for n in range(2, maximum_order+1):
        if n == 9:
            from higher_vertex_census import ir_orders
            census.canonical_orders = ir_orders
            census.canon.cache_clear()
        previous = graphs
        previous_counts = dict(zip(graphs, coords*Matrix([1]+params)))
        graphs = grow(previous)
        matrix, rhs, flags = extension_system(previous_counts, previous, graphs, params=(v, k, 1, 2))
        zeros = dict.fromkeys(params, 0)
        rhs_columns = Matrix.hstack(rhs.subs(zeros), *(rhs.diff(p) for p in params))
        coords, free, pivots = eliminate(matrix, rhs_columns)
        old_width = len(params)+1
        selected = []
        if n == 6:
            selected = [i for i, adj in enumerate(graphs.values()) if all(row.bit_count() == 3 for row in adj)]
            new_params = [Symbol('P')]
        elif n == 7:
            selected = [i for i, adj in enumerate(graphs.values()) if min(row.bit_count() for row in adj) >= 3]
            new_params = [Symbol('H')]
        elif n >= 8:
            selected = [i for i, adj in enumerate(graphs.values()) if min(row.bit_count() for row in adj) >= 3]
            new_params = [Symbol(f'C{n}_{list(graphs)[i]}') for i in selected]
        else:
            new_params = []
        assert len(selected) == len(free) == len(new_params)
        if free:
            dense_rows = coords[selected, :]
            change = dense_rows[:, old_width:].inv()
            right = coords[:, old_width:]*change
            coords = (coords[:, :old_width]-right*dense_rows[:, :old_width]).row_join(right)
        params += new_params
        assert matrix*coords == rhs_columns.row_join(Matrix.zeros(matrix.rows, len(free)))
        assert [sum(coords[:, i]) for i in range(coords.cols)] == [comb(v, n)]+[0]*len(params)
        stage = {'order': n, 'graph_types': len(graphs), 'equations': matrix.rows, 'rank': len(pivots),
                 'parameters': list(map(str, params)),
                 'canonical_convention': 'individualisation_refinement' if n == 9 else 'degree_refinement_then_all_cell_permutations',
                 'new_parameter_graphs': [{'name': str(name), 'code': list(graphs)[i],
                                           'adjacency_bits': list(list(graphs.values())[i])}
                                          for name, i in zip(new_params, selected)],
                 'counts': [{'code': code, 'adjacency_bits': list(adj),
                             'edges': sum(row.bit_count() for row in adj)//2,
                             'degrees': sorted(row.bit_count() for row in adj),
                             'affine': list(map(str, coords.row(i)))}
                            for i, (code, adj) in enumerate(graphs.items())],
                 'families': affine_families(n, graphs, coords)}
        stages.append(stage)
        print((v, k), 'order', n, 'types', len(graphs), 'parameters', len(params), flush=True)
    return {'srg_parameters': [v, k, 1, 2], 'maximum_order': maximum_order,
            'family_convention': 'Signed combinatorial representatives; not projected-vector counts in these test graphs.',
            'stages': stages, 'seconds': round(time.monotonic()-start, 3)}


def verify_rook(packet):
    graph = tuple(sum(1 << j for j in range(9) if i != j and
                      (i//3 == j//3 or i % 3 == j % 3)) for i in range(9))
    parameters = {}
    checked = 0
    for stage in packet['stages']:
        if stage['order'] == 9:
            from higher_vertex_census import ir_orders
            census.canonical_orders = ir_orders
        else:
            census.canonical_orders = DEGREE_CANONICAL_ORDERS
        census.canon.cache_clear()
        counts = Counter(canon(decode(stage['order'], encode(graph, order)))[0]
                         for order in combinations(range(9), stage['order']))
        for item in stage['new_parameter_graphs']:
            parameters[item['name']] = counts[item['code']]
        values = Matrix([1]+[parameters[name] for name in stage['parameters']])
        for row in stage['counts']:
            prediction = (Matrix([[Rational(x) for x in row['affine']]])*values)[0]
            assert prediction == counts[row['code']], (stage['order'], row['code'], prediction, counts[row['code']])
            checked += 1
    return {'all_type_counts_checked': checked, 'actual_dense_invariants': parameters}


def verify_99(packet):
    checks = []
    files = [(7, 'codex_seven_vertex_census.json'), (8, 'codex_order8_census.json')]
    if packet['maximum_order'] == 9:
        files.append((9, 'codex_order9_census.json'))
    for n, file in files:
        old = json.loads((ROOT/'data'/file).read_text())
        old_rows = {row['code']: list(map(Rational, row['affine'])) for row in old['counts']}
        width = len(old['parameters'])+1
        transform = [[1]+[0]*(width-1), [0, 1]+[0]*(width-2), [133056, -6, Rational(-1, 4)]+[0]*(width-3)]
        stage = next(s for s in packet['stages'] if s['order'] == n)
        old8 = json.loads((ROOT/'data/codex_order8_census.json').read_text())
        rows8 = {row['code']: list(map(Rational, row['affine'])) for row in old8['counts']}
        for name in stage['parameters'][2:]:
            code = int(name.split('_')[1])
            if n == 9 and name.startswith('C8_'):
                transform.append(rows8[code]+[0]*(width-len(rows8[code])))
            else:
                transform.append(old_rows[code])
        transform = Matrix(transform)
        for row in stage['counts']:
            assert Matrix([[Rational(x) for x in row['affine']]])*transform == Matrix([old_rows[row['code']]])
        checks.append({'order': n, 'all_type_formulas_checked': len(old_rows)})
    return checks


def main(maximum_order=8):
    for v, k in [(99, 14), (243, 22), (9, 4)]:
        packet = run(v, k, maximum_order)
        if v == 99:
            packet['existing_99_census_agreement'] = verify_99(packet)
        if v == 9:
            packet['actual_graph_verification'] = verify_rook(packet)
        path = ROOT/f'data/codex_census_validation_{v}.json'
        path.write_text(json.dumps(packet, indent=2)+'\n', encoding='utf-8')
        print('Saved', path.name, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-order', type=int, choices=(8, 9), default=8)
    main(parser.parse_args().max_order)
