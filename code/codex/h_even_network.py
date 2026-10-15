"""The h-even block is a difference of two connected weighted Laplacians.

Answer to LAB790: its rank is a spectral multiplicity, not a count of
components in the natural network. All calculations use fixed geometry and
one new algebraic fixture; no producer border is read or audited.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_profile_join import LABELS
from three_star_column_domains import k8


def geometry():
    index = {p: i for i, p in enumerate(LABELS)}
    orbits = [((0, 2), (1, 3)), ((0, 3), (1, 2))]
    orbits += [((0, y), (1, y)) for y in range(4, 14)]
    orbits += [((2, y), (3, y)) for y in range(4, 14)]
    basis = sp.zeros(44, 22)
    for j, orbit in enumerate(orbits):
        for p in orbit:
            basis[index[p], j] = 1
    assert basis.T*basis == 2*sp.eye(22)
    k = sp.Matrix(44, 44, lambda i, j: sp.Rational(k8(LABELS[i], LABELS[j]), 8))
    kp = basis.T*k*basis/2
    r0 = kp+sp.ones(22)/2
    assert all(value >= 0 and (4*value).q == 1 for value in r0)
    w = sp.Matrix([2, 2]+[1]*20)
    v = sp.Matrix([0, 0]+[1]*10+[-1]*10)
    demand = sp.Matrix([4, 4]+[6]*20)
    assert r0*w == 3*w+12*sp.ones(22, 1)-demand
    assert (3*sp.eye(22)-kp)*v == -2*v
    for y in range(10):
        for z in range(10):
            assert kp[2+y, 12+z] == -sp.Rational(1, 2)+sp.Rational(3, 4)*int(y == z)+sp.Rational(1, 4)*int(z == (y ^ 1))
            assert kp[2+y, 2+z] == sp.Rational(3, 4)*int(y == z)+sp.Rational(1, 4)*int(z == (y ^ 1))
        assert all(kp[i, 2+y] == kp[i, 12+y] == 0 for i in range(2))
    # The fixed conductances alone already connect all22 vertices.
    assert all(r0[0, j] > 0 for j in range(1, 22))
    return dict(orbits=orbits, basis=basis, K=kp, R0=r0, w=w, v=v, demand=demand)


def laplacian(conductances):
    return sp.diag(*[sum(conductances.row(i)) for i in range(conductances.rows)])-conductances


def report():
    g = geometry()
    w, v, d = g['w'], g['v'], g['demand']
    dw = sp.diag(*w)
    # A new rational fixture meeting the two required aggregate star equations.
    # Its entries are not half-integral and it is not asserted to be a graph.
    gamma = d*d.T/(w.dot(d))-v*v.T/10
    assert all(value >= 0 for value in gamma)
    assert gamma*w == d and gamma*v == -2*v
    a = 3*sp.eye(22)-gamma-g['K']
    r = gamma+g['R0']
    lr = laplacian(dw*r*dw)
    lk = 24*dw-w*w.T
    assert a*w == sp.zeros(22, 1) and a*v == sp.zeros(22, 1)
    assert dw*a*dw == lr-lk/2
    assert a == 3*sp.eye(22)-r+sp.ones(22)/2
    # Clear denominators before exact elimination; avoid expression growth.
    rank_a = DomainMatrix.from_Matrix(a).rank()
    rank_h = DomainMatrix.from_Matrix(3*sp.eye(22)-r).rank()
    assert rank_a == 20 and rank_h == 21
    spectrum = DomainMatrix.from_Matrix(a).charpoly()
    x = sp.Symbol('x')
    polynomial = sp.Poly.from_list([sp.sympify(c) for c in spectrum], x)
    factors = sp.factor_list(polynomial.as_expr())[1]
    assert all(sp.degree(factor, x) == 1 for factor, _ in factors)
    eigenvalues = [(-sp.Poly(factor, x).nth(0)/sp.Poly(factor, x).nth(1), multiplicity)
                   for factor, multiplicity in factors]
    assert all(value >= 0 for value, _ in eigenvalues)
    fixed_conductance_support = sum(1 for i, j in combinations(range(22), 2) if g['R0'][i, j] > 0)
    return dict(status='H_EVEN_RANK_IS_SPECTRAL_MULTIPLICITY_NOT_NETWORK_COMPONENTS',
        h='(0 1)(2 3), outer letters fixed; h need not preserve Gamma.',
        orbits=g['orbits'], K_plus=[[str(x) for x in g['K'].row(i)] for i in range(22)],
        nonnegative_fixed_geometry_times4=(4*g['R0']).tolist(),
        fixed_conductance_graph=dict(vertices=22, edges=int(fixed_conductance_support), components=1,
                                     reason='The first overlap orbit has a strictly positive fixed conductance to every other orbit.'),
        formula=dict(G='Gamma_plus=Q^T Gamma Q/2 in the orthonormal orbit basis.',
                     R='Gamma_plus+K_plus+J/2, entrywise nonnegative.',
                     A='3I-R+J/2.', w=[2, 2]+[1]*20, v=[0, 0]+[1]*10+[-1]*10,
                     weighted_row_equation='R*w=3*w+12*1.',
                     laplacian='D_w*A*D_w=L_R-(1/2)L_K, with edge conductances w_i*w_j*R_ij and w_i*w_j respectively.',
                     L_K='24D_w-w*w^T.',
                     rank10='Equivalent, under A PSD, to generalized eigenvalue1/2 of (L_R,L_K) having multiplicity11 on1-perp.',
                     integer_rank10='4R is nonnegative integral; rankA=10 iff eigenvalue12 of4R has multiplicity11. Under A PSD its other eigenvalues consist of one above12 and ten below12.'),
        proof=[
            'The even star vectors are s_l=(1,1,1^10,0^10) and s_m=(1,1,0^10,1^10). C1 gives A*s_l=A*s_m=0. Their sum is w and their difference is v. The weighted degree equation for R follows from A*w=0 and sum(w)=24.',
            'The fixed geometric part R0=K_plus+J/2 is nonnegative and already connected, independently of the variable adjacencies. Thus the component count of its Laplacian is always one; it cannot encode the changing rank of A.',
            'Conjugate by D_w. The weighted degree equation gives D_w*A*D_w=L_R-L_K/2 exactly. L_K is positive definite on1-perp. Under A PSD, every generalized eigenvalue of the pair on that subspace is at least1/2; each equality adds a kernel dimension, besides the constant vector. Hence nullityA=1+mult(1/2).',
            'Alternatively H=3I-R=A-J/2 has kernel ker(A) intersect1-perp: Hx=0 implies0=w^T Hx=-12*1^T x, and the converse is immediate. Thus nullityH=nullityA-1. Under A PSD, H has exactly one negative eigenvalue (test w), at most one because the update has rank one, and rankA positive eigenvalues. This gives the stated eigenvalue multiplicity for4R.',
            'The matrix A itself necessarily has positive off-diagonal entries. All O-L and O-R entries are nonpositive. On L_y,R_y, A=-Gamma_plus-1/4<0. From A*v=A*w=0, each cross-row satisfies sum_z A[L_y,R_z]=-sum_i A[L_y,O_i]>=0. Hence each L row, and each R row, contains a strictly positive cross entry: at least10 positive off-diagonal pairs in total.',
            'These positive entries can only occur at distinct outer letters: for z=y^1 the entry is1/4-Gamma_plus, and for z different from y,y^1 it is1/2-Gamma_plus. Gamma_plus is half-integral for a binary border, so every strictly positive one corresponds to an empty original2x2 adjacency block.',
            'The direct analogue of adding the one known star-difference mode also fails to produce an ordinary Laplacian: A+alpha*v*v^T, alpha>0, has positive entries inside L. For any L_y, its aggregate adjacency towards O+L sums to2; among the eight non-mate L_z, at most four can have nonzero half-integral adjacency. At a zero entry, K_plus is zero, so the update creates the positive entry alpha. Positive diagonal rescaling cannot change its sign. This only rules out this canonical one-mode construction, not all possible representations.'],
        own_fixture=dict(scope='Rational nonnegative aggregate adjacency satisfying the two even-star equations, not a binary/half-integral graph or a full C1/C2 border.',
                         A_psd=True, rank_A=rank_a, rank_3I_minus_R=rank_h, congruence_identity='PASS',
                         exact_spectrum=[dict(value=str(value), multiplicity=multiplicity) for value, multiplicity in eigenvalues]),
        consequences='The proposed component-count shortcut is unavailable in this natural network. RankA=10 remains a strong spectral multiplicity condition. This does not refute H-INV or ODD9, nor prove rankA=10 for nullity14.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = report()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, default=str)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'fixed_conductance_graph', 'formula', 'own_fixture', 'consequences')}, default=str))
