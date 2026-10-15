"""Exact weighted-network reduction of ODD9, with no symmetry assumption.

The producer is responsible for admissibility and full T/U positivity.
This computes a new nine-dimensional Schur object, not an audit of a seed.
The default report uses only our algebraic fixtures; it does not read seeds.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_c55_general_overlap import TWO_LABELS, two_star_catalogue
from four_star_profile_join import LABELS
from three_star_column_domains import k8


def line_network(gamma):
    """Return 8T_X = L8-u*u^t, and the components and a grounded L8."""
    gamma = sp.Matrix(gamma)
    if gamma.shape != (24, 24) or gamma != gamma.T or any(gamma[i, i] for i in range(24)):
        raise ValueError('Expected a symmetric loopless24-label two-star matrix.')
    if any(value not in (0, 1) for value in gamma):
        raise ValueError('Expected binary adjacencies.')
    for i in range(24):
        if any(sum(gamma[i, j] for j in range(start, start+12)) != 1 for start in (0, 12)):
            raise ValueError('Each two-star vertex needs one neighbour in each star.')
    index = {p: i for i, p in enumerate(TWO_LABELS)}
    flip = sp.zeros(24)
    mate = sp.zeros(24)
    for i, (a, y) in enumerate(TWO_LABELS):
        flip[i, index[a ^ 1, y]] = 1
        mate[i, index[a, y ^ 1]] = 1
    u = sp.Matrix([1]*12+[-1]*12)
    laplacian = 8*(2*sp.eye(24)-gamma)+3*(sp.eye(24)-flip)+(sp.eye(24)-mate)+(sp.eye(24)-flip*mate)
    direct = sp.Matrix(24, 24, lambda i, j: 24*int(i == j)-8*gamma[i, j]-k8(TWO_LABELS[i], TWO_LABELS[j]))
    assert direct == laplacian-u*u.T
    assert laplacian*u == 24*u and laplacian*sp.ones(24, 1) == sp.zeros(24, 1)
    unseen = set(range(24))
    components = []
    while unseen:
        root = min(unseen)
        component, stack = {root}, [root]
        unseen.remove(root)
        while stack:
            i = stack.pop()
            neighbours = {j for j in unseen if laplacian[i, j] < 0}
            unseen.difference_update(neighbours)
            component.update(neighbours)
            stack.extend(neighbours)
        components.append(sorted(component))
    assert all(sum(u[i] for i in component) == 0 for component in components)
    roots = [component[0] for component in components]
    retained = [i for i in range(24) if i not in roots]
    return dict(L8=laplacian, M8=direct, u=u, components=components,
                grounds=roots, retained=retained, grounded=laplacian.extract(retained, retained))


def grounded_schur(network, sources, diagonal):
    """Sources are q=Gamma_X,F*P; actual Gram cross block is -8q."""
    q, d8 = sp.Matrix(sources), sp.Matrix(diagonal)
    if q.shape != (24, 9) or d8.shape != (9, 9) or d8 != d8.T:
        raise ValueError('Expected sources24x9 and a symmetric9x9 diagonal block.')
    if network['u'].T*q != sp.zeros(1, 9):
        raise ValueError('Sources must be orthogonal to the forced star difference.')
    violations = []
    for component in network['components']:
        sums = [sum(q[i, j] for i in component) for j in range(9)]
        if any(sums):
            violations.append(dict(component=component, source_sums=list(map(str, sums))))
    if violations:
        return dict(status='COMPONENT_SOURCE_IMBALANCE_T_NOT_PSD', violations=violations,
                    proof='A known kernel indicator has nonzero pairing with an odd vector. Its2x2 Gram determinant is negative.')
    keep = network['retained']
    ground = network['grounded']
    reduced = q.extract(keep, range(9))
    response = ground.inv(method='DM')*reduced
    schur = d8-64*reduced.T*response
    det = schur.det(method='domain-ge')
    tree_product = ground.det(method='domain-ge')
    integer_det = sp.cancel(tree_product*det)
    assert integer_det.q == 1 and tree_product > 0
    rank = 9 if det else schur.rank()
    result = dict(status='EXACT_ODD9_SCHUR_REDUCTION', components=len(network['components']),
                  grounded_dimension=ground.rows, tree_product=str(tree_product),
                  integer_bordered_dimension=ground.rows+9, integer_bordered_determinant=str(integer_det),
                  schur=[[str(x) for x in schur.row(i)] for i in range(9)],
                  schur_determinant=str(det), odd_rank_gain=rank,
                  ODD9_for_this_input=rank == 9,
                  positivity_scope='Full T/U positivity is a producer hypothesis, not certified by this routine. Under T PSD, the Schur matrix is PSD and ODD9 is equivalent to strictly positive bordered determinant.')
    if rank < 9:
        t = schur.nullspace()[0]
        potential = sp.zeros(24, 1)
        for i, value in zip(keep, 8*response*t):
            potential[i] = value
        assert network['M8']*potential == 8*q*t
        result['extra_relation_in_compressed_Gram'] = dict(
            old_coefficients=list(map(str, potential)), odd_difference_coordinates=list(map(str, t)),
            scope='It lies in the full T kernel if the supplied full T is PSD; otherwise only compressed-kernel membership follows.')
    return result


def reduce_border(gamma, labels=LABELS):
    """Produce the new Schur matrix from a four-star adjacency array."""
    labels = tuple(tuple(sorted(p)) for p in labels)
    if len(labels) != 44 or set(labels) != set(LABELS):
        raise ValueError('Expected the44 labels meeting0,1,2,3.')
    gamma = sp.Matrix(gamma)
    index = {p: i for i, p in enumerate(labels)}
    old = [index[p] for p in TWO_LABELS]
    network = line_network(gamma.extract(old, old))
    f = sp.zeros(44, 10)
    for j, y in enumerate(range(4, 14)):
        f[index[2, y], j], f[index[3, y], j] = 1, -1
    p = sp.zeros(10, 9)
    for j in range(9):
        p[j, j], p[9, j] = 1, -1
    odd = f*p
    correction = sp.Matrix(44, 44, lambda i, j: k8(labels[i], labels[j]))
    assert correction*odd == sp.zeros(44, 9)
    sources = gamma.extract(old, range(44))*odd
    diagonal = 8*odd.T*(3*sp.eye(44)-gamma)*odd
    return grounded_schur(network, sources, diagonal)


def fixture_line(c):
    """Algebraic two-star fixtures with c components, not asserted C2 graphs."""
    groups = [list(range(7-c))]+[[i] for i in range(7-c, 6)]
    sigma = list(range(12))
    for group in groups:
        for i, pair in enumerate(group):
            for bit in (0, 1):
                sigma[2*pair+bit] = 2*group[(i+1) % len(group)]+bit
    gamma = sp.zeros(24)
    for a in (0, 1):
        for y in range(12):
            gamma[12*a+y, 12*a+(y ^ 1)] = 1
    for y, z in enumerate(sigma):
        gamma[y, 12+z] = gamma[12+z, y] = 1
    return gamma


def report():
    # All own active patterns, no producer seed. These check the exact new identity.
    histogram = Counter()
    for pattern in two_star_catalogue():
        network = line_network(pattern['gamma'])
        histogram[len(network['components'])] += 1
    fixtures = []
    for c in range(1, 7):
        network = line_network(fixture_line(c))
        assert len(network['components']) == c
        assert network['M8'].rank() == 23-c
        potential = sp.zeros(24, 9)
        for j in range(9):
            for a in (0, 1):
                potential[12*a+j, j] = 1
                potential[12*a+11, j] = -1
        q = network['L8']*potential
        for target_rank in (8, 9):
            target = sp.diag(*([1]*target_rank+[0]*(9-target_rank)))
            d8 = 64*potential.T*network['L8']*potential+target
            reduced = grounded_schur(network, q, d8)
            assert reduced['odd_rank_gain'] == target_rank
            assert sp.Matrix(reduced['schur']) == target
            fixtures.append(dict(components=c, desired_schur_rank=target_rank,
                                 tree_product=reduced['tree_product'], result='PASS'))
    imbalance = sp.zeros(24, 9)
    imbalance[0, 0] = imbalance[12, 0] = 1
    rejected = grounded_schur(network, imbalance, sp.eye(9))
    assert rejected['status'] == 'COMPONENT_SOURCE_IMBALANCE_T_NOT_PSD'
    return dict(status='EXACT_WEIGHTED_NETWORK_REDUCTION_ODD9_STILL_OPEN',
        line_formula='8T_X=L8-u*u^T; L8=8(2I-Gamma_X)+3(I-F)+(I-M)+(I-FM).',
        notation=dict(F='Swap the two central letters0 and1.', M='Swap each outer letter with its mate.',
                      u='Twelve+1 coefficients on star0, twelve-1 on star1.'),
        proof=[
            'Gamma_X is the union of two perfect matchings: one within the stars and one between the stars. Thus2I-Gamma_X is a graph Laplacian. F,M,FM are fixed-point-free involutions, so L8 is a weighted graph Laplacian, with positive conductances8,3,1,1 (add weights when edges coincide).',
            'The exact geometry gives8T_X=L8-u*u^T. Also L8*u=24u, u^T*u=24, and every network component has zero sum of u. Subtracting u*u^T removes exactly this eigenmode. The remaining kernel consists of the c component indicators, hence rankT_X=23-c.',
            'Let f_y=e_{2y}-e_{3y}, y=4,...,13. Their sum belongs to the span of X_l modulo the known star2-minus-star3 kernel. Choose P=[e_0-e_9,...,e_8-e_9] to span the coefficient-sum-zero subspace. These nine combinations represent the whole possible odd rank gain.',
            'The root-letter incidence of F_odd*P is zero, hence K*F_odd*P=0. Put q=Gamma[X_l,:]*F_odd*P and d8=8P^T F_odd^T(3I-Gamma)F_odd P. Exact central-star counts give u^Tq=0. Positivity additionally forces each column of q to sum to zero on every network component.',
            'Ground one vertex per component. The positive definite integer matrix G is the grounded principal submatrix of L8, of size24-c. With q_g its grounded rows, the exact odd Schur matrix is S9=d8-64q_g^T G^(-1)q_g. The missing u mode causes no correction since u^Tq=0. Its rank is precisely the odd gain beyond X_l.',
            'The integer bordered matrix B=[[G,-8q_g],[-8q_g^T,d8]] has size33-c and detB=detG*detS9. detG is the product of weighted spanning-tree counts of the components. Under the producer hypothesis T>=0, S9 is PSD, so ODD9 is equivalent to detB>0. detB=0 produces an exact additional odd relation.',
            'This is a new explicit potential/energy formulation. It does not establish strict positivity for all admissible four-star structures; U positivity and C2 have not yet been used to force it.'],
        single_line_checks=dict(own_patterns=122, component_histogram=dict(histogram)),
        schur_fixtures=fixtures,
        component_imbalance_fixture='PASS: a new algebraic source violates a component sum while remaining perpendicular to u; the PSD obstruction is detected.',
        fixture_scope='The twelve bordered fixtures are algebraic Gram matrices with prescribed Schur rank8 or9, not Conway borders. They test the reduction and zero-determinant branch, not ODD9.',
        limitations=['ODD9 remains open; no universal determinant lower bound is proved.',
                     'No peer graph, rank, positivity certificate or automorphism group was re-audited.',
                     'Finite matrix dimension is not an affordable enumeration bound for all choices of its entries.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', help='Optional producer adjacency; default uses our algebraic fixtures only.')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.input:
        data = json.loads(Path(args.input).read_text(encoding='utf-8-sig'))
        gamma = data.get('gamma', data.get('adjacency'))
        if gamma is None:
            gamma = sp.zeros(44)
            for i, j in data['edges']:
                gamma[i, j] = gamma[j, i] = 1
        result = reduce_border(gamma, data['labels'])
    else:
        result = report()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k in ('status', 'single_line_checks', 'schur_fixtures', 'odd_rank_gain', 'schur_determinant', 'limitations')}))
