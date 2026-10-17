"""Exact check of the co-Heawood equitable partition (exploration, LAB 17/10/2026).
Claim (derived by projecting the support indicator onto the eigenspaces 14, 3, -4 of srg(99,14,1,2)): for an integral
-4-eigenvector of norm 14 (co-Heawood), the partition support (14) / linked (70) / free (15) is equitable with quotient
[[4,10,0],[2,9,3],[0,14,0]].  This script redoes the eigenspace computation with exact fractions only (no graph needed):
given |supp| = 14, A s = 4 s + 2 1_L (each support vertex: 4 support nbrs; linked: 2; free: 0), it solves for the
components of s and 1_L, 1_F and returns the forced neighbour counts per class."""
from fractions import Fraction as Fr

n, k = 99, 14
# s = a 1 + s3 + s4 (orthogonal, eigenvalues 14, 3, -4); |s|^2 = 14, s^T A s = 56
a = Fr(14, n)
# unknown norms x = |s3|^2, y = |s4|^2 :  n a^2 + x + y = 14 ; 14 n a^2 + 3x - 4y = 56
na2 = n * a * a
x = (Fr(56) - 14 * na2 + 4 * (Fr(14) - na2)) / 7
y = Fr(14) - na2 - x
print("|s_3|^2 =", x, " |s_-4|^2 =", y)
# 1_L = (A s - 4 s)/2 = ((14-4) a / 2) 1 + ((3-4)/2) s3 + ((-4-4)/2) s4
cL = ((14 - 4) * a / 2, Fr(-1, 2), Fr(-4))
cF = (1 - a - cL[0], -1 - cL[1], -1 - cL[2])      # 1_F = 1 - s - 1_L
normF = n * cF[0] ** 2 + cF[1] ** 2 * x + cF[2] ** 2 * y
print("1_L = %s 1 + %s s3 + %s s4 ; 1_F = %s 1 + %s s3 + %s s4 ; |1_F|^2 = %s" % (cL + cF + (normF,)))
# value of (s3, s4) at a vertex of each class from s(u) and 1_L(u):  s(u) = a + s3 + s4,  1_L(u) = cL0 + cL1 s3 + cL2 s4
for name, su, Lu in (("support", 1, 0), ("linked", 0, 1), ("free", 0, 0)):
    # solve s3 + s4 = su - a ; cL1 s3 + cL2 s4 = Lu - cL0
    det = cL[2] - cL[1]
    s4 = ((Lu - cL[0]) - cL[1] * (su - a)) / det
    s3 = (su - a) - s4
    nbr = lambda c: k * c[0] + 3 * c[1] * s3 - 4 * c[2] * s4      # (A v)(u) for v = c0 1 + c1 s3 + c2 s4
    supp_n = k * a + 3 * s3 - 4 * s4
    print("%-8s: support nbrs %s, linked nbrs %s, free nbrs %s" % (name, supp_n, nbr(cL), nbr(cF)))
