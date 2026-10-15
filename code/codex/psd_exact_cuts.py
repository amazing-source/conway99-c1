"""Exact finite cuts for rational affine PSD models and proof formats.

Model: M(x)=offset+sum_j x_j*coefficient[j], all matrices rational.
Every rational q gives the globally valid linear inequality
  sum_j (-q^t coefficient[j] q) x_j <= q^t offset q.
This module constructs primitive integer rows and exact separating vectors.
It does not run a MILP, reconstruct its search, or prove C1 infeasible.

A Farkas certificate suffices only for linear infeasibility.  The optional
binary-tree format adds a covering 0/1 split at each node and a rational
Farkas certificate at every leaf.  The caller supplies valid model rows;
their combinatorial provenance must be retained in an actual proof bundle.
"""
from math import gcd, lcm
from pathlib import Path
import argparse
import json

import sympy as sp


def rational(value):
    value = sp.sympify(value)
    if not value.is_Rational:
        raise ValueError('Use integers or exact rational strings, not floating values.')
    return value


def symmetric_matrix(value):
    matrix = sp.Matrix(value).applyfunc(rational)
    if matrix.rows != matrix.cols or matrix != matrix.T:
        raise ValueError('Expected a symmetric rational matrix.')
    return matrix


def integer_vector(vector):
    vector = [rational(x) for x in vector]
    scale = lcm(*(int(x.q) for x in vector))
    out = [int(scale*x) for x in vector]
    common = gcd(*out)
    if not common:
        raise ValueError('A direction must be nonzero.')
    out = [x//common for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return out


def integer_row(coefficients, rhs):
    values = [rational(x) for x in coefficients]+[rational(rhs)]
    scale = lcm(*(int(x.q) for x in values))
    integers = [int(scale*x) for x in values]
    common = gcd(*integers) or 1
    integers = [x//common for x in integers]
    return dict(coefficients=integers[:-1], rhs=integers[-1],
                positive_scale=str(sp.Rational(scale, common)))


def negative_direction(matrix):
    """Exact congruence: return PSD, or an integer q with q^t M q<0.

    Zero diagonal pivots with a nonzero off-diagonal entry are handled
    directly.  Negative rational values are never truncated to integers.
    """
    original = symmetric_matrix(matrix)
    current = original.copy()
    n = current.rows
    basis = [sp.eye(n).col(i) for i in range(n)]
    positive = zero = 0

    def failure(vector):
        q = integer_vector(vector)
        value = (sp.Matrix(q).T*original*sp.Matrix(q))[0]
        assert value < 0
        return dict(psd=False, integer_witness=q, quadratic_value=str(value))

    for i in range(n):
        pivot = current[i, i]
        if pivot < 0:
            return failure(basis[i])
        if pivot == 0:
            j = next((j for j in range(i+1, n) if current[i, j]), None)
            if j is not None:
                t = -(current[j, j]+1)/(2*current[i, j])
                return failure(basis[j]+t*basis[i])
            zero += 1
            continue
        positive += 1
        for j in range(i+1, n):
            basis[j] -= current[i, j]/pivot*basis[i]
        for j in range(i+1, n):
            for k in range(j, n):
                value = current[j, k]-current[j, i]*current[i, k]/pivot
                current[j, k] = current[k, j] = value
    return dict(psd=True, positive_pivots=positive, nullity=zero)


def psd_cut(offset, coefficients, vector):
    """Produce an integer <= row from any exact nonzero direction.

    A rounded numerical direction is fine when supplied as integers.  It
    need not be an eigenvector.  This guarantees validity, not separation.
    """
    offset = symmetric_matrix(offset)
    coefficients = [symmetric_matrix(c) for c in coefficients]
    q = sp.Matrix(integer_vector(vector))
    if q.rows != offset.rows or any(c.shape != offset.shape for c in coefficients):
        raise ValueError('Inconsistent affine-model dimensions.')
    row = integer_row([-(q.T*c*q)[0] for c in coefficients], (q.T*offset*q)[0])
    row.update(kind='rational_PSD_direction', integer_witness=list(map(int, q)))
    return row


def adjacency_psd_cut(offset, edge_orbits, vector, adjacency_sign):
    """A full-space PSD row directly in binary edge-orbit variables.

    M=offset+adjacency_sign*Gamma, with sign=-1 for T and +1 for U.
    Each orbit is a list of unordered pairs i<j sharing one variable.
    Missing pairs are taken as fixed zero.  Square assignments and other
    fixed nonzero edges can remain variables with exact equality rows.
    No candidate graph or affine coefficient matrices need be constructed.
    """
    if adjacency_sign not in (-1, 1):
        raise ValueError('Adjacency sign must be -1 or +1.')
    offset = symmetric_matrix(offset)
    q = integer_vector(vector)
    if len(q) != offset.rows:
        raise ValueError('Wrong vector dimension.')
    coefficients, seen = [], set()
    for orbit in edge_orbits:
        value = 0
        for i, j in orbit:
            i, j = sorted((i, j))
            if not 0 <= i < j < len(q) or (i, j) in seen:
                raise ValueError('Invalid or repeated pair in the orbit partition.')
            seen.add((i, j))
            value += 2*q[i]*q[j]
        coefficients.append(-adjacency_sign*value)
    column = sp.Matrix(q)
    row = integer_row(coefficients, (column.T*offset*column)[0])
    row.update(kind='rational_PSD_edge_orbit_direction',
               integer_witness=q, adjacency_sign=adjacency_sign)
    return row


def separate(offset, coefficients, assignment):
    """An exact separation oracle; no graph sample or solver is loaded."""
    offset = symmetric_matrix(offset)
    coefficients = [symmetric_matrix(c) for c in coefficients]
    assignment = [rational(x) for x in assignment]
    if len(coefficients) != len(assignment):
        raise ValueError('Wrong assignment length.')
    current = offset.copy()
    for x, c in zip(assignment, coefficients):
        current += x*c
    result = negative_direction(current)
    if result['psd']:
        return result
    row = psd_cut(offset, coefficients, result['integer_witness'])
    slack = row['rhs']-sum(a*x for a, x in zip(row['coefficients'], assignment))
    assert slack < 0
    result.update(cut=row, exact_slack=str(slack))
    return result


def farkas_certificate(rows, multipliers):
    """Certify sum lambda_i*(a_i*x<=b_i) yields 0<0.

    Multipliers may be a full list or a sparse {row_index: rational} map.
    Every supplied row must already be a valid model inequality.  This
    routine does not infer the provenance of arbitrary linear constraints.
    """
    if not rows:
        raise ValueError('No inequalities supplied.')
    n = len(rows[0]['coefficients'])
    if isinstance(multipliers, dict):
        values = [sp.Rational(0)]*len(rows)
        for key, value in multipliers.items():
            key = int(key)
            if not 0 <= key < len(rows):
                raise ValueError('Unknown row index in Farkas multiplier.')
            values[key] += rational(value)
    else:
        values = [rational(x) for x in multipliers]
    if len(values) != len(rows) or any(x < 0 for x in values):
        raise ValueError('Farkas multipliers must be nonnegative and match the rows.')
    combined = [sp.Rational(0)]*n
    rhs = sp.Rational(0)
    for row, weight in zip(rows, values):
        if len(row['coefficients']) != n:
            raise ValueError('Inconsistent row dimension.')
        for j, a in enumerate(row['coefficients']):
            combined[j] += weight*rational(a)
        rhs += weight*rational(row['rhs'])
    if any(combined) or rhs >= 0:
        raise ValueError('Not a contradiction: require zero left side and negative right side.')
    return dict(status='EXACT_LINEAR_CONTRADICTION', rhs=str(rhs),
                nonzero_multipliers=sum(x != 0 for x in values))


def binary_tree_certificate(rows, n_variables, tree):
    """Check a finite covering branch tree with exact Farkas leaves.

    Row order at a leaf is: supplied global rows; x_j<=1 for increasing j;
    -x_j<=0 for increasing j; then branch rows along that root-to-leaf path.
    Node schema: {'split':j,'zero':node,'one':node}.
    Leaf schema: {'multipliers': sparse_map_or_full_list}.
    Zero appends x_j<=0; one appends -x_j<=-1.  All variables are binary.
    This consumes a proof, and cannot extract one from a MILP status flag.
    """
    if any(len(row['coefficients']) != n_variables for row in rows):
        raise ValueError('Wrong global row dimension.')
    bounded_rows = list(rows)
    for sign, rhs in ((1, 1), (-1, 0)):
        for j in range(n_variables):
            coefficients = [0]*n_variables
            coefficients[j] = sign
            bounded_rows.append(dict(coefficients=coefficients, rhs=rhs))

    def visit(node, current, fixed):
        if 'multipliers' in node:
            if 'split' in node:
                raise ValueError('A node cannot be both a leaf and a split.')
            farkas_certificate(current, node['multipliers'])
            return 1, len(fixed)
        j = node.get('split')
        if not isinstance(j, int) or not 0 <= j < n_variables or j in fixed:
            raise ValueError('Invalid or repeated binary split.')
        leaves, depth = 0, 0
        for label, sign, rhs in (('zero', 1, 0), ('one', -1, -1)):
            if label not in node:
                raise ValueError('Both children are required to cover a binary split.')
            coefficients = [0]*n_variables
            coefficients[j] = sign
            child_rows = current+[dict(coefficients=coefficients, rhs=rhs)]
            count, child_depth = visit(node[label], child_rows, fixed | {j})
            leaves += count
            depth = max(depth, child_depth)
        return leaves, depth

    leaves, depth = visit(tree, bounded_rows, set())
    return dict(status='EXACT_BINARY_CONTRADICTION', leaves=leaves, maximum_depth=depth)


def report():
    checks = []
    for matrix in (sp.Matrix([[0, 1], [1, 0]]),
                   sp.Matrix([[-sp.Rational(1, 1000)]]),
                   sp.Matrix([[1, 2], [2, 1]])):
        result = negative_direction(matrix)
        assert not result['psd']
        checks.append(result)
    assert negative_direction(sp.Matrix([[1, 1], [1, 1]])) == dict(
        psd=True, positive_pivots=1, nullity=1)
    # A dimension-ten congruence fixture, not an SRG boundary.
    change = sp.eye(10)
    for i in range(9):
        change[i, i+1] = i+1
    fixture = change.T*sp.diag(1, 1, 1, 1, 1, 1, 1, 1, 0, -sp.Rational(1, 7))*change
    assert not negative_direction(fixture)['psd']
    offset = sp.diag(1, sp.Rational(1, 4))
    coefficient = sp.Matrix([[0, 1], [1, 0]])
    cut = psd_cut(offset, [coefficient], [1, -2])
    assert cut['coefficients'] == [2] and cut['rhs'] == 1
    orbit_cut = adjacency_psd_cut(offset, [[(0, 1)]], [1, -2], 1)
    assert orbit_cut['coefficients'] == cut['coefficients'] and orbit_cut['rhs'] == cut['rhs']
    separation = separate(offset, [coefficient], [1])
    assert not separation['psd']
    assert separate(offset, [coefficient], [0])['psd']
    linear_rows = [dict(coefficients=[1], rhs=0), dict(coefficients=[-1], rhs=-1)]
    linear_certificate = farkas_certificate(linear_rows, [1, 1])
    # 2x=1 has a feasible real point x=1/2, but no binary point.
    binary_rows = [dict(coefficients=[2], rhs=1), dict(coefficients=[-2], rhs=-1)]
    assert all(sum(sp.Rational(1, 2)*a for a in row['coefficients']) <= row['rhs']
               for row in binary_rows)
    tree = {'split': 0,
            'zero': {'multipliers': {'1': 1, '4': 2}},
            'one': {'multipliers': {'0': 1, '4': 2}}}
    binary_certificate = binary_tree_certificate(binary_rows, 1, tree)
    rejected = 0
    for invalid in ([1, -1], [1, 0]):
        try:
            farkas_certificate(linear_rows, invalid)
        except ValueError:
            rejected += 1
    try:
        binary_tree_certificate(binary_rows, 1, {'split': 0, 'zero': tree['zero']})
    except ValueError:
        rejected += 1
    try:
        psd_cut([[0.5]], [[[1]]], [1])
    except ValueError:
        rejected += 1
    assert rejected == 4
    return dict(status='EXACT_PSD_CUT_AND_FINITE_PROOF_PRIMITIVES',
                rational_negative_examples=checks, example_cut=cut,
                exact_separation=separation, linear_certificate=linear_certificate,
                binary_example=dict(rows=binary_rows, tree=tree,
                                    fractional_witness=['1/2'], certificate=binary_certificate),
                rejected_invalid_inputs=rejected,
                scope='Own algebraic fixtures only. No producer MILP, candidate graph, or C1 exclusion tested.',
                limitation='No infeasibility proof generator or tree-size bound. A floating MILP status is not an exact certificate.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report()
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, separators=(',', ':'))+'\n', encoding='utf-8')
    print(json.dumps({key: result[key] for key in (
        'status', 'linear_certificate', 'binary_example', 'rejected_invalid_inputs')}))
