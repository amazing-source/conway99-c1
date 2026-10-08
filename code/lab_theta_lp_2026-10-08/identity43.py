"""C1, lab session. Check, in my own coordinates, Codex's identity at r = 43 (d = 42):
    2 a_8 + 16 a_9 + a_13 = 2632 + 7 a_7 + 49 b_1 + 7 a_10 + 2 a_11 + a_12        (identically on the 7-parameter family),
and print the analogous relation among a_7..a_13 and b_1 for the other ranks (exact, normalised to integer coefficients).
  python identity43.py <N>"""
import sys, math
from fractions import Fraction as Fr
import theta_lp as T
T.selfcheck()
A, B = T.family(42)
lhs = T.add(T.add(T.sc(A[8], 2), T.sc(A[9], 16)), A[13])
rhs = T.add(T.add(T.add(T.add(T.add(T.aff(2632), T.sc(A[7], 7)), T.sc(B[1], 49)), T.sc(A[10], 7)), T.sc(A[11], 2)), A[12])
print("d = 42: identity holds identically on the family:", lhs == rhs, flush=True)
for d in (42, 40, 38, 36, 34):
    A, B = T.family(d)
    forms = [A[n] for n in range(7, 14)] + [B[1]]                        # 8 affine forms in 7 parameters: one relation
    # solve sum_i w_i * coef(form_i) = 0 on the 7 parameters
    M = [[forms[i][k] for i in range(8)] for k in range(1, 8)]           # 7 x 8
    piv = []; r = 0
    for c in range(8):
        p = next((i for i in range(r, 7) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; q = M[r][c]; M[r] = [x / q for x in M[r]]
        for i in range(7):
            if i != r and M[i][c] != 0: f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = [c for c in range(8) if c not in piv]; assert len(free) == 1
    w = [Fr(0)] * 8; w[free[0]] = Fr(1)
    for i, c in enumerate(piv): w[c] = -M[i][free[0]]
    den = 1
    for x in w: den = den * x.denominator // math.gcd(den, x.denominator)
    w = [x * den for x in w]; g = 0
    for x in w: g = math.gcd(g, int(x))
    w = [int(x) // g for x in w]
    if w[2] < 0: w = [-x for x in w]
    const = -sum(wi * f[0] for wi, f in zip(w, forms))
    names = ["a_%d" % n for n in range(7, 14)] + ["b_1"]
    print("d = %d (r = %d): %s = %s" % (d, d + 1, " ".join("%+d %s" % (wi, nm) for wi, nm in zip(w, names) if wi), const), flush=True)
