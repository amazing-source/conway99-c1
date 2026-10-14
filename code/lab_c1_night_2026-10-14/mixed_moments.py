"""Mixed moments across the two eigenspaces of srg(99,14,1,2).

In the (-4)-space: (u_x,u_y) = 28, -8, 1; (q_T,u_x) = 4, -2, 1; (q_T,q_T') = 4, 0 (meeting), 1 - j (disjoint, j edges).
In the 3-space (u'_x = sqrt(77) E_3 e_x, q'_T = u'_a + u'_b + u'_c): (u',u') = 42, 9, -2; (q',u') = 60, 5, -6;
(q',q') = 180, 70 (meeting), 11 j - 18.
For exponents (a,b): S = sum_T q_T^a x q'_T^b, V = sum_x u_x^a x u'_x^b. Cauchy-Schwarz |S|^2 |V|^2 >= <S,V>^2 with
|S|^2 = 231 (c0 + c1 pbar): prints the resulting bound on the average prism number pbar.
"""
from fractions import Fraction as Fr


def P(x, k):
    return Fr(1) if k == 0 else Fr(x) ** k


for a in range(0, 8):
    for b in range(0, 8):
        if a + b < 2 or a + b > 9:
            continue
        def perline(p):
            n = {0: 32 - p, 1: 144 + 3 * p, 2: 36 - 3 * p, 3: p}
            return P(4, a) * P(180, b) + 18 * P(0, a) * P(70, b) + sum(n[j] * P(1 - j, a) * P(11 * j - 18, b) for j in range(4))
        c0 = perline(Fr(0))
        c1 = perline(Fr(1)) - c0
        SV = 231 * (3 * P(4, a) * P(60, b) + 36 * P(-2, a) * P(5, b) + 60 * P(1, a) * P(-6, b))
        VV = 99 * (P(28, a) * P(42, b) + 14 * P(-8, a) * P(9, b) + 84 * P(1, a) * P(-2, b))
        if VV == 0:
            print("a=%d b=%d  V = 0 (and <S,V> = %s)" % (a, b, SV))
            continue
        rhs = SV * SV / VV / 231          # c0 + c1 pbar >= rhs
        if c1 == 0:
            verdict = "no pbar (holds: %s)" % (c0 >= rhs)
        else:
            bound = (rhs - c0) / c1
            verdict = ("pbar <= %.4f" if c1 < 0 else "pbar >= %.4f") % float(bound)
        print("a=%d b=%d  %s" % (a, b, verdict))
