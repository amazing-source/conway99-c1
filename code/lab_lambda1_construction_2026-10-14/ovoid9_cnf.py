"""3-ovoid CNF of P(W(9),x0): one variable per point, exactly 3 of the 9 points on each of the 891 lines (14/10/2026).
usage: python ovoid9_cnf.py <gq9.json> <out.cnf>"""
import itertools, json, sys
G = json.load(open(sys.argv[1])); lines = G["lines"]
cls = []
for L in lines:
    for sub in itertools.combinations(L, 4):
        cls.append([-(p + 1) for p in sub])
    for sub in itertools.combinations(L, 7):
        cls.append([p + 1 for p in sub])
with open(sys.argv[2], "w") as fh:
    fh.write("p cnf 729 %d\n" % len(cls))
    for c in cls:
        fh.write(" ".join(map(str, c)) + " 0\n")
print("3-ovoid CNF: 729 variables, %d clauses" % len(cls))
