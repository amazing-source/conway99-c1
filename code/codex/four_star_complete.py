"""Complete a rank30 four-star block all the way to a Conway adjacency99.

Enumerate every valid outside column, assemble its forced T Gram edges,
enforce the residual U rank, then check the full SRG identity exactly.
No successful stage is mistaken for a full graph. Incomplete enumeration
cannot yield a nonexistence conclusion.

Global sufficiency: for the complete84 root-pair labels, T+U=7 Pi,
where Pi projects onto ker B and has rank70. T has trace210. Therefore
T,U PSD and rankT<=30 imply that T has exactly30 eigenvalues all equal7;
U then has rank40. These identities recover the SRG polynomial for the
99-vertex bordered adjacency. The code additionally checks that integer
polynomial directly before writing a constructed graph.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_completion_columns import prepare, inverse_on_range, enumerate_column
from hmatch_cycle_reflections import B, LABELS
from schur_domain_join import join_domains, residual_rank_check

OUTSIDE = [p for p in combinations(range(4, 14), 2) if p[1] != (p[0] ^ 1)]


def sr_graph(gamma, labels, k):
    n = 1+k+len(labels)
    adjacency = np.zeros((n, n), dtype=np.int64)
    adjacency[0, 1:k+1] = adjacency[1:k+1, 0] = 1
    for r in range(k):
        adjacency[1+r, 1+(r ^ 1)] = 1
    for j, label in enumerate(labels):
        for r in label:
            adjacency[1+r, 1+k+j] = adjacency[1+k+j, 1+r] = 1
    adjacency[1+k:, 1+k:] = gamma
    return adjacency


def is_srg(adjacency, k, lam=1, mu=2):
    n = len(adjacency)
    return (not np.any(np.diag(adjacency)) and np.array_equal(adjacency, adjacency.T)
            and not np.any((adjacency != 0) & (adjacency != 1))
            and np.all(adjacency.sum(axis=1) == k)
            and np.array_equal(adjacency@adjacency, (k-mu)*np.eye(n, dtype=np.int64)+(lam-mu)*adjacency+mu))


def run(source, output, seconds=60, per_column=5):
    started = time.monotonic()
    gamma, t8, u15, kt, ku = prepare(json.loads(Path(source).read_text(encoding='utf-8')))
    assert kt.shape[1] == 14, 'This mode requires local T rank30.'
    ti, ui = inverse_on_range(t8), inverse_on_range(u15)
    residual_rank = 40-len(ui[0])
    assert residual_rank >= 0
    report = dict(source_file=str(source), status='INCOMPLETE',
                  T_local_rank=len(ti[0]), U_local_rank=len(ui[0]), U_residual_rank=residual_rank,
                  columns=[], scope='Complete finite search for this fixed labelled seed when exhausted; no coverage of all C1 seeds is asserted.')
    domains = []
    for label in OUTSIDE:
        remaining = started+seconds-time.monotonic()
        if remaining <= 0:
            break
        column = enumerate_column(label, gamma, kt, ku, ti, ui, min(per_column, remaining))
        report['columns'].append(column)
        print(json.dumps(dict(stage='COLUMNS', label=label, status=column['status'], complete=column['complete'], count=len(column['domains']))), flush=True)
        if column['complete'] and not column['domains']:
            report.update(status='NO_COMPLETION', empty_label=label, reason='An outside column domain is empty.')
            break
        if not column['complete']:
            report['reason'] = 'A column domain was not exhaustively enumerated.'
            break
        domains.append(column['domains'])
    if len(domains) == 40:
        def offsets(i, j):
            p, q = OUTSIDE[i], OUTSIDE[j]
            intersection = len(set(p)&set(q))
            mates = sum((r ^ 1) in q for r in p)
            return 3*intersection+mates-2, 4*intersection-mates+2

        def block(selected, pair):
            order = sorted(selected)
            matrix = np.zeros((44+len(order), 44+len(order)), dtype=np.int64)
            matrix[:44, :44] = gamma
            for a, i in enumerate(order, 44):
                neighbours = domains[i][selected[i]]['neighbours']
                matrix[a, neighbours] = matrix[neighbours, a] = 1
            for a, b in combinations(range(len(order)), 2):
                i, j = order[a], order[b]
                matrix[44+a, 44+b] = matrix[44+b, 44+a] = pair(i, selected[i], j, selected[j])[0]
            return matrix, list(LABELS)+[OUTSIDE[i] for i in order]

        def partial(selected, pair):
            matrix, labels = block(selected, pair)
            degree = matrix.sum(axis=1)
            if np.any(degree > 12) or np.any(degree+(40-len(selected)) < 12):
                return False
            incidence = np.array([[int(r in p) for p in labels] for r in range(14)], dtype=np.int64)
            total = matrix@matrix+matrix+incidence.T@incidence
            np.fill_diagonal(total, 0)
            return not np.any(total > 2)

        def leaf(selected, pair):
            matrix, labels = block(selected, pair)
            return is_srg(sr_graph(matrix, labels, 14), 14)

        joined = join_domains(domains, ti, ui, offsets, residual_rank,
                              seconds=max(.01, started+seconds-time.monotonic()),
                              partial_check=partial, leaf_check=leaf)
        report['assembly'] = joined
        if joined['solutions']:
            solution = joined['solutions'][0]
            assembled = np.zeros((84, 84), dtype=np.int64)
            assembled[:44, :44] = gamma
            for i, value in enumerate(solution['assignment']):
                neighbours = domains[i][value]['neighbours']
                assembled[44+i, neighbours] = assembled[neighbours, 44+i] = 1
            for i, j in solution['edges']:
                assembled[44+i, 44+j] = assembled[44+j, 44+i] = 1
            adjacency = sr_graph(assembled, list(LABELS)+OUTSIDE, 14)
            assert is_srg(adjacency, 14)
            graph_file = Path(output).with_name(Path(output).stem+'_GRAPH99.json')
            graph_file.write_text(json.dumps(dict(parameters=[99, 14, 1, 2], adjacency=adjacency.tolist(),
                                                  source_file=str(source), exact_SRG_identity=True), indent=2)+'\n', encoding='utf-8')
            report.update(status='SRG99_CONSTRUCTED', graph_file=str(graph_file))
        else:
            report['status'] = 'NO_COMPLETION' if joined['exhaustive'] else 'INCOMPLETE'
    report['seconds'] = time.monotonic()-started
    Path(output).write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('columns', 'assembly')}), flush=True)
    return report


def construction_control():
    """Positive end-to-end assembly on the9-vertex rook SRG, not a peer audit.

    Its4-vertex second neighbourhood has T4=3vv^t, U=0. One seed vertex
    saturates rankT. Each of the other3 domains below has one prescribed
    column, with one extra wrong-sign option that the join must eliminate.
    """
    labels = [(0, 2), (0, 3), (1, 2), (1, 3)]
    vector = np.array([1, -1, -1, 1], dtype=np.int64)
    gamma = np.array([[int(i != j and len(set(p)&set(q)) == 1) for j, q in enumerate(labels)]
                      for i, p in enumerate(labels)], dtype=np.int64)
    gram = 3*np.outer(vector, vector)
    k4 = 4*np.eye(4, dtype=np.int64)-4*gamma-gram
    lu = 2*np.eye(4, dtype=np.int64)+gamma
    domains = [[dict(T_coordinates=[int(gram[0, j])], U_coordinates=[], U_residual_numerator='0',
                     U_residual_denominator='1', neighbours=[0] if gamma[0, j] else [])] for j in range(1, 4)]
    domains[0].insert(0, dict(domains[0][0], T_coordinates=[3]))
    inverse_t = ([0], np.array([[1]], dtype=object), 3)
    inverse_u = ([], np.zeros((0, 0), dtype=object), 1)

    def leaf(selected, pair):
        matrix = np.zeros((4, 4), dtype=np.int64)
        for i, value in selected.items():
            matrix[0, i+1] = matrix[i+1, 0] = bool(domains[i][value]['neighbours'])
        for i, j in combinations(range(3), 2):
            matrix[i+1, j+1] = matrix[j+1, i+1] = pair(i, selected[i], j, selected[j])[0]
        return is_srg(sr_graph(matrix, labels, 4), 4)

    joined = join_domains(domains, inverse_t, inverse_u,
                          lambda i, j: (int(k4[i+1, j+1]), int(lu[i+1, j+1])), 0,
                          t_scale=4, u_scale=1, max_solutions=0, leaf_check=leaf)
    assert joined['exhaustive'] and len(joined['solutions']) == 1
    assert joined['solutions'][0]['assignment'] == [1, 0, 0]
    # The sign obstruction missed by checking only2x2 rank1 minors.
    assert not residual_rank_check([[1, 1, 1], [1, 1, -1], [1, -1, 1]], 1, final=True)
    assert residual_rank_check([[1, -2, 3], [-2, 4, -6], [3, -6, 9]], 1, final=True)
    return dict(status='POSITIVE_CONSTRUCTION_CONTROL_PASSED', parameters=[9, 4, 1, 2],
                reconstructed_vertices=9, join=joined, exact_rank1_sign_obstruction_checked=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source')
    parser.add_argument('--output', required=True)
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--per-column', type=float, default=5)
    parser.add_argument('--construction-control', action='store_true')
    args = parser.parse_args()
    if args.construction_control:
        result = construction_control()
        Path(args.output).write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(result), flush=True)
    else:
        if not args.source:
            parser.error('--source is required without --construction-control')
        run(args.source, args.output, args.seconds, args.per_column)
