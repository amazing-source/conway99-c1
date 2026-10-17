"""Search a prescribed flat kernel relation with nonzero overlap difference.

This constructs new local candidates; no producer graph is read. Exact
binary/C1/C1-prime/C2 constraints and exact integer PSD cuts are used.
An unfinished search is not an exclusion. Floating eigenvalues only suggest
integer separating vectors; each cut is checked with integer arithmetic.
"""
import argparse
from itertools import combinations, permutations
import json
from pathlib import Path
import sys
import time

import numpy as np
from ortools.sat.python import cp_model


LABELS = list(combinations(range(14), 2))
LABELS = [p for p in LABELS if p[0] < 4 and p[1] != (p[0] ^ 1)]
INDEX = {p: i for i, p in enumerate(LABELS)}
EDGES = list(combinations(range(44), 2))


def prism_options(vertices):
    """All labelled triangular prisms compatible with the root incidences.

    Under the C2 capacities, any induced graph on six vertices of minimum
    degree three is a triangular prism. In Gamma*q=3*q each of the six
    positive vertices has at least three positive neighbours. Hence both
    signs induce prisms and there are no edges between the two signs.
    """
    local_pairs = list(combinations(range(6), 2))
    records = []
    for other in combinations(range(1, 6), 2):
        triangle = (0,)+other
        rest = tuple(i for i in range(6) if i not in triangle)
        for matching in permutations(rest):
            g = np.zeros((6, 6), dtype=np.int64)
            for i, j in list(combinations(triangle, 2))+list(combinations(rest, 2))+list(zip(triangle, matching)):
                g[i, j] = g[j, i] = 1
            square = g@g
            if all(square[i, j] <= 2-g[i, j]-len(set(LABELS[vertices[i]]) & set(LABELS[vertices[j]]))
                   for i, j in local_pairs):
                records.append([int(g[i, j]) for i, j in local_pairs])
    return records


def vertical_edges_closed(vertices, allowed):
    pairs = list(combinations(vertices, 2))
    for row in allowed:
        adjacency = {i: set() for i in vertices}
        for value, (i, j) in zip(row, pairs):
            if value:
                adjacency[i].add(j)
                adjacency[j].add(i)
        for i, j in pairs:
            if j in adjacency[i] and not (adjacency[i] & adjacency[j]):
                if not (set(LABELS[i]) & set(LABELS[j])):
                    return False
    return True


def run(seconds=40, rounds=30, pattern='overlapping_doubles', historical_search=False):
    started = time.monotonic()
    positive = [(0, 2), (3, 4), (0, 6), (1, 8), (2, 10), (3, 12)]
    negative = [(0, 3), (2, 4), (0, 8), (1, 6), (2, 12), (3, 10)]
    if pattern == 'prism_compatible':
        positive = [(0, 2), (2, 4), (1, 6), (1, 8), (3, 10), (3, 12)]
        negative = [(0, 3), (3, 4), (1, 10), (1, 12), (2, 6), (2, 8)]
    q = np.zeros(44, dtype=np.int64)
    for p in positive:
        q[INDEX[p]] = 1
    for p in negative:
        q[INDEX[p]] = -1
    incidence = np.array([[int(c in p) for p in LABELS] for c in range(14)])
    assert not np.any(incidence @ q)
    assert sum(q[INDEX[p]] * v for p, v in
               [((0, 2), 1), ((0, 3), -1), ((1, 2), -1), ((1, 3), 1)]) == 2
    if pattern == 'prism_compatible' and not historical_search:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from four_star_flat_c4do_obstruction import certificate
        proof = certificate()
        return dict(status='EXCLUDED_ANALYTICALLY_BY_FLAT_C4DO_THEOREM',
                    labels=LABELS, q=q.tolist(), certificate=proof,
                    seconds=time.monotonic()-started,
                    scope='The later analytic proof supersedes the historical UNKNOWN searches on this support.')
    K8 = np.array([[3*len(set(p) & set(r)) +
                    sum((c ^ 1) in r for c in p)-2
                    for r in LABELS] for p in LABELS], dtype=np.int64)
    T0 = 24*np.eye(44, dtype=np.int64)-K8
    U0 = np.array([[60*int(i == j)-4*len(set(p) & set(r)) +
                    sum((c ^ 1) in r for c in p)-2
                    for j, r in enumerate(LABELS)] for i, p in enumerate(LABELS)],
                  dtype=np.int64)
    assert not np.any(K8 @ q)
    model = cp_model.CpModel()
    edges = {e: model.NewBoolVar('e_%d_%d' % e) for e in EDGES}
    def var(i, j):
        return 0 if i == j else edges[min(i, j), max(i, j)]
    for i, p in enumerate(LABELS):
        for c in range(14):
            count = sum(var(i, j) for j, r in enumerate(LABELS) if c in r)
            limit = 2-int(c in p)-int((c ^ 1) in p)
            model.Add(count == limit) if c < 4 else model.Add(count <= limit)
        model.Add(sum(int(q[j])*var(i, j) for j in range(44) if q[j]) == 3*int(q[i]))
    overlap = [INDEX[p] for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
    model.Add(sum(var(i, j) for i, j in combinations(overlap, 2)) <= 3)
    c2_pairs, cuts, steps = set(), [], []
    signs = [[int(i) for i in np.flatnonzero(q == value)] for value in (1, -1)]
    options = [prism_options(vertices) for vertices in signs]
    if not all(options):
        return dict(status='EXCLUDED_BY_SIX_VERTEX_PRISM_LEMMA', labels=LABELS,
                    q=q.tolist(), allowed_prisms=list(map(len, options)),
                    seconds=time.monotonic()-started)
    for vertices, allowed in zip(signs, options):
        model.AddAllowedAssignments([var(i, j) for i, j in combinations(vertices, 2)], allowed)
    for i in signs[0]:
        for j in signs[1]:
            model.Add(var(i, j) == 0)
    # In these patterns every vertical edge is already closed by a root
    # neighbour. A vertex outside both prisms can meet each in at most one.
    for vertices, allowed in zip(signs, options):
        if vertical_edges_closed(vertices, allowed):
            for i in np.flatnonzero(q == 0):
                model.Add(sum(var(int(i), j) for j in vertices) <= 1)
    def add_c2(i, j):
        products = []
        for k in range(44):
            if k in (i, j):
                continue
            both = model.NewBoolVar('c_%d_%d_%d' % (i, j, k))
            model.AddMultiplicationEquality(both, [var(i, k), var(j, k)])
            products.append(both)
        model.Add(sum(products)+var(i, j) <=
                  2-len(set(LABELS[i]) & set(LABELS[j])))
        c2_pairs.add((i, j))
    for i, j in EDGES:
        if q[i] or q[j]:
            add_c2(i, j)
    last = None
    for iteration in range(rounds):
        remaining = seconds-(time.monotonic()-started)
        if remaining <= 0:
            break
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = remaining
        status = solver.Solve(model)
        step = dict(iteration=iteration, status=solver.StatusName(status),
                    solve_seconds=solver.WallTime())
        steps.append(step)
        if status == cp_model.INFEASIBLE:
            return dict(status='PRESCRIBED_RELATION_UNSAT', labels=LABELS,
                        q=q.tolist(), steps=steps, psd_cuts=cuts,
                        C2_pairs_added=len(c2_pairs), seconds=time.monotonic()-started,
                        scope='Only this prescribed twelve-entry relation and its relabellings are excluded by this finite model. No general C4DO or N9-NG proof.')
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break
        G = np.zeros((44, 44), dtype=np.int64)
        for i, j in EDGES:
            G[i, j] = G[j, i] = solver.Value(edges[i, j])
        assert np.array_equal(G @ q, 3*q)
        common = G @ G
        bad = [(i, j) for i, j in EDGES
               if common[i, j] > 2-G[i, j]-len(set(LABELS[i]) & set(LABELS[j]))]
        step['C2_violations'] = len(bad)
        last = dict(edges=[[i, j] for i, j in EDGES if G[i, j]], C2_violations=len(bad))
        if bad:
            for i, j in bad:
                assert (i, j) not in c2_pairs
                add_c2(i, j)
        added = 0
        for name, base, slope in [('T8', T0, -8), ('U15', U0, 15)]:
            matrix = base+slope*G
            values, vectors = np.linalg.eigh(matrix.astype(float))
            step[name+'_minimum_approximate'] = float(values[0])
            for j, value in enumerate(values):
                if value >= -1e-7:
                    break
                for scale in (1, 2, 4, 8, 16, 32, 64, 128, 512):
                    z = np.rint(scale*vectors[:, j]/max(abs(vectors[:, j]))).astype(np.int64)
                    energy = int(z @ matrix @ z)
                    if energy >= 0:
                        continue
                    coefficient = {e:2*slope*int(z[e[0]]*z[e[1]]) for e in EDGES}
                    constant = int(z @ base @ z)
                    model.Add(sum(c*edges[e] for e, c in coefficient.items() if c)+constant >= 0)
                    cuts.append(dict(matrix=name, vector=z.tolist(), rejected_energy=energy,
                                     constant=constant, iteration=iteration))
                    added += 1
                    break
        step['PSD_cuts_added'] = added
        if not added and not bad:
            return dict(status='NUMERICAL_PSD_CANDIDATE_NEEDS_EXACT_CERTIFICATE',
                        labels=LABELS, q=q.tolist(), candidate=last, steps=steps,
                        psd_cuts=cuts, seconds=time.monotonic()-started)
    return dict(status='UNRESOLVED', labels=LABELS, q=q.tolist(), last_candidate=last,
                steps=steps, psd_cuts=cuts, C2_pairs_added=len(c2_pairs),
                seconds=time.monotonic()-started,
                scope='Time/iteration limit; no exclusion and no PSD counterexample.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seconds', type=float, default=40)
    p.add_argument('--rounds', type=int, default=30)
    p.add_argument('--pattern', choices=('overlapping_doubles', 'prism_compatible'),
                   default='overlapping_doubles')
    p.add_argument('--historical-search', action='store_true',
                   help='Reproduce obsolete solver exploration despite the later analytic exclusion.')
    p.add_argument('--output', required=True)
    args = p.parse_args()
    report = run(args.seconds, args.rounds, args.pattern, args.historical_search)
    report['pattern'] = args.pattern
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items()
                      if k in ('status', 'steps', 'seconds', 'C2_pairs_added')}, indent=2))
