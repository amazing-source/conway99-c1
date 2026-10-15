"""Profiles of ker T_S on Y (outer labels of stars 2,3) and on Y' (outer labels of stars 0,1); exact annihilators.
usage: python profile_annihilator.py <json>"""
import json, sys
from fractions import Fraction as F
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
from exact_lin import rref, nullspace
f = sys.argv[1]
d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
E = set()
for a, b in d["edges"]: E.add((a, b)); E.add((b, a))
T = [[(3 if i == j else 0) - (1 if (i, j) in E else 0) - F(int(round(8 * kval(S[i], S[j]))), 8) for j in range(n)] for i in range(n)]
Kb = nullspace(T)
print(f, "nullity", len(Kb))
OUT = list(range(4, 14))
for side, (s1, s2) in (("Y (stars 2,3)", (2, 3)), ("Y' (stars 0,1)", (0, 1))):
    Ylab = [frozenset((s1, y)) for y in OUT] + [frozenset((s2, y)) for y in OUT]
    P = [[v[idx[s]] for s in Ylab] for v in Kb]
    Rp, piv = rref(P)
    ann = nullspace(Rp)
    print(side, ": profile dim", len(Rp), " annihilator dim", len(ann))
    names = ["%d%s" % (s1, format(y, 'x')) for y in OUT] + ["%d%s" % (s2, format(y, 'x')) for y in OUT]
    print("   profiles (RREF):")
    print("      " + " ".join("%4s" % nm for nm in names))
    for row in Rp:
        print("      " + " ".join("%4s" % (str(x) if x != 0 else ".") for x in row))
