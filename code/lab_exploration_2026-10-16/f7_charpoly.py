"""Which eigenvalues of the label graph feed the balanced 7-adic drop (exploration, LAB 16/10/2026).
V_inf = {h : B Gamma_S^j h = 0 for all j} is the largest Gamma_S-invariant subspace of the balanced space ker B; balanced
eigenvectors of Gamma_S are the eigenvectors of Gamma_S on V_inf.  We factor the characteristic polynomial of Gamma_S on
V_inf over Q and list the factors f with f(3) = 0 mod 7 (3 = -4 mod 7), with the mod-7 balanced kernel dimension
b7 = dim ker_7 [Gamma_S - 3I ; B] for comparison.
usage: python f7_charpoly.py <block json> [...]"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f7_kernel_look import load  # noqa: E402
from f7_classform import rref_mod  # noqa: E402

x = sp.symbols("x")
for path in sys.argv[1:]:
    S, E = load(path)
    n = len(S)
    G = sp.Matrix(n, n, lambda i, j: 1 if i != j and frozenset((S[i], S[j])) in E else 0)
    B = sp.Matrix([[1 if r in l else 0 for l in S] for r in range(14)])
    stack = B
    cur = B
    while True:
        cur = cur * G
        new = stack.col_join(cur)
        if new.rank() == stack.rank():
            break
        stack = new
    V = stack.nullspace()
    d = len(V)
    Vm = sp.Matrix.hstack(*V) if V else sp.zeros(n, 0)
    # matrix of Gamma_S on V_inf: G Vm = Vm C
    C = (Vm.T * Vm).LUsolve(Vm.T * G * Vm) if d else sp.zeros(0, 0)
    assert (G * Vm - Vm * C).is_zero_matrix
    cp = sp.factor_list(C.charpoly(x).as_expr()) if d else (1, [])
    b7 = 44 - len(rref_mod([[int(v) for v in row] for row in (G - 3 * sp.eye(n)).col_join(B).tolist()], 7)[0])
    print("%s: dim V_inf = %d, b7 = %d" % (path.replace("\\", "/").split("/")[-1], d, b7))
    for f, m in cp[1]:
        p = sp.Poly(f, x)
        hit = int(p.eval(3)) % 7 == 0
        r7 = 0
        if hit:  # multiplicity of 3 as a root of f mod 7
            q = sp.Poly(p.as_expr(), x, modulus=7)
            while q.degree() > 0 and q.eval(3) == 0:
                q = sp.quo(q, sp.Poly(x - 3, x, modulus=7))
                r7 += 1
        print("    %s ^%d %s" % (sp.sstr(f), m, ("  <- f(3) = 0 mod 7 (root mult %d)" % r7) if hit else ""))
