"""Synthetic test of the corank-1 rule at 7 far vertices (LAB, NOTE_ORDRE2_7ADIQUE §2.3 (iv), 20/10/2026).

Model as in o2_parity.py: L of type U_m + 7 U''_rho at 7 (m = 8 - rho), M = L^#(7) = U''^{-1} + U^{-1}(7); H = 7 Pi.
For 7 coordinates X with rank_7 H_XX = rho (first layer full): s = H/7 on K = ker(H_XX mod 7) (dim 7 - rho).
Claim (P): if s has corank 1, let s0 be its non-degenerate part (dim 6 - rho) and C the complement of s0 in U (a plane,
det C = det U * det s0 mod squares).  If C is anisotropic (chi(-det C) = -1), then v_7(det H_XX) - (6 - rho) is odd and
>= 3; if C is hyperbolic there is no condition.  (rho = 6: s0 is empty, C = U_2, and this is (C43).)
Output: for corank-1 samples, histogram of v_7(det H_XX) - (6 - rho), split by the predicted type of C.
usage: python o2_corank.py <seed> <rho> <samples> [aniso|hyper|any]"""
import json
import random
import sys
from fractions import Fraction

import sympy as sp

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from o2_parity import build, rank_mod, kernel_mod, chi, v7  # noqa: E402

P = 7


def main():
    seed, rho, samples = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    cls = sys.argv[4] if len(sys.argv) > 4 else "any"
    rng = random.Random(seed)
    while True:
        B, G, chi_m = build(rng, rho, cls)
        if sp.multiplicity(7, G.det()) == rho:
            break
    Bs = sp.Matrix(B.tolist())
    Hs = 7 * Bs * G.inv() * Bs.T
    H = [[Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1])) for v in Hs.row(i)] for i in range(60)]
    m = 8 - rho
    hist = {"C aniso": {}, "C hyper": {}}
    n_full = n_cor1 = 0
    for _ in range(samples):
        X = rng.sample(range(60), 7)
        Hx = [[H[i][j] for j in X] for i in X]
        Hm = [[(v.numerator * pow(v.denominator, -1, P)) % P for v in row] for row in Hx]
        if rank_mod(Hm) != rho:
            continue
        n_full += 1
        Kb = kernel_mod(Hm)                                   # vectors y with H y = 0 mod 7 (H symmetric)
        Hsp = sp.Matrix(Hx)
        Kmat = sp.Matrix([list(map(int, y)) for y in Kb]).T     # 7 x (7 - rho), integer lift
        S = (Kmat.T * Hsp * Kmat) / 7
        Sm = [[(int(sp.fraction(S[i, j])[0]) * pow(int(sp.fraction(S[i, j])[1]), -1, P)) % P
               for j in range(S.shape[1])] for i in range(S.shape[0])]
        rs = rank_mod(Sm)
        if rs != (7 - rho) - 1:
            continue
        n_cor1 += 1
        dim = 7 - rho
        d0 = 1
        if dim - 1 > 0:
            d0 = None
            import itertools
            for idx in itertools.combinations(range(dim), dim - 1):
                dd = int(sp.Matrix([[Sm[i][j] for j in idx] for i in idx]).det()) % P
                if dd:
                    d0 = dd
                    break
            if d0 is None:
                continue
        # C = complement of s0 in U: det C = det U * det s0 (mod squares); anisotropic iff chi(-det C) = -1
        aniso = (chi(-1) * chi_m * chi(d0) == -1)
        det = Hsp.det()
        det = Fraction(int(sp.fraction(det)[0]), int(sp.fraction(det)[1]))
        if det == 0:
            continue
        e = v7(det) - (6 - rho)
        key = "C aniso" if aniso else "C hyper"
        hist[key][e] = hist[key].get(e, 0) + 1
    print(json.dumps({"seed": seed, "rho": rho, "chi(det U)": chi_m, "first layer full": n_full, "corank-1 s": n_cor1,
                      "v7(det) - (6 - rho), C anisotropic": {str(a): b for a, b in sorted(hist["C aniso"].items())},
                      "v7(det) - (6 - rho), C hyperbolic": {str(a): b for a, b in sorted(hist["C hyper"].items())}}))


if __name__ == "__main__":
    main()
