"""Synthetic test of the depth-7 rule at a prime p where the far lattice is unimodular (LAB, NOTE_ORDRE2 §2.5).

Claim (P, corrected 20/10 after a failed first version that used the unit part of det Pi_XX): L a rank-8 lattice,
unimodular at an odd prime p, Pi the orthogonal projector on L (x) Q, X a set of 7 coordinates with
v_p(det Pi_XX) = 1.  Then (-det(L) * d0 | p) = +1, where d0 = discriminant of the rank-6 form Pi_XX mod p
(det of any nonsingular 6 x 6 principal minor mod p).  The first version, with u = det(Pi_XX)/p, is reported too.
(Reason: Pi_XX = Gram of 7 vectors of L (x) Z_p; the rank-6 unimodular part N_0 splits off, its complement C in L is a
unimodular plane of determinant det(L)/det(N_0), and C must represent p * unit, i.e. be isotropic mod p.)
Control: the opposite sign (det(L) * u | p) should be +1 only about half of the time.
usage: python o2_hasse7.py <seed> <samples> [pmax]"""
import json
import random
import sys
from fractions import Fraction

import sympy as sp


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def main():
    seed, samples = int(sys.argv[1]), int(sys.argv[2])
    pmax = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    rng = random.Random(seed)
    B = sp.Matrix(60, 8, lambda i, j: rng.randrange(-3, 4))
    G = B.T * B
    dG = int(G.det())
    Pi = B * G.inv() * B.T
    primes = [p for p in sp.primerange(3, pmax) if dG % p]
    ok = bad = ctrl_plus = tested = 0
    old_ok = 0
    for _ in range(samples):
        X = rng.sample(range(60), 7)
        d = Pi.extract(X, X).det()
        d = Fraction(int(sp.fraction(d)[0]), int(sp.fraction(d)[1]))
        if d == 0:
            continue
        for p in primes:
            if d.numerator % p == 0 and (d.numerator // p) % p != 0:
                tested += 1
                u = (d.numerator // p) * pow(d.denominator, -1, p) % p
                old_ok += legendre(-dG * u, p) == 1
                sub = Pi.extract(X, X)
                Mp = [[(int(sp.fraction(sub[i, j])[0]) * pow(int(sp.fraction(sub[i, j])[1]), -1, p)) % p
                       for j in range(7)] for i in range(7)]
                d0 = None
                for drop in range(7):
                    idx = [t for t in range(7) if t != drop]
                    m6 = sp.Matrix([[Mp[i][j] for j in idx] for i in idx])
                    dd = int(m6.det()) % p
                    if dd:
                        d0 = dd
                        break
                if d0 is None:
                    continue
                if legendre(-dG * d0, p) == 1:
                    ok += 1
                else:
                    bad += 1
                ctrl_plus += legendre(dG * d0, p) == 1
    print(json.dumps({"seed": seed, "det G": dG, "tests (X, p) with v_p(det Pi_XX) = 1": tested,
                      "rule (-det L * d0 | p) = +1 holds": ok, "rule fails": bad,
                      "control (det L * d0 | p) = +1": ctrl_plus, "first version (u = det/p) holds": old_ok}))


if __name__ == "__main__":
    main()
