"""Exact necessary cuts on the graph of triangular prisms in Conway C1.

Vertices are the 231 triangles; an edge joins disjoint triangles with
three cross edges.  A partial graph may contain fewer vertices/edges.
All cuts are monotone under adding vertices/edges (up to 231 vertices).
Only the Python standard library is used. No historic files are read.

Proof and scope: notes/JOURNAL_C1_NUIT_2026_10_14.md, 14 October morning.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


ORDER = 231
BETA = F(2, 13629)
EPSILON = BETA * ORDER
MEAN_BOUND = 10 - EPSILON
SQUARE_BUDGET = ORDER * 590**2


def adjacency(order, edges):
    if not 0 <= order <= ORDER:
        raise ValueError("The partial prism graph has at most 231 vertices")
    a = [[0] * order for _ in range(order)]
    for u, v in edges:
        if not (0 <= u < order and 0 <= v < order) or u == v:
            raise ValueError("Invalid simple edge")
        a[u][v] = a[v][u] = 1
    return a


def square_degree_cut(a):
    """Pad missing triangles by isolated vertices, hence their degree is 0."""
    degrees = list(map(sum, a))
    score = sum((59 * d + 2)**2 for d in degrees)
    score += (ORDER - len(a)) * 2**2
    return dict(pass_cut=score <= SQUARE_BUDGET, score=score,
                budget=SQUARE_BUDGET, degrees=degrees)


def ten_core(a):
    active = set(range(len(a)))
    degree = list(map(sum, a))
    queue = [i for i in active if degree[i] < 10]
    while queue:
        i = queue.pop()
        if i not in active:
            continue
        active.remove(i)
        for j in active:
            if a[i][j]:
                degree[j] -= 1
                if degree[j] == 9:
                    queue.append(j)
    return sorted(active)


def resolvent_cut(a):
    """Exact test of 10I-P > 0 and 1^t(10I-P)^-1 1 <= 13629/2.

    Fraction-free elimination of [[2(10I-P),2*1],[2*1^t,13629]].
    Leading pivots through P must be positive; the last can be zero.
    This is equivalent to 10I-P-BETA*J >= 0 for nonnegative symmetric P.
    The test uses only the displayed vertices, a necessary principal cut.
    """
    n = len(a)
    z = [[20 * (i == j) - 2 * a[i][j] for j in range(n)] + [2]
         for i in range(n)]
    z.append([2] * n + [13629])
    previous = 1
    for k in range(n + 1):
        pivot = z[k][k]
        if pivot < 0 or (k < n and pivot == 0):
            return dict(pass_cut=False, failed_leading_order=k + 1,
                        failed_determinant=str(pivot))
        if k == n:
            return dict(pass_cut=True, final_determinant=str(pivot))
        for i in range(k + 1, n + 1):
            for j in range(i, n + 1):
                value, remainder = divmod(
                    pivot * z[i][j] - z[i][k] * z[k][j], previous)
                assert remainder == 0
                z[i][j] = z[j][i] = value
        previous = pivot


def check_partial(order, edges):
    a = adjacency(order, edges)
    square = square_degree_cut(a)
    core = ten_core(a)
    local_max = max(square['degrees'], default=0)
    if local_max > 12:
        return dict(pass_cut=False, reason='a prism degree exceeds 12')
    if not square['pass_cut']:
        return dict(reason='quadratic degree budget', **square)
    if core:
        return dict(pass_cut=False, reason='nonempty 10-core', core=core)
    exact = resolvent_cut(a)
    return dict(reason='exact rational spectral cut', **exact)


def harmonic_tensor(x):
    d = len(x)
    norm = sum(t * t for t in x)
    h = {}
    for i, j, k in product(range(d), repeat=3):
        value = F(x[i] * x[j] * x[k]) - F(norm, d + 2) * (
            x[i] * (j == k) + x[j] * (i == k) + x[k] * (i == j))
        if value:
            h[i, j, k] = value
    for i in range(d):
        assert sum(h.get((i, j, j), 0) for j in range(d)) == 0
    return h


def derive_and_check():
    # Direct coordinate checks of the trace-free tensor formula, including d=44.
    for d in (2, 3, 44):
        x = [2, 1] + [0] * (d - 2)
        y = [1, -3] + [0] * (d - 2)
        hx, hy = harmonic_tensor(x), harmonic_tensor(y)
        inner = sum(v * hy.get(k, 0) for k, v in hx.items())
        dot = sum(a * b for a, b in zip(x, y))
        nx, ny = sum(v*v for v in x), sum(v*v for v in y)
        assert inner == dot**3 - F(3 * nx * ny, d + 2) * dot

    # M is the Gram matrix of the q_T; these are its six relation entries.
    m = [4, 0, 1, 0, -1, -2]
    prism = [0, 0, 0, 0, 0, 1]
    for i, (v, p) in enumerate(zip(m, prism)):
        assert v**3 - F(24, 23)*v == 60*(i == 0) - 6*p - F(v, 23)
    vertex_norm = 99 * (28**3 + 14*(-8)**3 + 84)
    mixed = 3*4**3 + 36*(-2)**3 + 60
    assert vertex_norm == 1471932 and mixed == -36
    assert F(mixed**2, vertex_norm) / 6 == BETA
    assert MEAN_BOUND == F(588, 59) and EPSILON == F(2, 59)

    # For fixed integer degree sum, the convex square sum is minimized by
    # the two nearest integer degrees. This even allows degree 11, which
    # can only weaken the valid upper bound.
    feasible_totals = []
    bounds = {}
    for e in range(ORDER * 6 + 1):
        low, count_high = divmod(2 * e, ORDER)
        minimum = (ORDER-count_high)*(59*low+2)**2
        minimum += count_high*(59*(low+1)+2)**2
        if minimum <= SQUARE_BUDGET:
            feasible_totals.append(e)
        if e in (1150, 1151):
            bounds[str(e)] = dict(minimum_score=minimum,
                                 budget=SQUARE_BUDGET,
                                 pass_cut=minimum <= SQUARE_BUDGET)
    assert max(feasible_totals) == 1150

    complete10 = adjacency(10, ((i,j) for i in range(10) for j in range(i)))
    complete11 = adjacency(11, ((i,j) for i in range(11) for j in range(i)))
    # K_(9,12) has empty 10-core but spectral radius sqrt(108)>10.
    bipartite = adjacency(21, ((i,j) for i in range(9) for j in range(9,21)))
    assert resolvent_cut(complete10)['pass_cut']
    assert not resolvent_cut(complete11)['pass_cut']
    assert not ten_core(bipartite)
    assert not resolvent_cut(bipartite)['pass_cut']
    # Old total-count bound passes, new quadratic budget fails.
    edges = {tuple(sorted((i, (i+j) % ORDER)))
             for i in range(ORDER) for j in range(1,6)}
    edges -= {(0,1),(2,3),(4,5),(6,7)}
    witness = adjacency(ORDER, edges)
    assert len(edges) == 1151
    assert F(2*len(edges), ORDER) <= MEAN_BOUND
    assert not square_degree_cut(witness)['pass_cut']
    assert not check_partial(ORDER, edges)['pass_cut']
    assert check_partial(10, ((i,j) for i in range(10) for j in range(i)))['pass_cut']
    assert not check_partial(21, ((i,j) for i in range(9) for j in range(9,21)))['pass_cut']
    return dict(status='exact checks pass', ambient_dimension=44,
                harmonic_cubic_gram='60I - 6P - M/23',
                necessary_psd='10I - P - M/138 - (2/13629)J',
                prism_spectral_radius='strictly less than 10',
                prism_graph_degeneracy_at_most=9,
                mean_prism_degree_at_most=str(MEAN_BOUND),
                quadratic_degree_bound='sum_T (59*p(T)+2)^2 <= 231*590^2',
                unordered_prism_bound=1150, integer_checks=bounds,
                fixtures=dict(K10='passes necessary cut; not a C1 witness',
                              K11='rejected: spectral radius 10',
                              K9_12='rejected despite empty 10-core',
                              circulant_minus_4_edges='1151 edges: old mean passes, new square cut fails'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path,
                        help='JSON with order and edges of a partial prism graph')
    parser.add_argument('--output', type=Path,
                        default=Path('data/codex_night_20261014/prism_spectral_cut.json'))
    args = parser.parse_args()
    if args.input:
        instance = json.loads(args.input.read_text(encoding='utf-8'))
        report = check_partial(instance['order'], instance['edges'])
    else:
        report = derive_and_check()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
