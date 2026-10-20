"""rho = 0 (rank 37 type) version of o2_corank.py: L unimodular at 7 (rank 8), H = 7 Pi, first layer empty, s = Pi_XX mod 7.
Claim (P): for 7 coordinates with s of corank 1, C = complement of the non-degenerate part s0 (dim 6) in L/7 (a plane,
det C = det L * det s0 mod squares).  If C is anisotropic, v_7(det H_XX) - 6 is odd and >= 3, i.e. v_7(det Pi_XX) is even
and >= 2; if C is hyperbolic, no condition.
usage: python o2_corank0.py <seed> <samples> [chi(det L) wanted: 1|-1]"""
import itertools
import json
import random
import sys
from fractions import Fraction

import numpy as np
import sympy as sp

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from o2_parity import rank_mod, chi, v7  # noqa: E402

P = 7


def main():
    seed, samples = int(sys.argv[1]), int(sys.argv[2])
    want = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    rng = random.Random(seed)
    while True:
        B = np.array([[rng.randrange(-3, 4) for _ in range(8)] for _ in range(60)], dtype=np.int64)
        G = sp.Matrix(B.tolist()).T * sp.Matrix(B.tolist())
        dG = int(G.det())
        if dG % P and (want == 0 or chi(dG) == want):
            break
    chi_L = chi(dG)
    Bs = sp.Matrix(B.tolist())
    Hs = 7 * Bs * G.inv() * Bs.T
    H = [[Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1])) for v in Hs.row(i)] for i in range(60)]
    hist = {"C aniso": {}, "C hyper": {}}
    n_cor1 = 0
    for _ in range(samples):
        X = rng.sample(range(60), 7)
        Hx = [[H[i][j] for j in X] for i in X]
        Sm = [[((v / 7).numerator * pow((v / 7).denominator, -1, P)) % P for v in row] for row in Hx]   # Pi mod 7
        if rank_mod(Sm) != 6:
            continue
        n_cor1 += 1
        d0 = None
        for idx in itertools.combinations(range(7), 6):
            dd = int(sp.Matrix([[Sm[i][j] for j in idx] for i in idx]).det()) % P
            if dd:
                d0 = dd
                break
        aniso = (chi(-1) * chi_L * chi(d0) == -1)
        det = sp.Matrix(Hx).det()
        det = Fraction(int(sp.fraction(det)[0]), int(sp.fraction(det)[1]))
        if det == 0:
            continue
        e = v7(det) - 6
        key = "C aniso" if aniso else "C hyper"
        hist[key][e] = hist[key].get(e, 0) + 1
    print(json.dumps({"seed": seed, "rho": 0, "chi(det L)": chi_L, "corank-1 s": n_cor1,
                      "v7(det) - 6, C anisotropic": {str(a): b for a, b in sorted(hist["C aniso"].items())},
                      "v7(det) - 6, C hyperbolic": {str(a): b for a, b in sorted(hist["C hyper"].items())}}))


if __name__ == "__main__":
    main()
