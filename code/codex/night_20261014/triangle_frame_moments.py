"""Exact Schur-product trace inequalities for the 231 triangle vectors.

Derived directly from SRG(99,14,1,2); no previous research files are read.
Only rational symbolic arithmetic is used.
"""
from itertools import combinations_with_replacement
from pathlib import Path
import json
import sympy as s


def derive():
    t = s.symbols('t', real=True)
    counts = [1,18,32-t,144+3*t,36-3*t,t]
    # Relations: diagonal, intersecting, disjoint with j=0,1,2,3 cross edges.
    I = [1,0,0,0,0,0]
    L = [0,1,0,0,0,0]
    L2 = [18,5,0,1,2,3]
    p18 = [s.Rational(1,231)]*6
    p0 = [(21*i+4*l-l2+1)/s.Integer(21) for i,l,l2 in zip(I,L,L2)]
    p7 = [(l2+3*l-s.Rational(18,11))/70 for l,l2 in zip(L,L2)]
    pm3 = [i-a-b-c for i,a,b,c in zip(I,p18,p0,p7)]
    projectors = {'constant':p18,'zero':p0,'seven':p7,'minus_three':pm3}
    output = {}
    for names in combinations_with_replacement(projectors,3):
        value = s.factor(sum(counts[i]*s.prod(projectors[n][i] for n in names) for i in range(6)))
        output[','.join(names)] = str(value)
    # u_x=sqrt(63) P_-4 e_x, q_T=sqrt(7) P_-4 1_T.
    # Their inner products are respectively (28,-8,1), (4,0,1,0,-1,-2),
    # and (4,-2,1) for incidence / one neighbour / no neighbour.
    vertex_cube_norm = 99*(28**3+14*(-8)**3+84)
    mixed_cube_inner = 231*(3*4**3+36*(-2)**3+60)
    triangle_cube_norm = s.factor(231*sum(counts[i]*(21*p0[i])**3 for i in range(6)))
    norm_lower_bound = s.Rational(mixed_cube_inner**2,vertex_cube_norm)
    mean_bound = s.solve(triangle_cube_norm-norm_lower_bound,t)[0]
    prism_pair_bound = int(s.floor(231*mean_bound/2))
    assert vertex_cube_norm == 1471932 and mixed_cube_inner == -8316
    assert s.expand(triangle_cube_norm-1386*(10-t)) == 0
    assert mean_bound == s.Rational(588,59) and prism_pair_bound == 1151
    # Verify the spectral projector polynomials independently in Q[z]/m(z).
    z = s.symbols('z')
    eigenvalues = (18,0,7,-3)
    minimal = s.prod(z-a for a in eigenvalues)
    poly_j = 231*z*(z-7)*(z+3)/(18*(18-7)*(18+3))
    polys = [poly_j/231,(21+4*z-z*z+poly_j)/21,
             (z*z+3*z-s.Rational(18,11)*poly_j)/70]
    polys.append(1-sum(polys))
    for i,p in enumerate(polys):
        for j,q in enumerate(polys):
            assert s.rem(s.expand(p*q-(p if i==j else 0)),minimal,z)==0
    return dict(projectors={k:list(map(str,v)) for k,v in projectors.items()},
                counts=list(map(str,counts)), trace_per_triangle=output,
                cubic_tensors=dict(vertex_cube_norm=vertex_cube_norm,
                                   mixed_inner_product=mixed_cube_inner,
                                   triangle_cube_norm=str(triangle_cube_norm),
                                   norm_lower_bound=str(norm_lower_bound),
                                   mean_prism_degree_upper_bound=str(mean_bound),
                                   unordered_prism_upper_bound=prism_pair_bound,
                                   some_triangle_has_at_most=9),
                explanation='Every trace expression must be >=0 for t equal to the average number of disjoint triangles joined by three edges. The mixed cubic tensor inequality strengthens this to t<=588/59<10.')


if __name__ == '__main__':
    out = Path('data/codex_night_20261014/triangle_frame_moments.json')
    out.parent.mkdir(parents=True,exist_ok=True)
    report = derive()
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Exact projector and cubic tensor checks: PASS')
    print('Mean prism degree <=',report['cubic_tensors']['mean_prism_degree_upper_bound'])
    print('Unordered prisms <=',report['cubic_tensors']['unordered_prism_upper_bound'])
    print('A base triangle with at most 9 prism partners always exists.')
