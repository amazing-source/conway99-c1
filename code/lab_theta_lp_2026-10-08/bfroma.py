"""C1, lab session. The dual shell counts b_1..b_6 written as affine functions of (a_7, ..., a_13), exactly, for each rank.
  python bfroma.py <N>        prints   D * b_k = const + sum_n coef_n a_n   with integer coefficients (D a power of 7)."""
import sys, math
from fractions import Fraction as Fr
import theta_lp as T
T.selfcheck()
for d in (42, 40, 38, 36, 34):
    A, B = T.family(d)
    # change of parameters: a_n (n = 7..13) = A[n] affine in beta; invert on the 7 x 7 linear part
    M = [[A[n][k] for k in range(1, 8)] + [Fr(int(i == j)) for j in range(7)] for i, n in enumerate(range(7, 14))]
    for c in range(7):
        p = next(i for i in range(c, 7) if M[i][c] != 0); M[c], M[p] = M[p], M[c]; q = M[c][c]; M[c] = [x / q for x in M[c]]
        for i in range(7):
            if i != c and M[i][c] != 0: f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[c])]
    inv = [row[7:] for row in M]                                         # beta_k = sum_i inv[k][i] (a_(7+i) - A[7+i][0])
    print("d = %d (r = %d):" % (d, d + 1), flush=True)
    for kb in range(1, 7):
        f = B[kb]; coef = [sum(f[k + 1] * inv[k][i] for k in range(7)) for i in range(7)]
        const = f[0] - sum(coef[i] * A[7 + i][0] for i in range(7))
        den = 1
        for x in coef + [const]: den = den * x.denominator // math.gcd(den, x.denominator)
        print("   %d * b_%d = %d %s" % (den, kb, int(const * den), " ".join("%+d a_%d" % (int(coef[i] * den), 7 + i) for i in range(7) if coef[i])), flush=True)
