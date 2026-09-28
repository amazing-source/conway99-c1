# CHECK (exact linear algebra, no solver): the A-invariant spans found for J1a (v) and (iii).
# Basis order (v): [H=h1|star, s=hexagon sign vector, D=d on zeros]; columns = images under A.
import sympy as sp
Mv = sp.Matrix([[-2, -1, -3],
                [-4, -2,  6],
                [-2,  1, -1]])
print('(v) charpoly:', sp.factor(Mv.charpoly().as_expr()))
print('(v) rank(M+4I) =', (Mv + 4*sp.eye(3)).rank(), ' rank(M-3I) =', (Mv - 3*sp.eye(3)).rank())
for vec, name in [((1, 2, 0), 'h1=H+2s'), ((0, -3, 1), 'u=D-3s'), ((-1, 2, 1), 'phi=-H+2s+D')]:
    x = sp.Matrix(vec)
    print('  ', name, '-> A x =', list(Mv * x), ' ratio', [sp.nsimplify((Mv*x)[i] / x[i]) if x[i] != 0 else None for i in range(3)])
# Gram check (vertex level): |H|^2=24, |s|^2=6, |D|^2=36, all mutually orthogonal (disjoint supports).
G = sp.diag(24, 6, 36)
for a, b, n in [((1,2,0),(1,2,0),'|h1|^2'), ((0,-3,1),(0,-3,1),'|u|^2'), ((1,2,0),(0,-3,1),'<h1,u>'), ((-1,2,1),(-1,2,1),'|phi|^2')]:
    print('  ', n, '=', (sp.Matrix(a).T * G * sp.Matrix(b))[0])
# symmetry check: A symmetric => G*M must be symmetric (self-adjointness on the span)
print('(v) G*M symmetric:', (G*Mv - (G*Mv).T) == sp.zeros(3))
# (iii): basis [H, s, D, G, iota], with |H|^2=24, |s|^2=6, |D|^2=32, |G|^2 = sum of (y_d - y_g)^2 over roots, |iota|^2=4.
Mi = sp.Matrix([[-2, -1, -3, 0, 0],
                [-4, -2,  6, 0, 0],
                [-2,  1, -1, 0, 0],
                [ 0,  0, -1, 0, 1],
                [-2,  1,  0, 12, -1]])
print('(iii) charpoly:', sp.factor(Mi.charpoly().as_expr()))
print('(iii) rank(M+4I) =', (Mi + 4*sp.eye(5)).rank(), ' rank(M-3I) =', (Mi - 3*sp.eye(5)).rank())
