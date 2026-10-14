"""Farkas certificates for the infeasible cases of theta7_lp.lp_exact, checked exactly and independently of the
simplex: a certificate is (lam, mu) with mu >= 0, lam^T E + mu^T G = 0 and lam.e + mu.g > 0; then no a satisfies
E a = e and G a >= g. The script prints the constraints that carry positive weight.

usage: python theta7_cert.py b lines(0/1) roots(0/1) [nmax] [a3low]
"""
import sys
from fractions import Fraction

import exact_lp as X
import theta7_lp as T

b, lines, roots = int(sys.argv[1]), bool(int(sys.argv[2])), bool(int(sys.argv[3]))
nmax = int(sys.argv[4]) if len(sys.argv) > 4 else 45
a3low = int(sys.argv[5]) if len(sys.argv) > 5 else 0      # optional: a_3 >= a3low (NOTE_NIGHT 19)
s = -Fraction(7) ** (11 - b // 2) if b <= 22 else -Fraction(1, 7 ** (b // 2 - 11))
MA = T.MA_ALL[:nmax]
MWB = [[s * x for x in row] for row in T.MW_ALL[:nmax]]
E, e, G, g, names_e, names_g = [], [], [], [], [], []
E.append(MA[0]); e.append(1); names_e.append("a_0 = 1")
E.append(MWB[0]); e.append(1); names_e.append("c_0 = 1")
for n in range(1, 7):
    E.append(MWB[n]); e.append(0); names_e.append("c_%d = 0" % n)
for n in range(1, nmax):
    G.append(MA[n]); g.append(0); names_g.append("a_%d >= 0" % n)
    if n >= 7:
        G.append(MWB[n]); g.append(0); names_g.append("c_%d >= 0" % n)
if lines:
    G.append(MA[2]); g.append(462); names_g.append("a_2 >= 462")
if roots:
    for m in range(1, (nmax - 1) // 7 + 1):
        G.append([c - a for a, c in zip(MA[m], MWB[7 * m])]); g.append(0); names_g.append("c_%d >= a_%d" % (7 * m, m))
if a3low:
    G.append(MA[3]); g.append(a3low); names_g.append("a_3 >= %d" % a3low)
ne, ng = len(E), len(G)
# unknowns: lam (ne, free), mu (ng, >= 0).  Equalities: sum lam_i E_i + sum mu_j G_j = 0 (15 coordinates).
EQ = [[E[i][k] for i in range(ne)] + [G[j][k] for j in range(ng)] for k in range(15)]
eq = [0] * 15
INE = [[0] * ne + [int(j == t) for j in range(ng)] for t in range(ng)]
ine = [0] * ng
INE.append([Fraction(v) for v in e] + [Fraction(v) for v in g])
ine.append(1)
ok, x = X.feasible(EQ, eq, INE, ine, ne + ng)
if not ok:
    print("b=%d lines=%s roots=%s: no certificate (the programme is feasible)" % (b, lines, roots))
    sys.exit(0)
lam, mu = x[:ne], x[ne:]
# independent exact verification
assert all(m >= 0 for m in mu)
for k in range(15):
    assert sum(lam[i] * Fraction(E[i][k]) for i in range(ne)) + sum(mu[j] * Fraction(G[j][k]) for j in range(ng)) == 0
val = sum(lam[i] * Fraction(e[i]) for i in range(ne)) + sum(mu[j] * Fraction(g[j]) for j in range(ng))
assert val > 0
print("b=%d lines=%s roots=%s nmax=%d: INFEASIBLE, certificate verified exactly (value %s)" % (b, lines, roots, nmax, float(val)))
used = [(names_g[j], float(mu[j])) for j in range(ng) if mu[j] != 0]
print("inequalities with positive weight:", used)
