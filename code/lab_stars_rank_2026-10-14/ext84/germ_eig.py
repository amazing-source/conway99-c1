"""Exact eigenspaces of T_SS for theta = 3, 5, 7: rational bases (LLL-reduced integer vectors), supports, star sums,
and whether Gamma v = 0, K v = 0 (theta = 3 <=> (Gamma + K) v = 0)."""
import sys, json
import numpy as np
import sympy as sp
sys.path.insert(0, ".")
from modp_germ import t8, geometry

def intbasis(vecs):
    M = sp.Matrix.hstack(*vecs).T
    M = M * sp.ilcm(*[sp.fraction(x)[1] for x in M])
    from sympy.matrices.normalforms import hermite_normal_form
    rows = [M.row(i) for i in range(M.rows)]
    return [r / sp.igcd(*[int(x) for x in r]) for r in rows]

for f in sys.argv[1:]:
    d = json.load(open(f))
    labels = [tuple(sorted(l)) for l in d["labels"]]
    M8, G = t8(labels, d["edges"])
    B, P = geometry(labels)
    T = sp.Matrix(M8.tolist()) / 8
    Gm = sp.Matrix(G.tolist())
    Km = 3 * sp.eye(44) - Gm - T
    print("==", f.split("/")[-1].split("\\")[-1])
    for th in (3, 5, 7):
        E = (T - th * sp.eye(44)).nullspace()
        if not E:
            continue
        vs = intbasis(E)
        print("  theta=%d dim %d" % (th, len(vs)))
        for v in vs:
            vv = [int(x) for x in v]
            supp = [(labels[i], vv[i]) for i in range(44) if vv[i]]
            Bv = (B @ np.array(vv)).tolist()
            Gv = (Gm * sp.Matrix(vv)).T.tolist()[0]
            Kv = (Km * sp.Matrix(vv)).T.tolist()[0]
            print("    |supp| %d, star sums %s, Gamma v = 0: %s, K v = 0: %s" % (len(supp), Bv, all(x == 0 for x in Gv), all(x == 0 for x in Kv)))
            print("      ", supp if len(supp) <= 16 else supp[:16] + ["..."])
