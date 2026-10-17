"""Independent six-vertex extension census and finite grid collision audit.

The census uses only extension identities for zero, one or two marked
vertices. Counts are affine in the number P of induced triangular prisms.
"""
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
import json

from sympy import Matrix, Symbol
from joint_theta_small_shells import decode, encode, canonical_flag, marks

ROOT = Path(__file__).resolve().parents[2]


def grown_graphs(previous):
    out = {}
    for adj in previous.values():
        n = len(adj)
        for mask in range(1 << n):
            new = tuple(adj[i] | (((mask >> i) & 1) << n) for i in range(n)) + (mask,)
            if any((new[i] & new[j]).bit_count() > (1 if new[i] >> j & 1 else 2)
                   for i, j in combinations(range(n+1), 2)):
                continue
            code = canonical_flag(new)[0]
            out[code] = decode(n+1, code)
    return dict(sorted(out.items()))


def census_six():
    source = json.loads((ROOT/'data/codex_joint_theta_small_shells.json').read_text())
    counts5 = {int(k): v for k, v in source['induced_subgraph_censuses'][-1]
               ['counts_by_canonical_edge_code'].items()}
    graphs5 = {code: decode(5, code) for code in counts5}
    graphs = grown_graphs(graphs5)
    rhs = Counter()
    for code, adj in graphs5.items():
        for mark in marks(5):
            chosen = [i for i in range(5) if mark >> i & 1]
            if not chosen:
                value = 94
            elif len(chosen) == 1:
                value = 14-adj[chosen[0]].bit_count()
            else:
                i, j = chosen
                value = (1 if adj[i] >> j & 1 else 2)-(adj[i] & adj[j]).bit_count()
            rhs[canonical_flag(adj, mark)] += counts5[code]*value
    columns = []
    for adj in graphs.values():
        col = Counter()
        for v in range(6):
            order = [i for i in range(6) if i != v]
            sub = decode(5, encode(adj, order))
            neighbours = sum(1 << i for i, j in enumerate(order) if adj[v] >> j & 1)
            for mark in marks(5):
                if neighbours & mark == mark:
                    col[canonical_flag(sub, mark)] += 1
        assert not (set(col)-set(rhs))
        columns.append([col[key] for key in rhs])
    matrix = Matrix.hstack(*map(Matrix, columns))
    target = Matrix(list(rhs.values()))
    solution, parameters = matrix.gauss_jordan_solve(target)
    assert len(parameters) == 1
    prism = [code for code, adj in graphs.items()
             if all(row.bit_count() == 3 for row in adj)]
    assert len(prism) == 1
    idx = list(graphs).index(prism[0])
    P = Symbol('P')
    parameter_value = (P-solution[idx].subs(parameters[0], 0))/solution[idx].coeff(parameters[0])
    solution = solution.subs(parameters[0], parameter_value)
    assert matrix*solution == target
    assert sum(solution) == comb(99, 6)
    edge_counts = Counter()
    records = []
    for (code, adj), value in zip(graphs.items(), solution):
        edges = sum(row.bit_count() for row in adj)//2
        edge_counts[edges] += value
        records.append({'code': code, 'edges': edges, 'degrees': sorted(row.bit_count() for row in adj),
                        'count': str(value), 'constant': int(value.subs(P, 0)),
                        'prism_coefficient': int(value.coeff(P))})
    assert edge_counts[7] == 831600+36*P
    assert edge_counts[8] == 20790-9*P
    assert edge_counts[9] == P
    assert [sum(r['edges'] == e for r in records) for e in (7, 8, 9)] == [10, 3, 1]
    assert any(r['edges'] == 8 and r['constant'] == 8316 and r['prism_coefficient'] == -6 for r in records)
    # Triangle minus an anticomplete induced path, counted with both signs.
    triangle_path = 0
    for (_, adj), value in zip(graphs.items(), solution):
        signs = 0
        for triple in combinations(range(6), 3):
            T = sum(1 << i for i in triple)
            Y = 63 ^ T
            if all((adj[i] & T).bit_count() == 2 and not (adj[i] & Y) for i in triple):
                if sum((adj[i] & Y).bit_count() for i in range(6) if Y >> i & 1) == 4:
                    signs += 2
        triangle_path += signs*value
    assert triangle_path == 731808+12*P
    independent_rows = list(matrix.T.rref()[1])
    # Append the prism count to get a square full-rank certificate.
    augmented = matrix.col_join(Matrix([[int(i == idx) for i in range(len(graphs))]]))
    pivots = list(augmented.T.rref()[1])
    minor_det = augmented[pivots, :].det(method='domain-ge')
    assert minor_det
    return {'graph_types': len(graphs), 'equations': matrix.rows, 'rank': len(independent_rows),
            'prism_code': prism[0], 'counts': records, 'edge_totals': {str(k): str(v) for k, v in edge_counts.items()},
            'triangle_minus_far_path_signed_count': str(triangle_path),
            'matrix': [list(map(int, matrix.row(i))) for i in range(matrix.rows)],
            'rhs': list(rhs.values()), 'full_rank_rows_after_prism_constraint': pivots,
            'nonzero_minor_determinant': str(minor_det)}


def grid_audit():
    adj = tuple(sum(1 << j for j in range(9) if i != j and (i//3 == j//3 or i%3 == j%3))
                for i in range(9))
    def edges(mask):
        return sum((adj[i] & mask).bit_count() for i in range(9) if mask >> i & 1)//2
    out = Counter()
    details = Counter()
    by_q = Counter()
    for chosen in combinations(range(9), 3):
        Y = sum(1 << i for i in chosen)
        W = 511 ^ Y
        by_q[22-2*edges(W)] += 1
        if edges(Y) in (1, 2):
            assert edges(W) == edges(Y)+6
            out[f'negative_triple_Q{22-2*edges(W)}'] += 1
    for chosen in combinations(range(9), 4):
        S = sum(1 << i for i in chosen)
        # z outside R has either its unique R-neighbour in S (40 choices)
        # or in R\S (50 choices). Then e(W) = 3+e(S)-d_S(z).
        for d, number in ((0, 50), (1, 40)):
            by_q[16-2*edges(S)+2*d] += number
        if edges(S) != 4:
            continue
        deg = sorted((adj[i] & S).bit_count() for i in chosen)
        kind = 'cycle' if deg == [2, 2, 2, 2] else 'paw'
        assert deg in ([2, 2, 2, 2], [1, 2, 2, 3])
        # z outside grid, far from S. It has its unique grid neighbour in R\S.
        # Each of the five possible neighbours has ten outside neighbours.
        details[kind+'_outside_z'] += 50
        # z must be outside R: its coefficient in 1_W+1_S-e_z is zero.
    out['four_set_minus_vertex_Q8'] = sum(details.values())
    assert out == {'negative_triple_Q8': 36, 'negative_triple_Q6': 36,
                   'four_set_minus_vertex_Q8': 2250}
    assert by_q[6] == 36 and by_q[8] == 2286 and by_q[10] == 3606
    return {'unsigned_collisions_per_grid': dict(out), 'four_set_collision_details': dict(details),
            'signed_collisions_by_Q': {q: 2*c for q, c in sorted(by_q.items())},
            'signed_Q6_subtraction': 72, 'signed_Q8_subtraction': 4572}


def twin_collision_audit():
    prism = tuple(sum(1 << j for j in range(6) if i != j and
                      (i//3 == j//3 or i % 3 == j % 3)) for i in range(6))
    triangles, paths = [], []
    for T in combinations(range(6), 3):
        mask = sum(1 << i for i in T)
        e = sum((prism[i] & mask).bit_count() for i in T)//2
        if e == 3:
            triangles.append(T)
        elif e == 2:
            paths.append(T)
    assert len(triangles) == 2 and len(paths) == 12
    positive_orientation = []
    for offset in (0, 6):
        for T in triangles:
            for Y in paths:
                v = [0]*12
                for i in T:
                    v[i+offset] = 1
                for i in Y:
                    v[i+6-offset] = -1
                positive_orientation.append(tuple(v))
    # Formal quotient by the relation 1_S - 1_R = 0, for two twin prisms.
    relation = [1]*6+[-1]*6
    def quotient(v):
        return tuple(x-v[0]*w for x, w in zip(v, relation))
    assert len(set(map(quotient, positive_orientation))) == 48
    both_signs = positive_orientation+[tuple(-x for x in v) for v in positive_orientation]
    assert len(set(both_signs)) == 96
    histogram = Counter(Counter(map(quotient, both_signs)).values())
    assert histogram == {2: 48}
    return {'paths_in_prism': 12, 'unordered_partitions_into_two_paths': 6,
            'signed_representatives_for_one_twin_pair': 96,
            'distinct_images_modulo_twin_relation': 48,
            'loss_per_unordered_twin_pair': 48,
            'warning': 'The signed triangle-minus-path family is NOT injective in the presence of twin prisms.'}


def main():
    census = census_six()
    print('Census:', census['graph_types'], 'types;', census['equations'], 'equations; rank', census['rank'], flush=True)
    print('Edge counts:', census['edge_totals'], flush=True)
    grid = grid_audit()
    print('Grid collisions:', grid, flush=True)
    twin = twin_collision_audit()
    print('Twin collision audit:', twin, flush=True)
    report = {'census': census, 'grid': grid, 'twins': twin,
              'scope': 'Exact identities and finite grid audit; injectivity arguments are in the accompanying note.'}
    (ROOT/'data/codex_six_vertex_grid_audit.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
