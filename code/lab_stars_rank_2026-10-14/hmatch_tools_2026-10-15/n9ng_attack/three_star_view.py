"""Three-star kernel (stars a, mate(a), b) of a four-star structure: dimension vs 2 + c, and the mixed relations.
usage: python three_star_view.py <json> <a> <b>   (a, b in 0..3, b not a or mate(a))"""
import json, sys
from fractions import Fraction as F
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
from exact_lin import rref, nullspace, rank
f = sys.argv[1]; a = int(sys.argv[2]); b = int(sys.argv[3])
d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
E = set()
for p, q in d["edges"]: E.add((p, q)); E.add((q, p))
T = [[(3 if i == j else 0) - (1 if (i, j) in E else 0) - F(int(round(8 * kval(S[i], S[j]))), 8) for j in range(n)] for i in range(n)]
def ker(stars):
    lab = [i for i in range(n) if S[i] & set(stars)]
    return lab, nullspace([[T[i][j] for j in lab] for i in lab])
labX, NX = ker((a, a ^ 1))
lab3, N3 = ker((a, a ^ 1, b))
print(f, "stars %d,%d + %d: two-star nullity %d (c = %d), three-star nullity %d" % (a, a ^ 1, b, len(NX), len(NX) - 1, len(N3)))
# profile of the three-star kernel on the outer labels of star b
outer = [i for i in lab3 if not (S[i] & {a, a ^ 1})]
P = [[v[lab3.index(i)] for i in outer] for v in N3]
Rp, piv = rref(P)
print("profile dim on the 10 outer labels of star %d: %d" % (b, len(Rp)))
names = ["".join(format(c, 'x') for c in sorted(S[i])) for i in outer]
print("      " + " ".join("%5s" % nm for nm in names))
for row in Rp:
    print("      " + " ".join("%5s" % (str(x) if x != 0 else ".") for x in row))
