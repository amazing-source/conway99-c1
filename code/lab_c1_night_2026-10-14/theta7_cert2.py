"""Exact Farkas certificates (checked independently of the simplex) for the theta programme of NOTE_NIGHT 19 with
the rigorous shell bounds. Constraint spec on the command line, e.g.
   python theta7_cert2.py 26 "a2>=462,a4>=14970,c7<=7920" [nmax]
Always included: a_0 = 1, c_0 = 1, c_1..c_6 = 0, a_n >= 0, c_n >= 0, c_7m >= a_m."""
import sys
from fractions import Fraction
import exact_lp as X
import theta7_lp as T

b = int(sys.argv[1]); spec = sys.argv[2]; nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 40
s = -Fraction(7) ** (11 - b // 2) if b <= 22 else -Fraction(1, 7 ** (b // 2 - 11))
MA = T.MA_ALL[:nmax]
MWB = [[s * x for x in row] for row in T.MW_ALL[:nmax]]
E, e, G, g, names = [MA[0], MWB[0]], [1, 1], [], [], []
for n in range(1, 7):
    E.append(MWB[n]); e.append(0)
for n in range(1, nmax):
    G.append(MA[n]); g.append(0); names.append("a_%d>=0" % n)
    if n >= 7:
        G.append(MWB[n]); g.append(0); names.append("c_%d>=0" % n)
for m in range(1, (nmax - 1) // 7 + 1):
    G.append([c - a for a, c in zip(MA[m], MWB[7 * m])]); g.append(0); names.append("c_%d>=a_%d" % (7 * m, m))
for item in spec.split(","):
    if not item:
        continue
    op = ">=" if ">=" in item else "<="
    lhs, rhs = item.split(op)
    row = MA[int(lhs[1:])] if lhs[0] == "a" else MWB[int(lhs[1:])]
    if op == ">=":
        G.append(row); g.append(int(rhs))
    else:
        G.append([-x for x in row]); g.append(-int(rhs))
    names.append(item)
ne, ng = len(E), len(G)
EQ = [[E[i][k] for i in range(ne)] + [G[j][k] for j in range(ng)] for k in range(15)]
INE = [[0] * ne + [int(j == t) for j in range(ng)] for t in range(ng)]
INE.append([Fraction(v) for v in e] + [Fraction(v) for v in g])
ok, x = X.feasible(EQ, [0] * 15, INE, [0] * ng + [1], ne + ng)
if not ok:
    print("b=%d [%s]: feasible (no certificate)" % (b, spec)); sys.exit(0)
lam, mu = x[:ne], x[ne:]
assert all(m >= 0 for m in mu)
for k in range(15):
    assert sum(lam[i] * Fraction(E[i][k]) for i in range(ne)) + sum(mu[j] * Fraction(G[j][k]) for j in range(ng)) == 0
val = sum(lam[i] * Fraction(e[i]) for i in range(ne)) + sum(mu[j] * Fraction(g[j]) for j in range(ng))
assert val > 0
print("b=%d [%s] nmax=%d: INFEASIBLE, certificate verified exactly; weights on: %s"
      % (b, spec, nmax, [names[j] for j in range(ng) if mu[j] != 0]))
