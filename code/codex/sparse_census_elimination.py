"""Exact sparse elimination with minimum-row and column-degree pivoting.

Only graph-count columns are pivoted; affine parameter columns are carried
along. Every operation is rational. Reverse substitution constructs an
explicit solution, which the caller verifies against the original matrix.
"""
from fractions import Fraction as F
import heapq
import time

from sympy import Matrix, Rational


def eliminate(matrix, rhs, verbose=False):
    started = time.monotonic()
    nr, nc = matrix.shape
    k = rhs.cols
    rows = [{} for _ in range(nr)]
    columns = [set() for _ in range(nc)]
    for (i, j), value in matrix.todok().items():
        rows[i][j] = F(value)
        columns[j].add(i)
    for (i, j), value in rhs.todok().items():
        if value:
            rows[i][nc+j] = -F(value)
    degrees = [sum(j < nc for j in row) for row in rows]
    heap = [(degree, i) for i, degree in enumerate(degrees) if degree]
    heapq.heapify(heap)
    equations, pivots = [], []
    while heap:
        degree, i = heapq.heappop(heap)
        if rows[i] is None or not degree or degree != degrees[i]:
            continue
        row = rows[i]
        pivot = min((j for j in row if j < nc), key=lambda j: (len(columns[j]), j))
        value = row[pivot]
        normalised = {j: x/value for j, x in row.items()}
        equations.append((pivot, normalised))
        pivots.append((i, pivot, str(value)))
        neighbours = list(columns[pivot]-{i})
        for j in row:
            if j < nc:
                columns[j].remove(i)
        rows[i] = None
        degrees[i] = 0
        for h in neighbours:
            target = rows[h]
            factor = target[pivot]
            for j, x in normalised.items():
                previous = target.get(j, F(0))
                updated = previous-factor*x
                if updated:
                    target[j] = updated
                    if j < nc and not previous:
                        columns[j].add(h)
                        degrees[h] += 1
                elif previous:
                    del target[j]
                    if j < nc:
                        columns[j].remove(h)
                        degrees[h] -= 1
            if degrees[h]:
                heapq.heappush(heap, (degrees[h], h))
        if verbose and len(pivots) % 1000 == 0:
            print('Sparse pivots', len(pivots), 'seconds', round(time.monotonic()-started, 2), flush=True)
    residual = [row for row in rows if row]
    assert not residual, ('Additional relations on old parameters', residual[:3])
    pivot_cols = {j for _, j, _ in pivots}
    free_cols = [j for j in range(nc) if j not in pivot_cols]
    width = k+len(free_cols)
    coordinates = [[F(0)]*width for _ in range(nc)]
    for i, col in enumerate(free_cols):
        coordinates[col][k+i] = F(1)
    for pivot, equation in reversed(equations):
        value = [-equation.get(nc+j, F(0)) for j in range(k)]+[F(0)]*len(free_cols)
        for j, coefficient in equation.items():
            if j >= nc or j == pivot:
                continue
            for h, x in enumerate(coordinates[j]):
                if x:
                    value[h] -= coefficient*x
        coordinates[pivot] = value
    result = Matrix([[Rational(x.numerator, x.denominator) for x in row] for row in coordinates])
    return result, free_cols, pivots
