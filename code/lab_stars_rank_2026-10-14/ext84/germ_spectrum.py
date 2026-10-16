"""Exact spectral anatomy of a germ: char poly of T_SS factored over Q, multiplicities, pseudo-determinant, integer
kernel lattice determinant, and the identity class(Lambda_S) = class(pdet(T_SS) * det_std(N_S)) (8^rank removed)."""
import sys, json
import numpy as np
import sympy as sp
sys.path.insert(0, ".")
from modp_germ import t8, LABELS84

def sqclass(q):
    q = sp.Rational(q)
    num, den = sp.fraction(q)
    n = int(num) * int(den)
    sign = -1 if n < 0 else 1
    n = abs(n)
    f = sp.factorint(n)
    return sign, sorted(p for p, e in f.items() if e % 2)

for f in sys.argv[1:]:
    d = json.load(open(f))
    labels = [tuple(sorted(l)) for l in d["labels"]]
    M8, G = t8(labels, d["edges"])
    T = sp.Matrix(M8.tolist()) / 8
    x = sp.symbols("x")
    cp = T.charpoly(x).as_expr()
    fac = sp.factor_list(sp.Poly(cp, x))
    print("==", f.split("/")[-1])
    pdet = sp.Integer(1)
    for poly, mult in fac[1]:
        P = sp.Poly(poly, x)
        if P.degree() == 1 and P.eval(0) == 0:
            print("   eigenvalue 0  mult %d" % mult)
            continue
        roots_prod = (-1) ** P.degree() * P.eval(0) / P.LC()
        pdet *= roots_prod ** mult
        if P.degree() == 1:
            print("   eigenvalue %s  mult %d" % (sp.nsimplify(-P.eval(0) / P.LC()), mult))
        else:
            print("   irreducible deg %d mult %d  norm %s  (%s)" % (P.degree(), mult, roots_prod, P.as_expr() if P.degree() <= 4 else "..."))
    # integer kernel lattice
    ker = T.nullspace()
    Kq = sp.Matrix.hstack(*ker)
    # make integral and saturate: use HNF / Smith via sympy
    Kq = Kq * sp.ilcm(*[sp.fraction(v)[1] for v in Kq])
    Kint = sp.Matrix(Kq).applyfunc(int)
    from sympy.matrices.normalforms import smith_normal_form
    # saturation: N_S = Q-span intersect Z^44; det_std(N) = det(K^T K) / (product of invariant factors)^2
    snf = smith_normal_form(Kint.T, domain=sp.ZZ)
    inv = [snf[i, i] for i in range(min(snf.shape)) if snf[i, i] != 0]
    gram = Kint.T * Kint
    detN = gram.det() / (sp.prod(inv) ** 2)
    print("   rank %d, nullity %d, pdet(T_SS) = %s" % (44 - len(ker), len(ker), sp.factorint(abs(sp.fraction(pdet)[0])), ), "/", sp.factorint(sp.fraction(pdet)[1]))
    print("   det_std(N_S) =", sp.factorint(detN))
    print("   class(pdet) =", sqclass(pdet), " class(det N_S) =", sqclass(detN), " class(product) =", sqclass(pdet * detN))
