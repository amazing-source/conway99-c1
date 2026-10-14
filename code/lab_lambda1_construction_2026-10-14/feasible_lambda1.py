"""Feasible parameter sets srg(v,k,1,mu), v <= VMAX (14/10/2026). lambda = 1 means: every edge in exactly one triangle,
so the graph is the collinearity graph of a partial quadrangle PQ(2,t,mu) with k = 2(t+1) and mu <= t+1 = k/2.
Conditions checked: v = 1 + k + k(k-2)/mu integral; integral eigenvalues (or the conference case); integral
multiplicities; Krein conditions; absolute bound. Exact arithmetic (fractions, integer square roots).
usage: python feasible_lambda1.py <VMAX>"""
import math
import sys
from fractions import Fraction as Fr

VMAX = int(sys.argv[1])
out = []
for k in range(4, 2 * VMAX, 2):
    for mu in range(2, k // 2 + 1):
        if (k * (k - 2)) % mu:
            continue
        v = 1 + k + k * (k - 2) // mu
        if v > VMAX:
            continue
        lam = 1
        D = (lam - mu) ** 2 + 4 * (k - mu)
        sq = math.isqrt(D)
        if sq * sq != D:
            if not (k == 2 * mu and lam == mu - 1):
                continue
            out.append((v, k, lam, mu, "conference"))
            continue
        if (lam - mu + sq) % 2:
            continue
        r = (lam - mu + sq) // 2
        s = (lam - mu - sq) // 2
        f2 = Fr((v - 1) * (-s) - k, r - s)
        g2 = Fr((v - 1) * r + k, r - s)
        if f2.denominator != 1 or g2.denominator != 1 or f2 <= 0 or g2 <= 0:
            continue
        f, g = int(f2), int(g2)
        krein1 = (r + 1) * (k + r + 2 * r * s) <= (k + r) * (s + 1) ** 2
        krein2 = (s + 1) * (k + s + 2 * r * s) <= (k + s) * (r + 1) ** 2
        absb = v <= f * (f + 3) // 2 and v <= g * (g + 3) // 2
        if not (krein1 and krein2 and absb):
            continue
        out.append((v, k, lam, mu, "r=%d^%d s=%d^%d t=%d" % (r, f, s, g, k // 2 - 1)))
for row in sorted(out):
    print("srg(%d,%d,%d,%d)  %s" % row)
print("%d feasible parameter sets with lambda = 1 and v <= %d" % (len(out), VMAX))
